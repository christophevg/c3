# Auth Module Template

## auth.py

```python
"""Authentication handlers for the {{api_name}} API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


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
  """Bearer token authentication (OAuth)."""

  def __init__(self, token: str):
    self.token = token

  def apply(self) -> dict[str, str]:
    return {"Authorization": f"Bearer {self.token}"}


class BasicAuth(AuthHandler):
  """Basic authentication."""

  def __init__(self, username: str, password: str):
    import base64

    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    self.credentials = credentials

  def apply(self) -> dict[str, str]:
    return {"Authorization": f"Basic {self.credentials}"}


class ApiKeyAuth(AuthHandler):
  """API key authentication."""

  def __init__(self, api_key: str, header_name: str = "X-API-Key"):
    self.api_key = api_key
    self.header_name = header_name

  def apply(self) -> dict[str, str]:
    return {self.header_name: self.api_key}
```

## Template Variables

| Variable | Source |
|----------|--------|
| `{{api_name}}` | OpenAPI `info.title` |

## Important Notes

1. **CookieAuth** must accept both `cookie_value` and `cookie_name` parameters
2. Default cookie name is `"session"` but users may specify others (e.g., `remember_token`)
3. The cookie is sent as `Cookie: {name}={value}` header

## Common Cookie Names

| Name | Use Case |
|------|----------|
| `session` | Flask-Login default session cookie |
| `remember_token` | Flask-Login "remember me" token |
| `connect.sid` | Express/Connect session cookie |