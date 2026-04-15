# Client Module Template

## client.py (Sync)

```python
"""Sync client for {{api_name}} API."""

import json
import traceback
from typing import Any, Callable, TypeVar, Optional
from urllib.parse import urlencode
import requests

from .models import *
from .auth import AuthHandler
from .exceptions import APIError

T = TypeVar("T")


class {{client_class_name}}:
  """Client for {{api_name}} API.

  Args:
    base_url: API base URL (default: {{default_base_url}})
    auth: Authentication handler
    timeout: Request timeout in seconds

  Example:
    >>> client = {{client_class_name}}()
    >>> user = client.get_user(123)
    >>> print(user.name)
  """

  def __init__(
    self,
    base_url: str = "{{default_base_url}}",
    auth: AuthHandler | None = None,
    timeout: int = 30,
  ):
    self.base_url = base_url.rstrip("/")
    self.auth = auth
    self.timeout = timeout
    self._session = requests.Session()
    self._trace = False
    self._verbose = False

  def set_trace(self, trace: bool) -> None:
    """Enable or disable endpoint URL tracing."""
    self._trace = trace

  def set_verbose(self, verbose: bool) -> None:
    """Enable or disable verbose request logging."""
    self._verbose = verbose

  def _parse_list(
    self,
    data: list[Any],
    model_class: type[T],
    field_name: str = "items",
  ) -> list[T]:
    """Parse a list that may contain mixed types (primitives + objects).

    Args:
      data: Raw list from API
      model_class: Target model class with from_dict method
      field_name: Field name for error context

    Returns:
      List of parsed model instances
    """
    items = []
    for i, item in enumerate(data):
      try:
        if isinstance(item, (int, str)):
          # Primitive: create minimal instance with just ID
          items.append(model_class(id=str(item)))  # type: ignore
        elif isinstance(item, dict):
          # Object: parse fully
          items.append(model_class.from_dict(item))  # type: ignore
        elif item is None:
          # Skip nulls
          continue
        else:
          if self._verbose:
            print(f"[WARN] Unexpected type in {field_name}[{i}]: {type(item)}")
      except Exception as e:
        frame = traceback.extract_stack()[-2]
        raise type(e)(
          f"{e}\n"
          f"  at {frame.filename}:{frame.lineno} ({frame.name})\n"
          f"  while parsing {field_name}[{i}]: {json.dumps(item, indent=2)[:200]}"
        ) from None
    return items

  def _request(
    self,
    method: str,
    path: str,
    params: dict[str, Any] | None = None,
    json_data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
  ) -> Any:
    """Make HTTP request to API."""
    url = f"{self.base_url}{path}"
    req_headers = headers or {}

    if self.auth:
      req_headers.update(self.auth.apply())

    # Build full URL for tracing
    full_url = url
    if params:
      full_url = f"{url}?{urlencode(params)}"

    # Show endpoint URL when trace is enabled
    if self._trace:
      print(f"[TRACE] {method} {full_url}")

    if self._verbose:
      print(f"[DEBUG] Request: {method} {url}")
      print(f"[DEBUG] Headers: {req_headers}")
      if params:
        print(f"[DEBUG] Params: {params}")
      if json_data:
        print(f"[DEBUG] Body: {json_data}")

    response = self._session.request(
      method=method,
      url=url,
      params=params,
      json=json_data,
      headers=req_headers,
      timeout=self.timeout,
    )

    if self._verbose:
      print(f"[DEBUG] Response: {response.status_code}")
      try:
        body = response.json()
        body_str = json.dumps(body, indent=2)
        if len(body_str) > 1000:
          body_str = body_str[:1000] + "\n... (truncated)"
        print(f"[DEBUG] Body:\n{body_str}")
      except Exception:
        print(f"[DEBUG] Body (raw): {response.text[:500]}")

    if not response.ok:
      raise APIError(
        status_code=response.status_code,
        message=response.text,
        url=url,
      )

    # Parse response with error context
    try:
      return response.json()
    except Exception as e:
      if self._verbose:
        frame = traceback.extract_stack()[-3]
        print(f"[DEBUG] Error in {frame.filename}:{frame.lineno} ({frame.name})")
        print(f"[DEBUG] Raw response: {response.text[:500]}")
      raise type(e)(f"{e} (at {frame.filename}:{frame.lineno} in {frame.name})") if self._verbose else e

  # ============================================
  # Endpoint Methods
  # ============================================

  {{#each endpoints}}
  def {{method_name}}(self{{#each params}}, {{name}}: {{type}}{{/each}}) -> {{return_type}}:
    """{{summary}}

    {{description}}

    Args:
    {{#each params}}
      {{name}}: {{param_description}}
    {{/each}}

    Returns:
      {{return_type}}: {{return_description}}
    """
    {{#if has_request_object}}
    data = self._request(
      method="{{http_method}}",
      path="{{path}}",
      {{#if has_params}}
      params={
      {{#each query_params}}
        "{{name}}": {{name}},
      {{/each}}
      },
      {{/if}}
      json_data={{request_param}}.to_dict(),
    )
    {{else}}
    data = self._request(
      method="{{http_method}}",
      path="{{path}}",
      {{#if has_params}}
      params={
      {{#each query_params}}
        "{{name}}": {{name}},
      {{/each}}
      },
      {{/if}}
      {{#if has_body}}
      json_data={
      {{#each body_params}}
        "{{name}}": {{name}},
      {{/each}}
      },
      {{/if}}
      {{#if has_auth_override}}
      headers={"Authorization": f"Bearer {{{auth_param}}}"},
      {{/if}}
    )
    {{/if}}
    {{#if returns_model}}
    return {{return_model}}.from_dict(data)
    {{else if returns_list}}
    return [{{return_model}}.from_dict(item) for item in data]
    {{else if returns_optional}}
    if data is None:
      return None
    return {{return_model}}.from_dict(data)
    {{else}}
    return data
    {{/if}}
  {{/each}}
```

## Method Generation Patterns

### Pattern 1: Simple GET with Model Return

```python
def get_user(self, user_id: str) -> User:
  """Get a user by ID.

  Args:
    user_id: User identifier

  Returns:
    User: User details
  """
  data = self._request(
    method="GET",
    path=f"/users/{user_id}",
  )
  return User.from_dict(data)
```

### Pattern 2: POST with Request Object

```python
def create_session(self, request: SessionCreateRequest) -> SessionCreateResponse:
  """Create a new session.

  Args:
    request: Session creation parameters

  Returns:
    SessionCreateResponse: Created session details
  """
  data = self._request(
    method="POST",
    path="/sessions",
    json_data=request.to_dict(),
  )
  return SessionCreateResponse.from_dict(data)
```

### Pattern 3: GET with Query Parameters

```python
def search_users(self, email: str) -> list[UserInfo]:
  """Search for users by email prefix.

  Args:
    email: Email prefix (min 3 chars)

  Returns:
    list[UserInfo]: Matching users
  """
  data = self._request(
    method="GET",
    path="/users",
    params={"email": email},
  )
  return [UserInfo.from_dict(item) for item in data]
```

### Pattern 4: Optional Return (may be null)

```python
def get_current_session(self) -> Session | None:
  """Get current active session, if any.

  Returns:
    Session or None: Active session or None
  """
  data = self._request(
    method="GET",
    path="/sessions/current",
  )
  if data is None:
    return None
  return Session.from_dict(data)
```

### Pattern 5: Auth Override (operation-specific auth)

```python
def create_auth_session(self, token: str) -> User:
  """Create session via OAuth.

  This endpoint uses Bearer auth directly, not the client's default auth.

  Args:
    token: OAuth bearer token

  Returns:
    User: Authenticated user info
  """
  data = self._request(
    method="POST",
    path="/session",
    headers={"Authorization": f"Bearer {token}"},
  )
  return User.from_dict(data)
```

### Pattern 6: PATCH/PUT with Partial Update

```python
def update_topic(self, topic_id: str, update: TopicUpdate) -> dict[str, Any]:
  """Update a topic.

  Args:
    topic_id: Topic identifier
    update: Partial update request

  Returns:
    dict with 'topic' and 'treeitems'
  """
  data = self._request(
    method="PATCH",
    path=f"/topics/{topic_id}",
    json_data=update.to_dict(),
  )
  return {
    "topic": Topic.from_dict(data.get("topic", {})),
    "treeitems": [TreeItem.from_dict(t) for t in data.get("treeitems", [])],
  }
```

## async_client.py (Async)

Same patterns as sync client, but with `async def` and `await`:

```python
async def get_user(self, user_id: str) -> User:
  """Get a user by ID."""
  data = await self._request(
    method="GET",
    path=f"/users/{user_id}",
  )
  return User.from_dict(data)
```

## Template Variables

| Variable | Source |
|----------|--------|
| `{{api_name}}` | OpenAPI `info.title` |
| `{{client_class_name}}` | Derived from package name (e.g., `PetStoreClient`) |
| `{{default_base_url}}` | OpenAPI `servers[0].url` (preserve exactly - may be relative) |
| `{{endpoints}}` | Generated from `paths` |
| `{{method_name}}` | `operationId` or derived from path+method |
| `{{http_method}}` | GET, POST, PUT, DELETE, etc. |
| `{{path}}` | API path with `{param}` placeholders |
| `{{return_type}}` | Model class or `list[Model]` or `dict[str, Any]` |
| `{{return_model}}` | Model class name for parsing |
| `{{has_request_object}}` | True if operation uses request body model |
| `{{request_param}}` | Name of request parameter |
| `{{has_auth_override}}` | True if operation has different security than default |
| `{{auth_param}}` | Name of auth parameter (e.g., `token`) |

## Important Notes

1. **Always parse responses into typed models** - Never return raw dicts from client methods
2. **Use request objects for complex operations** - POST/PUT/PATCH with multiple fields
3. **Handle operation-level security overrides** - Check `security` field per operation
4. **Preserve relative URLs from spec** - Don't assume localhost
5. **Import models explicitly** - Use `from .models import Model1, Model2` not `*`