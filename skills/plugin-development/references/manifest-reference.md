# Plugin Manifest Reference (plugin.json)

**Reference for:** `plugin-development` skill
**Location:** `.claude-plugin/plugin.json`

---

## Required Fields

Only `name` is required:

```json
{
  "name": "my-plugin"
}
```

### Name Requirements

- Use kebab-case format (lowercase with hyphens)
- Must be unique across installed plugins
- No spaces or special characters
- Pattern: `/^[a-z][a-z0-9]*(-[a-z0-9]+)*$/`
- Examples: `code-review-assistant`, `test-runner`, `api-docs`

---

## Metadata Fields

```json
{
  "name": "code-review-assistant",
  "version": "1.2.0",
  "description": "Automates code review with style checks and suggestions",
  "author": {
    "name": "Jane Developer",
    "email": "jane@example.com",
    "url": "https://janedeveloper.com"
  },
  "homepage": "https://docs.example.com/code-review",
  "repository": "https://github.com/janedev/code-review-assistant",
  "license": "MIT",
  "keywords": ["code-review", "automation", "quality", "ci-cd"]
}
```

### Version Format

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes

**Warning:** If you change plugin code without bumping the version, existing users won't see changes due to caching.

---

## Component Path Fields

Paths are relative to plugin root and must start with `./`:

```json
{
  "skills": "./custom/skills/",
  "commands": ["./commands", "./admin-commands"],
  "agents": "./specialized-agents",
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "monitors": "./monitors.json"
}
```

### Path Behavior

- Custom paths **replace** default directories (not supplement)
- Exception: `hooks`, `mcpServers`, and `lspServers` **merge** with defaults
- Must be relative to plugin root
- Must start with `./`
- Cannot use absolute paths
- Support arrays for multiple locations

### Default Paths (Auto-Discovery)

If not specified, these defaults are used:

| Component | Default Location |
|-----------|-----------------|
| `skills` | `./skills/` |
| `commands` | `./commands/` |
| `agents` | `./agents/` |
| `hooks` | `./hooks/hooks.json` |
| `mcpServers` | `./.mcp.json` |
| `lspServers` | `./.lsp.json` |
| `monitors` | `./monitors.json` |

---

## User Configuration

Prompt users for configuration values at enable time:

```json
{
  "userConfig": {
    "api_endpoint": {
      "description": "Your team's API endpoint",
      "sensitive": false
    },
    "api_token": {
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

### Storage

- Non-sensitive values: Stored in `settings.json`
- Sensitive values: Stored in system keychain
- Access via: `${user_config.KEY}` substitution

---

## Channels (Message Injection)

Declare message injection channels for external integrations:

```json
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": { 
          "description": "Bot token", 
          "sensitive": true 
        },
        "owner_id": { 
          "description": "User ID", 
          "sensitive": false 
        }
      }
    }
  ]
}
```

---

## Dependencies

Declare plugin dependencies with optional version constraints:

```json
{
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### Version Operators

| Operator | Meaning |
|----------|---------|
| `1.2.3` | Exact version |
| `~1.2.3` | Compatible (>=1.2.3, <1.3.0) |
| `^1.2.3` | Compatible (>=1.2.3, <2.0.0) |
| `>=1.2.3` | Minimum version |
| `<2.0.0` | Maximum version |

---

## MCP Servers Inline

Define MCP servers directly in plugin.json:

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}",
        "API_KEY": "${API_KEY}"
      }
    },
    "plugin-api": {
      "type": "sse",
      "url": "https://mcp.example.com/sse"
    }
  }
}
```

### Server Types

| Type | Transport | Best For | Auth |
|------|-----------|----------|------|
| `stdio` | Process | Local tools, custom servers | Env vars |
| `sse` | HTTP | Hosted services, cloud APIs | OAuth |
| `http` | REST | API backends, token auth | Tokens |
| `ws` | WebSocket | Real-time, streaming | Tokens |

---

## Complete Example

```json
{
  "name": "code-review-assistant",
  "version": "2.1.0",
  "description": "Automated code review with style checks and AI suggestions",
  "author": {
    "name": "DevTools Team",
    "email": "devtools@example.com",
    "url": "https://devtools.example.com"
  },
  "homepage": "https://docs.example.com/code-review",
  "repository": "https://github.com/devtools/code-review-assistant",
  "license": "MIT",
  "keywords": ["code-review", "automation", "quality"],
  
  "userConfig": {
    "default_branch": {
      "description": "Default branch for comparisons",
      "sensitive": false
    }
  },
  
  "mcpServers": {
    "review-api": {
      "type": "sse",
      "url": "https://api.example.com/review/sse",
      "headers": {
        "Authorization": "Bearer ${user_config.api_token}"
      }
    }
  },
  
  "dependencies": [
    { "name": "git-helpers", "version": ">=1.0.0" }
  ]
}
```

---

## Validation

Run validation to check manifest:

```bash
claude plugin validate .
```

Checks:
- `plugin.json` syntax
- Required fields present
- Path references exist
- Skill/agent frontmatter valid
- Hook configuration valid