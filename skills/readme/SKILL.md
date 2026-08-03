---
name: readme
description: |
  Create and maintain README.md files for agentic projects. Use when creating, updating, or reviewing READMEs. Examples: "create a README", "update the README", "review README structure", "add badges to README".
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

## Philosophy: End-User First

**The README is the front-door.** Full end-user documentation lives in a
`docs/` folder published to ReadTheDocs (Sphinx + MyST + `sphinx_rtd_theme`).
This skill covers the README; the docs/ standard is covered by the
[`c3:documentation`](../documentation/SKILL.md) skill. The two are
complementary: the README is concise and front-door-critical (works on
GitHub AND on PyPI, where repo-relative file links do NOT work), and
`docs/` is the all-inclusive narrative the README links into via absolute
ReadTheDocs URLs.

**READMEs must be END-USER ORIENTED, not developer oriented.**

### End-User README (✓)

- **What is this?** — Clear description in first 50 words
- **Quick Start** — 3 commands or less to run
- **How to Use** — User-facing functionality
- **How to Test** — How to verify it works
- **User Acceptance Testing** — Steps for users to verify

**Example structure:**
```markdown
# Project Name

Brief description (50 words max)

## Quick Start

```bash
uv sync
make run
```

## How to Use

1. Step 1
2. Step 2
3. Step 3

## Testing

```bash
make test
```
```

### Developer README (✗)

- Architecture details
- Implementation notes
- Developer setup
- Code structure
- Internal design

**These belong in:**
- `docs/architecture.md`
- `docs/developer-guide.md`
- `CLAUDE.md` (for AI agents)
- `analysis/` (for design docs)

**NOT in README.**

## When to Use This Skill

Use this skill when:
- User says "create a README" or "add a README"
- User says "update the README" or "improve the README"
- User says "review the README structure"
- New project initialization
- After significant project changes
- Before releases/publishing

**When NOT to use this skill:** For full tutorials, user guides, or
all-inclusive documentation, use [`c3:documentation`](../documentation/SKILL.md)
(docs/ + Sphinx + ReadTheDocs) — this skill covers the README front-door only.
The README is lean (under 500 lines); the tutorial and full narrative live in
`docs/`.

## File Location

**README.md belongs in the project root.**

| Location | Use Case |
|----------|----------|
| `README.md` (root) | **Project README** — standard, required |
| `.github/README.md` | GitHub profile/org README (not for projects) |

**Why root:**

1. **PyPI expects it** — `readme = "README.md"` in pyproject.toml
2. **Convention** — GitHub, GitLab, Bitbucket all look there first
3. **Tooling** — Most tools assume root location
4. **Visibility** — Appears in file listings, clones, GitHub repo landing page

**What goes in `.github/` instead:**

| File | Purpose |
|------|---------|
| `FUNDING.yml` | Sponsorship configuration |
| `ISSUE_TEMPLATE/` | Issue templates |
| `PULL_REQUEST_TEMPLATE.md` | PR template |
| `workflows/` | GitHub Actions |
| `CODEOWNERS` | Code ownership rules |

**Note:** `.github/README.md` is for user/org profile repos (e.g., `github.com/username/.github`), not for project repositories.

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
| 3 | **Check for `.github/README.md`** — if exists, move to root |
| 4 | If exists, analyze current structure |
| 5 | Identify missing sections |
| 6 | Identify outdated badges/info |

**Critical:** If `.github/README.md` exists but `README.md` does not, move it to root:
```bash
mv .github/README.md README.md
```

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
| End-user focus | User can follow without questions |

## README Validation Checklist

**Before marking complete, verify:**

- [ ] **Title + Description** in first 50 words
- [ ] **What is this?** — Clear explanation for non-developers
- [ ] **Quick Start** — 3 commands or less:
  - [ ] Installation: `uv sync` (NOT multiple install commands)
  - [ ] Run: `make run` or single `uv run` command
  - [ ] Test: `make test` or `uv run pytest`
- [ ] **How to Use** — User-facing features, not internal architecture
- [ ] **How to Test** — Clear testing instructions
- [ ] **User Acceptance Testing** — Steps for users to verify (if applicable)
- [ ] **Badges** — Appropriate for project type (5-10 max)
- [ ] **PACKAGE.md** — PyPI packages must have PACKAGE.md file with badge
- [ ] **Total length** — Under 500 lines
- [ ] **End-user can complete** — Setup without asking questions

**End-user validation:**

Ask yourself: "Can a user follow this README from start to finish without asking me questions?"

If NO → README is incomplete. Add missing steps or clarifications.

**Common end-user questions (and how to fix):**

| Question | Fix |
|-----------|-----|
| "What do I install?" | Single `uv sync` command |
| "How do I run it?" | Single `make run` or `uv run` command |
| "Which command first?" | Number steps: 1, 2, 3 |
| "What's the output?" | Show expected output in examples |
| "How do I know it works?" | Add "Expected result" after commands |

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

See `patterns/badge-selection.md` for detailed badge configuration.

**Summary by Project Type:**

| Project Type | Badges | Count |
|--------------|--------|-------|
| Python (PyPI) | PyPI, Python, uv, CI, Coverage, License, PACKAGE.md, Agentic | 8 |
| Python (Non-PyPI) | Python, uv, CI (if exists), License, Agentic | 4-5 |
| Web App | CI, License, Agentic | 3 |
| Config/Tools | Platform, License, Agentic | 3 |
| Documentation | Last Update, License, Agentic | 3 |
| Jekyll Site | GitHub Pages, License, Agentic | 3 |

**Badge Placement:**

```markdown
# Project Name

[![Badge1][badge1]][link1]
[![Badge2][badge2]][link2]
[![Badge3][badge3]][link3]

> Short description

[body]

[badge1]: https://...
[link1]: https://...
```

- **One badge per line** for readability
- **Description immediately after** badges (blank line, then `> description`)
- **Link references** at the bottom of the file

**Key Rules:**

1. **Agentic badge is required** for all projects built using agentic workflow
2. **uv badge is required** for all Python projects (standard package manager)
3. **PACKAGE.md is mandatory for all PyPI packages** — provides AI-optimized documentation
4. **PACKAGE.md badge required if PACKAGE.md exists** — indicates AI-optimized docs available
5. **License badge only if LICENSE file exists** — check for `LICENSE`, `LICENSE.txt`, or `LICENSE.md`
6. **CI badge only if workflow exists** — check `.github/workflows/` for actual filename
7. **CI badge filename must match** — use `ci.yml`, `test.yml`, `test.yaml`, etc. as appropriate
8. **Downloads badge is removed** (rate limiting causes broken badges)
9. **Deploy badge is removed** (not using GH Actions for deployment)

**Badge sources:**
- PyPI: `https://img.shields.io/pypi/v/{package}.svg`
- Python versions: `https://img.shields.io/pypi/pyversions/{package}.svg`
- Python (static): `https://img.shields.io/badge/Python-{version}-blue.svg`
- uv: `https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json`
- Coverage: `https://img.shields.io/coveralls/github/{user}/{repo}.svg`
- CI: `https://img.shields.io/github/actions/workflow/status/{user}/{repo}/{workflow}.svg` (replace `{workflow}` with actual filename from `.github/workflows/`)
- License: `https://img.shields.io/github/license/{user}/{repo}.svg`
- PACKAGE.md: `https://img.shields.io/badge/pkgq-PACKAGE.md-blueviolet` (links to `https://github.com/christophevg/pkgq#readme`)
- Agentic: `https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square` (links to `https://christophe.vg/about/Agentic-Workflow`)

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
| README in `.github/` | Move to root: `mv .github/README.md README.md` |

## Related Skills

- [`c3:documentation`](../documentation/SKILL.md) — the docs/ + Sphinx + ReadTheDocs standard. README is the front-door; `docs/` is the full narrative.
- commit — For committing README changes
- develop-skill — For updating this skill itself
