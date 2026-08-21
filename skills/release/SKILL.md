---
name: release
description: |
  Standardize release preparation and publishing workflow. Use when preparing a release, publishing to PyPI, or release-manager starts release process. Handles version bump decisions, changelog updates, CI verification, tagging, and PyPI upload.
---

# Release Workflow

Standardized release preparation and publishing workflow for Python packages.

## Overview

| Step | Action | Purpose |
|------|--------|---------|
| 1 | Determine version bump | Major/minor/patch based on commits |
| 2 | Update version files | pyproject.toml, __init__.py |
| 3 | Update changelog | Document changes |
| 4 | Local pre-publish checks | Verify quality before pushing |
| 5 | Commit version bump | Record version change |
| 6 | Push | Send to remote |
| 7 | Wait for CI | Authoritative quality check |
| 8 | Build package | Create wheel and sdist |
| 9 | Verify package | Confirm contents are correct |
| 10 | Create tag | Mark release point |
| 11 | Create GitHub release | Announce release |
| 12 | Upload to PyPI | Distribute package |

## When to Use

- User asks to "prepare release" or "publish"
- Release-manager starts release process
- After PR merge, ready to release
- Version needs to be bumped and published

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
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Count by type
git log $(git describe --tags --abbrev=0)..HEAD --oneline | grep -c "^.*feat:"
git log $(git describe --tags --abbrev=0)..HEAD --oneline | grep -c "^.*fix:"
```

**Decision rules:**
- `feat:` commits present → Minor bump
- Only `fix:` commits → Patch bump
- Breaking API changes detected → Major bump
- If unclear, ask owner

## Workflow

### Step 1: Determine Version Bump

```bash
# Check current version
grep '^version =' pyproject.toml

# Check commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~10")..HEAD --oneline
```

Based on commit types, determine bump level. If uncertain, ask owner.

### Step 2: Update Version Files

**Update pyproject.toml:**
```bash
# Current: version = "0.3.1"
# New: version = "0.4.0"
```

**Update src/**/__init__.py:**
```bash
# Find __init__.py files with __version__
find src -name "__init__.py" -exec grep -l "__version__" {} \;

# Update __version__ = "0.3.1" to __version__ = "0.4.0"
```

### Step 3: Update Changelog

**Check for existing changelog:**
```bash
ls docs/changelog.md CHANGELOG.md 2>/dev/null
```

**Add release section:**
```markdown
## 0.4.0 (2026-05-26)

### Added
- Feature 1 description
- Feature 2 description

### Fixed
- Bug fix description

### Changed
- Change description
```

**Extract changes from commits:**
```bash
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~10")..HEAD --pretty=format:"- %s"
```

### Step 4: Run Local Pre-Publish Checks

```bash
# Sync dependencies
uv sync --all-extras

# Run tests
make test

# Run linting
make lint

# Run type checking
make typecheck

# Format code (if not in make lint)
ruff format src tests
```

**If any check fails:** Fix the issue before proceeding.

### Step 5: Commit Version Bump

```bash
# Stage version files
git add pyproject.toml src/**/__init__.py docs/changelog.md CHANGELOG.md uv.lock

# Commit
git commit -m "$(cat <<'EOF'
chore: bump version to X.Y.Z

- Change 1
- Change 2

🤖 Implemented together with a coding agent.
EOF
)"
```

### Step 6: Push

```bash
# Get current branch
current_branch=$(git branch --show-current)

# Push to remote
git push origin "$current_branch"
```

### Step 7: Wait for CI to Pass

**CRITICAL: Do not proceed until CI passes.**

```bash
# Check CI status
gh pr checks

# Or watch the run
gh run watch
```

**If CI fails:**
1. View failure details: `gh run view {id} --log-failed`
2. Debug and fix the issue
3. Commit and push fixes to the same branch
4. Return to Step 7 (wait for CI)

**Why wait?** If CI fails, additional fixes will be needed, resulting in new commits. Tagging should only happen after CI confirms the release is good.

### Step 8: Build Package

**Only after CI passes:**

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build
uv build
```

This creates:
- `dist/<package>-<version>-py3-none-any.whl` (wheel)
- `dist/<package>-<version>.tar.gz` (source distribution)

### Step 9: Verify Package Contents

**CRITICAL: Always verify before publishing.**

```bash
# List wheel contents
unzip -l dist/*.whl | head -40
```

**Check for:**
- Source files present (not just `.dist-info/`)
- Correct package structure
- No local path references

**If package is empty or wrong:** Fix hatch configuration, rebuild.

### Step 10: Create Annotated Tag

```bash
# Create tag with message
git tag -a vX.Y.Z -m "Release X.Y.Z: Brief Description"

# Push tag
git push origin vX.Y.Z
```

### Step 11: Create GitHub Release

```bash
# Create release with notes
gh release create vX.Y.Z \
  --title "vX.Y.Z - Brief Description" \
  --notes "$(cat <<'EOF'
## Summary

Brief description of what this release includes.

## Changes

### Added
- Feature 1
- Feature 2

### Fixed
- Bug fix 1

### Changed
- Change 1

## Installation

```bash
pip install package-name==X.Y.Z
```
EOF
)"
```

### Step 12: Upload to PyPI

**Use the granular upload target, not the full publish pipeline:**

```bash
# Upload to PyPI (if make publish was already run for pre-publish checks)
make upload

# Or directly:
uv run twine upload dist/*
```

**If the upload fails (e.g. HTTP 400):**

1. **Check PyPI first** — the upload may have partially succeeded (one file
   uploaded, the second rejected). Visit
   `https://pypi.org/project/package-name/` to verify before retrying.
2. **Do NOT re-run `make publish`** — it re-executes the entire test suite,
   build, and pre-publish cycle. Use `make upload` or
   `uv run twine upload dist/*` directly to retry just the upload.
3. **Max 3 retries** — after 3 failed attempts, stop and ask the user to
   investigate (per the retry policy in the global agent instructions).

**Verify publication:**
```bash
# Open PyPI page
open https://pypi.org/project/package-name/

# Test install
pip install package-name==X.Y.Z
```

## Quick Reference

```bash
# 1. Determine bump: git log --oneline since last tag
# 2. Update: pyproject.toml, __init__.py, changelog
# 3. Check: make test && make lint && make typecheck
# 4. Commit: git commit -m "chore: bump version to X.Y.Z"
# 5. Push: git push origin <branch>
# 6. Wait CI: gh pr checks
# 7. Build: rm -rf dist && uv build
# 8. Verify: unzip -l dist/*.whl | head -40
# 9. Tag: git tag -a vX.Y.Z -m "Release X.Y.Z"
# 10. Push tag: git push origin vX.Y.Z
# 11. GitHub release: gh release create vX.Y.Z
# 12. Upload: make upload (or uv run twine upload dist/*)
```

## Common Issues

| Issue | Solution |
|-------|----------|
| CI fails after push | Fix issue, commit, push, wait again |
| Package empty in wheel | Check hatch `packages` configuration |
| Version already on PyPI | Cannot overwrite - bump version again |
| PyPI upload returns HTTP 400 | Upload may have partially succeeded. Check `https://pypi.org/project/<name>/` before retrying. Use `make upload` (not `make publish`) to retry — avoids re-running tests. Max 3 retries, then ask user. |
| PyPI upload fails (other) | Check for `[tool.uv.sources]` in pyproject.toml |

## Related Skills

- `c3:pypi-publish` - Detailed pre-publish checklist and PyPI upload
- `c3:commit` - Commit workflow
- `c3:github` - GitHub release management
