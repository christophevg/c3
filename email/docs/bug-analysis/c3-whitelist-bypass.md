# Bug Analysis: C3 - reply_email() Whitelist Bypass

## Summary

**Bug ID**: C3
**Severity**: Critical (Security Vulnerability)
**Status**: Fixed
**Date**: 2026-04-28

## Description

The `reply_email()` method in `smtp/client.py` bypassed the recipient whitelist check that `send_email()` enforces. This allowed emails to be sent to recipients outside the configured whitelist, violating the security policy.

## Impact

- **Security**: Users relying on the recipient whitelist to restrict email recipients could have their policy bypassed by using `reply_email()` instead of `send_email()`.
- **Data Exfiltration**: Malicious actors could exfiltrate data to unauthorized addresses via replies.

## Root Cause

`send_email()` correctly implements:
1. Email address validation (`validate_email()`)
2. Recipient whitelist check (`get_recipient_whitelist().is_allowed()`)

`reply_email()` implemented neither:
1. No email validation
2. No whitelist check
3. Direct call to `_send()` without any security controls

## Fix

Added two lines to `reply_email()` before creating the `EmailMessage`:

```python
# Validate email address
validate_email(to)

# Check recipient whitelist
whitelist = get_recipient_whitelist()
if not whitelist.is_allowed(to):
    raise WhitelistError(f"Recipients not in whitelist: {to}")
```

**File**: `src/email_mcp/smtp/client.py` (lines 126-132)

## Tests

Created `tests/test_smtp_client.py` with 5 test cases:

| Test | Purpose |
|------|---------|
| `test_reply_email_bypasses_whitelist` | Confirms `WhitelistError` raised for blocked recipient |
| `test_reply_email_allows_whitelisted` | Confirms normal flow works for allowed recipient |
| `test_reply_email_disabled_whitelist_allows_all` | Confirms disabled whitelist allows all |
| `test_reply_email_invalid_address` | Confirms email format validation works |
| `test_reply_email_missing_at_symbol` | Confirms validation catches malformed addresses |

All tests pass. No regressions in existing SMTP/server tests.

## Verification

```bash
python -m pytest tests/test_smtp_client.py tests/test_server.py -v
# 16 passed
```

## Lessons Learned

1. **Security functions must be called consistently**: Any method that sends email should use the same validation and whitelist checks.
2. **Test coverage gaps**: Zero tests for SMTPClient allowed this bug to persist.
3. **Code review patterns**: When adding security controls to one method, audit all similar methods.

## Related Issues

- C24: `reply_email` should also have `validate_email()` — merged into this fix
- M13: `reply_email` should accept `list[str]` for consistency — separate issue, low priority