---
name: quart-webapp
type: knowledge
description: |
  Use this skill when creating or modifying Quart webapps with Uvicorn. Covers application factory pattern, WebSocket endpoints, CORS configuration, and Python webapp standards. Examples: "create a Quart webapp", "add WebSocket endpoint", "configure CORS for webapp", "set up uvicorn".
---

# quart-webapp

Patterns and best practices for Quart/Uvicorn webapps in Python.

## Overview

| Capability | Description |
|------------|-------------|
| Application factory | Quart factory pattern with configuration |
| WebSocket support | Real-time bidirectional communication |
| CORS configuration | Cross-origin resource sharing setup |
| Security patterns | CSWSH prevention, origin validation |
| Test UI | Simple interfaces for testing endpoints |

## When to Use This Skill

Use this skill when:
- Creating a new Quart webapp
- Adding WebSocket endpoints
- Configuring CORS for webapps
- Setting up Uvicorn server
- Implementing health check endpoints
- Creating test pages for WebSocket testing
- Working with Python async web frameworks

## Project Structure

```
src/<project>/webapp/
├── __init__.py           # Public API exports
├── __main__.py           # Entry point: uv run python -m <project>.webapp
├── app.py                # Application factory
├── routes/
│   ├── __init__.py
│   ├── health.py         # Health check endpoint
│   ├── index.py          # Index page (optional test UI)
│   └── chat.py           # WebSocket endpoint
├── middleware/
│   ├── __init__.py
│   ├── cors.py           # CORS and origin validation
│   └── auth.py           # Authentication hooks
├── handlers/
│   ├── __init__.py
│   └── websocket.py      # WebSocket event handlers
└── session/
    ├── __init__.py
    └── manager.py         # Session management
```

## Dependencies

```toml
[project.dependencies]
quart = ">=0.19.0,<0.21.0"
quart-cors = ">=0.7.0,<0.9.0"
uvicorn = ">=0.30.0,<0.35.0"
```

## Application Factory Pattern

### app.py

```python
from quart import Quart
from quart_cors import cors

def create_app(config: Config | None = None) -> Quart:
    """Create and configure Quart application.
    
    Args:
        config: Configuration object (loads default if not provided).
    
    Returns:
        Configured Quart application.
    """
    app = Quart(__name__)
    
    # Load configuration
    if config is None:
        from <project>.config import load_config_with_defaults
        config = load_config_with_defaults()
    
    # Store config in app context
    app.config["APP_CONFIG"] = config
    
    # Configure CORS
    app = cors(app, allow_origin=list(config.webapp.cors_origins))
    
    # Register blueprints
    from <project>.webapp.routes.health import health_bp
    from <project>.webapp.routes.index import index_bp
    from <project>.webapp.routes.chat import chat_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(chat_bp)
    
    return app

# For uvicorn: uv run uvicorn <project>.webapp:app
app = create_app()
```

### __init__.py

```python
from <project>.webapp.app import create_app, app

__all__ = ["create_app", "app"]
```

### __main__.py

```python
import uvicorn

from <project>.config import load_config_with_defaults
from <project>.webapp import app

def main():
    """Run Quart webapp with Uvicorn."""
    config = load_config_with_defaults()
    
    print(f"Starting webapp on {config.webapp.host}:{config.webapp.port}")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        app,
        host=config.webapp.host,
        port=config.webapp.port,
        log_level="debug" if config.webapp.debug else "info",
    )

if __name__ == "__main__":
    main()
```

## Health Check Endpoint

### routes/health.py

```python
from quart import Blueprint, Response, jsonify
from quart_cors import cors_exempt

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
@cors_exempt  # Public endpoint, no CORS restriction
async def health_check() -> Response:
    """Health check endpoint.
    
    Returns:
        JSON response with status and version.
    """
    try:
        from <project> import __version__
        version = __version__
    except ImportError:
        version = "unknown"
    
    return jsonify({"status": "healthy", "version": version})
```

**Pattern:**
- Always use `@cors_exempt` for public health endpoints
- Return JSON with status and version
- Keep it simple and fast
- No authentication required

## WebSocket Endpoint

### routes/chat.py

```python
from quart import Blueprint, websocket, current_app
from quart_cors import cors_exempt
import json

chat_bp = Blueprint("chat", __name__)

@chat_bp.websocket("/ws/chat")
async def chat_websocket():
    """WebSocket chat endpoint.
    
    Handles real-time communication with event streaming.
    """
    # Get configuration
    config = current_app.config["APP_CONFIG"]
    
    # Validate origin (CSWSH prevention)
    origin = websocket.headers.get("Origin", "")
    if not validate_origin(origin, config.webapp.cors_origins):
        return  # Connection rejected
    
    # WebSocket event loop
    try:
        while True:
            data = await websocket.receive()
            message = json.loads(data)
            
            # Process message...
            response = {"type": "echo", "content": message.get("content")}
            
            await websocket.send(json.dumps(response))
    except Exception as e:
        # Handle disconnect
        pass
```

### Security: Origin Validation

```python
from urllib.parse import urlparse

def validate_origin(origin: str, allowed_origins: list[str]) -> bool:
    """Validate WebSocket origin to prevent CSWSH.
    
    WebSocket connections do not enforce CORS.
    The server must validate the Origin header.
    
    Args:
        origin: Origin header from WebSocket handshake.
        allowed_origins: List of allowed origins.
    
    Returns:
        True if origin is allowed, False otherwise.
    """
    if not origin:
        return False
    
    # Parse origin
    try:
        parsed = urlparse(origin)
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # Normalize: scheme://host:port
        port = f":{parsed.port}" if parsed.port else ""
        normalized = f"{parsed.scheme}://{parsed.hostname}{port}"
    except Exception:
        return False
    
    # Check against allowed origins
    for allowed in allowed_origins:
        allowed_parsed = urlparse(allowed)
        allowed_port = f":{allowed_parsed.port}" if allowed_parsed.port else ""
        allowed_normalized = f"{allowed_parsed.scheme}://{allowed_parsed.hostname}{allowed_port}"
        
        if normalized == allowed_normalized:
            return True
    
    return False
```

**Pattern:**
- Always validate origin for WebSocket endpoints
- Normalize URLs for comparison
- Reject 'null' origin (file://, data://)
- Exact match required (no subdomain matching)

## Test UI Pattern

### routes/index.py

```python
from quart import Blueprint
from quart_cors import cors_exempt

index_bp = Blueprint("index", __name__)

@index_bp.route("/", methods=["GET"])
@cors_exempt  # Public page
async def index() -> str:
    """Index page with WebSocket test UI.
    
    Returns:
        HTML page with test interface.
    """
    return """<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
    <style>
        /* Simple styling */
        body { font-family: sans-serif; max-width: 800px; margin: 50px auto; }
        .status { padding: 10px; border-radius: 4px; margin: 10px 0; }
        .disconnected { background: #fee; color: #c00; }
        .connected { background: #efe; color: #0a0; }
        input { width: 100%; padding: 10px; margin: 10px 0; }
        button { padding: 10px 20px; margin: 5px; }
        #output { background: #f8f8f8; padding: 15px; height: 400px; overflow-y: auto; }
    </style>
</head>
<body>
    <h1>WebSocket Test</h1>
    <div id="status" class="status disconnected">Disconnected</div>
    <button onclick="connect()">Connect</button>
    <button onclick="disconnect()">Disconnect</button>
    <input type="text" id="message" placeholder='{"type": "message", "content": "Hello!"}'>
    <button onclick="sendMessage()">Send</button>
    <div id="output"></div>
    
    <script>
        // WebSocket test implementation
        // See full example in the project
    </script>
</body>
</html>"""
```

**Pattern:**
- Create a simple HTML test page for every WebSocket endpoint
- Include connection status indicator
- Provide message input and output display
- Add send/receive buttons
- Make it easy to test end-to-end

## CORS Configuration

### middleware/cors.py

```python
from quart import Quart
from quart_cors import cors
from typing import Sequence
from urllib.parse import urlparse

def configure_cors(app: Quart, cors_origins: Sequence[str]) -> None:
    """Configure CORS for the Quart application.
    
    Args:
        app: Quart application instance.
        cors_origins: List of allowed CORS origins.
    
    Security Notes:
        - Wildcard (*) origins are NOT allowed
        - Origins are validated to prevent misconfiguration
    """
    # Validate CORS configuration
    if "*" in cors_origins:
        raise ValueError(
            "Wildcard (*) CORS origin is not allowed for security. "
            "Explicitly list allowed origins."
        )
    
    # Validate each origin
    for origin in cors_origins:
        parsed = urlparse(origin)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid CORS origin: {origin}")
    
    # Apply CORS middleware
    app = cors(app, allow_origin=list(cors_origins))
```

## Port Selection

**Standard ports:**
- Development: 8000 (avoid 5000 on macOS - AirPlay conflict)
- Production: 80 (HTTP) or 443 (HTTPS)

**Configuration:**

```python
@dataclass(frozen=True)
class WebappConfig:
    host: str = "localhost"
    port: int = 8000  # Avoid 5000 on macOS (AirPlay)
    debug: bool = False
    cors_origins: tuple[str, ...] = ("http://localhost:3000", "http://localhost:8000")
```

## Common Mistakes to Avoid

### 1. Don't use `make_response()` in Quart routes

```python
# WRONG - Returns coroutine
async def health_check():
    from quart import make_response
    response = make_response(html)  # This is a coroutine!
    return response

# CORRECT - Return string directly
async def health_check():
    return "<html>...</html>"  # Quart handles Response creation
```

### 2. Don't use port 5000 on macOS

```python
# WRONG - AirPlay uses port 5000
port: int = 5000  # Will conflict on macOS

# CORRECT - Use port 8000
port: int = 8000  # No conflict
```

### 3. Always use `@cors_exempt` for public endpoints

```python
# WRONG - Health check blocked by CORS
@health_bp.route("/health")
async def health_check():
    return jsonify({"status": "healthy"})

# CORRECT - Public endpoint exempted
@health_bp.route("/health")
@cors_exempt
async def health_check():
    return jsonify({"status": "healthy"})
```

### 4. Always use `json.dumps()` for WebSocket messages

```python
# WRONG - JSON injection vulnerability
await websocket.send(f'{{"type": "error", "message": "{error}"}}')

# CORRECT - Proper JSON serialization
import json
await websocket.send(json.dumps({"type": "error", "message": str(error)}))
```

### 5. Don't forget to export app for uvicorn

```python
# WRONG - Only create_app exported
from <project>.webapp import create_app
# Can't run: uv run uvicorn <project>.webapp:app

# CORRECT - Both create_app and app exported
from <project>.webapp import create_app, app
# Can run: uv run uvicorn <project>.webapp:app
```

## Testing

### Test WebSocket with Python

```python
import asyncio
import json
import websockets

async def test_websocket():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as ws:
        # Send message
        await ws.send(json.dumps({"type": "message", "content": "Hello!"}))
        
        # Receive response
        response = await ws.recv()
        print(f"Received: {response}")

asyncio.run(test_websocket())
```

### Test Health Endpoint

```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "version": "0.1.0"}
```

## Entry Points

### Recommended: Uvicorn (ASGI)

```bash
uv run uvicorn <project>.webapp:app --reload
```

### Module Entry Point

```bash
uv run python -m <project>.webapp
```

## Security Checklist

- [ ] Origin validation for WebSocket endpoints (CSWSH prevention)
- [ ] CORS configuration with explicit origins (no wildcard)
- [ ] Session limits enforced (DoS protection)
- [ ] Message validation (injection prevention)
- [ ] JSON serialization with `json.dumps()` (no f-strings)
- [ ] Public endpoints use `@cors_exempt`
- [ ] Authentication hooks ready for production auth

## Related Patterns

- `patterns/websocket-events.md` - Event-driven WebSocket patterns
- `patterns/session-management.md` - Session lifecycle management
- `patterns/cors-security.md` - CORS security best practices
