---
name: python-project
description: Use this skill when setting up or managing Python projects with uv-based tooling. Examples: "uv init my-app", "migrate setup.py to uv", "add pytest to project".
---

# Python Project Setup with uv

Standard Python project setup using `uv` as the unified tool for dependency management, virtual environments, and Python version management.

## Prerequisites

**Install uv globally before using this skill:**

```bash
# macOS (recommended)
brew install uv

# Or via official installer (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

**Why global installation?** `uv` manages Python versions and virtual environments per-project. It should be available system-wide, not installed in a project's virtual environment.

**Before using uv commands, verify it's available:** `which uv` or `uv --version`

## Why uv?

`uv` replaces multiple tools with a single fast solution (10-100x faster than pip):

| Replaces | Benefit |
|----------|---------|
| pip, pip-tools | 10-100x faster package resolution |
| virtualenv, venv | Built-in, automatic management |
| pyenv, pyenv-virtualenv | Built-in Python version management |
| poetry | Simpler configuration |
| pipx | `uvx` command for one-off tools |

## Virtual Environment Strategy

**One `.venv` per project.** No manual activation — use `uv run`.

| Context | Command |
|---------|---------|
| Running code | `uv run python main.py` |
| Running tests | `uv run pytest` |
| Running linters | `uv run ruff check src/` |
| Multi-version testing | `uv run tox` |
| One-off scripts | `uv run --with pandas script.py` |
| System-wide tools | `uvx ruff check .` |

**Never manually:**
- ❌ Create virtual environments (`python -m venv`)
- ❌ Activate environments (`source .venv/bin/activate`)
- ❌ Create multiple environments per project
- ❌ Use `requirements.txt` files

## Python Version Support

| Project Type | Python Versions | `requires-python` |
|--------------|-----------------|-------------------|
| Libraries | 3.10, 3.11, 3.12 | `>=3.10` |
| Applications | 3.11 | `>=3.11` |

## Project Initialization

```bash
# Create new application
uv init my-app && cd my-app

# Create new library
uv init --lib my-library && cd my-library

# Initialize existing project
cd existing-project && uv init
```

### Project Structure

```
my-project/
├── pyproject.toml      # All configuration
├── uv.lock              # Locked dependencies (commit this!)
├── .python-version     # Pinned Python version
├── .venv/               # Auto-managed (gitignore)
├── src/my_package/
│   ├── __init__.py
│   └── py.typed        # PEP 561 marker
└── tests/
    ├── conftest.py
    └── test_*.py
```

### Add Dependencies

```bash
uv add fastapi uvicorn      # Production
uv add --dev pytest ruff    # Development
uv add --optional docs sphinx  # Optional (libraries)
```

## Daily Commands

### Running and Testing

```bash
uv run python main.py                    # Run application
uv run pytest                            # Run all tests
uv run pytest tests/test_module.py       # Run specific file
uv run pytest -n auto                    # Run in parallel
uv run pytest --cov=src --cov-report=term-missing  # With coverage
```

### Code Quality

```bash
uv run ruff check src/         # Lint
uv run ruff check --fix src/   # Auto-fix
uv run ruff format src/        # Format
uv run mypy src/               # Type check
```

### Dependency Management

```bash
uv add package-name                 # Add dependency
uv remove package-name              # Remove dependency
uv sync                             # Sync to lock file
uv sync --frozen                    # Verify lock is current
uv lock --upgrade                   # Update all deps
uv lock --upgrade-package pkg       # Update specific dep
```

### Python Version Management

```bash
uv python install 3.12     # Install Python version
uv python pin 3.12         # Pin for project
uv python list             # List available versions
```

### Multi-Version Testing with tox

**One-time setup — install all required Python versions:**

```bash
uv python install 3.10 3.11 3.12
# Or with Makefile:
make install-pythons
```

**Run tests across all versions:**

```bash
uv run tox              # All configured environments
uv run tox -e py310     # Specific version
uv run tox -e py311
uv run tox -e py312
uv run tox parallel     # Parallel execution
```

**How it works:**

| Tool | Role |
|------|------|
| `uv python install` | Installs Python versions (no pyenv needed) |
| `tox` | Creates temporary isolated environments for each version |
| `uv run tox` | Runs tox using the project's virtual environment |

**Note:** tox creates and manages its own environments in `.tox/` — you don't create them manually. They're cleaned up automatically.

### Project Management

```bash
uv build          # Build package
uv publish        # Publish to PyPI
uvx ruff check .  # Run one-off tools
```

## Template Files

Complete templates for project configuration:

| Template | Description |
|----------|-------------|
| `templates/pyproject-library.toml` | Full pyproject.toml for libraries |
| `templates/makefile` | Development workflow Makefile |
| `templates/github-actions-app.yml` | CI workflow for applications |
| `templates/github-actions-lib.yml` | CI workflow for libraries |

## GitHub Actions CI

Run tests automatically on push. Create `.github/workflows/test.yml`:

**Key settings:**

| Setting | Purpose |
|---------|---------|
| `matrix.os` | Test on Linux, macOS, Windows |
| `matrix.python-version` | Test multiple Python versions (libraries) |
| `--frozen` | Fail if lock file is out of date |
| `on: push` | Run on every push |
| `on: [push, pull_request]` | Also run on PRs (libraries) |

See `templates/github-actions-app.yml` and `templates/github-actions-lib.yml` for complete workflows.

## ReadTheDocs Configuration

`.readthedocs.yaml`:

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

**Critical:** Always use `extra_requirements: - docs` (never `dev`):

| Wrong | Correct |
|-------|---------|
| `extra_requirements: - dev` | `extra_requirements: - docs` |
| Installs all dev tools unnecessarily | Only installs Sphinx dependencies |
| Slower builds, larger environment | Minimal, focused environment |

## Building Documentation

Documentation uses Sphinx with the ReadTheDocs theme. Define docs dependencies in `pyproject.toml`:

```toml
[project.optional-dependencies]
docs = [
  "sphinx>=7.0.0",
  "sphinx-rtd-theme>=2.0.0",
  "myst-parser>=2.0.0",
]
```

**Build documentation locally:**

```bash
# Sync docs dependencies
uv sync --extra docs

# Build HTML docs (use sphinx-build directly)
cd docs; uv run sphinx-build -M html . _build
```

**Note:** Use `sphinx-build` directly instead of `make html` — it works without requiring a `docs/Makefile`.

## Migration from Legacy Setup

When migrating from `setup.py`, `requirements.txt`, or other legacy approaches:

1. **Initialize:** `cd existing-project && uv init`
2. **Add dependencies:** `uv add <packages>` from requirements.txt
3. **Add dev dependencies:** `uv add --dev pytest ruff mypy`
4. **Update structure:** Move to `src/` layout, add `py.typed`
5. **Remove old files:** setup.py, setup.cfg, requirements*.txt, tox.ini, .coveragerc
6. **Verify:** `uv sync && uv run pytest && uv run ruff check src`

## Comparison: uv vs Legacy Tools

| Aspect | uv | Legacy (pip + pyenv) |
|--------|-----|---------------------|
| Speed | 10-100x faster | Baseline |
| Virtual envs | Automatic | Manual |
| Python versions | Built-in | Requires pyenv |
| Lock files | Built-in | Requires pip-tools |
| Config files | One (pyproject.toml) | Multiple |

## When to Use Alternatives

| Scenario | Tool |
|----------|------|
| Data science with C/Fortran libs | Conda |
| Legacy project maintenance | Keep existing setup |
| Team using Poetry | Stay with Poetry |

## Related Skills

- `python` - Python best practices and coding conventions
- `documentation` - Sphinx documentation setup
- `pypi-publish` - Publishing to PyPI

## Sources

- [uv Documentation](https://docs.astral.sh/uv/)
- [Python Packaging Guide](https://pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html)
- [Scientific Python - Simple Packaging](https://learn.scientific-python.org/development/guides/packaging-simple/)
- [tox Documentation](https://tox.wiki/)