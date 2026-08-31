---
name: git-scripting
description: Guide safe git command usage in scripts, Makefiles, and automation. Use when writing shell scripts or Makefiles that interact with git repositories, or when user says "/git-scripting".
type: knowledge
---

# Git Scripting

Safe patterns for git commands in scripts, Makefiles, and automation.

# When

Auto-triggers (knowledge skill — domain mention suffices): writing Makefile
targets that touch git, shell scripts that check git state, automating git
across repositories, CI scripting with git commands. Also on explicit
invocation.

# Inputs

A script, Makefile, or automation context that will run git commands —
existing or being written.

# Core patterns

## Current branch, safely

```bash
# Handles normal branches and detached HEAD
branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
```

## Unpushed commits — current branch only

WRONG: `git log --branches --not --remotes --exit-code` — matches ALL local
branches (false positives on local-only branches, pushes even when the
current branch is clean). Use:

```bash
ahead=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "0")
if [ "$ahead" -gt 0 ]; then
  git push
fi
```

## Repository check

```bash
# plain checkout… …or worktrees/submodules:
if git -C "$dir" rev-parse --git-dir > /dev/null 2>&1; then ...
```

## Change checks

```bash
git diff --cached --quiet      # staged changes?
git diff --quiet               # unstaged changes?
git diff-index --quiet HEAD    # any uncommitted change (both kinds)
git ls-files --others --exclude-standard   # untracked files
```

# Common mistakes

1. `--branches` matches ALL local branches — script false positives. Scope
   to the current branch.
2. Missing upstream: `git rev-list --count @{upstream}..HEAD` fails on a
   new branch — append `2>/dev/null || echo "0"`.
3. Unsilenced stderr pollutes automation output — suppress for expected
   failure paths.
4. Check commands without `--quiet` dump payload into logs.

# Makefile specifics

- `$$` escapes to a single `$` for the shell; a single `$` is eaten by make.
- Subshell scope: `cd dir && ahead=$(...)` loses `ahead` after the line —
  keep dependent commands in the same subshell.
- Non-file-producing targets are declared `.PHONY`.

# Validation checklist

- [ ] Missing upstream handled gracefully (default, not failure)
- [ ] Current branch only — never `--branches` in scripts
- [ ] stderr suppressed for expected-failure paths
- [ ] `--quiet` on check commands
- [ ] Detached HEAD handled
- [ ] Worktree-safe where applicable
- [ ] Tested on clean AND dirty repos

# Deliverables

- Correct, quiet, upstream-safe git snippets for scripts/Makefiles.

# Related

- `c3:commit` — commit conventions once the script's changes land
- `c3:git-activity-report` — summarizing multi-repo activity
- `c3:release-manager` — delegate for operational git work