# Client Module Template

## client.py (Sync)

```python
"""Sync client for {{api_name}} API."""

from typing import Any
import requests

from .models import *
from .auth import AuthHandler
from .exceptions import APIError


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
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{self.base_url}{path}"
        req_headers = headers or {}
        
        if self.auth:
            req_headers.update(self.auth.apply())
        
        response = self._session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            headers=req_headers,
            timeout=self.timeout,
        )
        
        if not response.ok:
            raise APIError(
                status_code=response.status_code,
                message=response.text,
                url=url
            )
        
        return response.json()
    
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
        return self._request(
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
            json={{body_param}},
            {{/if}}
        )
    {{/each}}
```

## async_client.py (Async)

```python
"""Async client for {{api_name}} API."""

from typing import Any
import aiohttp

from .models import *
from .auth import AuthHandler
from .exceptions import APIError


class Async{{client_class_name}}:
    """Async client for {{api_name}} API.
    
    Args:
        base_url: API base URL (default: {{default_base_url}})
        auth: Authentication handler
        timeout: Request timeout in seconds
    """
    
    def __init__(
        self,
        base_url: str = "{{default_base_url}}",
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
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make async HTTP request to API."""
        url = f"{self.base_url}{path}"
        req_headers = headers or {}
        
        if self.auth:
            req_headers.update(self.auth.apply())
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=req_headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if not response.ok:
                    text = await response.text()
                    raise APIError(
                        status_code=response.status,
                        message=text,
                        url=url
                    )
                return await response.json()
    
    {{#each endpoints}}
    async def {{method_name}}(self{{#each params}}, {{name}}: {{type}}{{/each}}) -> {{return_type}}:
        """{{summary}}"""
        return await self._request(
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
            json={{body_param}},
            {{/if}}
        )
    {{/each}}
```

## Template Variables

| Variable | Source |
|----------|--------|
| `{{api_name}}` | OpenAPI `info.title` |
| `{{client_class_name}}` | Derived from package name (e.g., `PetStoreClient`) |
| `{{default_base_url}}` | OpenAPI `servers[0].url` |
| `{{endpoints}}` | Generated from `paths` |
| `{{method_name}}` | `operationId` or derived from path+method |
| `{{http_method}}` | GET, POST, PUT, DELETE, etc. |
| `{{path}}` | API path with `{param}` placeholders |