# Progress Patterns

Rich progress bar and spinner patterns.

## Simple Progress (track)

```python
from rich.progress import track

for item in track(items, description="Processing..."):
  process(item)
```

## Advanced Progress (Progress)

```python
from rich.progress import Progress

with Progress() as progress:
  task = progress.add_task("Processing", total=len(items))
  
  for item in items:
    process(item)
    progress.update(task, advance=1)
```

## Multi-Task Progress

```python
from rich.progress import Progress

with Progress() as progress:
  download = progress.add_task("[red]Downloading", total=1000)
  process = progress.add_task("[green]Processing", total=1000)
  
  while not progress.finished:
    # Update independently
    progress.update(download, advance=10)
    progress.update(process, advance=5)
```

## Progress Columns

```python
from rich.progress import (
  Progress,
  SpinnerColumn,
  BarColumn,
  TextColumn,
  TimeElapsedColumn,
  TimeRemainingColumn,
  TaskProgressColumn,
)

progress = Progress(
  SpinnerColumn(),
  TextColumn("[progress.description]{task.description}"),
  BarColumn(),
  TaskProgressColumn(),
  TimeElapsedColumn(),
  TimeRemainingColumn(),
)
```

## Built-in Columns

| Column | Description |
|--------|-------------|
| `SpinnerColumn` | Animated spinner |
| `TextColumn` | Formatted text |
| `BarColumn` | Progress bar |
| `TaskProgressColumn` | Percentage (N%) |
| `TimeElapsedColumn` | Elapsed time |
| `TimeRemainingColumn` | ETA |
| `FileSizeColumn` | File size |
| `DownloadColumn` | Download progress |
| `TransferSpeedColumn` | Speed |
| `MofNCompleteColumn` | N/M counter |

## Indeterminate Progress

```python
# No total = indeterminate
task = progress.add_task("Connecting...", total=None)
# ... later
progress.update(task, total=100, completed=50)  # Now determinate
```

## Spinner Patterns

```python
# Status spinner (simple)
with console.status("[bold green]Loading...", spinner="dots"):
  do_work()

# Progress with spinner column
progress = Progress(SpinnerColumn(), TextColumn("{task.description}"))
```

**Spinner Names**: `dots`, `earth`, `clock`, `moon`, `runner`, `pong`, `arrow`, `line`, `star`, `toggle`

## Live Progress Display

```python
from rich.live import Live
from rich.progress import Progress

progress = Progress()
task = progress.add_task("Working", total=100)

with Live(progress, refresh_per_second=4):
  for i in range(100):
    time.sleep(0.05)
    progress.update(task, completed=i + 1)
```

## Progress with Table

```python
from rich.progress import Progress
from rich.table import Table

progress = Progress(expand=True)

# Create layout
table = Table.grid()
table.add_row(progress)
table.add_row("Status: Running")

with Live(table):
  # ...
```

## Download Progress

```python
from rich.progress import Progress, DownloadColumn, TransferSpeedColumn

with Progress(
  "[progress.description]{task.description}",
  DownloadColumn(),
  TransferSpeedColumn(),
) as progress:
  task = progress.add_task("download.zip", total=file_size)
  # Update with bytes downloaded
  progress.update(task, advance=chunk_size)
```

## Transient Progress (Disappear on Complete)

```python
with Progress(transient=True) as progress:
  task = progress.add_task("Processing", total=100)
  # Progress bar disappears after completion
```

## Common Patterns

| Pattern | Use Case |
|---------|----------|
| `track()` | Simple iteration |
| `Progress()` | Multi-task, custom columns |
| `transient=True` | Hide after completion |
| `spinner=` | Indeterminate tasks |
| `refresh_per_second` | Control refresh rate (default: 10) |
| `advance=` | Increment by amount |
| `completed=` | Set absolute value |

## Performance Tips

- Lower `refresh_per_second` for faster operations (default: 10)
- Use `transient=True` to clear progress after completion
- Batch updates instead of per-item for large datasets