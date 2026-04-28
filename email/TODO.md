# TODO - Email MCP Server

## Backlog (Prioritized)

### P1 - Critical

- [x] **C1: Fix IMAP connection race condition** — `imap/client.py:34-38`
  `_lock` only protects `connect()`, not individual operations. Concurrent tool calls interleave IMAP commands.
  Acceptance: Add operation-level `asyncio.Lock` or checkout/checkin connection pool

- [x] **C2: Fix RuntimeError misclassified as rate limits** — `server.py:62-63,97-98,129-131`
  All `RuntimeError` exceptions are mapped to "Rate limit exceeded", including auth failures, protocol errors, and incorrect `message_id` in `get_email` / `download_attachment`.
  Affects: `list_folders`, `search_emails`, `get_email`, `download_attachment`, `send_email`, `reply_email`, `move_email`, `delete_email`, `mark_email_read`.
  Acceptance: Introduce custom `RateLimitError` or distinct error tuple from `ConnectionPool`; ensure non-rate-limit `RuntimeError`s surface as appropriate generic or specific errors.
  **Fixed:** Added `RateLimitError` custom exception in `connections/pool.py`, raised from pool on rate limit exhaustion. Updated all tool handlers in `server.py` to catch `RateLimitError` specifically instead of generic `RuntimeError`. Regression tests in `tests/test_server.py`.

- [ ] **C3: Fix `reply_email()` whitelist bypass** — `smtp/client.py:116-140`
  `reply_email()` bypasses recipient whitelist check - security vulnerability.
  Acceptance: Add same whitelist check as `send_email()` before sending

- [ ] **C4: Fix attachment download symlink race** — `imap/client.py:288-313`
  Workspace confinement can be bypassed via symlink between check and write.
  Acceptance: Use `os.path.realpath()` to resolve final path and verify within workspace

- [ ] **C5: Fix SMTP exception chain swallowing** — `smtp/client.py:196-197`
  SMTP exceptions lose all error details - original exception is swallowed.
  Acceptance: Use `raise RuntimeError(...) from e` to preserve exception chain

### P2 - High

- [ ] **H1: Fix non-atomic `move_message`** — `imap/client.py:214-223`
  COPY → STORE+Deleted → EXPUNGE is not atomic. If STORE/EXPUNGE fails after COPY, message exists in both folders.
  Acceptance: Use IMAP `MOVE` extension if available, or document limitation clearly

- [ ] **H2: Fix auth exception handling** — `imap/client.py:69-71`
  `except Exception as e:` catches connection errors, DNS failures, protocol bugs, misreporting as auth failures.
  Acceptance: Catch specific exceptions (`aioimaplib.Abort`, `TimeoutError`) separately from auth errors

- [ ] **H3: Tighten IMAP criteria regex** — `imap/client.py:24`
  IMAP criteria regex allows single quotes which can break out of quoted strings in certain IMAP commands.
  Acceptance: Tighten regex or use proper IMAP command escaping

- [ ] **H4: Add CRLF injection protection** — `smtp/client.py:159-197`
  `_send()` method doesn't validate `in_reply_to` or `references` headers for header injection.
  Acceptance: Sanitize header values to prevent CRLF injection attacks

- [ ] **H5: Sanitize download_attachment errors** — `server.py:170-171`
  `download_attachment` passes raw exception message to user - may leak internal details.
  Acceptance: Use generic error message and log details separately

- [ ] **H6: Add internationalized email validation** — `smtp/client.py:54-62`
  Email validation only checks format, not encoding (international domains/addresses).
  Acceptance: Consider using `email.utils` or library handling internationalized addresses

- [ ] **H7: Fix overly broad auth exception handling** — `imap/client.py:69`
  `except Exception:` catches connection errors, DNS failures, protocol bugs.
  Acceptance: Catch specific exceptions separately from auth errors

- [ ] **H8: Replace `time.time()` with `time.monotonic()`** — `safety/rate_limiter.py:31`
  Non-monotonic clock vulnerable to system clock jumps - breaks expiry logic.
  Acceptance: Replace with `time.monotonic()`

- [ ] **H9: Optimize attachment download** — `imap/client.py:291`
  Fetches `BODY.PEEK[]` (entire message) to extract one attachment - excessive memory/bandwidth.
  Acceptance: Use `BODYSTRUCTURE` to find part number, fetch only `BODY.PEEK[<part>]`

- [ ] **H10: Add client layer tests** — `tests/`
  Zero tests for IMAPClient, SMTPClient, ConnectionPool, server.py tools, OAuth2 paths.
  Acceptance: Mock-based tests for all operations, >80% coverage

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

- [ ] **M1: Guard unsafe `disconnect()`** — `imap/client.py:78`
  `logout()` called on potentially broken connection without state check - can raise unhandled exceptions.
  Acceptance: Guard with try/except or check connection health before logout

- [ ] **M2: Complete `disconnect_all()` for SMTP** — `connections/pool.py:92-98`
  Iterates only IMAP clients, clears SMTP dict without calling disconnect logic.
  Acceptance: Add `disconnect()` to `SMTPClient` and call it in `disconnect_all()`

- [ ] **M3: Cache JSON parsing in `get_accounts()`** — `config.py:145-166`
  Repeated JSON parsing from scratch on every call.
  Acceptance: Cache parsed result on first access

- [ ] **M4: Fix rudimentary `.env` parser** — `config.py:15-30`
  Doesn't handle quoted values, inline comments, or escaped characters.
  Acceptance: Use `python-dotenv` as required dependency or skip gracefully

- [ ] **M5: Harden symlink traversal protection** — `imap/client.py:270-279`
  `Path.resolve()` follows symlinks - `relative_to()` may pass incorrectly if workspace contains symlinks.
  Acceptance: Use `os.path.realpath()` on both paths before `relative_to()` check

- [ ] **M6: Remove dead code in `tools/definitions.py`** — `tools/definitions.py:1-324`
  Entire file defines Pydantic classes that FastMCP does not consume (infers schemas from signatures).
  Acceptance: Delete file entirely or wire into build

- [ ] **M7: Add HTML body fallback** — `imap/client.py:328-342`
  `_get_body()` returns `""` for HTML-only emails.
  Acceptance: Fall back to `text/html` part when no `text/plain` exists

- [ ] **M8: Add attachment size limits** — `smtp/client.py:205-218`
  `_add_attachments()` reads entire files into memory without size limits - OOM risk.
  Acceptance: Add configurable max attachment size, reject oversized files

- [ ] **M9: Add error sanitization for resources** — `server.py:391-405`
  `list_accounts_resource`, `list_folders_resource` have no try/except blocks.
  Acceptance: Wrap resource handlers with same exception-sanitization pattern as tools

- [ ] **M10: Fix path leakage in tool errors** — `server.py:227-228`
  `FileNotFoundError` sends full filesystem path to client.
  Acceptance: Sanitize to generic error message

- [ ] **M11: Cache whitelist lowercase lists** — `config.py:72-86`
  `RecipientWhitelist.is_allowed()` rebuilds lowercase lists on every call.
  Acceptance: Store domains/addresses lowercased at initialization

- [ ] **M12: Fix fragile folder parsing** — `imap/client.py:98-104`
  Splits on `"` which breaks if folder names contain quotes.
  Acceptance: Use proper IMAP LIST response parser or document limitation

- [ ] **M13: Make `reply_email` accept `list[str]`** — `server.py:245,191`
  API inconsistency: `reply_email` takes `to: str` while `send_email` takes `to: list[str]`.
  Acceptance: Accept `list[str]` for consistency or document intentional difference

- [ ] **M14: Remove deprecated pytest-asyncio fixture** — `tests/conftest.py:14-19`
  `event_loop` fixture conflicts with `asyncio_mode = "auto"` in `pyproject.toml`.
  Acceptance: Remove fixture, rely on auto mode

- [ ] **M15: Expose or remove `forward_email` method** — `smtp/client.py:142-157`
  Method exists but is not exposed as MCP tool - dead code.
  Acceptance: Expose as tool or remove

- [ ] **M16: Extract exception handling helper** — `server.py`
  ~72 lines of identical exception handling boilerplate duplicated across all tools.
  Acceptance: Extract `_handle_tool_errors()` decorator or helper

- [ ] **M17: Genericize client getters** — `connections/pool.py:50-90`
  `get_imap_client()` and `get_smtp_client()` are ~90% identical.
  Acceptance: Introduce generic `_get_client()` method

- [ ] **M18: Extract TLS context utility** — `imap/client.py`, `smtp/client.py`
  Duplicate TLS context setup in both clients.
  Acceptance: Extract shared `create_tls_context()` utility

- [ ] **M19: Standardize tool return types** — `server.py:311,346,379`
  Mutation tools return different key sets.
  Acceptance: Standardize return type: `{status, message_id, folder?, timestamp}`

- [ ] **M20: Standardize error handling patterns** — `imap/client.py`
  Methods return different types on error: `True`, `bool`, sparse dict, raise exception.
  Acceptance: Establish consistent pattern

- [ ] **M21: Fix redundant `select_folder()` calls** — `imap/client.py:135,172`
  Methods call `select_folder()` (which calls `connect()`) then also call `connect()` directly.
  Acceptance: Remove redundant calls

- [ ] **M22: Remove unused `use_ssl` field** — `config.py:50`
  Field defined but never read - neither IMAPClient nor SMTPClient references it.
  Acceptance: Remove or wire into connection logic

- [ ] **M23: Fix type hint in `_send()`** — `smtp/client.py:159`
  Types `msg: EmailMessage` but `send_email()` passes `MIMEMultipart` (not a subclass).
  Acceptance: Change type hint to `email.message.Message` or union type

- [ ] **M24: Add `validate_email()` to `reply_email`** — `smtp/client.py:124`
  `send_email()` validates addresses but `reply_email()` doesn't.
  Acceptance: Add `validate_email(to)` before calling `_send()`

- [ ] **M25: Improve test naming** — `tests/test_path_traversal.py`
  `test_valid_output_dir` actually asserts that `/tmp` (outside workspace) is rejected.
  Acceptance: Rename to `test_invalid_output_dir_rejected`

- [ ] **M26: Fix weak secret assertion** — `tests/test_config.py:62`
  Passes if `"SecretStr"` appears anywhere in repr, even if raw value is leaked elsewhere.
  Acceptance: Assert raw secret is absent and field is masked

- [ ] **Make rate limits configurable at runtime**
  - Environment variables for IMAP/SMTP limits
  - Per-account rate limit override
  - Acceptance: Limits configurable without code changes

- [ ] **Add IMAP connection checkout/checkin pool (future enhancement)**
  - Replace single `IMAPClient` per account with a pool of reusable connections
  - Enables true concurrency for same-account operations without command interleaving
  - Requires connection health monitoring, SELECT state tracking, and reconnection logic
  - See `analysis/api-c1-race-condition.md` for architecture decision and tradeoffs
  - Acceptance: Pool size configurable, connections checked out per operation, health validated on checkin

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

- [ ] **L1: Document empty env string behavior** — `config.py`
  `env_parse_none_str=""` means `EMAIL_RECIPIENT_DOMAINS=""` becomes `None`.
  Acceptance: Document behavior explicitly or remove `env_parse_none_str`

- [ ] **L2: Define search limit constants** — `server.py:73`
  Magic numbers `ge=1, le=500` should be named constants.
  Acceptance: Define `DEFAULT_SEARCH_LIMIT = 50`, `MAX_SEARCH_LIMIT = 500`

- [ ] **L3: Document `DEFAULT_WORKSPACE` portability** — `imap/client.py:21`
  Uses `/tmp` which may not exist on all systems.
  Acceptance: Use `platformdirs` or document environment variable

- [ ] **L4: Improve email regex for quoted parts** — `smtp/client.py:21`
  Regex doesn't handle all valid addresses (quoted local parts).
  Acceptance: Consider using `email_validator` library

- [ ] **L5: Extract `\\Deleted` constant** — `imap/client.py:220,238`
  Magic string appears in multiple places.
  Acceptance: Define `DELETED_FLAG = "\\Deleted"`

- [ ] **L6: Extract `INBOX` constant** — `imap/client.py:130,169,230`
  Magic string appears as default in multiple signatures.
  Acceptance: Define `DEFAULT_FOLDER = "INBOX"`

- [ ] **L7: Extract `ALL` constant** — `imap/client.py:131`
  Magic string appears as default search criteria.
  Acceptance: Define `DEFAULT_SEARCH_CRITERIA = "ALL"`

- [ ] **L8: Document `forward_email` attachment limitation** — `smtp/client.py:142-157`
  Forwarded attachments missing - doesn't carry over original attachments.
  Acceptance: Document limitation or implement MIME part forwarding

- [ ] **L9: Fix undefined variable reference** — `README.md` / `.mcp.json`
  `${CLAUDE_PLUGIN_ROOT}` is referenced but not a standard variable.
  Acceptance: Verify actual mechanism or use concrete path

- [ ] **L10: Document lock purpose** — `imap/client.py:34`
  Lock per-client but connection also per-client - appears to provide no concurrency protection.
  Acceptance: Document why it's needed or move to connection pool level

- [ ] **L11: Optimize whitelist checks** — `config.py:72-86`
  Lowercase lists rebuilt on every call - inefficient.
  Acceptance: Pre-compute lowercase lists at initialization (also M11)

- [ ] **L12: Fix silent partial failure in `fetch_message`** — `imap/client.py:15-165`
  Returns sparse dict (only `id`/`folder`) if `raw_message` not found.
  Acceptance: Raise clear error instead of returning partial data

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
