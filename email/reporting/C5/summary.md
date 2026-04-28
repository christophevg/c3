# Task Summary: C5 - Fix SMTP Exception Chain Swallowing

## What Was Implemented

Fixed exception chain swallowing in SMTP client by adding `from e` to preserve the original exception when converting `SMTPException` to `RuntimeError`.

## Location

- **File**: `src/email_mcp/smtp/client.py`
- **Lines**: 204-205

## Change

```python
# Before:
except aiosmtplib.SMTPException as e:
  raise RuntimeError("Failed to send email. Check server logs for details.")

# After:
except aiosmtplib.SMTPException as e:
  raise RuntimeError("Failed to send email. Check server logs for details.") from e
```

## Key Decisions

1. **Minimal fix**: Only added `from e` - no refactoring required
2. **Security maintained**: User-facing message remains generic (no SMTP internals leaked)
3. **Debugging enabled**: Full exception chain now available in traceback for root cause analysis

## Tests Added

`tests/test_smtp_client.py::TestSMTPExceptionChaining`:
- `test_smtp_exception_chain_preserved`: Verifies `__cause__` is the original SMTPException
- `test_smtp_exception_message_unchanged`: Verifies RuntimeError message remains generic

## Files Modified

| File | Change |
|------|--------|
| `src/email_mcp/smtp/client.py` | Added `from e` to preserve exception chain |
| `tests/test_smtp_client.py` | Added 2 tests for exception chaining |
| `TODO.md` | Marked C5 as complete |
| `docs/bug-analysis/C5.md` | Bug analysis report |

## Lessons Learned

- Python's `from` keyword is essential when converting library exceptions to domain-specific exceptions
- Exception chaining provides debugging context without changing user-facing behavior
- Generic error messages are important for security, but shouldn't lose debugging context

## Risk Assessment

**No breaking changes**:
- Exception type unchanged (`RuntimeError`)
- Exception message unchanged
- Only adds `__cause__` attribute for debugging