# Config/Tools Repository README Template

Use this template for configuration repositories, dotfile managers, skill/agent collections, etc.

```markdown
# {repo-name}

[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]

> One-line description of what this configuration/toolset provides.

## Overview

Brief description of what problem this solves and who it's for.

## Quick Install

\`\`\`bash
# Single command install if possible
make install
\`\`\`

## Requirements

- Requirement 1 (e.g., Python 3.10+)
- Requirement 2 (e.g., Claude Code CLI)

## Installation

### Step-by-Step

\`\`\`bash
# Clone
git clone https://github.com/{user}/{repo}.git
cd {repo}

# Install (symlink approach)
make install
\`\`\`

### What Gets Installed

| Component | Target | Purpose |
|-----------|--------|---------|
| Component 1 | `~/.dir/file` | Description |
| Component 2 | `~/.dir/file2` | Description |

## Configuration

### Available Options

| Option | Default | Description |
|--------|---------|-------------|
| `option1` | `default1` | What this option does |
| `option2` | `default2` | What this option does |

### Customization

\`\`\`bash
# How to customize
\`\`\`

## Usage

### Basic Usage

\`\`\`bash
# Basic commands
\`\`\`

### Advanced Usage

\`\`\`bash
# Advanced commands
\`\`\`

## Components

### Component 1

Brief description of this component.

| Item | Description |
|------|-------------|
| Item 1 | Description |
| Item 2 | Description |

### Component 2

Brief description of this component.

## Files Explained

| File | Purpose |
|------|---------|
| `file1` | What this file configures |
| `file2` | What this file configures |

## Uninstall

\`\`\`bash
make uninstall
\`\`\`

## Contributing

Contributions welcome! See guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)

[license]: LICENSE
```

## Badge Reference

For config/tools repositories:

| Badge | Markdown |
|-------|----------|
| License | `[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]` |

**Optional badges**:
- Platform: `https://img.shields.io/badge/platform-mac%20%7C%20linux%20%7C%20windows-lightgrey`

## Section Guidelines

- **Quick Install**: Goal is one command if possible
- **What Gets Installed**: Transparency about file system changes
- **Configuration**: Table format for options
- **Components**: If repo has multiple distinct components (skills, agents, etc.)
- **Files Explained**: Help users understand what each file does
- **Uninstall**: Always document how to remove the installation