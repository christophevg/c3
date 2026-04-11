# Components API Reference

Rich visual components API reference.

## Table

```python
from rich.table import Table
from rich.box import ROUNDED

table = Table(
  title="Title",           # Above table
  caption="Caption",        # Below table
  width=None,               # Fixed width
  box=ROUNDED,             # Box style
  padding=(0, 1),          # Cell padding
  expand=False,            # Fill terminal width
  show_header=True,
  show_footer=False,
  show_edge=True,
  show_lines=False,        # Lines between rows
  row_styles=None,         # Alternating row styles
  header_style="bold",
  border_style=None
)

# Add column
table.add_column(
  "Header",
  footer="Footer",
  style="cyan",
  justify="left",          # left, center, right
  vertical="top",          # top, middle, bottom
  overflow="ellipsis",     # ellipsis, crop, fold
  width=None,
  ratio=None,              # Flex ratio
  no_wrap=False
)

# Add row
table.add_row("A", "B", "C", style=None, end_section=False)
```

## Panel

```python
from rich.panel import Panel
from rich.box import ROUNDED

panel = Panel(
  "Content",
  title="Title",
  subtitle="Subtitle",
  box=ROUNDED,
  expand=True,
  style="none",            # Border and content
  border_style="none",     # Border only
  padding=(0, 1),
  width=None,
  height=None
)

# Fit to content
Panel.fit("Content", title="Title")
```

## Progress

```python
from rich.progress import Progress, track

# Simple
for item in track(items, description="Processing..."):
  process(item)

# Advanced
progress = Progress(
  *columns,                    # Column objects
  console=None,
  auto_refresh=True,
  refresh_per_second=10,
  transient=False,            # Clear on finish
  disable=False,
  expand=False
)

task = progress.add_task(
  "Description",
  total=100,
  completed=0,
)

progress.update(task, advance=10)
progress.update(task, completed=50)
```

### Column Types

```python
from rich.progress import (
  SpinnerColumn,
  TextColumn,
  BarColumn,
  TaskProgressColumn,
  TimeElapsedColumn,
  TimeRemainingColumn,
  FileSizeColumn,
  DownloadColumn,
  TransferSpeedColumn,
  MofNCompleteColumn,
)

SpinnerColumn(spinner_name="dots")
TextColumn("[progress.description]{task.description}")
BarColumn(bar_width=None, complete_style="green")
TaskProgressColumn()
TimeElapsedColumn()
TimeRemainingColumn()
```

## Layout

```python
from rich.layout import Layout

layout = Layout()
layout.split_column(
  Layout(Panel("Top"), name="top", size=10),
  Layout(Panel("Bottom"), name="bottom")
)

# Access by name
layout["top"].update(Panel("Updated"))

# Split further
layout["bottom"].split_row(
  Layout(Panel("Left"), name="left"),
  Layout(Panel("Right"), name="right")
)
```

## Columns

```python
from rich.columns import Columns

columns = Columns(
  ["A", "B", "C"],
  padding=(0, 1),
  width=None,          # Fixed width
  expand=False,
  equal=False,         # Equal columns
  column_first=False,  # Fill top-to-bottom
  align="left"
)
```

## Tree

```python
from rich.tree import Tree

tree = Tree("Root", guide_style="blue")
tree.add("Child 1").add("Grandchild")
tree.add("Child 2")

# Hide root
tree = Tree("Root", hide_root=True)
```

## Syntax

```python
from rich.syntax import Syntax

syntax = Syntax(
  code,
  "python",
  theme="monokai",
  line_numbers=True,
  line_range=(1, 10),
  word_wrap=False,
  background_color=None,
  indent_guides=False
)

# From file
Syntax.from_path("file.py", theme="monokai")
```

## Markdown

```python
from rich.markdown import Markdown

md = Markdown(
  markdown_text,
  code_theme="monokai",
  hyperlinks=True,
  inline_code_lexer=None,
  inline_code_theme=None
)
```

## Live

```python
from rich.live import Live

with Live(
  renderable,
  refresh_per_second=4,
  console=None,
  transient=False,        # Clear on exit
  screen=False,           # Alternate screen buffer
  auto_refresh=True,
  redirect_stdout=True,
  redirect_stderr=True
) as live:
  live.update(new_renderable)
```

## Text

```python
from rich.text import Text

text = Text("Hello", style="bold red")
text.append(" World", style="italic")
text.stylize("underline", 0, 5)

# From markup
text = Text.from_markup("[bold]Hello[/]")

# Assemble
text = Text.assemble(
  ("Hello", "bold cyan"),
  (" ", None),
  ("World", "magenta")
)

# Properties
text.plain        # Plain string
text.cell_len     # Terminal cells
```

## Style

```python
from rich.style import Style

style = Style(
  color="red",
  bgcolor="black",
  bold=True,
  italic=False,
  underline=False,
  dim=False,
  strike=False,
  link="https://..."
)

# Parse
style = Style.parse("bold red on black")

# Combine
combined = style1 + style2
```