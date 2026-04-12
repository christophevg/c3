---
name: textual
description: Guide Python Textual framework for building terminal user interfaces (TUIs) with CSS styling and reactive state. Use when user mentions textual, TUI, terminal UI, or code imports textual. Use for interactive apps when Rich is insufficient. MUST be used BEFORE exploring Textual code or running one-off scripts to understand Textual APIs.
---

# Textual

Guide Python's Textual framework for building sophisticated terminal user interfaces (TUIs). Use Textual when Rich alone would require too much overhead for interactivity.

## Overview

| Capability | Description |
|------------|-------------|
| App Architecture | App class, lifecycle, screens |
| Widgets | 35+ built-in widgets |
| CSS Styling | Separate `.tcss` files |
| Layout | Grid, dock, horizontal, vertical |
| Events | Message passing, key bindings |
| State | Reactive attributes, watch, compute |
| Async | Workers, timers |

## When to Use This Skill

**IMPORTANT: Use this skill BEFORE exploring Textual code or running one-off Python scripts.** This skill contains comprehensive API knowledge that can save significant exploration time.

Use this skill when:
- User mentions "textual", "TUI", "terminal UI", "text-based UI"
- Code imports `textual` or `from textual import`
- User asks about building interactive terminal applications
- Rich alone would require too much overhead
- You need to understand Textual widget APIs (TextArea, Input, DataTable, etc.)
- You need to know key bindings, cursor movement, selection handling
- You need to implement auto-height or dynamic widget sizing

Ask clarification when:
- User asks about "terminal app" or "console output" (could be Rich or Textual)

## Project Structure

```
myapp/
├── __main__.py        # Entry point
├── app.py             # App class
├── styles/
│   └── main.tcss      # Main CSS file
├── screens/
│   ├── __init__.py
│   ├── home.py        # Home screen
│   └── settings.py    # Settings screen
└── widgets/
    ├── __init__.py
    └── custom.py       # Custom widgets
```

## App Basics

```python
# app.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class MyApp(App):
  CSS_PATH = "styles/main.tcss"
  TITLE = "My App"
  BINDINGS = [
    ("q", "quit", "Quit"),
    ("s", "settings", "Settings"),
  ]
  
  def compose(self) -> ComposeResult:
    yield Header()
    yield Container()
    yield Footer()
  
  def on_mount(self) -> None:
    # Setup after entering app mode
    pass
  
  def action_quit(self) -> None:
    self.exit()
```

## Screen Management

```python
# screens/home.py
from textual.screen import Screen
from textual.widgets import Static

class HomeScreen(Screen):
  CSS_PATH = "styles/home.tcss"
  
  def compose(self) -> ComposeResult:
    yield Static("Home Screen")

# In app
def action_settings(self) -> None:
  self.push_screen("settings")

# Push by name (from SCREENS dict)
SCREENS = {"settings": SettingsScreen}
self.push_screen("settings")

# Pop screen
self.pop_screen()

# Modal screen (blocks underlying)
class ConfirmScreen(ModalScreen[bool]):
  ...
  def on_button_pressed(self, event):
    self.dismiss(True)
```

## Common Widgets

### Input

```python
from textual.widgets import Input

yield Input(
  placeholder="Enter text",
  validators=[],
)
```

### Button

```python
from textual.widgets import Button

yield Button("Click Me", variant="primary")
# variants: default, primary, success, warning, error
```

### DataTable

```python
from textual.widgets import DataTable

table = DataTable()
table.add_column("Name")
table.add_column("Value")
table.add_row("Item 1", "100")
```

### ListView

```python
from textual.widgets import ListView, ListItem, Label

yield ListView(
  ListItem(Label("Item 1")),
  ListItem(Label("Item 2")),
)
```

### TextArea

```python
from textual.widgets import TextArea

yield TextArea.code_editor(code, language="python")
```

### TabbedContent

```python
from textual.widgets import TabbedContent, TabPane

with TabbedContent():
  with TabPane("Tab 1"):
    yield Static("Content 1")
  with TabPane("Tab 2"):
    yield Static("Content 2")
```

## Layout with CSS

```css
/* styles/main.tcss */
Screen {
  layout: vertical;
}

#header {
  dock: top;
  height: 3;
}

#sidebar {
  dock: left;
  width: 20;
}

#content {
  layout: grid;
  grid-size: 2 2;
  grid-columns: 1fr 1fr;
}

#footer {
  dock: bottom;
  height: 3;
}
```

## Event Handling

### Method Handlers

```python
def on_button_pressed(self, event: Button.Pressed) -> None:
  # Handle button press
  pass

def on_input_changed(self, event: Input.Changed) -> None:
  # Handle input change
  pass
```

### @on Decorator

```python
from textual import on

@on(Button.Pressed, "#quit")
def quit_app(self):
  self.exit()
```

### Custom Messages

```python
class MyWidget(Static):
  class Selected(Message):
    def __init__(self, value):
      self.value = value
      super().__init__()
  
  def on_click(self):
    self.post_message(self.Selected(self.value))

# Handler in parent
def on_my_widget_selected(self, message: MyWidget.Selected):
  print(f"Selected: {message.value}")
```

## Key Bindings

```python
BINDINGS = [
  ("q", "quit", "Quit"),
  ("r", "refresh", "Refresh"),
  ("ctrl+s", "save", "Save"),
]

def action_refresh(self) -> None:
  self.refresh()

def action_save(self) -> None:
  self.save()
```

## Reactive State

```python
from textual.reactive import reactive

class MyWidget(Widget):
  count = reactive(0)
  
  def watch_count(self, old: int, new: int) -> None:
    # Called when count changes
    self.update(f"Count: {new}")
  
  def increment(self) -> None:
    self.count += 1
```

## Workers (Async)

```python
from textual import work

@work(exclusive=True)
async def fetch_data(self):
  data = await api.fetch()
  self.update_display(data)

@work(thread=True)
def blocking_task(self):
  result = slow_operation()
  self.call_from_thread(self.update, result)
```

## Timers

```python
def on_mount(self):
  # One-shot timer
  self.set_timer(10, self.refresh_data)
  
  # Repeating interval
  self.clock_timer = self.set_interval(1, self.update_clock)

def on_unmount(self):
  self.clock_timer.stop()
```

## Common Issues

| Issue | Solution |
|-------|----------|
| CSS not loading | Check `CSS_PATH` is relative to app file |
| Widget not found | Use `query_one()` or `query()` correctly |
| Events not bubbling | Check `event.stop()` or widget focus |
| Layout not working | Verify CSS selectors match widget IDs |
| Blocking UI | Use `@work` decorator for async |

## Pattern Files

- `patterns/app-structure.md` - Project structure patterns
- `patterns/widgets.md` - Widget patterns
- `patterns/events.md` - Event handling patterns
- `patterns/state.md` - State management patterns

## Template Files

- `templates/app-scaffold.md` - App scaffolding
- `templates/screen-template.md` - Screen template
- `templates/widget-template.md` - Custom widget template

## Reference Files

- `references/widgets-catalog.md` - Complete widget catalog
- `references/css-reference.md` - CSS syntax reference

## Related Skills

- python - Base skill for Python development
- rich - Console output (used by Textual internally)