---
name: release
description: This skill should be used when the user asks to "release", "publish a new version", "bump version", "create a release", "prepare for release", or "tag a release". It guides the version management and release process for the C3 plugin.
version: 1.0.0
---

# Release Process for C3 Plugin

Guide for managing versions and publishing releases of the C3 plugin.

## Overview

The release process involves:
1. Determining version bump type (major, minor, patch)
2. Updating version in plugin.json
3. Updating CHANGELOG.md
4. Creating git tag
5. Pushing to GitHub

## Version Management

### Check Current Version

```bash
make version-current
```

### Bump Version

Choose the appropriate bump type:

| Type | When to Use |
|------|-------------|
| `major` | Breaking changes |
| `minor` | New features (backward-compatible) |
| `patch` | Bug fixes |

```bash
# Preview changes
make version-bump-minor

# Or use the script directly
python bin/version.py bump --part minor --dry-run
```

## Release Process

### Step 1: Ensure Clean State

```bash
git status
git diff
```

Verify all changes are committed. The working tree should be clean.

### Step 2: Update CHANGELOG.md

Review the `[Unreleased]` section in CHANGELOG.md:

- All new features should be under `### Added`
- Breaking changes under `### Changed` or `### Breaking`
- Bug fixes under `### Fixed`

### Step 3: Create Release

```bash
# For new features (backward-compatible)
make release-minor

# For bug fixes
make release-patch

# For breaking changes
make release-major
```

This will:
- Update version in `.claude-plugin/plugin.json`
- Move `[Unreleased]` content to new version section
- Add release date

### Step 4: Create Git Tag

```bash
make tag
```

This creates an annotated tag for the current version.

### Step 5: Push to GitHub

```bash
git push origin main --tags
```

## Distribution

### Plugin Installation

Users install the plugin via:

```bash
claude plugin marketplace add christophevg/marketplace
claude plugin install c3@christophe.vg
```

### Version Availability

After pushing tags, the new version is immediately available:
- GitHub release is created
- Marketplace picks up the new version
- Users can update with `claude plugin update c3`

## Checklist

Before releasing:

- [ ] All tests pass
- [ ] CHANGELOG.md has entries for all changes
- [ ] Version bump type is appropriate
- [ ] Working tree is clean (no uncommitted changes)
- [ ] You're on the main branch

After releasing:

- [ ] Tag is created and pushed
- [ ] GitHub release is created (automatic with tag)
- [ ] Plugin can be installed from marketplace

## Version Numbers

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, backward-compatible

Examples:
- `1.0.0` → `1.1.0` - New skill added
- `1.1.0` → `1.1.1` - Bug fix in existing skill
- `1.1.1` → `2.0.0` - Breaking change in skill interface