---
name: python-best-practices
description: Use this skill any time when editing Python code
---

# Python Best Practices

When creating Python code, ALWAYS use the best practices in the sections below.

## Always use 2 space indentation

Always use 2 space indentation!

## All Imports on Top

Always put all imports at the top of the module.

Don't use imports inside functions!

## Use Fully Qualified Module Names when Importing

Don't use relative module paths when its possible to use the fully qualified module name.

* 🛑 Don't use `from ..my_module.my_submodule import function_name`
* ✅ Use: `from my_project.my_module.my_submodule import function_name`

## Import Organization for Packages

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

3. **Common mistake**: Importing a class from the wrong module causes `ImportError`
4. **Pattern**: Define class in its logical module, import in `__init__.py`, list in `__all__`

## Function Parameters

Always expose configurable variables, as function parameters. Add sensible defaults, using environment variables if possibly available.

### Example

```python
def a_command(an_argument=None):
  if an_argument is None:
    an_argument = os.environ.get("ARGUMENT_ENV_VAR_NAME", "a sensible default")
  # perform logic using `an_argument`
```

## Use Classes to group Functions with common Configuration

If a module contains several functions that share common configuration parameters, create a class grouping those functions, adding properties for those common parameters.

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

## Error Handling Security

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

## Authentication Testing Patterns

When testing authenticated endpoints, mock at the middleware level:

```python
# tests/conftest.py should provide shared fixtures
def create_mock_session(session_id=None, user_id=None, token='session-token'):
  """Create a mock session for authentication testing."""
  from bson.objectid import ObjectId
  from datetime import datetime, timedelta

  if session_id is None:
    session_id = ObjectId()
  if user_id is None:
    user_id = ObjectId()

  now = datetime.utcnow()
  expires_at = now + timedelta(days=30)

  return {
    'id': str(session_id),
    'user_id': str(user_id),
    'token': token,
    'created_at': now.isoformat(),
    'expires_at': expires_at.isoformat()
  }

# In test files:
@pytest.fixture
def mock_db():
  with patch('kookiecooky.auth_middleware.get_valid_session') as mock_get_session:
    yield {'auth_middleware_get_valid_session': mock_get_session}

def test_authenticated_endpoint(self, client):
  user_id = ObjectId()
  session = create_mock_session(user_id=user_id)

  # Mock authentication
  self.mock_db['auth_middleware_get_valid_session'].return_value = session

  # Include Authorization header
  response = client.get(
    '/api/protected',
    headers={'Authorization': f'Bearer {session["token"]}'}
  )
```

**Key Points:**
1. Mock `kookiecooky.auth_middleware.get_valid_session`, not `kookiecooky.pages.auth.get_valid_session`
2. Use Bearer token authentication in tests (more reliable than cookies)
3. Always include the Authorization header in authenticated requests

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

## Async-First Design Pattern

When designing Python modules that involve I/O operations (database, network, file system), **prefer async-first with optional sync wrappers**.

### Design Principle

**Primary implementation:** Async-first using `async`/`await`
**Convenience layer:** Sync wrapper classes for simpler usage

This approach provides:
- **Maximum flexibility**: Async clients for async applications (FastAPI, Quart, asyncio)
- **Simplicity**: Sync wrappers for scripts, CLI tools, synchronous applications
- **Performance**: No thread overhead in async contexts
- **Consistency**: Same API surface for both async and sync users

### Implementation Pattern

```python
# 1. Primary async implementation (IMAPClient, SMTPClient, etc.)
class IMAPClient:
    """Async IMAP client - primary implementation."""
    
    async def connect(self) -> IMAP4_SSL:
        """Async connection establishment."""
        ...
    
    async def search(self, folder: str = "INBOX") -> list[str]:
        """Async search operation."""
        ...
    
    async def __aenter__(self) -> IMAPClient:
        await self.connect()
        return self
    
    async def __aexit__(self, *args) -> None:
        await self.disconnect()

# 2. Sync wrapper (SyncIMAPClient, SyncSMTPClient, etc.)
class SyncIMAPClient:
    """Synchronous wrapper around IMAPClient.
    
    Uses dedicated event loop in background thread (Strategy 2).
    """
    
    def __init__(self, account: EmailAccount):
        self._async_client = IMAPClient(account)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()
    
    def __enter__(self) -> SyncIMAPClient:
        return self
    
    def __exit__(self, *args) -> None:
        self.disconnect()
    
    def _run_coroutine(self, coro: object) -> Any:
        """Run coroutine in dedicated event loop."""
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()
    
    def connect(self) -> IMAP4_SSL:
        """Sync wrapper around async connect."""
        return self._run_coroutine(self._async_client.connect())
    
    def search(self, folder: str = "INBOX") -> list[str]:
        """Sync wrapper around async search."""
        return self._run_coroutine(self._async_client.search(folder))
```

### Key Implementation Details

1. **Context Manager Support**: Both async and sync versions support context managers
2. **Error Handling**: Sync wrappers should wrap network errors in `RuntimeError`
3. **Thread Safety**: Each sync client has its own event loop and thread
4. **Connection Pooling**: Preserved from async implementation
5. **Type Annotations**: Full type annotations for both async and sync versions

### Package Exports

```python
# __init__.py
from .async_client import AsyncClient  # Primary
from .sync_client import SyncClient    # Wrapper

__all__ = ["AsyncClient", "SyncClient", ...]
```

### When to Use Which

| Use Async Clients | Use Sync Clients |
|-------------------|------------------|
| FastAPI, Quart, etc. | Scripts, CLI tools |
| asyncio-based apps | Synchronous applications |
| Need max performance | Simplicity is priority |
| Already using async/await | No existing async context |

### What NOT to Do

```python
# ❌ WRONG: Using sync client in async context
async def my_async_function():
    with SyncIMAPClient(account) as client:  # Error: nested event loop
        messages = client.search()

# ✅ CORRECT: Use async client in async context
async def my_async_function():
    async with IMAPClient(account) as client:
        messages = await client.search()
```

### Documentation Pattern

When documenting both APIs:

```markdown
## Choosing Async or Sync

This package provides **both async and sync APIs**:

- **Async clients** (IMAPClient, SMTPClient): For async applications (FastAPI, Quart, asyncio)
- **Sync clients** (SyncIMAPClient, SyncSMTPClient): For simpler synchronous code (scripts, CLI tools)

Both client types provide identical functionality - sync clients are thin wrappers around async clients using a dedicated event loop in a background thread.
```

## Related Skills

- `python-project` - Project setup, dependency management, and virtual environments with uv
