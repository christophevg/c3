---
name: pyenv
description: Manage Python versions and virtual environments with PyEnv
---

# PyEnv Skill

Manage Python versions and virtual environments with PyEnv. Provides intelligent environment setup with best practice guidance.

## Purpose

Simplify Python environment management by:
- Detecting project Python requirements
- Guiding version and naming decisions
- Creating environments with best practices
- Offering auto-activation setup

## When to Use

Use this skill when:
- Starting a new Python project
- Setting up a project after cloning
- Managing Python versions across projects
- Creating virtual environments
- Troubleshooting environment issues
- Setting up tool-specific virtualenvs for skills/agents

User mentions: "pyenv", "virtual environment", "venv", "python version", "activate environment"

## Project Types

### Standard Python Projects

Normal Python projects with a `.python-version` file. The skill detects and manages the virtualenv.

### Python Package Projects

Detected by presence of `.pypi-template` file. These projects:
- Use a globally shared `pypi-template` virtualenv (managed by pyenv-virtualenv)
- May have additional virtualenvs for testing against different Python versions
- The skill should recognize this and not create project-specific venvs

### Tool Virtualenvs

Skills and agents that use their own tools (requiring additional packages) should have dedicated virtualenvs:
- Virtualenv name: `{skill-name}-tool` or `{agent-name}-tool`
- Activated only during tool execution
- Creates isolated run-environment for each tool

## Current User Setup

- **Auto-activation**: Already implemented via `pyenv-virtualenv-init` in shell config
- **`.python-version` files**: Present in most projects
- The skill should detect existing auto-activation and not re-offer setup

## Activation

Invoke with: `/pyenv`

## Behavior

### Step 1: Detect Current State

Check for:
1. `.python-version` file (version pin)
2. `.pypi-template` file (Python package project)
3. Existing virtual environment
4. pyenv-virtualenv-init in shell config (already configured?)

### Step 2: Determine Project Type

**Python Package Project** (has `.pypi-template`):
```
Detected Python package project (pypi-template found).

Package projects use:
  - Shared pypi-template virtualenv (for packaging tools)
  - Additional virtualenvs for multi-version testing

Configure:
  1. Use existing pypi-template virtualenv
  2. Create test virtualenvs for: {versions}
  3. Both

Choice: [1-3]
```

**Standard Python Project** (no `.pypi-template`):
Proceed with normal environment setup.

**Tool Virtualenv Request** (skill/agent context):
```
Setting up tool virtualenv for: {skill-name}

This creates an isolated environment for the skill's tools.
Name: {skill-name}-tool
Packages: {required-packages}

Create? [Y/n]
```

### Step 3: Present Options

If no environment detected, guide user through:

**Version Selection:**
```
Python version for this project:

Installed versions:
  1. {latest_stable} (latest stable)
  2. {lts_version} (LTS - recommended for most projects)
  3. {compat_version} (maximum compatibility)
  4. {other_installed}...
  5. Other version...

Choice: [1-5]
```

**Naming Convention:**
```
Virtual environment naming:

  1. .venv (standard, project-local) - recommended
  2. {project-name} (pyenv-virtualenv style)

Choice: [1-2]
```

### Step 4: Create Environment

Execute:
```bash
# For .venv style
pyenv install -s {version}
python -m venv .venv
echo "{version}" > .python-version

# For pyenv-virtualenv style
pyenv install -s {version}
pyenv virtualenv {version} {project-name}
pyenv local {project-name}

# For tool virtualenv
pyenv virtualenv {version} {tool-name}-tool
pyenv activate {tool-name}-tool
pip install {packages}
```

### Step 5: Auto-Activation Check

Check if pyenv-virtualenv-init already configured:

```bash
grep -q "pyenv virtualenv-init" ~/.zshrc
```

**If already configured:**
```
✓ Auto-activation already configured
  Environment will activate automatically when entering directory
```

**If not configured:**
```
Enable automatic activation?

This adds the following to your shell config:
  eval "$(pyenv virtualenv-init -)"

Benefits:
  - Auto-activate when entering project directory
  - Never forget to activate again

[Y/n]:
```

### Step 6: Store Preferences

Save preferences to project memory or user memory:
- Python version choice
- Naming preference
- Project type (standard/package)
- Tool virtualenvs created

## User Preferences

### Preference Detection Order

1. Project MEMORY.md (`pyenv-preferences`)
2. User global memory (`pyenv-defaults`)
3. Interactive prompt

### Preference Storage

Project memory:
```yaml
---
name: pyenv-preferences
type: project
---

python_version: "3.12.7"
naming_style: pyenv-virtualenv
environment_name: my-project
auto_activation: enabled
```

## Best Practice Review

Run review after environment creation or on request.

### Checks

| Check | Pass | Warning | Fail |
|-------|------|---------|------|
| Version pinned | Exact version in .python-version | Version range (3.12) | No version file |
| Version committed | .python-version in git | Not in git | - |
| Environment exists | venv exists and valid | - | venv missing |
| Auto-activation | pyenv-virtualenv-init configured | - | Not configured |
| IDE detection | .venv or pyenv-virtualenv style | - | Unknown style |

### Review Output

```markdown
# PyEnv Configuration Review

## Current Setup
- Python version: {version}
- Environment: {name}
- Naming: {style}
- Auto-activation: {status}

## Best Practice Compliance

| Practice | Status | Notes |
|----------|--------|-------|
| Version pinned | {status} | {notes} |
| .python-version committed | {status} | {notes} |
| Auto-activation | {status} | {notes} |

## Recommendations

{list of recommendations}
```

## Commands

### Version Detection

```bash
# List installed versions
pyenv versions --bare

# Check .python-version
test -f .python-version && cat .python-version

# Check for virtual environment
pyenv version-name  # Returns current active

# Check for pypi-template (package project)
test -f .pypi-template && echo "package-project" || echo "standard-project"

# Check for shared pypi-template virtualenv
pyenv versions --bare | grep -q "pypi-template" && echo "exists" || echo "missing"
```

### Environment Creation

```bash
# Install Python if needed
pyenv install -s {version}

# Create with pyenv-virtualenv
pyenv virtualenv {version} {name}

# Set local
pyenv local {name}

# Standard venv approach
python -m venv .venv
echo "{version}" > .python-version

# Tool virtualenv (isolated for skill/agent tools)
pyenv virtualenv {version} {tool-name}-tool
# Skill activates it during tool execution only
```

### Auto-Activation Check

```bash
# Check shell config for existing auto-activation
grep -q "pyenv virtualenv-init" ~/.zshrc && echo "configured" || echo "not configured"
```

### Package Project Commands

```bash
# Create shared pypi-template virtualenv (if missing)
pyenv virtualenv {version} pypi-template

# Create test virtualenv for specific Python version
pyenv virtualenv {test-version} {project-name}-test-{version}

# List project virtualenvs
pyenv versions --bare | grep "{project-name}"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| pyenv not found | pyenv not installed | Guide user to https://pyenv.run |
| Python version not installed | Requested version missing | Offer to install: `pyenv install {version}` |
| Environment name conflict | Name already exists | Offer: reuse, rename, delete |
| Permission denied | Shell config read-only | Provide manual instructions |

## Examples

### New Project Setup

```
User: /pyenv

Skill: Checking Python environment...

No Python version configured for this project.

Python version for this project:
  1. 3.13.0 (latest stable)
  2. 3.12.7 (LTS - recommended)
  3. 3.10.13 (maximum compatibility)
  4. 3.11.9 (installed)

Choice: 2

Virtual environment naming:
  1. .venv (standard, project-local)
  2. my-project (pyenv-virtualenv style)

Choice: 1

✓ Installing Python 3.12.7...
✓ Creating virtual environment .venv
✓ Setting Python version to 3.12.7

✓ Auto-activation already configured (pyenv-virtualenv-init found)

Environment ready! Python 3.12.7 in .venv
```

### Python Package Project

```
User: /pyenv

Skill: Checking Python environment...

Detected Python package project (.pypi-template found).

Package projects use:
  1. Shared pypi-template virtualenv (for packaging tools)
  2. Test virtualenvs for multi-version testing

Found: Python 3.12.7 (from .python-version)
Found: pypi-template virtualenv ✓

Test virtualenvs:
  3.10.13: missing
  3.11.9: missing
  3.12.7: missing (current version)

Create test virtualenvs for multi-version testing?
  1. None (use current version only)
  2. Create for all supported versions
  3. Create for specific versions

Choice: 2

✓ Creating test virtualenvs...
✓ Created my-package-test-3.10.13
✓ Created my-package-test-3.11.9
✓ Created my-package-test-3.12.7

Test with: pyenv activate my-package-test-3.12.7 && pytest
```

### Tool Virtualenv Setup

```
User: I need to set up a tool virtualenv for the SVG skill

Skill: Setting up tool virtualenv...

Tool name: svg-creation-tool
Required packages: drawsvg, svgwrite
Python version: (using project default 3.12.7)

Create virtualenv: svg-creation-tool? [Y/n]: Y

✓ Creating virtualenv svg-creation-tool
✓ Installing drawsvg...
✓ Installing svgwrite...

Tool virtualenv ready!
Activation: pyenv activate svg-creation-tool
Deactivation: pyenv deactivate

Note: Skills should activate this only during tool execution.
```

### Existing Project with Auto-Activation

```
User: /pyenv

Skill: Checking Python environment...

Found Python 3.12.7 (from .python-version)
Found virtual environment: my-project ✓
Auto-activation: already configured ✓

Environment is ready. What would you like to do?
  1. Review best practices
  2. Recreate environment
  3. Change Python version
  4. Manage test virtualenvs
  5. Exit

Choice: 1

[Best practice review output]
```

## Integration

### With Python Skill

Coordinate with python skill for:
- Project detection
- Dependency management
- Virtual environment context

### With Research Skill

If user asks about Python versions or pyenv features, research skill can provide current information.

## Constraints

- DO NOT modify shell config without user confirmation
- DO NOT commit .python-version without user approval
- ALWAYS check for existing environments before creating
- ALWAYS prefer exact version pins (3.12.7) over ranges (3.12)
- ALWAYS verify pyenv is installed before proceeding

## Implementation

### Scripts

The skill uses Python scripts in `scripts/` directory:

| Script | Purpose |
|--------|---------|
| `detect.py` | Environment detection |
| `create_env.py` | Environment creation |
| `preferences.py` | Preference storage |
| `review.py` | Best practice review |
| `skill_context.py` | Context generation |
| `integrate.py` | Main integration entry point |

### Usage in Skill

```python
# Get detection context
context = run_python_script("integrate.py --context --json")

# Get questions for AskUserQuestion
questions = run_python_script("integrate.py --questions")

# Run best practice review
review = run_python_script("review.py")
```

### Dialog Flow

1. **Detection Phase**
   ```python
   context = detect.detect_environment()
   ```

2. **Question Generation**
   ```python
   questions = get_dialog_questions(context)
   # Returns AskUserQuestion format
   ```

3. **Answer Processing**
   ```python
   actions = process_answers(answers, context)
   ```

4. **Execution**
   ```python
   messages = execute_actions(actions, context)
   ```

### Integration Points

- Use `AskUserQuestion` with questions from `get_dialog_questions()`
- Execute actions based on answers
- Display best practice review with `review.run_best_practice_review()`
- Store preferences with `preferences.record_version_choice()`

## Lessons Learned

### Session 2026-04-06: Tool Virtualenv for Skills

**Context:** Created `svg-skill` virtualenv for the SVG skill's drawsvg dependency.

**What worked:**
1. Used `pyenv virtualenv {version} {skill-name}` naming convention
2. Activated with `PYENV_VERSION=svg-skill python script.py`
3. Installed only required packages (drawsvg)
4. Clean separation from project environments

**Pattern for Skill Virtualenvs:**
```bash
# Create
pyenv virtualenv {python-version} {skill-name}

# Use in scripts
PYENV_VERSION={skill-name} python {script}.py

# Install packages
pyenv activate {skill-name}
pip install {packages}
```

**Naming Convention:**
- Use simple names: `svg-skill`, not `svg-creation-skill-tool`
- Keep name consistent with skill directory name
- Don't append `-tool` or `-env` suffix