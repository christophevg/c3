---
name: project-migrate
description: |
  Use this skill when migrating existing Python projects to the uv-based standard. Migrates pyproject.toml, Makefile, GitHub Actions, ReadTheDocs, and removes legacy files. Examples: "migrate project to uv", "update project to new standard", "modernize Python project setup", "add uv support to old project", "bring project up to standard", "setup uv for existing project", "convert legacy setup to uv".
---

# Python Project Migration to uv

Migrate existing Python projects to the uv-based standard. This skill ensures all configuration files are updated consistently.

## When to Use This Skill

Use this skill when:
- User says "migrate project to uv"
- User says "update project to new standard"
- User says "modernize Python project setup"
- User says "add uv support to old project"
- User says "bring project up to standard"
- User says "setup uv for existing project"
- User mentions "old project" with "uv" or "Makefile"
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

**Required sections (in order):**

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
skip_install = false
commands_pre = [
  ["uv", "pip", "install", "-e", "."],
  ["uv", "pip", "install", "pytest", "pytest-cov", "pytest-asyncio"],
]
commands = [["pytest", "tests", "-v", "--cov=package_name", "--cov-report=term-missing"]]

[tool.ruff]
line-length = 100
target-version = "py310"
indent-width = 2

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["package_name"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

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
```

**Verify:**
- ✅ `hatchling` as build backend
- ✅ `tox-uv` in dev dependencies
- ✅ `tox` config uses `commands_pre` workaround
- ✅ `docs` extra is **separate** from `dev` (not mixed)
- ✅ `ruff` and `mypy` tool configs present
- ✅ Hatch build config is correct (no conflicting `sources` and `packages`)

**Critical Check:** Don't use conflicting hatch build configuration:

```toml
# WRONG - causes empty wheel:
[tool.hatch.build]
sources = ["src"]

[tool.hatch.build.targets.wheel]
packages = ["src/package_name"]  # src/ prefix conflicts with sources

# CORRECT - use ONE approach:
[tool.hatch.build.targets.wheel]
packages = ["src/package_name"]

# OR (alternative):
[tool.hatch.build]
sources = ["src"]

[tool.hatch.build.targets.wheel]
packages = ["package_name"]  # No src/ prefix when sources is set
```
- ✅ Sections in correct order (see python-project skill)

**Section Order (Standard):**
1. `[build-system]`
2. `[project]`
3. `[project.optional-dependencies]`
4. `[project.urls]`
5. `[project.scripts]`
6. `[tool.hatch.build.targets.wheel]`
7. `[tool.pytest.ini_options]`
8. `[tool.mypy]`
9. `[tool.ruff]`
10. `[tool.ruff.lint]`
11. `[tool.ruff.lint.isort]`
12. `[tool.ruff.format]`
13. `[tool.coverage.run]`
14. `[tool.coverage.report]`
15. `[tool.tox]`

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

Update to use the standard Makefile format:

```makefile
-include ~/.yoker/Makefile

.PHONY: env-dev env-run install-pythons test test-cov test-all format lint typecheck check run docs docs-view build publish publish-test clean clean-all help

## Environment

env-dev: ## Install all dependencies (dev + docs)
	uv sync --all-extras

env-run: ## Install runtime dependencies only
	uv sync

install-pythons: ## Install Python 3.10, 3.11, 3.12
	uv python install 3.10 3.11 3.12

## Testing

test: env-dev ## Run tests (usage: make test / optional: TEST=file|file:test_name)
	uv run pytest -v $(TEST)

test-cov: env-dev ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing $(TEST)

test-all: env-dev ## Run tests on all Python versions
	uv run tox

## Code Quality

format: env-dev ## Format code and fix linting issues
	uv run ruff format src tests
	uv run ruff check --fix src tests

lint: env-dev ## Check code for linting issues
	uv run ruff check src tests

typecheck: env-dev ## Run type checking
	uv run mypy src

check: format lint typecheck test ## Run all quality checks

## Running

run: env-run ## Run the application
	uv run python -m package_name

## Documentation

docs: env-dev ## Build HTML documentation
	cd docs && uv run sphinx-build -M html . _build

docs-view: docs ## Build and open documentation in browser
	open docs/_build/html/index.html

## Build & Publish

build: ## Build distribution packages
	uv build

publish: build ## Publish to PyPI
	uv run twine upload dist/*

publish-test: build ## Publish to TestPyPI
	uv run twine upload --repository testpypi dist/*

## Cleanup

clean: ## Remove build artifacts
	rm -rf dist/ build/ *.egg-info .pytest_cache .coverage .mypy_cache .ruff_cache
	rm -rf docs/_build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

clean-all: clean ## Remove virtualenv and lock file
	rm -rf .venv uv.lock

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | grep -v "install-pythons\|sync" | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
```

**Verify:**
- ✅ `env-dev` uses `--all-extras`
- ✅ `install-pythons` target present
- ✅ `test-all` target present with `uv run tox`
- ✅ `docs` target uses `sphinx-build` directly
- ✅ `check` runs format, lint, typecheck, test in order
- ✅ No references to pip, pyenv, or manual venv activation
- ✅ Help system with `## comments`

**Critical Check:** Ensure `docs` target uses `sphinx-build`:

```makefile
# WRONG: uses make html (requires docs/Makefile)
docs:
  cd docs && uv run make html

# CORRECT: uses sphinx-build directly
docs: env-dev ## Build HTML documentation
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

# Check Makefile has standard targets
grep -E "^(env-dev|env-run|install-pythons|test|test-cov|test-all|format|lint|typecheck|check|run|docs|docs-view|build|publish|clean|clean-all|help):" Makefile

# Check Makefile check order
grep -A1 "^check:" Makefile | grep "format lint typecheck test"

# Check GitHub Actions has all 4 jobs
grep -E "^  (test|lint|typecheck|build):" .github/workflows/test.yaml
```

**Common issues to check:**

| File | Check For | Fix |
|------|-----------|-----|
| `pyproject.toml` | `docs` deps in `dev` extra | Move to separate `docs = [...]` |
| `pyproject.toml` | Missing `ruff.format` section | Add `[tool.ruff.format]` section |
| `pyproject.toml` | Wrong section order | Reorder to standard sequence |
| `.readthedocs.yaml` | `extra_requirements: - dev` | Change to `- docs` |
| `Makefile` | `uv run make html` | Change to `sphinx-build -M html . _build` |
| `Makefile` | Non-standard target names | Rename to `env-dev`, `env-run`, `check` |
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

4. **Clean up legacy files (optional):**
   - Remove any remaining pyenv-related `.python-version` files
   - Project now uses uv's `.python-version` format

## Related Skills

- `python-project` — Reference standard for uv-based projects
- `python` — Python best practices and coding conventions
- `readme` — README creation and standards
