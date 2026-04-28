# Task Summary: H2 - Fix Auth Exception Handling

## What Was Implemented

Fixed broad exception handling during IMAP authentication by splitting the single `except Exception` handler into specific catch blocks for different error types.

## Location

- **File**: `src/email_mcp/imap/client.py`
- **Lines**: 64-111 (connect method)

## Changes

### 1. Added Imports

```python
import socket
import ssl
import traceback
import aioimaplib
```

### 2. Wrapped Entire Connection Setup

The exception handling now covers:
- `IMAP4_SSL()` creation
- `wait_hello_from_server()`
- Authentication (`login()` / `authenticate()`)

### 3. Specific Exception Handlers

| Exception Type | Error Message | Logged as Auth Failure? |
|---------------|---------------|------------------------|
| `ValueError` | "Configuration error: {e}" | Yes |
| `TimeoutError` | "Connection timed out. Check server availability." | No |
| `ConnectionError` | "Connection lost: {e}" | No |
| `ssl.SSLError` | "TLS error: {e}. Check server certificate." | No |
| `aioimaplib.Abort` | "Protocol error: {e}" | No |
| `aioimaplib.Error` | "Authentication failed. Check server logs for details." | Yes |
| `socket.gaierror` (OSError) | "DNS resolution failed for {host}" | No |
| `OSError` | "Network error: {e}" | No |
| `Exception` | "An unexpected error occurred: {type}: {e}" | No |

## Key Decisions

1. **Auth failure logging isolated**: Only `ValueError` and `aioimaplib.Error` are logged as auth failures
2. **Actionable messages**: Each error type has a specific, actionable message
3. **Exception chaining**: All use `raise ... from e` to preserve debug context
4. **Python 3.11+ compatibility**: Consolidated timeout handlers (`asyncio.TimeoutError` is an alias for `TimeoutError` in 3.11+)

## Tests Added

`tests/test_imap_client.py::TestAuthExceptionHandling` (8 tests):
- `test_invalid_password_raises_auth_error`: Verifies auth error for invalid credentials
- `test_oauth2_invalid_token_raises_auth_error`: Verifies auth error for invalid OAuth2 token
- `test_connection_timeout_raises_timeout_error`: Verifies timeout message
- `test_network_disconnect_raises_connection_error`: Verifies connection error message
- `test_dns_failure_raises_dns_error`: Verifies DNS-specific message
- `test_tls_error_raises_tls_message`: Verifies TLS error message
- `test_abort_raises_protocol_error`: Verifies protocol error message
- `test_oserror_raises_network_error`: Verifies network error message

## Files Modified

| File | Change |
|------|--------|
| `src/email_mcp/imap/client.py` | Added imports, split exception handling |
| `tests/test_imap_client.py` | Added 8 tests, updated existing auth test to use `aioimaplib.Error` |
| `TODO.md` | Marked H2 and H7 as complete |
| `docs/bug-analysis/H2.md` | Bug analysis report |

## Lessons Learned

- Broad `except Exception` catches everything including network errors, DNS failures, TLS errors
- Exception hierarchy must be caught in order (most specific first)
- In Python 3.11+, `asyncio.TimeoutError` is an alias for `TimeoutError`
- Auth failure audit logging should only apply to actual credential issues

## Risk Assessment

**No breaking changes**:
- All errors still raise `RuntimeError`
- Error messages are more specific (better UX)
- Public API unchanged