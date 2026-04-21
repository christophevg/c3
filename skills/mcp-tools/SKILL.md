---
name: mcp-tools
description: Use this skill when you need to work with MCP (Model Context Protocol) tools exposed by MCP servers. Covers tool discovery, naming conventions, and configuration for sub-agents. Use when the user mentions "MCP tools", "use the MCP server", or you need to access functionality exposed by configured MCP servers.
version: 2.0.0
---

# Using MCP Tools

Guide for working with MCP tools in Claude Code, including configuration for custom sub-agents.

---

## ⚠️ Critical: Sub-Agent Limitation

**MCP tools do NOT automatically inherit to custom sub-agents.**

- The **general-purpose agent** gets MCP tools injected at session start
- **Custom sub-agents** do NOT inherit them automatically
- There is **no ToolSearch** available to sub-agents
- There is **no programmatic way** to discover MCP tools in sub-agents

**Workaround:** Explicitly list MCP tool names in the sub-agent's `allowed_tools` definition.

---

## Tool Naming Convention

MCP tools follow this pattern:

```
mcp__<server-name-with-underscores>__<tool-name>
```

**Important:** Server names use **underscores**, not colons!

| Config Server Name | Tool Prefix |
|-------------------|-------------|
| `plugin:c3:email` | `mcp__plugin_c3_email__*` |
| `claude-in-chrome` | `mcp__claude_in_chrome__*` |
| `computer-use` | `mcp__computer_use__*` |

---

## Configuring Sub-Agent Access

To grant a sub-agent access to MCP tools, explicitly list them in the agent definition:

```yaml
allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Skill
  - Agent
  # MCP Email Tools - explicitly listed
  - mcp__plugin_c3_email__list_accounts
  - mcp__plugin_c3_email__list_folders
  - mcp__plugin_c3_email__search_emails
  - mcp__plugin_c3_email__get_email
  - mcp__plugin_c3_email__send_email
  - mcp__plugin_c3_email__reply_email
  - mcp__plugin_c3_email__move_email
  - mcp__plugin_c3_email__delete_email
  - mcp__plugin_c3_email__download_attachment
```

### Wildcard Pattern

Some configurations may support wildcards:

```yaml
allowed_tools:
  - mcp__plugin_c3_email__*  # All email tools
```

Test whether wildcards work for your Claude Code version.

---

## Available Email Tools

| Tool | Description |
|------|-------------|
| `list_accounts` | List configured email accounts |
| `list_folders` | List folders/mailboxes for an account |
| `search_emails` | Search emails with IMAP criteria |
| `get_email` | Fetch a single email by ID |
| `send_email` | Send a new email |
| `reply_email` | Reply to an existing email |
| `move_email` | Move email between folders |
| `delete_email` | Delete an email |
| `download_attachment` | Download attachment from email |

---

## Finding Tool Names

To discover what tools an MCP server exposes:

### Method 1: Check the General-Purpose Agent

Start a general-purpose agent session and ask for tool definitions:

```
What MCP tools do you have access to?
What (exact) function definitions were provided to you?
```

### Method 2: Check MCP Server Source

Look at the MCP server's tool definitions file:

```
~/.claude/plugins/cache/<plugin>/email/src/email_mcp/tools/definitions.py
```

### Method 3: Check MCP Server Connection

```
claude mcp list
```

Shows connected servers. Then derive tool names from server name.

---

## Usage Example

Once configured, use MCP tools directly:

```
# List accounts
mcp__plugin_c3_email__list_accounts()

# Search emails
mcp__plugin_c3_email__search_emails(
  account: "default",
  folder: "INBOX",
  criteria: "ALL",
  limit: 50
)

# Get specific email
mcp__plugin_c3_email__get_email(
  account: "default",
  message_id: "<message-id>",
  folder: "INBOX"
)
```

---

## Workflow Summary

| Step | Action |
|------|--------|
| 1 | Identify MCP server name from config |
| 2 | Convert to tool prefix (replace `:` with `_`) |
| 3 | List tools explicitly in sub-agent definition |
| 4 | Use tools directly — no ToolSearch needed |

---

## Security Notes

- MCP tools run with user permissions
- Email tools may send/delete emails — verify before destructive actions
- Only grant tools that the sub-agent actually needs

---

## Related Skills

- `mcp-server` — Building and deploying MCP servers
- `update-config` — Configuring settings and permissions