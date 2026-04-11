# State Management Patterns

Textual reactive state patterns.

## Basic Reactive

```python
from textual.reactive import reactive

class MyWidget(Static):
  count = reactive(0)
  
  def increment(self):
    self.count += 1
```

## Watch Methods

```python
class MyWidget(Static):
  count = reactive(0)
  
  # One argument (new value only)
  def watch_count(self, new_count: int) -> None:
    self.update(f"Count: {new_count}")
  
  # Two arguments (old and new)
  def watch_count(self, old: int, new: int) -> None:
    if old != new:
      self.update(f"Count changed: {old} -> {new}")
```

## Compute Methods

```python
class MyWidget(Widget):
  red = reactive(0)
  green = reactive(0)
  blue = reactive(0)
  
  def compute_color(self) -> tuple[int, int, int]:
    return (self.red, self.green, self.blue)
  
  def watch_color(self, color: tuple) -> None:
    # Called when any of red, green, blue change
    self.styles.background = f"rgb({color[0]}, {color[1]}, {color[2]})"
```

## Validate Methods

```python
class MyWidget(Static):
  count = reactive(0)
  
  def validate_count(self, value: int) -> int:
    # Clamp to valid range
    if value < 0:
      return 0
    if value > 100:
      return 100
    return value
```

## Reactive Parameters

```python
class MyWidget(Static):
  # Full control
  name = reactive(
    default="default",
    layout=False,      # Perform layout on change
    repaint=True,      # Perform repaint on change
    init=True,         # Call watchers on mount
    always_update=False,  # Call watchers even if unchanged
    recompose=False,   # Re-run compose() on change
    bindings=False,    # Refresh bindings on change
  )
  
  # Non-refreshing reactive
  from textual.reactive import var
  counter = var(0)  # Doesn't trigger repaint
```

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `layout` | `False` | Perform layout on change |
| `repaint` | `True` | Perform repaint on change |
| `init` | `True` | Call watchers on mount |
| `always_update` | `False` | Call watchers even if unchanged |
| `recompose` | `False` | Re-run compose() on change |
| `bindings` | `False` | Refresh bindings on change |

## Data Binding (Parent to Child)

```python
class ParentApp(App):
  time = reactive(time.time)
  
  def compose(self):
    yield ChildWidget().data_bind(time=ParentApp.time)

class ChildWidget(Static):
  time = reactive(0.0)
  
  def watch_time(self, new_time: float):
    self.update(f"Time: {new_time}")
```

## Reactive with Callable Default

```python
import time

class MyWidget(Static):
  timestamp = reactive(time.time)  # Called on each access
  
  # Or use lambda
  items = reactive(list)  # New list each time
```

## Common Patterns

### Toggle

```python
class MyWidget(Static):
  active = reactive(False)
  
  def watch_active(self, active: bool):
    self.set_class(active, "active")
  
  def toggle(self):
    self.active = not self.active
```

### Counter

```python
class MyWidget(Static):
  count = reactive(0, layout=True)
  
  def increment(self):
    self.count += 1
  
  def reset(self):
    self.count = 0
```

### Selection

```python
class MyWidget(Static):
  selected_id = reactive(None)
  
  def watch_selected_id(self, old_id, new_id):
    # Deselect old
    if old_id:
      old_widget = self.query_one(f"#{old_id}")
      old_widget.remove_class("selected")
    
    # Select new
    if new_id:
      new_widget = self.query_one(f"#{new_id}")
      new_widget.add_class("selected")
```

### Loading State

```python
class MyScreen(Screen):
  loading = reactive(False)
  
  def watch_loading(self, loading: bool):
    self.query_one("#spinner").set_class(loading, "visible")
    self.query_one("#content").set_class(loading, "hidden")
  
  @work
  async def fetch_data(self):
    self.loading = True
    try:
      data = await api.fetch()
      self.update_display(data)
    finally:
      self.loading = False
```

## Execution Order

When a reactive attribute changes:

1. `compute_<attr>()` - Calculate derived value
2. `validate_<attr>()` - Validate and possibly modify
3. `watch_<attr>()` - React to change
4. UI update (if `repaint=True` or `layout=True`)

## var vs reactive

| Feature | `reactive()` | `var()` |
|---------|--------------|---------|
| Repaint on change | Yes (default) | No |
| Layout on change | Optional | No |
| Use case | UI state | Internal counters, flags |

```python
from textual.reactive import reactive, var

class MyWidget(Static):
  # UI state - triggers repaint
  text = reactive("")
  
  # Internal state - no repaint
  click_count = var(0)
```