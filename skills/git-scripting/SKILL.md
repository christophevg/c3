---
name: git-scripting
description: Guide safe git command usage in scripts, Makefiles, and automation. Use when writing shell scripts that interact with git repositories.
---

# Git Scripting

Safe patterns for using git commands in scripts, Makefiles, and automation contexts.

## When to Use This Skill

**Automatic triggers:**
- Writing Makefile targets that interact with git
- Creating shell scripts that check git state
- Automating git operations across multiple repositories
- Building CI/CD scripts with git commands

**Manual invocation:**
- User asks about git commands in scripts
- User says "/git-scripting"
- User requests Makefile targets for git operations

## Common Patterns

### Checking for Unpushed Commits

**WRONG:** `git log --branches --not --remotes --exit-code`
- Checks ALL branches (including untracked ones)
- Will trigger false positives for local-only branches
- Returns exit 0 when ANY branch has commits not in remotes

```bash
# DON'T USE THIS
if git log --branches --not --remotes --exit-code > /dev/null 2>&1; then
  git push  # Wrong! Pushes even when current branch is clean
fi
```

**CORRECT:** `git rev-list --count @{upstream}..HEAD`
- Checks only the current branch against its upstream
- Returns `0` if no upstream configured (safe default)
- Returns count of commits ahead

```bash
# USE THIS INSTEAD
ahead=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "0")
if [ "$ahead" -gt 0 ]; then
  git push
fi
```

### Iterating Over Git Repositories

```makefile
.PHONY: push

push:
	@for dir in */; do \
		if [ -d "$$dir/.git" ]; then \
			cd "$$dir" && \
			branch=$$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null); \
			ahead=$$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "0"); \
			if [ "$$ahead" -gt 0 ]; then \
				echo "Pushing $$dir ($$branch) - $$ahead commits ahead"; \
				git push; \
			fi; \
			cd ..; \
		fi; \
	done
```

### Getting Current Branch Name Safely

```bash
# Handles both normal branches and detached HEAD
branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
```

### Checking if Directory is a Git Repository

```bash
if [ -d "$dir/.git" ]; then
  # It's a git repository
fi

# Or for worktrees and submodules:
if git -C "$dir" rev-parse --git-dir > /dev/null 2>&1; then
  # It's a git repository (including worktrees)
fi
```

### Checking for Uncommitted Changes

```bash
# Check for staged changes
if ! git diff --cached --quiet; then
  echo "Has staged changes"
fi

# Check for unstaged changes
if ! git diff --quiet; then
  echo "Has unstaged changes"
fi

# Check for either (staged or unstaged)
if ! git diff --quiet --cached && ! git diff --quiet; then
  # Actually, this is wrong - use:
if ! git diff-index --quiet HEAD; then
  echo "Has uncommitted changes"
fi
```

### Checking for Untracked Files

```bash
# Check for untracked files
if [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "Has untracked files"
fi
```

## Common Mistakes to Avoid

### 1. Using `--branches` in Scripts

**Problem:** `--branches` matches ALL local branches, not just the current one.

```bash
# Wrong - checks all branches
git log --branches --not --remotes

# Correct - checks current branch only
git rev-list --count @{upstream}..HEAD
```

### 2. Forgetting to Handle Missing Upstream

**Problem:** New branches may not have an upstream configured.

```bash
# Wrong - fails if no upstream
git rev-list --count @{upstream}..HEAD

# Correct - gracefully handle missing upstream
git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "0"
```

### 3. Not Silencing Errors

**Problem:** Git errors can pollute script output.

```bash
# Wrong - shows error if no upstream
branch=$(git symbolic-ref --short HEAD)

# Correct - suppresses error
branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
```

### 4. Forgetting `--quiet` for Check Commands

**Problem:** Output from check commands clutters script output.

```bash
# Wrong - outputs diff content
if git diff; then
  echo "Has changes"
fi

# Correct - silent check
if ! git diff --quiet; then
  echo "Has changes"
fi
```

## Makefile-Specific Notes

### Escaping Dollar Signs

In Makefiles, `$$` becomes a single `$` in the shell:

```makefile
# Wrong - Make interprets $dir
echo $dir

# Correct - Make passes $dir to shell
echo $$dir
```

### Subshell Variable Scope

Variables set in subshells don't persist:

```makefile
# Wrong - 'ahead' is empty after cd ends
cd dir && ahead=$(git rev-list --count @{upstream}..HEAD)
echo $$ahead  # Empty!

# Correct - all in same subshell
cd dir && ahead=$(git rev-list --count @{upstream}..HEAD) && echo $$ahead
```

### Phony Targets

Always declare targets that don't create files as `.PHONY`:

```makefile
.PHONY: push status clean

push:
	# ...

status:
	# ...
```

## Validation Checklist

Before finalizing a git script:

- [ ] Handles missing upstream gracefully (returns 0 or default)
- [ ] Only checks current branch, not all branches
- [ ] Suppresses stderr for expected failure cases
- [ ] Uses `--quiet` for check commands
- [ ] Handles detached HEAD state
- [ ] Works with worktrees if applicable
- [ ] Tested on clean repo (no false positives)
- [ ] Tested on dirty repo (detects correctly)