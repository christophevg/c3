# Badge Selection Guide

This pattern defines how to select appropriate badges for different project types.

## Badge Sources

### Primary Source: Shields.io

Shields.io is the most popular badge service (1.6 billion images/month).

**URL format**: `https://img.shields.io/{type}/{params}`

## Badge Categories

### Distribution Badges

**PyPI**:
```markdown
[![PyPI](https://img.shields.io/pypi/v/package-name.svg)][pypi]
```
- Shows current version
- Links to PyPI page

**Python versions**:
```markdown
[![Python](https://img.shields.io/pypi/pyversions/package-name.svg)][pypi]
```
- Shows supported Python versions
- Links to PyPI page

**Downloads**:
```markdown
[![Downloads](https://img.shields.io/pypi/dm/package-name.svg)][pypi]
```
- Shows monthly downloads
- Links to PyPI page

---

### Build/Quality Badges

**CI Status**:
```markdown
[![CI](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml.svg)][ci]
```
- Shows build status
- Links to workflow

**Coverage**:
```markdown
[![Coverage](https://img.shields.io/coveralls/github/user/repo.svg)][coveralls]
```
- Shows test coverage percentage
- Links to Coveralls

**Code Quality**:
```markdown
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black.svg)][ruff]
```
- Shows linting tool
- Custom badge

---

### License Badges

**GitHub License**:
```markdown
[![License](https://img.shields.io/github/license/user/repo.svg)][license]
```
- Detects license from LICENSE file
- Links to LICENSE

**Custom License**:
```markdown
[![License](https://img.shields.io/badge/License-MIT-blue.svg)][license]
```
- Manual license type
- Blue color for MIT

---

### Documentation Badges

**ReadTheDocs**:
```markdown
[![Docs](https://img.shields.io/readthedocs/package-name.svg)][docs]
```
- Shows docs build status
- Links to docs

**GitHub Pages**:
```markdown
[![Pages](https://img.shields.io/github/deployments/user/repo/github-pages.svg)][pages]
```
- Shows deployment status
- Links to site

---

### Platform Badges

**Platform Support**:
```markdown
[![Platform](https://img.shields.io/badge/platform-mac%20%7C%20linux%20%7C%20windows-lightgrey.svg)][platform]
```
- Manual badge
- Shows supported platforms

---

## Badge Selection by Project Type

### Python (PyPI)

**Required**:
1. PyPI version
2. Python versions
3. License

**Recommended**:
4. CI status
5. Coverage

**Optional**:
6. Downloads
7. Documentation
8. Code style

**Example row**:
```markdown
[![PyPI](https://img.shields.io/pypi/v/package.svg)][pypi]
[![Python](https://img.shields.io/pypi/pyversions/package.svg)][pypi]
[![CI](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml.svg)][ci]
[![Coverage](https://img.shields.io/coveralls/github/user/repo.svg)][coveralls]
[![License](https://img.shields.io/github/license/user/repo.svg)][license]
```

---

### Python (Non-PyPI)

**Required**:
1. License

**Optional**:
2. CI status

**Example**:
```markdown
[![CI](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml.svg)][ci]
[![License](https://img.shields.io/github/license/user/repo.svg)][license]
```

---

### Web Applications

**Required**:
1. License

**Recommended**:
2. Deploy status
3. CI status

**Example**:
```markdown
[![Deploy](https://img.shields.io/github/deployments/user/repo/production.svg)][deploy]
[![CI](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml.svg)][ci]
[![License](https://img.shields.io/github/license/user/repo.svg)][license]
```

---

### Config/Tools Repositories

**Required**:
1. License

**Optional**:
2. Platform support
3. CI status

**Example**:
```markdown
[![Platform](https://img.shields.io/badge/platform-mac%20%7C%20linux-lightgrey.svg)][platform]
[![License](https://img.shields.io/github/license/user/repo.svg)][license]
```

---

### Documentation Repositories

**Required**:
1. License

**Optional**:
2. Last update
3. GitHub Pages status

**Example**:
```markdown
[![Last Update](https://img.shields.io/github/last-commit/user/repo.svg)][commits]
[![License](https://img.shields.io/github/license/user/repo.svg)][license]
```

---

### Jekyll Static Sites

**Required**:
1. License

**Optional**:
2. GitHub Pages status

**Example**:
```markdown
[![GitHub Pages](https://img.shields.io/github/deployments/user/repo/github-pages.svg)][pages]
[![License](https://img.shields.io/github/license/user/repo.svg)][license]
```

---

## Badge Best Practices

### 1. Count

**Maximum 10 badges**. More creates clutter and reduces impact.

**Priority order**:
1. Distribution (PyPI, npm)
2. Build/Quality (CI, Coverage)
3. License
4. Documentation
5. Compatibility

---

### 2. Placement

**Position**: Top of README, after title and description.

**Before**:
```markdown
# Project Name

> Description

## About
```

**After**:
```markdown
# Project Name

[![Badge1][link1]][Badge1]
[![Badge2][link2]][Badge2]

> Description

## About
```

---

### 3. Clickability

**Always make badges clickable**. Use reference-style links:

```markdown
[![PyPI](https://img.shields.io/pypi/v/package.svg)][pypi]

[pypi]: https://pypi.org/project/package/
```

This allows:
- Badge to be clicked
- Clean badge line
- Easy to update links

---

### 4. Grouping

**Group related badges together**:

```markdown
<!-- Distribution -->
[![PyPI][badge-pypi]][pypi]
[![Python][badge-python]][pypi]

<!-- Quality -->
[![CI][badge-ci]][ci]
[![Coverage][badge-coverage]][coveralls]

<!-- Legal -->
[![License][badge-license]][license]
```

---

### 5. Color Awareness

**Shield.io colors**:
- `brightgreen` = passing/success
- `green` = good
- `yellowgreen` = warning
- `yellow` = in progress
- `orange` = attention
- `red` = critical/failure
- `blue` = informational
- `lightgrey` = neutral

**Override color** (for custom badges):
```markdown
[![Custom](https://img.shields.io/badge/label-message-color.svg)][link]
```

---

## Badge Generators

### Shields.io

**URL**: https://shields.io

**Features**:
- 100+ badge types
- Custom badges
- Dynamic badges

**Custom badge**:
```
https://img.shields.io/badge/{label}-{message}-{color}.svg
```

Example:
```markdown
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)][python]
```

---

### Badgen

**URL**: https://badgen.net

**Alternative** to Shields.io with different style.

---

## Badge Validation Checklist

Before adding badges, verify:

- [ ] Badge URL is correct
- [ ] Badge renders correctly
- [ ] Link destination is valid
- [ ] Badge count under 10
- [ ] Badges are grouped logically
- [ ] All badges are clickable