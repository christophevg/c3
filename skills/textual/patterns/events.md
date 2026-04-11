# Event Patterns

Textual event handling patterns.

## Event Handler Naming

```python
# Widget-specific events
def on_button_pressed(self, event: Button.Pressed):
  pass

def on_input_changed(self, event: Input.Changed):
  pass

def on_input_submitted(self, event: Input.Submitted):
  pass

# General events
def on_mount(self):
  pass

def on_click(self, event: events.Click):
  pass

def on_key(self, event: events.Key):
  pass
```

## @on Decorator

For targeted event handling:

```python
from textual import on

@on(Button.Pressed, "#save")
def save(self):
  self.save_data()

@on(Input.Submitted, "#search")
def search(self, event: Input.Submitted):
  self.do_search(event.value)

@on(DataTable.RowSelected)
def row_selected(self, event: DataTable.RowSelected):
  print(f"Row: {event.row_key}")
```

## Event Bubbling

Events bubble from child to parent. Control with:

```python
def on_key(self, event: events.Key):
  if event.key == "escape":
    event.stop()  # Stop bubbling
    self.close()
```

## Custom Messages

```python
from textual.message import Message

class MyWidget(Static):
  class Clicked(Message):
    """Posted when widget is clicked."""
    def __init__(self, x: int, y: int):
      self.x = x
      self.y = y
      super().__init__()
  
  def on_click(self, event: events.Click):
    self.post_message(self.Clicked(event.x, event.y))

# Parent handler
def on_my_widget_clicked(self, message: MyWidget.Clicked):
  print(f"Clicked at ({message.x}, {message.y})")
```

## Key Bindings

### App-Level Bindings

```python
class MyApp(App):
  BINDINGS = [
    ("q", "quit", "Quit"),
    ("r", "refresh", "Refresh"),
    ("ctrl+s", "save", "Save"),
    ("ctrl+q", "quit", "Quit"),
  ]
  
  def action_quit(self) -> None:
    self.exit()
  
  def action_refresh(self) -> None:
    self.refresh_data()
```

### Widget-Level Bindings

```python
class MyWidget(Static):
  BINDINGS = [
    ("enter", "select", "Select"),
    ("delete", "delete", "Delete"),
  ]
  
  def action_select(self) -> None:
    self.select_item()
```

### Dynamic Bindings

```python
def check_action(self, action: str, parameters: tuple) -> bool | None:
  """Control binding visibility."""
  if action == "next_page" and self.page >= self.max_pages:
    return False  # Hide
  if action == "prev_page" and self.page <= 1:
    return None   # Disable (dim)
  return True    # Show and enable

# Refresh bindings after state change
page = reactive(1, bindings=True)
```

## Focus Events

```python
def on_focus(self, event: events.Focus):
  """Widget received focus."""
  self.add_class("focused")

def on_blur(self, event: events.Blur):
  """Widget lost focus."""
  self.remove_class("focused")
```

## Mouse Events

```python
def on_click(self, event: events.Click):
  print(f"Clicked at ({event.x}, {event.y})")

def on_mouse_move(self, event: events.MouseMove):
  print(f"Mouse at ({event.x}, {event.y})")

def on_mouse_down(self, event: events.MouseDown):
  print(f"Mouse down: {event.button}")
```

## Screen Events

```python
def on_screen_resume(self, event: events.ScreenResume):
  """Screen returned to top of stack."""
  self.refresh_data()

def on_screen_suspend(self, event: events.ScreenSuspend):
  """Another screen pushed on top."""
  pass
```

## Event Flow

1. Event posted to widget's message queue
2. Widget's handler method called
3. Handler can `stop()` event (prevents bubbling)
4. If not stopped, event bubbles to parent
5. Continue until handled or reaches App

## Common Patterns

| Pattern | Use Case |
|---------|----------|
| `on_<event>()` | Widget-specific handling |
| `@on(Event, selector)` | Targeted handling |
| `event.stop()` | Prevent bubbling |
| `post_message(msg)` | Custom events |
| BINDINGS | Key shortcuts |

## Example: Form Handling

```python
class FormScreen(Screen):
  def compose(self):
    yield Input(id="name", placeholder="Name")
    yield Input(id="email", placeholder="Email")
    yield Button("Submit", id="submit")
  
  @on(Button.Pressed, "#submit")
  def submit(self):
    name = self.query_one("#name", Input).value
    email = self.query_one("#email", Input).value
    self.submit_form(name, email)
  
  @on(Input.Submitted)
  def enter_submit(self, event: Input.Submitted):
    if event.input.id == "email":
      self.submit()
```