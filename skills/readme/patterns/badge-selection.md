# Badge Selection Guide

This pattern defines how to select appropriate badges for different project types.

## Badge Sources

### Primary Source: Shields.io

Shields.io is the most popular badge service (1.6 billion images/month).

**URL format**: `https://img.shields.io/{type}/{params}`

---

## Badge Types

### Distribution Badges

| Badge | URL | Purpose |
|-------|-----|---------|
| PyPI version | `https://img.shields.io/pypi/v/{package}.svg` | Current version |
| Python versions | `https://img.shields.io/pypi/pyversions/{package}.svg` | Supported Python |
| Python version (static) | `https://img.shields.io/badge/Python-{version}-blue.svg` | Python version (non-PyPI) |

### Package Manager Badge

| Badge | URL | Purpose |
|-------|-----|---------|
| uv | `https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json` | uv package manager |

**Usage**: All Python projects using uv should include this badge.

### Build/Quality Badges

| Badge | URL | Purpose |
|-------|-----|---------|
| CI status | `https://img.shields.io/github/actions/workflow/status/{user}/{repo}/{workflow}.svg` | Build status |
| Coverage | `https://img.shields.io/coveralls/github/{user}/{repo}.svg` | Test coverage % |

**Important:** The CI badge workflow filename must match the actual file in `.github/workflows/`. Common filenames:
- `ci.yml` or `ci.yaml` - for CI workflows
- `test.yml` or `test.yaml` - for test workflows

Check the workflow file with: `ls .github/workflows/`

### License Badge

| Badge | URL | Purpose |
|-------|-----|---------|
| License | `https://img.shields.io/github/license/{user}/{repo}.svg` | Usage rights |

### Documentation Badges

| Badge | URL | Purpose |
|-------|-----|---------|
| ReadTheDocs | `https://img.shields.io/readthedocs/{package}.svg` | Docs status |
| GitHub Pages | `https://img.shields.io/github/deployments/{user}/{repo}/github-pages.svg` | Pages status |

### Platform Badge

| Badge | URL | Purpose |
|-------|-----|---------|
| Platform | `https://img.shields.io/badge/platform-mac%20%7C%20linux-lightgrey.svg` | Compatibility |

### Workflow Badge

| Badge | URL | Purpose |
|-------|-----|---------|
| Agentic | `https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square` | Agentic methodology |

**Usage**: Include this badge for projects built using agentic workflow (AI agents implementing architecture).

### Documentation Standard Badge

| Badge | URL | Purpose |
|-------|-----|---------|
| PACKAGE.md | `https://img.shields.io/badge/pkgq-PACKAGE.md-blueviolet` | AI-optimized documentation |

**Usage**: Include this badge for projects with a PACKAGE.md file in the repository root. This indicates the package provides AI-optimized documentation for agent consumption.

**Format**: `[![PACKAGE.md](https://img.shields.io/badge/pkgq-PACKAGE.md-blueviolet)](https://github.com/christophevg/pkgq#readme)`

---

## Badge Sets by Project Type

### Python (PyPI Package)

**Requirement**: All PyPI packages MUST have a PACKAGE.md file in the repository root. This provides AI-optimized documentation for agent consumption.

```markdown
[![PyPI](https://img.shields.io/pypi/v/{package}.svg)][pypi]
[![Python](https://img.shields.io/pypi/pyversions/{package}.svg)][pypi]
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]
[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]
[![Coverage](https://img.shields.io/coveralls/github/{user}/{repo}.svg)][coveralls]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]
[![PACKAGE.md](https://img.shields.io/badge/pkgq-PACKAGE.md-blueviolet)](https://github.com/christophevg/pkgq#readme)
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)
```

**8 badges**: PyPI, Python, uv, CI, Coverage, License, PACKAGE.md, Agentic

---

### Python (Non-PyPI / Local)

```markdown
[![Python](https://img.shields.io/badge/Python-{version}-blue.svg)][python]
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]
[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)
```

**5 badges**: Python, uv, CI, License, Agentic

**Note**: Replace `{version}` with the Python version from `.python-version` or `pyproject.toml`.

---

### Web Application

```markdown
[![CI](https://img.shields.io/github/actions/workflow/status/{user}/{repo}/ci.yml.svg)][ci]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)
```

**3 badges**: CI, License, Agentic

---

### Config/Tools Repository

```markdown
[![Platform](https://img.shields.io/badge/platform-mac%20%7C%20linux-lightgrey.svg)][platform]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)
```

**3 badges**: Platform, License, Agentic

---

### Documentation Repository

```markdown
[![Last Update](https://img.shields.io/github/last-commit/{user}/{repo}.svg)][commits]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)
```

**3 badges**: Last Update, License, Agentic

---

### Jekyll Static Site

```markdown
[![GitHub Pages](https://img.shields.io/github/deployments/{user}/{repo}/github-pages.svg)][pages]
[![License](https://img.shields.io/github/license/{user}/{repo}.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)
```

**3 badges**: GitHub Pages, License, Agentic

---

## Badge Count Summary

| Project Type | Badge Count |
|--------------|-------------|
| Python (PyPI) | 8 |
| Python (Non-PyPI) | 5 |
| Web Application | 3 |
| Config/Tools | 3 |
| Documentation | 3 |
| Jekyll Static Site | 3 |

---

## Best Practices

### Placement

Position badges at the top of README, after title and description:

```markdown
# Project Name

[![Badge1][link1]][Badge1]
[![Badge2][link2]][Badge2]

> Description

## About
```

### Clickability

Always use reference-style links:

```markdown
[![PyPI](https://img.shields.io/pypi/v/package.svg)][pypi]

[pypi]: https://pypi.org/project/package/
```

### Link References

Add link references at the bottom of README:

```markdown
[pypi]: https://pypi.org/project/{package}/
[uv]: https://docs.astral.sh/uv/
[python]: https://python.org/
[ci]: https://github.com/{user}/{repo}/actions
[coveralls]: https://coveralls.io/github/{user}/{repo}
[license]: https://github.com/{user}/{repo}/blob/main/LICENSE
```

---

## Validation Checklist

- [ ] Badge URLs are correct
- [ ] Badges render correctly
- [ ] Link destinations are valid
- [ ] Badges are clickable
- [ ] Badge count matches project type
- [ ] Agentic badge present for agentic projects
- [ ] License badge only if LICENSE file exists (check for `LICENSE`, `LICENSE.txt`, or `LICENSE.md`)
- [ ] CI badge only if workflow file exists — check `.github/workflows/` for actual filename
- [ ] CI badge workflow filename matches actual file (e.g., `ci.yml`, `test.yml`, `test.yaml`)
- [ ] PACKAGE.md badge present if PACKAGE.md file exists in repository root
- [ ] PyPI packages have PACKAGE.md file (mandatory for all PyPI projects)

