# Models Module Template

## Overview

**ALWAYS use dataclass** for models. TypedDict is NOT suitable because:
1. No runtime validation
2. No serialization methods
3. No IDE autocomplete for methods
4. Cannot distinguish request vs response models

## Key Principles

1. **Required fields from OpenAPI `required` array** - Fields listed in the `required` array of a schema must NOT be `Optional` in the dataclass
2. **Use modern type hints** - Use `list[str]` not `List[str]` (Python 3.9+), use `X | None` not `Optional[X]` (Python 3.10+)
3. **Defensive parsing** - Add `isinstance(data, dict)` checks in `from_dict` methods
4. **Export all models** - Every model class used anywhere must be in `__all__`
5. **No `__str__` needed** - The REPL uses `vars(obj)` for Rich display, dataclass default `__repr__` is sufficient

## models.py

```python
"""Data models for {{api_name}} API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ============================================
# Request Models (need to_dict method)
# ============================================

@dataclass
class {{model_name}}Request:
  """Request body for {{operation}}."""
  
  {{#each required_fields}}
  {{name}}: {{type}}  # Required per OpenAPI spec
  {{/each}}
  {{#each optional_fields}}
  {{name}}: {{type}} | None = None
  {{/each}}
  
  def to_dict(self) -> dict[str, Any]:
    """Serialize request for API call."""
    result: dict[str, Any] = {}
    {{#each required_fields}}
    result["{{name}}"] = self.{{name}}
    {{/each}}
    {{#each optional_fields}}
    if self.{{name}} is not None:
      result["{{name}}"] = self.{{name}}
    {{/each}}
    return result


# ============================================
# Response Models (need from_dict classmethod)
# ============================================

@dataclass
class {{model_name}}:
  """{{model_description}}."""
  
  # Required fields (from OpenAPI 'required' array)
  {{#each required_fields}}
  {{name}}: {{type}}
  {{/each}}
  # Optional fields
  {{#each optional_fields}}
  {{name}}: {{type}} | None = None
  {{/each}}
  
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "{{model_name}}":
    """Parse model from API response.
    
    Args:
      data: Raw dict from API response
      
    Returns:
      Parsed model instance
      
    Raises:
      TypeError: If data is not a dict
    """
    if not isinstance(data, dict):
      raise TypeError(
        f"Expected dict for {{model_name}}, got {type(data).__name__}: {data!r}"
      )
    {{#if has_nested_models}}
    # Parse nested models
    {{#each nested_fields}}
    {{nested_name}}_data = data.get("{{api_name}}"{{#if default}}, {{default}}{{/if}})
    {{nested_name}} = {{model_type}}.from_dict({{nested_name}}_data) if {{nested_name}}_data else None
    {{/each}}
    {{/if}}
    return cls(
      {{#each fields}}
      {{name}}={{#if is_nested}}{{name}}_data{{else}}data.get("{{api_name}}"{{#if default}}, {{default}}{{/if}}){{/if}},
      {{/each}}
    )


# ============================================
# Shared Models (need both methods)
# ============================================

@dataclass
class {{model_name}}Shared:
  """{{model_description}} - used in both requests and responses."""
  
  {{#each required_fields}}
  {{name}}: {{type}}
  {{/each}}
  {{#each optional_fields}}
  {{name}}: {{type}} | None = None
  {{/each}}
  
  def to_dict(self) -> dict[str, Any]:
    """Serialize for API request."""
    result: dict[str, Any] = {}
    {{#each fields}}
    if self.{{name}} is not None:
      result["{{api_name}}"] = self.{{name}}
    {{/each}}
    return result
  
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "{{model_name}}Shared":
    """Parse from API response."""
    if not isinstance(data, dict):
      raise TypeError(
        f"Expected dict for {{model_name}}Shared, got {type(data).__name__}"
      )
    return cls(
      {{#each fields}}
      {{name}}=data.get("{{api_name}}"{{#if default}}, {{default}}{{/if}}),
      {{/each}}
    )


# ============================================
# Nested Model Handling
# ============================================

@dataclass
class Parent:
  """Model with nested child models."""
  
  id: str
  name: str
  child: Child | None = None  # Optional nested object
  children: list[Child] = field(default_factory=list)  # List of nested objects
  
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "Parent":
    if not isinstance(data, dict):
      raise TypeError(f"Expected dict for Parent, got {type(data).__name__}")
    
    # Parse optional nested single object
    child_data = data.get("child")
    child = Child.from_dict(child_data) if child_data else None
    
    # Parse nested list
    children_data = data.get("children", [])
    children = [Child.from_dict(c) for c in children_data]
    
    return cls(
      id=data.get("id", ""),
      name=data.get("name", ""),
      child=child,
      children=children,
    )


# ============================================
# Model with Required Nested Object
# ============================================

@dataclass
class FollowRelationship:
  """Follow relationship between users."""
  
  follower: str  # Required per OpenAPI 'required' array
  following: UserInfo  # Required - NOT optional!
  created_at: str  # Required
  
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "FollowRelationship":
    if not isinstance(data, dict):
      raise TypeError(f"Expected dict for FollowRelationship, got {type(data).__name__}")
    
    # Required nested object - always parse, never None
    following_data = data.get("following", {})
    return cls(
      follower=data.get("follower", ""),
      following=UserInfo.from_dict(following_data),
      created_at=data.get("created_at", ""),
    )


# ============================================
# Model Field Defaults Reference
# ============================================

"""
ALWAYS provide safe defaults for OPTIONAL fields only:

| Type | Default |
|------|---------|
| str | "" (only if optional) |
| int | 0 (only if optional) |
| float | 0.0 (only if optional) |
| bool | False (only if optional) |
| list | field(default_factory=list) |
| dict | field(default_factory=dict) |
| X \| None | None |

REQUIRED fields (from OpenAPI 'required' array):
- NO default value
- NO Optional wrapper
- NO | None union

NEVER use direct dict access - always use .get() with defaults.
"""
```

## Model Categories

### Request Models
- Need `to_dict()` method for serialization
- Used as parameters for POST/PUT/PATCH operations
- Mark required fields without Optional

### Response Models
- Need `from_dict()` classmethod for parsing
- Used as return types for client methods
- All fields should have safe defaults

### Shared Models
- Need both `to_dict()` and `from_dict()`
- Used in both requests and responses
- Example: User object returned by GET, used in PUT

## REPL Visualization

Models are displayed in the REPL using Rich:

1. **Single model**: `_display()` converts to dict via `vars(obj)` → `_display_dict()` → Rich Panel
2. **List of models**: `_display_list()` detects dataclass via `hasattr(obj, "__dict__")` → Rich Table

**Do NOT add `__str__` or `__repr__` methods** - the default dataclass `__repr__` is sufficient for debugging, and the REPL handles visualization via Rich.

## Template Variables

| Variable | Source |
|----------|--------|
| `{{model_name}}` | Schema name from OpenAPI |
| `{{model_description}}` | Schema description |
| `{{fields}}` | Properties from schema |
| `{{api_name}}` | Original field name in API (may differ from Python name) |
| `{{type}}` | Mapped Python type |
| `{{default}}` | Default value for optional fields |

## Type Mapping

| OpenAPI Type | Python Type |
|--------------|-------------|
| `string` | `str` |
| `integer` | `int` |
| `number` | `float` |
| `boolean` | `bool` |
| `array` | `List[ItemType]` |
| `object` | `dict[str, Any]` |
| `string: date-time` | `str` (ISO format) |
| `string: email` | `str` |
| `$ref` | Referenced model class |

## Common Patterns

### Enum Types
```python
from enum import Enum

class Status(str, Enum):
  ACTIVE = "active"
  COMPLETED = "completed"
  ABANDONED = "abandoned"
```

### Recursive Models
```python
@dataclass
class TreeItem:
  id: str
  name: str
  children: List["TreeItem"] = field(default_factory=list)
  
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "TreeItem":
    return cls(
      id=data.get("id", ""),
      name=data.get("name", ""),
      children=[cls.from_dict(c) for c in data.get("children", [])],
    )
```

### Mixed-Type Fields
```python
from typing import Any

@dataclass
class Config:
  # Field may contain different types - use Any
  properties: List[Any] = field(default_factory=list)
```

## Rich Console Support

Models displayed in the REPL should implement `__rich_console__` for beautiful rendering:

```python
import dataclasses
from rich.console import Console, ConsoleOptions, RenderResult
from rich.scope import render_scope

@dataclass
class User:
  email: Optional[str] = None
  name: Optional[str] = None
  picture: Optional[str] = None

  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "User":
    ...

  def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
    yield render_scope(dataclasses.asdict(self), title=self.__class__.__name__)
```

**Why**: Rich doesn't natively support dataclasses. The `__rich_console__` method enables:
- Beautiful nested rendering in table cells
- Consistent styling across all model types
- Automatic field visualization with proper formatting

**When to add**: Add `__rich_console__` to models that:
- Are displayed directly in the REPL (single objects)
- Appear in lists that render as tables
- Contain nested models that benefit from structured display

**Required imports** at top of models.py:
```python
import dataclasses
from rich.console import Console, ConsoleOptions, RenderResult
from rich.scope import render_scope
```