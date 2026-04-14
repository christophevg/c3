# prompt_toolkit Reference

## Overview

`prompt_toolkit` is a library for building powerful interactive command lines in Python. Used by IPython, ptpython, and many other tools.

## Installation

```bash
pip install prompt_toolkit
```

## Core Concepts

### PromptSession

```python
from prompt_toolkit import PromptSession

session = PromptSession()
line = session.prompt("> ")
```

### Completers

```python
from prompt_toolkit.completion import Completer, Completion

class MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        # Yield completions
        yield Completion(
            "suggestion",
            start_position=-len(word),
            display="suggestion",
            display_meta="description"
        )
```

### History

```python
from prompt_toolkit.history import FileHistory

session = PromptSession(
    history=FileHistory("~/.myapp_history")
)
```

## Completion Types

### WordCompleter

```python
from prompt_toolkit.completion import WordCompleter

completer = WordCompleter(
    ["login", "logout", "get_user", "list_users"],
    ignore_case=True
)
```

### NestedCompleter

```python
from prompt_toolkit.completion import NestedCompleter

completer = NestedCompleter.from_nested_dict({
    "user": {
        "list": None,
        "get": None,
        "create": None,
    },
    "auth": {
        "login": None,
        "logout": None,
    },
})
```

### FuzzyCompleter

```python
from prompt_toolkit.completion import FuzzyCompleter

completer = FuzzyCompleter(WordCompleter(["login", "logout"]))
# "lgn" will match "login"
```

## Styling

### FormattedText

```python
from prompt_toolkit.formatted_text import FormattedText

prompt_text = FormattedText([
    ("class:prompt", "api> "),
])
line = session.prompt(prompt_text)
```

### Style

```python
from prompt_toolkit.styles import Style

style = Style.from_dict({
    "prompt": "ansicyan bold",
    "meta": "ansigray",
})
session = PromptSession(style=style)
```

## Key Bindings

```python
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()

@bindings.add("c-t")  # Ctrl+T
def _(event):
    """Do something on Ctrl+T."""
    event.app.current_buffer.insert_text("test")
```

## Validators

```python
from prompt_toolkit.validation import Validator, ValidationError

class NumberValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text.isdigit():
            raise ValidationError(message="Must be a number")

session = PromptSession(validator=NumberValidator())
```

## Auto-Suggestions

```python
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

session = PromptSession(
    auto_suggest=AutoSuggestFromHistory()
)
```

## Common Patterns

### REPL with Completion

```python
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory

commands = ["login", "logout", "get", "list", "help", "exit"]
completer = WordCompleter(commands)

session = PromptSession(
    history=FileHistory("~/.myapp_history"),
    completer=completer,
)

while True:
    try:
        line = session.prompt("myapp> ")
        if line.strip() == "exit":
            break
        # Process command
    except KeyboardInterrupt:
        continue
    except EOFError:
        break
```

### Dynamic Completion

```python
class DynamicCompleter(Completer):
    def __init__(self, client):
        self.client = client
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        
        if len(words) <= 1:
            # Complete command names
            for cmd in self.client._commands:
                if cmd.startswith(words[0] if words else ""):
                    yield Completion(cmd, start_position=-len(words[-1] if words else ""))
        else:
            # Complete parameters
            command = words[0]
            if hasattr(self.client, f"complete_{command}"):
                completer = getattr(self.client, f"complete_{command}")
                yield from completer(words[-1])
```

## Integration with rich

```python
from rich.console import Console
from prompt_toolkit import PromptSession

console = Console()
session = PromptSession()

while True:
    line = session.prompt("app> ")
    result = process(line)
    console.print(result)  # Rich output
```

## External References

- [prompt_toolkit Docs](https://python-prompt-toolkit.readthedocs.io/)
- [prompt_toolkit GitHub](https://github.com/prompt-toolkit/python-prompt-toolkit)
- [Examples](https://github.com/prompt-toolkit/python-prompt-toolkit/tree/master/examples)