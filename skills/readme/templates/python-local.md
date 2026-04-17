# Python Package (Non-PyPI) README Template

Use this template for Python packages not published to PyPI (internal tools, private packages, etc.).

```markdown
# {package-name}

[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]

> One-line description of what the package does.

## Overview

Brief description of why this package exists and what problem it solves.

## Requirements

- Python 3.X+
- Other dependencies listed in pyproject.toml

## Installation

### From Source

\`\`\`bash
git clone https://github.com/{user}/{repo}.git
cd {repo}
pip install -e .
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
pip install -e ".[dev]"
\`\`\`

### Testing

\`\`\`bash
pytest
\`\`\`

### Code Style

This project uses ruff for linting:

\`\`\`bash
ruff check .
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

[license]: LICENSE
```

## Badge Reference

For non-PyPI Python packages, use minimal badges:

| Badge | Markdown |
|-------|----------|
| License | `[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]` |

**Optional badges** (if applicable):
- CI: `[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]`

## Section Guidelines

- **Overview**: Explain why this isn't on PyPI (internal tool, prototype, etc.)
- **Requirements**: Be explicit about Python version and dependencies
- **Installation**: Focus on source installation
- **Project Structure**: Helpful for contributors since no PyPI docs exist