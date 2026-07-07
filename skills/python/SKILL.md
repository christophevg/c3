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

### Line Breaking

**Don't wrap short constructs across multiple lines.** A one-line call that fits under 100 chars beats a 4-line wrapped version. Wrap only when a line exceeds 100 characters or breaking genuinely aids readability.

```python
# ❌ Needless wrapping
logger.warning(
  "Agent definition not found for %s",
  name,
)

register_plugin_agents(
  registry,
  loader,
  config,
)

__all__ = [
  "Client",
  "AsyncClient",
  "Session",
]

# ✅ Single line
logger.warning("Agent definition not found for %s", name)
register_plugin_agents(registry, loader, config)
__all__ = ["Client", "AsyncClient", "Session"]
```

Short signatures, single-argument calls, and small collections stay on one line. Let the 100-char limit, not aesthetics, decide when to break.

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

### Keep `__all__` and Imports in Sync

`__all__` and the import block must reflect what actually exists. When you remove a symbol, remove it from `__all__`, drop its import, and delete any `TYPE_CHECKING` import that only existed for it.

```python
# ❌ Stale after register_configured_plugin_agents was removed
from .registry import register_plugin_agents, register_configured_plugin_agents  # dead

__all__ = [
  "register_plugin_agents",
  "register_configured_plugin_agents",  # dead
  "Session",  # dead TYPE_CHECKING import
]

# ✅ Cleaned up
from .registry import register_plugin_agents

__all__ = ["register_plugin_agents"]
```

## Inline Single-Use Indirections

**Rule:** If a function/method has exactly one call site and its body is shorter than (or comparable to) its signature, inline it. Keep functions only when they have multiple call sites or real logic worth naming.

### When to inline

| Signal | Action |
|--------|--------|
| One call site + body is a single expression | Inline |
| One call site + body is 1-3 lines of trivial logic | Inline |
| One call site + body has real logic worth naming | Keep (judgment call) |
| Multiple call sites | Keep |
| Empty intermediate subclass (no behavior, just a parent) | Flatten — subclass extends baseclass directly |
| Intermediate variable used once, then passed once | Inline the expression at the call site |

### Examples

**Inline (single-use wrapper):**
```python
# Before — indirection
def _run_bootstrap(ui):
    return BootstrapWizard(ui).run() == BootstrapResult.WRITTEN

# After — inlined at the call site
if BootstrapWizard(ui).run() == BootstrapResult.WRITTEN:
    ...
```

**Inline (single-line property):**
```python
# Before — indirection
@property
def max_recursion_depth(self):
    return self.config.tools.agent.max_recursion_depth

# After — inline at the one call site
self.config.tools.agent.max_recursion_depth
```

**Flatten empty intermediate class:**
```python
# Before — empty indirection layer
class BasicContextManager(ContextManager):
    pass  # no behavior

class SimpleContextManager(BasicContextManager):
    ...

# After — flattened
class SimpleContextManager(ContextManager):
    ...
```

**Inline (single-use intermediate variable):**
```python
# Before — intermediate exists only to be passed once
effective_plugins = plugins if plugins is not None else extra_plugins
agent = _create_agent(effective_plugins)

# After — ternary inlined at the one call site
agent = _create_agent(plugins if plugins is not None else extra_plugins)
```

### When NOT to inline

- The function has multiple call sites (DRY)
- The function name adds meaningful documentation value (the name explains intent better than the code)
- The function encapsulates complex logic that would make the call site harder to read
- The function is part of a public API or protocol

### Rationale

Indirections (single-use wrappers, empty intermediate classes, one-line properties) add cognitive overhead without value. They force the reader to jump to a definition just to find a one-liner. Inlining makes the code flow linear and readable. This aligns with the broader principle of removing redundancy: if the abstraction doesn't earn its keep, it's noise.

## Use Classes to Group Functions with Common Configuration

If a module contains several functions that share common configuration parameters, create a class grouping those functions, adding properties for those common parameters.

## Thin Constructors

`__init__` stays thin: assign fields and call at most one named helper for multi-step setup. Don't drop a 25-line resolution cascade directly in the constructor — extract it.

```python
# ❌ Multi-step logic inlined in __init__
def __init__(self, name, registry, path=None):
  self.name = name
  if name in registry:
    self._definition = registry[name]
  elif path is not None and path.exists():
    self._definition = load(path)
  elif default_path.exists():
    self._definition = load(default_path)
  else:
    raise NotFoundError(name)

# ✅ Thin constructor, logic in a named helper
def __init__(self, name, registry, path=None):
  self.name = name
  self._definition = self._resolve_definition(name, registry, path)

def _resolve_definition(self, name, registry, path):
  """Best-effort cascade: registry → path → default."""
  # ...
```

A reader scanning `__init__` should see the shape of the object, not the algorithm that built it.

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

## Defaults and Environment

**Don't use `None`-sentinel parameters that re-read the environment on every call.** Give the parameter a real default value, computed once as a module constant at import.

```python
# ❌ Re-reads env per call; None-sentinel obscures the real default
def __init__(self, console_logging: bool | None = None):
  effective = (
    console_logging
    if console_logging is not None
    else os.environ.get("YOKER_CONSOLE_LOGGING", "") == "1"
  )
  self.console_logging = effective

# ✅ Module constant computed once; parameter has a real default
CONSOLE_LOGGING = os.environ.get("YOKER_CONSOLE_LOGGING", "") == "1"

def __init__(self, console_logging: bool = CONSOLE_LOGGING):
  self.console_logging = console_logging
```

Read environment variables once at import, not per call. If a caller needs to override, they pass the value — no `None`-sentinel dance.

## Comments and Docstrings

**Use the `python-comments` skill** for detailed commenting guidelines. Key principles:

- **Why-only.** Comments explain intent, not mechanics. Delete any comment that restates what the code says.
- **Docstrings** required on public APIs (modules, classes, public methods).
- **Args/Returns** only when signature doesn't tell the full story (type hints handle types).
- **Private helpers** (prefixed `_`) need no docstring unless logic is non-obvious.

## Anti-Patterns to Avoid

| Anti-pattern | Why it's bloat | Instead |
|--------------|----------------|---------|
| **Reimplementing existing libraries** | NIH — maintenance burden, missing edge cases | Use `litellm`, `httpx`, `pydantic`, etc. |
| Sync + async parallel APIs for everything | Maintenance cost for callers that don't exist | Add sync facade only when needed |
| Parameter + env var + default for every variable | Config pyramid nobody varies | Hardcode sensible defaults; add config when proven |
| Base class for one subclass | Indirection with no payoff | Delete the base; keep the concrete class |
| `try/except` around code that can't throw | Hides real errors | Catch only what can actually fail |
| Helper called once | Layer with no caller diversity | Inline it |
| Defensive type-checking inside typed code | Protects against nothing | Trust the type system |
| Config object for one value | Over-engineering | Pass the value directly |
| Abstract factory returning one concrete | Factory with no variation | Return the concrete directly |
| `param: T \| None = None` + `os.environ.get` per call | Re-reads env, hides the real default | Module constant; parameter keeps a real default |
| Multi-step setup logic in `__init__` | Constructor narrates an algorithm | Extract a named `_resolve_*` helper |
| Dead branch kept "just in case" with an apologetic comment | Unreachable code with a comment excuse | Delete the branch |
| Needless multi-line wrapping of short calls/signatures/collections | 4 lines for a 60-char call | Keep it on one line |

For comment-specific anti-patterns, see the `python-comments` skill.

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
- [ ] Is there a dead branch kept "just in case"? If so, delete it.

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
- [ ] For docstrings: Are Args/Returns needed, or does the signature tell the story?
- [ ] See `python-comments` skill for detailed guidelines.

**Construction & defaults test:**
- [ ] Does any parameter use `None`-sentinel + per-call env fallback? If so, use a module constant with a real default.
- [ ] Is `__init__` doing multi-step logic? If so, extract a named helper.
- [ ] Are `__all__` and the imports stale after a removal? If so, clean them up.

**Style test:**
- [ ] 2-space indentation enforced?
- [ ] Line length under 100?
- [ ] Type annotations present on public functions?
- [ ] Any short call/signature/collection wrapped across lines needlessly? If so, collapse it.

## References

- John Ousterhout, *A Philosophy of Software Design* — deep modules, classitis, information hiding
- Sandi Metz, "The Wrong Abstraction" — duplication vs. wrong abstraction, rule of three
- `clevis` — configuration loading from TOML + env + CLI

## Related Skills

- `python-project` - Project setup, dependency management, and virtual environments with uv
- `python-comments` - Detailed guidelines for comments and docstrings (tight, relevant, WHY-not-WHAT)
