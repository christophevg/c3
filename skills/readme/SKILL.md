---
name: readme
description: Create and maintain README.md files for agentic projects. Use when creating, updating, or reviewing READMEs. Examples: "create a README", "update the README", "review README structure", "add badges to README".
---

# readme

Create and maintain README.md files with appropriate structure, badges, and content for different project types.

## Overview

| Capability | Description |
|------------|-------------|
| Project type detection | Identify Python (PyPI/non-PyPI), config/tools, web app, Jekyll, docs |
| Template generation | Generate appropriate README structure for project type |
| Badge selection | Auto-select relevant badges based on project type |
| Section validation | Check existing READMEs against best practices |
| Maintenance workflow | Keep READMEs synchronized with project evolution |

## When to Use This Skill

Use this skill when:
- User says "create a README" or "add a README"
- User says "update the README" or "improve the README"
- User says "review the README structure"
- New project initialization
- After significant project changes
- Before releases/publishing

## Project Type Detection

Detect project type by analyzing repository contents:

| File/Dir Present | Project Type |
|-----------------|--------------|
| `pyproject.toml` with `[project]` name | Python package (check for PyPI) |
| `setup.py`, `setup.cfg` | Python package (legacy) |
| `_config.yml`, `_posts/`, `_layouts/` | Jekyll static site |
| `app.py`, `main.py` + `templates/` | Web app (Flask/FastAPI) |
| `Makefile` with symlink install | Config/tools repository |
| `INDEX.md`, `PLAN.md`, no code | Documentation repository |

### PyPI Detection

Check if Python package is published to PyPI:

1. **Check pyproject.toml** for PyPI metadata
2. **Check for badges** referencing PyPI
3. **Verify package exists** on pypi.org
4. **If yes** → PyPI template with badges
5. **If no** → Local Python template

## Workflow

### Phase 1: Analyze Project

| Step | Action |
|------|--------|
| 1 | Detect project type |
| 2 | Check for existing README.md |
| 3 | If exists, analyze current structure |
| 4 | Identify missing sections |
| 5 | Identify outdated badges/info |

### Phase 2: Generate/Update README

| Action | Description |
|--------|-------------|
| Create new | Use appropriate template |
| Update existing | Fill gaps, fix outdated content |
| Add badges | Select based on project type |

### Phase 3: Validate

| Check | Validation |
|-------|------------|
| Essential sections | Present and populated |
| Badge count | 5-10 maximum |
| Quick Start | Works in 3 commands max |
| Links | All valid |
| Line count | Under 500 lines |

## Section Requirements by Type

### All Projects (Required)

| Section | Purpose |
|---------|---------|
| Title + Description | What is this? (first 50 words critical) |
| Badges | Quick status overview |
| Quick Start | 30-second setup |
| License | Legal clarity |

### Python Packages (Additional)

| Section | Required For |
|---------|--------------|
| Installation | All Python packages |
| Usage | All Python packages |
| API Reference | Complex libraries |
| Development | Contributing developers |
| Changelog | PyPI packages |

### Web Apps (Additional)

| Section | Purpose |
|---------|---------|
| Tech Stack | Frameworks and versions |
| Deployment | How to deploy |
| Screenshots | Visual preview |
| Environment Variables | Configuration options |

### Config/Tools (Additional)

| Section | Purpose |
|---------|---------|
| Requirements | Prerequisites |
| Configuration | Customization options |
| Files Explained | What each file does |

## Badge Selection Logic

| Project Type | Recommended Badges |
|--------------|-------------------|
| Python (PyPI) | PyPI version, Python versions, Coverage, CI, License |
| Python (local) | CI, License |
| Web App | Deploy status, CI, License |
| Config/Tools | License, Platform support |
| Documentation | Last update, License |

**Badge sources:**
- PyPI: `https://img.shields.io/pypi/v/{package}`
- Python versions: `https://img.shields.io/pypi/pyversions/{package}`
- Coverage: `https://img.shields.io/coveralls/github/{user}/{repo}`
- CI: `https://img.shields.io/github/actions/workflow/status/{user}/{repo}/{workflow}`
- License: `https://img.shields.io/github/license/{user}/{repo}`

## Template Files

- `templates/python-pypi.md` — PyPI package template
- `templates/python-local.md` — Non-PyPI Python template
- `templates/config-tools.md` — Config/skills repo template
- `templates/web-app.md` — Web application template
- `templates/jekyll-site.md` — Jekyll static site template
- `templates/documentation.md` — Documentation repo template

## Pattern Files

- `patterns/section-content.md` — What each section should contain
- `patterns/badge-selection.md` — Detailed badge logic
- `patterns/maintenance-workflow.md` — Keeping READMEs in sync

## Common Issues

| Issue | Solution |
|-------|----------|
| README too long | Move details to docs/, add links |
| Outdated badges | Regenerate from current project info |
| Missing Quick Start | Create 3-step minimal setup |
| No badges | Add based on project type |
| Dead links | Validate all URLs |

## Related Skills

- commit — For committing README changes
- develop-skill — For updating this skill itself