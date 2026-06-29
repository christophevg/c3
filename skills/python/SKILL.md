---
name: python-best-practices
description: Use this skill any time when editing Python code
---

# Python Best Practices

When creating Python code, ALWAYS use the best practices in the sections below.

## Core Philosophy: Tight Code

**Duplication is cheaper than the wrong abstraction.** Wait for three proven cases before extracting. A module should earn its existence; a layer should survive deletion-testing. When in doubt, inline.

**Deep modules, not many modules.** (Ousterhout) A module's interface should be simpler than its implementation. If the interface is nearly as complex as the body, the module isn't hiding anything — it's shallow. Prefer fewer, deeper modules over many shallow ones.

**Deletion is the default question.** For any abstraction, helper, or layer, ask: "What breaks if I delete this?" If nothing, delete it. Code that doesn't exist has zero maintenance cost.

## Library-First Check (NIH Principle)

**Before implementing any abstraction, check if a library already does it.** This prevents reinventing solutions that already exist.

### When to Check

| Before implementing | Check for |
|---------------------|----------|
| Provider abstraction for LLMs, APIs, databases | `litellm`, `langchain`, `instructor`, `haystack` |
| HTTP client wrappers | `httpx`, `aiohttp`, `requests` |
| Configuration management | `clevis`, `pydantic-settings`, `dynaconf` |
| CLI argument parsing | `clevis` (if already using), `click`, `argparse` |
| Logging/observability | `structlog`, `loguru`, `opentelemetry` |
| Data validation | `pydantic`, `marshmallow`, `msgspec` |
| Async patterns (caching, rate limiting) | `asyncio` stdlib, `aiocache`, `asyncio-throttle` |
| Data processing pipelines | `pandas`, `polars`, `dask` |
| Task queues | `celery`, `arq`, `dramatiq` |

### How to Check

1. **Search PyPI**: `pip search <keyword>` or `https://pypi.org/search/?q=<keyword>`
2. **Search GitHub**: `<keyword> python library`
3. **Check dependency lists**: If you already depend on a framework, use its built-in patterns

### Decision Matrix

| Library exists? | Maintenance quality | Decision |
|-----------------|-------------------|----------|
| No library | N/A | Implement yourself |
| Library exists, unmaintained | No releases in 2+ years | Implement yourself or contribute |
| Library exists, active | Recent releases, good docs | **Use the library** |
| Library exists, but wrong abstraction | Active but doesn't fit | Consider contributing upstream or implementing |

### Why This Matters

- **Every line of code you write is a line you maintain.** A library with 10K users has 10K people finding edge cases.
- **Edge cases multiply.** Provider abstraction sounds simple until you hit streaming, tool calls, thinking/reasoning, token counting, rate limits, retry logic, error mapping, and version drift.

## Indentation and Style

**2-space indentation** is the house style. This is non-standard for Python (PEP 8 specifies 4) but consistent across this project's JS/Vue/CSS.

**Ruff config to enforce:**

```toml
# pyproject.toml
[tool.ruff.format]
indent-style = "space"
indent-width = 2
```

**Other style:**
- Line length: 100 characters
- Imports: standard library, third-party, local — separated, alphabetized
- Fully qualified imports preferred over relative: `from myproject.mymodule import func`
- Type annotations on all public functions

## Imports

### All Imports on Top

Always put all imports at the top of the module. Don't use imports inside functions!

### Use Fully Qualified Module Names

Don't use relative module paths when possible. Use the fully qualified module name.

* 🛑 Don't use `from ..my_module.my_submodule import function_name`
* ✅ Use: `from my_project.my_module.my_submodule import function_name`

### Import Organization for Packages

When creating Python packages with multiple modules, organize imports correctly in `__init__.py`:

1. **Import from defining module**: Always import classes from the module where they are defined
2. **Re-export in `__init__.py`**: Make public classes available at package level

```python
# CORRECT: Import from defining module
# src/mypackage/__init__.py
from .auth import Token, OAuth2Auth
from .models import User, Config
from .client import Client

__all__ = ["Token", "OAuth2Auth", "User", "Config", "Client"]

# WRONG: Import from wrong module
from .models import Token  # Token is defined in auth.py, not models.py
```

## Function Parameters

Always expose configurable variables as function parameters. Add sensible defaults, using environment variables if available.

### Example

```python
def a_command(an_argument=None):
  if an_argument is None:
    an_argument = os.environ.get("ARGUMENT_ENV_VAR_NAME", "a sensible default")
  # perform logic using `an_argument`
```

## Use Classes to Group Functions with Common Configuration

If a module contains several functions that share common configuration parameters, create a class grouping those functions, adding properties for those common parameters.

## Abstraction Timing

**Rule of three:** Tolerate near-duplication until the same shape appears three times. Then extract — but keep the abstraction shallow until more use cases clarify the right interface.

**Don't:**
- Extract a base class for one implementation
- Create a "generic" factory for one concrete type
- Add a config parameter "just in case"
- Build a plugin system for one plugin

**Do:**
- Inline code until duplication is proven painful
- Wait for the third instance to reveal the right abstraction
- Keep extracted helpers small and focused

## Async-First Pattern

For I/O-bound operations (database, network, filesystem), default to async:

1. **Write `AsyncClient` as the primary implementation.** This is the source of truth.
2. **Sync wrapper via `asyncio.run`, not a background thread.**

```python
# sync.py
import asyncio

def _run(coro):
  return asyncio.run(coro)

class Client:
  """Thin sync facade over AsyncClient. No threads, no resident loop."""

  def __init__(self, *args, **kwargs):
    self._args, self._kwargs = args, kwargs

  def __enter__(self):
    self._async = AsyncClient(*self._args, **self._kwargs)
    _run(self._async.__aenter__())
    return self

  def __exit__(self, *exc):
    _run(self._async.__aexit__(*exc))

  def request(self, query):
    return _run(self._async.request(query))
```

**When to add the sync facade:** Only when a sync caller exists or is planned this quarter. No speculative dual APIs.

**What this removes:** No `threading`, no `new_event_loop`, no `run_coroutine_threadsafe`, no per-client thread management. `asyncio.run` creates and tears down a fresh loop per call — appropriate for the sync path, which by definition isn't latency-sensitive.

### Package Exports

```python
# __init__.py
from .async_client import AsyncClient  # Primary async implementation
from .client import Client             # Sync wrapper

__all__ = ["Client", "AsyncClient"]
```

## Configurability: Clevis Pattern

**Configuration lives at the edge, not threaded through every function.**

Use `clevis` to load a dataclass-based config from TOML + env + CLI. Functions receive a config object or specific extracted values — never param+env+default pyramids.

```python
# config.py
from dataclasses import dataclass
import clevis

@dataclass
class AppConfig:
  database_url: str
  pool_size: int = 10

def load_config():
  return clevis.load(AppConfig)  # TOML + env + CLI merge

# client.py
class AsyncClient:
  def __init__(self, config: AppConfig):  # receives config object
    self._config = config
```

**Rule:** Add a parameter only when a caller needs to vary it. Add an env var only when ops/deployment overrides it. Configurability is earned, not default.

## Comments and Docstrings

**Why-only.** Comments explain intent, not mechanics. Delete any comment that restates what the code says.

```python
# WRONG: restates the code
# Increment the counter
counter += 1

# RIGHT: explains why
# Retry on transient failures; the upstream service has brief outages.
for _ in range(3):
  try:
    return await client.fetch()
  except TransientError:
    await asyncio.sleep(0.5)
```

**Docstrings:** Required on public module-level functions and classes. Private helpers (prefixed `_`) need no docstring unless the logic is non-obvious.

Docstring format: one-line summary, then `Args:`, `Returns:`, `Raises:` if non-empty. No redundant "This function does..." preamble.

```python
def fetch_user(user_id: str) -> User:
  """Fetch a user by ID from the database.

  Args:
    user_id: The user's unique identifier.

  Returns:
    The User object.

  Raises:
    NotFoundError: If the user does not exist.
    DatabaseError: If the query fails.
  """
```

## Anti-Patterns to Avoid

| Anti-pattern | Why it's bloat | Instead |
|--------------|----------------|---------|
| **Reimplementing existing libraries** | NIH — maintenance burden, missing edge cases | Use `litellm`, `httpx`, `pydantic`, etc. |
| Sync + async parallel APIs for everything | Maintenance cost for callers that don't exist | Add sync facade only when needed |
| Parameter + env var + default for every variable | Config pyramid nobody varies | Hardcode sensible defaults; add config when proven |
| Base class for one subclass | Indirection with no payoff | Delete the base; keep the concrete class |
| `try/except` around code that can't throw | Hides real errors | Catch only what can actually fail |
| Comments restating code | Noise; rots when code changes | Delete the comment |
| Helper called once | Layer with no caller diversity | Inline it |
| Defensive type-checking inside typed code | Protects against nothing | Trust the type system |
| Config object for one value | Over-engineering | Pass the value directly |
| Abstract factory returning one concrete | Factory with no variation | Return the concrete directly |

## Testing Patterns

Tests use `pytest` with the following patterns:

- Use `monkeypatch` fixture for environment variable manipulation
- Use `unittest.mock.patch` and `MagicMock` for mocking dependencies
- Use `autouse=True` fixtures for test setup
- Group related tests in classes (e.g., `TestMongoDBConnection`, `TestMongoDBOperations`)
- Use descriptive test names that explain what is being tested
- Test both success and error paths

### Example Test Structure

```python
class TestMyFeature:
  """Tests for MyFeature."""

  @pytest.fixture(autouse=True)
  def setup_env(self, monkeypatch):
    """Set up environment for tests."""
    monkeypatch.setenv("MY_VAR", "value")
    # Create mocks
    self.mock_service = MagicMock()
    # Patch dependencies
    self.patcher = patch('myapp.mymodule.get_service', return_value=self.mock_service)
    self.patcher.start()
    yield
    self.patcher.stop()

  def test_success_case(self):
    """Test successful operation."""
    # Arrange
    self.mock_service.get_data.return_value = {"key": "value"}

    # Act
    result = my_function()

    # Assert
    assert result == expected
    self.mock_service.get_data.assert_called_once()

  def test_error_case(self):
    """Test error handling."""
    self.mock_service.get_data.side_effect = Exception("error")

    with pytest.raises(MyError):
      my_function()
```

## Security Best Practices

When working with databases or external services:

- **Never log credentials** - Connection URIs may contain passwords
- **Use specific exceptions** - Catch `bson.errors.InvalidId` instead of broad `Exception`
- **Keep operations in try blocks** - Ensure errors are properly caught
- **Thread-safe singletons** - Always use locks with double-checked locking for singleton patterns in multi-worker environments
- **Escape regex in search** - Use `re.escape()` before passing user input to MongoDB `$regex` to prevent ReDoS attacks
- **Configurable pool sizes** - Use environment variables for connection pool sizes instead of hardcoding

### Error Handling Security

Never expose internal error details to clients:

```python
# WRONG - exposes database details
except DatabaseError as e:
  return make_error_response('INTERNAL_ERROR', str(e), status_code=500)

# CORRECT - generic message
except DatabaseError as e:
  logger.error(f"Database error: {e}\n{traceback.format_exc()}")
  return make_error_response('INTERNAL_ERROR', 'An unexpected error occurred', status_code=500)
```

This applies to all exception types that could expose internal implementation details:
- DatabaseError
- NotFoundError
- Any third-party library exceptions

### Atomic File Creation for Sensitive Files

When creating files with sensitive content (session cache, credentials, tokens), use atomic creation with secure permissions:

```python
import os

# Atomic creation with secure permissions (0600)
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'w') as f:
  f.write(content)
```

**This ensures:**
- **No race condition** — `O_EXCL` fails if file already exists
- **Correct permissions from creation** — 0600 means only owner can read/write
- **Atomic operation** — File either exists completely or not at all

**When to use:**
- Session cache files
- Credential files
- Token storage
- Any file containing sensitive data

## Extending Third-Party Frameworks

When creating classes that extend third-party framework classes (e.g., Textual's App, FastAPI's APIRouter):

### Pre-Implementation Checklist

1. **Review parent class API** - Check documentation for existing properties/methods
2. **Check for naming conflicts** - Ensure new names don't shadow parent class members
3. **Use descriptive prefixes/suffixes** - E.g., `theme_name` instead of `theme` if parent has `theme`

### Common Pitfalls

```python
# WRONG - shadows parent property
class App(TextualApp):
    @property
    def theme(self) -> str:  # Conflicts with TextualApp.theme
        return self._theme

# CORRECT - uses distinct name
class App(TextualApp):
    @property
    def theme_name(self) -> str:  # No conflict
        return self._theme_name
```

### Framework-Specific Considerations

| Framework | Common Conflicts | Solution |
|-----------|-----------------|----------|
| Textual | `theme`, `title`, `styles` | Use `theme_name`, `app_title`, `custom_styles` |
| FastAPI | `get`, `post`, `router` | Names are usually fine (decorator methods) |
| Pydantic | `model_`, `schema_` | Avoid underscore prefixes in field names |

## Pre-Commit Workflow

Before committing Python code, run these checks:

```bash
# 1. Run tests
make test

# 2. Run linting
make lint

# 3. Format code (if not in make lint)
ruff format src tests

# 4. Run type checking
make typecheck
```

**Combined command:**
```bash
make test && make lint && ruff format src tests && make typecheck
```

**Why multiple gates:** The commit skill will also run formatting checks as a final gate. Running both ensures early feedback and catches issues before the commit phase.

## Review Checklist

Use these questions when reviewing code. Each "no" is a candidate for deletion or simplification.

**Deletion test:**
- [ ] Would deleting this abstraction break anything? If not, delete it.
- [ ] Is this helper called from more than one place? If not, inline it.
- [ ] Is this config parameter ever varied in tests or deployment? If not, hardcode it.

**Abstraction test:**
- [ ] Does this base class have at least two concrete implementations? If not, delete the base.
- [ ] Has this pattern appeared three times with variation? If not, tolerate duplication.
- [ ] Is the interface simpler than the implementation? If not, the module is shallow.

**Async test:**
- [ ] Does a sync caller exist or is one planned this quarter? If not, no sync wrapper needed.
- [ ] Is the sync wrapper using `asyncio.run` (no thread)? If using `threading`/`new_event_loop`, justify.

**Config test:**
- [ ] Is config loaded once at the edge (clevis)? If threaded through functions, refactor.
- [ ] Is this parameter needed by callers? If only tests vary it, consider dependency injection instead.

**Comment test:**
- [ ] Does this comment explain WHY rather than WHAT? If WHAT, delete it.
- [ ] Is this public API documented? If not, add docstring.

**Style test:**
- [ ] 2-space indentation enforced?
- [ ] Line length under 100?
- [ ] Type annotations present on public functions?

## References

- John Ousterhout, *A Philosophy of Software Design* — deep modules, classitis, information hiding
- Sandi Metz, "The Wrong Abstraction" — duplication vs. wrong abstraction, rule of three
- `clevis` — configuration loading from TOML + env + CLI

## Related Skills

- `python-project` - Project setup, dependency management, and virtual environments with uv