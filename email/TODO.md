# TODO - Email MCP Server

## Inbox Input

*Unstructured ideas captured during development. To be refined and prioritized.*

- get_email: RuntimeError is handled as a Rate limit problem, which is not in case an incorrect message_id is provided (RuntimeError handling is like that in more tools)

## Backlog (Prioritized)

### P1 - Critical

*No critical items - server is operational.*

### P2 - High

- [ ] **Add comprehensive IMAP/SMTP operation tests**
  - Mock-based tests for all IMAP operations (list_folders, search, fetch, move, delete)
  - Mock-based tests for all SMTP operations (send, reply, forward)
  - Integration tests against local test server
  - Acceptance: >80% code coverage

- [ ] **Add OAuth2 authentication flow tests**
  - Test OAuth2 authentication path in IMAP client
  - Test OAuth2 authentication path in SMTP client
  - Mock OAuth2 token refresh
  - Acceptance: OAuth2 flow fully tested

- [ ] **Add audit logging tests**
  - Test `log_email_sent` called after SMTP send
  - Test `log_auth_attempt` called for auth success/failure
  - Test `log_rate_limited` called when exceeded
  - Acceptance: All audit events verified

### P3 - Medium

- [ ] **Make rate limits configurable at runtime**
  - Environment variables for IMAP/SMTP limits
  - Per-account rate limit override
  - Acceptance: Limits configurable without code changes

- [ ] **Add email body parsing tests**
  - Test `_decode_header()` with various encodings
  - Test `_get_body()` with multipart messages
  - Test `_list_attachments()` filename extraction
  - Acceptance: Body parsing edge cases covered

- [ ] **Add IMAP IDLE support**
  - Real-time email notifications
  - Event-based push to MCP client
  - Acceptance: New emails trigger notifications

- [ ] **Improve folder listing compatibility**
  - Detect and handle different IMAP server quirks
  - Add fallback LIST patterns for strict servers
  - Acceptance: Works with Gmail, Outlook, iCloud, Fastmail

- [ ] **Add TLS configuration tests**
  - Verify TLS 1.2 minimum enforced
  - Test certificate verification
  - Test with self-signed certificates (dev mode)
  - Acceptance: TLS configuration verified

### P4 - Low

- [ ] **Add email search filters**
  - Date range filter
  - From/To filter
  - Subject filter
  - Has attachments filter
  - Acceptance: Rich search capabilities

- [ ] **Add email templates support**
  - Load templates from files
  - Variable substitution
  - Acceptance: Template-based email composition

- [ ] **Add calendar integration**
  - Extract calendar invites
  - Create calendar events from emails
  - Acceptance: Calendar event extraction

- [ ] **Add contact extraction**
  - Extract email addresses from messages
  - Build contact database
  - Acceptance: Contact management tools

- [ ] **Add multi-account batch operations**
  - Search across all accounts
  - Move/copy between accounts
  - Acceptance: Cross-account operations

- [ ] **Document EMAIL_WORKSPACE for production**
  - Add to README security section
  - Provide deployment guide
  - Acceptance: Production deployment documented

## Done

- [x] **Create Email MCP server structure** — 2026-04-20
- [x] **Implement IMAP client with aioimaplib** — 2026-04-20
- [x] **Implement SMTP client with aiosmtplib** — 2026-04-20
- [x] **Add rate limiting** — 2026-04-20
- [x] **Add audit logging** — 2026-04-20
- [x] **Add path traversal protection** — 2026-04-20
- [x] **Add TLS 1.2 minimum enforcement** — 2026-04-20
- [x] **Add recipient whitelist** — 2026-04-20
- [x] **Fix iCloud IMAP LIST compatibility** — 2026-04-20
- [x] **Fix IMAP SELECT response parsing** — 2026-04-20
- [x] **Fix IMAP FETCH response parsing** — 2026-04-20
- [x] **Add foundational test suite** — 2026-04-20
- [x] **Create testing documentation** — 2026-04-20

## Known Issues

| Issue | Workaround | Priority |
|-------|-----------|----------|
| IMAP LIST syntax varies by provider | Use `list('""', '"*"')` format | Medium |
| aioimaplib returns bytearray for message content | Handle both bytes and bytearray | Low |
| Some IMAP servers return different FETCH formats | Parse multiple response formats | Medium |

## Dependencies to Monitor

| Package | Version | Notes |
|---------|---------|-------|
| fastmcp | >=3.0.0 | MCP framework - no 'description' param in constructor |
| aioimaplib | >=1.0.0 | Async IMAP - specific LIST syntax required |
| aiosmtplib | >=3.0.0 | Async SMTP |
| pydantic | >=2.0.0 | Configuration validation |
| pydantic-settings | >=2.0.0 | Environment variable loading |

## Security Checklist

| Item | Status | Notes |
|------|--------|-------|
| SSL certificate verification | ✅ | `ssl.create_default_context()` |
| TLS 1.2 minimum | ✅ | `context.minimum_version` |
| Credentials from env only | ✅ | No hardcoded secrets |
| SecretStr for passwords | ✅ | Not in repr/logs |
| Rate limiting | ✅ | Token bucket |
| Audit logging | ✅ | JSON structured |
| Path traversal protection | ✅ | Workspace confinement |
| Recipient whitelist | ✅ | Optional filtering |
| Input validation | ✅ | IMAP criteria, email addresses |
| Error message sanitization | ✅ | Generic errors to client |
