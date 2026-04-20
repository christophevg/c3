# MCP Server Testing and Debugging

**Reference for:** `mcp-server` skill

---

## MCP Inspector (Official Tool)

The MCP Inspector is the primary tool for testing MCP servers.

### Installation and Usage

```bash
# Install and run
npx @modelcontextprotocol/inspector python my_server.py

# For TypeScript/Node servers
npx @modelcontextprotocol/inspector node server.js

# With arguments
npx @modelcontextprotocol/inspector python my_server.py --config config.json
```

### Capabilities

- **Protocol validation** - Verifies JSON-RPC compliance
- **Tool testing** - Invoke tools with custom parameters
- **Resource browsing** - List and read resources
- **Prompt testing** - Test prompt templates
- **Spec conformance** - Check against MCP specification

### Limitations

- Cannot see `console.log` output (stdout is protocol)
- Cannot observe real client traffic
- No multi-server debugging

---

## The Stdio Debugging Problem

### Critical: Log to stderr, NOT stdout

In stdio servers, `stdout` is reserved for the protocol. Any debug output to stdout breaks the connection.

```python
import sys
import logging

# ❌ NEVER - Breaks the protocol
print("debug info")

# ✅ CORRECT - Log to stderr
print("debug info", file=sys.stderr)

# ✅ BETTER - Structured logging to file
logging.basicConfig(
    filename='/tmp/mcp-debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("my-server")

@mcp.tool
def my_tool(query: str) -> dict:
    logger.debug(f"Processing query: {query}")
    # ...
    logger.debug(f"Result: {result}")
    return result
```

### FastMCP Context Logging

```python
from fastmcp import Context

@mcp.tool
async def process(query: str, ctx: Context = None) -> dict:
    # These go to stderr (FastMCP handles this)
    await ctx.info("Processing started")
    await ctx.debug(f"Query: {query}")
    await ctx.warning("Deprecated parameter used")
    
    result = await compute(query)
    
    await ctx.info(f"Processing complete: {len(result)} items")
    return result
```

---

## Testing Strategies

### Unit Testing

```python
import pytest
from my_server import mcp

def test_tool_schema():
    """Test tool schemas are valid."""
    tools = mcp.list_tools()
    
    for tool in tools:
        assert tool.name.isidentifier()
        assert tool.description
        assert "type" in tool.inputSchema
        assert tool.inputSchema["type"] == "object"

def test_tool_execution():
    """Test tool executes correctly."""
    result = mcp.call_tool("add", {"a": 2, "b": 3})
    assert result == 5

@pytest.mark.asyncio
async def test_async_tool():
    """Test async tool."""
    result = await mcp.call_tool_async("process", {"query": "test"})
    assert "status" in result
```

### Integration Testing

```python
import pytest
from fastmcp import FastMCP
from fastmcp.client import Client

@pytest.fixture
def client():
    """Create test client."""
    return Client(mcp)

@pytest.mark.asyncio
async def test_tool_via_client(client):
    """Test tool through MCP client."""
    result = await client.call_tool("add", {"a": 5, "b": 7})
    assert result == 12

@pytest.mark.asyncio
async def test_resource_via_client(client):
    """Test resource through MCP client."""
    content = await client.read_resource("config://app")
    assert "version" in content
```

### Security Testing

```python
import pytest

def test_path_traversal_prevented():
    """Test path traversal is blocked."""
    with pytest.raises(ValueError, match="traversal"):
        safe_path("../../../etc/passwd")

def test_shell_injection_prevented():
    """Test shell injection is blocked."""
    with pytest.raises(ValueError, match="dangerous"):
        validate_no_dangerous_patterns("test; rm -rf /")

def test_credentials_not_returned():
    """Test credentials are filtered."""
    result = get_user("user123")
    assert "password" not in result
    assert "api_key" not in result
```

### Schema Drift Detection

```python
def test_tool_schema_snapshot(snapshot):
    """Detect breaking changes in tool schemas."""
    tools = mcp.list_tools()
    
    # Compare against known-good snapshot
    assert tools == snapshot

def test_resource_schema_snapshot(snapshot):
    """Detect breaking changes in resource schemas."""
    resources = mcp.list_resources()
    assert resources == snapshot
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: MCP Server Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install fastmcp pytest pytest-asyncio
      
      - name: Run unit tests
        run: pytest tests/unit -v
      
      - name: Run integration tests
        run: pytest tests/integration -v
      
      - name: Check tool schemas
        run: pytest tests/schemas -v --snapshot-check
      
      - name: Run MCP Inspector
        run: npx @modelcontextprotocol/inspector python src/server.py &
            sleep 5
            # Run automated tests against inspector
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/unit -v
        language: system
        pass_filenames: false
        always_run: true
      
      - id: mypy
        name: mypy
        entry: mypy src/
        language: system
        pass_filenames: false
      
      - id: schema-check
        name: schema-check
        entry: pytest tests/schemas -v
        language: system
        pass_filenames: false
```

---

## Debugging Techniques

### Enable Debug Logging

```python
import logging

# Enable all debug output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('/tmp/mcp-debug.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
```

### Protocol-Level Debugging

```python
# Monkey-patch to log all protocol messages
import json

original_send = server.send
async def logged_send(message):
    print(f"SEND: {json.dumps(message, indent=2)}", file=sys.stderr)
    return await original_send(message)

server.send = logged_send
```

### Connection Testing

```python
# Test basic connectivity
import asyncio
from fastmcp import FastMCP

async def test_connection():
    mcp = FastMCP("test")
    
    # Test tool
    result = await mcp.call_tool_async("test", {})
    print(f"Tool result: {result}")
    
    # Test resource
    content = await mcp.read_resource_async("test://resource")
    print(f"Resource content: {content}")

asyncio.run(test_connection())
```

### Error Isolation

```python
@mcp.tool
def debug_tool(query: str) -> dict:
    """Tool with detailed error reporting."""
    try:
        result = risky_operation(query)
        return {"success": True, "result": result}
    
    except ValueError as e:
        # Client-friendly error
        raise ToolError(f"Invalid input: {e}")
    
    except Exception as e:
        # Log full traceback for debugging
        logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
        
        # Return generic error to client
        raise ToolError("Internal error - check server logs")
```

---

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Server not responding | stdout used for logs | Use stderr or file logging |
| Tool not found | Incorrect registration | Check `@mcp.tool` decorator |
| Protocol error | Malformed response | Validate JSON structure |
| Timeout | Slow operation | Add explicit timeout |
| Path denied | Traversal blocked | Check allowed roots |
| Auth failure | Missing credentials | Check environment variables |

---

## Performance Testing

```python
import asyncio
import time
from statistics import mean, stdev

async def benchmark_tool(name: str, args: dict, n: int = 100):
    """Benchmark tool performance."""
    times = []
    
    for _ in range(n):
        start = time.perf_counter()
        await mcp.call_tool_async(name, args)
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        "tool": name,
        "iterations": n,
        "mean_ms": mean(times) * 1000,
        "stdev_ms": stdev(times) * 1000,
        "min_ms": min(times) * 1000,
        "max_ms": max(times) * 1000,
    }

# Run benchmarks
async def run_benchmarks():
    results = await asyncio.gather(
        benchmark_tool("add", {"a": 1, "b": 2}),
        benchmark_tool("query", {"table": "users"}),
    )
    
    for r in results:
        print(f"{r['tool']}: {r['mean_ms']:.2f}ms (±{r['stdev_ms']:.2f})")
```