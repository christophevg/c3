# Console API Reference

Rich Console class API reference.

## Constructor

```python
Console(
  file=None,           # Output file (default: sys.stdout)
  width=None,          # Force width (default: terminal width)
  height=None,         # Force height
  style=None,          # Default style
  no_color=False,      # Disable colors
  force_terminal=None, # Force terminal mode
  force_interactive=None,
  soft_wrap=False,
  theme=None,          # Theme instance
  highlighter=None,    # Highlighter instance
  log_time_format="[%X]",
  log_path=True
)
```

## Methods

### print()

```python
console.print(
  *objects,
  sep=' ',           # Separator
  end='\n',          # End character
  style=None,        # Default style
  justify=None,      # "left", "center", "right", "full"
  overflow=None,     # "ellipsis", "crop", "fold"
  no_wrap=None,      # Disable wrapping
  emoji=None,        # Enable emoji
  markup=None,       # Enable markup
  highlight=None,    # Enable highlighting
  width=None,        # Force width
  height=None,       # Force height
)
```

### log()

```python
console.log(
  *objects,
  _stack_offset=1,   # Stack offset for path
  _locals={},        # Local variables to show
  log_locals=False,  # Show all locals
  **kwargs,          # Passed to print()
)
```

### rule()

```python
console.rule(
  title="",
  *,
  characters="─",
  style="rule.line",
  align="center",
)
```

### status()

```python
with console.status(
  status,
  spinner="dots",
  spinner_style="status.spinner",
  speed=1.0,
) as status:
  status.update("New status")
```

### capture()

```python
with console.capture() as capture:
  console.print("Hello")
output = capture.get()
```

### print_exception()

```python
console.print_exception(
  show_locals=False,
  max_frames=100,
  width=None,
  extra_lines=3,
  suppress=[],
  word_wrap=False,
)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `width` | int | Console width |
| `height` | int | Console height |
| `size` | tuple | (width, height) |
| `is_terminal` | bool | True if terminal |
| `is_interactive` | bool | True if interactive |
| `encoding` | str | Output encoding |

## Control Methods

| Method | Description |
|--------|-------------|
| `clear(home=True)` | Clear screen |
| `clear_live()` | Clear live display |
| `bell()` | Terminal bell |
| `show_cursor(show=True)` | Show/hide cursor |
| `set_window_title(title)` | Set terminal title |

## Rendering Methods

| Method | Description |
|--------|-------------|
| `render(object)` | Render to renderable |
| `render_str(object)` | Render to string |
| `print_json(data)` | Pretty print JSON |
| `print_python(obj)` | Print Python repr |

## Example Usage

```python
from rich.console import Console
from rich.theme import Theme

# Basic
console = Console()
console.print("[bold]Hello[/]")

# With theme
theme = Theme({"error": "bold red"})
console = Console(theme=theme)
console.print("[error]Error![/]")

# Capture output
with console.capture() as capture:
  console.print("Test")
print(capture.get())

# Status animation
with console.status("Loading...", spinner="dots") as status:
  do_work()
  status.update("Still loading...")
```