# App Structure Patterns

Textual application structure patterns.

## Recommended Structure

```
myapp/
├── __main__.py           # Entry point
├── app.py                # App class
├── styles/
│   ├── main.tcss         # Main CSS
│   └── widgets/          # Widget-specific CSS (optional)
├── screens/
│   ├── __init__.py
│   ├── home.py
│   └── settings.py
└── widgets/
    ├── __init__.py
    └── custom.py
```

## Entry Point

```python
# __main__.py
from myapp.app import MyApp

if __name__ == "__main__":
  app = MyApp()
  app.run()
```

## App Class

```python
# app.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from myapp.screens.home import HomeScreen
from myapp.screens.settings import SettingsScreen

class MyApp(App):
  """Main application."""
  
  CSS_PATH = "styles/main.tcss"
  TITLE = "My App"
  SUB_TITLE = "v1.0"
  
  SCREENS = {
    "home": HomeScreen,
    "settings": SettingsScreen,
  }
  
  BINDINGS = [
    ("q", "quit", "Quit"),
    ("h", "app.push_screen('home')", "Home"),
    ("s", "app.push_screen('settings')", "Settings"),
  ]
  
  def on_mount(self) -> None:
    self.push_screen("home")
  
  def action_quit(self) -> None:
    self.exit()
```

## Screen Module

```python
# screens/home.py
from textual.screen import Screen
from textual.widgets import Static, Container
from textual.app import ComposeResult

class HomeScreen(Screen):
  CSS_PATH = "../styles/home.tcss"
  
  def compose(self) -> ComposeResult:
    yield Header()
    yield Container(
      Static("Welcome to My App"),
    )
    yield Footer()
```

## Widget Module

```python
# widgets/custom.py
from textual.widgets import Static
from textual.app import ComposeResult

class MyWidget(Static):
  """Custom widget with embedded CSS."""
  
  DEFAULT_CSS = """
  MyWidget {
    padding: 1;
    border: solid green;
  }
  """
  
  def compose(self) -> ComposeResult:
    yield Static("Widget content")
```

## CSS Organization

```css
/* styles/main.tcss */
@import "widgets/*.tcss";  /* Import widget CSS (optional) */

/* App-level styles */
App {
  background: $surface;
}

Screen {
  layout: vertical;
}

/* Common components */
#header {
  dock: top;
  height: 3;
  content-align: center middle;
}

#footer {
  dock: bottom;
  height: 1;
}
```

```css
/* styles/home.tcss */
HomeScreen {
  layout: vertical;
}

HomeScreen Container {
  padding: 1 2;
}
```

## Package Structure (pip-installable)

```
myapp/
├── pyproject.toml
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       ├── styles/
│       ├── screens/
│       └── widgets/
└── tests/
```

## Minimal Structure (Single File)

```python
# myapp.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class MyApp(App):
  CSS = """
  Screen { layout: vertical; }
  """
  
  def compose(self) -> ComposeResult:
    yield Header()
    yield Static("Hello")
    yield Footer()

if __name__ == "__main__":
  MyApp().run()
```

## CSS Loading Priority

1. `CSS_PATH` - External file (recommended)
2. `CSS` - Inline string (for simple apps)
3. `DEFAULT_CSS` - In widget class (for reusable widgets)

```python
class MyApp(App):
  # External CSS file (recommended)
  CSS_PATH = "styles/main.tcss"

class SimpleApp(App):
  # Inline CSS (simple apps only)
  CSS = """
  Screen { layout: vertical; }
  """

class MyWidget(Static):
  # Widget default CSS
  DEFAULT_CSS = """
  MyWidget { padding: 1; }
  """
```

## Screen Navigation Patterns

### Stack-Based

```python
# Push/pop screens
self.push_screen("settings")  # Add to stack
self.pop_screen()             # Remove top
```

### Mode-Based (Multiple Stacks)

```python
class MyApp(App):
  MODES = {
    "dashboard": DashboardScreen,
    "settings": SettingsScreen,
  }
  
  def on_mount(self):
    self.switch_mode("dashboard")
```

## Import Patterns

```python
# In app.py - import screens
from myapp.screens import HomeScreen, SettingsScreen

# In screens - import widgets
from myapp.widgets import MyWidget

# In widgets - use textual imports only
from textual.widgets import Static
```