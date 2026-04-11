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