# Logging Patterns

Rich logging patterns using RichHandler.

## Basic RichHandler Setup

Configure in entry points only (`__main__.py`), never in importable modules.

```python
# __main__.py
import logging
from rich.logging import RichHandler

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
```

## RichHandler Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `show_time` | `True` | Display timestamp |
| `show_level` | `True` | Display log level |
| `show_path` | `True` | Display file path and line |
| `markup` | `False` | Enable Rich markup in messages |
| `rich_tracebacks` | `False` | Enable rich traceback formatting |
| `tracebacks_show_locals` | `False` | Show local variables in tracebacks |
| `tracebacks_suppress` | `[]` | Modules to suppress in tracebacks |
| `log_time_format` | `"[%X]"` | Time format string |

## Patterns

### Minimal Logging

```python
logging.basicConfig(
  level="INFO",
  format="%(message)s",
  handlers=[RichHandler(show_path=False)]
)
```

### Development Logging (Full Details)

```python
logging.basicConfig(
  level="DEBUG",
  format="%(message)s",
  handlers=[
    RichHandler(
      show_time=True,
      show_level=True,
      show_path=True,
      markup=True,
      rich_tracebacks=True,
      tracebacks_show_locals=True,
    )
  ]
)
```

### Production Logging (Minimal)

```python
logging.basicConfig(
  level="INFO",
  format="%(message)s",
  handlers=[
    RichHandler(
      show_time=True,
      show_level=True,
      show_path=False,
      rich_tracebacks=False,
    )
  ]
)
```

### Suppressing Third-Party Tracebacks

```python
import click

logging.basicConfig(
  handlers=[
    RichHandler(
      rich_tracebacks=True,
      tracebacks_suppress=[click],
    )
  ]
)
```

## Global Traceback Installation

Install Rich traceback handler globally (separate from logging):

```python
from rich.traceback import install

install(
  show_locals=True,
  max_frames=100,
  extra_lines=3,
)
```

## Console.log for Quick Debugging

```python
from rich.console import Console

console = Console()

# With local variables
console.log("Debug info", log_locals=True)

# Regular log
console.log("Processing", item, status="done")
```

## Integration with Other Libraries

### Typer

```python
import typer
from rich.logging import RichHandler
import logging

logging.basicConfig(handlers=[RichHandler()])

app = typer.Typer()

@app.command()
def command():
  log = logging.getLogger(__name__)
  log.info("Command executed")
```

### argparse

Use `rich-argparse` for styled help output:

```python
from rich_argparse import RichHelpFormatter

parser = argparse.ArgumentParser(
  formatter_class=RichHelpFormatter
)
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| RichHandler in library | Affects all users | Only in entry points |
| Multiple basicConfig calls | Only first applies | Configure once at startup |
| format with rich_tracebacks | Format ignored for tracebacks | Use default format |