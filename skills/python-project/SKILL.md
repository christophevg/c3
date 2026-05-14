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

## Phase 0: UV Setup Validation (MANDATORY)

**CRITICAL: Validate UV setup BEFORE any implementation work.**

### Validation Checklist

Run ALL of these checks before starting work:

```bash
# 1. Check for pyproject.toml
ls pyproject.toml

# 2. Verify uv is installed
uv --version

# 3. Sync dependencies
uv sync

# 4. Verify package imports work
uv run python -c "from app import server"  # or main module

# 5. Verify tests can collect
uv run pytest --collect-only
```

**If ANY check fails, STOP and fix setup before continuing.**

### Common Issues

| Issue | Fix |
|-------|-----|
| `uv: command not found` | Install uv globally |
| `No pyproject.toml` | Run `uv init` |
| `Module not found` | Run `uv sync` |
| `ImportError` | Check `[tool.uv.sources]` paths |
| `Tests can't collect` | Install pytest: `uv add --dev pytest` |

### Pre-Implementation Gate

**DO NOT proceed to implementation until:**
- [ ] `uv sync` completes successfully
- [ ] Package imports work (`uv run python -c "..."`)
- [ ] Tests can collect (`uv run pytest --collect-only`)

**Only THEN start implementation.**

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

## Command Pattern: ALWAYS use `uv run`

**CRITICAL: ALL commands MUST use `uv run`. NEVER run commands directly.**

| Wrong | Correct |
|-------|---------|
| `pytest` | `uv run pytest` |
| `python main.py` | `uv run python main.py` |
| `black .` | `uv run black .` |
| `ruff check .` | `uv run ruff check .` |

**Why:**
- `uv run` ensures correct virtual environment
- `uv run` manages Python version automatically
- Direct commands may use wrong Python/environment

### Installation

**Single command is sufficient:**

```bash
uv sync
```

DO NOT give multiple installation commands:
- ❌ `uv sync && uv sync --extra dev && uv pip install -e .`
- ✓ `uv sync`

The `uv sync` command:
- Creates `.venv` if needed
- Installs all dependencies
- Installs dev dependencies (from `[project.optional-dependencies]`)
- Syncs to lock file

### Running Tests

```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/test_module.py

# With coverage
uv run pytest --cov=src

# Parallel execution
uv run pytest -n auto
```

### Running Application

```bash
# Web application
uv run gunicorn -k uvicorn.workers.UvicornWorker app:asgi_app

# Or via Makefile
make run
```

### Code Quality

```bash
# Format code
uv run black .
uv run ruff format .

# Lint
uv run ruff check .

# Type check
uv run mypy src/

# Or via Makefile
make check
```

## Makefile (Required)

**ALL Python projects MUST have a Makefile with uv-based targets.**

### Standard Makefile

Create `Makefile` at project root:

```makefile
include ~/.claude/Makefile

# Testing
test:
	uv run pytest

test-cov:
	uv run pytest --cov=src --cov-report=term-missing

test-all:
	uv run tox

# Code Quality
format:
	uv run black .
	uv run ruff format .

lint:
	uv run ruff check .

typecheck:
	uv run mypy src/

check: format lint typecheck test

# Running
run:
	uv run gunicorn -k uvicorn.workers.UvicornWorker app:asgi_app

# Or for CLI apps:
# run:
#     uv run python -m package_name

# Documentation
docs:
	cd docs && uv run sphinx-build -M html . _build

# All
all: check docs
```

### Makefile Requirements

| Target | Purpose | Required |
|--------|---------|-----------|
| `test` | Run tests | ✓ Required |
| `run` | Run application | ✓ Required |
| `format` | Format code | ✓ Required |
| `lint` | Lint code | ✓ Required |
| `check` | Format + lint + test | ✓ Required |
| `test-cov` | Coverage report | Recommended |
| `docs` | Build docs | If has docs |
| `all` | Complete check | Recommended |

### Why Makefile?

1. **Consistent commands** - Same `make test` across all projects
2. **uv integration** - All targets use `uv run`
3. **Onboarding** - New developers know `make check`
4. **CI/CD** - GitHub Actions can use `make check`

### Using Makefile

```bash
make test      # Run tests
make run       # Start application
make check     # Run all quality checks
make all       # Complete check (including docs)
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
| `templates/readme.md` | README with badges and standard sections |
| `templates/docs-conf.py` | Sphinx configuration and docs templates |
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

**Coverage Reporting:**

Library workflows include coverage reporting to Coveralls:

```yaml
- name: Run tests
  run: uv run pytest -v --cov=src --cov-report=xml

- name: Upload coverage to Coveralls
  uses: coverallsapp/github-action@v2
  if: matrix.python-version == '3.11' && matrix.os == 'ubuntu-latest'
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

The `if` condition ensures coverage is uploaded once (not for every matrix combination).

**Note:** `coveralls>=3.3.0` should be included in dev dependencies for coverage reporting.

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

## Entry Point Naming

**Choose script names carefully to avoid conflicts:**

| Avoid | Reason | Use Instead |
|-------|--------|-------------|
| `mcp` | Conflicts with existing MCP CLI tools | `mcp-server`, `<project>-mcp` |
| `serve` | Generic, may conflict | `<project>-serve` |
| `cli` | Too generic | `<project>-cli` |
| `main` | Not descriptive | `<project>` |

**Entry point function naming:**

```toml
# pyproject.toml
[project.scripts]
my-package = "mypackage.module:run"  # Use run(), not main()
```

```python
# src/mypackage/module.py
def run() -> None:
    """Run the application."""
    # Entry point logic

if __name__ == "__main__":
    run()
```

**Why `run()` instead of `main()`:**
- `main()` is a common pattern for scripts run directly
- `run()` is explicit for entry points called via script
- Avoids confusion with `if __name__ == "__main__"` pattern

**Avoid `__main__.py` for CLI entry points:**
- `__main__.py` makes package runnable as `python -m package`
- But entry point scripts (`my-package = "package:run"`) are preferred
- `__main__.py` is appropriate for applications, not library packages

## Standard Project Structure

**For a new Python package, create this structure:**

```
my-package/
├── pyproject.toml           # From template
├── uv.lock                   # Generated by uv sync
├── .python-version          # Pinned Python version
├── .gitignore               # Standard Python gitignore
├── LICENSE                  # MIT (or your choice)
├── README.md                 # With badges, quick start
├── .readthedocs.yaml         # ReadTheDocs config
├── .github/
│   └── workflows/
│       └── test.yml          # CI workflow
├── docs/
│   ├── conf.py               # Sphinx config
│   ├── index.rst             # Documentation index
│   ├── installation.md       # Installation guide
│   ├── api.md                # API reference
│   └── configuration.md      # Configuration docs
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── py.typed          # PEP 561 marker
│       └── module.py
├── tests/
│   ├── conftest.py
│   └── test_module.py
└── Makefile                  # From template
```

## Local Development vs PyPI Publishing

**CRITICAL: Local development configuration must be removed before PyPI publishing.**

### Local Development Configuration

When developing against local checkouts of dependencies:

```toml
# pyproject.toml - for local development ONLY
[tool.uv.sources]
baseweb = { path = "../baseweb", editable = true }
oatk = { path = "../oatk", editable = true }

[tool.uv.workspace]
members = ["packages/*"]
```

This tells uv to use local paths instead of PyPI packages.

### Before PyPI Publishing

**REMOVE these sections before building for PyPI:**

```bash
# These sections reference local paths that don't exist on PyPI
# Delete them from pyproject.toml before:
#   uv build
#   uv publish
```

| Section | Action | Why |
|---------|--------|-----|
| `[tool.uv.sources]` | Remove | References local paths |
| `[tool.uv.workspace]` | Remove | Defines workspace members |

### Workflow

```bash
# Local development:
uv add --editable ../baseweb    # Creates [tool.uv.sources]
uv sync                         # Uses local package

# Before PyPI publish:
# 1. Remove [tool.uv.sources] and [tool.uv.workspace] from pyproject.toml
# 2. Update dependencies to PyPI versions:
uv add baseweb>=0.5.0           # Uses PyPI version
uv sync
# 3. Build and publish:
uv build
uv publish --token $PYPI_TOKEN

# After publishing (for continued local dev):
# Re-add local sources:
uv add --editable ../baseweb
```

### Verify Before Publishing

```bash
# Check wheel contents for local path references
unzip -l dist/*.whl | head -30

# Should show source files, not .dist-info only
# Should NOT contain any local paths
```

## Pre-Publish Checklist

**Before publishing to PyPI, verify:**

### Code Quality
- [ ] `make all` passes (lint, test, typecheck)
- [ ] All tests pass on all Python versions (`make test-all`)
- [ ] Coverage is adequate (check `make test-cov`)

### Documentation
- [ ] `make docs` builds successfully
- [ ] README has badges (PyPI, Python, License, CI, etc.)
- [ ] README has installation and quick start sections
- [ ] README links to documentation
- [ ] All doc content is unique (no duplicates across files)

### Project Files
- [ ] LICENSE file exists
- [ ] .readthedocs.yaml configured
- [ ] .github/workflows/test.yml exists
- [ ] pyproject.toml has correct metadata
- [ ] Entry point names don't conflict with common tools

### Publishing Workflow
- [ ] Test on TestPyPI first: `make publish-test`
- [ ] Install from TestPyPI to verify: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ my-package`
- [ ] Create git tag: `git tag v0.1.0 -m "Release v0.1.0"`
- [ ] Push tag: `git push origin v0.1.0`
- [ ] Publish to PyPI: `make publish`

## Sources

- [uv Documentation](https://docs.astral.sh/uv/)
- [Python Packaging Guide](https://pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html)
- [Scientific Python - Simple Packaging](https://learn.scientific-python.org/development/guides/packaging-simple/)
- [tox Documentation](https://tox.wiki/)