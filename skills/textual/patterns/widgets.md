# Widget Patterns

Common Textual widget patterns.

## Input Widget

```python
from textual.widgets import Input

# Basic
yield Input(placeholder="Enter text")

# With validation
from textual.validators import Integer

yield Input(
  placeholder="Age",
  validators=[Integer(minimum=0, maximum=120)],
)

# Handle changes
def on_input_changed(self, event: Input.Changed):
  self.value = event.value

# Handle submit
def on_input_submitted(self, event: Input.Submitted):
  self.process(event.value)
```

## Button Widget

```python
from textual.widgets import Button

# Basic
yield Button("Click Me")

# With variant
yield Button("Save", variant="primary")
# variants: default, primary, success, warning, error

# Handle press
def on_button_pressed(self, event: Button.Pressed):
  if event.button.id == "save":
    self.save()
```

## DataTable Widget

```python
from textual.widgets import DataTable

def on_mount(self):
  table = self.query_one(DataTable)
  table.add_columns("Name", "Age", "City")
  table.add_row("Alice", 30, "NYC")
  table.add_row("Bob", 25, "LA")

# With cursor type
table.cursor_type = "row"  # cell, row, column, none

# Zebra striping
table.zebra_stripes = True

# Fixed columns
table.fixed_columns = 1
```

## ListView Widget

```python
from textual.widgets import ListView, ListItem, Label

yield ListView(
  ListItem(Label("Item 1")),
  ListItem(Label("Item 2")),
  ListItem(Label("Item 3")),
)

# Handle selection
def on_list_view_selected(self, event: ListView.Selected):
  item = event.item
  label = item.query_one(Label)
  print(f"Selected: {label.renderable}")
```

## Select Widget

```python
from textual.widgets import Select

yield Select(
  [
    ("Option 1", "value1"),
    ("Option 2", "value2"),
    ("Option 3", "value3"),
  ],
  allow_blank=True,
)

# Handle change
def on_select_changed(self, event: Select.Changed):
  print(f"Selected: {event.value}")
```

## TabbedContent Widget

```python
from textual.widgets import TabbedContent, TabPane

with TabbedContent():
  with TabPane("General"):
    yield Static("General settings")
  with TabPane("Advanced"):
    yield Static("Advanced settings")

# Programmatic tab switch
tabs = self.query_one(TabbedContent)
tabs.active = "advanced"  # TabPane id
```

## Tree Widget

```python
from textual.widgets import Tree

tree: Tree[str] = Tree("Root")
tree.root.add("Child 1").add("Grandchild")
tree.root.add("Child 2")
tree.root.expand()

# Handle selection
def on_tree_node_selected(self, event: Tree.NodeSelected):
  print(f"Selected: {event.node.data}")
```

## TextArea Widget

```python
from textual.widgets import TextArea

# Basic
yield TextArea("Initial text")

# Code editor with syntax highlighting
yield TextArea.code_editor(
  "def hello():\n    pass",
  language="python"
)

# Handle change
def on_text_area_changed(self, event: TextArea.Changed):
  text = event.text_area.text
```

### Extending TextArea

Common patterns for extending TextArea:

```python
from textual.widgets import TextArea
from textual.geometry import Size
from textual.widgets.text_area import Selection

class CustomTextArea(TextArea):
  DEFAULT_CSS = """
  CustomTextArea {
    height: auto;  /* Auto-height */
    min-height: 1;
  }
  """
  
  BINDINGS = [
    ("f7", "select_all", "Select all"),
    ("ctrl+shift+a", "select_all", "Select all"),
  ]
  
  def __init__(self, max_height: int = 10, **kwargs):
    self._max_height = max_height
    super().__init__(**kwargs)
  
  def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
    """Override for auto-height based on content."""
    lines = self.wrapped_document.height  # Visual lines after soft wrap
    return max(1, min(lines, self._max_height))
```

### TextArea Key Bindings

| Binding | Action | Notes |
|---------|--------|-------|
| Arrow keys | `cursor_up/down/left/right` | Move cursor |
| Ctrl+← / Ctrl+→ | `cursor_word_left/right` | Word movement |
| Home / Ctrl+A | `cursor_line_start` | NOT select all! |
| End / Ctrl+E | `cursor_line_end` | End of line |
| F7 | `select_all` | Select all text |
| F6 | `select_line` | Select current line |
| Shift+arrows | `cursor_*(select=True)` | Extend selection |
| Ctrl+C | `copy` | Copy to clipboard |
| Ctrl+V | `paste` | Paste from clipboard |
| Ctrl+X | `cut` | Cut to clipboard |
| Ctrl+Z | `undo` | Undo last edit |
| Ctrl+Y | `redo` | Redo last undone edit |

### TextArea Properties

| Property | Type | Description |
|----------|------|-------------|
| `text` | `str` | Get/set full text content |
| `cursor_location` | `tuple[int, int]` | (row, col) cursor position |
| `selection` | `Selection` | Current selection |
| `selected_text` | `str` | Selected text string |
| `wrapped_document.height` | `int` | Visual lines (after soft wrap) |
| `document` | `Document` | Underlying document |
| `read_only` | `bool` | Read-only mode |

### Selection Handling

```python
from textual.widgets.text_area import Selection

# Get current selection
sel = text_area.selection  # Selection(start=(row, col), end=(row, col))
text = text_area.selected_text  # Selected string

# Set selection programmatically
text_area.selection = Selection((0, 0), (0, 5))  # Select first 5 chars

# Select all
text_area.select_all()

# Clear selection (move cursor)
text_area.cursor_location = (0, 0)
```

### Cursor Movement with Selection

```python
# Basic movement (no selection)
text_area.action_cursor_right()
text_area.action_cursor_left()
text_area.action_cursor_up()
text_area.action_cursor_down()

# Movement with selection
text_area.action_cursor_right(select=True)
text_area.action_cursor_left(select=True)

# Word movement
text_area.action_cursor_word_right()
text_area.action_cursor_word_left()

# Line start/end
text_area.action_cursor_line_start()
text_area.action_cursor_line_end()
```

### Auto-Height Pattern

For widgets that grow with content:

```python
class AutoGrowTextArea(TextArea):
  DEFAULT_CSS = """
  AutoGrowTextArea {
    height: auto;
    min-height: 1;
  }
  """
  
  def __init__(self, max_height: int = 10, **kwargs):
    self._max_height = max_height
    super().__init__(**kwargs)
  
  def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
    """Return visual line count, clamped to max_height."""
    # wrapped_document.height returns visual lines (after soft wrapping)
    # Returns 1 for empty document (minimum height)
    lines = self.wrapped_document.height
    return max(1, min(lines, self._max_height))
```

### Important: Import Locations

```python
# Selection is NOT in textual.widgets!
from textual.widgets.text_area import Selection  # Correct

# Size is in textual.geometry
from textual.geometry import Size

# Key events are in textual.events
from textual.events import Key

# Messages are in textual.message
from textual.message import Message
```

### Common Pitfalls

1. **Ctrl+A is NOT select all** - It moves to line start (like Home). Use F7 or add your own binding.

2. **wrapped_document.height requires mounting** - Returns 1 if widget not mounted. The `get_content_height` method is called during layout after mounting.

3. **Selection direction matters** - When selecting backwards (left/up), `selection.start > selection.end`.

4. **Terminal may intercept Cmd+A on macOS** - Terminal apps intercept `Cmd+A` for "Select All" in the terminal window. Use F7 or Ctrl+Shift+A instead.

5. **Selection import path** - `Selection` is in `textual.widgets.text_area`, NOT `textual.widgets`.

### Selection Backward Behavior

When selecting backwards:
- `selection.start` = original cursor position
- `selection.end` = new cursor position
- `selection.start > selection.end` (reversed)

```python
# Selecting left from position 5
text_area.cursor_location = (0, 5)
text_area.action_cursor_left(select=True)
# Result: selection.start = (0, 5), selection.end = (0, 4)
```

## Collapsible Widget

```python
from textual.widgets import Collapsible

with Collapsible(title="Advanced Options"):
  yield Static("Hidden content")
```

## ProgressBar Widget

```python
from textual.widgets import ProgressBar

yield ProgressBar(total=100)

# Update progress
bar = self.query_one(ProgressBar)
bar.advance(10)
```

## Container Widgets

```python
from textual.containers import (
  Container,
  Vertical,
  Horizontal,
  VerticalScroll,
  HorizontalScroll,
  Grid,
  Center,
)

# Vertical layout
with Vertical():
  yield Static("Top")
  yield Static("Bottom")

# Horizontal layout
with Horizontal():
  yield Static("Left")
  yield Static("Right")

# Grid layout
with Grid():
  yield Static("1,1")
  yield Static("1,2")
  yield Static("2,1")
  yield Static("2,2")

# Centered content
with Center():
  yield Static("Centered")
```

## Static Widget (Custom)

```python
from textual.widgets import Static

class MyWidget(Static):
  DEFAULT_CSS = """
  MyWidget {
    padding: 1;
    border: solid blue;
  }
  """
  
  def on_mount(self):
    self.update("Hello")
```

## Widget Query Patterns

```python
# Query single widget
table = self.query_one(DataTable)

# Query by ID
widget = self.query_one("#my-widget")

# Query multiple
inputs = self.query(Input)

# Query by type
labels = self.query(Label)

# Get by ID shorthand
widget = self.get_widget_by_id("my-widget")
```

## Widget Communication

### Parent to Child

```python
# Set reactive value
child = self.query_one(MyWidget)
child.value = "new value"
```

### Child to Parent (Messages)

```python
class MyWidget(Static):
  class Submitted(Message):
    def __init__(self, value: str):
      self.value = value
      super().__init__()
  
  def on_click(self):
    self.post_message(self.Submitted("value"))

# Parent handler
def on_my_widget_submitted(self, message: MyWidget.Submitted):
  print(f"Got: {message.value}")
```