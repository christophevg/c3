# Makefile Template

```makefile
.PHONY: env-dev env-run install-pythons test test-cov test-all format lint typecheck check run docs docs-view build publish publish-test clean all help

include ~/.claude/Makefile

env-dev: ## Install all dependencies (dev + docs)
	uv sync --all-extras

env-run: ## Install runtime dependencies only
	uv sync

install-pythons: ## Install all supported Python versions
	uv python install 3.10 3.11 3.12

# Testing
test: env-dev ## Run all tests
	uv run pytest -v

test-cov: env-dev ## Run tests with coverage report
	uv run pytest --cov=src --cov-report=term-missing

test-all: env-dev ## Run tests on all Python versions (tox)
	uv run tox

# Code Quality
format: env-dev ## Format code and auto-fix linting issues
	uv run ruff format src tests
	uv run ruff check --fix src tests

lint: env-dev ## Check code for linting issues
	uv run ruff check src tests

typecheck: env-dev ## Run type checking
	uv run mypy src

check: format lint typecheck test ## Run all quality checks

# Running
run: env-run ## Run the application
	uv run python -m package_name

# Documentation
docs: env-dev ## Build HTML documentation
	cd docs && uv run sphinx-build -M html . _build

docs-view: docs ## Build and open documentation in browser
	open docs/_build/html/index.html

# Building
build: env-dev ## Build distribution packages
	uv build

publish: build ## Publish to PyPI (requires credentials)
	uv publish

publish-test: build ## Publish to TestPyPI (requires credentials)
	uv publish --repository testpypi

# Cleanup
clean: ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info .pytest_cache .coverage .mypy_cache .ruff_cache
	rm -rf docs/_build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Default
all: help ## Show this help message

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | grep -v "install-pythons\|sync" | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
```

## Key Features

1. **Environment targets** - `env-dev` and `env-run` ensure dependencies are synced
2. **Help system** - `## comments` enable `make help` documentation
3. **Combined format** - Runs both `ruff format` and `ruff check --fix`
4. **docs-view** - Builds docs and opens in browser (macOS)
5. **PHONY declarations** - Prevents conflicts with files of same name
6. **Default to help** - Running `make` shows help, doesn't run checks
7. **Multi-version testing** - `test-all` runs tox across Python versions

## Usage

```bash
make              # Show help
make install-pythons  # Install Python 3.10, 3.11, 3.12 (one-time)
make env-dev      # Install all dependencies
make check        # Run all quality checks
make test         # Run tests (current Python)
make test-all     # Run tests on all Python versions
make run          # Run application
make docs-view    # Build and view docs
```