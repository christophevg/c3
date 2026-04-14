# Python Code Generation Patterns

## Package Structure

```
{package_name}/
├── pyproject.toml          # Modern package config
├── src/{package_name}/
│   ├── __init__.py         # Public API exports
│   ├── client.py           # Sync client
│   ├── async_client.py     # Async client
│   ├── models.py           # Request/response models
│   ├── auth.py             # Authentication
│   ├── exceptions.py       # Custom exceptions
│   ├── __main__.py         # Entry point
│   └── repl.py             # REPL shell
└── README.md
```

## Client Class Pattern

### Sync Client
```python
from typing import TypeVar
import requests
from .models import *
from .auth import AuthHandler

T = TypeVar("T")

class APIClient:
    """Client for {api_name} API."""
    
    def __init__(
        self,
        base_url: str = "{default_base_url}",
        auth: AuthHandler | None = None,
        timeout: int = 30
    ):
        self.base_url = base_url.rstrip("/")
        self.auth = auth
        self.timeout = timeout
        self._session = requests.Session()
    
    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json: dict | None = None,
        **kwargs
    ) -> dict:
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {})
        if self.auth:
            headers.update(self.auth.apply())
        response = self._session.request(
            method, url, params=params, json=json,
            headers=headers, timeout=self.timeout, **kwargs
        )
        response.raise_for_status()
        return response.json()
```

### Async Client
```python
import aiohttp

class AsyncAPIClient:
    """Async client for {api_name} API."""
    
    def __init__(
        self,
        base_url: str = "{default_base_url}",
        auth: AuthHandler | None = None,
        timeout: int = 30
    ):
        self.base_url = base_url.rstrip("/")
        self.auth = auth
        self.timeout = timeout
    
    async def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json: dict | None = None,
        **kwargs
    ) -> dict:
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {})
        if self.auth:
            headers.update(self.auth.apply())
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, params=params, json=json,
                headers=headers, timeout=self.timeout, **kwargs
            ) as response:
                response.raise_for_status()
                return await response.json()
```

## Model Generation

### TypedDict (Preferred for minimal deps)
```python
from typing import TypedDict, Optional

class User(TypedDict):
    """User object."""
    id: int
    name: str
    email: str
    created_at: Optional[str]

class UserCreate(TypedDict):
    """User creation request."""
    name: str
    email: str
```

### dataclass (Alternative)
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """User object."""
    id: int
    name: str
    email: str
    created_at: Optional[str] = None

@dataclass
class UserCreate:
    """User creation request."""
    name: str
    email: str
```

## Method Generation

### From OpenAPI Operation
```python
def generate_method(operation: dict, path: str, method: str) -> str:
    operation_id = operation.get("operationId", f"{method}_{path}")
    summary = operation.get("summary", "")
    description = operation.get("description", "")
    
    # Extract parameters
    params = extract_parameters(operation)
    param_docs = "\n".join(
        f"        {p.name}: {p.description}"
        for p in params
    )
    
    # Extract response type
    response_schema = extract_response_schema(operation)
    return_type = schema_to_type(response_schema) if response_schema else "dict"
    
    return f'''
    def {operation_id}(self{format_params(params)}) -> {return_type}:
        """{summary}
        
        Args:
{param_docs}
        
        Returns:
            {return_type}
        """
        return self._request("{method.upper()}", "{path}"{format_args(params)})
    '''
```

## Authentication Handlers

### API Key
```python
class APIKeyAuth:
    """API Key authentication."""
    
    def __init__(self, key: str, header_name: str = "X-API-Key"):
        self.key = key
        self.header_name = header_name
    
    def apply(self) -> dict[str, str]:
        return {self.header_name: self.key}
```

### Bearer Token
```python
class BearerAuth:
    """Bearer token authentication."""
    
    def __init__(self, token: str):
        self.token = token
    
    def apply(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}
```

### Basic Auth
```python
class BasicAuth:
    """Basic authentication."""
    
    def __init__(self, username: str, password: str):
        import base64
        credentials = base64.b64encode(
            f"{username}:{password}".encode()
        ).decode()
        self.credentials = credentials
    
    def apply(self) -> dict[str, str]:
        return {"Authorization": f"Basic {self.credentials}"}
```

## pyproject.toml Template

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{package_name}"
version = "0.1.0"
description = "{api_description}"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.28.0",
    "aiohttp>=3.8.0",
    "prompt_toolkit>=3.0.0",
    "rich>=13.0.0",
]

[project.scripts]
{package_name} = "{package_name}.__main__:main"

[tool.hatch.build.targets.wheel]
packages = ["src/{package_name}"]
```

## Best Practices

1. **Type hints everywhere** - Enable mypy strict mode
2. **Docstrings from descriptions** - Preserve API documentation
3. **Separate sync/async** - Different files, same interface
4. **Configurable base URL** - Support different environments
5. **Connection pooling** - Use Session for sync client
6. **Proper error handling** - Custom exceptions with context