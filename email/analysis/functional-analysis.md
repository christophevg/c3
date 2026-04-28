# Functional Analysis: Email Gateway MCP Server

**Date**: 2026-04-28
**Version**: 0.1.1
**Analyst**: Functional Analyst Agent

---

## Executive Summary

The Email Gateway MCP Server is a Model Context Protocol (MCP) wrapper around IMAP and SMTP email protocols. It provides Claude Code with email capabilities through a well-defined tool interface, enabling email reading, searching, sending, and management operations without exposing the underlying protocol complexity.

---

## System Overview

### Purpose

Provide email capabilities to Claude Code through the Model Context Protocol, enabling:
- Email reading and searching via IMAP
- Email sending and replying via SMTP
- Email organization (move, delete, mark as read)
- Attachment handling (download)

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code (MCP Client)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ MCP Protocol
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Email MCP Server                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  FastMCP     │  │ Connection  │  │ Safety Layer        │  │
│  │  Server      │  │ Pool        │  │ ┌─────────────────┐ │  │
│  │              │  │             │  │ │ Rate Limiter    │ │  │
│  │  Tools:      │  │ ┌─────────┐ │  │ └─────────────────┘ │  │
│  │  - list_*    │  │ │ IMAP    │ │  │ ┌─────────────────┐ │  │
│  │  - search_*  │  │ │ Client  │ │  │ │ Audit Logger   │ │  │
│  │  - get_*     │  │ └─────────┘ │  │ └─────────────────┘ │  │
│  │  - send_*    │  │ ┌─────────┐ │  │ ┌─────────────────┐ │  │
│  │  - move_*    │  │ │ SMTP    │ │  │ │ Whitelist      │ │  │
│  │  - delete_*  │  │ │ Client  │ │  │ └─────────────────┘ │  │
│  │  - mark_*    │  │ └─────────┘ │  └─────────────────────┘  │
│  └─────────────┘  └─────────────┘                            │
│  ┌─────────────┐  ┌─────────────┐                            │
│  │  Resources  │  │  Prompts    │                            │
│  │  - accounts │  │  - compose  │                            │
│  │  - folders  │  │  - summarize│                            │
│  └─────────────┘  └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ IMAP (993) / SMTP (587/465)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Email Providers                            │
│  Gmail, Outlook, iCloud, Fastmail, etc.                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. FastMCP Server Layer

**Location**: `src/email_mcp/server.py`

**Responsibility**: MCP protocol implementation and tool definition

**Components**:

| Component | Type | Description |
|-----------|------|-------------|
| `mcp` | FastMCP instance | Main MCP server, named "email" |
| Tools | 10 functions | IMAP/SMTP operations exposed as MCP tools |
| Resources | 2 handlers | Account and folder listing as MCP resources |
| Prompts | 3 templates | Email composition and summarization assistance |

**Tool Catalog**:

| Tool | Protocol | Operation | Description |
|------|----------|-----------|-------------|
| `list_accounts` | Config | Read | List configured email accounts |
| `list_folders` | IMAP | Read | List mailboxes for an account |
| `search_emails` | IMAP | Read | Search messages with IMAP criteria |
| `get_email` | IMAP | Read | Fetch a single message |
| `download_attachment` | IMAP | Read | Download attachment to workspace |
| `send_email` | SMTP | Write | Send a new email |
| `reply_email` | SMTP | Write | Reply to an existing thread |
| `move_email` | IMAP | Write | Move message between folders |
| `delete_email` | IMAP | Write | Remove message permanently |
| `mark_email_read` | IMAP | Write | Mark message as read/unread |

### 2. Connection Pool Layer

**Location**: `src/email_mcp/connections/pool.py`

**Responsibility**: Connection lifecycle management for multiple accounts

**Design Pattern**: Singleton with lazy initialization

**Key Functions**:

| Function | Purpose |
|----------|---------|
| `get_pool()` | Get or create global connection pool singleton |
| `get_imap_client(account)` | Get/create IMAP client with rate limiting |
| `get_smtp_client(account)` | Get/create SMTP client with rate limiting |
| `disconnect_all()` | Clean disconnect of all clients |

**Connection Model**:

```
ConnectionPool (Singleton)
├── _imap_clients: dict[str, IMAPClient]
├── _smtp_clients: dict[str, SMTPClient]
├── _accounts: list[EmailAccount]
└── _client_lock: asyncio.Lock
```

**Rate Limit Integration**:
- IMAP: 60 requests/minute/account (configurable)
- SMTP: 100 sends/hour/account (configurable)
- Rate limit checked before client acquisition
- Blocked requests raise `RuntimeError`

### 3. IMAP Client Layer

**Location**: `src/email_mcp/imap/client.py`

**Responsibility**: IMAP protocol operations for email retrieval

**Key Operations**:

| Operation | IMAP Commands | Notes |
|-----------|---------------|-------|
| `connect()` | CAPABILITY, LOGIN/AUTHENTICATE | OAuth2 or password auth |
| `list_folders()` | LIST "" "*" | Provider-specific quoting |
| `select_folder()` | SELECT | Required before search/fetch |
| `search()` | SEARCH | Criteria validation with regex |
| `fetch_message()` | FETCH BODY.PEEK[] | Full message download |
| `move_message()` | COPY + STORE + EXPUNGE | Non-atomic (known issue) |
| `delete_message()` | STORE + EXPUNGE | Permanent removal |
| `mark_message()` | STORE | Flag manipulation |
| `download_attachment()` | FETCH BODY.PEEK[] + decode | Workspace-confined |

**Security Measures**:

| Measure | Implementation |
|---------|----------------|
| TLS 1.2 minimum | `ssl.create_default_context()` with `minimum_version` |
| Path traversal | Workspace confinement + basename + hash prefix |
| IMAP injection | Criteria regex validation |
| Workspace restriction | `EMAIL_WORKSPACE` environment variable |

**Known Issues**:

| Issue | Severity | Description |
|-------|----------|-------------|
| C1: IMAP race condition | Critical | Lock only protects `connect()`, not operations |
| H9: Inefficient attachment | High | Fetches entire message for one attachment |
| M1: Unsafe disconnect | Medium | No state check before `logout()` |

### 4. SMTP Client Layer

**Location**: `src/email_mcp/smtp/client.py`

**Responsibility**: SMTP protocol operations for email sending

**Key Operations**:

| Operation | SMTP Commands | Notes |
|-----------|---------------|-------|
| `send_email()` | EHLO, STARTTLS/AUTH, MAIL, RCPT, DATA | Full composition |
| `reply_email()` | Same + In-Reply-To, References | Thread continuation |
| `forward_email()` | Exists but not exposed as tool | Dead code (M15) |

**Security Measures**:

| Measure | Implementation |
|---------|----------------|
| TLS 1.2 minimum | Same as IMAP |
| Recipient whitelist | Domain and address filtering |
| Address validation | Basic regex for email format |
| Attachment size | Unbounded (known issue M8) |

**Whitelist Enforcement**:

```python
# RecipientWhitelist.is_allowed(email)
if not whitelist.is_allowed(recipient):
    raise WhitelistError(f"Recipient not in whitelist: {recipient}")
```

**Known Issues**:

| Issue | Severity | Description |
|-------|----------|-------------|
| C3: Whitelist bypass | Critical | `reply_email()` skips whitelist check |
| C5: Exception swallowing | Critical | SMTP exceptions lose context |
| H4: CRLF injection | High | Headers not sanitized |
| M8: Unbounded attachments | Medium | No size limit, OOM risk |

### 5. Configuration Layer

**Location**: `src/email_mcp/config.py`

**Responsibility**: Environment-based configuration loading

**Configuration Hierarchy**:

```
ServerConfig (Pydantic Settings)
├── accounts_json: str | None          # Multi-account JSON
├── Single account fallback:
│   ├── imap_host, smtp_host, username
│   └── password, oauth2_token
├── Rate limiting:
│   └── imap_requests_per_minute (60)
│   └── smtp_sends_per_hour (100)
└── Whitelist:
    ├── recipient_whitelist_json
    ├── recipient_whitelist_domains
    └── recipient_whitelist_addresses
```

**Environment Variable Prefix**: `EMAIL_`

**Example Configuration**:

```bash
# Single account
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_USERNAME=user@gmail.com
EMAIL_PASSWORD=app-password

# Multiple accounts (JSON)
EMAIL_ACCOUNTS_JSON='[{"name": "work", ...}]'

# Whitelist
EMAIL_RECIPIENT_DOMAINS=example.com,trusted.org
```

### 6. Safety Layer

**Location**: `src/email_mcp/safety/`

**Components**:

#### Rate Limiter (`rate_limiter.py`)

- Token bucket algorithm per account
- Separate limits for IMAP (per minute) and SMTP (per hour)
- Async-compatible with `acquire()` and `release()`
- Known issue: Uses `time.time()` instead of `time.monotonic()` (H8)

#### Audit Logger (`audit.py`)

- JSON-structured logging for sensitive operations
- Logs: auth attempts, email sends, attachment downloads, rate limits
- Fields: timestamp, account, operation, success/failure, error message
- Known issue: Potential hostname leakage in error logs (M12)

---

## Data Flow Analysis

### Email Read Flow

```
Claude Code                MCP Server                IMAP Client              IMAP Server
    │                          │                          │                        │
    │ list_accounts            │                          │                        │
    ├─────────────────────────>│ get_pool()              │                        │
    │                          ├─────────────────────────>│                        │
    │                          │ get_accounts()           │                        │
    │                          │<─────────────────────────┤                        │
    │<─────────────────────────┤                          │                        │
    │                          │                          │                        │
    │ search_emails(account)   │                          │                        │
    ├─────────────────────────>│ get_imap_client()        │                        │
    │                          ├─────────────────────────>│ connect()              │
    │                          │                          ├───────────────────────>│
    │                          │                          │<───────────────────────┤
    │                          │                          │ search()               │
    │                          │                          ├───────────────────────>│
    │                          │                          │<───────────────────────┤
    │                          │<─────────────────────────┤                        │
    │<─────────────────────────┤                          │                        │
    │                          │                          │                        │
    │ get_email(account, id)   │                          │                        │
    ├─────────────────────────>│ get_imap_client()        │                        │
    │                          ├─────────────────────────>│ fetch_message()        │
    │                          │                          ├───────────────────────>│
    │                          │                          │<───────────────────────┤
    │                          │<─────────────────────────┤                        │
    │<─────────────────────────┤                          │                        │
```

### Email Send Flow

```
Claude Code                MCP Server                SMTP Client              SMTP Server
    │                          │                          │                        │
    │ send_email(to, subject)  │                          │                        │
    ├─────────────────────────>│ whitelist.filter()       │                        │
    │                          │<─────────────────────────┤                        │
    │                          │ get_smtp_client()        │                        │
    │                          ├─────────────────────────>│ connect()              │
    │                          │                          ├───────────────────────>│
    │                          │                          │<───────────────────────┤
    │                          │                          │ send()                 │
    │                          │                          ├───────────────────────>│
    │                          │                          │<───────────────────────┤
    │                          │ audit.log_email_sent()    │                        │
    │                          │<─────────────────────────┤                        │
    │<─────────────────────────┤                          │                        │
```

---

## Security Model

### Threat Mitigation

| Threat | Mitigation | Status |
|--------|-----------|--------|
| Credential exposure | `SecretStr`, no logging | ✅ Implemented |
| MITM attacks | TLS 1.2 minimum, cert verification | ✅ Implemented |
| Path traversal | Workspace confinement, basename, hash | ⚠️ Symlink issue (M5) |
| Recipient spam | Whitelist filtering | ⚠️ Bypass in reply (C3) |
| Rate limiting abuse | Token bucket per account | ⚠️ Non-monotonic clock (H8) |
| IMAP injection | Criteria regex | ⚠️ Single quote issue (H3) |
| Header injection | None | ❌ CRLF vulnerability (H4) |
| DoS via attachments | None | ❌ Unbounded reads (M8) |

### Authentication Methods

| Method | Support | Notes |
|--------|---------|-------|
| Password | ✅ | App-specific passwords recommended |
| OAuth2 | ✅ | Gmail/Outlook support |
| XOAuth2 | ✅ | Via `oauth2_token` config |

---

## Error Handling

### Error Categories

| Category | Response to Client | Audit Log | Example |
|----------|-------------------|-----------|---------|
| Account not found | `ToolError("Account not found")` | ✅ | Invalid account name |
| Rate limited | `ToolError("Rate limit exceeded")` | ✅ | Too many requests |
| Provider error | `ToolError("Failed to ...")` | ✅ | Connection failure |
| Whitelist violation | `WhitelistError` | ✅ | Recipient not allowed |
| Validation error | `ToolError` | ✅ | Invalid criteria |

### Known Error Issues

| Issue | Severity | Description |
|-------|----------|-------------|
| C2: RuntimeError misclassification | Critical | All `RuntimeError` mapped to "Rate limit exceeded" |
| M10: Path leakage | Medium | `FileNotFoundError` exposes filesystem paths |

---

## Performance Characteristics

### Connection Pooling

- **Singleton pattern**: One pool per process
- **Lazy initialization**: Clients created on first use
- **No reconnection**: Broken connections require restart (known issue)

### Rate Limiting

| Protocol | Limit | Window | Algorithm |
|----------|-------|--------|-----------|
| IMAP | 60 requests | 1 minute | Token bucket |
| SMTP | 100 sends | 1 hour | Token bucket |

### Memory Considerations

| Operation | Memory Impact | Known Issue |
|-----------|---------------|-------------|
| Message fetch | Full body in memory | - |
| Attachment download | Full message fetched | H9: Inefficient |
| Attachment upload | Full file in memory | M8: Unbounded |
| Rate limiter | Unbounded dict growth | - |

---

## Integration Points

### MCP Tools Exposed

```python
# Read operations
list_accounts() -> list[dict]
list_folders(account) -> list[dict]
search_emails(account, folder, criteria, limit) -> dict
get_email(account, message_id, folder) -> dict
download_attachment(account, message_id, filename, output_dir, folder) -> dict

# Write operations
send_email(account, to, subject, body, cc, bcc, html_body, attachments) -> dict
reply_email(account, message_id, to, subject, body, folder, html_body, attachments) -> dict
move_email(account, message_id, source_folder, dest_folder) -> dict
delete_email(account, message_id, folder) -> dict
mark_email_read(account, message_id, folder) -> dict
```

### MCP Resources Exposed

```python
# Dynamic resources
list_accounts_resource() -> list[dict]
list_folders_resource(account) -> list[dict]
```

### MCP Prompts Exposed

```python
# Composition assistance
compose_email_prompt(subject, to, context) -> str
summarize_email_prompt(email_content) -> str
analyze_email_prompt(email_content) -> str
```

---

## Known Issues Summary

### Critical (Must Fix)

| ID | Issue | Impact |
|----|-------|--------|
| C1 | IMAP connection race condition | Data corruption, wrong messages |
| C2 | RuntimeError misclassified as rate limit | User confusion on auth failures |
| C3 | reply_email whitelist bypass | Security vulnerability |
| C4 | Attachment symlink race | Path traversal vulnerability |
| C5 | SMTP exception swallowing | Debugging impossible |

### High Priority

| ID | Issue | Impact |
|----|-------|--------|
| H1-H10 | Various issues | See TODO.md for details |

### Medium Priority

| ID | Issue | Impact |
|----|-------|--------|
| M1-M26 | Various issues | See TODO.md for details |

### Low Priority

| ID | Issue | Impact |
|----|-------|--------|
| L1-L12 | Various issues | See TODO.md for details |

---

## Test Coverage

### Implemented Tests

| Test File | Coverage |
|-----------|----------|
| `test_config.py` | Configuration parsing, secret masking |
| `test_rate_limiter.py` | Token bucket algorithm |
| `test_whitelist.py` | Domain and address filtering |
| `test_path_traversal.py` | Workspace confinement logic |

### Missing Tests (H10)

| Layer | Status |
|-------|--------|
| IMAPClient | ❌ No tests |
| SMTPClient | ❌ No tests |
| ConnectionPool | ❌ No tests |
| Server tools | ❌ No tests |
| OAuth2 paths | ❌ No tests |

---

## Future Enhancements

See [TODO.md](../TODO.md) for prioritized backlog items.

Key improvements planned:
1. Fix critical concurrency and security issues (C1-C5)
2. Add comprehensive test coverage
3. Implement efficient attachment download (BODYSTRUCTURE)
4. Add reconnection logic for dropped connections
5. Expose `forward_email` as tool (currently dead code)

---

## References

- [FastMCP Documentation](https://github.com/anthropics/fastmcp)
- [aioimaplib](https://github.com/bamthomas/aioimaplib)
- [aiosmtplib](https://github.com/cole/aiosmtplib)
- [IMAP RFC 3501](https://datatracker.ietf.org/doc/html/rfc3501)
- [SMTP RFC 5321](https://datatracker.ietf.org/doc/html/rfc5321)
- [Code Review Findings](../reviews/)