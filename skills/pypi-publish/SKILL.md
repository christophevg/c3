---
name: pypi-publish
description: |
  Publish Python packages to PyPI with proper checks and workflow. Use when publishing to PyPI, releasing a package, or before running twine upload. Examples: "publish to PyPI", "release to PyPI", "upload to PyPI".
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

**Note:** For complete release workflow (version bump, changelog, CI verification, tagging), use the `c3:release` skill instead.

## Version Bump Decision

Before updating version, determine bump type:

| Change Type | Bump | Example |
|-------------|------|---------|
| Bug fixes | Patch | 0.3.1 → 0.3.2 |
| New features (backward compatible) | Minor | 0.3.1 → 0.4.0 |
| Breaking changes | Major | 0.3.1 → 1.0.0 |

**Check recent commits:**

```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~10")..HEAD --oneline

# Count by type
git log $(git describe --tags --abbrev=0)..HEAD --oneline | grep -c "^.*feat:"
git log $(git describe --tags --abbrev=0)..HEAD --oneline | grep -c "^.*fix:"
```

**Decision rules:**
- `feat:` commits present → Minor bump
- Only `fix:` commits → Patch bump
- Breaking API changes detected → Major bump
- If unclear, ask owner

## Pre-Publish Checklist

**CRITICAL: Complete these checks before building.**

Before publishing, verify:

1. **README image paths use absolute URLs**:
   ```markdown
   # WRONG - won't display on PyPI
   ![Alt](media/image.svg)
   ![Alt](docs/image.png)
   
   # CORRECT - works on PyPI
   ![Alt](https://raw.githubusercontent.com/owner/repo/main/media/image.svg)
   ```
   - PyPI doesn't serve relative paths from the package
   - All images in README must use `raw.githubusercontent.com` URLs
   - Check: `grep -n '!\[.*](media/' README.md` should return nothing

2. **Hatch build configuration is correct**:
   ```toml
   # CORRECT - use this pattern:
   [tool.hatch.build.targets.wheel]
   packages = ["src/package_name"]
   
   # WRONG - conflicting configuration causes empty wheel:
   [tool.hatch.build]
   sources = ["src"]
   
   [tool.hatch.build.targets.wheel]
   packages = ["src/package_name"]  # WRONG: includes src/ when sources is set
   ```
   - Never use both `[tool.hatch.build]` sources AND `packages = ["src/..."]`
   - When `sources = ["src"]` is set, packages must be relative: `["package_name"]`
   - Or just omit `sources` and use `packages = ["src/package_name"]`

3. **Version is synced across all files**:
   ```bash
   # Check version in pyproject.toml
   grep '^version =' pyproject.toml
   
   # Check version in __init__.py
   grep '^__version__ = ' src/package/__init__.py
   ```
   - Both must match exactly
   - uv.lock will update automatically on build

4. **Build configuration is correct** in `pyproject.toml`:
   ```toml
   # CORRECT - use this pattern:
   [tool.hatch.build.targets.wheel]
   packages = ["src/package_name"]
   
   # WRONG - conflicting configuration:
   [tool.hatch.build]
   sources = ["src"]  # Don't use this with packages = ["src/..."]
   
   [tool.hatch.build.targets.wheel]
   packages = ["src/package_name"]  # WRONG when sources is set
   ```
   - Never use both `sources` and `packages` with `src/` prefix
   - Use ONE approach: either `packages = ["src/package"]` OR `sources = ["src"]` with `packages = ["package"]`

5. **Remove local development configuration**:
   ```toml
   # REMOVE before publishing:
   [tool.uv.sources]
   package-name = { path = "../local-path", editable = true }

   [tool.uv.workspace]
   members = ["packages/*"]
   ```
   - These sections cause PyPI to fail or create broken packages
   - They reference local paths that don't exist on PyPI

6. **Entry point is correct**:
   ```toml
   [project.scripts]
   package-name = "package.__main__:main"  # Must exist!
   ```
   - Check that the module and function actually exist
   - Common mistake: `package.main:cli` when file doesn't exist

7. **License format is correct**:
   ```toml
   license = "MIT"
   license-files = ["LICENSE"]
   ```
   - Avoid deprecated `{text = "MIT"}` format
   - Include a LICENSE file

8. **Version is bumped** if updating existing package

9. **Dependencies are synced**:
   - Run `uv sync --all-extras` before building

## Workflow

### Step 1: Sync Dependencies

```bash
# Sync all dependencies
uv sync --all-extras
```

### Step 2: Run Pre-Publish Checks

```bash
# Check for Makefile pre-publish target
make pre-publish

# Or manually:
make check

# Or directly:
uv run pytest -v
uv run ruff check src tests
uv run mypy src
```

### Step 3: Clean Previous Builds

```bash
make clean

# Or manually:
rm -rf dist/ build/ *.egg-info
```

### Step 5: Build Distribution Packages

```bash
# For uv-managed projects:
uv build

# Or via Makefile:
make build
```

This creates:
- `dist/<package>-<version>-py3-none-any.whl` (wheel)
- `dist/<package>-<version>.tar.gz` (source distribution)

### Step 6: Verify Package Contents (Before Upload)

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

**Best practice: Use `make publish` which runs pre-publish checks automatically.**

```bash
# Preferred: make publish runs pre-publish checks then uploads
make publish

# Alternative: Manual upload (if you ran pre-publish separately)
uv run twine upload dist/*
```

```bash
# Check for Makefile publish target
grep -A2 "^publish:" Makefile

# If exists, use it:
make publish

# Otherwise, use twine (preferred):
uv run twine upload dist/*

# Note: uv publish is unreliable - use twine instead
```

### Step 8: Create Git Tag

```bash
# Tag the release
git tag v<VERSION>

# Push the tag
git push --tags
```

### Step 9: Verify Publication

```bash
# Wait a moment for PyPI to index
open https://pypi.org/project/package_name/

# Verify install works
uv pip install package_name==VERSION
```

## Common Mistakes to Avoid

| Mistake | Symptom | Fix |
|---------|---------|-----|
| **Empty wheel** | Package installs but module not found | Check hatch `packages = ["src/package_name"]` |
| **Local paths in wheel** | PyPI upload fails or broken package | Remove `[tool.uv.sources]` and `[tool.uv.workspace]` |
| Wrong entry point | `ModuleNotFoundError` after install | Verify module exists before building |
| Old license format | Deprecation warnings | Use `license = "MIT"` with LICENSE file |
| Missing LICENSE file | Badge shows no license | Create LICENSE file |
| Not in virtualenv | Packages install to wrong Python | Run `uv sync` before building |
| Forgetting to build | Old dist files uploaded | Remove `dist/` before rebuilding |
| Version already exists | Upload fails with "File already exists" | Bump version, cannot overwrite on PyPI |
| Multiple versions in dist | Upload fails with "400 Bad Request" | Clean dist before building, or use `make publish` (if it cleans) |

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
