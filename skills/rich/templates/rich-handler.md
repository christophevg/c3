# RichHandler Template

RichHandler configuration templates.

## Development Setup

```python
# __main__.py
import logging
from rich.logging import RichHandler

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
      log_time_format="[%Y-%m-%d %H:%M:%S]",
    )
  ]
)

log = logging.getLogger(__name__)
```

## Production Setup

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
      show_path=False,
      rich_tracebacks=False,
    )
  ]
)
```

## CLI Application Setup

```python
# cli/__main__.py
import logging
from rich.logging import RichHandler
import sys

# Determine log level from args
level = "DEBUG" if "--debug" in sys.argv else "INFO"

logging.basicConfig(
  level=level,
  format="%(message)s",
  handlers=[
    RichHandler(
      show_time=False,
      show_level=True,
      show_path=level == "DEBUG",
      rich_tracebacks=True,
      tracebacks_show_locals=level == "DEBUG",
    )
  ]
)
```

## Flask Application Setup

```python
# app/logging_config.py
import logging
from rich.logging import RichHandler

def setup_logging(app):
  """Setup logging for Flask application."""
  logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
      RichHandler(
        show_time=True,
        show_level=True,
        show_path=False,
        rich_tracebacks=True,
      )
    ]
  )
  
  # Set werkzeug logger
  logging.getLogger("werkzeug").setLevel(logging.WARNING)

# In app factory or __init__.py
from app.logging_config import setup_logging
setup_logging(app)
```

## Typer Application Setup

```python
# cli/__main__.py
import typer
from rich.logging import RichHandler
import logging

def setup_logging(verbose: bool = False):
  level = "DEBUG" if verbose else "INFO"
  logging.basicConfig(
    level=level,
    format="%(message)s",
    handlers=[
      RichHandler(
        show_time=False,
        show_level=True,
        show_path=verbose,
        rich_tracebacks=True,
      )
    ]
  )

app = typer.Typer()

@app.callback()
def main(verbose: bool = False):
  """CLI application."""
  setup_logging(verbose)

@app.command()
def command():
  log = logging.getLogger(__name__)
  log.info("Command executed")
```

## Library Pattern (No Global Setup)

```python
# library code - DO NOT configure logging
import logging

log = logging.getLogger(__name__)

def process():
  log.debug("Processing...")
  log.info("Complete")
```

```python
# application entry point - configure logging
import logging
from rich.logging import RichHandler

logging.basicConfig(
  handlers=[RichHandler(rich_tracebacks=True)]
)

from mylib import process  # Library uses configured logging

if __name__ == "__main__":
  process()
```

## Anti-Patterns to Avoid

```python
# WRONG: Configure logging in library module
# mylib/__init__.py
logging.basicConfig(...)  # Never do this!

# CORRECT: Library just uses getLogger
log = logging.getLogger(__name__)
```

```python
# WRONG: Multiple basicConfig calls
logging.basicConfig(level="DEBUG")  # First call
logging.basicConfig(level="INFO")   # Ignored!

# CORRECT: Configure once at startup
if __name__ == "__main__":
  logging.basicConfig(level="INFO")
```