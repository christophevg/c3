# Consensus Report: simple-email-gw Package Extraction

**Date:** 2026-05-07
**Status:** ✅ Approved

## Summary

All domain agents agree on the extraction approach. The package will be created as a standalone PyPI package at `~/Workspace/agentic/simple-email-gw` with standard Python project structure.

## Architecture Decisions

### Package Structure
```
simple-email-gw/
├── src/simple_email_gw/
│   ├── __init__.py           # Public API exports
│   ├── cli.py                # `mcp` command entry point
│   ├── server.py             # FastMCP server
│   ├── config.py             # Pydantic settings
│   ├── imap/client.py        # Async IMAP client
│   ├── smtp/client.py        # Async SMTP client
│   ├── connections/pool.py   # Connection pool + rate limiting
│   └── safety/               # Rate limiter, audit, sanitization
├── tests/                    # Migrated from email/tests
├── pyproject.toml
├── README.md
└── SECURITY.md
```

### Entry Point
```toml
[project.scripts]
mcp = "simple_email_gw.cli:main"
```

Enables: `uvx --from simple-email-gw mcp`

### Public API
```python
from simple_email_gw import IMAPClient, SMTPClient, ConnectionPool
from simple_email_gw.config import EmailAccount
```

## Security Requirements

### Blocking Issues (Must Fix Before PyPI)

| ID | Issue | Fix |
|----|-------|-----|
| C1 | IMAP folder CRLF injection | Add `sanitize_folder_name()` |
| C2 | Attachment filename CRLF injection | Add `sanitize_filename()` |
| H1 | IMAP message ID validation | Add `sanitize_message_id_numeric()` |
| H4 | Rate limiter non-monotonic clock | Replace `time.time()` with `time.monotonic()` |

### High Priority (Address During Extraction)

| ID | Issue | Fix |
|----|-------|-----|
| H2 | Unbounded attachment size | Add `MAX_ATTACHMENT_SIZE` config |
| H3 | Path leakage in errors | Sanitize error messages |
| H5 | Error message sanitization | Generic errors for client |

## Migration Plan

1. **Create project** - `uv init simple-email-gw` in `~/Workspace/agentic/`
2. **Copy modules** - Migrate from `email/src/email_mcp/` to `src/simple_email_gw/`
3. **Update imports** - Change `email_mcp.*` to `simple_email_gw.*`
4. **Configure pyproject.toml** - Dependencies, entry points, metadata
5. **Migrate tests** - Copy from `email/tests/`
6. **Create documentation** - README.md, SECURITY.md
7. **Quality improvements** - Address security findings
8. **Publish to PyPI** - After all tests pass

## Dependencies

| Package | Version | Notes |
|---------|---------|-------|
| fastmcp | >=3.0.0,<4.0.0 | MCP server framework |
| aioimaplib | >=1.0.0,<2.0.0 | Async IMAP |
| aiosmtplib | >=3.0.0,<4.0.0 | Async SMTP |
| pydantic | >=2.0.0,<3.0.0 | Settings/validation |
| pydantic-settings | >=2.0.0,<3.0.0 | Environment config |

## C3 Integration (After PyPI)

1. Update `.mcp.json` to use `uvx --from simple-email-gw mcp`
2. Remove `email/` folder from C3
3. Update skills/agents that reference email MCP

## Agent Approvals

| Agent | Status | Notes |
|-------|--------|-------|
| api-architect | ✅ Approved | Architecture sound for PyPI |
| security-engineer | ✅ Approved | Security findings documented, blocking issues identified |

## Next Steps

1. ✅ Consensus reached
2. → Invoke python-developer for project setup
3. Security fixes during migration
4. Test migration
5. PyPI publication