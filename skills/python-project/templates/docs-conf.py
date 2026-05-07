# Sphinx Configuration Template

`docs/conf.py`:

```python
"""Sphinx configuration for my-package."""

project = "my-package"
copyright = "2025, Your Name"
author = "Your Name"

# Read version from package
import tomllib
from pathlib import Path

pyproject = Path(__file__).parent.parent / "pyproject.toml"
with open(pyproject, "rb") as f:
    data = tomllib.load(f)
    version = data["project"]["version"]

release = version

# Extensions
extensions = [
  "myst_parser",
  "sphinx.ext.autodoc",
  "sphinx.ext.napoleon",
  "sphinx.ext.viewcode",
]

# Use MyST for markdown
source_suffix = [".rst", ".md"]

# Theme
html_theme = "furo"
html_title = f"{project} {version}"

# Options
html_static_path = ["_static"]
templates_path = ["_templates"]

# MyST options
myst_enable_extensions = [
  "deflist",
  "html_admonition",
  "html_image",
  "linkify",
  "replacements",
  "smartquotes",
  "tasklist",
]
```

## index.rst Template

`docs/index.rst`:

```rst
my-package Documentation
========================

Brief description of what my-package does.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   api

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   configuration
   examples

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

## installation.md Template

`docs/installation.md`:

```markdown
# Installation

## Requirements

- Python 3.10 or higher

## Install from PyPI

\`\`\`bash
pip install my-package
\`\`\`

## Install with uv

\`\`\`bash
uv add my-package
\`\`\`

## Development Installation

\`\`\`bash
git clone https://github.com/username/my-package.git
cd my-package
make dev-env
\`\`\`

## Next Steps

- [API Reference](api.md)
- [Configuration](configuration.md)
```

## .readthedocs.yaml Template

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.12"

sphinx:
  configuration: docs/conf.py

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs  # IMPORTANT: Use 'docs', not 'dev'
```