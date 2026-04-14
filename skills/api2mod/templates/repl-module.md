# REPL Module Template

## repl.py

```python
"""Interactive REPL for {{api_name}} API."""

import cmd
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel

from .client import {{client_class_name}}


class APICompleter(Completer):
    """Completer for API commands."""
    
    def __init__(self, commands: dict[str, str]):
        self.commands = commands
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        word = document.get_word_before_cursor()
        
        # Complete command name
        if " " not in text:
            for cmd, doc in self.commands.items():
                if cmd.startswith(word):
                    first_line = doc.split("\n")[0] if doc else ""
                    yield Completion(
                        cmd,
                        start_position=-len(word),
                        display=cmd,
                        display_meta=first_line[:50]
                    )


class {{repl_class_name}}(cmd.Cmd):
    """Interactive REPL for {{api_name}} API.
    
    Commands:
    {{#each commands}}
        {{name}} - {{summary}}
    {{/each}}
    
    Special commands:
        help <command> - Show command documentation
        exit          - Exit the REPL
    """
    
    prompt = "{{package_name}}> "
    intro = """Welcome to {{api_name}} REPL.
    
Type 'help' for available commands, 'help <command>' for details.
Press Tab for autocompletion. Type 'exit' to quit.
"""
    
    def __init__(self, client: {{client_class_name}}):
        super().__init__()
        self.client = client
        self.console = Console()
        self.session: PromptSession | None = None
        self._setup_completer()
    
    def _setup_completer(self):
        """Set up command completer."""
        self._commands = {
            {{#each commands}}
            "{{name}}": """{{summary}}

{{detailed_help}}
""",
            {{/each}}
        }
        self._completer = APICompleter(self._commands)
    
    def _display(self, result: Any) -> None:
        """Pretty-print result with rich."""
        if result is None:
            self.console.print("[dim]Done[/dim]")
            return
        
        if isinstance(result, list):
            self._display_list(result)
        elif isinstance(result, dict):
            self._display_dict(result)
        else:
            self.console.print(result)
    
    def _display_list(self, items: list) -> None:
        """Display list as table."""
        if not items:
            self.console.print("[dim]No results[/dim]")
            return
        
        # Use first item to determine columns
        if isinstance(items[0], dict):
            table = Table(show_header=True, header_style="bold")
            for key in items[0].keys():
                table.add_column(key)
            for item in items:
                table.add_row(*[str(v) for v in item.values()])
            self.console.print(table)
        else:
            for item in items:
                self.console.print(f"  • {item}")
    
    def _display_dict(self, item: dict) -> None:
        """Display dict as formatted output."""
        self.console.print(Panel(str(item), title="Result", expand=False))
    
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
        )
        
        if intro:
            self.console.print(intro)
        
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
        try:
            args = self._parse_args("{{name}}", arg)
            result = self.client.{{name}}(**args)
            self._display(result)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def help_{{name}}(self) -> None:
        """Show help for {{name}}."""
        self.console.print(Panel(self.do_{{name}}.__doc__, title="{{name}}"))
    {{/each}}
    
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
    
    args = parser.parse_args()
    
    # Create client
    if getattr(args, "async"):
        import asyncio
        client = Async{{client_class_name}}(base_url=args.base_url)
    else:
        client = {{client_class_name}}(base_url=args.base_url)
    
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
|----------|--------|
| `{{repl_class_name}}` | Derived from package name (e.g., `PetStoreRepl`) |
| `{{commands}}` | Generated from client methods |
| `{{package_name}}` | User-specified package name |