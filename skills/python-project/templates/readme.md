# README Template

```markdown
# my-package

[![PyPI version](https://img.shields.io/pypi/v/my-package.svg)](https://pypi.org/project/my-package/)
[![Python versions](https://img.shields.io/pypi/pyversions/my-package.svg)](https://pypi.org/project/my-package/)
[![License](https://img.shields.io/github/license/username/my-package.svg)](https://github.com/username/my-package/blob/main/LICENSE)
[![CI](https://github.com/username/my-package/actions/workflows/test.yml/badge.svg)](https://github.com/username/my-package/actions/workflows/test.yml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-blue.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy.readthedocs.io/)
[![Read the Docs](https://img.shields.io/readthedocs/my-package.svg)](https://my-package.readthedocs.io/)

Brief description of what my-package does.

> **Note:** This package provides **async-only** APIs. (Include if applicable)

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

### Using pip

```bash
pip install my-package
```

### Using uv

```bash
uv add my-package
```

## Quick Start

```python
from my_package import Client

client = Client()
result = client.do_something()
print(result)
```

## Configuration

```bash
export MY_PACKAGE_OPTION=value
```

See [Configuration](docs/configuration.md) for detailed options.

## Documentation

Full documentation available at [my-package.readthedocs.io](https://my-package.readthedocs.io/).

## Development

```bash
make dev-env    # Install development dependencies
make test       # Run tests
make lint       # Run linter
make typecheck  # Run type checker
make all        # Run all checks
make docs       # Build documentation
```

## License

MIT License - see [LICENSE](LICENSE) for details.
```

## Required README Sections

| Section | Purpose |
|---------|---------|
| Badges | Quick project status overview |
| Description | What the package does |
| Installation | How to install |
| Quick Start | Minimal working example |
| Configuration | Essential config options |
| Documentation | Link to full docs |
| Development | Dev setup commands |
| License | License info |

## Standard Badges

Include these badges in every README:

| Badge | Badge URL |
|-------|-----------|
| PyPI version | `https://img.shields.io/pypi/v/PACKAGE.svg` |
| Python versions | `https://img.shields.io/pypi/pyversions/PACKAGE.svg` |
| License | `https://img.shields.io/github/license/USER/REPO.svg` |
| CI | `https://github.com/USER/REPO/actions/workflows/test.yml/badge.svg` |
| Code style | `https://img.shields.io/badge/code%20style-ruff-blue.svg` |
| Type checked | `https://img.shields.io/badge/type%20checked-mypy-blue.svg` |
| ReadTheDocs | `https://img.shields.io/readthedocs/PACKAGE.svg` |
| Agentic workflow (optional) | `https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square` |

### Agentic Workflow Badge

For projects built using agentic workflow (AI agents implementing architecture), add:

```markdown
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Coding-Agent)
```

This badge should be included for projects in `~/Workspace/agentic/` or any project explicitly built with agentic development practices.