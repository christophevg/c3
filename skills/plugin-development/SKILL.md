---
name: plugin-development
description: This skill should be used when the user asks to "create a plugin", "scaffold a plugin", "understand plugin structure", "organize plugin components", "set up plugin.json", "add commands, agents, skills, hooks", "configure auto-discovery", or needs guidance on plugin directory layout, manifest configuration, component organization, file naming conventions, or Claude Code plugin architecture best practices.
version: 1.0.0
---

# Plugin Development for Claude Code

Guide for designing, creating, maintaining, and improving Claude Code plugins that bundle skills, agents, hooks, and MCP servers.

## Overview

Claude Code plugins are self-contained extension packages that follow a standardized structure with automatic component discovery. They differ from standalone `.claude/` configurations in three key ways:

1. **Namespacing** - Plugin skills are prefixed (e.g., `/my-plugin:hello`)
2. **Distribution** - Shared via marketplaces with version control
3. **Reusability** - Work across multiple projects

---

## Phase 1: Discovery

Before scaffolding, understand what the plugin needs:

### Questions to Ask

1. **What does the plugin do?**
   - Skills only? Agents only? Both?
   - MCP server integration?
   - Hooks for automation?

2. **What components are needed?**
   | Component | Purpose | When to Use |
   |-----------|---------|-------------|
   | Skills | Model-invoked capabilities | Most plugins |
   | Agents | Autonomous subprocesses | Complex multi-step tasks |
   | Hooks | Event-driven automation | Automation workflows |
   | MCP Servers | External tool integration | API wrappers, services |

3. **How will it be distributed?**
   - Personal use → Local install
   - Team use → Project scope
   - Public → Marketplace

---

## Phase 2: Structure

Create the plugin directory:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── skills/                   # Skills (preferred format)
│   └── skill-name/
│       └── SKILL.md
├── agents/                   # Agent definitions
│   └── agent-name.md
├── hooks/
│   └── hooks.json           # Event handlers
├── .mcp.json                # MCP servers (optional)
└── README.md                # Documentation
```

### Critical Rules

1. **Manifest location**: `plugin.json` MUST be in `.claude-plugin/`
2. **Component locations**: All components MUST be at plugin root, NOT inside `.claude-plugin/`
3. **Optional components**: Only create directories you actually use
4. **Naming convention**: Use kebab-case for all directory and file names

---

## Phase 3: Manifest

Create `.claude-plugin/plugin.json`:

### Minimal Manifest

```json
{
  "name": "my-plugin"
}
```

### Recommended Manifest

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "homepage": "https://docs.example.com",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

### Version Format

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes

**Warning:** If you change plugin code without bumping version, existing users won't see changes due to caching.

---

## Phase 4: Components

### Skills

Create in `skills/` directory:

```
skills/
├── code-reviewer/
│   ├── SKILL.md              # Required
│   ├── references/           # Optional: Detailed docs
│   └── examples/             # Optional: Working examples
└── pdf-processor/
    └── SKILL.md
```

**SKILL.md frontmatter:**

```yaml
---
name: skill-name
description: This skill should be used when the user asks to "specific phrase", "another phrase".
version: 1.0.0
---
```

**Writing style:**
- Third person in description ("This skill should be used when...")
- Imperative/infinitive form in body ("To accomplish X, do Y")
- Keep SKILL.md lean (1,500-2,000 words)
- Move detailed content to references/

### Agents

Create in `agents/` directory:

```markdown
---
name: agent-name
description: Use this agent when [conditions]. Examples:
<example>
Context: [situation]
user: "[request]"
assistant: "[response]"
<commentary>[why triggered]</commentary>
</example>
model: inherit
color: blue
tools: ["Read", "Grep", "Glob"]
---

You are a specialized agent...
```

### Hooks

Create in `hooks/hooks.json`:

```json
{
  "description": "Plugin hook configuration",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate file write safety..."
          }
        ]
      }
    ]
  }
}
```

### MCP Servers

Create in `.mcp.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.py"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**Always use `${CLAUDE_PLUGIN_ROOT}` for paths.**

---

## Phase 5: Validate and Test

### Validation

```bash
claude plugin validate .
```

Checks:
- `plugin.json` syntax
- Skill/agent frontmatter
- Hook configuration
- Path references

### Local Testing

```bash
# Test with plugin directory
claude --plugin-dir /path/to/plugin

# Test specific components
claude --plugin-dir /path/to/plugin --skill skill-name
```

---

## Phase 6: Distribute

### For Marketplace Distribution

Update marketplace `marketplace.json`:

```json
{
  "name": "my-marketplace",
  "owner": { "name": "Author", "email": "author@example.com" },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin"
    }
  ]
}
```

### For GitHub Distribution

```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": {
        "source": "github",
        "repo": "username/repo"
      }
    }
  ]
}
```

### Installation

```bash
# From marketplace
claude plugin install my-plugin@marketplace-name

# From GitHub
claude plugin install username/repo

# From local path
claude plugin install /path/to/plugin
```

---

## Portable Paths

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin directory |
| `${CLAUDE_PLUGIN_DATA}` | Persistent data directory |
| `${user_config.KEY}` | User-configured values |

### Usage

```json
{
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/run.sh",
  "args": ["${CLAUDE_PLUGIN_ROOT}/config.json"]
}
```

**Never use:**
- Hardcoded absolute paths
- Relative paths from working directory
- Home directory shortcuts (`~`)

---

## Progressive Disclosure

Skills use a three-level loading system:

| Level | Content | When Loaded | Size |
|-------|---------|--------------|------|
| 1 | Metadata (name + description) | Always | ~100 words |
| 2 | SKILL.md body | When triggered | <5,000 words |
| 3 | references/, examples/, scripts/ | As needed | Unlimited |

**Best practice:** Keep SKILL.md lean (1,500-2,000 words). Move detailed content to references/.

---

## Additional Resources

### Reference Files

- **`references/manifest-reference.md`** — Complete plugin.json schema
- **`references/component-patterns.md`** — Skills, agents, hooks, MCP servers
- **`references/marketplace-distribution.md`** — Publishing and versioning
- **`references/progressive-disclosure.md`** — Content organization best practices

### External Links

- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)