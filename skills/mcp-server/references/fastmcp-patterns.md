# FastMCP Implementation Patterns

**Reference for:** `mcp-server` skill
**Framework:** FastMCP 3.x (Python)

---

## Basic Server Structure

```python
from fastmcp import FastMCP

mcp = FastMCP("server-name")

# Tools, resources, prompts defined here

if __name__ == "__main__":
    mcp.run()  # stdio transport (default)
```

**Note:** FastMCP 3.x constructor accepts only the server name. The `description` parameter is not supported.

---

## Tool Definitions

### Simple Tool

```python
@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

### Tool with Validation

```python
from typing import Annotated
from pydantic import Field

@mcp.tool
def search(
    query: Annotated[str, Field(description="Search query", min_length=1)],
    limit: Annotated[int, Field(ge=1, le=100)] = 10
) -> list[dict]:
    """Search for items matching the query."""
    return perform_search(query, limit)
```

### Tool with Context Access

```python
from fastmcp import Context

@mcp.tool
async def process(query: str, ctx: Context = None) -> dict:
    """Process a query with logging."""
    await ctx.info(f"Processing: {query}")
    result = await compute(query)
    await ctx.debug(f"Result: {result}")
    return result
```

### Tool with Pydantic Model

```python
from pydantic import BaseModel

class QueryParams(BaseModel):
    table: Annotated[str, Field(pattern=r'^[a-zA-Z_][a-zA-Z0-9_]*$')]
    limit: Annotated[int, Field(ge=1, le=1000)] = 100
    offset: Annotated[int, Field(ge=0)] = 0

@mcp.tool
def query(params: QueryParams) -> list[dict]:
    """Query a database table."""
    return db.query(params.table, params.limit, params.offset)
```

---

## Resource Definitions

### Static Resource

```python
@mcp.resource("config://app")
def get_config() -> str:
    """Get application configuration."""
    return json.dumps({"version": "1.0", "debug": False})
```

### Parameterized Resource Template

```python
@mcp.resource("file://{path*}")
def read_file(path: str) -> str:
    """Read a file from the workspace."""
    return open(f"/workspace/{path}").read()
```

### Binary Resource

```python
@mcp.resource("image://{id}")
def get_image(id: str) -> bytes:
    """Get an image by ID."""
    return database.get_image_bytes(id)
```

### Resource with Metadata

```python
from fastmcp import ResourceResult

@mcp.resource("data://{collection}/{id}")
def get_data(collection: str, id: str) -> ResourceResult:
    """Get data with metadata."""
    return ResourceResult(
        content=fetch_data(collection, id),
        mime_type="application/json",
        metadata={"created": "2024-01-01"}
    )
```

---

## Prompt Definitions

### Simple Prompt

```python
from fastmcp.prompts import Message

@mcp.prompt
def code_review(code: str) -> str:
    """Generate a code review request."""
    return f"Please review this code for bugs and improvements:\n\n{code}"
```

### Multi-Message Prompt

```python
@mcp.prompt
def analyze_data(data: str) -> list[Message]:
    """Generate a data analysis request."""
    return [
        Message(role="assistant", content="I'll analyze your data."),
        Message(role="user", content=f"Analyze this:\n{data}"),
    ]
```

### Prompt with Arguments

```python
@mcp.prompt
def translate(text: str, language: str = "spanish") -> str:
    """Translate text to another language."""
    return f"Translate the following to {language}:\n\n{text}"
```

---

## Error Handling

### Tool Errors

```python
from fastmcp.exceptions import ToolError

@mcp.tool
def divide(a: int, b: int) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ToolError("Division by zero is not allowed")
    return a / b
```

### Error Masking

```python
# Hide internal details from clients
mcp = FastMCP("MyApp", mask_error_details=True)

# Only ToolError messages are visible to clients
# Other exceptions show generic error message
```

---

## Dependency Injection

### Using Depends

```python
from fastmcp import Depends

def get_database():
    return Database()

@mcp.tool
def query(db: Database = Depends(get_database), query: str) -> list:
    """Query the database."""
    return db.execute(query)
```

### Hidden Dependencies

```python
# Dependencies are hidden from the LLM - not in schema
@mcp.tool
def get_user(user_id: str, db: Database = Depends(get_database)) -> dict:
    """Get user by ID."""
    return db.get_user(user_id)
```

---

## Lifespan Management

### Async Context Manager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Startup
    db = await Database.connect()
    yield {"db": db}
    # Shutdown
    await db.disconnect()

mcp = FastMCP("MyApp", lifespan=lifespan)
```

### Using Lifespan State

```python
@mcp.tool
async def query(state: dict, query: str) -> list:
    """Query using lifespan database."""
    return await state["db"].execute(query)
```

---

## Transport Options

### stdio (Default)

```python
if __name__ == "__main__":
    mcp.run()  # stdio transport
```

### HTTP/SSE

```python
if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

### Programmatic

```python
import asyncio
from fastmcp import FastMCP

mcp = FastMCP("MyApp")

async def main():
    # For embedding in other applications
    async with mcp.run_async() as (read, write):
        await handle_connection(read, write)

asyncio.run(main())
```

---

## Complete Example

```python
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from typing import Annotated

# Create server
mcp = FastMCP("example-server")

# Define models
class Item(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    value: Annotated[int, Field(ge=0)]

# Tools
@mcp.tool
def create_item(item: Item) -> dict:
    """Create a new item."""
    return {"id": 1, "name": item.name, "value": item.value}

@mcp.tool
async def process_items(ctx: Context = None) -> dict:
    """Process all items with logging."""
    await ctx.info("Starting processing")
    result = await compute_items()
    await ctx.debug(f"Processed {len(result)} items")
    return {"processed": len(result)}

# Resources
@mcp.resource("items://{id}")
def get_item(id: str) -> str:
    """Get item by ID."""
    return json.dumps(fetch_item(id))

# Prompts
@mcp.prompt
def analyze_item(item_id: str) -> str:
    """Generate item analysis request."""
    return f"Analyze the item with ID {item_id} for patterns."

# Run
if __name__ == "__main__":
    mcp.run()
```