---
name: spec2mod
description: Generate Python module from OpenAPI/Swagger/Postman spec. Use when user has an API spec file and wants a Python client library, CLI, and REPL.
---

# spec2mod

Generate a complete Python package from an OpenAPI/Swagger/Postman specification.

## Overview

| Capability | Description |
|------------|-------------|
| Spec Parsing | OpenAPI 3.0/3.1, Swagger 2.0, Postman, Insomnia |
| Client Generation | Sync + async clients with typed methods |
| Model Generation | TypedDict/dataclass models from schemas |
| REPL Generation | Interactive shell with rich formatting |
| CLI Generation | Command-line interface with flags |

## When to Use This Skill

Use this skill when:
- User has an OpenAPI/Swagger/Postman spec file
- User wants to generate a Python client from an API spec
- User mentions "spec2mod" or "generate from spec"
- doc2spec or api2mod needs to generate a module from a spec

**Do NOT use for unstructured documentation** — use doc2spec first.

## Input

| Type | Example |
|------|---------|
| Local file path | `/path/to/openapi.yaml` |
| URL to spec | `https://api.example.com/openapi.json` |
| Postman collection | `collection.json` |
| Insomnia export | `insomnia.yaml` |

## Workflow

```
OpenAPI Spec → Parse → Generate Package → Test → Done
```

### Step 0: Check for Existing Implementation

**Before generating**, check if an implementation already exists:

1. Look for existing package in output directory
2. If exists, compare features with `templates/test-features.md` checklist
3. Preserve any custom features not in templates
4. Note any features to carry forward

### Step 1: Load and Validate Spec

Read the spec file or fetch from URL:

```python
import yaml
import json

def load_spec(source: str) -> dict:
  """Load API spec from file path or URL."""
  if source.startswith("http"):
    import requests
    response = requests.get(source)
    content = response.text
  else:
    content = Path(source).read_text()

  # Parse YAML or JSON
  if content.strip().startswith("{"):
    return json.loads(content)
  return yaml.safe_load(content)
```

### Step 2: Detect Format

| Format | Detection |
|--------|-----------|
| OpenAPI 3.x | `"openapi"` key with version "3.x" |
| OpenAPI 3.1 | `"openapi": "3.1.x"` |
| OpenAPI 3.0 | `"openapi": "3.0.x"` |
| Swagger 2.0 | `"swagger": "2.0"` |
| Postman | `"info"` with `"_postman_id"` |
| Insomnia | `"_type": "export"` |

### Step 3: Extract API Information

From the spec, extract:

```yaml
# OpenAPI structure
info:
  title: API Name          # → package name, client class name
  version: "1.0.0"         # → package version
  description: "..."       # → README, docstrings

servers:
  - url: https://api.example.com/v1  # → default base URL

paths:
  /users:
    get:
      operationId: listUsers    # → method name
      summary: List all users   # → docstring
      parameters: [...]         # → method arguments
      responses:
        200:
          content:
            application/json:
              schema:           # → return type, models

components:
  schemas:                       # → model classes
    User:
      type: object
      properties:
        id: {type: integer}
        name: {type: string}

securitySchemes:                  # → auth handlers
  bearerAuth:
    type: http
    scheme: bearer
```

### Step 4: Generate Package Structure

Create the package:

```
{package_name}/
├── pyproject.toml          # Package config with entry point
├── src/{package_name}/
│   ├── __init__.py         # Public API exports
│   ├── client.py           # Sync client class
│   ├── async_client.py     # Async client class
│   ├── models.py           # TypedDict/dataclass models
│   ├── auth.py             # Authentication handlers
│   ├── auth_cache.py       # Token persistence
│   ├── __main__.py         # Entry point (CLI + REPL)
│   └── repl.py             # REPL with persistent history
├── research/               # Copy of spec + sources
│   ├── openapi.yaml        # Original spec
│   └── SOURCES.md          # Source reference
└── README.md               # Usage documentation
```

### Step 4.5: Generate Comprehensive SOURCES.md

The `research/SOURCES.md` file must contain **complete endpoint documentation** extracted from the OpenAPI spec:

**Required sections:**

```markdown
# Sources

## OpenAPI Specification

- **File**: `openapi.yaml`
- **Source**: <original source path or URL>
- **Version**: <from info.version>
- **Title**: <from info.title>

## API Endpoints

The OpenAPI specification defines the following endpoint groups:

### <Tag Name> (<Description from tags>)
- `<METHOD> <path>` - <summary>
  - <description details>
  - Parameters: <list parameters>
  - Returns: <response schema>

### <Next Tag>
...

## Authentication

<Detail all security schemes from securitySchemes>

1. **<Scheme Name>** (<type>)
   - Type: <type>
   - In: <location>
   - Name: <parameter name>
   - Description: <from spec>

## Generated Package

This package was generated from the OpenAPI specification using the `spec2mod` skill.
```

**CRITICAL**: Do NOT summarize - include ALL endpoints with their details. This documentation is used to verify the generated client matches the spec.

### Step 5: Generate Client Code

For each endpoint in `paths`:

1. **Method name**: Use `operationId` or derive from path+method
2. **Arguments**: Map parameters (path, query, header, body)
3. **Return type**: Map response schema to model class
4. **Docstring**: Use `summary` and `description`

**CRITICAL PATTERNS:**

1. **Return typed models, not raw dicts:**
   ```python
   def get_user(self, user_id: str) -> User:
     data = self._request("GET", f"/users/{user_id}")
     return User.from_dict(data)  # NOT: return data
   ```

2. **Use request objects for complex operations:**
   ```python
   def create_session(self, request: SessionCreateRequest) -> SessionCreateResponse:
     data = self._request("POST", "/sessions", json_data=request.to_dict())
     return SessionCreateResponse.from_dict(data)
   ```

3. **Handle operation-level security overrides:**
   ```python
   def create_auth_session(self, token: str) -> User:
     # This endpoint uses Bearer auth, NOT client.auth
     data = self._request(
       "POST", "/session",
       headers={"Authorization": f"Bearer {token}"}
     )
     return User.from_dict(data)
   ```

4. **Preserve relative base URLs from spec:**
   - If spec shows `url: /api`, use `/api` as default
   - Don't assume localhost

See `templates/client-module.md` for generated code patterns.

### Step 6: Generate Models

**ALWAYS use dataclass** for models. TypedDict is NOT suitable because:
- No runtime validation via `from_dict()` parsing
- No serialization via `to_dict()` for requests
- No IDE autocomplete for methods

**CRITICAL: Respect OpenAPI `required` array:**

```yaml
FollowRelationship:
  type: object
  required:           # ← These fields are REQUIRED
    - follower
    - following
    - created_at
  properties:
    following:
      $ref: '#/components/schemas/UserInfo'  # Required nested object!
```

Generated code must have:
```python
@dataclass
class FollowRelationship:
  follower: str              # Required - no default
  following: UserInfo         # Required - no | None, no default!
  created_at: str             # Required - no default
```

**Use modern type hints (Python 3.10+):**
- `list[str]` not `List[str]`
- `X | None` not `Optional[X]`
- Remove unused `Optional` imports

**Model Categories:**

| Category | Needs `to_dict()` | Needs `from_dict()` |
|----------|-------------------|---------------------|
| Request only | Yes | No |
| Response only | No | Yes |
| Shared | Yes | Yes |

For each schema in `components/schemas`:

1. **dataclass** for all object types
2. **Enum** for enumeration types
3. **TypeAlias** for simple type references
4. **Check `required` array** - fields in `required` must NOT be Optional

See `templates/models-module.md` for patterns.

### Step 7: Generate Authentication

From `securitySchemes`:

| Type | Generated Handler |
|------|-------------------|
| `http: bearer` | BearerAuth class |
| `http: basic` | BasicAuth class |
| `apiKey: header` | ApiKeyAuth class |
| `oauth2` | OAuth2Handler class |

### Step 8: Generate REPL

Create interactive shell:
- Each client method becomes a command
- **Add user-friendly aliases** (e.g., `whoami` → `get_session`)
- Argument hints as ghost text (auto_suggest)
- Rich formatting with tables and panels
- Persistent history across sessions
- `trace`, `verbose`, `debug` commands

**Command Aliases:**

| Alias | Method | Why |
|-------|--------|-----|
| `whoami` | `get_session` | Common CLI convention |
| `search` | `search_users` | Shorter |
| `topic` | `get_topic` | Simpler |
| `login <token>` | `create_auth_session` | Accepts parameter |

For methods that accept auth tokens (like `login`), the REPL command should accept the token as an argument.

See `templates/repl-module.md` for patterns.

### Step 9: Generate Entry Point

`__main__.py` with:

```python
def main() -> None:
  parser = argparse.ArgumentParser(...)
  parser.add_argument("--resume", help="Resume from cached auth")
  parser.add_argument("--trace", help="Show endpoint URLs")
  parser.add_argument("--verbose", help="Show request details")
  # ...
```

See `templates/entry-point-module.md` for patterns.

### Step 10: Test Generated Package

```bash
cd {package_name}
python -m venv .venv && source .venv/bin/activate
pip install -e .
{package_name} --help
{package_name}  # Launch REPL
```

**IMPORTANT**: Verify all features from `templates/test-features.md` are present:

```bash
# Test welcome banner and cookie command
echo -e "cookie test_value remember_token\ndebug" | python -m {package_name} --base-url http://localhost:8000/api
```

Expected output must include:
- Welcome banner with API name and version
- `✓ Session cookie 'remember_token' set`
- Debug info showing `Auth: cookie (remember_token)`

### Step 11: Validate Generated Package

**CRITICAL**: Run these validation checks before considering the package complete:

#### Check 1: Export Completeness

Verify all models are exported in `__init__.py`:

```bash
# Check that all model classes used are exported
python -c "
from {package_name} import *
# Also verify specific models exist
from {package_name} import Question  # Nested models must be exported
"
```

#### Check 2: No Undefined Exports

Verify `__init__.py` doesn't export non-existent symbols:

```bash
# This should fail if ValidationError is exported but not defined
python -c "from {package_name} import ValidationError"
```

#### Check 3: Required Fields Are Not Optional

Verify models match OpenAPI `required` array:

```python
# If OpenAPI says 'following' is required, this should work:
from {package_name} import FollowRelationship, UserInfo

rel = FollowRelationship(
  follower="user@example.com",
  following=UserInfo(email="other@example.com", name="Other"),
  created_at="2024-01-01"
)
# NOT: following=None  # Should fail if required!
```

#### Check 4: Import Validation

```bash
# Run mypy to catch type errors
pip install mypy
mypy src/{package_name}
```

#### Check 5: Run Tests

```bash
pip install -e ".[dev]"
pytest
```

## Output Package Features

### Sync and Async Clients

```python
# Sync usage
from {package_name} import Client
client = Client()
users = client.list_users()

# Async usage
from {package_name} import AsyncClient
client = AsyncClient()
users = await client.list_users()
```

### REPL with Rich Formatting

```python
{package_name}> user 123
┌─────────────────────────────────────┐
│ User Details                        │
├─────────────────────────────────────┤
│ ID:    123                          │
│ Name:  John Doe                     │
│ Email: john@example.com             │
└─────────────────────────────────────┘
```

### CLI Mode

```bash
{package_name} list_users --limit 10
{package_name} get_user 123
```

## Template Files

| Template | Purpose |
|----------|---------|
| `pyproject.toml.md` | Package configuration |
| `client-module.md` | Sync/async client classes |
| `models-module.md` | Data models from schemas |
| `auth-module.md` | Authentication handlers |
| `auth-cache-module.md` | Token persistence |
| `repl-module.md` | Interactive REPL |
| `entry-point-module.md` | CLI entry point |

## Pattern Files

| Pattern | Purpose |
|---------|---------|
| `openapi-parsing.md` | Spec parsing patterns |
| `code-generation.md` | Code generation patterns |
| `repl-design.md` | REPL design patterns |

## Common Issues

| Issue | Solution |
|-------|----------|
| Missing operationId | Derive from path: `GET /users/{id}` → `get_user` |
| Circular schema refs | Use `from __future__ import annotations` |
| Mixed-type responses | Use `list[Any]` with defensive parsing |
| Auth not standard | Generate custom handler, document in code |
| Cookies not persisting | Fix httpx `.local` domain normalization |

## Related Skills

- **doc2spec** - Converts unstructured docs to OpenAPI spec
- **api2mod** - Orchestrates full docs → module workflow