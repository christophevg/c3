# Python Package (PyPI) README Template

Use this template for Python packages published to PyPI.

```markdown
# {package-name}

[![PyPI](https://img.shields.io/pypi/v/{package-name}.svg)][pypi]
[![Python](https://img.shields.io/pypi/pyversions/{package-name}.svg)][pypi]
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]
[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]
[![Coverage](https://img.shields.io/coveralls/github/{user}/{repo}.svg)][coveralls]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)

> One-line description of what the package does.

## Installation

\`\`\`bash
pip install {package-name}
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

### Advanced Usage

\`\`\`python
# Advanced example
\`\`\`

## Documentation

Full documentation: https://{package-name}.readthedocs.io

## Development

### Requirements

- Python 3.X+
- [uv](https://docs.astral.sh/uv/) for dependency management
- Dependencies listed in pyproject.toml

### Setup

\`\`\`bash
git clone https://github.com/{user}/{repo}.git
cd {repo}
uv sync
\`\`\`

### Testing

\`\`\`bash
uv run pytest
\`\`\`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

[MIT](LICENSE)

[pypi]: https://pypi.org/project/{package-name}/
[uv]: https://docs.astral.sh/uv/
[ci]: https://github.com/{user}/{repo}/actions
[coveralls]: https://coveralls.io/github/{user}/{repo}
[license]: https://github.com/{user}/{repo}/blob/main/LICENSE
```

## Badge Reference

For PyPI packages, include these badges (7 total):

| Badge | Markdown |
|-------|----------|
| PyPI version | `[![PyPI](https://img.shields.io/pypi/v/{package}.svg)][pypi]` |
| Python versions | `[![Python](https://img.shields.io/pypi/pyversions/{package}.svg)][pypi]` |
| uv | `[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]` |
| CI | `[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]` |
| Coverage | `[![Coverage](https://img.shields.io/coveralls/github/{user}/{repo}.svg)][coveralls]` |
| License | `[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]` |
| Agentic | `[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)` |

**Important:**

- **Agentic badge is required** for all projects built using agentic workflow
- **uv badge is required** for all Python projects (standard package manager)
- **Downloads badge is NOT used** (rate limiting causes broken badges)
- **CI badge only if workflow exists** — check `.github/workflows/` before adding

## Section Guidelines

- **Quick Start**: Minimal example that demonstrates core functionality
- **Features**: Table format for quick scanning
- **Usage**: Progressive examples (basic → advanced)
- **Development**: For contributors who want to hack on the package
- **Changelog**: Link to separate file for maintenance