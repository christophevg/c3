# App Scaffold Template

Basic Textual application scaffold.

## Full Structure

```
myapp/
├── __main__.py
├── app.py
├── styles/
│   └── main.tcss
├── screens/
│   ├── __init__.py
│   └── home.py
└── widgets/
    └── __init__.py
```

## __main__.py

```python
"""Entry point for myapp."""
from myapp.app import MyApp

if __name__ == "__main__":
  app = MyApp()
  app.run()
```

## app.py

```python
"""Main application."""
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from myapp.screens.home import HomeScreen

class MyApp(App):
  """My TUI application."""
  
  CSS_PATH = "styles/main.tcss"
  TITLE = "MyApp"
  SUB_TITLE = "v1.0"
  
  SCREENS = {
    "home": HomeScreen,
  }
  
  BINDINGS = [
    ("q", "quit", "Quit"),
    ("?", "help", "Help"),
  ]
  
  def on_mount(self) -> None:
    self.push_screen("home")
  
  def action_quit(self) -> None:
    self.exit()
  
  def action_help(self) -> None:
    self.push_screen("help")
```

## styles/main.tcss

```css
/* Main application styles */

/* App background */
App {
  background: $surface;
}

/* Header */
Header {
  dock: top;
  background: $primary;
  color: $text-on-primary;
}

/* Footer */
Footer {
  dock: bottom;
  background: $panel;
}

/* Key bindings in footer */
Footer .footer--key {
  background: $primary;
  color: $text-on-primary;
}

/* Main content area */
Screen {
  layout: vertical;
  align: center middle;
}

/* Common containers */
Container {
  padding: 1 2;
}

/* Messages */
.message {
  margin: 1;
  padding: 1;
}

.message.error {
  border: solid red;
  color: $error;
}

.message.success {
  border: solid green;
  color: $success;
}
```

## screens/__init__.py

```python
"""Screens package."""
from myapp.screens.home import HomeScreen

__all__ = ["HomeScreen"]
```

## screens/home.py

```python
"""Home screen."""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Container

class HomeScreen(Screen):
  """Home screen."""
  
  CSS_PATH = "../styles/home.tcss"
  
  def compose(self) -> ComposeResult:
    yield Container(
      Static("Welcome to MyApp", classes="title"),
      Static("Press ? for help", classes="hint"),
    )
```

## styles/home.tcss

```css
/* Home screen styles */

HomeScreen Container {
  align: center middle;
}

HomeScreen .title {
  text-style: bold;
  color: $primary;
  margin: 1;
}

HomeScreen .hint {
  color: $text-muted;
}
```

## widgets/__init__.py

```python
"""Widgets package."""
# Add custom widgets here
```

## pyproject.toml (Optional)

```toml
[project]
name = "myapp"
version = "0.1.0"
dependencies = [
  "textual>=0.47.0",
]

[project.scripts]
myapp = "myapp.__main__:main"

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
```

## Minimal Single-File

```python
#!/usr/bin/env python
"""Minimal Textual app."""
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class MyApp(App):
  CSS = """
  Screen { layout: vertical; }
  """
  
  def compose(self) -> ComposeResult:
    yield Header()
    yield Static("Hello, World!")
    yield Footer()

if __name__ == "__main__":
  MyApp().run()
```