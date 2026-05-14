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

**CRITICAL: Complete these checks before building.**

Before publishing, verify:

1. **Build configuration is correct** in `pyproject.toml`:
   ```toml
   # For hatch builds:
   [tool.hatch.build.targets.wheel]
   packages = ["src/package_name"]  # NOT ["package_name"]

   # For setuptools:
   [tool.setuptools.packages.find]
   where = ["src"]
   ```
   - Wrong `packages` configuration creates empty wheels
   - Verify path matches actual source directory

2. **Remove local development configuration**:
   ```toml
   # REMOVE before publishing:
   [tool.uv.sources]
   package-name = { path = "../local-path", editable = true }

   [tool.uv.workspace]
   members = ["packages/*"]
   ```
   - These sections cause PyPI to fail or create broken packages
   - They reference local paths that don't exist on PyPI

3. **Entry point is correct**:
   ```toml
   [project.scripts]
   package-name = "package.__main__:main"  # Must exist!
   ```
   - Check that the module and function actually exist
   - Common mistake: `package.main:cli` when file doesn't exist

4. **License format is correct**:
   ```toml
   license = "MIT"
   license-files = ["LICENSE"]
   ```
   - Avoid deprecated `{text = "MIT"}` format
   - Include a LICENSE file

5. **Version is bumped** if updating existing package

6. **Virtual environment is activated**:
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

### Step 4: Clean Previous Builds

```bash
rm -rf dist/ build/ *.egg-info
```

### Step 5: Build Distribution Packages

```bash
# For uv-managed projects:
uv build

# For hatch projects:
hatch build

# For setuptools:
python -m build
```

This creates:
- `dist/<package>-<version>-py3-none-any.whl` (wheel)
- `dist/<package>-<version>.tar.gz` (source distribution)

### Step 6: Verify Package Contents

**CRITICAL: Always verify before publishing.**

```bash
# List wheel contents
unzip -l dist/*.whl | head -30
```

**Check for:**
- Source files present (not just `.dist-info/`)
- Correct package structure
- No local path references

**Example of good output:**
```
Archive:  package_name-1.0.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
      123  2024-01-01 00:00   package_name/__init__.py
     4567  2024-01-01 00:00   package_name/module.py
```

**Example of bad output (empty package):**
```
Archive:  package_name-1.0.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
       42  2024-01-01 00:00   package_name-1.0.0.dist-info/METADATA
```

If the wheel is empty (only `.dist-info/` files), the `packages` configuration is wrong.

### Step 7: Upload to PyPI

```bash
uv publish --token $PYPI_TOKEN

# Or with twine:
twine upload dist/*
```

### Step 8: Verify Publication

```bash
# Wait a moment for PyPI to index
open https://pypi.org/project/package_name/

# Verify install works
pip install package_name==VERSION
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
| **Empty wheel** | Package installs but module not found | Check hatch `packages = ["src/package_name"]` |
| **Local paths in wheel** | PyPI upload fails or broken package | Remove `[tool.uv.sources]` and `[tool.uv.workspace]` |
| Wrong entry point | `ModuleNotFoundError` after install | Verify module exists before building |
| Old license format | Deprecation warnings | Use `license = "MIT"` with LICENSE file |
| Missing LICENSE file | Badge shows no license | Create LICENSE file |
| Not in virtualenv | Packages install to wrong Python | Check `.python-version`, activate first |
| Forgetting to build | Old dist files uploaded | Remove `dist/` before rebuilding |
| Version already exists | Upload fails with "File already exists" | Bump version, cannot overwrite on PyPI |

### Empty Wheel (No Source Files)

**Most common issue when migrating to src layout.**

Symptom: Package installs but `import package` fails with `ModuleNotFoundError`

Cause: Wrong hatch `packages` configuration

Fix:
```toml
# Wrong (references project root):
[tool.hatch.build.targets.wheel]
packages = ["baseweb"]

# Correct (references src directory):
[tool.hatch.build.targets.wheel]
packages = ["src/baseweb"]
```

Verification:
```bash
unzip -l dist/*.whl | head -30
# Should show source files, not just .dist-info/
```

### Invalid URL Error on Upload

Symptom: PyPI rejects upload with "Invalid URL" error

Cause: `[tool.uv.sources]` or `[tool.uv.workspace]` still in pyproject.toml

Fix: Remove these sections before publishing - they reference local paths that don't exist on PyPI

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