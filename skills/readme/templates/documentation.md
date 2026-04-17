# Documentation Repository README Template

Use this template for documentation-only repositories (plans, research, knowledge bases).

```markdown
# {repo-name}

[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]

> One-line description of what this documentation covers.

## Overview

Brief description of the purpose and scope of this documentation.

## What's Inside

| Section | Description |
|---------|-------------|
| Section 1 | Description of section 1 |
| Section 2 | Description of section 2 |
| Section 3 | Description of section 3 |

## File Index

| File | Purpose |
|------|---------|
| `INDEX.md` | Main navigation |
| `PLAN.md` | Overall plan/roadmap |
| `TODO.md` | Task backlog |

## Quick Start

### Reading the Docs

Start with `INDEX.md` for navigation, or `PLAN.md` for the overview.

### Contributing

1. Follow the structure guidelines
2. Use consistent formatting
3. Update the index when adding new files

## Structure

\`\`\`
{repo-name}/
├── README.md        # This file
├── INDEX.md         # Navigation index
├── PLAN.md          # Overall plan
├── TODO.md          # Task backlog
├── section1/
│   ├── topic1.md
│   └── topic2.md
└── section2/
    └── topic3.md
\`\`\`

## Organization Principles

1. **Hierarchical** - Topics organized by category
2. **Cross-linked** - Related documents reference each other
3. **Status-tracked** - TODOs and progress documented

## Status Tracking

| Status | Meaning |
|--------|---------|
| ✅ | Complete |
| 🚧 | In Progress |
| 📋 | Planned |
| ❌ | Blocked |

## Contributing

### Adding New Documentation

1. Create file in appropriate directory
2. Add frontmatter with status
3. Update INDEX.md
4. Cross-link related documents

### Formatting Guidelines

- Use two-space indentation
- Include status in frontmatter
- Add "Back to top" links for long documents

## Navigation

| From | To |
|------|----|
| Start | `INDEX.md` → `PLAN.md` |
| Topics | `INDEX.md` → specific topic |
| Tasks | `TODO.md` |

## License

[MIT](LICENSE)

[license]: LICENSE
```

## Badge Reference

For documentation repositories:

| Badge | Markdown |
|-------|----------|
| License | `[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]` |

**Optional badges**:
- Last update: `https://img.shields.io/github/last-commit/{user}/{repo}`

## Section Guidelines

- **What's Inside**: High-level overview of main sections
- **File Index**: Quick reference for key files
- **Structure**: Directory layout visualization
- **Organization Principles**: How docs are organized
- **Status Tracking**: If applicable, explain status system
- **Navigation**: How to move through the documentation