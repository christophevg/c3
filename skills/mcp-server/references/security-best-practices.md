# MCP Server Security Best Practices

**Reference for:** `mcp-server` skill
**Priority levels:** CRITICAL > HIGH > MEDIUM

---

## Transport Security

### CRITICAL: Use stdio for Local Servers

```python
# ✅ CORRECT - No network exposure
mcp.run()  # stdio transport (default)

# ✅ CORRECT - Remote server with TLS
mcp.run(transport="http", port=8000)  # Use with HTTPS/TLS

# ❌ NEVER - Exposing stdio over network
# Don't use tools like ngrok to expose stdio servers
```

### CRITICAL: Require TLS for Remote Servers

```python
# For HTTP/SSE transport, always use TLS
# Configure reverse proxy (nginx, caddy) with TLS
# Or use Cloudflare Workers with automatic TLS
```

---

## Input Validation

### CRITICAL: Validate All Inputs

```python
from pydantic import BaseModel, Field
from typing import Annotated
import re

class SafeQuery(BaseModel):
    # Validate string patterns
    table: Annotated[str, Field(
        pattern=r'^[a-zA-Z_][a-zA-Z0-9_]*$',
        description="Table name (alphanumeric with underscores)"
    )]
    
    # Validate ranges
    limit: Annotated[int, Field(ge=1, le=1000)] = 100
    
    # Validate formats
    email: Annotated[str, Field(
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )]

@mcp.tool
def query(params: SafeQuery) -> list[dict]:
    """Query with validated inputs."""
    return db.query(params.table, params.limit)
```

### CRITICAL: Prevent Path Traversal

```python
from pathlib import Path

ALLOWED_ROOT = Path("/data/workspace").resolve()

def safe_path(user_path: str) -> Path:
    """Validate path doesn't escape allowed root."""
    target = (ALLOWED_ROOT / user_path).resolve()
    
    if not str(target).startswith(str(ALLOWED_ROOT)):
        raise ValueError(f"Path traversal detected: {user_path}")
    
    if not target.exists():
        raise ValueError(f"Path does not exist: {user_path}")
    
    return target

@mcp.tool
def read_file(path: str) -> str:
    """Read a file safely."""
    safe = safe_path(path)
    return safe.read_text()
```

### CRITICAL: Reject Dangerous Patterns

```python
DANGEROUS_PATTERNS = [
    r'\.\./',           # Path traversal
    r'[<>&|;]',         # Shell metacharacters
    r'\x00',            # Null bytes
    r'[$`\\]',          # Variable expansion
]

def validate_no_dangerous_patterns(value: str, field: str):
    """Reject inputs with dangerous patterns."""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, value):
            raise ValueError(f"Invalid {field}: dangerous pattern detected")

@mcp.tool
def execute(command: str, args: Annotated[str, Field(min_length=1)]) -> str:
    """Execute a command safely."""
    validate_no_dangerous_patterns(args, "args")
    # ... proceed
```

---

## Credential Management

### CRITICAL: Load from Environment Only

```python
import os

# ✅ CORRECT - Load from environment
API_KEY = os.environ.get("MY_API_KEY")
DB_URL = os.environ.get("DATABASE_URL")

# ❌ NEVER - Hardcode credentials
# API_KEY = "sk-abc123"  # NEVER DO THIS
# DB_URL = "postgres://user:pass@host/db"  # NEVER
```

### CRITICAL: Never Return Secrets

```python
@mcp.tool
def get_user(user_id: str) -> dict:
    """Get user information."""
    user = db.get_user(user_id)
    
    # ✅ CORRECT - Filter sensitive fields
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        # "api_key": user.api_key,  # OMITTED
        # "password_hash": user.password_hash,  # OMITTED
    }
```

### CRITICAL: Never Log Credentials

```python
import logging
import traceback

# ✅ CORRECT - Log safely
logger.error(f"Database error: {e}")

# ❌ NEVER - Log connection strings or tokens
# logger.error(f"Failed to connect: {DB_URL}")  # NEVER
# logger.error(f"API call failed: {API_KEY}")   # NEVER

# ✅ CORRECT - Mask in tracebacks
try:
    result = api.call()
except Exception as e:
    logger.error(f"API error: {e}\n{traceback.format_exc()}")
```

---

## Command Execution Safety

### CRITICAL: Never Pass User Input to Shell

```python
import subprocess

# ❌ NEVER - Shell injection vulnerability
# subprocess.run(f"git clone {user_url}", shell=True)  # NEVER

# ✅ CORRECT - Use argument list
@mcp.tool
def clone_repo(url: str) -> str:
    """Clone a repository safely."""
    validate_url(url)
    
    result = subprocess.run(
        ["git", "clone", url],
        capture_output=True,
        text=True
    )
    
    return result.stdout
```

### HIGH: Use Subprocess Safely

```python
@mcp.tool
def run_tool(name: str, args: list[str], timeout: int = 30) -> dict:
    """Run a tool with timeout and validation."""
    # Validate tool name is in allowed list
    if name not in ALLOWED_TOOLS:
        raise ValueError(f"Unknown tool: {name}")
    
    # Validate each argument
    for arg in args:
        validate_no_dangerous_patterns(arg, "argument")
    
    result = subprocess.run(
        [name] + args,
        capture_output=True,
        text=True,
        timeout=timeout
    )
    
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
```

---

## Resource Limits

### MEDIUM: Set Timeouts

```python
from fastmcp import FastMCP

mcp = FastMCP("MyApp")

# Set default timeout for all operations
# (FastMCP handles this internally, but be aware)

@mcp.tool
async def slow_operation(timeout: int = 30) -> dict:
    """Operation with explicit timeout."""
    import asyncio
    
    try:
        result = await asyncio.wait_for(
            perform_operation(),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        raise ToolError(f"Operation timed out after {timeout}s")
```

### MEDIUM: Limit Output Size

```python
MAX_OUTPUT_SIZE = 100_000  # characters

@mcp.tool
def read_file(path: str) -> str:
    """Read file with size limit."""
    safe = safe_path(path)
    content = safe.read_text()
    
    if len(content) > MAX_OUTPUT_SIZE:
        # Return truncated with indicator
        return content[:MAX_OUTPUT_SIZE] + "\n... [truncated]"
    
    return content
```

---

## Least Privilege

### HIGH: Run as Non-Root

```bash
# ✅ CORRECT - Run as dedicated user
sudo -u mcp_user python server.py

# ✅ CORRECT - Use containers with limited user
docker run --user 1000:1000 my-mcp-server
```

### HIGH: Limit File Access

```python
# Define allowed roots explicitly
ALLOWED_PATHS = {
    "workspace": Path("/workspace").resolve(),
    "data": Path("/data").resolve(),
}

@mcp.tool
def read_file(scope: str, path: str) -> str:
    """Read file from allowed scope."""
    if scope not in ALLOWED_PATHS:
        raise ValueError(f"Unknown scope: {scope}")
    
    root = ALLOWED_PATHS[scope]
    target = (root / path).resolve()
    
    if not str(target).startswith(str(root)):
        raise ValueError("Path escapes allowed scope")
    
    return target.read_text()
```

---

## Security Checklist

| Priority | Check | Status |
|----------|-------|--------|
| CRITICAL | stdio transport for local servers | ☐ |
| CRITICAL | TLS for remote servers | ☐ |
| CRITICAL | All inputs validated | ☐ |
| CRITICAL | No path traversal (`../`) | ☐ |
| CRITICAL | Credentials from env vars only | ☐ |
| CRITICAL | Never return secrets | ☐ |
| CRITICAL | Never log credentials | ☐ |
| CRITICAL | No shell injection | ☐ |
| HIGH | Subprocess uses argument lists | ☐ |
| HIGH | Timeouts set | ☐ |
| HIGH | Run as non-root user | ☐ |
| MEDIUM | Output size limits | ☐ |
| MEDIUM | Error masking enabled | ☐ |