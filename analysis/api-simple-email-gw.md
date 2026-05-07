# API Architecture: simple-email-gw Package

**Date**: 2025-05-07
**Task**: Extract email MCP server from C3 plugin into standalone PyPI package
**Context**: C3 has an `email/` folder with MCP server implementation that needs to become `simple-email-gw`

## Summary

This document defines the architecture for extracting the email MCP server from the C3 plugin into a standalone Python package called `simple-email-gw`. The package will provide IMAP/SMTP client functionality with security features, connection pooling, and an MCP server entry point for use with `uvx --from simple-email-gw mcp`.

## Current Implementation Analysis

### Module Structure (email/src/email_mcp/)

| Module | Purpose | Lines | Dependencies |
|--------|---------|-------|--------------|
| `__init__.py` | Package metadata | 3 | None |
| `__main__.py` | Entry point wrapper | 7 | server |
| `server.py` | FastMCP server with 9 tools, 2 resources, 2 prompts | 467 | fastmcp, connections, imap, smtp |
| `config.py` | Pydantic settings, EmailAccount, RecipientWhitelist | 205 | pydantic-settings |
| `imap/client.py` | Async IMAP client with connection management | 428 | aioimaplib, config, safety |
| `smtp/client.py` | Async SMTP client with TLS 1.2+ enforcement | 311 | aiosmtplib, config, safety |
| `connections/pool.py` | Singleton connection pool with rate limiting | 117 | imap, smtp, safety |
| `safety/rate_limiter.py` | Token bucket rate limiter | 64 | asyncio |
| `safety/audit.py` | Audit logging (email sent, auth, rate limit) | 111 | logging, json |
| `safety/sanitize.py` | CRLF injection prevention | 163 | None |
| `tools/__init__.py` | (empty placeholder) | 1 | None |
| `tools/definitions.py` | (not yet implemented) | - | - |

### Dependencies (requirements.txt)

```
fastmcp>=3.0.0
aioimaplib>=1.0.0
aiosmtplib>=3.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
```

### Security Features

1. **Rate Limiting**: Token bucket algorithm (60/min IMAP, 100/hour SMTP per account)
2. **Audit Logging**: Structured JSON logs for email sent, auth, rate limits, downloads
3. **CRLF Injection Prevention**: Header sanitization for subject, Message-IDs, references
4. **Path Traversal Protection**: Workspace confinement for attachment downloads
5. **TLS 1.2+ Enforcement**: Minimum TLS version for all connections
6. **Recipient Whitelist**: Optional domain/address restrictions

### MCP Tools Exposed

| Tool | Purpose | Account Scope |
|------|---------|---------------|
| `list_accounts` | List configured email accounts | Global |
| `list_folders` | List IMAP folders | Per account |
| `search_emails` | Search messages by IMAP criteria | Per account |
| `get_email` | Fetch single message | Per account |
| `download_attachment` | Download attachment to workspace | Per account |
| `send_email` | Send new email | Per account |
| `reply_email` | Reply to thread | Per account |
| `move_email` | Move between folders | Per account |
| `delete_email` | Delete message | Per account |
| `mark_email_read` | Mark message as read | Per account |

---

## Package Architecture

### Module Structure (src/simple_email_gw/)

```
simple-email-gw/
├── pyproject.toml
├── uv.lock
├── .python-version
├── src/
│   └── simple_email_gw/
│       ├── __init__.py           # Public API surface
│       ├── __main__.py           # `python -m simple_email_gw` entry point
│       ├── cli.py                # CLI entry point (`mcp` command)
│       ├── server.py             # FastMCP server (from email_mcp/server.py)
│       ├── config.py             # Configuration (from email_mcp/config.py)
│       ├── imap/
│       │   ├── __init__.py       # Re-export IMAPClient
│       │   └── client.py        # IMAP client (from email_mcp/imap/client.py)
│       ├── smtp/
│       │   ├── __init__.py       # Re-export SMTPClient
│       │   └── client.py        # SMTP client (from email_mcp/smtp/client.py)
│       ├── connections/
│       │   ├── __init__.py       # Re-export ConnectionPool, RateLimitError
│       │   └── pool.py           # Connection pool (from email_mcp/connections/pool.py)
│       └── safety/
│           ├── __init__.py       # Re-export safety utilities
│           ├── rate_limiter.py   # Rate limiter (from email_mcp/safety/rate_limiter.py)
│           ├── audit.py          # Audit logging (from email_mcp/safety/audit.py)
│           └── sanitize.py       # CRLF prevention (from email_mcp/safety/sanitize.py)
├── tests/
│   ├── conftest.py               # Pytest fixtures
│   ├── test_config.py
│   ├── test_rate_limiter.py
│   ├── test_sanitize.py
│   ├── test_whitelist.py
│   ├── test_path_traversal.py
│   ├── test_imap_client.py
│   ├── test_smtp_client.py
│   └── test_server.py
└── docs/
    ├── README.md                 # User documentation
    ├── CONFIGURATION.md          # Configuration guide
    ├── TESTING.md                # Testing guide (from email/docs/TESTING.md)
    └── API.md                    # Programmatic API docs
```

### Entry Points

#### 1. MCP Server Command (`[project.scripts]`)

```toml
[project.scripts]
mcp = "simple_email_gw.cli:main"
```

**Usage**:
```bash
uvx --from simple-email-gw mcp
# Or:
python -m simple_email_gw
```

#### 2. Programmatic API

Users can import and use the package directly:

```python
from simple_email_gw import IMAPClient, SMTPClient, ConnectionPool
from simple_email_gw.config import EmailAccount, ServerConfig
from simple_email_gw.safety import RateLimiter, sanitize_subject

# Create account
account = EmailAccount(
    name="work",
    imap_host="imap.gmail.com",
    smtp_host="smtp.gmail.com",
    username="user@gmail.com",
    password="app-password"
)

# Use IMAP client
async with IMAPClient(account) as client:
    folders = await client.list_folders()
    messages = await client.search(folder="INBOX")

# Use SMTP client
smtp = SMTPClient(account)
await smtp.send_email(
    to=["recipient@example.com"],
    subject="Test",
    body="Hello world"
)
```

---

## Public API Surface

### Package-Level Exports (`__init__.py`)

```python
"""Simple Email Gateway - IMAP/SMTP client with security features."""

from simple_email_gw.imap.client import IMAPClient
from simple_email_gw.smtp.client import SMTPClient
from simple_email_gw.connections.pool import ConnectionPool, RateLimitError
from simple_email_gw.config import EmailAccount, ServerConfig, RecipientWhitelist
from simple_email_gw.safety import (
    RateLimiter,
    sanitize_subject,
    sanitize_message_id,
    sanitize_references,
)

__version__ = "0.1.0"
__all__ = [
    # Clients
    "IMAPClient",
    "SMTPClient",
    # Connection management
    "ConnectionPool",
    "RateLimitError",
    # Configuration
    "EmailAccount",
    "ServerConfig",
    "RecipientWhitelist",
    # Safety utilities
    "RateLimiter",
    "sanitize_subject",
    "sanitize_message_id",
    "sanitize_references",
]
```

### Subpackage Exports

#### `simple_email_gw.imap`

```python
from simple_email_gw.imap.client import IMAPClient, SecurityError

__all__ = ["IMAPClient", "SecurityError"]
```

#### `simple_email_gw.smtp`

```python
from simple_email_gw.smtp.client import SMTPClient, WhitelistError, validate_email

__all__ = ["SMTPClient", "WhitelistError", "validate_email"]
```

#### `simple_email_gw.connections`

```python
from simple_email_gw.connections.pool import ConnectionPool, RateLimitError, get_pool

__all__ = ["ConnectionPool", "RateLimitError", "get_pool"]
```

#### `simple_email_gw.safety`

```python
from simple_email_gw.safety.rate_limiter import RateLimiter
from simple_email_gw.safety.audit import (
    log_event,
    log_email_sent,
    log_auth_attempt,
    log_rate_limited,
    log_attachment_download,
)
from simple_email_gw.safety.sanitize import (
    sanitize_message_id,
    sanitize_references,
    sanitize_header_value,
    sanitize_subject,
)

__all__ = [
    "RateLimiter",
    "log_event",
    "log_email_sent",
    "log_auth_attempt",
    "log_rate_limited",
    "log_attachment_download",
    "sanitize_message_id",
    "sanitize_references",
    "sanitize_header_value",
    "sanitize_subject",
]
```

#### `simple_email_gw.config`

```python
from simple_email_gw.config.config import (
    EmailAccount,
    ServerConfig,
    RecipientWhitelist,
    RateLimitConfig,
    get_config,
    get_accounts,
    get_recipient_whitelist,
)

__all__ = [
    "EmailAccount",
    "ServerConfig",
    "RecipientWhitelist",
    "RateLimitConfig",
    "get_config",
    "get_accounts",
    "get_recipient_whitelist",
]
```

---

## Extraction Plan

### Phase 1: Project Initialization

1. Create package with `uv init --lib simple-email-gw`
2. Set up `src/simple_email_gw/` layout
3. Configure `.python-version` (3.11+)
4. Initialize `pyproject.toml` with metadata

### Phase 2: Core Module Migration

Move files from `email/src/email_mcp/` to `src/simple_email_gw/`:

| Source | Destination | Modifications |
|--------|-------------|---------------|
| `config.py` | `config/config.py` | Split into `config/__init__.py` and `config/config.py` |
| `server.py` | `server.py` | Update imports to `simple_email_gw.*` |
| `imap/client.py` | `imap/client.py` | Update imports |
| `smtp/client.py` | `smtp/client.py` | Update imports |
| `connections/pool.py` | `connections/pool.py` | Update imports |
| `safety/rate_limiter.py` | `safety/rate_limiter.py` | No changes needed |
| `safety/audit.py` | `safety/audit.py` | No changes needed |
| `safety/sanitize.py` | `safety/sanitize.py` | No changes needed |

**Import Updates**:

```python
# OLD (email_mcp)
from email_mcp.config import EmailAccount
from email_mcp.connections.pool import get_pool

# NEW (simple_email_gw)
from simple_email_gw.config import EmailAccount
from simple_email_gw.connections import get_pool
```

### Phase 3: Test Migration

Move tests from `email/tests/` to `tests/`:

| Source | Destination | Modifications |
|--------|-------------|---------------|
| `conftest.py` | `tests/conftest.py` | Update imports |
| `test_*.py` | `tests/test_*.py` | Update imports |

**Import Updates**:

```python
# OLD
from email_mcp.config import EmailAccount
from email_mcp.connections import pool as pool_module

# NEW
from simple_email_gw.config import EmailAccount
from simple_email_gw.connections import pool as pool_module
```

### Phase 4: Entry Point Setup

Create `cli.py` for the `mcp` command:

```python
"""CLI entry point for simple-email-gw MCP server."""

from simple_email_gw.server import main

def main() -> None:
    """Run the MCP server."""
    main()

if __name__ == "__main__":
    main()
```

Update `__main__.py`:

```python
"""Entry point for running as module: python -m simple_email_gw."""

from simple_email_gw.server import main

if __name__ == "__main__":
    main()
```

### Phase 5: C3 Integration

After PyPI publication:

1. Remove `email/` from C3
2. Update `.mcp.json` in C3 to use `uvx --from simple-email-gw mcp`
3. Update documentation to reference the standalone package

---

## PyPI Configuration

### pyproject.toml

```toml
[project]
name = "simple-email-gw"
version = "0.1.0"
description = "Simple email gateway with IMAP/SMTP clients, connection pooling, and MCP server"
authors = [{name = "Christophe VG", email = "contact@christophe.vg"}]
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
keywords = ["email", "imap", "smtp", "mcp", "model-context-protocol"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]

dependencies = [
    "fastmcp>=3.0.0",
    "aioimaplib>=1.0.0",
    "aiosmtplib>=3.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.4.0",
    "mypy>=1.9.0",
]

[project.scripts]
mcp = "simple_email_gw.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/simple_email_gw"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### Build and Publish Workflow

```bash
# Build
uv build

# Check build
uv run twine check dist/*

# Publish to TestPyPI (optional)
uv publish --index-url https://test.pypi.org/simple/ --token $TEST_PYPI_TOKEN

# Publish to PyPI
uv publish --token $PYPI_TOKEN
```

### Version Strategy

Follow Semantic Versioning:

| Version | When to Bump |
|---------|--------------|
| Major (0.x.x) | Breaking API changes |
| Minor (x.1.x) | New features, backward compatible |
| Patch (x.x.1) | Bug fixes |

---

## MCP Server Interface

### Tool Definitions (RESTful-Inspired)

The MCP server exposes tools that follow RESTful resource patterns:

**Resources** (nouns):
- `account` - Email account configuration
- `folder` - IMAP folder/mailbox
- `message` - Email message
- `attachment` - Email attachment

**Operations** (verbs via tool names):

| Tool | HTTP Equivalent | Description |
|------|-----------------|-------------|
| `list_accounts` | `GET /accounts` | List configured accounts |
| `list_folders` | `GET /accounts/{id}/folders` | List folders for account |
| `search_emails` | `GET /messages?account=...&folder=...` | Search messages |
| `get_email` | `GET /messages/{id}` | Fetch single message |
| `download_attachment` | `GET /attachments/{id}` | Download attachment |
| `send_email` | `POST /messages` | Create and send message |
| `reply_email` | `POST /messages/{id}/reply` | Reply to thread |
| `move_email` | `PATCH /messages/{id}` with `folder` update | Move message |
| `delete_email` | `DELETE /messages/{id}` | Delete message |
| `mark_email_read` | `PATCH /messages/{id}` with `flags` update | Mark as read |

### Configuration Approach

Environment variables follow `EMAIL_` prefix pattern:

```bash
# Single account configuration
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_USERNAME=user@gmail.com
EMAIL_PASSWORD=app-password

# Multiple accounts (JSON)
EMAIL_ACCOUNTS_JSON='[{"name":"work","imap_host":"imap.gmail.com",...}]'

# Recipient whitelist
EMAIL_RECIPIENT_DOMAINS=gmail.com,icloud.com
EMAIL_RECIPIENT_ADDRESSES=admin@company.com

# Rate limits (optional)
EMAIL_RATE_LIMITS='{"imap_requests_per_minute":60,"smtp_sends_per_hour":100}'
```

### Error Handling

Tools return `ToolError` with user-friendly messages:

```python
from fastmcp.exceptions import ToolError

# Example error responses
raise ToolError(f"Account not found: {account}")
raise ToolError("Rate limit exceeded. Please try again later.")
raise ToolError("Failed to fetch message. Check server logs for details.")
```

Internal errors are logged but not exposed to users (security best practice).

---

## Testing Strategy

### Unit Tests

| Test File | Coverage |
|-----------|----------|
| `test_config.py` | Account parsing, whitelist configuration |
| `test_rate_limiter.py` | Token bucket algorithm, window expiry |
| `test_sanitize.py` | CRLF injection prevention |
| `test_whitelist.py` | Domain/address filtering |
| `test_path_traversal.py` | Workspace confinement |
| `test_imap_client.py` | IMAP operations (mocked) |
| `test_smtp_client.py` | SMTP operations (mocked) |
| `test_server.py` | MCP tool responses (mocked) |

### Integration Tests

Use MCP Inspector for manual testing:

```bash
npx @modelcontextprotocol/inspector uvx --from simple-email-gw mcp
```

### Coverage Goals

| Module | Target Coverage |
|--------|-----------------|
| `config.py` | 90%+ |
| `safety/*.py` | 95%+ |
| `imap/client.py` | 80%+ |
| `smtp/client.py` | 80%+ |
| `connections/pool.py` | 85%+ |
| `server.py` | 75%+ |

---

## Documentation Structure

### README.md

```markdown
# simple-email-gw

A simple email gateway with IMAP/SMTP clients, connection pooling, and MCP server.

## Features

- Async IMAP and SMTP clients (aioimaplib, aiosmtplib)
- Connection pooling with automatic management
- Token bucket rate limiting
- Audit logging for security compliance
- CRLF injection prevention
- Recipient whitelist enforcement
- TLS 1.2+ minimum encryption
- MCP server for AI assistant integration

## Installation

```bash
# Run directly with uvx
uvx --from simple-email-gw mcp

# Or install in your project
uv add simple-email-gw
```

## Quick Start

[Programmatic usage examples...]

## Configuration

[Environment variable guide...]

## MCP Server

[Tool documentation...]

## Security

[Security features overview...]
```

### API.md

Programmatic API documentation with:
- Class references for `IMAPClient`, `SMTPClient`, `ConnectionPool`
- Method signatures and examples
- Error handling patterns
- Rate limiting usage
- Audit logging integration

---

## Dependencies Analysis

### Core Dependencies

| Package | Purpose | C3-Specific? |
|---------|---------|--------------|
| `fastmcp>=3.0.0` | MCP server framework | No |
| `aioimaplib>=1.0.0` | Async IMAP client | No |
| `aiosmtplib>=3.0.0` | Async SMTP client | No |
| `pydantic>=2.0.0` | Data validation | No |
| `pydantic-settings>=2.0.0` | Settings management | No |

### Optional Dependencies

| Package | Purpose | When to Add |
|---------|---------|-------------|
| `python-dotenv` | .env file loading | Already in config.py (optional import) |

### C3-Specific Code to Remove

None - the `email/` module is self-contained and has no C3 dependencies.

---

## Action Items

### Immediate (Extraction Phase)

1. **Create package structure**
   - `uv init --lib simple-email-gw`
   - Set up `src/simple_email_gw/` layout
   - Configure `pyproject.toml` with dependencies

2. **Migrate core modules**
   - Copy `config.py` → `config/config.py`
   - Copy `imap/client.py` → `imap/client.py`
   - Copy `smtp/client.py` → `smtp/client.py`
   - Copy `connections/pool.py` → `connections/pool.py`
   - Copy `safety/*.py` → `safety/*.py`
   - Copy `server.py` → `server.py`

3. **Update imports**
   - Replace `email_mcp.*` with `simple_email_gw.*`
   - Create `__init__.py` files with proper exports

4. **Set up entry points**
   - Create `cli.py` with `main()` function
   - Update `__main__.py`
   - Add `[project.scripts]` to pyproject.toml

5. **Migrate tests**
   - Copy all test files from `email/tests/`
   - Update imports
   - Verify all tests pass

### Short-Term (Quality Phase)

6. **Address quality issues from email/TODO.md**
   - H5: IMAP response robustness (iCloud status messages)
   - H6: OAuth2 XOAUTH2 string encoding
   - H7: IMAP capability caching
   - H8: SMTP error message sanitization
   - H9: Path validation error clarity
   - H10: Configuration error separation
   - H11: Rate limit wait-and-retry
   - H12: Connection pool cleanup
   - H13: Audit log rotation

7. **Add missing tests**
   - Integration tests for MCP tools
   - Edge case tests for error handling

### Medium-Term (Publication Phase)

8. **Documentation**
   - Write README.md
   - Write API.md (programmatic usage)
   - Write CONFIGURATION.md
   - Adapt TESTING.md

9. **CI/CD Setup**
   - GitHub Actions workflow
   - Multi-version testing (3.11, 3.12, 3.13)
   - Coverage reporting

10. **PyPI Publication**
    - Build package
    - Test on TestPyPI
    - Publish to PyPI

### Long-Term (Integration Phase)

11. **C3 Integration**
    - Update `.mcp.json` to use `simple-email-gw`
    - Remove `email/` folder from C3
    - Update C3 documentation

---

## References

- `/c3:python-project` - Project structure standards
- `/c3:python` - Python coding best practices
- `email/docs/TESTING.md` - Testing documentation
- `email/src/email_mcp/` - Current implementation