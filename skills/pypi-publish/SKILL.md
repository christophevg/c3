---
name: pypi-publish
description: Publish Python packages to PyPI with proper checks and workflow. Use when publishing to PyPI, releasing a package, or before running twine upload. Examples: "publish to PyPI", "release to PyPI", "upload to PyPI".
---

# pypi-publish

Publish Python packages to PyPI with proper checks and workflow.

## Overview

| Capability | Description |
|------------|-------------|
| Pre-publish validation | Verify entry points, license, version |
| Build workflow | Step-by-step build and upload process |
| Common mistakes | Troubleshooting table for common issues |
| Badge integration | README badges for published packages |

## When to Use

- Publishing a new version to PyPI
- Before running `twine upload`
- After building a Python package
- User asks to "publish to PyPI" or "release to PyPI"

## Pre-Publish Checklist

Before publishing, verify:

1. **Entry point is correct** in `pyproject.toml`:
   ```toml
   [project.scripts]
   package-name = "package.__main__:main"  # Must exist!
   ```
   - Check that the module and function actually exist
   - Common mistake: `package.main:cli` when file doesn't exist

2. **License format is correct**:
   ```toml
   license = "MIT"
   license-files = ["LICENSE"]
   ```
   - Avoid deprecated `{text = "MIT"}` format
   - Include a LICENSE file

3. **Version is bumped** if updating existing package

4. **Virtual environment is activated**:
   - Check for `.python-version` file
   - Activate: `source ~/.pyenv/versions/<name>/bin/activate`

## Workflow

### Step 1: Activate Virtual Environment

```bash
# Check for .python-version
cat .python-version 2>/dev/null

# If exists, activate
source ~/.pyenv/versions/<name>/bin/activate
```

### Step 2: Install Build Dependencies

```bash
pip install -e ".[dev]"
```

### Step 3: Run Tests (if they exist)

```bash
pytest tests/ -v
```

### Step 4: Build Distribution Packages

```bash
python -m build
```

This creates:
- `dist/<package>-<version>-py3-none-any.whl` (wheel)
- `dist/<package>-<version>.tar.gz` (source distribution)

### Step 5: Verify Package

```bash
# Check the wheel contents
unzip -l dist/*.whl

# Verify entry points
python -c "import <package>; print('OK')"
```

### Step 6: Upload to PyPI

```bash
twine upload dist/*
```

### Step 7: Verify Publication

```bash
# Wait a few seconds for PyPI to index
pip install <package> --dry-run
```

## Common Mistakes to Avoid

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Wrong entry point | `ModuleNotFoundError` after install | Verify module exists before building |
| Old license format | Deprecation warnings | Use `license = "MIT"` with LICENSE file |
| Missing LICENSE file | Badge shows no license | Create LICENSE file |
| Not in virtualenv | Packages install to wrong Python | Check `.python-version`, activate first |
| Forgetting to build | Old dist files uploaded | Remove `dist/` before rebuilding |

## Badge URLs

After publishing, add badges to README:

```markdown
[![PyPI version](https://badge.fury.io/py/<package>.svg)](https://badge.fury.io/py/<package>)
[![PyPI downloads](https://img.shields.io/pypi/dm/<package>.svg)](https://pypistats.org/packages/<package>)
[![License](https://img.shields.io/github/license/<user>/<repo>)](https://github.com/<user>/<repo>/blob/master/LICENSE)
```

Use shields.io endpoints for dynamic badges.

## Related Skills

- python - Python development guidance
- commit - Commit workflow after publishing
- bug-fixing - Debug publication issues