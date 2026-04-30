---
name: project-migrate
description: Use this skill when migrating existing Python projects to the uv-based standard. Migrates pyproject.toml, Makefile, GitHub Actions, ReadTheDocs, and removes legacy files. Examples: "migrate project to uv", "update project to new standard", "modernize Python project setup".
---

# Python Project Migration to uv

Migrate existing Python projects to the uv-based standard. This skill ensures all configuration files are updated consistently.

## When to Use This Skill

Use this skill when:
- User says "migrate project to uv"
- User says "update project to new standard"
- User says "modernize Python project setup"
- Project uses legacy setup (setup.py, requirements.txt, pyenv)
- Project needs to align with python-project skill standards

## Migration Checklist

When migrating a project, verify **all** of these files:

| File | Check |
|------|-------|
| `pyproject.toml` | Dependencies, tool configs, extras |
| `Makefile` | Targets use uv commands |
| `.python-version` | Pinned Python version |
| `.readthedocs.yaml` | Python 3.12, pip install with extras |
| `.github/workflows/test.yaml` | Multi-OS, uv-based CI |
| `README.md` | Root location (not `.github/`) |
| `requirements*.txt` | **Remove** (migrated to pyproject.toml) |
| `setup.py` / `setup.cfg` | **Remove** (migrated to pyproject.toml) |
| `tox.ini` | **Remove** (migrated to pyproject.toml) |
| `.coveragerc` | **Remove** (migrated to pyproject.toml) |

## Migration Steps

### Step 1: pyproject.toml

Update to use hatchling and uv-based tool configuration:

**Required sections:**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "package-name"
version = "0.1.0"
requires-python = ">=3.10"  # Libraries: ">=3.10", Apps: ">=3.11"

[project.optional-dependencies]
dev = [
  "pytest>=8.0.0",
  "pytest-cov>=5.0.0",
  "pytest-asyncio>=0.23.0",
  "mypy>=1.13.0",
  "ruff>=0.8.0",
  "tox>=4.0.0",
  "tox-uv>=1.0.0",
  "build>=1.0.0",
]
docs = [
  "sphinx>=7.0.0",
  "sphinx-rtd-theme>=2.0.0",
  "myst-parser>=2.0.0",
]

[tool.hatch.build]
sources = ["src"]

[tool.hatch.build.targets.wheel]
packages = ["src/package_name"]

[tool.tox]
env_list = ["py310", "py311", "py312"]

[tool.tox.env_run_base]
description = "run tests with pytest"
commands_pre = [
  ["uv", "pip", "install", "-e", "."],
  ["uv", "pip", "install", "pytest", "pytest-cov", "pytest-asyncio"],
]
commands = [["pytest", "tests", "-v", "--cov=package_name", "--cov-report=term-missing"]]
```

**Verify:**
- ✅ `hatchling` as build backend
- ✅ `tox-uv` in dev dependencies
- ✅ `tox` config uses `commands_pre` workaround
- ✅ `docs` extra is **separate** from `dev` (not mixed)
- ✅ `ruff` and `mypy` tool configs present

**Critical Check:** Ensure `docs` dependencies are NOT in `dev`:

```toml
# WRONG: docs deps mixed into dev
dev = [
  "pytest>=8.0.0",
  "sphinx>=7.0.0",  # ❌ Should be in docs extra
]

# CORRECT: separate extras
dev = ["pytest>=8.0.0", ...]
docs = ["sphinx>=7.0.0", "sphinx-rtd-theme>=2.0.0", "myst-parser>=2.0.0"]
```

### Step 2: Makefile

Update to use uv commands:

```makefile
.PHONY: install install-pythons sync test lint format typecheck check tox docs build publish clean

install:
  uv sync --all-extras

install-pythons:
  uv python install 3.10 3.11 3.12

sync:
  uv sync --frozen --all-extras

test:
  uv run pytest

lint:
  uv run ruff check src tests

format:
  uv run ruff format src tests

typecheck:
  uv run mypy src

check: lint typecheck test

tox:
  uv run tox

docs:
  cd docs; uv run sphinx-build -M html . _build

build:
  uv build

publish: build
  uv publish

clean:
  rm -rf build/ dist/ *.egg-info .tox .pytest_cache .ruff_cache .mypy_cache
  find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
```

**Verify:**
- ✅ `install` uses `--all-extras`
- ✅ `install-pythons` target present
- ✅ `tox` target present with `uv run`
- ✅ `docs` target uses `sphinx-build` directly (not `make html`)
- ✅ No references to pip, pyenv, or manual venv activation

**Critical Check:** Ensure `docs` target uses `sphinx-build`:

```makefile
# WRONG: uses make html (requires docs/Makefile)
docs:
  cd docs && uv run make html

# CORRECT: uses sphinx-build directly
docs:
  cd docs && uv run sphinx-build -M html . _build
```

### Step 3: .python-version

Create or verify:

```
3.12
```

For libraries supporting multiple versions, this pins the development version.

### Step 4: .readthedocs.yaml

Update to use pip with extras:

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
        - docs
```

**Verify:**
- ✅ Python version matches project (3.10/3.11/3.12)
- ✅ Uses `pip` with `extra_requirements`
- ✅ Uses `extra_requirements: - docs` (NOT `dev`)
- ✅ **NOT** using `requirements: requirements.docs.txt`

**Critical Check:** Ensure the extra is `docs`, not `dev`:

```yaml
# WRONG: uses dev extra (installs too much)
python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - dev  # ❌ Should be "docs"

# CORRECT: uses docs extra
python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs  # ✅ Only docs dependencies
```

### Step 5: GitHub Actions

Update `.github/workflows/test.yaml`:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: ["ubuntu-latest", "macos-latest", "windows-latest"]
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --frozen --all-extras

      - name: Run tests
        run: uv run pytest -v --cov=src --cov-report=xml

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --frozen --all-extras
      - run: uv run ruff check src tests
      - run: uv run ruff format --check src tests

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --frozen --all-extras
      - run: uv run mypy src

  build:
    runs-on: ubuntu-latest
    needs: [test, lint, typecheck]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv build
```

**Verify:**
- ✅ Uses `astral-sh/setup-uv@v5`
- ✅ Multi-OS testing (Linux, macOS, Windows)
- ✅ Multi-Python testing for libraries
- ✅ `--frozen --all-extras` flags for dependency lock (installs dev dependencies)
- ✅ **All 4 jobs present:** `test`, `lint`, `typecheck`, `build`
- ✅ `build` job has `needs: [test, lint, typecheck]`

**Critical Check:** Ensure all 4 jobs exist:

```bash
# Verify all jobs are present
grep -E "^  (test|lint|typecheck|build):" .github/workflows/test.yaml
```

| Missing Job | Impact |
|-------------|--------|
| `test` | ❌ No tests run |
| `lint` | ❌ No code style checks |
| `typecheck` | ❌ No type checking |
| `build` | ❌ Package may not build correctly |

### Step 6: README.md Location

Check README location:

```bash
# If README is in .github/, move it to root
mv .github/README.md README.md
```

**Verify:**
- ✅ `README.md` exists in project root
- ✅ `pyproject.toml` has `readme = "README.md"`

### Step 7: Remove Legacy Files

Delete files that are no longer needed:

```bash
# Remove legacy dependency files
rm -f requirements.txt requirements-dev.txt requirements-test.txt requirements.docs.txt

# Remove legacy build files
rm -f setup.py setup.cfg

# Remove legacy config files (now in pyproject.toml)
rm -f tox.ini .coveragerc

# Remove .github/README.md if moved to root
rm -f .github/README.md
```

### Step 8: Verify Migration

**Run these commands to verify:**

```bash
# Clean and reinstall
rm -rf .venv
uv sync --all-extras

# Run tests
make test

# Run linters
make lint

# Run type checker
make typecheck

# Run all checks
make check

# Build package
make build

# Build docs
make docs
```

**Verify configuration files:**

```bash
# Check pyproject.toml has separate docs extra
grep -A 5 "\[project.optional-dependencies\]" pyproject.toml | grep docs

# Check .readthedocs.yaml uses docs extra (not dev)
grep "extra_requirements" .readthedocs.yaml

# Check Makefile docs target uses sphinx-build
grep "sphinx-build" Makefile

# Check GitHub Actions has all 4 jobs
grep -E "^  (test|lint|typecheck|build):" .github/workflows/test.yaml
```

**Common issues to check:**

| File | Check For | Fix |
|------|-----------|-----|
| `pyproject.toml` | `docs` deps in `dev` extra | Move to separate `docs = [...]` |
| `.readthedocs.yaml` | `extra_requirements: - dev` | Change to `- docs` |
| `Makefile` | `uv run make html` | Change to `uv run sphinx-build` |
| GitHub Actions | Missing `build` job | Add `build` job with `needs` |

## Common Migration Issues

| Issue | Solution |
|-------|----------|
| `tox` can't find Python versions | Run `make install-pythons` first |
| `ModuleNotFoundError` in tox | Use `commands_pre` workaround for tox-uv |
| `sphinx-build: command not found` | Add `docs` extra, use `uv sync --all-extras` |
| `mypy: command not found` | Add to dev dependencies, sync with `--all-extras` |
| `ruff/pytest/mypy: command not found` in CI | Use `uv sync --frozen --all-extras` in GitHub Actions |
| Coverage not finding package | Use `--cov=package_name` not `--cov=src` |

## Post-Migration

After successful migration:

1. **Commit all changes:**
   ```bash
   git add -A
   git commit -m "migrate: update project to uv-based standard"
   ```

2. **Update TODO.md:**
   - Mark migration task as complete
   - Remove any legacy-related TODO items

3. **Verify CI passes:**
   - Push to GitHub
   - Check GitHub Actions workflow passes

4. **Clean up pyenv (optional):**
   - Remove pyenv virtualenvs for this project
   - Keep pyenv installed during transition period

## Related Skills

- `python-project` — Reference standard for uv-based projects
- `python` — Python best practices and coding conventions
- `readme` — README creation and standards