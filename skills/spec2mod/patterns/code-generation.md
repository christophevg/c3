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

## Model Design Decision

**ALWAYS use dataclass for models.** TypedDict is NOT suitable because:

1. **No runtime validation** - Errors only at type-check time
2. **No serialization** - Cannot implement `to_dict()` for requests
3. **No parsing** - Cannot implement `from_dict()` for responses
4. **No IDE method autocomplete** - Only property hints

### Model Categories

| Category | Needs `to_dict()` | Needs `from_dict()` | Example |
|----------|-------------------|---------------------|---------|
| Request only | Yes | No | `SessionCreateRequest` |
| Response only | No | Yes | `Session`, `User` |
| Shared | Yes | Yes | `UserInfo` |

### Dataclass Model Pattern

```python
from dataclasses import dataclass, field
from typing import Any, Optional, List

@dataclass
class User:
  """User response model."""
  
  id: str
  name: str
  email: str
  created_at: Optional[str] = None
  
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "User":
    """Parse from API response with safe defaults."""
    if not isinstance(data, dict):
      raise TypeError(f"Expected dict for User, got {type(data).__name__}")
    return cls(
      id=data.get("id", ""),
      name=data.get("name", ""),
      email=data.get("email", ""),
      created_at=data.get("created_at"),
    )


@dataclass
class CreateUserRequest:
  """User creation request model."""
  
  name: str
  email: str
  
  def to_dict(self) -> dict[str, Any]:
    """Serialize for API request."""
    return {
      "name": self.name,
      "email": self.email,
    }
```

## Client Class Pattern

### Sync Client

```python
from typing import TypeVar, Optional
import requests
from .models import User, CreateUserRequest
from .auth import AuthHandler

T = TypeVar("T")


class Client:
  """Client for {api_name} API."""
  
  def __init__(
    self,
    base_url: str = "{default_base_url}",
    auth: AuthHandler | None = None,
    timeout: int = 30,
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
    json_data: dict | None = None,
    headers: dict | None = None,
  ) -> Any:
    url = f"{self.base_url}{path}"
    req_headers = headers or {}
    if self.auth:
      req_headers.update(self.auth.apply())
    response = self._session.request(
      method, url, params=params, json=json_data,
      headers=req_headers, timeout=self.timeout,
    )
    response.raise_for_status()
    return response.json()
  
  # ============================================
  # Method Patterns
  # ============================================
  
  def get_user(self, user_id: str) -> User:
    """Get user by ID - returns typed model."""
    data = self._request("GET", f"/users/{user_id}")
    return User.from_dict(data)
  
  def create_user(self, request: CreateUserRequest) -> User:
    """Create user - uses request object."""
    data = self._request("POST", "/users", json_data=request.to_dict())
    return User.from_dict(data)
  
  def list_users(self) -> list[User]:
    """List users - returns typed list."""
    data = self._request("GET", "/users")
    return [User.from_dict(item) for item in data]
  
  def get_current_user(self) -> User | None:
    """Get current user - optional return."""
    data = self._request("GET", "/users/me")
    if data is None:
      return None
    return User.from_dict(data)
  
  def create_auth_session(self, token: str) -> User:
    """Create session - auth override at operation level."""
    data = self._request(
      "POST", "/session",
      headers={"Authorization": f"Bearer {token}"}
    )
    return User.from_dict(data)
```

### Async Client

```python
import aiohttp


class AsyncClient:
  """Async client for {api_name} API."""
  
  def __init__(
    self,
    base_url: str = "{default_base_url}",
    auth: AuthHandler | None = None,
    timeout: int = 30,
  ):
    self.base_url = base_url.rstrip("/")
    self.auth = auth
    self.timeout = timeout
  
  async def _request(
    self,
    method: str,
    path: str,
    params: dict | None = None,
    json_data: dict | None = None,
    headers: dict | None = None,
  ) -> Any:
    url = f"{self.base_url}{path}"
    req_headers = headers or {}
    if self.auth:
      req_headers.update(self.auth.apply())
    async with aiohttp.ClientSession() as session:
      async with session.request(
        method, url, params=params, json=json_data,
        headers=req_headers, timeout=self.timeout,
      ) as response:
        response.raise_for_status()
        return await response.json()
  
  async def get_user(self, user_id: str) -> User:
    """Get user by ID."""
    data = await self._request("GET", f"/users/{user_id}")
    return User.from_dict(data)
```

## Authentication Handlers

```python
from abc import ABC, abstractmethod


class AuthHandler(ABC):
  """Base class for authentication handlers."""
  
  @abstractmethod
  def apply(self) -> dict[str, str]:
    """Return headers to add to requests."""
    pass


class CookieAuth(AuthHandler):
  """Cookie authentication."""
  
  def __init__(self, cookie_value: str, cookie_name: str = "session"):
    self.cookie_value = cookie_value
    self.cookie_name = cookie_name
  
  def apply(self) -> dict[str, str]:
    return {"Cookie": f"{self.cookie_name}={self.cookie_value}"}


class BearerAuth(AuthHandler):
  """Bearer token authentication."""
  
  def __init__(self, token: str):
    self.token = token
  
  def apply(self) -> dict[str, str]:
    return {"Authorization": f"Bearer {self.token}"}
```

## Response Handling Patterns

### Pattern 1: Typed Model Return

```python
def get_topic(self, topic_id: str) -> Topic:
  """Get topic - always returns typed model."""
  data = self._request("GET", f"/topics/{topic_id}")
  return Topic.from_dict(data)
```

### Pattern 2: List of Models

```python
def list_topics(self) -> list[Topic]:
  """List topics - parse each item."""
  data = self._request("GET", "/topics")
  return [Topic.from_dict(item) for item in data]
```

### Pattern 3: Optional Return (may be null)

```python
def get_current_session(self) -> Session | None:
  """Get current session - may be None."""
  data = self._request("GET", "/sessions/current")
  if data is None:
    return None
  return Session.from_dict(data)
```

### Pattern 4: Request Object for Complex Body

```python
def create_session(self, request: SessionCreateRequest) -> SessionCreateResponse:
  """Create session - use request object."""
  data = self._request("POST", "/sessions", json_data=request.to_dict())
  return SessionCreateResponse.from_dict(data)
```

### Pattern 5: Auth Override at Operation Level

Some operations specify different security than the client default:

```python
def create_auth_session(self, token: str) -> User:
  """Create session via OAuth.
  
  This endpoint uses Bearer auth directly, not client.auth.
  The OpenAPI spec has security: [bearer: []] for this operation.
  """
  data = self._request(
    "POST", "/session",
    headers={"Authorization": f"Bearer {token}"}
  )
  return User.from_dict(data)
```

### Pattern 6: Complex Response with Multiple Models

```python
def update_topic(self, topic_id: str, update: TopicUpdate) -> dict[str, Any]:
  """Update topic - returns multiple related objects."""
  data = self._request(
    "PATCH", f"/topics/{topic_id}",
    json_data=update.to_dict(),
  )
  return {
    "topic": Topic.from_dict(data.get("topic", {})),
    "treeitems": [TreeItem.from_dict(t) for t in data.get("treeitems", [])],
  }
```

### Pattern 7: Mixed-Type List Handling

```python
def get_items(self) -> list[Item]:
  """Get items - handles both IDs and full objects."""
  data = self._request("GET", "/items")
  items = []
  for item in data:
    if isinstance(item, (int, str)):
      # API returned just the ID
      items.append(Item(id=str(item), name=""))
    elif isinstance(item, dict):
      # API returned full object
      items.append(Item.from_dict(item))
  return items
```

## Defensive Parsing Patterns

### Type Validation in from_dict

**CRITICAL**: Always validate input type before parsing:

```python
@classmethod
def from_dict(cls, data: dict[str, Any]) -> "Model":
  """Parse model with type validation."""
  if not isinstance(data, dict):
    raise TypeError(
      f"Expected dict for {cls.__name__}, got {type(data).__name__}: {data!r}"
    )
  return cls(
    id=data.get("id", ""),
    name=data.get("name", ""),
  )
```

### Safe List Parsing with Context

```python
def get_devices(self) -> list[Device]:
  """Get devices with error context."""
  data = self._request("GET", "/devices")
  devices = []
  for i, item in enumerate(data):
    try:
      if isinstance(item, (int, str)):
        devices.append(Device(id=str(item), name=""))
      elif isinstance(item, dict):
        devices.append(Device.from_dict(item))
    except Exception as e:
      raise type(e)(
        f"{e}\n  while parsing devices[{i}]\n  data: {item!r}"
      ) from None
  return devices
```

### Model Field Defaults

Always provide safe defaults for optional fields:

```python
@dataclass
class Resource:
  id: str = ""                    # Empty string default
  name: str = ""                  # Empty string default
  count: int = 0                  # Zero default
  enabled: bool = False           # False default
  tags: list[str] = field(default_factory=list)  # Empty list
  metadata: dict[str, Any] = field(default_factory=dict)  # Empty dict
  config: Optional[dict] = None   # None for truly optional
```

### Never Use Direct Dict Access

**WRONG** - Will crash on missing keys:
```python
return cls(id=data["id"], name=data["name"])  # Crashes!
```

**RIGHT** - Safe with defaults:
```python
return cls(id=data.get("id", ""), name=data.get("name", ""))
```

## Base URL Handling

**IMPORTANT**: Preserve the base URL exactly as specified in the OpenAPI spec:

```yaml
servers:
  - url: /api  # Relative URL - preserve as-is
```

```python
# CORRECT: Use the spec value exactly
base_url: str = "/api"

# WRONG: Don't assume localhost
base_url: str = "http://localhost:5000/api"
```

The user will provide the full URL when instantiating the client for their environment.

## pyproject.toml Template

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{package_name}"
version = "0.1.0"
description = "Python client for {api_name}"
readme = "README.md"
requires-python = ">=3.10"
authors = [
  { name = "{author_name}", email = "{author_email}" }
]
dependencies = [
  "requests>=2.28.0",
  "aiohttp>=3.8.0",
  "prompt_toolkit>=3.0.0",
  "rich>=13.0.0",
]

[project.scripts]
{package_name} = "{package_name}.__main__:main"
```

## Best Practices

1. **Type hints everywhere** - Enable mypy strict mode
2. **Always parse responses** - Return typed models, never raw dicts
3. **Use request objects** - For complex POST/PUT/PATCH operations
4. **Separate sync/async** - Different files, same interface
5. **Preserve spec URLs** - Don't assume localhost
6. **Connection pooling** - Use Session for sync client
7. **Proper error handling** - Custom exceptions with context
8. **Include author email** - Required for PyPI