# Project Setup Patterns

Patterns for initializing and configuring Baseweb projects.

## Project Initialization

### Minimal Project Structure

When creating a new Baseweb project, use the minimal template from `baseweb-demo` bare branch:

```
project/
├── module_name/
│   ├── __init__.py
│   └── web/
│       ├── __init__.py
│       └── pages/
│           ├── __init__.py
│           └── index.js       # Hello world example
├── .env                       # Environment configuration
├── .gitignore
├── Makefile                   # Development commands
├── README.md                  # Project description
├── requirements.txt           # Python dependencies
└── tests/
    └── test_setup.py
```

### Server Initialization Pattern

```python
# module_name/__init__.py

import os
import logging
from dotenv import load_dotenv, find_dotenv

# Load environment
load_dotenv(find_dotenv())
load_dotenv(find_dotenv(".env.local"), override=True)

# Configure logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
logging.basicConfig(level=LOG_LEVEL, format=FORMAT)

# Silence verbose modules
for module in ["gunicorn.error", "socketio.server", "urllib3"]:
    logging.getLogger(module).setLevel(logging.WARN)

# Create server (Flask)
from baseweb import Baseweb
server = Baseweb("module_name")
server.log_config()

# Configure static files
from pathlib import Path
HERE = Path(__file__).resolve().parent
server.app_static_folder = HERE / "static"

# Register global components
server.register_component("app.js", HERE)

# Load pages
from .web.pages import *  # noqa
```

### Async Server (Quart)

For async projects using Quart:

```python
# module_name/__init__.py

import eventlet
eventlet.monkey_patch()

import os
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
load_dotenv(find_dotenv(".env.local"), override=True)

# ... same logging setup ...

from baseweb.async import Baseweb  # Note: async import
server = Baseweb("module_name")

# ... rest is same ...
```

## Environment Configuration

### Environment Variables

Baseweb uses `APP_*` environment variables for configuration:

| Variable | Purpose | Example |
|----------|---------|---------|
| `APP_NAME` | Application name | `"myapp"` |
| `APP_TITLE` | Page title | `"My Application"` |
| `APP_URL` | Public URL | `"https://example.com"` |
| `APP_AUTHOR` | Author name | `"John Doe"` |
| `APP_DESCRIPTION` | Meta description | `"My application description"` |
| `APP_COLOR_SCHEME` | Theme | `"dark"` or `"light"` |
| `APP_COLOR` | Primary color | `"#1976D2"` |
| `APP_STYLE` | Style mode | `"web"` or `"pwa"` |
| `APP_SOCKETIO` | Enable Socket.IO | `"yes"` or `"no"` |
| `APP_FAVICON_SUPPORT` | Enable favicon | `"yes"` or `"no"` |
| `APP_KEEP_ALIVE` | Use keep-alive | `"yes"` or `"no"` |

### .env File

```env
APP_NAME=myapp
APP_TITLE=My Application
APP_URL=http://localhost:5000
APP_COLOR_SCHEME=dark
APP_COLOR=#1976D2
APP_SOCKETIO=yes
LOG_LEVEL=DEBUG
```

### .env.local File

For local overrides (not committed to git):

```env
APP_URL=http://localhost:5000
LOG_LEVEL=DEBUG
```

## Authentication Setup

### Authenticator Function

```python
from baseweb import server

def authenticator(scope, request, *args, **kwargs):
    """
    Authenticate requests for protected endpoints.
    
    Args:
        scope: Permission scope (e.g., "app.resource.action")
        request: Flask request object
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    # Option 1: HTTP Basic Auth
    auth = request.authorization
    if auth:
        return validate_user(auth.username, auth.password, scope)
    
    # Option 2: Token-based auth
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token:
        return validate_token(token, scope)
    
    # Option 3: Session-based auth
    if hasattr(request, 'session') and 'user' in request.session:
        return check_permission(request.session['user'], scope)
    
    return False

server.authenticator = authenticator
```

### Socket.IO Authentication

```python
from baseweb import server
import logging

logger = logging.getLogger(__name__)

@server.socketio.on("connect")
def on_connect():
    """Handle client connection."""
    logger.info(f"Client connected: {server.request.sid}")

@server.socketio.on("disconnect")
def on_disconnect():
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {server.request.sid}")
```

## Component Registration

### Single Component

```python
import os
from module_name.web import server

HERE = os.path.dirname(__file__)
server.register_component("mypage.js", HERE, route="/mypage")
```

### Batch Registration

For projects with many components:

```python
from pathlib import Path
from module_name.web import server

COMPONENTS = Path(__file__).parent

for component in [
    "common",
    "utils",
    "header",
    "footer",
    "dashboard",
    "settings"
]:
    server.register_component(f"{component}.js", COMPONENTS)
```

### External Scripts

```python
# Register external JavaScript libraries
server.register_external_script("https://cdn.example.com/library.js")

# For conditional registration (e.g., reCAPTCHA)
recaptcha_key = os.environ.get("APP_RECAPTCHA_SITE_KEY")
if recaptcha_key:
    server.settings["recaptcha"] = recaptcha_key
    server.register_external_script(
        f"https://www.google.com/recaptcha/api.js?render={recaptcha_key}"
    )
```

## Custom JSON Encoding

```python
import json
from flask import make_response
from datetime import datetime

class Encoder(json.JSONEncoder):
    """Custom JSON encoder for handling special types."""
    
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, set):
            return list(o)
        return super().default(o)

@server.api.representation("application/json")
def output_json(data, code, headers=None):
    """Use custom encoder for API responses."""
    resp = make_response(json.dumps(data, cls=Encoder), code)
    resp.headers.extend(headers or {})
    return resp
```

## Makefile Pattern

```makefile
PROJECT = myapp

.PHONY: help envs run test clean

help:
	@echo "Available commands:"
	@echo "  make envs    - Create virtual environments"
	@echo "  make run     - Run the application"
	@echo "  make test    - Run tests"
	@echo "  make clean   - Remove generated files"

envs:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	. .venv/bin/activate && pip install -r requirements.base.txt

run:
	. .venv/bin/activate && python -m $(PROJECT)

test:
	. .venv/bin/activate && pytest tests/ -v

clean:
	rm -rf __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
```

## Dependencies

### requirements.txt

```txt
baseweb>=1.0.0
flask>=2.0.0
flask-restful>=0.3.9
python-dotenv>=0.19.0
```

### requirements.base.txt (Development)

```txt
pytest>=7.0.0
pytest-cov>=3.0.0
black>=22.0.0
flake8>=4.0.0
```