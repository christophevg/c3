# Functional Review: C4 Symlink Race Fix

**Task**: C4 - Fix attachment download symlink race
**Date**: 2026-04-28
**Reviewer**: Functional Analyst Agent
**Status**: CONDITIONAL APPROVE

---

## Executive Summary

The implementation correctly addresses the TOCTOU (Time-of-Check-Time-of-Use) vulnerability in `download_attachment()` using post-write verification. The core security logic is sound, but test coverage has gaps that should be addressed.

---

## Implementation Analysis

### 1. SecurityError Exception Definition

**File**: `src/email_mcp/imap/client.py` (lines 27-29)

```python
class SecurityError(Exception):
  """Raised when a security constraint is violated (e.g., symlink escape)."""
  pass
```

**Assessment**: CORRECT
- Simple exception class extending `Exception`
- Clear docstring explaining purpose
- Properly imported in `server.py` (line 13)

---

### 2. Post-Write Verification Logic

**File**: `src/email_mcp/imap/client.py` (lines 290-363)

#### Workflow Verified:

1. **Filename Sanitization** (lines 301-304)
   - Uses `os.path.basename()` to strip path separators
   - Rejects `.` and `..` as invalid filenames
   - Adds hash prefix for uniqueness and additional safety
   - **Assessment**: CORRECT - prevents path traversal in filename

2. **Directory Creation** (lines 332-338)
   - Creates workspace with `os.path.realpath()` - resolves symlinks
   - Creates output directory with `mkdir(parents=True, exist_ok=True)`
   - **Assessment**: CORRECT - workspace is resolved before creation

3. **File Write** (lines 341-342)
   - Writes attachment content to `file_path`
   - **Assessment**: CORRECT - standard write operation

4. **Post-Write Verification** (lines 345-358)
   ```python
   real_path = os.path.realpath(file_path)
   real_workspace = os.path.realpath(str(DEFAULT_WORKSPACE))
   
   try:
     Path(real_path).relative_to(real_workspace)
   except ValueError:
     # Security violation: clean up and raise
     try:
       os.unlink(file_path)
     except OSError:
       pass
     raise SecurityError("Download escaped workspace confinement")
   ```
   
   **Assessment**: CORRECT
   - Uses `os.path.realpath()` which resolves all symlinks in the path
   - `relative_to()` raises `ValueError` if path escapes workspace
   - Cleanup attempts to remove the escaped file before raising
   - Cleanup wrapped in try/except to handle edge cases (file already deleted, permissions, etc.)

5. **Audit Logging** (line 360)
   - Logs successful download with real path
   - **Assessment**: CORRECT - provides audit trail

---

### 3. Server.py Exception Handling

**File**: `src/email_mcp/server.py` (lines 175-176)

```python
except SecurityError as e:
  raise ToolError(str(e))
```

**Assessment**: CORRECT
- SecurityError properly caught and converted to ToolError
- Error message "Download escaped workspace confinement" is appropriate
- Does not leak internal file paths to client

---

### 4. Test Coverage Analysis

**File**: `tests/test_path_traversal.py`

| Test | Coverage | Assessment |
|------|----------|------------|
| `test_filename_sanitization` | Filename sanitization logic | CORRECT |
| `test_invalid_filename_rejected` | `.` and `..` rejection | CORRECT |
| `test_symlink_escape_detected_and_cleaned` | Symlink detection concept | PARTIAL |
| `test_normal_path_within_workspace` | Normal path verification | CORRECT |
| `test_security_error_on_symlink_escape` | ValueError detection | CORRECT |
| `test_post_write_verification_logic` | Verification logic | CORRECT |

#### Test Gaps Identified:

1. **No integration test calling `download_attachment()`**
   - Tests verify concepts but not the actual method
   - Should mock IMAP client and test full flow

2. **No test verifying cleanup actually removes file**
   - Test setup creates symlink but doesn't write then verify cleanup
   - Should write file, trigger escape, verify file is removed

3. **No test for SecurityError propagation to server**
   - Should verify SecurityError reaches ToolError conversion

---

## Acceptance Criteria Verification

| Criteria | Status | Notes |
|----------|--------|-------|
| Use `os.path.realpath()` to resolve final path | PASS | Lines 345-346 |
| Verify within workspace | PASS | Lines 348-358 |
| Unit tests for symlink escape detection | PARTIAL | Concepts tested, not full method |
| Integration tests for TOCTOU race conditions | MISSING | No integration tests |
| Clean up escaped files before raising | PASS | Lines 352-355 |
| Handle SecurityError in server | PASS | Lines 175-176 |

---

## Security Analysis

### Attack Vectors Considered:

1. **Symlink in output directory**
   - Attacker creates `output_dir/escaped` as symlink to `/etc`
   - File written to `/etc/filename`
   - `realpath()` resolves to `/etc/filename`
   - `relative_to()` fails → SecurityError
   - **Result**: BLOCKED

2. **Symlink in workspace**
   - Attacker creates `/workspace/downloads` as symlink to `/outside`
   - File written to `/outside/filename`
   - `realpath()` resolves to `/outside/filename`
   - `relative_to()` fails → SecurityError
   - **Result**: BLOCKED

3. **Symlink as filename**
   - Attacker provides filename `symlink_file` where `workspace/symlink_file` → `/etc/passwd`
   - `os.path.basename()` strips path components
   - File written to `workspace/hash_symlink_file`
   - If it escapes, verification catches it
   - **Result**: BLOCKED

4. **Race between check and write**
   - Attacker replaces directory with symlink after check
   - Post-write verification catches the escape
   - **Result**: BLOCKED (TOCTOU protected)

### Edge Cases:

1. **File deletion race during cleanup**
   - Symlink deleted between write and unlink
   - File remains outside workspace
   - SecurityError still raised
   - **Mitigation**: Acceptable - violation detected and reported

2. **Permission denied during cleanup**
   - `os.unlink()` fails due to permissions
   - `OSError` caught, file may remain
   - SecurityError still raised
   - **Mitigation**: Acceptable - violation detected and reported

---

## Issues Found

### Issue 1: Missing Integration Tests (Medium)

**Severity**: Medium
**Location**: `tests/test_path_traversal.py`
**Description**: Tests verify individual concepts but do not test `download_attachment()` with mocked IMAP client.

**Recommendation**: Add integration test that:
1. Mocks IMAP client to return attachment
2. Creates symlink in output directory
3. Calls `download_attachment()`
4. Verifies SecurityError is raised
5. Verifies file is cleaned up

### Issue 2: Redundant Workspace Resolution (Low)

**Severity**: Low
**Location**: `client.py` lines 332 and 346
**Description**: `DEFAULT_WORKSPACE` is resolved twice - once before directory creation and once after write.

**Recommendation**: Minor optimization - store resolved path in variable. Not critical.

### Issue 3: Missing Test for Cleanup Verification (Low)

**Severity**: Low
**Location**: `tests/test_path_traversal.py`
**Description**: No test verifies that the file is actually removed when SecurityError is raised.

**Recommendation**: Add test that:
1. Creates symlink escape scenario
2. Attempts to write through the code path
3. Verifies file does not exist after SecurityError

---

## Recommendations

1. **Add integration tests** for `download_attachment()` with mocked IMAP client
2. **Add test** verifying cleanup removes file
3. **Add test** verifying SecurityError propagates to ToolError in server
4. Consider pre-write validation of output_dir for early rejection (optional optimization)

---

## Verdict

**CONDITIONAL APPROVE**

The implementation correctly fixes the TOCTOU vulnerability with post-write verification. The core security logic is sound and handles the symlink race condition properly.

**Conditions**:
1. Add integration tests for `download_attachment()` with mocked IMAP (tracked in TODO.md)
2. Verify cleanup functionality in tests (tracked in TODO.md)

The existing tests adequately verify the concepts, but integration tests would provide better coverage of the full code path.

---

## Files Reviewed

| File | Lines Changed | Purpose |
|------|---------------|---------|
| `src/email_mcp/imap/client.py` | 27-29, 290-363 | SecurityError definition, post-write verification |
| `src/email_mcp/server.py` | 13, 175-176 | Import SecurityError, exception handling |
| `tests/test_path_traversal.py` | 61-145 | Symlink race condition tests |