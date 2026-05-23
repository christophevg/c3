# Branch Workflow

## Branch Types

| Type | Purpose | Example |
|------|---------|---------|
| `feature/` | New features | `feature/42-async-agent` |
| `fix/` | Bug fixes | `fix/123-null-pointer` |
| `docs/` | Documentation | `docs/api-reference` |
| `chore/` | Maintenance | `chore/update-deps` |
| `refactor/` | Code refactoring | `refactor/auth-module` |
| `test/` | Test improvements | `test/add-integration-tests` |

## Naming Convention

```
{type}/{issue-number}-{short-description}
```

- Use kebab-case for description
- Keep description under 50 characters
- Include issue number if applicable
- Use imperative mood (add-user-auth, not added-user-auth)

## Branch Lifecycle

```
main/master
    │
    ├── Create branch
    │   git checkout -b feature/42-new-feature
    │
    ├── Work on branch
    │   git add, git commit, git push
    │
    ├── Create PR
    │   gh pr create
    │
    ├── Review & CI
    │   gh pr checks, gh run view
    │
    ├── Merge
    │   gh pr merge (by user)
    │
    └── Cleanup
        git checkout main
        git pull
        git branch -d feature/42-new-feature
```

## Commands

### Creating Branches

```bash
# Check current branch
git branch --show-current

# Create from current branch
git checkout -b feature/42-new-feature

# Create from specific branch
git checkout -b feature/42-new-feature main

# Push to remote (set upstream)
git push -u origin feature/42-new-feature
```

### Managing Branches

```bash
# List local branches
git branch

# List all branches (including remote)
git branch -a

# Delete local branch (merged)
git branch -d feature/42-new-feature

# Delete local branch (force, unmerged)
git branch -D feature/42-new-feature

# Delete remote branch
git push origin --delete feature/42-new-feature
```

### Branch Status

```bash
# See branches with last commit
git branch -v

# See merged branches
git branch --merged main

# See unmerged branches
git branch --no-merged main

# Check if branch tracks remote
git rev-parse --abbrev-ref --symbolic-full-name @{upstream}
```

## Safety Rules

1. **Never commit directly to main/master** - Always use feature branches
2. **Never force push to shared branches** - Use `--force-with-lease` if necessary
3. **Pull before creating branch** - Ensure you're up to date
4. **Delete after merge** - Keep branch list clean

## Common Scenarios

### Scenario: Start New Feature

```bash
# 1. Ensure main is up to date
git checkout main
git pull

# 2. Create feature branch
git checkout -b feature/42-new-feature

# 3. Push to remote
git push -u origin feature/42-new-feature
```

### Scenario: Feature Complete, Ready for PR

```bash
# 1. Ensure all commits pushed
git status

# 2. If unpushed commits
git push

# 3. Create PR
gh pr create --title "feat: add new feature" --body "..."
```

### Scenario: Branch Behind Main

```bash
# 1. Fetch latest
git fetch origin

# 2. Rebase on main
git rebase origin/main

# 3. Force push (with lease for safety)
git push --force-with-lease
```

### Scenario: Fix Commit on Wrong Branch

```bash
# 1. Create correct branch from current position
git checkout -b feature/42-correct-branch

# 2. Reset wrong branch
git checkout feature/41-wrong-branch
git reset --hard origin/feature/41-wrong-branch

# 3. Push correct branch
git checkout feature/42-correct-branch
git push -u origin feature/42-correct-branch
```