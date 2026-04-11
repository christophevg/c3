# Screen Template

Textual screen template.

## Basic Screen

```python
# screens/my_screen.py
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Container

class MyScreen(Screen):
  """My screen description."""
  
  CSS_PATH = "../styles/my_screen.tcss"
  
  def compose(self) -> ComposeResult:
    yield Container(
      Static("Content"),
    )
```

## Screen with Form

```python
# screens/form_screen.py
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
  Static,
  Input,
  Button,
  Container,
)
from textual.containers import Vertical

class FormScreen(Screen):
  """Form screen."""
  
  CSS_PATH = "../styles/form.tcss"
  
  BINDINGS = [
    ("escape", "back", "Back"),
  ]
  
  def compose(self) -> ComposeResult:
    with Container(classes="form"):
      yield Static("Enter Details", classes="title")
      yield Input(id="name", placeholder="Name")
      yield Input(id="email", placeholder="Email")
      with Container(classes="buttons"):
        yield Button("Submit", variant="primary", id="submit")
        yield Button("Cancel", id="cancel")
  
  def action_back(self) -> None:
    self.app.pop_screen()
  
  def on_button_pressed(self, event: Button.Pressed) -> None:
    if event.button.id == "submit":
      self.submit_form()
    elif event.button.id == "cancel":
      self.app.pop_screen()
  
  def submit_form(self) -> None:
    name = self.query_one("#name", Input).value
    email = self.query_one("#email", Input).value
    # Process form...
    self.app.pop_screen()
```

```css
/* styles/form.tcss */
FormScreen Container.form {
  align: center middle;
  width: 50;
}

FormScreen .title {
  text-style: bold;
  margin: 1;
}

FormScreen Input {
  margin: 1;
}

FormScreen .buttons {
  layout: horizontal;
  margin-top: 1;
}

FormScreen Button {
  margin: 0 1;
}
```

## Modal Screen

```python
# screens/confirm_screen.py
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Static, Button
from textual.containers import Container

class ConfirmScreen(ModalScreen[bool]):
  """Confirmation dialog."""
  
  CSS_PATH = "../styles/confirm.tcss"
  
  BINDINGS = [
    ("escape", "cancel", "Cancel"),
  ]
  
  def __init__(self, message: str):
    super().__init__()
    self.message = message
  
  def compose(self) -> ComposeResult:
    with Container(classes="dialog"):
      yield Static(self.message, classes="message")
      with Container(classes="buttons"):
        yield Button("Confirm", variant="error", id="confirm")
        yield Button("Cancel", id="cancel")
  
  def action_cancel(self) -> None:
    self.dismiss(False)
  
  def on_button_pressed(self, event: Button.Pressed) -> None:
    self.dismiss(event.button.id == "confirm")
```

```css
/* styles/confirm.tcss */
ConfirmScreen {
  align: center middle;
}

ConfirmScreen Container.dialog {
  background: $surface;
  border: thick $primary;
  padding: 2;
  width: 50;
}

ConfirmScreen .message {
  margin: 1;
}

ConfirmScreen .buttons {
  layout: horizontal;
  margin-top: 1;
}

ConfirmScreen Button {
  margin: 0 1;
}
```

## Data Screen

```python
# screens/data_screen.py
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Container

class DataScreen(Screen):
  """Screen with data table."""
  
  def compose(self) -> ComposeResult:
    yield Container(DataTable(id="table"))
  
  def on_mount(self) -> None:
    table = self.query_one(DataTable)
    table.add_columns("Name", "Value", "Status")
    self.load_data()
  
  def load_data(self) -> None:
    table = self.query_one(DataTable)
    table.add_row("Item 1", "100", "OK")
    table.add_row("Item 2", "200", "WARN")
```

## Screen with Tabs

```python
# screens/tabbed_screen.py
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import TabbedContent, TabPane, Static

class TabbedScreen(Screen):
  """Screen with tabbed content."""
  
  def compose(self) -> ComposeResult:
    with TabbedContent(initial="general"):
      with TabPane("General", id="general"):
        yield Static("General settings")
      with TabPane("Advanced", id="advanced"):
        yield Static("Advanced settings")
```