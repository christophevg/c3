# Security Analysis: CRLF Injection Vulnerability (H4)

**Date**: 2026-04-30
**Task**: H4 - Add CRLF injection protection for SMTP headers
**Severity**: Critical (CVSS 9.1)
**CWE**: CWE-93 (Improper Neutralization of CRLF Sequences)
**CVE Related**: CVE-2024-6923 (Python email module header injection)

---

## Executive Summary

The email MCP server is vulnerable to CRLF injection attacks through user-controlled email header fields. Python's `email.message.EmailMessage` module (prior to patched versions) does not properly quote newlines in email headers during serialization, allowing attackers to inject arbitrary headers or manipulate email content.

---

## 1. Threat Analysis

**Classification**: Injection Vulnerability
**OWASP Category**: A03:2021 - Injection

### Affected Components

| File | Lines | Vulnerable Parameter | Risk Level |
|------|-------|---------------------|------------|
| `smtp/client.py` | 80-87, 137-143 | `to`, `subject`, `cc`, `bcc`, `in_reply_to`, `references` | Critical |
| `imap/client.py` | 170, 196, 237, 292 | `folder`, `message_id` | High |
| `server.py` | 73, 82, 107, 139 | Tool parameters passed to clients | Medium |

---

## 2. Attack Vectors

### Vector A: Email Header Injection (Critical - CVSS 9.1)

**Location**: `smtp/client.py`, lines 80-87

**Attack Scenario**:
```
Subject: "Important Update\r\nBcc: attacker@evil.com\r\n\r\nMalicious content here"
```

**Impact**:
1. **Header Injection**: Attacker injects arbitrary email headers (Bcc, Cc, X-*)
2. **Content Manipulation**: MIME headers can be pushed into message body
3. **Data Exfiltration**: Silent Bcc to external addresses
4. **Spoofing**: Override envelope sender or add fake authentication headers

### Vector B: IMAP Command Injection (High - CVSS 7.5)

**Location**: `imap/client.py`, lines 170, 196

**Attack Scenario**:
```
folder: "INBOX\r\nDELETE ALL\r\nSELECT "
```

**Impact**:
1. **Command Injection**: Arbitrary IMAP commands execution
2. **Data Deletion**: Unintended message deletion
3. **Mailbox Manipulation**: Create/delete folders
4. **Information Disclosure**: Access to other mailboxes

### Vector C: Log Entry Injection (Low - Mitigated)

**Location**: `safety/audit.py`, line 43

**Status**: MITIGATED - The `log_event` function uses `json.dumps()` which properly escapes CRLF characters.

---

## 3. Recommended Mitigations

### Mitigation A: Input Validation and Sanitization (Critical Priority)

**Location**: Create new file `src/email_mcp/safety/sanitize.py`

```python
"""Input sanitization for CRLF injection prevention."""

import re

# Pattern to detect CRLF sequences (CR, LF, CRLF, and encoded variants)
CRLF_PATTERN = re.compile(r'[\r\n]|(%0[dD])|(%0[aA])')

def sanitize_header(value: str, max_length: int = 1000) -> str:
  """Sanitize a value for use in email headers.

  Removes CRLF sequences and truncates to max_length.
  """
  if not value:
    raise ValueError("Header value cannot be empty")

  # Remove CRLF sequences
  sanitized = CRLF_PATTERN.sub('', value).strip()

  if not sanitized:
    raise ValueError("Header value contains only invalid characters")

  # Truncate to max length
  if len(sanitized) > max_length:
    sanitized = sanitized[:max_length]

  return sanitized

def sanitize_folder_name(folder: str) -> str:
  """Sanitize IMAP folder name."""
  if not folder:
    raise ValueError("Folder name cannot be empty")

  if CRLF_PATTERN.search(folder):
    raise ValueError("Folder name contains invalid characters")

  if any(ord(c) < 32 for c in folder):
    raise ValueError("Folder name contains control characters")

  return folder.strip()

def sanitize_message_id(message_id: str) -> str:
  """Sanitize IMAP message ID (should be numeric)."""
  if not message_id:
    raise ValueError("Message ID cannot be empty")

  if not message_id.isdigit():
    raise ValueError("Message ID must be numeric")

  return message_id
```

### Mitigation B: Apply Sanitization in SMTP Client (Critical Priority)

**Location**: `smtp/client.py`

```python
from email_mcp.safety.sanitize import sanitize_header

# In send_email and reply_email methods:
try:
  subject = sanitize_header(subject)
  validated_to = [sanitize_header(addr) for addr in to]
except ValueError as e:
  raise ValueError(f"Invalid header value: {e}") from e
```

### Mitigation C: Apply Sanitization in IMAP Client (High Priority)

**Location**: `imap/client.py`

```python
from email_mcp.safety.sanitize import sanitize_folder_name, sanitize_message_id

# In select_folder method:
safe_folder = sanitize_folder_name(folder)

# In fetch_message method:
safe_id = sanitize_message_id(message_id)
```

### Mitigation D: Update Python Version (Critical Priority)

**CVE-2024-6923** affects Python 3.8 through 3.13 (unpatched versions). Update to:
- Python 3.8.20+
- Python 3.9.21+
- Python 3.10.16+
- Python 3.11.11+
- Python 3.12.5+
- Python 3.13+

### Mitigation E: Defense in Depth - Email Policy (Medium Priority)

Use `email.policy.SMTP` policy for stricter header handling:

```python
from email.policy import SMTP

msg = EmailMessage(policy=SMTP)
```

---

## 4. Testing Approach

### Test Case 1: Email Header CRLF Injection

```python
import pytest
from email_mcp.safety.sanitize import sanitize_header

def test_crlf_injection_subject():
  """Test that CRLF in subject is sanitized."""
  malicious = "Important Update\r\nBcc: attacker@evil.com"

  with pytest.raises(ValueError):
    sanitize_header(malicious)

def test_encoded_crlf_injection():
  """Test URL-encoded CRLF detection."""
  malicious = "Hello%0D%0ABcc: attacker@evil.com"

  with pytest.raises(ValueError):
    sanitize_header(malicious)
```

### Test Case 2: IMAP Command Injection

```python
def test_imap_folder_crlf_injection():
  """Test that CRLF in folder names is rejected."""
  from email_mcp.safety.sanitize import sanitize_folder_name

  malicious = "INBOX\r\nDELETE ALL"

  with pytest.raises(ValueError, match="invalid characters"):
    sanitize_folder_name(malicious)
```

### Test Case 3: Fuzzing

```python
@pytest.mark.parametrize("payload", [
  "\r\n", "\n", "\r", "%0D", "%0A", "%0d%0a", "\x0d\x0a",
  " ", " ",  # Unicode newlines
  "Hello\r\nWorld\nTest\rEnd",
])
def test_fuzz_crlf_variants(payload):
  """Fuzz test for various CRLF representations."""
  result = sanitize_header("prefix" + payload + "suffix")
  assert "\r" not in result
  assert "\n" not in result
```

### Test Case 4: Regression Test

```python
def test_legitimate_headers_preserved():
  """Test that legitimate headers work correctly."""
  assert sanitize_header("Normal Subject") == "Normal Subject"
  assert sanitize_header("Re: Meeting Tomorrow") == "Re: Meeting Tomorrow"
```

---

## 5. Severity Assessment

| Finding | CVSS | Severity | Priority |
|---------|------|----------|----------|
| Email Header Injection via CVE-2024-6923 | 9.1 | Critical | P1 |
| IMAP Folder/Command Injection | 7.5 | High | P2 |
| Log Injection | 2.0 | Low | Mitigated |

---

## 6. References

- **CVE-2024-6923**: [Python email module header injection](https://www.cve.org/CVERecord?id=CVE-2024-6923)
- **CWE-93**: [Improper Neutralization of CRLF Sequences](https://cwe.mitre.org/data/definitions/93.html)
- **OWASP A03:2021**: [Injection](https://owasp.org/Top10/A03_2021-Injection/)
- **Python Fix PR GH-122233**: [Encode newlines in headers](https://github.com/python/cpython/pull/122233)