# Email MCP Server - Testing Guide

## Overview

This document describes the testing procedures and implemented functionality of the Email MCP Server.

## Implemented Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Environment   │     │   Email MCP     │     │   Email Server  │
│   Configuration │────▶│     Server      │────▶│  (IMAP/SMTP)    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │                       │                       │
   .env file              FastMCP Tools            iCloud/Gmail
   env vars               (9 tools)               etc.
```

### Configuration Flow

1. **Load Configuration**: Server reads from environment variables or `.env` file
2. **Parse Accounts**: Single account (individual vars) or multiple accounts (JSON)
3. **Parse Whitelist**: Optional recipient restrictions (domains/addresses)
4. **Create Connection Pool**: Singleton pool manages IMAP/SMTP clients

### IMAP Operations Flow

```
list_accounts ──▶ get_accounts() ──▶ Return configured accounts
     │
list_folders ──▶ get_imap_client() ──▶ IMAP LIST command
     │
search_emails ──▶ IMAP SEARCH ──▶ Return message IDs
     │
get_email ──▶ IMAP FETCH ──▶ Parse and return message content
     │
download_attachment ──▶ Validate path ──▶ Save to workspace
```

### SMTP Operations Flow

```
send_email ──▶ Validate emails ──▶ Check whitelist ──▶ Audit log ──▶ SMTP send
     │
reply_email ──▶ Set In-Reply-To ──▶ Check whitelist ──▶ SMTP send
```

### Security Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      Rate Limiting                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │ IMAP: 60/min │    │SMTP: 100/hr │    │ Token Bucket│       │
│  │ per account  │    │ per account │    │   Algorithm │       │
│  └─────────────┘    └─────────────┘    └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Audit Logging                           │
│  • Email sent (recipients, subject, attachments)            │
│  • Authentication (success/failure, method)                  │
│  • Rate limit exceeded                                        │
│  • Attachment downloads                                       │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Path Traversal Protection                  │
│  1. Validate output_dir is within workspace                  │
│  2. Sanitize filename with os.path.basename()               │
│  3. Add hash prefix for uniqueness                           │
│  4. Workspace: EMAIL_WORKSPACE env var (default: /tmp)      │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    TLS 1.2 Enforcement                        │
│  ssl.create_default_context()                                │
│  context.minimum_version = ssl.TLSVersion.TLSv1_2            │
└─────────────────────────────────────────────────────────────┘
```

## MCP Inspector

The [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) is a developer tool for testing MCP servers.

### Installation

```bash
npx @modelcontextprotocol/inspector
```

### Running

```bash
# Start inspector with your server
npx @modelcontextprotocol/inspector python -m email_mcp.server

# Or start inspector first, then add server in UI
npx @modelcontextprotocol/inspector
```

The UI will be available at `http://localhost:6274`.

### Inspector Features

- **Tool Testing**: Call any MCP tool and see responses
- **Resource Viewing**: Browse MCP resources
- **Prompt Testing**: Test prompt templates
- **Debug Mode**: View raw protocol messages
- **Configuration**: Save server configurations

### Testing Workflow in Inspector

1. **Connect Server**
   - Command: `python -m email_mcp.server`
   - Server runs in stdio mode

2. **Test Tools**
   - `list_accounts` → Verify configuration loaded
   - `list_folders` → Check IMAP connectivity (account="default")
   - `search_emails` → Find messages (account="default", folder="INBOX")
   - `get_email` → Read a message (account="default", message_id="1")

3. **Verify Security**
   - Try blocked recipient (if whitelist enabled)
   - Check rate limiting after many requests
   - Verify path traversal rejection (invalid output_dir)

## Unit Tests

### Test Structure

```
email/tests/
├── conftest.py              # Pytest fixtures
├── test_config.py           # Configuration tests
├── test_rate_limiter.py     # Rate limiting tests
├── test_path_traversal.py   # Security tests
└── test_whitelist.py        # Whitelist tests
```

### Running Tests

```bash
cd email

# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py -v

# Run with coverage
pytest --cov=src/email_mcp tests/
```

### Test Categories

| Category | Tests | Coverage |
|----------|-------|----------|
| Configuration | Account parsing, JSON/env vars, SecretStr protection | ✅ |
| Rate Limiting | Token bucket, concurrent access, window expiry | ✅ |
| Path Traversal | Workspace confinement, filename sanitization | ✅ |
| Whitelist | Domain/address filtering, case insensitivity | ✅ |

### Key Test Cases

```python
# Configuration
test_password_account()         # Create account with password
test_oauth2_account()           # Create account with OAuth2
test_secrets_not_in_repr()      # Verify SecretStr doesn't leak

# Rate Limiting
test_allows_within_limit()      # Requests within limit pass
test_blocks_over_limit()        # Over-limit requests blocked
test_window_expiry()            # Requests reset after window

# Whitelist
test_domain_whitelist()         # Domain-based filtering
test_address_whitelist()        # Address-based filtering
test_combined_whitelist()       # Both domain and address

# Path Traversal
test_valid_output_dir()         # Valid workspace path works
test_path_outside_workspace()   # Invalid path rejected
```

## Manual Testing

### Quick Configuration Check

```bash
cd email
python -c "
import sys; sys.path.insert(0, 'src')
from email_mcp.config import get_accounts, get_recipient_whitelist

accounts = get_accounts()
whitelist = get_recipient_whitelist()

print(f'Accounts: {len(accounts)}')
for a in accounts:
    print(f'  {a.name}: {a.username} @ {a.imap_host}')
print(f'Whitelist: enabled={whitelist.enabled}')
"
```

### IMAP Connection Test

```bash
python -c "
import asyncio
import sys; sys.path.insert(0, 'src')

from email_mcp.config import get_accounts
from email_mcp.imap.client import IMAPClient

async def test():
    accounts = get_accounts()
    client = IMAPClient(accounts[0])
    
    await client.connect()
    print('✓ Connected')
    
    folders = await client.list_folders()
    print(f'✓ Folders: {[f[\"name\"] for f in folders]}')
    
    await client.select_folder('INBOX')
    ids = await client.search()
    print(f'✓ Messages: {len(ids)}')
    
    if ids:
        msg = await client.fetch_message(ids[0])
        print(f'✓ Latest: {msg[\"subject\"][:50]}')
    
    await client.disconnect()

asyncio.run(test())
"
```

### SMTP Test (with Whitelist)

```bash
python -c "
import asyncio
import sys; sys.path.insert(0, 'src')

from email_mcp.config import get_accounts, get_recipient_whitelist
from email_mcp.smtp.client import SMTPClient, WhitelistError

async def test():
    accounts = get_accounts()
    whitelist = get_recipient_whitelist()
    
    print(f'Whitelist enabled: {whitelist.enabled}')
    print(f'Allowed domains: {whitelist.domains}')
    print(f'Allowed addresses: {whitelist.addresses}')
    
    # Test filtering
    test_emails = ['user@icloud.com', 'external@gmail.com']
    allowed, blocked = whitelist.filter_recipients(test_emails)
    print(f'Test: allowed={allowed}, blocked={blocked}')

asyncio.run(test())
"
```

## Environment Variables

### Required (Single Account)

| Variable | Description | Example |
|----------|-------------|---------|
| `EMAIL_IMAP_HOST` | IMAP server hostname | `imap.gmail.com` |
| `EMAIL_SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `EMAIL_USERNAME` | Email address | `user@example.com` |
| `EMAIL_PASSWORD` | Password or app password | `secret` |

### Optional (Single Account)

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_IMAP_PORT` | IMAP port | `993` |
| `EMAIL_SMTP_PORT` | SMTP port | `587` |
| `EMAIL_AUTH_METHOD` | `password` or `oauth2` | `password` |
| `EMAIL_OAUTH2_TOKEN` | OAuth2 access token | - |

### Multiple Accounts

| Variable | Description |
|----------|-------------|
| `EMAIL_ACCOUNTS_JSON` | JSON array of account configs |

### Whitelist

| Variable | Description |
|----------|-------------|
| `EMAIL_RECIPIENT_WHITELIST_JSON` | Full whitelist config as JSON |
| `EMAIL_RECIPIENT_DOMAINS` | Comma-separated allowed domains |
| `EMAIL_RECIPIENT_ADDRESSES` | Comma-separated allowed addresses |

### Other

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_WORKSPACE` | Attachment download directory | `/tmp/email_workspace` |

## Email Provider Notes

### iCloud (mail.me.com)

- IMAP: `imap.mail.me.com:993` (SSL)
- SMTP: `smtp.mail.me.com:587` (STARTTLS)
- Requires app-specific password
- Strict IMAP LIST syntax: `list('""', '"*"')`

### Gmail

- IMAP: `imap.gmail.com:993`
- SMTP: `smtp.gmail.com:587`
- Requires app password or OAuth2
- Supports OAuth2 via `EMAIL_AUTH_METHOD=oauth2`

### Outlook/Office365

- IMAP: `outlook.office365.com:993`
- SMTP: `smtp.office365.com:587`
- May require OAuth2 for some accounts