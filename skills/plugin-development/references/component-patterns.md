# Plugin Component Patterns

**Reference for:** `plugin-development` skill

---

## Skills (SKILL.md)

Skills are model-invoked capabilities that Claude automatically uses based on task context. They are the **preferred format** for plugin functionality.

### Directory Structure

```
skills/
├── code-reviewer/
│   ├── SKILL.md              # Required
│   ├── references/           # Optional: Detailed docs
│   │   └── patterns.md
│   ├── examples/             # Optional: Working examples
│   │   └── review.md
│   └── scripts/              # Optional: Utility scripts
│       └── validate.sh
└── pdf-processor/
    └── SKILL.md
```

### SKILL.md Format

```markdown
---
name: skill-name
description: This skill should be used when the user asks to "specific phrase", "another phrase", mentions "keyword", or discusses topic-area.
version: 1.0.0
disable-model-invocation: false
allowed-tools: [Read, Write, Grep]
---

# Skill Name

Brief overview of what this skill does.

## When to Use

[Specific trigger conditions]

## Instructions

[Detailed procedural guidance]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier |
| `description` | Yes | Trigger conditions (third person) |
| `version` | No | Semantic version |
| `disable-model-invocation` | No | If true, only user-invoked |
| `allowed-tools` | No | Restrict tool access |
| `argument-hint` | No | Expected arguments for autocomplete |

### Writing Style

- **Third person in description:** "This skill should be used when..."
- **Imperative/infinitive form in body:** "To accomplish X, do Y"
- **Objective, instructional language:** No "You should..."

---

## Agents

Agents are autonomous subprocesses that handle complex, multi-step tasks independently. They have restricted tool access and specialized system prompts.

### File Format

```markdown
---
name: code-reviewer
description: Use this agent when [triggering conditions]. Examples:

<example>
Context: [Situation description]
user: "[User request]"
assistant: "[How assistant should respond]"
<commentary>
[Why this agent should be triggered]
</commentary>
</example>

model: inherit
color: blue
effort: medium
maxTurns: 20
tools: ["Read", "Grep", "Glob"]
disallowedTools: ["Write", "Edit"]
skills: ["code-analysis"]
memory: true
background: false
isolation: "worktree"
---

You are a specialized code reviewer...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Agent identifier (kebab-case) |
| `description` | Yes | Triggering conditions with `<example>` blocks |
| `model` | Yes | `inherit`, `sonnet`, `opus`, `haiku` |
| `color` | Yes | Visual identifier: `blue`, `cyan`, `green`, `yellow`, `magenta`, `red` |
| `effort` | No | `low`, `medium`, `high` |
| `maxTurns` | No | Maximum turns |
| `tools` | No | Array of allowed tools |
| `disallowedTools` | No | Array of blocked tools |
| `skills` | No | Skills to inherit |
| `memory` | No | Enable session memory |
| `background` | No | Run as background agent |
| `isolation` | No | Only valid value: `"worktree"` |

### Description Best Practices

Include 2-4 `<example>` blocks with:
- Context scenario
- User request
- Assistant response
- Commentary explaining trigger reasoning

---

## Hooks

Hooks are event-driven automation scripts that execute in response to Claude Code events.

### Hook Events

| Event | When it fires |
|-------|---------------|
| `SessionStart` | Session begins or resumes |
| `UserPromptSubmit` | User submits a prompt |
| `PreToolUse` | Before tool executes (can block) |
| `PostToolUse` | After tool succeeds |
| `PostToolUseFailure` | After tool fails |
| `Stop` | Main agent considers stopping |
| `SubagentStart` | Subagent spawned |
| `SubagentStop` | Subagent finishes |
| `Notification` | Claude sends notification |
| `SessionEnd` | Session terminates |
| `PreCompact` | Before context compaction |
| `PostCompact` | After context compaction |
| `FileChanged` | Watched file changes |
| `ConfigChange` | Configuration file changes |
| `CwdChanged` | Working directory changes |

### Hook Configuration

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
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Hook Types

| Type | Use For | Timeout |
|------|---------|---------|
| `prompt` | LLM-driven decisions, context-aware validation | 30s default |
| `command` | Deterministic checks, file operations | 60s default |
| `http` | POST to external service | 30s default |
| `agent` | Complex verification with tools | 60s default |

### Matchers

```json
"matcher": "Write"                    // Exact match
"matcher": "Write|Edit|Bash"          // Multiple tools
"matcher": "*"                         // All tools
"matcher": "mcp__.*"                   // All MCP tools (regex)
```

### Hook Output Format

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude",
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask"
  }
}
```

---

## MCP Servers

MCP servers connect Claude Code with external tools and services.

### Configuration in .mcp.json

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

### Tool Naming

MCP tools are automatically prefixed:

- Format: `mcp__<server-name>__<tool-name>`
- Example: `mcp__database__query`
- For plugins: `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`

---

## Environment Variables

### Plugin-Specific Variables

| Variable | Purpose |
|----------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin installation directory |
| `${CLAUDE_PLUGIN_DATA}` | Persistent data directory (survives updates) |
| `${user_config.KEY}` | User-configured values |

### Usage Locations

Available for substitution in:
- MCP and LSP server configs
- Hook commands
- Monitor commands
- Skill and agent content (non-sensitive values only)

### Persistent Data Directory

`CLAUDE_PLUGIN_DATA` resolves to `~/.claude/plugins/data/{id}/`

**Use for:**
- Installed dependencies
- Generated code
- Caches
- State files that survive updates