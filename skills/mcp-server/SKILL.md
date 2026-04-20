---
name: mcp-server
description: This skill should be used when the user asks to "build an MCP server", "create an MCP", "make an MCP integration", "wrap an API for Claude", "expose tools to Claude", "develop MCP tools", "implement MCP resources", or discusses building something with the Model Context Protocol. It provides comprehensive guidance for designing, creating, testing, and deploying MCP servers.
version: 1.0.0
---

# MCP Server Development

Guide for designing and building MCP (Model Context Protocol) servers that connect Claude to external tools, APIs, and data sources.

## Overview

MCP servers bridge Claude with external systems using a standardized protocol. Three primitives are available:

| Primitive | Controlled By | Purpose |
|-----------|---------------|---------|
| **Tools** | Model (Claude) | Functions Claude can invoke |
| **Resources** | Application | Contextual data Claude can read |
| **Prompts** | User | Templates users can invoke |

---

## Phase 1: Discovery

Before coding, understand the use case. Ask these questions:

### 1. What does it connect to?

| Connection Type | Recommended Approach |
|-----------------|----------------------|
| Cloud API (SaaS, REST, GraphQL) | Remote HTTP server |
| Local process, filesystem, desktop app | MCPB or local stdio |
| Hardware, OS-level APIs | MCPB |
| Pure logic/computation | Either - default to remote |

### 2. Who will use it?

- **Just me / my team** → Local stdio acceptable
- **Anyone who installs it** → Remote HTTP (preferred) or MCPB
- **Claude desktop with UI widgets** → MCP app

### 3. How many distinct actions?

- **Under ~15 actions** → One tool per action
- **Dozens to hundreds** → Search + execute pattern

### 4. Does a tool need user input mid-call?

- **Simple forms (pick, enter, confirm)** → Elicitation (spec-native)
- **Rich UI (charts, search, dashboards)** → MCP app widgets
- **Neither** → Plain tool returning text/JSON

### 5. What authentication does the service use?

- None / API key → Straightforward
- OAuth 2.0 → Remote server with CIMD or DCR support

---

## Phase 2: Recommend Deployment Model

Based on discovery answers, recommend ONE path:

### ⭐ Remote HTTP Server (Default)

Hosted service speaking MCP over streamable HTTP. Best for cloud API wrappers.

**Benefits:**
- Zero install friction - users add a URL
- One deployment serves all users
- OAuth flows work properly
- Works across Claude desktop, Claude Code, Claude.ai

**Choose unless** server must touch local machine.

### MCPB (Bundled Local Server)

Local server packaged with its runtime. No Node/Python needed on user machine.

**Choose when** server must run on user's machine:
- Reads local files
- Drives desktop apps
- Talks to localhost services
- Needs OS-level access

### Local stdio (Prototypes Only)

Script launched via `npx` / `uvx`. Fine for personal tools and prototypes.

**Not recommended for distribution** - users need runtime, no update mechanism.

---

## Phase 3: Pick Tool Design Pattern

### Pattern A: One Tool Per Action (Small Surface)

When action space is small (< ~15 operations), each gets a dedicated tool.

```
create_issue   — Create a new issue
update_issue   — Update an existing issue
search_issues  — Search issues by query
add_comment    — Add a comment
```

**Benefits:** Claude reads tool list once, knows exactly what's possible.

### Pattern B: Search + Execute (Large Surface)

When wrapping large APIs (dozens+ endpoints), use TWO tools:

```
search_actions  — Return matching actions with IDs and schemas
execute_action  — Run an action by ID with params
```

**Benefits:** Server holds catalog internally, context stays lean.

**Hybrid:** Promote 3-5 most-used actions to dedicated tools.

---

## Phase 4: Pick Framework

| Framework | Language | When to Use |
|-----------|----------|-------------|
| **FastMCP 3.x** | Python | Python preference, wrapping Python libraries |
| **TypeScript SDK** | TypeScript | Default choice, best spec coverage |

Both produce identical wire protocol.

---

## Phase 5: Scaffold Server

### FastMCP (Python)

```python
from fastmcp import FastMCP

mcp = FastMCP("server-name")

@mcp.tool
def my_tool(query: str) -> dict:
    """Tool description Claude sees."""
    return process(query)

if __name__ == "__main__":
    mcp.run()  # stdio (default)
    # mcp.run(transport="http", port=8000)  # HTTP
```

### TypeScript SDK

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({
  name: "server-name",
  version: "1.0.0"
});

server.tool("myTool", { query: z.string() }, async ({ query }) => ({
  content: [{ type: "text", text: JSON.stringify(process(query)) }]
}));

server.connect(transport);
```

---

## Phase 6: Test and Publish

### Testing

```bash
# MCP Inspector - official testing tool
npx @modelcontextprotocol/inspector python server.py
```

**Critical:** Log to stderr, NOT stdout (stdout is the protocol).

### Pre-submission Checklist

- Read/write tool split for destructive operations
- Required annotations on all tools
- Tool names under 128 characters
- No prompt injection in tool output
- Input validation on all parameters

### Distribution

- Submit to Anthropic Directory
- Create plugin wrapper for skills
- Document installation clearly

---

## Security Essentials

| Priority | Practice |
|----------|----------|
| CRITICAL | Use stdio for local servers (no network) |
| CRITICAL | Require TLS for remote servers |
| CRITICAL | Validate all inputs (types, ranges, formats) |
| CRITICAL | Reject path traversal (`../`) |
| CRITICAL | Load credentials from environment only |
| CRITICAL | Never return secrets in tool output |
| HIGH | Run as non-root user |
| HIGH | Use argument lists, never shell strings |

---

## Additional Resources

### Reference Files

Consult these for detailed implementation guidance:

- **`references/fastmcp-patterns.md`** — FastMCP decorator patterns, type hints, context injection
- **`references/security-best-practices.md`** — Input validation, credential management, path traversal prevention
- **`references/testing-debugging.md`** — MCP Inspector, stderr logging, CI/CD integration
- **`references/deployment-options.md`** — stdio, HTTP/SSE, Cloudflare Workers, Docker, MCPB

### External Links

- [MCP Specification](https://modelcontextprotocol.io/specification/latest)
- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Python SDK](https://py.sdk.modelcontextprotocol.io/)