# README Best Practices Reference

This reference consolidates best practices for README.md files.

## Essential Sections

Every README should include these core sections in order:

| Section | Purpose | Priority |
|---------|---------|----------|
| **Header** | Logo, title, one-line description, badges | Required |
| **About The Project** | What it does and why it exists | Required |
| **Quick Start** | 30-second setup instructions | Required |
| **Usage** | Basic usage examples with code | Required |
| **License** | Legal clarity | Required |
| **Contributing** | How to contribute | Recommended |
| **Roadmap** | Future plans | Optional |
| **Acknowledgments** | Credits and resources | Optional |
| **Table of Contents** | Navigation for longer READMEs | Recommended (500+ words) |

## The First 50 Words

**Critical**: The first 50 words answer: What is this? Why is it different? Who is it for?

**Good example**:
```markdown
# my-package

[![PyPI](https://img.shields.io/pypi/v/my-package.svg)][pypi]

> A fast, lightweight library for processing X with Y support.

my-package provides a simple API for X with features like Y and Z.
Designed for developers who need reliable X handling with minimal setup.
```

**Bad example**:
```markdown
# my-package

This is a package that I wrote because I needed something to process X.
It took me a while to figure out the best way to do this, but eventually...
```

## Project Type Variations

### Python Libraries (PyPI)

**Required sections**:
1. Project description + screenshot/GIF
2. Installation (all supported platforms)
3. Usage with code examples
4. Dependencies/Used technologies
5. Features
6. Contributing
7. Contributors
8. Author info
9. Changelog
10. License

**Badge recommendations**:
- PyPI version
- Python versions
- Coverage
- License
- CI status (optional)

**Modern Python structure**:
```
my-package/
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── core.py
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
```

---

### Python Libraries (Non-PyPI)

**Required sections**:
1. Project description
2. Requirements (Python version, dependencies)
3. Installation from source
4. Usage with code examples
5. Development
6. Project structure
7. License

**Badge recommendations**:
- License
- CI status (optional)

**Focus**:
- Source installation instructions
- Development setup
- Why not on PyPI (internal tool, prototype, etc.)

---

### Configuration/Tools Repositories

**Required sections**:
1. Purpose statement - Why this configuration exists
2. One-line setup - e.g., `sh -c "$(curl -fsLS get.chezmoi.io)"`
3. Configuration options - Table or structured list
4. Prerequisites - Dependencies, versions
5. Integration guide - How to use with existing setup

**Template structure**:
```markdown
## Overview
[What problem this solves]

## Quick Install
[Single command if possible]

## Requirements
[List prerequisites]

## Configuration
[How to customize]

## Usage Examples
[Before/after scenarios]

## Files Explained
[What each config file does]
```

**Examples**:
- chezmoi: One-line install, OS-specific guides
- Puppet Control Repo: Environment-specific sections

---

### Web Applications (Jekyll, Static Sites)

**Required sections**:
1. Overview
2. Tech stack
3. Quick start (local development)
4. Directory structure
5. Configuration
6. Deployment instructions
7. Plugins used
8. License

**Jekyll structure**:
```
├── _config.yml      # Configuration
├── _data/           # Site data
├── _drafts/         # Unpublished posts
├── _includes/       # Reusable partials
├── _layouts/        # Template wrappers
├── _posts/          # Blog posts
├── _sass/           # SASS partials
└── index.html       # Homepage
```

**Focus**:
- Local development setup
- Deployment instructions
- Screenshot/GIF of the live site
- Environment variables

---

### Documentation-Only Projects

**Required sections**:
1. What this is
2. Navigation (link to main docs, API reference, tutorials)
3. Contributing
4. Local setup (how to build/view docs)
5. Style guide (writing conventions)

**Focus**:
- Navigation and organization
- Contribution guidelines
- Less emphasis on installation

---

## Badge Best Practices

### Count

**Maximum 10 badges**. More creates clutter and reduces impact.

**Priority order**:
1. Distribution (PyPI, npm, Docker)
2. Build/Quality (CI, Coverage)
3. License
4. Documentation
5. Compatibility

### Placement

**Position at top** above or near the description.

```markdown
# Project Name

[![Badge 1][link1]][ref1]
[![Badge 2][link2]][ref2]

> Description

## About
```

### Clickability

**Always make badges clickable** using reference-style links:

```markdown
[![PyPI](https://img.shields.io/pypi/v/package.svg)][pypi]

<!-- Later in file -->
[pypi]: https://pypi.org/project/package/
```

### Grouping

Group related badges together:
- Distribution badges together
- Quality badges together
- Legal badges together

### Color Conventions

| Color | Meaning |
|-------|---------|
| `brightgreen` | Passing/success |
| `green` | Good |
| `yellowgreen` | Warning |
| `yellow` | In progress |
| `orange` | Attention |
| `red` | Critical/failure |
| `blue` | Informational |
| `lightgrey` | Neutral |

---

## Structure Patterns

### Modern README Template

```markdown
<div align="center">
  <img src="logo.png" width="120" />
  <h1>Project Name</h1>
  <p><strong>One-line value proposition</strong></p>

  [![Badge 1][badge1]][link1]
  [![Badge 2][badge2]][link2]
</div>

<div align="center">
  <img src="demo.gif" width="600" />
</div>

## Table of Contents
- [About](#about)
- [Quick Start](#quick-start)
- [Features](#features)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## About
[What and why — include "Why this project" section with emotional connection]

## Quick Start
\`\`\`bash
# Step 1
# Step 2
# Step 3
\`\`\`

## Features
| Feature | Description |
|---------|-------------|
| X | Does Y |

## Usage
[Code examples with explanations]

## Documentation
[Links to detailed docs]

## Contributing
[Invitation + steps]

## License
[License type]

<p align="right">(<a href="#table-of-contents">back to top</a>)</p>
```

### Formatting Best Practices

- **Use tables instead of bullet lists** for features (better scanability)
- **Code blocks** for all installation/usage commands
- **Numbered steps** for sequential instructions
- **Anchor links** `(#section-name)` for internal navigation
- **Back to top links** after each section
- **Collapsed sections** `<details><summary>` for secondary info

### Length Guidelines

- **Sweet spot**: 500-1,500 words
- Long enough to be comprehensive
- Short enough to be readable
- Use collapsible sections for detailed info

---

## Maintenance Solutions

### The Problem

READMEs drift from reality because:
- Manual updates are forgotten
- Version numbers become stale
- Installation instructions break
- Badges show outdated status

### Solution 1: HTML Comment Markers

Isolate auto-updated sections:

```markdown
<!-- STATS_START -->
![Stars](https://img.shields.io/github/stars/user/repo)
![Issues](https://img.shields.io/github/issues/user/repo)
<!-- STATS_END -->

Manual content here remains untouched.
```

**Advantages**:
- Uses `GITHUB_TOKEN` (no PAT management)
- Always has write access to its own repo
- Public repo data readable without tokens

### Solution 2: GitHub Actions Workflow

```yaml
name: Sync README
on:
  schedule:
    - cron: '30 9 * * *'  # 09:30 UTC (after source updates)
permissions:
  contents: write
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python sync_readme.py
      - run: |
          git config user.name "github-actions[bot]"
          git commit -am "chore: sync README stats" || exit 0
          git push
```

**Timing**: Stagger schedules — if source updates at 09:00, sync at 09:30+.

### Solution 3: Pre-Commit Hooks

Automate quality checks:

- **markdownlint-cli2** — Markdown syntax validation
- **lychee-action** — Dead link detection
- Badge image validation

---

## 2026-Specific Considerations

### LLM-Ready Documentation

Add `llms.txt` files to help AI assistants understand your project:
- **`llms.txt`** — Short summary at repo root
- **`llms-full.txt`** — Detailed context
- Follows the [llms.txt standard](https://llmstxt.org/)

### SEO Optimization

- Primary keyword in first 50 words
- Secondary keywords in section headers
- Descriptive alt text for images
- FAQ/Troubleshooting section for long-tail keywords
- Proper GitHub topics in About section

---

## Common Mistakes to Avoid

| Mistake | Solution |
|---------|----------|
| Wall of text without formatting | Use headers, lists, tables |
| No preview image or demo | Add screenshot/GIF |
| Too-long READMEs without collapsible sections | Use `<details>` for details |
| Missing badges | Add relevant badges at top |
| Complex setup instructions | Aim for 3-command quick start |
| Hardcoded secrets in examples | Use environment variables |
| No license file | Add LICENSE file |
| Dead links | Validate monthly |
| Empty GitHub About section | Add description and topics |

---

## Template-Ready Patterns

### Minimal Template (All Project Types)

```markdown
# Project Name
> One-line description

[Badges]

## Installation
\`\`\`bash
command
\`\`\`

## Usage
\`\`\`python
example
\`\`\`

## License
MIT
```

### Python Library Template

```markdown
# package-name
[![PyPI](https://img.shields.io/pypi/v/package-name.svg)][pypi]
[![Python](https://img.shields.io/pypi/pyversions/package-name.svg)][pypi]
[![License](https://img.shields.io/github/license/user/package-name.svg)][license]

> Short description of what the package does.

## Installation

\`\`\`bash
pip install package-name
\`\`\`

## Quick Start

\`\`\`python
from package_name import main_thing

result = main_thing("input")
\`\`\`

## Documentation

Full docs: https://package-name.readthedocs.io

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[MIT](LICENSE)

[pypi]: https://pypi.org/project/package-name/
[license]: LICENSE
```

---

## Sources

- GitHub README Template: The Complete 2026 Guide
- Building a Python Library in 2026
- GitHub README Best Practices: How to Write a README That Gets Stars
- Best-README-Template (othneildrew)
- Creating Great README Files for Your Python Projects (Real Python)
- Publishing Python Packages to PyPI: Complete Guide
- Configuration Repository Guide (Pullbase)
- Best Practices for GitHub Markdown Badges
- Cross-Repo README Sync with GitHub Actions
- awesome-readme-template (Louis3797)
- Stop Writing README Files by Hand: Auto-Generate API Docs on Every Merge