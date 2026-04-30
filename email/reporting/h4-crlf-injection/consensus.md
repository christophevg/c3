# Consensus Report: H4 CRLF Injection Protection

**Date**: 2026-04-30
**Task**: H4 - Add CRLF injection protection for SMTP headers

---

## Agent Reviews

| Agent | Status | Key Recommendations |
|-------|--------|---------------------|
| api-architect | ✅ Approved | `sanitize_message_id()`, `sanitize_references()`, update `reply_email()` |
| security-engineer | ✅ Approved | `sanitize_header()`, `sanitize_folder_name()`, comprehensive protection |

---

## Consensus Design

### 1. Sanitization Module

Create `src/email_mcp/safety/sanitize.py` with:

| Function | Purpose | Returns |
|----------|---------|---------|
| `sanitize_message_id(msg_id)` | Validate RFC 5322 Message-ID format | Validated string or raises `ValueError` |
| `sanitize_references(refs)` | Validate list of Message-IDs | Validated list or raises `ValueError` |
| `sanitize_header(value)` | Generic header sanitization | Sanitized string or raises `ValueError` |
| `sanitize_folder_name(folder)` | IMAP folder name validation | Validated string or raises `ValueError` |

### 2. Update SMTP Client

Modify `src/email_mcp/smtp/client.py`:

1. **`reply_email()` method** (lines 116-148):
   - Sanitize `in_reply_to` with `sanitize_message_id()`
   - Sanitize `references` with `sanitize_references()`

2. **`send_email()` method** (lines 72-115):
   - Sanitize `subject` with `sanitize_header()`
   - Consider explicit CRLF check in `validate_email()`

### 3. Update IMAP Client (Defense in Depth)

Modify `src/email_mcp/imap/client.py`:

- Sanitize `folder` parameter with `sanitize_folder_name()`

### 4. Error Handling

- Use `ValueError` for invalid input (fail-fast)
- Include clear error messages
- Log sanitization rejections for audit trail

---

## Test Strategy

| Test Type | Coverage |
|-----------|----------|
| Unit tests | `sanitize_message_id()`, `sanitize_references()`, `sanitize_header()` |
| Integration tests | `reply_email()` with malicious input |
| Fuzz tests | Various CRLF encodings (%0D, %0A, Unicode newlines) |
| Regression tests | Legitimate headers pass through correctly |

---

## Implementation Plan

1. Create `src/email_mcp/safety/sanitize.py`
2. Update `src/email_mcp/smtp/client.py` to use sanitization
3. Add unit tests in `tests/test_sanitize.py`
4. Add integration tests in `tests/test_smtp_client.py`

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Breaking valid Message-IDs | Strict RFC 5322 validation preserves valid IDs |
| False positives | Test with real-world Message-IDs |
| Incomplete coverage | Comprehensive fuzz testing |

---

## Approval

Both domain agents approve proceeding to implementation.