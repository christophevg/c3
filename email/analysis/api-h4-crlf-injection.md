# CRLF Injection Protection Analysis (H4)

**Date**: 2026-04-30
**Task**: H4 - Add CRLF injection protection for SMTP headers
**Location**: `email/src/email_mcp/smtp/client.py`
**Severity**: Medium (security vulnerability)

---

## Executive Summary

The SMTP client's `reply_email()` method accepts `in_reply_to` and `references` parameters without sanitization, creating a potential CRLF injection vulnerability. An attacker could craft malicious Message-ID values containing `\r\n` sequences to inject arbitrary email headers or perform header splitting attacks.

---

## Current Implementation Analysis

### Vulnerable Code (lines 116-148)

```python
async def reply_email(
  self,
  to: str,
  subject: str,
  body: str,
  in_reply_to: str,
  references: list[str] | None = None,
  html_body: str | None = None,
) -> dict[str, str]:
  """Send a reply preserving thread context."""
  # Validate email address
  validate_email(to)

  # Check recipient whitelist
  whitelist = get_recipient_whitelist()
  if not whitelist.is_allowed(to):
    raise WhitelistError(f"Recipients not in whitelist: {to}")

  msg = EmailMessage()

  msg["From"] = self.account.username
  msg["To"] = to
  msg["Subject"] = subject
  msg["In-Reply-To"] = in_reply_to  # UNSANITIZED - line 139

  if references:
    msg["References"] = " ".join(references)  # UNSANITIZED - line 142

  msg.set_content(body)
  if html_body:
    msg.add_alternative(html_body, subtype="html")

  return await self._send(msg, [to])
```

### Attack Vectors

1. **Header Injection via In-Reply-To**
   ```python
   in_reply_to = "<valid@id.com>\r\nBcc: attacker@evil.com\r\n"
   ```
   This would inject a Bcc header, potentially leaking the email to unauthorized recipients.

2. **Header Injection via References**
   ```python
   references = ["<msg1@id.com>\r\nX-Injected: evil", "<msg2@id.com>"]
   ```
   The `join()` operation doesn't sanitize, allowing injection.

3. **Header Splitting**
   ```python
   in_reply_to = "<valid@id.com>\r\n\r\n<html>malicious body</html>"
   ```
   Could inject content that bypasses email client filtering.

### Existing Protections

1. **Python email library** - The `EmailMessage` class does perform some header folding and validation, but it's not designed to prevent all CRLF injection attacks.

2. **Input source** - Message-IDs typically come from received emails (IMAP), which could be controlled by an attacker.

3. **No explicit validation** - There's no validation that `in_reply_to` and `references` are valid Message-ID formats.

---

## Recommended Sanitization Approach

### Option 1: Message-ID Format Validation (Recommended)

Validate that headers conform to RFC 5322 Message-ID format:

```python
# Add to smtp/client.py

import re

# RFC 5322 Message-ID format: <id@domain>
MESSAGE_ID_PATTERN = re.compile(r"^<[^<>@]+@[^<>@]+>$")

def validate_message_id(message_id: str) -> str:
  """Validate Message-ID format and reject CRLF sequences."""
  # Check for CRLF sequences
  if "\r" in message_id or "\n" in message_id:
    raise ValueError(f"Invalid Message-ID: contains newline characters")

  # Validate format
  if not MESSAGE_ID_PATTERN.match(message_id):
    raise ValueError(f"Invalid Message-ID format: {message_id}")

  return message_id
```

**Pros**: Strict validation, catches malformed IDs, prevents injection
**Cons**: May reject valid but unusual Message-IDs

### Option 2: CRLF Stripping

Strip CRLF sequences while preserving the value:

```python
def sanitize_header_value(value: str) -> str:
  """Remove CRLF sequences from header values."""
  # Remove CR, LF, and CRLF sequences
  return value.replace("\r", "").replace("\n", "")
```

**Pros**: Preserves content, no format assumptions
**Cons**: May silently modify valid content, doesn't catch malicious intent

### Option 3: Combined Approach (Best)

Validate format AND sanitize:

```python
def sanitize_message_id(message_id: str) -> str:
  """Validate and sanitize Message-ID for header safety."""
  # Reject CRLF sequences explicitly
  if "\r" in message_id or "\n" in message_id:
    raise ValueError("Message-ID contains invalid newline characters")

  # Validate format (angle-bracketed email-like string)
  if not message_id.startswith("<") or not message_id.endswith(">"):
    raise ValueError(f"Message-ID must be angle-bracketed: {message_id}")

  # Ensure no embedded angle brackets
  inner = message_id[1:-1]
  if "<" in inner or ">" in inner:
    raise ValueError(f"Message-ID contains invalid characters: {message_id}")

  return message_id


def sanitize_references(references: list[str]) -> list[str]:
  """Validate and sanitize a list of Message-IDs."""
  return [sanitize_message_id(ref) for ref in references]
```

---

## Code Changes Needed

### File: `email/src/email_mcp/smtp/client.py`

#### 1. Add sanitization functions (after line 28)

```python
def sanitize_message_id(message_id: str) -> str:
  """Validate and sanitize Message-ID for header safety.

  Prevents CRLF injection by rejecting newline characters and validating
  RFC 5322 Message-ID format.

  Args:
    message_id: A Message-ID string (should be angle-bracketed)

  Returns:
    The validated Message-ID

  Raises:
    ValueError: If the Message-ID contains newlines or has invalid format
  """
  # Reject CRLF sequences explicitly - this is the security fix
  if "\r" in message_id or "\n" in message_id:
    raise ValueError("Message-ID contains invalid newline characters")

  # Validate format: Message-IDs must be angle-bracketed
  if not message_id.startswith("<") or not message_id.endswith(">"):
    raise ValueError(f"Message-ID must be angle-bracketed: {message_id}")

  # Ensure no embedded angle brackets (prevents <a<b>@domain.com>)
  inner = message_id[1:-1]
  if "<" in inner or ">" in inner:
    raise ValueError(f"Message-ID contains invalid characters: {message_id}")

  return message_id


def sanitize_references(references: list[str]) -> list[str]:
  """Validate and sanitize a list of Message-ID references.

  Args:
    references: List of Message-ID strings

  Returns:
    List of validated Message-IDs

  Raises:
    ValueError: If any Message-ID is invalid
  """
  return [sanitize_message_id(ref) for ref in references]
```

#### 2. Update `reply_email()` method (lines 136-142)

```python
async def reply_email(
  self,
  to: str,
  subject: str,
  body: str,
  in_reply_to: str,
  references: list[str] | None = None,
  html_body: str | None = None,
) -> dict[str, str]:
  """Send a reply preserving thread context."""
  # Validate email address
  validate_email(to)

  # Sanitize Message-ID headers to prevent CRLF injection
  safe_in_reply_to = sanitize_message_id(in_reply_to)
  safe_references = sanitize_references(references) if references else None

  # Check recipient whitelist
  whitelist = get_recipient_whitelist()
  if not whitelist.is_allowed(to):
    raise WhitelistError(f"Recipients not in whitelist: {to}")

  msg = EmailMessage()

  msg["From"] = self.account.username
  msg["To"] = to
  msg["Subject"] = subject
  msg["In-Reply-To"] = safe_in_reply_to

  if safe_references:
    msg["References"] = " ".join(safe_references)

  msg.set_content(body)
  if html_body:
    msg.add_alternative(html_body, subtype="html")

  return await self._send(msg, [to])
```

---

## Trade-offs and Considerations

### Security vs. Compatibility

| Approach | Security | Compatibility | Recommendation |
|----------|----------|---------------|----------------|
| Strict validation | High | May break unusual but valid IDs | Use for new systems |
| Sanitization only | Medium | Preserves all content | Use for legacy systems |
| Combined (recommended) | High | Rejects invalid format | Best for security |

### Error Handling

Two strategies for handling invalid Message-IDs:

1. **Raise Exception** (Recommended)
   - Fail fast with clear error message
   - Forces caller to handle the issue
   - Prevents silent data modification

2. **Sanitize and Continue**
   - Removes problematic characters
   - Email still sends but may break threading
   - Silent modification may hide attacks

**Recommendation**: Raise `ValueError` for invalid Message-IDs. This is a security feature, not a user convenience feature. Invalid Message-IDs indicate either corrupted data or an attack attempt.

### Message-ID Sources

Message-IDs come from:

1. **Received emails via IMAP** - `get_email()` returns `message_id` field
2. **User-provided** - In case of manual reply construction

For IMAP-sourced Message-IDs:
- IMAP servers typically return valid Message-IDs
- But attacker-controlled emails could have malicious Message-IDs
- This is the primary threat vector

### Impact on Email Threading

- Valid Message-IDs in standard format will pass validation
- Email threading depends on matching Message-IDs exactly
- Sanitization must not modify valid Message-IDs
- Validation approach preserves exact values for valid inputs

### Performance

- Regex validation is O(1) per Message-ID
- No database or network calls
- Negligible performance impact

---

## Testing Recommendations

### Unit Tests

```python
# tests/test_smtp_client.py

import pytest
from email_mcp.smtp.client import sanitize_message_id, sanitize_references

class TestMessageIDSanitization:
  def test_valid_message_id(self):
    assert sanitize_message_id("<abc123@mail.example.com>") == "<abc123@mail.example.com>"

  def test_rejects_cr_injection(self):
    with pytest.raises(ValueError, match="newline"):
      sanitize_message_id("<valid@id.com>\r\nBcc: evil@attacker.com")

  def test_rejects_lf_injection(self):
    with pytest.raises(ValueError, match="newline"):
      sanitize_message_id("<valid@id.com>\nX-Injected: evil")

  def test_rejects_crlf_injection(self):
    with pytest.raises(ValueError, match="newline"):
      sanitize_message_id("<valid@id.com>\r\n\r\nInjected body")

  def test_rejects_unbracketed_id(self):
    with pytest.raises(ValueError, match="angle-bracketed"):
      sanitize_message_id("plain@id.com")

  def test_rejects_embedded_brackets(self):
    with pytest.raises(ValueError, match="invalid characters"):
      sanitize_message_id("<a<b>@domain.com>")

  def test_sanitize_references_valid(self):
    refs = ["<msg1@id.com>", "<msg2@id.com>"]
    assert sanitize_references(refs) == refs

  def test_sanitize_rejects_invalid_reference(self):
    refs = ["<msg1@id.com>", "invalid@injection\r\nEvil: yes"]
    with pytest.raises(ValueError):
      sanitize_references(refs)
```

### Integration Test

```python
@pytest.mark.asyncio
async def test_reply_email_rejects_crlf_injection(smtp_client):
  with pytest.raises(ValueError, match="newline"):
    await smtp_client.reply_email(
      to="recipient@example.com",
      subject="Re: Test",
      body="Reply body",
      in_reply_to="<valid@id.com>\r\nBcc: attacker@evil.com",
    )
```

---

## Additional Recommendations

### 1. Audit Other Headers

The `send_email()` method should also validate:

- `subject` parameter (line 82) - Could contain CRLF
- `to`, `cc`, `bcc` lists - Already validated by `validate_email()` but CRLF check is implicit in regex

Consider adding explicit CRLF check to `validate_email()`:

```python
def validate_email(address: str) -> str:
  """Validate email address format."""
  if "\r" in address or "\n" in address:
    raise ValueError(f"Email address contains invalid characters: {address}")
  if not EMAIL_PATTERN.match(address):
    raise ValueError(f"Invalid email address: {address}")
  return address
```

### 2. Subject Header Protection

Add subject sanitization:

```python
def sanitize_subject(subject: str) -> str:
  """Sanitize email subject for header safety."""
  # Remove CRLF sequences
  return subject.replace("\r", "").replace("\n", " ")
```

### 3. Centralized Header Sanitization

Consider creating a `headers.py` module with all header sanitization utilities:

```python
# email/src/email_mcp/smtp/headers.py

def sanitize_header_value(value: str) -> str:
  """Generic header value sanitization."""
  return value.replace("\r", "").replace("\n", "")

def validate_email_header(address: str) -> str:
  """Validate email address with CRLF protection."""
  # ... combined email + CRLF validation
```

---

## Conclusion

The CRLF injection vulnerability in `reply_email()` is a medium-severity security issue that could allow:

1. Header injection (Bcc, Cc, etc.)
2. Email body injection
3. Potential phishing or data exfiltration

**Recommended Fix**: Implement Message-ID validation with explicit CRLF rejection (Option 3 - Combined Approach).

**Priority**: Medium - Should be addressed before next release.

**Breaking Changes**: None for valid Message-IDs. Invalid Message-IDs will now raise `ValueError` instead of potentially causing security issues.

**Next Steps**:
1. Implement sanitization functions
2. Add unit tests
3. Update `reply_email()` method
4. Consider similar protection for `subject` and other headers