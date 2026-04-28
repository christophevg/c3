# Security Analysis: C4 - Attachment Download Symlink Race Condition

**Date**: 2026-04-28
**Analyst**: Security Engineer Agent
**Severity**: Critical (P1)

---

## Executive Summary

The `download_attachment()` method in `imap/client.py:285-341` contains a **Critical** TOCTOU (Time-of-Check to Time-of-Use) vulnerability that allows attackers to bypass workspace confinement and write files to arbitrary locations outside the designated workspace.

---

## Vulnerability Details

**CVSS Score**: 9.1 (Critical)

**OWASP Category**: A05:2021 - Injection (Path Traversal)

**CWE References**:
- CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition
- CWE-22: Improper Limitation of a Pathname to a Restricted Directory

---

## Vulnerable Code Analysis

```python
# Lines 293-304: Check phase
output_path = Path(output_dir).resolve()  # Line 294
workspace = DEFAULT_WORKSPACE.resolve()   # Line 295

# Ensure workspace exists
workspace.mkdir(parents=True, exist_ok=True)  # Line 298

# Workspace confinement check
try:
    output_path.relative_to(workspace)  # Line 302 - CHECK
except ValueError:
    raise ValueError(f"output_dir must be within workspace: {workspace}")

# ... IMAP operations ...

# Lines 333-337: Use phase
output_path.mkdir(parents=True, exist_ok=True)  # Line 334 - USE
file_path = output_path / final_filename
with open(file_path, "wb") as f:  # Line 336-337 - WRITE
    f.write(payload)
```

---

## Attack Vector

The race condition exploits the window between validation (line 302) and file write (lines 336-337):

```
Timeline of Attack:

T0: Attacker prepares directory structure
    /tmp/email_workspace/downloads/

T1: Victim calls download_attachment() with output_dir="/tmp/email_workspace/downloads"

T2: Code validates output_path is within workspace (line 302) - PASSES

T3: [RACE WINDOW] Attacker replaces downloads with symlink:
    ln -sf /etc /tmp/email_workspace/downloads

T4: Code creates directory (line 334) - mkdir follows symlink

T5: Code writes file - written to /etc/<hashed_filename>_<basename>
```

---

## Specific Issues Identified

### Issue 1: Path.resolve() Follows Symlinks

`Path.resolve()` follows symlinks, meaning:
- If `output_path` contains a symlink, it resolves to the target
- Check passes if resolved path appears within workspace
- But actual write location could be outside workspace

### Issue 2: mkdir with exist_ok=True is Unsafe

`output_path.mkdir(parents=True, exist_ok=True)` (line 334):
- Does not fail if path is a symlink
- Creates directories through symlinks
- No atomic creation guarantee

### Issue 3: TOCTOU Between Check and Write

Time window between validation (line 302) and write (line 336):
- Multiple async operations occur (IMAP fetch)
- Attacker has significant time to create symlink
- No atomic "validate-and-write" operation

### Issue 4: Incomplete Path Validation

Code validates `output_path` but writes to `output_path / final_filename`:
- Should validate the final target path
- Filename could contain null bytes or other exploits

---

## STRIDE Analysis

| Category | Violated | Threat | Mitigation |
|----------|----------|--------|------------|
| Tampering | Integrity | Attacker can write arbitrary files outside workspace | Atomic path validation and write |
| Information Disclosure | Confidentiality | Could overwrite sensitive files | Proper workspace confinement |
| Elevation of Privilege | Authorization | Bypass workspace restrictions | Strict path canonicalization |

---

## Recommended Remediation

### Primary Fix: Atomic Path Validation with os.path.realpath()

Key changes:
1. Use `os.path.realpath()` to resolve symlinks before validation
2. Validate the FINAL target path, not just parent directory
3. Use `os.O_CREAT | os.O_EXCL` for atomic file creation
4. Re-validate after directory creation to catch TOCTOU attacks

### Implementation Code

```python
import os

async def download_attachment(
    self,
    message_id: str,
    folder: str,
    filename: str,
    output_dir: str,
) -> str:
    """Download an attachment with secure workspace confinement."""

    # 1. Sanitize filename
    safe_filename = os.path.basename(filename)
    if not safe_filename or safe_filename in ('.', '..'):
        raise ValueError("Invalid filename")

    # 2. Hash prefix for uniqueness
    hashed_prefix = hashlib.sha256(filename.encode()).hexdigest()[:16]
    final_filename = f"{hashed_prefix}_{safe_filename}"

    # 3. Resolve workspace to real path (no symlinks)
    workspace = Path(os.path.realpath(str(DEFAULT_WORKSPACE)))
    workspace.mkdir(parents=True, exist_ok=True)

    # 4. Resolve output_dir - handle non-existent paths
    output_path = Path(output_dir)
    if output_path.exists():
        real_output = Path(os.path.realpath(str(output_path)))
    else:
        # Find existing ancestor and resolve it
        existing = output_path
        while not existing.exists() and existing != existing.parent:
            existing = existing.parent
        real_existing = Path(os.path.realpath(str(existing)))
        rel = output_path.relative_to(existing)
        real_output = real_existing / rel

    # 5. Final target path
    final_path = real_output / final_filename

    # 6. Validate AFTER full resolution
    try:
        final_path.resolve().relative_to(workspace)
    except ValueError:
        raise ValueError(f"output_dir must be within workspace: {workspace}")

    # 7. Atomic directory creation with verification
    real_output.mkdir(parents=True, exist_ok=True)

    # Re-check after directory creation (handles TOCTOU)
    real_output_after = Path(os.path.realpath(str(real_output)))
    try:
        real_output_after.relative_to(workspace)
    except ValueError:
        raise ValueError("Security violation: path escaped workspace")

    # 8. Create file atomically with O_EXCL
    fd = None
    try:
        fd = os.open(
            str(final_path),
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            mode=0o644
        )

        # IMAP fetch operations...
        async with self._operation_lock:
            client = await self.connect()
            # ... fetch attachment ...
            os.write(fd, payload)

    finally:
        if fd is not None:
            os.close(fd)

    return str(final_path)
```

---

## Key Security Principles Applied

1. **Canonicalize Before Validate**: Use `os.path.realpath()` to resolve all symlinks before checking boundaries
2. **Validate the Final Target**: Check complete destination path, not just parent
3. **Atomic Operations**: Use `O_CREAT | O_EXCL` to atomically create files
4. **Defense in Depth**: Re-validate after directory creation to catch TOCTOU
5. **Fail-Safe Defaults**: Raise exceptions on any path ambiguity

---

## Additional Security Recommendations

### 1. Workspace Path Validation at Startup

```python
SENSITIVE_PATHS = ['/etc', '/root', '/home', '/var', '/usr', '/bin', '/sbin']
resolved_workspace = os.path.realpath(str(DEFAULT_WORKSPACE))
for sensitive in SENSITIVE_PATHS:
    if resolved_workspace.startswith(sensitive):
        raise RuntimeError(f"EMAIL_WORKSPACE cannot be under {sensitive}")
```

### 2. Symlink Detection Tests

```python
def test_symlink_in_output_path_rejected(self, temp_workspace):
    """Test symlinks in output path are rejected."""
    outside_dir = tempfile.mkdtemp()
    symlink_path = temp_workspace / "malicious_link"
    os.symlink(outside_dir, symlink_path)

    with pytest.raises(ValueError, match="workspace"):
        asyncio.run(client.download_attachment("1", "INBOX", "test.txt", str(symlink_path)))
```

---

## Summary

| Finding | Severity | Confidence |
|---------|----------|------------|
| TOCTOU race condition | Critical | High |
| Symlink bypass vulnerability | Critical | High |
| Non-atomic file creation | High | High |

**Recommended Priority**: P1 - Fix immediately before production deployment

---

## References

- [OWASP Path Traversal Prevention](https://owasp.org/www-community/attacks/Path_Traversal)
- [CWE-367: TOCTOU Race Condition](https://cwe.mitre.org/data/definitions/367.html)
- [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)