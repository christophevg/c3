# Agent Permissions Refactoring

**Date:** 2026-05-26
**Status:** In Progress

## Summary

Refactoring agent permissions and workflows to:
1. Make agents more autonomous (less interactive intervention required)
2. Enforce standard workflow adherence
3. Keep context small through delegation to sub-agents
4. Standardize release workflow

## Goals

- Project-manager delegates everything to sub-agents (avoid context growth)
- All decisions through PR conversations (not AskUserQuestion)
- Sub-agents work autonomously and report back
- Clear ownership: functional-analyst owns TODO.md, release-manager handles releases

---

## 1. Agent Changes

### 1.1 Create: release-manager

**Purpose:** Single authority for source control and release operations

**Absorbs:** git-manager (deprecate)

**Responsibilities:**
- Report project state at session start (branch, PR status, issues, recent activity)
- Execute git operations
- Execute GitHub API operations (PRs, issues, releases)
- Execute release workflow

**Permissions:**
```yaml
allow:
  - skill
  - agent
  - Read
  - Bash(pwd)
  - Bash(ls *)
  - Bash(git *)
  - Bash(uv *)
  - Bash(twine *)
  - Bash(gh *)
deny:
  - Bash(gh auth *)
```

**Skills to invoke:** `c3:release`, `c3:github`, `c3:git-*`, `c3:pypi-publish`

---

### 1.2 Modify: project-manager

**Current permissions:** `Read`, `Glob`, `Grep`, `Skill`, `Write`, `Edit`, `Bash`, `AskUserQuestion`, `PushNotification`, `Agent`

**New permissions:**
```yaml
allow:
  - skill
  - agent
  - Read
  - Bash(pwd)
  - Bash(ls *)
```

**Workflow changes:**
1. **Session start**: Ask release-manager for project state
2. **All decisions through PR comments** (not AskUserQuestion)
3. **Delegate all work to sub-agents**:
   - Functional analyst: analysis, TODO management
   - Developer: implementation
   - Testing-engineer: test creation/validation
   - Release-manager: git, github, releases

---

### 1.3 Modify: python-developer

**Current permissions:** `Read`, `Glob`, `Grep`, `Skill`, `Write`, `Edit`, `Bash`

**New permissions:**
```yaml
allow:
  - Read
  - Glob
  - Grep
  - Skill
  - Write
  - Edit
  - Bash(uv *)
  - Bash(make *)
```

**Workflow:**
- Full autonomy on confirmed analysis implementation
- Must deliver: working code + passing tests + updated documentation
- Escalate blocking issues back to functional analyst
- Follow pre-commit workflow in c3:python skill

---

### 1.4 Modify: testing-engineer

**Current permissions:** `Read`, `Glob`, `Grep`, `Skill`, `Write`, `Edit`, `Bash`, `AskUserQuestion`, `PushNotification`

**New permissions:**
```yaml
allow:
  - Read
  - Glob
  - Grep
  - Skill
  - Write
  - Edit
  - Bash(uv *)
  - Bash(make *)
```

**Workflow:**
- Before implementation: Create test stubs (TDD)
- After implementation: Validate test coverage
- Report results to project-manager

---

### 1.5 Modify: functional-analyst

**Current permissions:** `Read`, `Glob`, `Grep`, `Skill`, `Write`, `Edit`, `AskUserQuestion`, `PushNotification`

**Permissions remain same:**
```yaml
allow:
  - Read
  - Glob
  - Grep
  - Skill
  - Write
  - Edit
  - AskUserQuestion
  - PushNotification
```

**Responsibilities:**
- Create and own TODO.md lifecycle (entire lifecycle)
- Analyze features/bugs
- Create analysis documents in `analysis/` folder
- Incorporate owner feedback into revised analysis
- Mark TODO items complete after merge

---

## 2. Skill Changes

### 2.1 Create: c3:release

**Purpose:** Standardized release workflow

**When to use:** User asks to "prepare release", "publish", or release-manager starts release process

**Workflow:**
```
1. Determine version bump
   - Review commits since last tag
   - feat: → minor, fix: → patch, breaking: → major
   - Ask owner if unclear

2. Update version files
   - pyproject.toml
   - src/**/__init__.py (if exists)

3. Update changelog
   - docs/changelog.md or CHANGELOG.md

4. Run local pre-publish checks
   - make test
   - make lint
   - make typecheck

5. Commit version bump
   - git add pyproject.toml changelog __init__.py
   - git commit -m "chore: bump version to X.Y.Z"

6. Push
   - git push <remote> <branch>

7. Wait for CI to pass
   - gh pr checks or gh run watch
   - If CI fails: fix with additional commits, return to step 4

8. Build package
   - rm -rf dist/
   - uv build

9. Verify package contents
   - unzip -l dist/*.whl | head -40

10. Create annotated tag
    - git tag -a vX.Y.Z -m "Release X.Y.Z: <title>"
    - git push <remote> vX.Y.Z

11. Create GitHub release
    - gh release create vX.Y.Z --title "vX.Y.Z - <title>" --notes "..."

12. Upload to PyPI
    - uv run twine upload dist/*
```

---

### 2.2 Modify: c3:project-manage

**Add sections:**

#### Implementation Plan Workflow

```markdown
## Implementation Plan Workflow

After analysis is complete:

1. Create PR branch with analysis documents committed
2. Post implementation plan as PR comment (NOT AskUserQuestion)
3. Wait for owner approval in PR comments
4. If owner requests changes:
   - Functional analyst incorporates feedback
   - Update analysis documents (new commit)
   - Post revised plan as PR comment
   - Return to step 3
5. If owner rejects entirely:
   - Close PR
   - Close related issue (if applicable)
   - Report to owner
6. If owner approves:
   - Proceed to implementation
```

#### Session Start Workflow

```markdown
## Session Start

1. Ask release-manager for project state:
   - Current branch
   - Open PRs
   - Recent commits
   - Related issues
2. Based on state, determine next action:
   - Continue in-progress PR
   - Start new feature
   - Address review feedback
   - Prepare release
```

#### Post-Merge Workflow

```markdown
## Post-Merge Workflow

After PR is merged:

1. Functional analyst updates TODO.md (mark items complete)
2. Ask owner: prepare release or continue with next task?
3. If release:
   - Delegate to release-manager
```

---

### 2.3 Modify: c3:commit

**Add section:**

```markdown
## Pre-Commit Validation

Before committing, verify:

1. Trailing newlines in all edited files
   - No file should end without newline
   - Can check with: `test "$(tail -c1 file | wc -l)" -ne 0`

2. Code formatting (Python projects)
   - Run: `ruff format src tests`
   - Or: `make lint` if it includes formatting

3. If validation fails:
   - Fix issues
   - Re-stage files
   - Attempt commit again
```

---

### 2.4 Modify: c3:python

**Add sections:**

```markdown
## Pre-Commit Workflow

Before committing Python code:

1. `make test` - Verify tests pass
2. `make lint` - Check linting
3. `ruff format src tests` - Format code (if not in make lint)
4. `make typecheck` - Type checking

Combined: `make test && make lint && ruff format src tests && make typecheck`

## Security Patterns

### Atomic File Creation for Sensitive Files

When creating files with sensitive content (session cache, credentials, etc.):

```python
import os

# Atomic creation with secure permissions (0600)
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'w') as f:
    f.write(content)
```

This ensures:
- No race condition (O_EXCL fails if file exists)
- Correct permissions from creation
- Atomic operation
```

---

### 2.5 Modify: c3:pypi-publish

**Add section:**

```markdown
## Version Bump Decision

Before updating version, determine bump type:

| Change Type | Bump | Example |
|-------------|------|---------|
| Bug fixes | Patch | 0.3.1 → 0.3.2 |
| New features (backward compatible) | Minor | 0.3.1 → 0.4.0 |
| Breaking changes | Major | 0.3.1 → 1.0.0 |

Check recent commits:
- `feat:` commits → Minor bump
- `fix:` commits → Patch bump
- Breaking API changes → Major bump
```

**Note:** This skill is now a sub-step of `c3:release`. The full release workflow is in `c3:release`.

---

## 3. Document Organization Changes

### 3.1 Analysis Folder Structure

**New structure:**
```
analysis/
├── <feature-analysis>.md      # Feature analysis documents
├── bug/                        # Bug analysis (moved from docs/bug-analysis/)
│   └── <bug-analysis>.md
└── reporting/                  # Consensus reports (moved from reporting/)
    └── <consensus-report>.md
```

**Skills/Agents to update:**
- Functional analyst → create in `analysis/`
- Bug-fixing agents → create in `analysis/bug/`
- Any agent creating consensus reports → create in `analysis/reporting/`

---

## 4. Permissions Summary Table

| Agent | Tools (Agent Frontmatter) | Notes |
|-------|---------------------------|-------|
| **project-manager** | `Read`, `Skill`, `Agent`, `AskUserQuestion`, `PushNotification` | No Bash - delegates everything |
| **release-manager** | `Read`, `Glob`, `Grep`, `Skill`, `Agent`, `Bash`, `AskUserQuestion`, `PushNotification` | Full Bash, avoid `gh auth` |
| **python-developer** | `Read`, `Glob`, `Grep`, `Skill`, `Write`, `Edit`, `Bash`, `AskUserQuestion` | Should use `make` and `uv` only |
| **testing-engineer** | `Read`, `Glob`, `Grep`, `Skill`, `Write`, `Edit`, `Bash`, `AskUserQuestion` | Should use `make` and `uv` only |
| **functional-analyst** | `Read`, `Glob`, `Grep`, `Skill`, `Write`, `Edit`, `AskUserQuestion`, `PushNotification` | No Bash needed |

**Important Limitation:** The agent frontmatter `tools:` field does NOT support tool arguments like `Bash(uv *)`. It only accepts simple tool names.

**For fine-grained Bash restrictions, use settings.json:**

```json
{
  "permissions": {
    "deny": [
      "Bash(gh auth *)"
    ]
  }
}
```

**Current approach:**
1. Remove Bash entirely from project-manager (relies on skill instructions + delegation)
2. Give other agents full Bash access
3. Restrict through skill instructions (e.g., "use `make` and `uv` only")
4. Optionally add settings.json deny patterns for security-critical commands

---

## 5. Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ PROJECT-MANAGER (Orchestrator)                                  │
│ Permissions: skill, agent, Read, Bash(pwd), Bash(ls *)         │
└─────────────────────────────────────────────────────────────────┘
         │
         │ delegates to
         ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ FUNCTIONAL      │  │ PYTHON          │  │ TESTING         │
│ ANALYST         │  │ DEVELOPER       │  │ ENGINEER        │
│                 │  │                 │  │                 │
│ Owns TODO.md    │  │ Implements      │  │ TDD stubs       │
│ Analysis docs   │  │ Tests + docs    │  │ Coverage valid. │
└─────────────────┘  └─────────────────┘  └─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ RELEASE-MANAGER (Source Control Authority)                      │
│ Permissions: skill, agent, Read, Bash(git/uv/twine/gh/*)       │
│ Deny: Bash(gh auth *)                                          │
└─────────────────────────────────────────────────────────────────┘
         │
         │ invokes skills
         ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ c3:release      │  │ c3:github       │  │ c3:pypi-publish │
│ (new)           │  │                 │  │                 │
│ Full workflow   │  │ PRs, issues     │  │ Upload step     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## 6. Implementation Order

1. ✅ Create `c3:release` skill
2. ✅ Create `release-manager` agent
3. ✅ Modify `project-manager` agent
4. ✅ Modify `python-developer` agent
5. ✅ Modify `testing-engineer` agent
6. ✅ Modify `functional-analyst` agent (no changes needed)
7. ✅ Modify `c3:project-manage` skill
8. ✅ Modify `c3:commit` skill
9. ✅ Modify `c3:python` skill
10. ✅ Modify `c3:pypi-publish` skill
11. ✅ Deprecate `git-manager` agent (keep file, update description)

## 7. Key Fix Applied

**Problem:** Project-manager was still making `git pull` and `gh issue list` calls despite having restricted permissions.

**Root cause:** The `c3:project-manage` skill contained instructions to run git/gh commands directly, and skill instructions override permission concerns in the agent's behavior.

**Solution:** Updated `c3:project-manage` skill to:
1. Remove all direct git/gh command instructions
2. Delegate all git/gh operations to release-manager via Agent calls
3. Update all workflow steps to use Agent delegation pattern

**Pattern established:** Skills for restricted agents should NEVER contain direct command instructions that the agent doesn't have permission to run. Instead, they should delegate to agents with appropriate permissions.

---

## 8. Open Items for Future Sessions

| Item | Notes |
|------|-------|
| Config discovery testing patterns | User wants to address separately |
| Agent frontmatter "knowledge to apply" | Mentioned but deferred |
| Other cross-cutting patterns | To be identified in future sessions |