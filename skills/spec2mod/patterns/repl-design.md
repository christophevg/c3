# REPL Design with cmd + prompt_toolkit

## Overview

Build an interactive REPL shell using Python's `cmd` module for command handling and `prompt_toolkit` for advanced autocompletion and UX.

## Architecture

```
┌─────────────────────────────────────────┐
│              APIRepl (cmd.Cmd)          │
├─────────────────────────────────────────┤
│  - do_login()                           │
│  - do_get_user()                        │
│  - complete_login()                     │
│  - complete_get_user()                  │
└─────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│         CompletionProvider              │
│         (prompt_toolkit)                │
├─────────────────────────────────────────┤
│  - CommandCompleter                     │
│  - ParamCompleter                       │
│  - DocPreview                           │
└─────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│            APIClient                    │
└─────────────────────────────────────────┘
```

## Base REPL Class

```python
import cmd
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import FormattedText
from rich.console import Console
from rich.syntax import Syntax

class APIRepl(cmd.Cmd):
    """Interactive REPL for {api_name} API."""
    
    prompt = "{package_name}> "
    intro = "Welcome to {api_name} REPL. Type 'help' for commands, 'exit' to quit."
    
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.console = Console()
        self.session: PromptSession | None = None
    
    def _display(self, result):
        """Pretty-print result with rich."""
        if isinstance(result, dict) or isinstance(result, list):
            syntax = Syntax(str(result), "python", theme="monokai")
            self.console.print(syntax)
        else:
            self.console.print(result)
    
    def _parse_args(self, arg: str) -> dict:
        """Parse command arguments.
        
        Supports:
        - Positional args: login user pass
        - Named args: login --username user --password pass
        """
        # Simple positional parsing for now
        return {"args": arg.split()}
    
    # Override cmdloop to use prompt_toolkit
    def cmdloop(self, intro=None):
        """Enhanced REPL with prompt_toolkit."""
        from prompt_toolkit import PromptSession
        from prompt_toolkit.formatted_text import FormattedText
        
        self.session = PromptSession()
        if intro:
            print(intro)
        
        while True:
            try:
                line = self.session.prompt(self.prompt)
                line = line.strip()
                if not line:
                    continue
                if line in ('exit', 'quit', 'q'):
                    print("Goodbye!")
                    break
                self.precmd(line)
                self.onecmd(line)
                self.postcmd(False, line)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except EOFError:
                break
```

## Command Generation

Each client method becomes a command:

```python
def generate_repl_command(method_name: str, method_params: list) -> str:
    """Generate cmd.Cmd do_* method for a client method."""
    params_str = ", ".join(p.name for p in method_params)
    return f'''
    def do_{method_name}(self, arg):
        """{method_name}({params_str})
        
        {method_docstring}
        """
        try:
            args = self._parse_args(arg)
            result = self.client.{method_name}(**args)
            self._display(result)
        except Exception as e:
            self.console.print(f"[red]Error: {{e}}[/red]")
    
    def help_{method_name}(self):
        """Show help for {method_name}."""
        self.console.print(self.do_{method_name}.__doc__)
    '''
```

## Autocompletion

### Command Completer

```python
from prompt_toolkit.completion import Completer, Completion

class APICompleter(Completer):
    """Custom completer for API commands."""
    
    def __init__(self, commands: dict[str, str]):
        """
        Args:
            commands: Map of command_name -> docstring
        """
        self.commands = commands
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        
        # Complete command name
        if " " not in text:
            for cmd, doc in self.commands.items():
                if cmd.startswith(text):
                    # Show first line of doc as meta
                    first_line = doc.split("\n")[0] if doc else ""
                    yield Completion(
                        cmd,
                        start_position=-len(text),
                        display=cmd,
                        display_meta=first_line
                    )
```

### Parameter Completer

```python
class ParamCompleter(Completer):
    """Complete parameters for a specific command."""
    
    def __init__(self, params: list[str]):
        self.params = params
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        
        if len(words) < 2:
            return
        
        # Get current param being typed
        current = words[-1] if words else ""
        
        # Complete parameter names
        if current.startswith("--"):
            param_name = current[2:]
            for param in self.params:
                if param.startswith(param_name):
                    yield Completion(
                        f"--{param}",
                        start_position=-len(current),
                        display=f"--{param}"
                    )
```

## Entry Point Integration

```python
# __main__.py
import sys
from .client import APIClient
from .repl import APIRepl

def main():
    """Entry point: CLI or REPL mode."""
    import argparse
    
    parser = argparse.ArgumentParser(description="{api_name} API client")
    parser.add_argument("command", nargs="?", help="Command to execute")
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--base-url", default="{default_url}")
    
    args = parser.parse_args()
    
    client = APIClient(base_url=args.base_url)
    
    if args.command:
        # CLI mode: execute command and exit
        import subprocess
        result = getattr(client, args.command)(*args.args)
        print(result)
    else:
        # REPL mode: interactive shell
        repl = APIRepl(client)
        repl.cmdloop()

if __name__ == "__main__":
    main()
```

## Rich Integration

```python
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel

class APIRepl(cmd.Cmd):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.console = Console()
    
    def _display(self, result):
        """Pretty-print result."""
        if isinstance(result, list):
            self._display_table(result)
        elif isinstance(result, dict):
            self._display_dict(result)
        else:
            self.console.print(result)
    
    def _display_table(self, items: list):
        """Display list as table."""
        if not items:
            self.console.print("[dim]No results[/dim]")
            return
        
        table = Table(show_header=True)
        for key in items[0].keys():
            table.add_column(key)
        for item in items:
            table.add_row(*[str(v) for v in item.values()])
        self.console.print(table)
    
    def _display_dict(self, item: dict):
        """Display dict as formatted panel."""
        self.console.print(Panel(str(item), title="Result"))
```

## Best Practices

1. **Preserve docstrings** - `help command` shows full documentation
2. **Graceful error handling** - Show errors in red, don't crash
3. **History support** - prompt_toolkit provides arrow key history
4. **Tab completion** - Complete commands and parameters
5. **Pretty output** - Rich formatting for responses
6. **Exit gracefully** - Support `exit`, `quit`, `q`, Ctrl+D