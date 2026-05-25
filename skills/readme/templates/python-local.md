# Python Package (Non-PyPI) README Template

Use this template for Python packages not published to PyPI (internal tools, private packages, etc.).

```markdown
# {package-name}

[![Python](https://img.shields.io/badge/Python-{version}-blue.svg)][python]
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]
[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)

> One-line description of what the package does.

## Overview

Brief description of why this package exists and what problem it solves.

## Requirements

- Python 3.X+
- [uv](https://docs.astral.sh/uv/) for dependency management
- Other dependencies listed in pyproject.toml

## Installation

### From Source

\`\`\`bash
git clone https://github.com/{user}/{repo}.git
cd {repo}
uv sync
\`\`\`

## Quick Start

\`\`\`python
from {package_name} import main_thing

result = main_thing("input")
\`\`\`

## Features

| Feature | Description |
|---------|-------------|
| Feature 1 | Description of feature 1 |
| Feature 2 | Description of feature 2 |

## Usage

### Basic Usage

\`\`\`python
# Example code
\`\`\`

### Configuration

\`\`\`python
# Configuration options
\`\`\`

## Development

### Setup

\`\`\`bash
uv sync --all-extras
\`\`\`

### Testing

\`\`\`bash
uv run pytest
\`\`\`

### Code Style

This project uses ruff for linting:

\`\`\`bash
uv run ruff check .
\`\`\`

## Project Structure

\`\`\`
{package-name}/
├── src/
│   └── {package_name}/
│       ├── __init__.py
│       └── core.py
├── tests/
├── pyproject.toml
└── README.md
\`\`\`

## License

[MIT](LICENSE)

[python]: https://python.org/
[uv]: https://docs.astral.sh/uv/
[ci]: https://github.com/{user}/{repo}/actions
[license]: https://github.com/{user}/{repo}/blob/main/LICENSE
```

## Badge Reference

For non-PyPI Python packages, include these badges (4-5 total):

| Badge | Markdown |
|-------|----------|
| Python version | `[![Python](https://img.shields.io/badge/Python-{version}-blue.svg)][python]` |
| uv | `[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]` |
| CI | `[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]` *(only if workflow exists)* |
| License | `[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]` |
| Agentic | `[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)` |

**Important:**

- **CI badge only if workflow exists** — check `.github/workflows/` before adding
- Replace `{version}` with Python version from `.python-version` or `pyproject.toml`
- **Agentic badge is required** for all projects built using agentic workflow

## Section Guidelines

- **Overview**: Explain why this isn't on PyPI (internal tool, prototype, etc.)
- **Requirements**: Be explicit about Python version and dependencies
- **Installation**: Focus on source installation with uv
- **Project Structure**: Helpful for contributors since no PyPI docs exist