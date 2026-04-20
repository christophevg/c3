# Marketplace Distribution

**Reference for:** `plugin-development` skill

---

## Marketplace Structure

A marketplace is a Git repository containing a catalog of plugins.

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json      # Required: Marketplace catalog
└── plugins/
    ├── plugin-one/
    │   └── .claude-plugin/
    │       └── plugin.json
    └── plugin-two/
        └── .claude-plugin/
            └── plugin.json
```

---

## marketplace.json Schema

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "metadata": {
    "description": "Internal development tools",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting",
      "version": "2.1.0",
      "author": { "name": "DevTools Team" },
      "category": "productivity",
      "tags": ["formatting", "style"],
      "strict": true
    }
  ]
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Marketplace identifier (used in `@name` suffix) |
| `owner` | Owner information with name and email |

### Plugin Entry Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Plugin identifier |
| `source` | Yes | Path or source specification |

---

## Plugin Sources

### Relative Path (Local)

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

### GitHub Repository

```json
{
  "name": "my-plugin",
  "source": {
    "source": "github",
    "repo": "username/repo"
  }
}
```

With specific branch or tag:

```json
{
  "name": "my-plugin",
  "source": {
    "source": "github",
    "repo": "username/repo",
    "ref": "v2.0.0"
  }
}
```

### Git URL

```json
{
  "name": "my-plugin",
  "source": {
    "source": "url",
    "url": "https://github.com/username/repo.git",
    "ref": "main"
  }
}
```

### Git Subdirectory

For repos with multiple plugins:

```json
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/username/plugins.git",
    "path": "plugins/my-plugin",
    "ref": "main"
  }
}
```

### npm Package

```json
{
  "name": "my-plugin",
  "source": {
    "source": "npm",
    "package": "@company/my-plugin",
    "version": "^2.0.0"
  }
}
```

---

## Strict Mode

| Value | Behavior |
|-------|----------|
| `true` (default) | `plugin.json` is authority; marketplace supplements |
| `false` | Marketplace entry is entire definition; conflicts cause failure |

Use `strict: false` when marketplace defines plugin metadata without a plugin.json file.

---

## Adding a Marketplace

```bash
# From GitHub
claude plugin marketplace add owner/repo

# Or in settings.json
{
  "extraKnownMarketplaces": {
    "company-name": {
      "source": {
        "source": "github",
        "repo": "company/plugins"
      }
    }
  }
}
```

### Private Repositories

For private GitHub repos, set `GITHUB_TOKEN` environment variable:

```bash
export GITHUB_TOKEN=ghp_xxx
claude plugin marketplace add company/private-plugins
```

For GitLab, use `GITLAB_TOKEN`.

---

## Plugin Lifecycle Commands

### Install

```bash
# Install from marketplace
claude plugin install plugin-name@marketplace-name

# Install from GitHub directly
claude plugin install owner/repo

# Install from local path
claude plugin install /path/to/plugin

# Install at specific scope
claude plugin install plugin-name --scope project
```

### Scopes

| Scope | Settings File | Use Case |
|-------|--------------|----------|
| `user` | `~/.claude/settings.json` | Personal (default) |
| `project` | `.claude/settings.json` | Team via VCS |
| `local` | `.claude/settings.local.json` | Project-specific (gitignored) |

### Uninstall

```bash
claude plugin uninstall plugin-name

# Keep data
claude plugin uninstall plugin-name --keep-data
```

### Enable/Disable

```bash
claude plugin enable plugin-name
claude plugin disable plugin-name
```

### Update

```bash
claude plugin update plugin-name

# Update all
claude plugin update --all
```

### List

```bash
# Installed plugins
claude plugin list

# Available in marketplace
claude plugin list --available

# JSON output
claude plugin list --json
```

---

## Version Management

### Semantic Versioning

Use `MAJOR.MINOR.PATCH`:

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes

### Pre-release Versions

```json
{
  "version": "2.0.0-beta.1"
}
```

Users can install pre-release:

```bash
claude plugin install my-plugin@2.0.0-beta.1
```

### Version Constraints

In plugin dependencies:

```json
{
  "dependencies": [
    { "name": "helper-lib", "version": "~2.1.0" }
  ]
}
```

---

## Publishing Workflow

### 1. Develop and Test

```bash
# Test locally
claude --plugin-dir /path/to/plugin

# Validate
claude plugin validate .
```

### 2. Version Bump

```bash
# For new features
npm version minor

# For bug fixes
npm version patch

# For breaking changes
npm version major
```

### 3. Update Changelog

```markdown
## [2.1.0] - 2026-04-20

### Added
- New code review skill
- Support for additional languages

### Changed
- Improved error handling

### Fixed
- Path resolution on Windows
```

### 4. Push to Repository

```bash
git add .
git commit -m "Release v2.1.0"
git tag v2.1.0
git push origin main --tags
```

### 5. Update Marketplace (if applicable)

Update `marketplace.json` with new version.

---

## Distribution Best Practices

1. **Complete metadata** before publishing
2. **Include README.md** with installation instructions
3. **Maintain CHANGELOG.md** for version history
4. **Test on clean install** without dev environment
5. **Validate** with `claude plugin validate`
6. **Document breaking changes** clearly
7. **Use pre-release versions** for testing
8. **Deprecate gracefully** before removal