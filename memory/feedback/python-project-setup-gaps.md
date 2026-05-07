# Python Project Setup Gaps

**Date**: 2025-05-07
**Session**: simple-email-gw initial release
**Context**: User had to provide extensive feedback for a new Python package project that should have been handled by existing agents and skills.

## Problem

When extracting and publishing `simple-email-gw` as a new PyPI package, the user had to provide 15+ additional instructions for things that should have been standard practice for Python projects.

## Missing Elements

### Project Structure

| Item | User Had to Request | Should Be Default |
|------|---------------------|-------------------|
| Makefile with utility targets | ✓ | Auto-created with standard targets |
| docs/ directory | ✓ | Auto-created with Sphinx setup |
| LICENSE file | ✓ | Auto-created (MIT by default) |
| .readthedocs.yaml | ✓ | Auto-created for ReadTheDocs |

### Makefile Gaps

The existing `templates/makefile` was missing:

| Target | Purpose | Status |
|--------|---------|--------|
| `publish-test` | Publish to TestPyPI first | Missing |
| `docs` | Build documentation | Wrong syntax |
| `test-all` | Run tox | Missing |
| `run-env` / `dev-env` | Proper prerequisites | Missing pattern |
| `all` | Run all checks | Missing |

### Entry Point Issues

| Issue | User Feedback | Root Cause |
|-------|---------------|------------|
| Script name `mcp` → `mcp-server` | Avoid name clashes | Skill doesn't warn about common names |
| `__main__.py` | Should be removed | Not an intended entry point for MCP |
| `main()` → `run()` | Better naming | Entry point should be explicit |

### README Gaps

| Missing | Should Include |
|---------|----------------|
| Badges | PyPI version, Python versions, License, CI, Code style, Type checked, ReadTheDocs |
| Async-only note | Explicit statement if package is async-only |
| Makefile commands | Updated target names |

### Documentation Gaps

| Issue | Impact |
|-------|--------|
| No Sphinx structure created | User had to create index.rst, conf.py |
| Duplicate content | API.md and quickstart.md had overlapping content |
| Not ReadTheDocs ready | Missing .readthedocs.yaml |

### Publishing Workflow Gaps

| Gap | Solution |
|-----|----------|
| No TestPyPI workflow | Add `publish-test` target using twine |
| uv publish doesn't work with keychain | Use twine instead (already in docs but not automated) |

## Root Causes

### 1. python-project Skill

The skill exists but:
- Templates are reference docs, not automatically applied
- No "new project setup" workflow
- Assumes user invokes skill explicitly

### 2. project-manager Agent

The agent has no awareness of:
- Python project setup requirements
- Standard project scaffolding
- Publishing workflow (TestPyPI → PyPI)

### 3. python-developer Agent

The agent focuses on implementation but:
- Doesn't ensure project structure is complete
- Doesn't verify documentation infrastructure
- Doesn't set up CI/CD automatically

### 4. Missing Integration

No agent or skill handles:
- End-to-end new package creation
- Checklist verification before publishing
- Documentation completeness check

## Recommendations

### 1. Create python-package-setup Skill

A new skill for new Python package projects that:

1. Creates standard project structure:
   - `pyproject.toml` from template
   - `Makefile` from enhanced template
   - `docs/` with Sphinx structure
   - `LICENSE` (MIT default)
   - `.readthedocs.yaml`
   - `.github/workflows/test.yml`
   - `.gitignore`

2. Prompts for:
   - Package name (warns if generic like "mcp")
   - Description
   - Author info
   - Entry point name (script name)
   - Python version support

3. Validates:
   - Entry point name doesn't clash with common tools
   - All standard files present
   - README has required sections
   - Documentation structure complete

### 2. Enhance python-project Skill

Add explicit setup workflow:

```markdown
## New Package Setup

When creating a new Python package project:

1. Create directory structure
2. Copy templates
3. Customize for project
4. Verify completeness
5. Initialize git
```

### 3. Enhance Makefile Template

Add missing targets:

```makefile
## run-env: Install production dependencies
run-env:
  uv sync

## dev-env: Install with all dependencies
dev-env:
  uv sync --all-extras

## test-all: Run tests with tox (all Python versions)
test-all: dev-env
  uv run tox

## docs: Build documentation
docs: dev-env
  cd docs && uv run sphinx-build -b html . _build/html

## publish: Publish to PyPI (requires credentials)
publish: build
  uv run twine upload dist/*

## publish-test: Publish to TestPyPI (requires credentials)
publish-test: build
  uv run twine upload --repository testpypi dist/*

## all: Run lint, test, and typecheck
all: dev-env
  uv run ruff check src/ tests/
  uv run pytest
  uv run mypy src/
```

### 4. Enhance project-manager Agent

Add Python project awareness to Phase 0:

```markdown
### Phase 0.5: Python Project Detection

If project is a Python package (has pyproject.toml):

1. Check for standard files:
   - [ ] LICENSE
   - [ ] Makefile with standard targets
   - [ ] docs/ with Sphinx structure
   - [ ] .readthedocs.yaml
   - [ ] .github/workflows/test.yml

2. If missing, invoke c3:functional-analyst:
   - "Create missing project infrastructure"
   - Use python-project skill templates

3. Verify README quality:
   - Badges present
   - Installation instructions
   - Quick start
   - Link to documentation
```

### 5. Create Pre-Publish Checklist Skill

A `/pre-publish` skill that verifies:

- [ ] All tests pass (`make all`)
- [ ] Documentation builds (`make docs`)
- [ ] README has badges and links
- [ ] LICENSE file exists
- [ ] CHANGELOG or version updated
- [ ] GitHub Actions workflow exists
- [ ] Tested on TestPyPI first (`make publish-test`)
- [ ] Git tag created

## Immediate Actions

1. Update `python-project/templates/makefile` with missing targets
2. Add entry point naming guidance to `python-project/SKILL.md`
3. Create documentation structure template in `python-project/templates/`
4. Add pre-publish checklist to `python-project/SKILL.md`
5. Update `project-manager` to check Python project infrastructure in Phase 0

## Related Files

- `/Users/xtof/Workspace/agentic/c3/skills/python-project/SKILL.md`
- `/Users/xtof/Workspace/agentic/c3/skills/python-project/templates/makefile`
- `/Users/xtof/Workspace/agentic/c3/agents/project-manager.md`
- `/Users/xtof/Workspace/agentic/c3/agents/python-developer.md`