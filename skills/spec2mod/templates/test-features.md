# spec2mod Feature Checklist

When generating a package from an OpenAPI spec, verify these features are present:

## REPL Features

### Welcome Banner
- [ ] Shows version info from `info.version`
- [ ] Shows API name from `info.title`
- [ ] Shows help/exit instructions
- [ ] Uses Rich Panel with border

### Cookie Command
- [ ] `do_cookie` method exists
- [ ] Accepts `<value> [name]` arguments
- [ ] Default cookie name is "session"
- [ ] Sets `client.auth` to `CookieAuth` with both `cookie_value` and `cookie_name`
- [ ] Shows success message with cookie name

### Debug Command
- [ ] Shows `Base URL`
- [ ] Shows `Auth` status and cookie name
- [ ] Shows `Trace` mode
- [ ] Shows `Verbose` mode

### Command Aliases
- [ ] `whoami` alias for `get_session` exists
- [ ] `search` alias for `search_users` exists (if applicable)
- [ ] `login <token>` command accepts token parameter
- [ ] Aliases are in COMMANDS list for autocomplete

### ARGUMENTS Dictionary
- [ ] Contains `"cookie": ["value", "name?"]`
- [ ] Contains aliases like `"whoami": []`, `"login": ["token"]`

### COMMANDS List
- [ ] Contains `"cookie"`
- [ ] Contains command aliases

### __init__ Method
- [ ] Initializes `self._cookie_name = "session"`

## Client Features

### Authentication
- [ ] `CookieAuth` class accepts `cookie_value` AND `cookie_name` parameters
- [ ] `CookieAuth.apply()` uses the specified cookie name (NOT hardcoded to "session")
- [ ] `BearerAuth` class in auth.py
- [ ] Auth handlers implement `apply()` method

### Trace/Verbose
- [ ] `set_trace()` method
- [ ] `set_verbose()` method
- [ ] `_trace` attribute
- [ ] `_verbose` attribute

### Response Parsing
- [ ] Methods return typed models, NOT raw dicts
- [ ] Uses `Model.from_dict(data)` pattern
- [ ] List returns use `[Model.from_dict(item) for item in data]`

### Request Objects
- [ ] Complex operations use request objects (e.g., `SessionCreateRequest`)
- [ ] Request objects have `to_dict()` method
- [ ] Client methods call `request.to_dict()` for serialization

### Auth Override Methods
- [ ] Methods with operation-level security accept auth parameters
- [ ] Example: `create_auth_session(self, token: str) -> User`
- [ ] Uses `headers={"Authorization": f"Bearer {token}"}`

### Base URL
- [ ] Default base URL matches spec exactly (preserves relative URLs)
- [ ] Does NOT assume localhost if spec has relative URL

## Models Features

### Dataclass Usage
- [ ] All models use `@dataclass` decorator (NOT TypedDict)
- [ ] Models have `from_dict()` classmethod for parsing
- [ ] Request models have `to_dict()` method for serialization

### Type Safety
- [ ] Fields have type hints
- [ ] Optional fields use `Optional[T] = None` or `= field(default=...)`
- [ ] List fields use `field(default_factory=list)`

### Error Handling
- [ ] `from_dict()` validates input is a dict
- [ ] Uses `.get()` with defaults, never direct access

## pyproject.toml Features

### Metadata
- [ ] Author includes both `name` and `email`
- [ ] Description is "Python client for {api_name}" (not API description)

## Template Variables

The following variables must be populated from the OpenAPI spec:

| Variable | Source |
|----------|--------|
| `{{api_name}}` | `info.title` |
| `{{api_version}}` | `info.version` |
| `{{package_name}}` | User input |
| `{{default_base_url}}` | `servers[0].url` (preserve exactly) |
| `{{author_name}}` | User input or git config |
| `{{author_email}}` | User input or git config |

## Test Commands

### Test 1: Welcome Banner and Cookie

```bash
echo -e "cookie test_value remember_token\ndebug" | python -m {{package_name}} --base-url http://localhost:8000/api
```

Expected output:
```
╭─────────────────────────────────────────╮
│ 🔥 {{api_name}} Client v{{api_version}} │
│ Type 'help' for available commands     │
│ Press Ctrl+D to exit                   │
╰─────────────────────────────────────────╯

{{package_name}}> cookie test_value remember_token
✓ Session cookie 'remember_token' set
{{package_name}}> debug
╭───────────────────────────────── Debug Info ─────────────────────────────────╮
│ Base URL: http://localhost:8000/api                                          │
│ Auth: cookie (remember_token)                                                │
│ Trace: False                                                                 │
│ Verbose: False                                                               ╰──────────────────────────────────────────────────────────────────────────────╯
```

### Test 2: Cookie Name is Used in Request

```bash
echo -e "cookie test_value remember_token\ntrace on\nwhoami" | python -m {{package_name}} --base-url http://localhost:8000/api --verbose
```

Expected output includes:
```
[TRACE] GET http://localhost:8000/api/session
[DEBUG] Headers: {'Cookie': 'remember_token=test_value'}
```

**CRITICAL**: The header must show `remember_token=`, NOT `session=`.

### Test 3: Dict Output Formatting

The `_display_dict` method should detect user info patterns and format nicely:

```python
# When dict has 'email' and 'name' keys:
{"email": "user@example.com", "name": "John Doe", "current": "user@example.com"}
```

Should output as:
```
╭─────────────────────────────── Result ───────────────────────────────────╮
│ Email:    user@example.com                                               │
│ Name:     John Doe                                                       │
│ Current:  user@example.com                                               │
╰──────────────────────────────────────────────────────────────────────────╯
```

**NOT** a raw dict like `{'email': '...', 'name': '...'}`

This is a generic pattern - any command returning a dict with `email` and `name` keys gets nice formatting.

### Test 3.5: Dataclass List Visualization

The `_display_list` method must handle dataclass objects (NOT just dicts):

```python
# Client returns dataclass objects, NOT dicts
topics = client.list_topics()  # Returns list[Topic]
print(type(topics[0]))  # <class 'package.models.Topic'>
```

When displayed in REPL, should show as Rich table:

```
╭──────────────────────────────────────────────────────────────────────╮
│ ID          │ Name                     │ Tags                         │
├─────────────┼──────────────────────────┼──────────────────────────────┤
│ abc123      │ French Vocabulary        │ french, vocab                │
│ def456      │ Math Formulas            │ math, formulas               │
╰──────────────────────────────────────────────────────────────────────╯
```

**NOT** as bullet points:
```
  • Topic(_id='abc123', name='French Vocabulary', ...)
  • Topic(_id='def456', name='Math Formulas', ...)
```

**Key Implementation**:
- `_display_list` must check `hasattr(first, "__dict__")` to detect dataclass objects
- Use `vars(first).keys()` to get field names
- Use `getattr(item, field)` to extract values
- Handle nested dataclass objects (e.g., `UserInfo` inside `FollowingStreak`)

### Test 3.6: Single Dataclass Visualization

Single dataclass objects should display as formatted dict:

```python
user = client.get_session()  # Returns User dataclass
# In REPL, should show as panel:
```

```
╭─────────────────────────────── Current User ───────────────────────────╮
│ Email:    user@example.com                                               │
│ Name:     John Doe                                                       │
│ Current:  user@example.com                                               │
╰──────────────────────────────────────────────────────────────────────────╯
```

**Key Implementation**:
- `_display` must check `hasattr(result, "__dict__")` before falling to generic print
- Convert dataclass to dict with `vars(result)`
- Pass to `_display_dict` for nice formatting

### Test 4: Models Return Typed Objects

```python
from {{package_name}} import Client

client = Client(base_url="http://localhost:8000/api")
user = client.get_session()
print(type(user))  # Should be <class '{{package_name}}.models.User'>, NOT <class 'dict'>
print(user.name)   # Should work with attribute access
```

### Test 5: Request Objects Work

```python
from {{package_name}} import Client, SessionCreateRequest

client = Client(base_url="http://localhost:8000/api")
request = SessionCreateRequest(kind="quiz", topics=["topic1", "topic2"])
response = client.create_session(request)
print(response.session_id)  # Should work
```

### Test 6: Login Command with Token

```bash
echo -e "login my_oauth_token_here\nwhoami" | python -m {{package_name}} --base-url http://localhost:8000/api --verbose
```

Expected output includes:
```
[TRACE] POST http://localhost:8000/api/session
[DEBUG] Headers: {'Authorization': 'Bearer my_oauth_token_here'}
```