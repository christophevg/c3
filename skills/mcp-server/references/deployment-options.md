# MCP Server Deployment Options

**Reference for:** `mcp-server` skill

---

## Transport Selection Guide

| Use Case | Transport | Reason |
|----------|-----------|--------|
| Local development | stdio | No network, simplest |
| CLI tools | stdio | No network exposure |
| VS Code extension | stdio | Embedded in editor |
| Remote server | HTTP/SSE | Network access required |
| Cloud deployment | HTTP/SSE | Load balancing, TLS |
| High-performance embedded | In-process | No serialization |

---

## stdio Transport (Local Servers)

### When to Use

- Local tools and integrations
- Desktop applications
- CLI tools
- Development and testing

### FastMCP Implementation

```python
from fastmcp import FastMCP

mcp = FastMCP("local-server")

# ... define tools, resources, prompts

if __name__ == "__main__":
    mcp.run()  # stdio is default
```

### Plugin Configuration

```json
// .mcp.json
{
  "mcpServers": {
    "my-tool": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.py"]
    }
  }
}
```

### Using uvx (Python)

```json
{
  "mcpServers": {
    "my-tool": {
      "command": "uvx",
      "args": ["my-mcp-package"]
    }
  }
}
```

### Using npx (Node)

```json
{
  "mcpServers": {
    "my-tool": {
      "command": "npx",
      "args": ["-y", "my-mcp-package"]
    }
  }
}
```

---

## HTTP/SSE Transport (Remote Servers)

### When to Use

- Cloud API wrappers
- Multi-user access
- Centralized services
- OAuth authentication

### FastMCP Implementation

```python
from fastmcp import FastMCP

mcp = FastMCP("remote-server")

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

### Plugin Configuration

```json
{
  "mcpServers": {
    "remote-api": {
      "type": "sse",
      "url": "https://api.example.com/sse"
    }
  }
}
```

### With Authentication

```json
{
  "mcpServers": {
    "remote-api": {
      "type": "sse",
      "url": "https://api.example.com/sse",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

---

## Cloudflare Workers Deployment

Fastest path to a live URL for remote servers.

### Setup

```bash
# Install Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login
```

### Project Structure

```
my-mcp-worker/
├── wrangler.toml
├── package.json
└── src/
    └── index.ts
```

### wrangler.toml

```toml
name = "my-mcp-server"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[vars]
ENVIRONMENT = "production"
```

### TypeScript Server

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0"
});

server.tool("greet", {
  name: z.string()
}, async ({ name }) => ({
  content: [{ type: "text", text: `Hello, ${name}!` }]
}));

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Handle MCP protocol
    return server.handle(request);
  }
};
```

### Deploy

```bash
# Deploy to Cloudflare
wrangler deploy

# Output: https://my-mcp-server.username.workers.dev
```

### Environment Variables

```bash
# Set secrets
wrangler secret put API_KEY

# Or in wrangler.toml (non-sensitive)
[vars]
MAX_RESULTS = "100"
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server
COPY . .

# Run as non-root
USER 1000:1000

# Expose port (for HTTP transport)
EXPOSE 8000

# Run server
CMD ["python", "server.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=${API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    restart: unless-stopped
```

### Running

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f mcp-server
```

---

## MCPB (Bundled Local Server)

For distributing local servers that users can install without Node/Python.

### When to Use

- Desktop applications
- Hardware access
- Local file system operations
- User-specific state

### Structure

```
my-mcpb/
├── manifest.json
├── server.py (or server.js)
└── runtime/
    └── ... (bundled interpreter)
```

### manifest.json

```json
{
  "name": "my-local-tool",
  "version": "1.0.0",
  "description": "Local MCP server",
  "runtime": "python",
  "entrypoint": "server.py",
  "tools": ["greet", "process"]
}
```

### Installation

Users install via:
```bash
/plugin install my-local-tool@mcpb
```

---

## Prefect Horizon (Free Hosting)

FastMCP offers free hosting through Prefect Horizon.

### Steps

1. Push code to GitHub
2. Sign in to horizon.prefect.io
3. Create project with entrypoint `my_server.py:mcp`

### Limitations

- Rate limits apply
- Cold starts on free tier
- Best for development/prototyping

---

## Environment Variables

### For Credentials

```python
import os

# Load from environment
API_KEY = os.environ.get("MY_API_KEY")
DB_URL = os.environ.get("DATABASE_URL")
```

### In Plugin Configuration

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.py"],
      "env": {
        "API_KEY": "${API_KEY}",
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### In Docker

```bash
# Pass environment variables
docker run -e API_KEY=xxx -e DATABASE_URL=xxx my-server

# Or use .env file
docker run --env-file .env my-server
```

---

## Health Checks

### For HTTP Servers

```python
from fastmcp import FastMCP

mcp = FastMCP("MyApp")

@mcp.tool
def health() -> dict:
    """Server health status."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "uptime": get_uptime()
    }
```

### Monitoring Endpoint

For HTTP transport, add a simple health endpoint:

```python
from fastapi import FastAPI
from fastmcp import FastMCP

mcp = FastMCP("MyApp")
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# Mount MCP
app.mount("/mcp", mcp.get_asgi_app())
```

---

## Scaling Considerations

### Stateless Design

```python
# ✅ CORRECT - Stateless tool
@mcp.tool
def process(query: str) -> dict:
    """Stateless processing."""
    return compute(query)

# ❌ AVOID - Stateful tool
_session_data = {}

@mcp.tool
def process_with_state(query: str) -> dict:
    """Stateful - problematic for scaling."""
    _session_data[query] = compute(query)
    return _session_data[query]
```

### Connection Pooling

```python
from contextlib import asynccontextmanager
import asyncpg

@asynccontextmanager
async def lifespan(app):
    # Shared connection pool
    app.db_pool = await asyncpg.create_pool(DATABASE_URL)
    yield
    await app.db_pool.close()

mcp = FastMCP("MyApp", lifespan=lifespan)
```

### Rate Limiting

```python
from functools import wraps
import time

def rate_limit(calls: int, period: int):
    """Rate limit decorator."""
    timestamps = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            timestamps[:] = [t for t in timestamps if now - t < period]
            
            if len(timestamps) >= calls:
                raise ToolError("Rate limit exceeded")
            
            timestamps.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@mcp.tool
@rate_limit(calls=10, period=60)
def limited_tool(query: str) -> dict:
    """Tool with rate limiting."""
    return process(query)
```

---

## Deployment Checklist

| Item | Status |
|------|--------|
| Transport selected appropriately | ☐ |
| Credentials in environment variables | ☐ |
| TLS enabled (for HTTP) | ☐ |
| Health check endpoint | ☐ |
| Error masking enabled | ☐ |
| Logging to stderr (stdio) | ☐ |
| Timeouts configured | ☐ |
| Rate limiting implemented | ☐ |
| Non-root user | ☐ |
| Documentation updated | ☐ |