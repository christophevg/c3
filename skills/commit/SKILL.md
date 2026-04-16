---
name: commit
description: Guide git commit operations with atomic commits and conventional format. Use when committing changes, creating commits, or when user says "/commit", "commit these changes", "create a commit". Analyzes changes, groups by functionality, detects sensitive files, and waits for user verification.
---

# commit

Guide git commit operations with atomic commits, functionality-based grouping, and conventional commit format.

## Overview

| Capability | Description |
|------------|-------------|
| Atomic commits | Group changes by logical functionality |
| Conventional format | Apply type/scope/description format |
| Sensitive file detection | Block .env, *.key, credentials files |
| User verification | Wait for approval before committing |

## When to Use This Skill

Use this skill when:
- User wants to commit changes
- User invokes "/commit" command
- User says "commit these changes" or "create a commit"
- Multiple changes need grouping analysis

## Pre-Commit Checklist

Before any commit, verify:

1. **Changes staged** - Run `git status` to check staged files
2. **Sensitive files** - Block if .env, *.key, *.pem, secrets.*, credentials.* detected
3. **Atomic grouping** - Verify changes represent one logical change
4. **User approval** - Present analysis and wait for confirmation

## Sensitive File Detection

Block commits containing these files:

| Pattern | Risk Level | Action |
|---------|------------|--------|
| `.env`, `.env.local`, `.env.*.local` | High | Block, warn about secrets |
| `*.pem`, `*.key` | High | Block, warn about credentials |
| `secrets.*`, `credentials.*` | High | Block, warn about sensitive data |
| `password`, `api_key`, `token` in code | Medium | Warn, suggest .env |

If sensitive file detected:
1. Immediately block commit
2. Warn user with specific file name
3. Suggest remediation: `git restore --staged <file>`
4. Recommend adding to .gitignore

## Functionality Analysis

### Identifying Logical Groupings

Analyze staged changes by:

**File Type:**
- `*.py` backend changes → separate commit
- `*.vue`, `*.tsx` frontend changes → separate commit
- `*.test.*`, `*_test.*` test changes → separate commit
- `*.md` documentation → separate commit

**Directory:**
- `src/api/` → API changes
- `src/models/` → data model changes
- `src/ui/` → UI changes
- `tests/` → test changes

**Change Type:**
- New functionality → `feat`
- Bug fixes → `fix`
- Refactoring → `refactor`
- Documentation → `docs`
- Tests → `test`

### Atomic Commit Test

Can you describe the commit without using "and"?

- ✓ "Fix null pointer exception on empty cart checkout"
- ✗ "Fix cart bug and update user model and add tests"

If multiple "and"s needed, split into separate commits.

### Handling Multi-Concern Files

When a file touches multiple concerns:

1. Use `git add -p` to stage specific hunks
2. Create separate commits for each logical change
3. If changes are intertwined, single commit with detailed body

## Commit Message Guidelines

### Conventional Commit Format

```
type(scope): description

[optional body]

[optional footer(s)]
```

### Core Types

| Type | Usage | Example |
|------|-------|---------|
| `feat` | New feature | `feat(cart): add quantity adjustment` |
| `fix` | Bug fix | `fix(checkout): handle empty cart` |
| `refactor` | Code restructuring | `refactor(api): simplify user endpoint` |
| `perf` | Performance improvement | `perf(search): optimize query` |
| `test` | Adding/updating tests | `test(cart): add checkout edge cases` |
| `docs` | Documentation changes | `docs(readme): update install steps` |
| `style` | Formatting (no logic change) | `style: fix indentation` |
| `chore` | Build, deps, tooling | `chore: update dependencies` |

### Seven Rules

1. Separate subject from body with a blank line
2. Limit subject to 50 characters
3. Capitalize the subject line
4. Don't end with a period
5. Use imperative mood ("Add feature" not "Added feature")
6. Wrap body at 72 characters
7. Explain what and why, not how

## Workflow Steps

### 1. Analyze Changes

```bash
git status
git diff --cached --stat
git diff --cached
```

Categorize changes:
- By file type (backend, frontend, tests, docs)
- By directory (api, models, ui, tests)
- By change type (feat, fix, refactor)

### 2. Present Analysis

Show user:
- Grouped changes with recommendations
- Any sensitive files detected
- Suggested commit boundaries

Then use AskUserQuestion to confirm the approach:
```
AskUserQuestion with:
  question: "How would you like to proceed with these changes?"
  header: "Commit plan"
  options:
    - label: "Proceed with suggested commits"
      description: "Create commits as proposed above"
    - label: "Combine into single commit"
      description: "Merge all changes into one commit"
    - label: "Cancel"
      description: "Abort without committing"
```

### 3. Validate Pre-conditions

- Check for `.pre-commit-config.yaml` or `package.json` with lint-staged
- Verify user has reviewed changes (per user memory)
- Confirm commit message format

### 4. Create Commits

For single logical change:
```bash
git commit -m "type(scope): description"
```

For multiple logical changes:
1. Propose grouping to user
2. Let user confirm or adjust
3. Create commits one by one after verification

### 5. Post-Commit

- Show commit hash
- Remind about push (don't auto-push)

## User Verification Requirement

**CRITICAL:** Never commit without user verification.

### Using AskUserQuestion for Confirmation

Always use the AskUserQuestion tool to request commit confirmation. This provides a clean UX with multiple choice options:

```
AskUserQuestion with:
  question: "Ready to commit? [commit message preview]"
  header: "Commit"
  options:
    - label: "Yes, proceed"
      description: "Create the commit with the proposed message"
    - label: "No, cancel"
      description: "Abort the commit operation"
    - label: "Edit message first"
      description: "You want to modify the commit message before proceeding"
  multiSelect: false
```

The tool automatically provides an "Other" option for custom input, allowing the user to specify alternative instructions.

### Verification Workflow

Per user memory (`commit_after_testing.md`):
1. Wait for visual confirmation of changes
2. User runs incremental builds locally
3. Request explicit approval via AskUserQuestion
4. Only proceed after user selects "Yes, proceed"

## Edge Cases

### Merge Conflicts

1. Explain how to resolve conflicts
2. Don't auto-commit after resolution
3. User must verify resolved changes

### Work in Progress

1. Support `wip:` or `--wip` prefix
2. Allow skipping pre-commit for drafts
3. Remind user to clean up before final commit

### Empty Commit

1. Warn if no changes staged
2. Suggest `git add` for specific files
3. Don't create empty commits

## Related Patterns

- `patterns/atomic-commits.md` - Detailed atomic commit patterns
- `patterns/conventional-commits.md` - Conventional commit format guide

## Common Issues

| Issue | Solution |
|-------|----------|
| Changes affect multiple concerns | Propose splitting into separate commits |
| Sensitive file in commit | Block immediately, warn user, suggest .gitignore |
| Pre-commit hooks failing | Explain failure, suggest fixes, don't skip without user approval |
| Commit message too long | Keep subject under 50 chars, move details to body |
| User didn't review changes | Present diff, wait for explicit approval |