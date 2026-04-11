---
name: rich
description: Guide Python Rich library usage for terminal output with styled text, tables, progress bars, and logging. Use when user mentions rich, console output, terminal formatting, progress bars, or code imports rich. Default choice for Python console applications.
---

# Rich

Guide Python's Rich library for rich terminal output including styled text, tables, progress bars, logging, and live displays. Rich is the default choice for Python applications requiring enhanced console output.

## Overview

| Capability | Description |
|------------|-------------|
| Console Output | Styled text with colors, bold, italic, etc. |
| Tables | Data tables with customizable columns, rows, borders |
| Progress Bars | Multi-task progress with spinners, ETA, percentage |
| Logging | RichHandler for beautiful log output |
| Live Displays | Real-time updates with Live and Status |
| Syntax Highlighting | Code highlighting with Pygments themes |
| Panels & Layouts | Bordered panels and split layouts |

## When to Use This Skill

Use this skill when:
- User mentions "rich", "console output", "terminal formatting"
- Code imports `rich` or `from rich import`
- User asks about progress bars, tables, styled logging
- Building CLI tools with enhanced output

Ask clarification when:
- User asks about "terminal UI" or "TUI" (could be Rich or Textual)
- Uncertain if interactive TUI is needed vs. enhanced output

## Console Class

The `Console` class is the core of Rich. Use one global instance.

```python
from rich.console import Console

console = Console()

# Basic output
console.print("[bold red]Error:[/] Something happened")
console.log("Processing complete")

# Rule/separator
console.rule("[bold blue]Section Title")
```

### Markup Syntax

Rich uses BBCode-style markup:

```python
# Basic styles
console.print("[bold]Bold[/]")
console.print("[italic red]Red italic[/]")
console.print("[bold yellow on blue]Styled background[/]")

# Links
console.print("[link=https://example.com]Click here[/link]")

# Shorthand: b=bold, i=italic, u=underline, d=dim, s=strike
console.print("[b]bold[/], [i]italic[/]")
```

### Style Attributes

- **Colors**: `red`, `blue`, `green`, `yellow`, `cyan`, `magenta`, `white`, `black`
- **Bright**: `bright_red`, `bright_blue`, etc.
- **Attributes**: `bold`, `italic`, `underline`, `dim`, `strike`, `blink`, `reverse`
- **Background**: `on red`, `on blue`

## Logging Setup

Configure RichHandler in entry points only (`__main__.py`), never in importable modules.

```python
# __main__.py or entry point
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
      tracebacks_show_locals=True,
    )
  ]
)
```

See `patterns/logging.md` for detailed patterns.

## Tables

```python
from rich.table import Table
from rich.box import ROUNDED, HEAVY_HEAD

table = Table(
  title="Results",
  box=ROUNDED,
  show_header=True,
  header_style="bold cyan",
)

table.add_column("Name", style="green")
table.add_column("Value", justify="right")
table.add_column("Status", style="bold")

table.add_row("Item 1", "100", "[green]OK[/]")
table.add_row("Item 2", "200", "[yellow]WARN[/]")

console.print(table)
```

See `patterns/tables.md` for detailed patterns.

## Progress Bars

### Simple (track)

```python
from rich.progress import track

for item in track(items, description="Processing..."):
  process(item)
```

### Advanced (Progress)

```python
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

with Progress(
  SpinnerColumn(),
  TextColumn("[progress.description]{task.description}"),
  BarColumn(),
  TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
) as progress:
  task = progress.add_task("[red]Downloading...", total=1000)
  
  while not progress.finished:
    progress.update(task, advance=10)
```

See `patterns/progress.md` for detailed patterns.

## Panels and Layouts

### Panels

```python
from rich.panel import Panel

panel = Panel(
  "Content here",
  title="Title",
  subtitle="Subtitle",
  border_style="blue",
)
console.print(panel)
```

### Layouts

```python
from rich.layout import Layout

layout = Layout()
layout.split_column(
  Layout(name="header", size=3),
  Layout(name="body"),
  Layout(name="footer", size=3),
)

layout["header"].update(Panel("Header"))
layout["body"].update(Panel("Content"))
layout["footer"].update(Panel("Footer"))

console.print(layout)
```

## Live Displays

```python
from rich.live import Live
from rich.table import Table

def generate_table():
  table = Table(title="Live Data")
  table.add_column("Time")
  table.add_column("Value")
  # ... add rows
  return table

with Live(generate_table(), refresh_per_second=4) as live:
  for _ in range(100):
    time.sleep(0.1)
    live.update(generate_table())
```

## Syntax Highlighting

```python
from rich.syntax import Syntax

syntax = Syntax(
  code_string,
  "python",
  theme="monokai",
  line_numbers=True,
)
console.print(syntax)

# From file
syntax = Syntax.from_path("script.py", theme="github-dark")
```

**Popular themes**: `monokai`, `github-dark`, `dracula`, `vim`

## Markdown Rendering

```python
from rich.markdown import Markdown

md = Markdown("""
# Heading
- Item 1
- Item 2
""")
console.print(md)
```

## Trees

```python
from rich.tree import Tree

tree = Tree("[bold blue]Root")
tree.add("[green]Child 1").add("[yellow]Grandchild")
tree.add("[green]Child 2")
console.print(tree)
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Output too slow | Batch output, use `Console(highlight=False)` |
| Colors not showing | Check terminal supports ANSI, avoid `no_color=True` |
| Progress bar flickers | Reduce `refresh_per_second` (default: 10) |
| Exception not formatted | Call `rich.traceback.install()` at startup |
| Piped output breaks | Use `force_terminal=False` or check `console.is_terminal` |

## Performance Tips

- Rich tables are ~18x slower than plain output
- Batch output instead of tight loops
- Use `transient=True` for progress bars
- Disable features: `console = Console(highlight=False)`

## When to Use Rich vs Textual

| Use Rich When | Use Textual When |
|---------------|------------------|
| Simple CLI output | Interactive TUI application |
| Progress bars, tables | Forms, input handling |
| Logging with styling | Event-driven interfaces |
| One-shot display | Persistent dashboard |

## Pattern Files

- `patterns/logging.md` - Logging setup patterns
- `patterns/tables.md` - Table creation patterns
- `patterns/progress.md` - Progress bar patterns

## Template Files

- `templates/console-setup.md` - Global console setup
- `templates/rich-handler.md` - RichHandler configuration

## Reference Files

- `references/api-console.md` - Console class API
- `references/api-components.md` - Component APIs

## Related Skills

- python - Base skill for Python development
- textual - TUI applications (when Rich is insufficient)