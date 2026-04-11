---
name: documentation
description: Use this skill when setting up or updating project documentation for Sphinx/readthedocs.org. Handles API reference, guides, and changelog updates.
---

# Documentation

This skill helps set up and maintain project documentation using Sphinx for publication on readthedocs.org.

## When to Use This Skill

- Setting up Sphinx documentation for a new project
- Updating API reference after adding new features
- Creating user guides and installation instructions
- Updating changelog after releases
- Fixing documentation build issues

## Documentation Structure

```
docs/
  _static/          # Static files (images, etc.)
  _templates/       # Custom templates (optional)
  api/              # API reference pages
    app.md
    exceptions.md
    plugins.md
    ...
  development/      # Development guides
    contributing.md
    changelog.md
  conf.py          # Sphinx configuration
  index.md          # Documentation home
  installation.md   # Installation guide
  quickstart.md     # Quick start guide
  requirements.txt  # Sphinx dependencies
  Makefile          # Build commands
```

## Workflow

### 1. Check Documentation Setup

Verify documentation structure exists:
- `docs/conf.py` - Sphinx configuration
- `docs/index.md` - Documentation home
- `docs/Makefile` - Build commands
- `docs/requirements.txt` - Dependencies

If missing, create standard Sphinx setup.

### 2. Update API Reference

When adding new public APIs:

1. Create or update `docs/api/{module}.md`
2. Use autodoc directives for automatic documentation
3. Include usage examples
4. Add to `docs/index.md` toctree

### 3. Update Changelog

When completing features:

1. Add entry to `docs/development/changelog.md`
2. Include: date, type (Added/Changed/Fixed/Removed), description
3. Reference issues/PRs if applicable

### 4. Update Guides

When adding new features:

1. Update `docs/quickstart.md` if API changes
2. Add examples to `docs/api/{module}.md`
3. Update `CLAUDE.md` if workflow changes

### 5. Build and Verify

Run `make docs` and verify:
- No warnings or errors
- All links resolve
- API reference is complete

## Sphinx Configuration

Standard `conf.py` for Python projects:

```python
# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath("../src"))

project = "project-name"
copyright = "YEAR, Author"
author = "Author"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

html_theme = "sphinx_rtd_theme"

# Autodoc settings
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# Intersphinx mappings
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
```

## Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
## [version] - YYYY-MM-DD

### Added
- New feature X

### Changed
- Modified feature Y

### Fixed
- Bug fix for Z

### Removed
- Deprecated feature W
```

## Common Issues

### Missing `docs/Makefile`

Create with standard Sphinx Makefile:
```makefile
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

### pyenv Virtualenv Detection

If `make docs` fails with "No virtual environment detected", update Makefile:

```makefile
# Check for venv or pyenv
define check_venv
	@if [ -z "$(VIRTUAL_ENV)" ] && [ "$(shell pyenv version-name 2>/dev/null)" != "$(VENV_NAME)" ]; then \
		echo "Error: No virtual environment detected."; \
		exit 1; \
	fi
endef
```

## Pre-commit Checklist

Before committing documentation:

1. Run `make docs` - no errors
2. Check all new APIs documented
3. Update changelog
4. Update screenshot if showcase changed
5. Ask user to verify screenshot