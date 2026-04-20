# Email MCP Server

MCP server for email exchange via IMAP/SMTP protocols.

## Overview

This server provides Claude Code with email capabilities through the Model Context Protocol (MCP). It supports:

- **IMAP operations**: List folders, search emails, read messages, download attachments
- **SMTP operations**: Send emails, reply to threads
- **Management**: Move and delete emails
- **Security**: Rate limiting, audit logging, TLS 1.2, recipient whitelisting

## Documentation

| Document | Description |
|----------|-------------|
| [TESTING.md](docs/TESTING.md) | Testing guide, implemented flow, MCP Inspector usage |
| [TODO.md](TODO.md) | Future improvements and known issues |

## Installation

### Prerequisites

Install the required dependencies:

```bash
pip install fastmcp aioimaplib aiosmtplib pydantic pydantic-settings
```

### As a Plugin

Add to your `.claude/plugins/` directory or install via marketplace. The plugin's `.mcp.json` will configure the MCP server automatically.

### Manual

```bash
cd email
pip install -e .
```

## Configuration

Configure email accounts through environment variables:

### Single Account (Simple)

```bash
export EMAIL_IMAP_HOST="imap.gmail.com"
export EMAIL_SMTP_HOST="smtp.gmail.com"
export EMAIL_USERNAME="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
```

### Multiple Accounts (JSON)

```bash
export EMAIL_ACCOUNTS_JSON='[
  {
    "name": "work",
    "imap_host": "imap.gmail.com",
    "imap_port": 993,
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "work@example.com",
    "password": "app-password",
    "auth_method": "password"
  },
  {
    "name": "personal",
    "imap_host": "imap.fastmail.com",
    "smtp_host": "smtp.fastmail.com",
    "username": "personal@example.com",
    "password": "app-password"
  }
]'
```

### OAuth2 Authentication

For Gmail/Outlook with OAuth2:

```bash
export EMAIL_AUTH_METHOD="oauth2"
export EMAIL_OAUTH2_TOKEN="your-oauth2-access-token"
```

### Recipient Whitelist

Limit who can receive emails by configuring a recipient whitelist:

**By domain (comma-separated):**

```bash
export EMAIL_RECIPIENT_DOMAINS="example.com,company.org"
```

**By address (comma-separated):**

```bash
export EMAIL_RECIPIENT_ADDRESSES="user@example.com,admin@company.org"
```

**JSON configuration (full control):**

```bash
export EMAIL_RECIPIENT_WHITELIST_JSON='{
  "enabled": true,
  "domains": ["example.com", "trusted.org"],
  "addresses": ["specific@external.com"]
}'
```

When configured, emails to addresses outside the whitelist will be rejected with an error.

## MCP Configuration

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["-m", "email_mcp"],
      "cwd": "/path/to/c3/email/src",
      "env": {
        "EMAIL_IMAP_HOST": "${EMAIL_IMAP_HOST}",
        "EMAIL_SMTP_HOST": "${EMAIL_SMTP_HOST}",
        "EMAIL_USERNAME": "${EMAIL_USERNAME}",
        "EMAIL_PASSWORD": "${EMAIL_PASSWORD}"
      }
    }
  }
}
```

> **Note**: The `cwd` must point to the `src` directory containing the `email_mcp` package.

## Available Tools

| Tool | Description |
|------|-------------|
| `list_accounts` | List configured email accounts |
| `list_folders` | List IMAP folders/mailboxes |
| `search_emails` | Search emails with IMAP criteria |
| `get_email` | Fetch a single email message |
| `download_attachment` | Download attachment from email |
| `send_email` | Send a new email |
| `reply_email` | Reply to an email thread |
| `move_email` | Move email between folders |
| `delete_email` | Delete an email message |

## Security

### SSL/TLS

All connections use SSL certificate verification by default:

- IMAP: Port 993 with implicit TLS
- SMTP: Port 587 with STARTTLS, or port 465 with implicit TLS

### Credentials

- Credentials are loaded from environment variables only
- Passwords are never logged or returned in tool output
- OAuth2 is supported for Gmail/Outlook authentication

### Workspace Confinement

Attachments are saved with hashed filenames to prevent path traversal attacks:

```python
safe_name = hashlib.sha256(filename.encode()).hexdigest()[:16] + "_" + filename
```

## Rate Limiting

Default limits protect against abuse:

- IMAP: 60 requests/minute/account
- SMTP: 100 sends/hour/account

## Development

### Run Locally

```bash
cd email/src
python -m email_mcp
```

### Test with MCP Inspector

```bash
npx @anthropic/mcp-inspector
```

### Project Structure

```
email/
├── src/email_mcp/
│   ├── __init__.py      # Package initialization
│   ├── __main__.py      # Entry point for `python -m email_mcp`
│   ├── server.py        # FastMCP server definition
│   ├── config.py        # Pydantic configuration
│   ├── connections/     # Connection pooling
│   ├── imap/            # IMAP client
│   ├── smtp/            # SMTP client
│   └── tools/           # Tool definitions
├── pyproject.toml
└── requirements.txt
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastmcp | >=3.0.0 | MCP server framework |
| aioimaplib | >=1.0.0 | Async IMAP client |
| aiosmtplib | >=3.0.0 | Async SMTP client |
| pydantic | >=2.0.0 | Configuration validation |
| pydantic-settings | >=2.0.0 | Environment loading |

## License

MIT License