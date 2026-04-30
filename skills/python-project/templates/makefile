# Makefile Template

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