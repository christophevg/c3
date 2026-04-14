---
name: api2mod
description: Convert API documentation into Python modules with client library, CLI, and REPL. Use when user mentions api2mod, converting API to module, generating client from OpenAPI/Swagger/Postman, or creating Python API clients.
---

# api2mod

Convert API documentation into a Python package providing a client library, CLI interface, and REPL-like interactive shell.

## Overview

| Capability | Description |
|------------|-------------|
| API Parsing | OpenAPI/Swagger, Postman, RapidAPI/Insomnia, custom docs |
| Client Generation | Sync + async methods, TypedDict/dataclass models |
| CLI Mode | Direct command execution with args |
| REPL Mode | Interactive shell with persistent history and rich formatting |
| Auth Support | Cookie auth (named cookies), Bearer token, Basic, Custom |

## When to Use This Skill

Use this skill when:
- User asks to convert API documentation to Python module
- User wants to generate a client library from OpenAPI/Swagger
- User needs a REPL for exploring an API interactively
- User mentions "api2mod"

## Workflow

```
API Documentation → Parse → Generate Package → Test → Done
                        ↓
                   Prompt for:
                   - Package name (default from API title)
                   - Output location
```

### Step 1: Gather Requirements

Ask the user for:
1. **API documentation source** - File path or URL to API docs
2. **Package name** - Suggest sensible default from API title
3. **Output location** - Default to current directory

### Step 2: Detect Format

Automatically detect the API documentation format:

| Format | Detection |
|--------|-----------|
| OpenAPI JSON | `"openapi"` key in JSON |
| OpenAPI YAML | `openapi:` at root |
| Swagger JSON | `"swagger"` key with version |
| Postman | `"info"` with `"_postman_id"` |
| Insomnia | `"_type": "export"` |
| Custom | Fallback to manual parsing |

### Step 3: Generate Package Structure

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
│   ├── __main__.py         # Entry point (CLI + REPL)
│   └── repl.py             # REPL with persistent history
└── README.md               # Usage documentation
```

### Step 4: Generate Client Code

For each API endpoint:
1. Create method on client class (sync + async versions)
2. Generate request/response models as TypedDict or dataclass
3. Include docstrings from API description
4. Handle authentication based on security schemes

### Step 5: Generate REPL Shell

Create interactive shell using `cmd` + `prompt_toolkit` + `rich`:
- Each client method becomes a command
- Persistent command history across sessions
- Rich formatting with colors, tables, panels
- Ctrl+C clears input (doesn't exit)

**Dependencies**: Include `rich>=13.0.0` in pyproject.toml alongside `httpx` and `prompt-toolkit`.

### Step 6: Configure Entry Point

Set up `pyproject.toml`:
- Console script entry point named after package
- If args provided → CLI mode (execute and exit)
- If no args → REPL mode (interactive)

### Step 7: Environment Variable Support

Add support for credentials via environment variables:

1. **Add dependency**: Include `python-dotenv>=1.0.0` in pyproject.toml

2. **Environment variable naming**: Use `{PREFIX}_{CRED}` convention:
   - `{PREFIX}_CLIENT_ID` - API client ID
   - `{PREFIX}_CLIENT_SECRET` - API client secret
   - `{PREFIX}_USERNAME` - Account username (for auto-auth)
   - `{PREFIX}_PASSWORD` - Account password (for auto-auth)
   - `{PREFIX}_BASE_URL` - Custom API base URL (optional)

3. **Load .env file**: Use `load_dotenv()` in the entry point

4. **Auto-authentication**: If username/password are provided via env vars, authenticate automatically on startup

```python
def main() -> None:
  # Load .env file from current directory
  load_dotenv()

  # Check for environment variables
  env_client_id = os.environ.get("PREFIX_CLIENT_ID")
  env_client_secret = os.environ.get("PREFIX_CLIENT_SECRET")
  env_username = os.environ.get("PREFIX_USERNAME")
  env_password = os.environ.get("PREFIX_PASSWORD")

  parser = argparse.ArgumentParser(...)
  parser.add_argument("--client-id", default=env_client_id, help="...")
  parser.add_argument("--client-secret", default=env_client_secret, help="...")
  parser.add_argument("--username", default=env_username, help="...")
  parser.add_argument("--password", default=env_password, help="...")
  # ...

  # Auto-authenticate if credentials provided
  if args.username and args.password:
    try:
      token = client.authenticate(args.username, args.password)
      console.print(f"[green]✓[/green] Authenticated (expires in {token.expires_in}s)")
    except Exception as e:
      console.print(f"[yellow]Warning:[/yellow] Auto-authentication failed: {e}")
```

5. **Create .env.example**: Provide example environment file

```env
# API Credentials
PREFIX_CLIENT_ID=your_client_id_here
PREFIX_CLIENT_SECRET=your_client_secret_here

# Account Credentials (for auto-authentication)
PREFIX_USERNAME=your_username_here
PREFIX_PASSWORD=your_password_here

# Optional
# PREFIX_BASE_URL=https://api.example.com/v1
```

### Step 8: Create Research Documentation

After gathering API documentation, create a `RESEARCH.md` file documenting all discovered information:

- All endpoints with HTTP methods, paths, parameters
- Authentication methods and flows
- Request/response formats
- Data models and their fields
- All source URLs for reference

This preserves API research for future maintenance and extension.

## Authentication Patterns

### Cookie Authentication

Support for cookie-based authentication with configurable cookie names:

```python
class CookieAuth:
    def __init__(self, cookie_value: str, cookie_name: str = "session"):
        self.cookie_value = cookie_value
        self.cookie_name = cookie_name

    def apply(self, cookies: dict) -> None:
        cookies[self.cookie_name] = self.cookie_value

class AuthManager:
    def set_cookie_auth(self, cookie_value: str, cookie_name: str = "session") -> None:
        self._auth = CookieAuth(cookie_value, cookie_name)
```

REPL command:
```
cookie <value> [name]
```

### Bearer Token Authentication

```python
class BearerAuth:
    def __init__(self, token: str):
        self.token = token

    def apply(self, headers: dict) -> None:
        headers["Authorization"] = f"Bearer {self.token}"
```

## httpx Cookie Domain Fix

**CRITICAL**: httpx normalizes `localhost` to `localhost.local` for cookie domains. This breaks cookie matching on subsequent requests.

Add this fix in the request method:

```python
def _request(self, method: str, path: str, ...) -> Any:
    # ... make request ...
    response = self._client.request(method, url, ...)
    
    # Fix httpx cookie domain normalization
    cookies_to_fix = []
    for cookie in list(self._client.cookies.jar):
        if cookie.domain and '.local' in cookie.domain:
            cookies_to_fix.append((
                cookie.name, cookie.value,
                cookie.domain.replace('.local', ''),
                cookie.path
            ))
            self._client.cookies.jar.clear(cookie.domain, cookie.path, cookie.name)
    
    for name, value, domain, path in cookies_to_fix:
        self._client.cookies.set(name, value, domain=domain, path=path)
    
    response.raise_for_status()
    return response.json()
```

## REPL Design Patterns

### Persistent Command History

Use `prompt_toolkit`'s `FileHistory` for cross-session history:

```python
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from pathlib import Path

class APIRepl(cmd.Cmd):
    # Command names for autocompletion
    COMMANDS = [
        "login", "logout", "whoami",
        "users", "user",
        # ... list all commands
    ]

    def __init__(self, ...):
        # Set up persistent history
        history_dir = Path.home() / ".{package_name}"
        history_dir.mkdir(exist_ok=True)
        history_file = history_dir / "history"

        # Set up autocompleter
        completer = WordCompleter(self.COMMANDS, ignore_case=True)

        self._session = PromptSession(
            history=FileHistory(str(history_file)),
            completer=completer,
        )

    def cmdloop(self, intro=None):
        if intro:
            print(intro)
        
        stop = None
        while not stop:
            try:
                line = self._session.prompt(self.prompt)
            except KeyboardInterrupt:
                # Ctrl+C: clear input, show fresh prompt
                print()
                continue
            except EOFError:
                # Ctrl+D: exit
                print()
                break
            
            if not line.strip():
                continue
            
            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
```

### Rich Formatting for Output

Use the `rich` library for beautiful, colored terminal output:

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree as RichTree

class APIRepl(cmd.Cmd):
    def __init__(self, ...):
        self._console = Console()

    def _error(self, message: str) -> None:
        """Print error message in red."""
        self._console.print(f"[red]Error:[/red] {message}")

    def _success(self, message: str) -> None:
        """Print success message in green."""
        self._console.print(f"[green]✓[/green] {message}")

    def do_whoami(self, arg: str) -> None:
        """Show current user: whoami"""
        try:
            user = self.client.get_session()
            table = Table(title=f"[bold]{user.get('name')}[/bold]")
            table.add_column("Field", style="cyan")
            table.add_column("Value")
            table.add_row("Email", user.get('email', ''))
            table.add_row("Name", user.get('name', ''))
            self._console.print(table)
        except Exception as e:
            self._error(str(e))

    def do_list_items(self, arg: str) -> None:
        """List items in a table."""
        try:
            items = self.client.list_items()
            table = Table(title="Items")
            table.add_column("Name", style="cyan")
            table.add_column("ID", style="dim")
            for item in items:
                table.add_row(item.get('name'), item.get('id'))
            self._console.print(table)
        except Exception as e:
            self._error(str(e))

    def do_get_item(self, arg: str) -> None:
        """Show single item in a panel."""
        try:
            item = self.client.get_item(arg.strip())
            self._console.print(Panel(
                f"[bold]{item.get('name')}[/bold]\n"
                f"ID: {item.get('id')}\n"
                f"Status: [yellow]{item.get('status')}[/yellow]",
                title="Item Details",
                border_style="cyan"
            ))
        except Exception as e:
            self._error(str(e))
```

**Common patterns**:
- Use `Table` for listing multiple items with columns
- Use `Panel` for single item details with borders
- Use `Tree` for hierarchical data (folders, categories)
- Color-code status indicators: green=success/good, yellow=warning, red=error
- Use emojis in titles for visual distinction: 📊, 📚, 👥, 🔥, etc.

### Debug and Verbose Commands

Include commands for troubleshooting:

```python
def do_debug(self, arg: str) -> None:
    """Show debug info: debug"""
    print(f"Base URL: {self.client._base_url}")
    print(f"Auth configured: {self.client.auth.is_authenticated}")
    print(f"Client cookies: {dict(self.client._client.cookies)}")

def do_verbose(self, arg: str) -> None:
    """Toggle verbose mode: verbose"""
    self._verbose = not self._verbose
    self.client.set_verbose(self._verbose)
    print(f"Verbose mode: {'on' if self._verbose else 'off'}")
```

### Verbose Request Logging

```python
def _request(self, method: str, path: str, ...) -> Any:
    if self._verbose:
        print(f"[DEBUG] Request: {method} {self._base_url}{path}")
        print(f"[DEBUG] Headers: {headers}")
        print(f"[DEBUG] Client cookies: {dict(self._client.cookies)}")
    
    response = self._client.request(...)
    
    if self._verbose:
        print(f"[DEBUG] Response: {response.status_code}")
        print(f"[DEBUG] Response cookies: {dict(response.cookies)}")
    
    # Fix cookie domains
    self._fix_cookie_domains()
    
    response.raise_for_status()
    return response.json()
```

## Model Generation Patterns

### Import All Nested Models

Always import nested models used in parsing:

```python
from .models import (
    Topic,
    TopicItem,       # Nested model
    Question,
    QuestionLabels,  # Deeply nested model
)

def _parse_topic(self, data: dict) -> Topic:
    question = None
    if data.get("question"):
        q = data["question"]
        labels = QuestionLabels(**q["labels"]) if q.get("labels") else None
        question = Question(type=q.get("type"), labels=labels)
    # ...
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Circular imports in models | Use `from __future__ import annotations` |
| Auth not detected | Check `securitySchemes` in OpenAPI spec |
| Large API exceeds context | Process endpoints in batches |
| Custom docs unclear | Ask user to clarify endpoint structure |
| Cookies not persisting | Fix httpx `.local` domain normalization |
| NameError in model parsing | Import all nested model classes |
| Ctrl+C exits REPL | Catch KeyboardInterrupt, continue loop |
| Output looks plain | Use rich Console, Table, Panel for formatting |

## Case-Specific Adaptations

### Example: Flask-Login Session Exchange

Flask-Login uses a long-lived `remember_token` cookie that must be exchanged for a short-lived session cookie. This requires:

1. Set the `remember_token` cookie
2. Call the session endpoint to get a session cookie
3. Use the session cookie for subsequent requests

This is specific to Flask-Login and not a default pattern. If the target API uses similar patterns, adapt the client accordingly.

## Related Skills

- **api-architect** - Designs APIs (creates specs, opposite direction)
- **python** - General Python code guidance
- **python-developer** - Implements generated code