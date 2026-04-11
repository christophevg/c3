# Console Setup Template

Global Console instance setup pattern.

## Basic Setup

```python
# utils/console.py
from rich.console import Console

# Single global instance
console = Console()
```

## Themed Console

```python
# utils/console.py
from rich.console import Console
from rich.theme import Theme

# Custom theme
theme = Theme({
  "info": "cyan",
  "warning": "yellow",
  "error": "bold red",
  "success": "bold green",
  "header": "bold blue",
  "key": "cyan",
  "value": "green",
})

console = Console(theme=theme)

# Usage
console.print("[info]Information message[/]")
console.print("[error]Error message[/]")
console.print("[success]Success![/]")
```

## No-Highlight Console

```python
# For performance or specific use cases
console = Console(highlight=False)
```

## File Output Console

```python
from rich.console import Console

# Output to file
file_console = Console(file=open("output.txt", "w"))

# Or with context manager
with open("output.txt", "w") as f:
  console = Console(file=f)
  console.print("Output to file")
```

## Import Pattern

```python
# In application code
from utils.console import console

def main():
  console.print("[bold]Starting application[/]")
```

## Entry Point Pattern

```python
# __main__.py
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme

# Setup theme
theme = Theme({
  "info": "cyan",
  "warning": "yellow",
  "error": "bold red",
  "success": "bold green",
})

# Global console
console = Console(theme=theme)

# Logging
logging.basicConfig(
  level="INFO",
  format="%(message)s",
  handlers=[
    RichHandler(
      show_time=True,
      show_level=True,
      show_path=True,
      rich_tracebacks=True,
    )
  ]
)

log = logging.getLogger(__name__)

def main():
  console.print("[header]Application Starting[/header]")
  log.info("Application initialized")
  
if __name__ == "__main__":
  main()
```

## Module Pattern

```
myapp/
├── __main__.py      # Entry point, logging setup
├── utils/
│   └── console.py   # Global console instance
└── services/
    └── processor.py # Import and use console
```

```python
# utils/console.py
from rich.console import Console
from rich.theme import Theme

theme = Theme({
  "info": "cyan",
  "warning": "yellow", 
  "error": "bold red",
  "success": "bold green",
})

console = Console(theme=theme)
```

```python
# services/processor.py
from utils.console import console

def process():
  console.print("[info]Processing...[/]")
  console.print("[success]Done![/]")
```