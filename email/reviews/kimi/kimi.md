# Email MCP Server - Code Review

**Date**: 2026-04-28
**Reviewer**: Code Reviewer Agent (via Claude Code)
**Scope**: `/Users/xtof/Workspace/agentic/c3/email/` - Full baseline review of the Email MCP Server codebase (IMAP/SMTP operations, connection pooling, safety, tests)

## Summary

The Email MCP Server is a well-structured async codebase with clear module separation, good use of Pydantic for configuration, and sensible security defaults (TLS 1.2, SecretStr, path traversal protection, recipient whitelisting). However, it has **critical concurrency bugs** in the IMAP client, **severe error classification issues** that mislead users, and **significant test coverage gaps** in the IMAP/SMTP client layers. The code is **not ready for production** without addressing the critical and high-priority findings below.

---

## Design Assessment

### Strengths
- Clean modular architecture (`config`, `connections`, `imap`, `smtp`, `tools`, `safety`)
- Async-first design with `aioimaplib` and `aiosmtplib`
- Pydantic models with `SecretStr` for credential handling
- TLS 1.2 minimum enforcement and certificate verification
- Recipient whitelist with domain and address filtering
- Structured audit logging (`safety/audit.py`)

### Concerns
- **Singleton `ConnectionPool`** reuses one `IMAPClient` per account, but `IMAPClient` only locks connection *establishment*, not operations. IMAP is a sequential protocol - this is a fundamental design flaw for concurrent use.
- **Dead code in `tools/definitions.py`** - Pydantic schema classes are defined but never wired into FastMCP (FastMCP infers schemas from function signatures). These add maintenance burden without value.
- **Sequence-number based IMAP API** - Message IDs are sequence numbers, not UIDs, making them volatile across folder changes. This is acceptable if documented, but risky for a multi-turn agent.

---

## Quality Issues

### Critical (Must Fix)

| ID | Location | Issue | Recommendation |
|----|----------|-------|----------------|
| C1 | `src/email_mcp/imap/client.py` | **IMAP connection race condition.** `IMAPClient._lock` (line 34/38) only protects `connect()`, not individual operations (`fetch_message`, `search`, `move_message`, etc.). Concurrent tool calls on the same account interleave IMAP commands on the same connection, corrupting the IMAP session or fetching wrong messages. | Add an operation-level `asyncio.Lock` to `IMAPClient` that guards every command sent to `_client`, or switch to a checkout/checkin connection pool where each operation gets exclusive connection access. |
| C2 | `src/email_mcp/server.py` | **Misclassification of all `RuntimeError` as rate limits.** Lines 62-63, 97-98, 129-131, etc. catch `RuntimeError` and raise `ToolError("Rate limit exceeded...")`. However, `IMAPClient.connect()` (line 71), `select_folder()`, `fetch_message()`, etc. all raise `RuntimeError` for auth failures, protocol errors, and folder-not-found. **Users are told "Rate limit exceeded" when their password is wrong.** (Also noted in `TODO.md`). | Introduce a custom `RateLimitError` or return a distinct error tuple from `ConnectionPool.get_imap_client()`. Only map that specific exception to the rate-limit user message. |

### High Priority

| ID | Location | Issue | Recommendation |
|----|----------|-------|----------------|
| H1 | `src/email_mcp/imap/client.py` | **Non-atomic `move_message`.** Lines 214-223: `copy` -> `store +Deleted` -> `expunge`. If `store` or `expunge` fails after `copy` succeeds, the message exists in both folders. If `copy` fails after `store` on a retry, data may be lost. | Use the IMAP `MOVE` extension if available, or wrap the sequence in a retry/rollback strategy. Document the limitation clearly. |
| H2 | `src/email_mcp/smtp/client.py` | **Exception swallowing.** Line 197: `except aiosmtplib.SMTPException as e: raise RuntimeError("Failed to send email...")` discards the original exception chain. Operators cannot diagnose SMTP errors from logs. | Use `raise RuntimeError(...) from e` to preserve the exception chain. |
| H3 | `src/email_mcp/imap/client.py` | **Overly broad auth exception handling.** Line 69: `except Exception as e:` catches connection errors, DNS failures, and protocol bugs, misreporting them as authentication failures in logs. | Catch specific exceptions (`aioimaplib.Abort`, `TimeoutError`, etc.) separately from auth errors. |
| H4 | `src/email_mcp/safety/rate_limiter.py` | **Non-monotonic clock.** Line 31 uses `time.time()` for window expiry. If the system clock jumps backwards, expired requests remain in the bucket forever; if forwards, valid requests are incorrectly expired. | Replace `time.time()` with `time.monotonic()`. |
| H5 | `src/email_mcp/imap/client.py` | **Inefficient attachment download.** Line 291: `download_attachment` fetches `BODY.PEEK[]` (the entire message) to extract one attachment. For large emails this causes excessive memory and bandwidth usage. | Use `BODYSTRUCTURE` to find the attachment part number, then fetch only `BODY.PEEK[<part>]`. |
| H6 | `tests/` | **Severe under-coverage of client and server layers.** Only `test_config.py`, `test_rate_limiter.py`, `test_path_traversal.py`, and `test_whitelist.py` exist. **Zero tests** for `IMAPClient`, `SMTPClient`, `ConnectionPool`, `server.py` tools, or OAuth2 paths. | Add mock-based tests for all IMAP/SMTP operations and FastMCP tool wrappers. Target >80% coverage as noted in `TODO.md`. |

### Medium Priority

| ID | Location | Issue | Recommendation |
|----|----------|-------|----------------|
| M1 | `src/email_mcp/imap/client.py` | **Unsafe `disconnect()`.** Line 78 calls `logout()` on a potentially broken connection without checking state, which can raise unhandled exceptions. | Guard with try/except or check connection health before logout. |
| M2 | `src/email_mcp/connections/pool.py` | **`disconnect_all()` incomplete.** Line 92-98 iterates only `_imap_clients.values()` and clears `_smtp_clients` without calling any disconnect logic on SMTP instances. | If persistent SMTP connections are added later, this will leak. Add `disconnect()` to `SMTPClient` and call it here. |
| M3 | `src/email_mcp/config.py` | **Repeated JSON parsing.** `ServerConfig.get_accounts()` (line 145-166) parses `accounts_json` from scratch on every call. | Cache the parsed result on first access. |
| M4 | `src/email_mcp/config.py` | **Rudimentary `.env` parser.** `_load_dotenv()` (lines 15-30) does not handle quoted values, inline comments, or escaped characters. | Use `python-dotenv` as a required dependency, or use `importlib.metadata` to detect its presence and skip gracefully rather than parsing manually. |
| M5 | `src/email_mcp/imap/client.py` | **Symlink traversal bypass risk.** Lines 270-279: `Path.resolve()` follows symlinks. If `DEFAULT_WORKSPACE` or `output_dir` contains a symlink to `/`, `relative_to()` may pass incorrectly. | Use `os.path.realpath()` on both paths before the `relative_to` check, or explicitly reject paths containing symlinks. |
| M6 | `src/email_mcp/tools/definitions.py` | **Dead code.** The entire file defines Pydantic input/output classes that FastMCP does not consume (FastMCP infers schemas from annotated function signatures). | Remove unless needed for an external schema consumer. If kept, wire them into the build or document their purpose. |
| M7 | `src/email_mcp/imap/client.py` | **No HTML body fallback.** `_get_body()` (lines 328-342) returns `""` for HTML-only emails. | Fall back to returning the `text/html` part (or a stripped version) when no `text/plain` exists. |
| M8 | `src/email_mcp/smtp/client.py` | **Unbounded attachment reads.** `_add_attachments()` (lines 205-218) reads entire files into memory without size limits. A large attachment can OOM the process. | Add a configurable max attachment size and reject oversized files before reading. |
| M9 | `src/email_mcp/server.py` | **Resources lack error sanitization.** Lines 391-405 (`list_accounts_resource`, `list_folders_resource`) have no try/except blocks. Errors bubble up as raw tracebacks to the MCP client. | Wrap resource handlers with the same exception-sanitization pattern used for tools. |
| M10 | `src/email_mcp/server.py` | **Path leakage in tool errors.** Line 227-228: `except FileNotFoundError as e: raise ToolError(str(e))` sends the full file system path to the client. | Sanitize to `"Attachment not found"` without the path. |
| M11 | `src/email_mcp/config.py` | **Inefficient whitelist checks.** `RecipientWhitelist.is_allowed()` (lines 72-86) rebuilds lowercase lists on every call. | Store domains/addresses lowercased at initialization. |
| M12 | `src/email_mcp/imap/client.py` | **Fragile folder parsing.** `list_folders()` (lines 98-104) splits on `"` which breaks if folder names contain quotes. | Use a proper IMAP LIST response parser (e.g., `imaplib` tokenization logic) or document the limitation strictly. |
| M13 | `src/email_mcp/server.py` | **API inconsistency.** `reply_email` takes `to: str` (single recipient), while `send_email` takes `to: list[str]`. | Make `reply_email` accept `list[str]` for consistency, or document the intentional difference. |
| M14 | `tests/conftest.py` | **Deprecated pytest-asyncio fixture.** `event_loop` fixture (line 14-19) conflicts with `asyncio_mode = "auto"` in `pyproject.toml` and is deprecated in modern `pytest-asyncio`. | Remove the `event_loop` fixture; rely on `asyncio_mode = "auto"`. |

### Low Priority (Nitpicks)

| ID | Location | Issue | Recommendation |
|----|----------|-------|----------------|
| L1 | `src/email_mcp/config.py` | **Empty env string behavior.** `env_parse_none_str=""` means `EMAIL_RECIPIENT_DOMAINS=""` becomes `None` rather than enabling an empty whitelist. | Document this behavior explicitly, or remove `env_parse_none_str` if empty strings should be meaningful. |
| L2 | `src/email_mcp/safety/audit.py` | **Potential log leakage.** `log_auth_attempt` passes `str(e)` directly into audit logs (line 70). Some IMAP/SMTP libraries include server responses that might leak internal hostnames. | Sanitize or classify error details before logging. |
| L3 | `tests/test_path_traversal.py` | **Confusing test naming.** `test_valid_output_dir` actually asserts that `/tmp` (outside the default workspace) is *rejected*. | Rename to `test_invalid_output_dir_rejected`. |
| L4 | `tests/test_config.py` | **Weak secret assertion.** `test_secrets_not_in_repr` (line 62) passes if `"SecretStr"` appears anywhere in the repr, even if the raw value is leaked elsewhere in the string. | Assert that the raw secret is absent and that the field is masked. |
| L5 | `src/email_mcp/imap/client.py` | **Silent partial failure.** `fetch_message` returns a sparse dict (only `id`/`folder`) if `raw_message` is not found in the FETCH response, instead of raising. | Raise a clear error like `RuntimeError("Message content missing in FETCH response")`. |
| L6 | `src/email_mcp/smtp/client.py` | **Forwarded attachments missing.** `forward_email` does not carry over original attachments. | Document limitation or implement MIME part forwarding. |
| L7 | `README.md` / `.mcp.json` | **Undefined variable reference.** `${CLAUDE_PLUGIN_ROOT}` is referenced in the README example but is not a standard Claude Code variable. | Verify and document the actual mechanism, or use a concrete path example. |

---

## Code Quality & Duplication (Additional Round)

The following issues were identified in a follow-up review focused specifically on DRY violations and structural duplication.

### Duplicate Logic

| ID | Location | Issue | Recommendation |
|----|----------|-------|----------------|
| D1 | `src/email_mcp/imap/client.py` | **`move_message()` duplicates `delete_message()`.** Lines 220-223 inline `store +FLAGS \Deleted` + `expunge()` — the exact same logic already encapsulated in `delete_message()` (lines 234-241). | Refactor `move_message()` to call `self.delete_message(message_id, folder=source_folder, expunge=True)` after the copy succeeds. |
| D2 | `src/email_mcp/server.py` | **Identical exception handling boilerplate in every tool.** Lines 55-65, 90-100, 123-133, etc. repeat the same `except ValueError / except RuntimeError / except Exception` ladder across all 10+ tool functions. This is ~72 lines of duplicated boilerplate. | Extract a decorator or `_handle_tool_errors()` helper that maps exception types to `ToolError` messages. This also fixes the `RuntimeError` misclassification bug (C2). |
| D3 | `src/email_mcp/connections/pool.py` | **`get_imap_client()` and `get_smtp_client()` are ~90% identical.** Lines 50-69 and 71-90 differ only in: client class (`IMAPClient` vs `SMTPClient`), internal dict key (`_imap_clients` vs `_smtp_clients`), limiter variable (`imap_limiter` vs `smtp_limiter`), and error message string. | Introduce a generic `_get_client(account_name, client_type, client_dict, limiter, operation_name)` method. |
| D4 | `src/email_mcp/imap/client.py` + `src/email_mcp/smtp/client.py` | **Duplicate TLS context setup.** Both create `ssl.create_default_context()` and set `minimum_version = ssl.TLSVersion.TLSv1_2`. | Extract a shared `create_tls_context()` utility function. |

### Dead Code

| ID | Location | Issue | Recommendation |
|----|----------|-------|----------------|
| DC1 | `src/email_mcp/tools/definitions.py` | **Entire file is dead code.** The Pydantic input/output classes (lines 13-195) and `TOOL_SCHEMAS` dictionary (lines 199-324) are never imported by `server.py`. FastMCP 3.x infers schemas directly from annotated function signatures. | Delete `tools/definitions.py` entirely. Remove the `tools/` package if it has no other purpose. |
| DC2 | `src/email_mcp/config.py` | **`use_ssl` field is never read.** Line 50 defines `use_ssl: bool = Field(default=True, ...)`, but neither `IMAPClient.connect()` nor `SMTPClient._send()` references it. Both unconditionally use SSL/TLS. | Either wire `use_ssl` into connection logic or remove the field to eliminate confusion. |

### Type Safety & Validation

| ID | Location | Issue | Recommendation |
|----|----------|-------|----------------|
| T1 | `src/email_mcp/smtp/client.py` | **Type hint bug in `_send()`.** Line 159 types `msg: EmailMessage`, but `send_email()` passes a `MIMEMultipart` when `html_body` or `attachments` are present. `MIMEMultipart` is not a subclass of `EmailMessage`. | Change type hint to `email.message.Message` or a union type. |
| T2 | `src/email_mcp/smtp/client.py` | **`reply_email()` skips email validation.** `send_email()` validates all `to`, `cc`, and `bcc` addresses (lines 55-62), but `reply_email()` (line 124) accepts `to: str` and passes it directly to `_send()` without calling `validate_email()`. | Add `validate_email(to)` in `reply_email()` before calling `_send()`. |

### Why These Were Missed Initially

1. **File-at-a-time vs. cross-file review:** The `move_message()` duplication is within a single file and should have been caught, but the dead schema code requires a cross-file import analysis to discover that `definitions.py` is never imported.
2. **Focus on security and functionality over structural quality:** The initial review prioritized runtime safety (TLS, path traversal, rate limiting) and functional correctness. DRY violations and dead code were secondary concerns.
3. **Familiarity assumption with FastMCP:** A reviewer unfamiliar with FastMCP 3.x's schema inference might assume the `TOOL_SCHEMAS` dictionary and Pydantic classes are necessary wiring, not realizing the framework generates them automatically.
4. **Missing static analysis:** These issues are exactly what static analysis catches best — unused imports, unreferenced symbols, code duplication metrics. A purely manual review is more likely to miss this class of issue.

---

## Security Assessment

### Positive Security Measures
- TLS 1.2 minimum enforced consistently (`ssl.TLSVersion.TLSv1_2`)
- Certificate verification enabled via `ssl.create_default_context()`
- `SecretStr` prevents accidental credential logging
- Path traversal protection via workspace confinement + basename sanitization + hash prefix
- Recipient whitelist with domain/address filtering
- Rate limiting (token bucket) per account
- Structured audit logging

### Security Concerns
1. **IMAP injection regex** (`IMAP_CRITERIA_PATTERN`) is basic. While it blocks obvious injection, it may also reject valid IMAP search criteria (e.g., `SENTBEFORE 01-Jan-2024` contains a hyphen and digits, which passes, but complex criteria might not). More importantly, `aioimaplib` may handle quoting safely; verify whether the regex adds value or creates a false sense of security.
2. **Symlink bypass in workspace confinement** (M5 above) is the most realistic attack vector against the attachment download feature.
3. **Attachment DoS** (M8 above) - no size limits on uploads or downloads.
4. **Error misclassification** (C2) is a security UX issue: attackers probing credentials learn only "Rate limit exceeded", but legitimate users with bad passwords also see "Rate limit exceeded", causing confusion and hiding brute-force attempts from legitimate users.

---

## Test Coverage

- **Well tested**: Configuration parsing (`test_config.py`), rate limiting algorithm (`test_rate_limiter.py`), whitelist logic (`test_whitelist.py`)
- **Weakly tested**: Path traversal tests are mostly logic assertions, not actual client integration tests.
- **Not tested at all**:
  - `IMAPClient` (connect, list, select, search, fetch, move, delete, mark, download)
  - `SMTPClient` (send, reply, forward, attachment handling)
  - `ConnectionPool` (singleton lifecycle, client reuse, disconnect)
  - `server.py` tool wrappers (error mapping, parameter passing)
  - OAuth2 authentication paths
  - TLS configuration verification
  - Audit logging integration

**Recommendation**: Prioritize adding `unittest.mock` based tests for `IMAPClient` and `SMTPClient` using the fixtures already defined in `conftest.py`.

---

## Async/Concurrency & Resource Management

1. **IMAP connection sharing** (C1) is the dominant concurrency bug. The current design assumes one operation at a time per account, but MCP servers can receive concurrent tool calls.
2. **SMTP `_lock`** is correctly used to serialize sends per account, which is appropriate since `aiosmtplib.send()` is one-shot anyway.
3. **Connection lifecycle**: `IMAPClient` has no automatic reconnection. If the server drops the connection, all subsequent operations fail until the process restarts or `disconnect_all()` is called. Consider adding a health check or catching `BrokenPipeError`/`ConnectionResetError` in operations and triggering reconnect.
4. **Rate limiter memory growth**: `RateLimiter._requests` dict grows unbounded because keys are never removed even if an account is unused. In a long-running process with many account names, this is a slow memory leak.

---

## Recommendations (Prioritized)

1. **Fix C2 immediately** (error misclassification). Introduce `class RateLimitError(RuntimeError): pass` and update `ConnectionPool` and `server.py` to use it.
2. **Fix C1** (IMAP race condition). Add `self._op_lock = asyncio.Lock()` to `IMAPClient` and wrap every public method that issues IMAP commands with `async with self._op_lock:`.
3. **Add comprehensive client tests** (H6). Use the existing `mock_imap_client` and `mock_smtp_client` fixtures to cover all tool operations.
4. **Fix exception chaining** (H2) in `SMTPClient._send` and `IMAPClient.connect()`.
5. **Use `time.monotonic()`** (H4) in the rate limiter.
6. **Harden workspace confinement** (M5) against symlink traversal before deploying to production.
7. **Review `move_message` atomicity** (H1) and document the COPY+STORE+EXPUNGE behavior clearly in tool descriptions.

---

## Conclusion

**Status**: Changes Required - Not ready for production merge.

**Summary**: The Email MCP Server demonstrates solid architectural foundations and good security defaults for a v0.1.1 project. However, the **IMAP concurrency bug (C1)** and **error misclassification bug (C2)** are blockers that will cause data corruption and user confusion in real-world use. The test suite also needs significant expansion to cover the IMAP and SMTP client layers before this codebase can be considered maintainable.

**Next Steps**:
1. Fix C1 and C2 (estimated 1-2 hours)
2. Add client-level tests for IMAP and SMTP (estimated 3-4 hours)
3. Re-review after fixes, focusing on integration testing with a real IMAP provider (Gmail/iCloud)
