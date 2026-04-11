# Widget Template

Textual custom widget template.

## Basic Widget

```python
# widgets/my_widget.py
from textual.widgets import Static
from textual.app import ComposeResult

class MyWidget(Static):
  """A custom widget."""
  
  DEFAULT_CSS = """
  MyWidget {
    padding: 1;
    border: solid blue;
  }
  """
  
  def on_mount(self) -> None:
    self.update("Widget content")
```

## Widget with Children

```python
# widgets/info_card.py
from textual.widgets import Static, Label
from textual.app import ComposeResult
from textual.containers import Vertical

class InfoCard(Static):
  """An information card widget."""
  
  DEFAULT_CSS = """
  InfoCard {
    border: solid $primary;
    padding: 1;
    width: auto;
    height: auto;
  }
  
  InfoCard .title {
    text-style: bold;
    color: $primary;
  }
  
  InfoCard .content {
    color: $text-muted;
  }
  """
  
  COMPONENT_CLASSES = {
    "info-card--title",
    "info-card--content",
  }
  
  def __init__(self, title: str, content: str):
    super().__init__()
    self.title = title
    self.content = content
  
  def compose(self) -> ComposeResult:
    yield Label(self.title, classes="title")
    yield Label(self.content, classes="content")
```

## Reactive Widget

```python
# widgets/counter.py
from textual.widgets import Static
from textual.app import ComposeResult
from textual.reactive import reactive

class Counter(Static):
  """A counter widget."""
  
  DEFAULT_CSS = """
  Counter {
    padding: 1;
    text-align: center;
  }
  """
  
  count = reactive(0)
  
  def on_mount(self) -> None:
    self.update_display()
  
  def watch_count(self, old: int, new: int) -> None:
    self.update_display()
  
  def update_display(self) -> None:
    self.update(f"Count: {self.count}")
  
  def increment(self) -> None:
    self.count += 1
  
  def decrement(self) -> None:
    self.count -= 1
  
  def reset(self) -> None:
    self.count = 0
```

## Widget with Custom Message

```python
# widgets/selectable_item.py
from textual.widgets import Static
from textual.message import Message

class SelectableItem(Static):
  """A selectable item widget."""
  
  DEFAULT_CSS = """
  SelectableItem {
    padding: 1;
  }
  
  SelectableItem:hover {
    background: $surface-lighten-1;
  }
  
  SelectableItem.selected {
    background: $primary;
    color: $text-on-primary;
  }
  """
  
  class Selected(Message):
    """Posted when item is selected."""
    def __init__(self, item: "SelectableItem"):
      self.item = item
      super().__init__()
  
  def __init__(self, value: str):
    super().__init__()
    self.value = value
    self.selected = False
  
  def on_click(self) -> None:
    self.toggle_select()
  
  def toggle_select(self) -> None:
    self.selected = not self.selected
    self.set_class(self.selected, "selected")
    self.post_message(self.Selected(self))
```

## Widget with BINDINGS

```python
# widgets/editable_text.py
from textual.widgets import Static
from textual.reactive import reactive

class EditableText(Static):
  """An editable text widget."""
  
  DEFAULT_CSS = """
  EditableText {
    padding: 1;
  }
  
  EditableText.editing {
    border: solid yellow;
  }
  """
  
  BINDINGS = [
    ("enter", "toggle_edit", "Edit"),
    ("escape", "cancel_edit", "Cancel"),
  ]
  
  text = reactive("")
  editing = reactive(False)
  
  def on_mount(self) -> None:
    self.update(self.text)
  
  def watch_editing(self, editing: bool) -> None:
    self.set_class(editing, "editing")
  
  def action_toggle_edit(self) -> None:
    self.editing = not self.editing
  
  def action_cancel_edit(self) -> None:
    self.editing = False
```

## Widget with compose()

```python
# widgets/panel_widget.py
from textual.widgets import Static, Button
from textual.app import ComposeResult
from textual.containers import Vertical

class PanelWidget(Static):
  """A panel with header and actions."""
  
  DEFAULT_CSS = """
  PanelWidget {
    border: solid $panel;
  }
  
  PanelWidget .header {
    background: $panel;
    padding: 1;
    text-style: bold;
  }
  
  PanelWidget .content {
    padding: 1;
  }
  
  PanelWidget .actions {
    layout: horizontal;
    padding: 1;
  }
  """
  
  def __init__(self, title: str):
    super().__init__()
    self.title = title
  
  def compose(self) -> ComposeResult:
    yield Static(self.title, classes="header")
    yield Static("Content here", classes="content")
    with Vertical(classes="actions"):
      yield Button("Action 1", id="action1")
      yield Button("Action 2", id="action2")
```

## Widget Directory Pattern

```
widgets/
├── __init__.py
├── counter.py
├── info_card.py
└── selectable_item.py
```

```python
# widgets/__init__.py
from myapp.widgets.counter import Counter
from myapp.widgets.info_card import InfoCard
from myapp.widgets.selectable_item import SelectableItem

__all__ = ["Counter", "InfoCard", "SelectableItem"]
```