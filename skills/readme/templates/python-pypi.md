# Python Package (PyPI) README Template

Use this template for Python packages published to PyPI.

```markdown
# {package-name}

[![PyPI](https://img.shields.io/pypi/v/{package-name}.svg)][pypi]
[![Python](https://img.shields.io/pypi/pyversions/{package-name}.svg)][pypi]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]

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
- Dependencies listed in pyproject.toml

### Setup

\`\`\`bash
git clone https://github.com/{user}/{repo}.git
cd {repo}
pip install -e ".[dev]"
\`\`\`

### Testing

\`\`\`bash
pytest
\`\`\`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

[MIT](LICENSE)

[pypi]: https://pypi.org/project/{package-name}/
[license]: LICENSE
```

## Badge Reference

For PyPI packages, include these badges:

| Badge | Markdown |
|-------|----------|
| PyPI version | `[![PyPI](https://img.shields.io/pypi/v/{package}.svg)][pypi]` |
| Python versions | `[![Python](https://img.shields.io/pypi/pyversions/{package}.svg)][pypi]` |
| License | `[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]` |
| CI | `[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]` |
| Coverage | `[![Coverage](https://img.shields.io/coveralls/github/{user}/{repo}.svg)][coveralls]` |
| Docs | `[![Docs](https://img.shields.io/readthedocs/{package}.svg)][docs]` |

**Optional badges** (if applicable):
- Downloads: `https://img.shields.io/pypi/dm/{package}`
- Code style: `https://img.shields.io/badge/code%20style-ruff-black`

## Section Guidelines

- **Quick Start**: Minimal example that demonstrates core functionality
- **Features**: Table format for quick scanning
- **Usage**: Progressive examples (basic → advanced)
- **Development**: For contributors who want to hack on the package
- **Changelog**: Link to separate file for maintenance