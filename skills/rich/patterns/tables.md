# Table Patterns

Rich table creation patterns.

## Basic Table

```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Data")
table.add_column("Name", style="cyan")
table.add_column("Value", justify="right")
table.add_column("Status")

table.add_row("Item 1", "100", "[green]OK")
table.add_row("Item 2", "200", "[yellow]WARN")
table.add_row("Item 3", "300", "[red]ERROR")

console.print(table)
```

## Table Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | str | Title above table |
| `caption` | str | Caption below table |
| `box` | Box | Border style (ROUNDED, SQUARE, etc.) |
| `show_header` | bool | Show header row |
| `show_footer` | bool | Show footer row |
| `show_edge` | bool | Show left/right edges |
| `show_lines` | bool | Lines between rows |
| `expand` | bool | Fill terminal width |
| `padding` | tuple | Cell padding |
| `row_styles` | list | Alternating row styles |

## Box Styles

```python
from rich.box import (
  ROUNDED,    # ╭──╮
  SQUARE,     # ┌──┐
  MINIMAL,    # ────
  SIMPLE,     # no border
  SIMPLE_HEAD, # header only
  HEAVY,      # ┏━━┓
  DOUBLE,     # ╔══╗
  ASCII,      # +--+
)

table = Table(box=HEAVY)
```

## Column Configuration

```python
table.add_column(
  "Name",
  style="cyan",
  justify="left",      # left, center, right
  vertical="middle",   # top, middle, bottom
  width=20,            # Fixed width
  ratio=2,             # Flex ratio
  no_wrap=False,       # Prevent wrapping
  footer="Total",      # Footer cell
)
```

## Alternating Row Colors

```python
table = Table(
  row_styles=["none", "dim"],
)
```

## Footer Row

```python
table = Table(show_footer=True)
table.add_column("Item", footer="Total")
table.add_column("Price", footer="$600", justify="right")
```

## Data Table Pattern

```python
def create_data_table(data: list[dict]) -> Table:
  """Create table from list of dictionaries."""
  if not data:
    return Table("No data")
  
  table = Table(box=ROUNDED, expand=True)
  
  # Add columns from first row keys
  for key in data[0].keys():
    table.add_column(key.title(), style="cyan")
  
  # Add rows
  for row in data:
    table.add_row(*[str(v) for v in row.values()])
  
  return table

# Usage
data = [
  {"name": "Alice", "age": 30, "city": "NYC"},
  {"name": "Bob", "age": 25, "city": "LA"},
]
console.print(create_data_table(data))
```

## Compact Table

```python
table = Table(
  box=SIMPLE_HEAD,
  padding=(0, 1),
  show_edge=False,
)
```

## Wide Table with Horizontal Scroll

```python
table = Table(expand=True)  # Use full terminal width
# Rich auto-wraps content; for scrolling, use pager:
console.print(table, soft_wrap=False)
```

## Sectioned Table

```python
table = Table(title="Results", show_lines=True)

table.add_column("Category")
table.add_column("Item")
table.add_column("Status")

# Section 1
table.add_row("[bold]Section A[/]", "", "")
table.add_row("", "Item 1", "OK")
table.add_row("", "Item 2", "OK")

# Section 2
table.add_row("[bold]Section B[/]", "", "")
table.add_row("", "Item 3", "WARN")
```

## Common Patterns

| Pattern | Description |
|---------|-------------|
| `expand=True` | Fill terminal width |
| `box=SIMPLE_HEAD` | Header border only |
| `row_styles=["none", "dim"]` | Zebra striping |
| `justify="right"` | Right-align numbers |
| `footer=` | Add footer row |
| `show_lines=True` | Row separators |