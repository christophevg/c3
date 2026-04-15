# REPL Module Template

## Command Aliases

When generating REPL commands, create user-friendly aliases for common operations:

| Alias | Method | Why |
|-------|--------|-----|
| `whoami` | `get_session` | Common CLI convention |
| `search` | `search_users` | Shorter |
| `topic` | `get_topic` | Simpler |
| `login <token>` | `create_auth_session` | Accepts token parameter |

Aliases are implemented as additional `do_*` methods that call the main method:

```python
def do_whoami(self, arg: str) -> None:
  """Alias for 'session' command."""
  self.do_session(arg)
```

For methods that require parameters (like `login`), the alias accepts the parameter:

```python
def do_login(self, arg: str) -> None:
  """Create session via OAuth.
  
  Usage: login <token>
  """
  parts = arg.strip().split()
  if not parts:
    self._show_usage("login")
    return
  token = parts[0]
  try:
    result = self.client.create_auth_session(token)
    self._display(result, title="Logged In")
  except Exception as e:
    self._error(str(e))
```

## repl.py

```python
"""Interactive REPL for {{api_name}} API."""

import cmd
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.document import Document
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel

from .client import {{client_class_name}}


class ArgumentHintSuggester(AutoSuggest):
    """Auto-suggester that shows argument hints as ghost text."""
    
    def __init__(self, arguments: dict[str, list[str]]):
        self.arguments = arguments
    
    def get_suggestion(self, buffer, document):
        """Get suggestion showing remaining arguments as ghost text."""
        text = document.text_before_cursor
        
        # Only suggest after a command is entered (has space)
        parts = text.strip().split()
        if len(parts) < 1:
            return None
        
        cmd = parts[0].lower()
        if cmd not in self.arguments:
            return None
        
        args = self.arguments[cmd]
        entered = len(parts) - 1
        
        if entered < len(args):
            remaining = args[entered:]
            suggestion_text = " ".join(f"<{a}>" for a in remaining)
            
            if text.endswith(" "):
                return Suggestion(suggestion_text)
            elif len(parts) > 1:
                remaining = args[entered:] if entered < len(args) else []
                if remaining:
                    suggestion_text = " ".join(f"<{a}>" for a in remaining)
                    return Suggestion(" " + suggestion_text)
        
        return None


class ArgumentHintCompleter(Completer):
    """Completer that only completes command names."""
    
    def __init__(self, commands: list[str]):
        self.commands = commands
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        word = document.get_word_before_cursor()
        
        # Only complete command names at the start (no space yet)
        if " " not in text.lstrip():
            for cmd in self.commands:
                if cmd.startswith(word.lower()):
                    yield Completion(
                        cmd,
                        start_position=-len(word),
                        display=cmd,
                    )


class {{repl_class_name}}(cmd.Cmd):
    """Interactive REPL for {{api_name}} API.
    
    Commands:
    {{#each commands}}
        {{name}} - {{summary}}
    {{/each}}
    
    Special commands:
        cookie <value> [name] - Set session cookie for authentication
        help <command> - Show command documentation
        trace          - Toggle endpoint URL tracing
        verbose        - Toggle verbose request logging
        debug          - Show debug information
        exit           - Exit the REPL
    """
    
    prompt = "{{package_name}}> "
    
    # API version from OpenAPI spec
    API_VERSION = "{{api_version}}"
    
    # Command argument specifications for usage hints
    # Format: "command": ["arg1", "arg2", "arg3?"] (? = optional)
    ARGUMENTS = {
        "cookie": ["value", "name?"],
        {{#each commands}}
        "{{name}}": [{{#each params}}"{{name}}",{{/each}}],
        {{/each}}
    }
    
    COMMANDS = [
        "cookie",
        {{#each commands}}
        "{{name}}",
        {{/each}}
        "debug", "trace", "verbose", "help", "exit", "quit"
    ]
    
    def __init__(self, client: {{client_class_name}}):
        super().__init__()
        self.client = client
        self.console = Console()
        self.session: PromptSession | None = None
        self._trace = False
        self._verbose = False
        self._cookie_name = "session"  # Default cookie name
        self._setup_completer()
    
    def _setup_completer(self):
        """Set up command completer and auto-suggester."""
        self._completer = ArgumentHintCompleter(self.COMMANDS)
        self._suggester = ArgumentHintSuggester(self.ARGUMENTS)
    
    def _error(self, message: str) -> None:
        """Print error message in red."""
        self.console.print(f"[red]Error:[/red] {message}")
    
    def _success(self, message: str) -> None:
        """Print success message in green."""
        self.console.print(f"[green]✓[/green] {message}")
    
    def _show_usage(self, command: str) -> None:
        """Show usage hint with argument placeholders.
        
        Args:
            command: Command name
        """
        if command not in self.ARGUMENTS:
            return
        
        args = self.ARGUMENTS[command]
        if not args:
            return
        
        arg_hints = " ".join(f"<{arg}>" for arg in args)
        self.console.print(f"[dim]{command} {arg_hints}[/dim]")
    
    def _get_arg_hint(self, text: str) -> str:
        """Get argument hint for the current input.
        
        Args:
            text: Current input text
        
        Returns:
            Hint string showing remaining arguments
        """
        parts = text.strip().split()
        if not parts:
            return ""
        
        cmd = parts[0].lower()
        if cmd not in self.ARGUMENTS:
            return ""
        
        args = self.ARGUMENTS[cmd]
        entered = len(parts) - 1
        
        if entered < len(args):
            remaining = args[entered:]
            hint = " ".join(f"<{a}>" for a in remaining)
            return hint
        
        return ""
    
    def _format_value(self, val: Any, field_name: str = "") -> Any:
        """Format a value for display in tables.

        Handles:
        - None: empty string
        - Dataclass with __rich_console__: return object for Rich to render
        - Dataclass objects: extract name/email or stringify
        - Lists of dataclass objects: show count for long lists, or items for short
        - Lists of primitives: comma-separated values
        - Other values: string representation

        Returns the value (possibly unchanged) so Rich can render it properly.
        """
        if val is None:
            return ""
        if hasattr(val, "__rich_console__"):
            # Let Rich render the dataclass with its __rich_console__ method
            return val
        if hasattr(val, "__dict__"):
            # Nested dataclass without __rich_console__ - extract useful identifier
            return getattr(val, "name", None) or getattr(val, "email", None) or str(val)
        if isinstance(val, list):
            if not val:
                return ""
            # For lists with >2 items, show count summary
            if len(val) > 2:
                item_name = field_name.rstrip("s") if field_name.endswith("s") else field_name
                return f"{len(val)} {item_name}s"
            # Short lists: show items
            if hasattr(val[0], "__dict__"):
                items = []
                for v in val:
                    name = getattr(v, "name", None) or getattr(v, "email", None)
                    items.append(name if name else str(v))
                return ", ".join(items)
            return ", ".join(str(v) for v in val)
        return str(val)
    
    def _display(self, result: Any, title: str = "Result") -> None:
        """Pretty-print result with rich."""
        if result is None:
            self.console.print("[dim]Done[/dim]")
            return
        
        if isinstance(result, list):
            self._display_list(result)
        elif isinstance(result, dict):
            self._display_dict(result, title=title)
        elif hasattr(result, "__dict__"):
            # Dataclass or regular object - display as dict
            self._display_dict(vars(result), title=title)
        else:
            self.console.print(result)
    
    def _display_list(self, items: list) -> None:
        """Display list as table or bullet points.

        Handles:
        - dicts: renders as table with keys as columns
        - dataclass objects: renders as table with field names as columns
        - primitives: renders as bullet points
        """
        if not items:
            self.console.print("[dim]No results[/dim]")
            return

        first = items[0]

        if isinstance(first, dict):
            # List of dicts - render as table
            table = Table(show_header=True, header_style="bold")
            for key in first.keys():
                table.add_column(key)
            for item in items:
                table.add_row(*[str(v) for v in item.values()])
            self.console.print(table)
        elif hasattr(first, "__dict__"):
            # List of dataclass objects - render as table
            table = Table(show_header=True, header_style="bold")
            fields = list(vars(first).keys())
            for field in fields:
                # Pretty column names (e.g., "_id" -> "ID")
                col_name = field.lstrip("_").replace("_", " ").title()
                table.add_column(col_name)
            for item in items:
                row_values = [self._format_value(getattr(item, field, None), field) for field in fields]
                table.add_row(*row_values)
            self.console.print(table)
        else:
            # Primitives - render as bullet points
            for item in items:
                self.console.print(f"  • {item}")
    
    def _display_dict(self, item: dict, title: str = "Result") -> None:
        """Display dict as formatted output.

        Detects common patterns and formats them nicely:
        - User info (has email/name): shows as labeled fields
        - Other dicts: shows as key-value pairs
        """
        # Check if this looks like user/session info
        if "email" in item and "name" in item:
            # User/session info - format nicely
            lines = []
            for key, value in item.items():
                if value is not None:
                    lines.append(f"[bold]{key.capitalize()}:[/bold]  {value}")
            self.console.print(Panel("\n".join(lines), title=title, border_style="green"))
        else:
            # Generic dict - show as key-value pairs
            lines = []
            for key, value in item.items():
                lines.append(f"[bold]{key}:[/bold]  {value}")
            self.console.print(Panel("\n".join(lines), title=title, expand=False))
    
    def cmdloop(self, intro: str | None = None) -> None:
        """Enhanced REPL with prompt_toolkit."""
        import os
        from pathlib import Path
        
        # Set up history file
        history_dir = Path.home() / ".{{package_name}}"
        history_dir.mkdir(exist_ok=True)
        history_file = history_dir / "history"
        
        self.session = PromptSession(
            history=FileHistory(str(history_file)),
            completer=self._completer,
            auto_suggest=self._suggester,
        )
        
        # Show welcome banner
        self.console.print(Panel(
            f"[bold]🔥 {{api_name}} Client v{self.API_VERSION}[/bold]\n"
            f"Type 'help' for available commands\n"
            f"Press Ctrl+D to exit",
            border_style="blue",
        ))
        self.console.print()
        
        while True:
            try:
                line = self.session.prompt(self.prompt)
                line = line.strip()
                
                if not line:
                    continue
                
                if line.lower() in ("exit", "quit", "q"):
                    self.console.print("[dim]Goodbye![/dim]")
                    break
                
                self.precmd(line)
                stop = self.onecmd(line)
                self.postcmd(stop, line)
                
            except KeyboardInterrupt:
                self.console.print("\n[dim]Use 'exit' to quit[/dim]")
            except EOFError:
                self.console.print("\n[dim]Goodbye![/dim]")
                break
    
    # ============================================
    # Authentication Commands
    # ============================================
    
    def do_cookie(self, arg: str) -> None:
        """Set session cookie for authentication.
        
        Usage: cookie <value> [name]
               value: The cookie value
               name: Cookie name (default: session)
        
        Examples:
          cookie abc123def456              # Sets 'session' cookie
          cookie abc123def456 remember_token  # Sets 'remember_token' cookie
        """
        parts = arg.strip().split()
        if not parts:
            self._show_usage("cookie")
            return
        
        cookie_value = parts[0]
        cookie_name = parts[1] if len(parts) > 1 else "session"
        
        try:
            from .auth import CookieAuth
            
            self._cookie_name = cookie_name
            self.client.auth = CookieAuth(cookie_value=cookie_value, cookie_name=cookie_name)
            self._success(f"Session cookie '{cookie_name}' set")
        except Exception as e:
            self._error(str(e))
    
    {{#each commands}}
    def do_{{name}}(self, arg: str) -> None:
        """{{summary}}
        
        Usage: {{name}} {{usage}}
        {{#if examples}}
        
        Examples:
        {{#each examples}}
          {{name}} {{args}}
        {{/each}}
        {{/if}}
        """
        # Check required arguments
        required_args = [a for a in self.ARGUMENTS.get("{{name}}", []) if not a.endswith("?")]
        parts = arg.strip().split() if arg else []
        if len(parts) < len(required_args):
            self._show_usage("{{name}}")
            return
        
        try:
            args = self._parse_args("{{name}}", arg)
            result = self.client.{{name}}(**args)
            self._display(result)
        except Exception as e:
            self._error(str(e))
    
    def help_{{name}}(self) -> None:
        """Show help for {{name}}."""
        self.console.print(Panel(self.do_{{name}}.__doc__, title="{{name}}"))
    {{/each}}
    
    # ========================================================================
    # Utility Commands
    # ========================================================================
    
    def do_debug(self, arg: str) -> None:
        """Show debug information.
        
        Usage: debug
        """
        auth_status = "cookie" if self.client.auth else "none"
        self.console.print(Panel(
            f"[bold]Base URL:[/bold] {self.client.base_url}\n"
            f"[bold]Auth:[/bold] {auth_status} ({self._cookie_name})\n"
            f"[bold]Trace:[/bold] {self._trace}\n"
            f"[bold]Verbose:[/bold] {self._verbose}",
            title="Debug Info",
            border_style="yellow"
        ))
    
    def do_trace(self, arg: str) -> None:
        """Toggle trace mode to show endpoint URLs.
        
        Usage: trace [on|off]
        
        When trace is enabled, the REPL shows the full endpoint URL
        for each API call, including query parameters.
        
        Examples:
          trace       - Toggle trace on/off
          trace on    - Enable trace mode
          trace off   - Disable trace mode
        """
        arg = arg.strip().lower()
        if arg == "on":
            self._trace = True
        elif arg == "off":
            self._trace = False
        else:
            self._trace = not self._trace
        
        self.client.set_trace(self._trace)
        self._success(f"Trace mode: {'on' if self._trace else 'off'}")
    
    def do_verbose(self, arg: str) -> None:
        """Toggle verbose mode for request logging.
        
        Usage: verbose [on|off]
        
        When verbose is enabled, the REPL shows detailed request
        and response information including headers and body data.
        
        Examples:
          verbose       - Toggle verbose on/off
          verbose on    - Enable verbose mode
          verbose off   - Disable verbose mode
        """
        arg = arg.strip().lower()
        if arg == "on":
            self._verbose = True
        elif arg == "off":
            self._verbose = False
        else:
            self._verbose = not self._verbose
        
        self.client.set_verbose(self._verbose)
        self._success(f"Verbose mode: {'on' if self._verbose else 'off'}")
    
    def do_help(self, arg: str) -> None:
        """Show help for commands."""
        if arg:
            help_func = getattr(self, f"help_{arg}", None)
            if help_func:
                help_func()
            else:
                self.console.print(f"[red]Unknown command: {arg}[/red]")
        else:
            self.console.print(self.__doc__)
    
    def _parse_args(self, command: str, arg: str) -> dict[str, Any]:
        """Parse command arguments.
        
        Supports:
        - Positional: login user pass
        - Named: login --username user --password pass
        """
        import shlex
        
        # Get command signature
        {{#each commands}}
        if command == "{{name}}":
            params = [{{#each params}}"{{name}}",{{/each}}]
        {{/each}}
        else:
            return {}
        
        tokens = shlex.split(arg) if arg else []
        result = {}
        
        # Parse named args (--name value)
        i = 0
        while i < len(tokens):
            if tokens[i].startswith("--"):
                name = tokens[i][2:]
                if i + 1 < len(tokens):
                    result[name] = tokens[i + 1]
                    i += 2
                else:
                    raise ValueError(f"Missing value for --{name}")
            else:
                # Positional arg
                if len(result) < len(params):
                    result[params[len(result)]] = tokens[i]
                    i += 1
                else:
                    raise ValueError(f"Unexpected argument: {tokens[i]}")
        
        return result
```

## __main__.py

```python
"""Entry point for {{package_name}} CLI/REPL."""

import sys
import argparse

from .client import {{client_class_name}}
from .async_client import Async{{client_class_name}}
from .repl import {{repl_class_name}}
from .auth_cache import AuthCache


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="{{api_name}} API client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to execute (omit for REPL mode)"
    )
    parser.add_argument(
        "args",
        nargs="*",
        help="Command arguments"
    )
    parser.add_argument(
        "--base-url",
        default="{{default_base_url}}",
        help="API base URL"
    )
    parser.add_argument(
        "--async",
        action="store_true",
        help="Use async client"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume previous session from cached authentication"
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable trace mode (show endpoint URLs)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose mode (show request/response details)"
    )

    args = parser.parse_args()

    # Create client
    if getattr(args, "async"):
        import asyncio
        client = Async{{client_class_name}}(base_url=args.base_url)
    else:
        client = {{client_class_name}}(base_url=args.base_url)

    # Apply trace/verbose settings from command line
    if args.trace:
        client.set_trace(True)
    if args.verbose:
        client.set_verbose(True)

    # Set up auth cache for token persistence
    auth_cache = AuthCache()

    # Try to resume from cache if --resume flag is set
    if args.resume:
        cached_token = auth_cache.load()
        if cached_token:
            # Restore token to client
            # Note: Implementation depends on auth system
            pass

    if args.command:
        # CLI mode: execute and exit
        try:
            method = getattr(client, args.command)
            result = method(*args.args)
            print(result)
        except AttributeError:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # REPL mode: interactive shell
        repl = {{repl_class_name}}(client)
        repl.cmdloop()


if __name__ == "__main__":
    main()
```

## Template Variables

| Variable | Source |
|----------|---------|
| `{{repl_class_name}}` | Derived from package name (e.g., `PetStoreRepl`) |
| `{{commands}}` | Generated from client methods |
| `{{package_name}}` | User-specified package name |
| `{{api_name}}` | OpenAPI `info.title` |
| `{{api_version}}` | OpenAPI `info.version` |