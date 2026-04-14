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
