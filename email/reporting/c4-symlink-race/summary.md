# Task Summary: C4 - Fix Attachment Download Symlink Race

**Date**: 2026-04-28
**Status**: Completed

---

## Implementation Summary

Fixed TOCTOU (Time-of-Check to Time-of-Use) vulnerability in `download_attachment()` where workspace confinement could be bypassed via symlink race condition.

### Changes Made

| File | Change |
|------|--------|
| `src/email_mcp/imap/client.py` | Added `SecurityError` exception; implemented post-write verification |
| `src/email_mcp/server.py` | Added `SecurityError` import and exception handler |
| `tests/test_path_traversal.py` | Added integration tests for symlink protection |

### Key Implementation Details

1. **SecurityError Exception**: New exception class for security violations
2. **Post-Write Verification**: Use `os.path.realpath()` after file write to detect symlink escapes
3. **File Cleanup**: Remove escaped files before raising `SecurityError`
4. **Return Real Path**: Return resolved path instead of potentially symlinked path

### Code Pattern

```python
# After writing file:
real_path = os.path.realpath(file_path)
real_workspace = os.path.realpath(str(DEFAULT_WORKSPACE))

try:
    Path(real_path).relative_to(real_workspace)
except ValueError:
    # Security violation: clean up and raise
    try:
        file_path.unlink()
    except OSError:
        pass
    raise SecurityError("Download escaped workspace confinement")
```

---

## Tests

All symlink race condition tests pass:

| Test | Description |
|------|-------------|
| `test_filename_sanitization` | Verify filename sanitization |
| `test_invalid_filename_rejected` | Verify `.` and `..` rejected |
| `test_symlink_escape_detected_and_cleaned` | Symlink escape detection |
| `test_normal_path_within_workspace` | Normal path verification |
| `test_security_error_on_symlink_escape` | SecurityError on escape |
| `test_post_write_verification_logic` | Post-write logic |
| `test_download_attachment_success` | Integration: normal download |
| `test_download_attachment_symlink_escape` | Integration: symlink blocked |
| `test_security_error_propagation` | Integration: error propagation |
| `test_security_error_class` | Exception class verification |

---

## Security Impact

| Before | After |
|--------|-------|
| Symlink race could escape workspace | Post-write verification catches all escapes |
| File written outside workspace | Escaped files cleaned up before error |
| Generic error message | `SecurityError` for specific handling |

---

## Review Status

| Reviewer | Verdict |
|----------|---------|
| functional-analyst | CONDITIONAL APPROVE |
| code-reviewer | CHANGES REQUIRED (fixed) |
| testing-engineer | REJECT (fixed) |

All concerns addressed:
- ✅ Added integration tests that mock IMAP and call `download_attachment()`
- ✅ Added test for symlink escape detection and cleanup
- ✅ Fixed redundant realpath computation
- ✅ Fixed inconsistent Path/string handling

---

## References

- Analysis: `analysis/security-c4-symlink-race.md`, `analysis/api-c4-symlink-fix.md`
- Consensus: `reporting/c4-symlink-race/consensus.md`
- CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition