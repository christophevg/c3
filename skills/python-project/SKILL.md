---
name: python-project
description: Use this skill when setting up or migrating Python projects to the standard hatchling-based setup
---

# Python Project Setup

This skill defines the standard Python project setup for all new and migrated projects.

## Standard Setup: hatchling + pyproject.toml

All Python projects should use the modern `pyproject.toml` configuration with `hatchling` as the build backend.

### Why hatchling?

- **Simpler configuration** - Fewer `[tool.*]` sections than setuptools
- **Modern defaults** - PEP 639 support for license metadata
- **Respects `.gitignore`** - Won't accidentally include test/tooling directories
- **Lightweight** - 83kB vs setuptools' 894kB
- **Active development** - Part of the Hatch ecosystem

### Standard pyproject.toml Template

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
description = "A brief description of the package"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
  {name = "Your Name", email = "your@email.com"}
]
classifiers = [
  "Development Status :: 3 - Alpha",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Typing :: Typed",
]
keywords = ["relevant", "keywords"]
dependencies = [
  "dependency>=1.0.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=7.0.0",
  "pytest-cov>=4.0.0",
  "pytest-asyncio>=0.21.0",
  "mypy>=1.0.0",
  "ruff>=0.1.0",
  "build>=1.0.0",
  "twine>=5.0.0",
  "sphinx>=7.0.0",
  "sphinx-rtd-theme>=2.0.0",
  "myst-parser>=2.0.0",
  "tox>=4.0.0",
]

[project.urls]
Homepage = "https://github.com/username/my-package"
Documentation = "https://my-package.readthedocs.io/"
Repository = "https://github.com/username/my-package"
Issues = "https://github.com/username/my-package/issues"

[project.scripts]
my-package = "mypackage.__main__:main"

[tool.hatch.build]
sources = ["src"]

[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]

# Testing configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --cov=mypackage --cov-report=term-missing"

# Type checking configuration
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true

# Linting configuration
[tool.ruff]
line-length = 100
target-version = "py310"
indent-width = 2

[tool.ruff.lint]
select = [
  "E",   # pycodestyle errors
  "W",   # pycodestyle warnings
  "F",   # pyflakes
  "I",   # isort
  "B",   # flake8-bugbear
  "C4",  # flake8-comprehensions
  "UP",  # pyupgrade
]
ignore = [
  "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["mypackage"]

# Coverage configuration
[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
  "pragma: no cover",
  "def __repr__",
  "raise NotImplementedError",
  "if TYPE_CHECKING:",
]

# Multi-version testing
[tool.tox]
env_list = ["py310", "py311", "py312"]

[tool.tox.env_run_base]
extras = ["dev"]
commands = [
  ["pytest", "-v", "--cov=mypackage", "--cov-report=term-missing"],
]
```

## Project Structure

### Standard Layout (src-layout)

```
my-package/
├── src/
│   └── mypackage/
│       ├── __init__.py      # Public API exports
│       ├── py.typed         # PEP 561 marker
│       └── ...              # Module files
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   └── test_*.py           # Test files
├── docs/
│   ├── conf.py
│   ├── index.md
│   └── Makefile
├── pyproject.toml
├── README.md
├── LICENSE
├── .readthedocs.yaml
├── .gitignore
└── .python-version         # pyenv version name
```

### Key Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | All project configuration (build, tools, metadata) |
| `src/mypackage/py.typed` | PEP 561 marker for type hints |
| `.readthedocs.yaml` | ReadTheDocs configuration |
| `.python-version` | pyenv virtual environment name |

## Migration from setup.py

When migrating a project from `setup.py` to the standard setup:

### Step 1: Create pyproject.toml

1. Copy the template above
2. Replace package name, description, dependencies
3. Add existing dependencies from `requirements.txt`
4. Add existing dev dependencies from `requirements.dev.txt` or `requirements-test.txt`

### Step 2: Update Project Structure

1. Move package to `src/` layout if not already there
2. Create `src/mypackage/py.typed` marker file
3. Update imports if moving to src-layout

### Step 3: Remove Old Files

Delete after migration:
- `setup.py`
- `setup.cfg`
- `tox.ini` (move config to pyproject.toml)
- `.coveragerc` (move config to pyproject.toml)
- `.pypi-template` (deprecated)

### Step 4: Update Makefile

Replace setuptools commands with modern equivalents:

| Old | New |
|-----|-----|
| `python setup.py sdist bdist_wheel` | `python -m build` |
| `coverage run -m pytest` | `pytest --cov` |

### Step 5: Verify

Run these commands to verify the migration:

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src tests

# Run type checking
mypy --strict src

# Build package
python -m build

# Check distribution
twine check dist/*
```

## Makefile Template

A minimal Makefile for development workflow:

```makefile
VENV_NAME := mypackage
PYTHON_VERSION := 3.11

.PHONY: setup install test lint typecheck build publish clean

setup:
  @if pyenv versions | grep -q "$(VENV_NAME)"; then \
    echo "Virtualenv '$(VENV_NAME)' already exists."; \
  else \
    pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME); \
  fi
  pyenv local $(VENV_NAME)

install: setup
  pip install -e ".[dev]"

test:
  pytest

lint:
  ruff check src tests

typecheck:
  mypy --strict src

check: lint typecheck

build:
  python -m build

publish: build
  twine upload dist/*

clean:
  rm -rf build/ dist/ *.egg-info
  find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
```

## ReadTheDocs Configuration

`.readthedocs.yaml`:

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: docs/conf.py

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - dev
```

## Comparison: hatchling vs setuptools.build_meta

| Aspect | hatchling | setuptools.build_meta |
|--------|-----------|----------------------|
| **Size** | 83 kB | 894 kB |
| **Dependencies** | 4 | 0 |
| **PEP 639 (license)** | ✅ Supported | ❌ Pending |
| **Package discovery** | Explicit config | Auto-discovery |
| **Gitignore support** | ✅ Default | ❌ Needs MANIFEST.in |
| **C/C++ extensions** | Via plugins | ✅ Native |
| **Configuration** | Simpler | More verbose |

## When to Keep setuptools

Keep `setuptools.build_meta` when:
- Building C/C++ extension modules
- Complex build customization that needs setuptools plugins
- Legacy codebase where migration cost outweighs benefits

## Related Skills

- `python` - Python best practices and coding conventions
- `documentation` - Sphinx documentation setup
- `pypi-publish` - Publishing to PyPI

## Sources

- [Python Packaging Guide - Build Tools](https://pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html)
- [Scientific Python - Simple Packaging](https://learn.scientific-python.org/development/guides/packaging-simple/)
- [Packaging Rundown - Coady](https://coady.github.io/posts/packaging-rundown.html)
- [Why Hatch?](https://hatch.pypa.io/latest/why/)