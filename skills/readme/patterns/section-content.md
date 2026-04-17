# Section Content Guide

This pattern defines what content should go in each README section.

## Essential Sections (All Projects)

### Title + Description

**Purpose**: Answer "What is this?" in the first 50 words.

**Content**:
- Project name as H1 header
- One-line tagline after title
- Brief description (2-3 sentences max)

**Example**:
```markdown
# my-package

> One-line description of what the package does.

This package provides X functionality for Y use case.
```

**Common mistakes**:
- Title too long or includes version
- Description buried in paragraphs
- Missing the "why" - explain the problem it solves

---

### Badges

**Purpose**: Quick visual status overview.

**Content**:
- 5-10 badges maximum
- Position at top near description
- Make badges clickable (link to relevant page)
- Group related badges (build, coverage, license)

**Badge groups**:
1. **Build/Quality**: CI, Coverage, Quality
2. **Distribution**: PyPI, npm, etc.
3. **License**: Legal status
4. **Compatibility**: Python/Node versions, platforms

**Example**:
```markdown
[![PyPI](https://img.shields.io/pypi/v/package.svg)][pypi]
[![Python](https://img.shields.io/pypi/pyversions/package.svg)][pypi]
[![License](https://img.shields.io/github/license/user/repo.svg)][license]
```

**Common mistakes**:
- Too many badges (clutter)
- Non-clickable badges
- Outdated badge URLs

---

### Quick Start

**Purpose**: Get user running in 30 seconds or less.

**Content**:
- Maximum 3 commands
- Copy-paste ready
- Minimal prerequisites
- Shows core functionality

**Format**:
```markdown
## Quick Start

\`\`\`bash
command1
command2
command3
\`\`\`
```

**What to include**:
- Installation (one command)
- Basic usage (one command)
- Expected output (brief)

**Common mistakes**:
- Too many steps
- Missing prerequisites
- Doesn't show any functionality
- Assumes user has environment set up

---

### License

**Purpose**: Legal clarity.

**Content**:
- Type of license (MIT, Apache-2.0, GPL-3.0, etc.)
- Link to LICENSE file

**Format**:
```markdown
## License

[MIT](LICENSE)
```

**Common mistakes**:
- No license section
- License type not specified
- LICENSE file missing

---

## Python-Specific Sections

### Installation

**Purpose**: How to install the package.

**PyPI packages**:
```markdown
## Installation

\`\`\`bash
pip install package-name
\`\`\`
```

**Non-PyPI packages**:
```markdown
## Installation

\`\`\`bash
git clone https://github.com/user/repo.git
cd repo
pip install -e .
\`\`\`
```

**Common mistakes**:
- Missing dependencies
- Not mentioning Python version requirements

---

### Usage

**Purpose**: Demonstrate how to use the package.

**Content**:
- Basic usage example
- Advanced usage (optional)
- Code examples with explanations

**Format**:
```markdown
## Usage

### Basic

\`\`\`python
from package import main_thing
result = main_thing("input")
\`\`\`

### Advanced

\`\`\`python
# Advanced example
\`\`\`
```

**Common mistakes**:
- No code examples
- Examples too complex for beginners
- Missing import statements

---

### Development

**Purpose**: Guide for contributors.

**Content**:
- Requirements
- Setup instructions
- Testing commands
- Linting/formatting

**Format**:
```markdown
## Development

### Setup

\`\`\`bash
pip install -e ".[dev]"
\`\`\`

### Testing

\`\`\`bash
pytest
\`\`\`
```

---

## Web App Sections

### Tech Stack

**Purpose**: Quick overview of technologies used.

**Format**:
```markdown
## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask 3.0 |
| Frontend | Vue.js 3 |
| Database | MongoDB 6.0 |
```

---

### Environment Variables

**Purpose**: Document configuration options.

**Format**:
```markdown
## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | App secret |
| `DEBUG` | No | False | Debug mode |
```

---

### Deployment

**Purpose**: How to deploy the application.

**Content**:
- Multiple options if applicable
- Docker deployment
- Platform-specific (Heroku, AWS, etc.)

---

## Config/Tools Sections

### Files Explained

**Purpose**: Document what each file does.

**Format**:
```markdown
## Files Explained

| File | Purpose |
|------|---------|
| `config.yaml` | Main configuration |
| `settings.json` | User preferences |
```

---

### Configuration

**Purpose**: Document customization options.

**Format**:
```markdown
## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `option1` | `default1` | Description |
```

---

## Documentation Repo Sections

### File Index

**Purpose**: Quick navigation reference.

**Format**:
```markdown
## File Index

| File | Purpose |
|------|---------|
| `INDEX.md` | Navigation |
| `PLAN.md` | Overview |
```

---

### Status Tracking

**Purpose**: Show progress on documentation.

**Format**:
```markdown
## Status

| Status | Meaning |
|--------|---------|
| ✅ | Complete |
| 🚧 | In Progress |
| 📋 | Planned |
```

---

## Optional Sections

### Table of Contents

**When to use**: README over 500 words.

**Format**:
```markdown
## Table of Contents

- [About](#about)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
```

---

### Contributing

**When to use**: All projects accepting contributions.

**Format**:
```markdown
## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
```

---

### Changelog

**When to use**: PyPI packages, actively maintained projects.

**Format**:
```markdown
## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
```

---

### Acknowledgments

**When to use**: Projects using third-party code, inspired by others.

**Format**:
```markdown
## Acknowledgments

- [Project](link) - Inspiration for X
- [Library](link) - Used for Y
```

---

### Screenshots/Media

**When to use**: Web apps, GUIs, visual tools.

**Format**:
```markdown
## Screenshots

![App Name Screenshot](docs/screenshot.png)

*Caption describing what's shown*
```

**Best practices**:
- Use GIFs for workflows
- PNG for static screenshots
- Keep file sizes reasonable (< 1MB)
- Use relative paths