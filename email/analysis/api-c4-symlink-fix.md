# API Analysis: C4 - Attachment Download Symlink Race Fix

**Date**: 2026-04-28
**Reviewer**: API Architect Agent
**Task**: Review backend fix for TOCTOU vulnerability in `download_attachment()`

---

## Summary

The `download_attachment()` method in `imap/client.py` has a Time-Of-Check-Time-Of-Use (TOCTOU) vulnerability where workspace confinement validation occurs before directory creation and file writing. An attacker with local access could create symlinks between the validation check and the actual write operation, potentially escaping the workspace confinement and writing files to arbitrary locations.

---

## Vulnerability Analysis

### Current Implementation Flow

```python
# Lines 293-304: Validation phase
output_path = Path(output_dir).resolve()  # Resolves symlinks at T0
workspace = DEFAULT_WORKSPACE.resolve()

try:
    output_path.relative_to(workspace)    # Check at T0
except ValueError:
    raise ValueError(...)

# Lines 334-337: Write phase (potentially T1, T2, T3)
output_path.mkdir(parents=True, exist_ok=True)  # At T1
file_path = output_path / final_filename        # At T2
with open(file_path, "wb") as f:                # At T3
    f.write(payload)
```

### Attack Vector

The vulnerability exists because:

1. **Symlink resolution happens once** - `resolve()` is called at line 294, capturing the path state at that moment
2. **Gap between check and write** - Directory creation (line 334) and file write (line 336) happen after the validation
3. **No post-write verification** - The final written file's actual location is never verified

**Attack scenario**:

```
T0: resolve() shows /tmp/email-workspace/downloads is within workspace
T1: Attacker creates symlink: ln -s /etc /tmp/email-workspace/downloads
T2: mkdir() follows symlink, writes to /etc/
T3: File written to /etc/evil.bin
```

### Why `resolve()` Is Insufficient

`Path.resolve()` resolves symlinks at call time, but:

- **Non-existent paths**: If `output_path` doesn't exist yet, `resolve()` cannot resolve components that don't exist
- **Intermediate symlinks**: Symlinks in parent directories created after `resolve()` but before `mkdir(parents=True)` are not caught
- **Race window**: The classic TOCTOU race - check passes, symlink created, write escapes

---

## Backend Design Recommendations

### Option 1: Post-Write Verification (Recommended)

Verify the actual written file location after the write operation:

```python
async def download_attachment(
    self,
    message_id: str,
    folder: str,
    filename: str,
    output_dir: str,
) -> str:
    """Download an attachment with workspace confinement."""
    workspace = DEFAULT_WORKSPACE.resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    # Sanitize filename
    safe_filename = os.path.basename(filename)
    hashed_prefix = hashlib.sha256(filename.encode()).hexdigest()[:16]
    final_filename = f"{hashed_prefix}_{safe_filename}"

    async with self._operation_lock:
        client = await self.connect()
        # ... fetch message logic ...

        for item in data:
            if isinstance(item, tuple) and len(item) == 2:
                raw_message = item[1]
                if isinstance(raw_message, bytes):
                    msg = email.message_from_bytes(raw_message)
                    for part in msg.walk():
                        if part.get_filename() == filename:
                            payload = part.get_payload(decode=True)
                            if payload:
                                # Create directory without following symlinks
                                output_path = Path(output_dir)
                                output_path.mkdir(parents=True, exist_ok=True)

                                file_path = output_path / final_filename

                                # Write file
                                with open(file_path, "wb") as f:
                                    f.write(payload)

                                # POST-WRITE VERIFICATION
                                real_path = os.path.realpath(file_path)
                                real_workspace = os.path.realpath(workspace)

                                if not os.path.commonpath([real_path, real_workspace]) == real_workspace:
                                    # Remove the escaped file
                                    os.unlink(file_path)
                                    raise SecurityError(
                                        f"Write escaped workspace: file written to {real_path}"
                                    )

                                log_attachment_download(self.account.name, filename, real_path)
                                return real_path
```

**Pros**:
- Catches all symlink-based escapes
- Works even if symlinks created after initial check
- Atomic detection and cleanup

**Cons**:
- Brief window where file exists outside workspace (before cleanup)
- Additional filesystem operations

### Option 2: Safe Directory Creation with O_NOFOLLOW

Use `os.open()` with `O_NOFOLLOW` for the final component:

```python
import os
import errno

def safe_write_file(base_dir: Path, filename: str, content: bytes) -> str:
    """Write file safely without following symlinks for the final component."""
    # Resolve the base directory (must exist)
    real_base = os.path.realpath(base_dir)

    # Create subdirectories safely
    target_dir = Path(real_base)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Final path - DO NOT use resolve() here
    final_path = target_dir / filename

    # Open with O_NOFOLLOW to prevent symlink attacks on final component
    try:
        fd = os.open(
            str(final_path),
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o644
        )
        try:
            os.write(fd, content)
        finally:
            os.close(fd)
    except OSError as e:
        if e.errno == errno.ELOOP:
            raise SecurityError(f"Symlink detected at {final_path}")
        raise

    # Verify final location
    real_final = os.path.realpath(final_path)
    if not real_final.startswith(real_base):
        os.unlink(final_path)
        raise SecurityError(f"Write escaped workspace")

    return real_final
```

**Pros**:
- Prevents symlink at final component
- More secure by design

**Cons**:
- `O_NOFOLLOW` only protects the final component, not intermediate directories
- Requires careful path manipulation
- More complex implementation

### Option 3: Use Secure Temporary File + Atomic Move

Write to a secure temp location, then move only if destination is safe:

```python
import tempfile
import shutil

def safe_download_attachment(
    self,
    message_id: str,
    folder: str,
    filename: str,
    output_dir: str,
) -> str:
    """Download attachment using secure temp file pattern."""
    workspace = DEFAULT_WORKSPACE.resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    # Sanitize filename
    safe_filename = os.path.basename(filename)
    hashed_prefix = hashlib.sha256(filename.encode()).hexdigest()[:16]
    final_filename = f"{hashed_prefix}_{safe_filename}"

    # Write to secure temp location first
    with tempfile.NamedTemporaryFile(
        mode='wb',
        dir=workspace,  # Secure: temp file created inside workspace
        delete=False,
        prefix='attachment-',
        suffix='.tmp'
    ) as tmp_file:
        tmp_path = Path(tmp_file.name)
        # ... fetch and write attachment content ...
        tmp_file.write(payload)

    # Verify destination is safe BEFORE moving
    dest_dir = Path(output_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    real_dest_dir = os.path.realpath(dest_dir)
    real_workspace = os.path.realpath(workspace)

    if not os.path.commonpath([real_dest_dir, real_workspace]) == real_workspace:
        tmp_path.unlink()  # Clean up temp file
        raise SecurityError(f"Destination directory escapes workspace")

    # Atomic move
    final_path = dest_dir / final_filename
    shutil.move(str(tmp_path), str(final_path))

    # Final verification
    real_final = os.path.realpath(final_path)
    if not os.path.commonpath([real_final, real_workspace]) == real_workspace:
        final_path.unlink()  # Clean up moved file
        raise SecurityError(f"Write escaped workspace")

    return str(real_final)
```

**Pros**:
- Temp file always created securely inside workspace
- Move operation is atomic
- Multiple verification points

**Cons**:
- Requires double the disk space briefly
- More complex flow

---

## Recommended Solution

**Use Option 1 (Post-Write Verification)** as the primary fix:

1. **Minimal code change** - Adds verification without restructuring the entire method
2. **Clear error handling** - Detects and cleans up escaped writes
3. **Defense in depth** - Works alongside existing protections

### Implementation Details

```python
# Add to imap/client.py

import os
from ..errors import SecurityError  # Or use existing exception

class SecurityError(Exception):
    """Raised when a security constraint is violated."""
    pass

async def download_attachment(
    self,
    message_id: str,
    folder: str,
    filename: str,
    output_dir: str,
    _workspace: Path | None = None,  # For testing
) -> str:
    """
    Download an attachment from a message with workspace confinement.

    Raises:
        SecurityError: If write would escape workspace confinement
        FileNotFoundError: If attachment not found in message
    """
    workspace = (_workspace or DEFAULT_WORKSPACE).resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    # Sanitize filename - remove path separators
    safe_filename = os.path.basename(filename)
    # Hash for uniqueness and additional safety
    hashed_prefix = hashlib.sha256(filename.encode()).hexdigest()[:16]
    final_filename = f"{hashed_prefix}_{safe_filename}"

    async with self._operation_lock:
        client = await self.connect()
        status, data = await client.select(folder)
        if status != "OK":
            raise RuntimeError(f"Failed to select folder {folder}: {status}")
        self._selected_folder = folder

        status, data = await client.fetch(message_id, "(BODY.PEEK[])")
        if status != "OK":
            raise RuntimeError("Failed to fetch message")

        for item in data:
            if isinstance(item, tuple) and len(item) == 2:
                raw_message = item[1]
                if isinstance(raw_message, bytes):
                    msg = email.message_from_bytes(raw_message)
                    for part in msg.walk():
                        if part.get_filename() == filename:
                            payload = part.get_payload(decode=True)
                            if payload:
                                # Create output directory
                                output_path = Path(output_dir)
                                output_path.mkdir(parents=True, exist_ok=True)

                                file_path = output_path / final_filename

                                # Write the file
                                with open(file_path, "wb") as f:
                                    f.write(payload)

                                # POST-WRITE VERIFICATION
                                # Use os.path.realpath to resolve any symlinks
                                real_path = os.path.realpath(file_path)
                                real_workspace = os.path.realpath(workspace)

                                # Verify file is within workspace
                                try:
                                    Path(real_path).relative_to(real_workspace)
                                except ValueError:
                                    # SECURITY VIOLATION: Clean up and raise
                                    try:
                                        os.unlink(file_path)
                                    except OSError:
                                        pass  # Best effort cleanup
                                    raise SecurityError(
                                        f"Attachment download escaped workspace confinement. "
                                        f"File location: {real_path}, Workspace: {real_workspace}"
                                    )

                                log_attachment_download(
                                    self.account.name,
                                    filename,
                                    real_path  # Log the real location
                                )
                                return str(real_path)

        raise FileNotFoundError(f"Attachment not found in message")
```

---

## Interface Changes

### New Exception Type

```python
# In src/email_mcp/errors.py (or appropriate location)

class SecurityError(Exception):
    """
    Raised when a security constraint is violated.

    This exception indicates an attempted security violation that was
    detected and prevented. It should not expose sensitive information
    in the message.
    """
    def __init__(self, message: str):
        # Sanitize message for external consumption
        self._internal_message = message
        super().__init__("Security constraint violated")

    @property
    def internal_message(self) -> str:
        """Internal message for logging only."""
        return self._internal_message
```

### MCP Tool Interface

No changes to the MCP tool signature. The error is mapped to a generic error message:

```python
# In server.py

@mcp.tool()
async def download_attachment(
    account: str,
    message_id: str,
    filename: str,
    output_dir: str = "downloads",
    folder: str = "INBOX",
) -> dict:
    """
    Download an attachment from an email message.

    Returns the path to the downloaded file within the workspace.
    """
    try:
        # ... existing code ...
    except SecurityError as e:
        # Log detailed message internally
        logger.error(f"Security violation: {e.internal_message}")
        # Return generic error to client
        raise ToolError("Download failed: security constraint violated")
```

---

## Backward Compatibility

### Breaking Changes

**None**. The fix is entirely internal.

### Behavioral Changes

| Aspect | Before | After |
|--------|--------|-------|
| Success path | Returns path | Returns realpath (symlinks resolved) |
| Symlink escape | File written outside workspace | File deleted, SecurityError raised |
| Error message | Generic error | Generic "security constraint violated" |

### Migration Path

No migration needed. Clients already using `download_attachment` will:

1. Receive the same response shape on success
2. See same error types (mapped from SecurityError)
3. Get realpath instead of potentially symlinked path (more accurate)

---

## Error Handling Approach

### Exception Hierarchy

```
Exception
├── SecurityError (NEW)
│   └── Raised for symlink escape attempts
├── FileNotFoundError
│   └── Attachment not found in message
└── RuntimeError
    └── IMAP protocol errors
```

### Error Response Format

Following RFC 7807 Problem Details:

```json
{
  "type": "https://api.email-mcp.local/errors/security-violation",
  "title": "Security Constraint Violated",
  "status": 403,
  "detail": "The requested operation was blocked for security reasons.",
  "instance": "/tools/download_attachment"
}
```

### Audit Logging

```python
# Log security violations for forensic analysis
logger.warning(
    "security.violation",
    extra={
        "operation": "download_attachment",
        "account": self.account.name,
        "attempted_path": file_path,
        "actual_path": real_path,
        "workspace": real_workspace,
    }
)
```

---

## Impact on Other Operations

### IMAP Operations

| Operation | Impact | Notes |
|-----------|--------|-------|
| `fetch_message()` | None | No filesystem writes |
| `list_folders()` | None | No filesystem writes |
| `search()` | None | No filesystem writes |
| `move_message()` | None | IMAP-only operations |
| `delete_message()` | None | IMAP-only operations |

### SMTP Operations

| Operation | Impact | Notes |
|-----------|--------|-------|
| `send_email()` | Similar vulnerability | Attachment uploads need same protection |
| `reply_email()` | Similar vulnerability | Attachment uploads need same protection |

### Recommendation

Apply similar post-write verification to SMTP attachment handling (M8, M10).

---

## Testing Requirements

### Unit Tests

```python
# tests/test_imap_client.py

import pytest
import os
import tempfile
from pathlib import Path

class TestDownloadAttachmentSecurity:
    """Test symlink race protection in download_attachment."""

    @pytest.mark.asyncio
    async def test_symlink_escape_detected_and_cleaned(self, tmp_path):
        """Verify symlink escape is detected and file is cleaned up."""
        # Setup: Create workspace and symlink target outside
        workspace = tmp_path / "workspace"
        outside = tmp_path / "outside"
        workspace.mkdir()
        outside.mkdir()

        # Create symlink in output dir pointing outside
        output_dir = workspace / "downloads"
        output_dir.mkdir()
        symlink_target = outside / "escaped.txt"
        (output_dir / "subdir").symlink_to(outside)

        # Attempt to download to symlinked location
        client = IMAPClient(...)  # Mock setup

        with pytest.raises(SecurityError):
            await client.download_attachment(
                message_id="1",
                folder="INBOX",
                filename="test.txt",
                output_dir=str(output_dir / "subdir"),
                _workspace=workspace,
            )

        # Verify no file was created outside workspace
        assert not (outside / "escaped.txt").exists()

    @pytest.mark.asyncio
    async def test_normal_download_succeeds(self, tmp_path):
        """Verify normal downloads work correctly."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        # ... normal download test ...
```

### Integration Tests

```python
# tests/integration/test_attachment_security.py

@pytest.mark.integration
async def test_rapid_symlink_attack():
    """
    Attempt to create symlink during download operation.
    This tests the TOCTOU fix under realistic attack conditions.
    """
    # ... integration test with real filesystem ...
```

---

## Action Items

1. **Implement SecurityError exception** in `errors.py` or appropriate module
2. **Update `download_attachment()`** with post-write verification
3. **Update `server.py`** to catch and handle SecurityError
4. **Add unit tests** for symlink escape detection
5. **Add integration tests** for TOCTOU race conditions
6. **Update TODO.md** to mark C4 as complete
7. **Consider applying same pattern to SMTP** (future work)

---

## References

- [CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition](https://cwe.mitre.org/data/definitions/367.html)
- [CWE-59: Improper Link Resolution Before File Access](https://cwe.mitre.org/data/definitions/59.html)
- [OWASP: Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [Python os.path.realpath documentation](https://docs.python.org/3/library/os.path.html#os.path.realpath)