# Atomic Commits Pattern

## Definition

An atomic commit represents one logical change - one reason to exist. You should be able to describe it in a single sentence without using "and".

## The Atomic Test

**Pass:** Can describe without "and"
- ✓ "Fix null pointer exception on empty cart checkout"
- ✓ "Add quantity adjustment to cart items"
- ✓ "Update user model to include preferences"

**Fail:** Requires "and" to describe
- ✗ "Fix cart bug and update user model and add tests"
- ✗ "Add feature X and refactor module Y"

## Benefits

| Benefit | Description |
|---------|-------------|
| Easier review | One concept to understand |
| Simple revert | Remove one change cleanly |
| Git bisect | Effective debugging |
| Clean cherry-pick | Pick specific changes |

## Splitting Strategies

### By File Type

Group changes by file type:

```
# Commit 1: Backend changes
git add src/api/*.py
git commit -m "feat(api): add user preferences endpoint"

# Commit 2: Frontend changes
git add src/ui/*.vue
git commit -m "feat(ui): add preferences panel"

# Commit 3: Tests
git add tests/*.py
git commit -m "test(api): add preferences endpoint tests"
```

### By Directory

Group changes by logical area:

```
# Commit 1: API changes
git add src/api/
git commit -m "feat(api): implement user preferences"

# Commit 2: Model changes
git add src/models/
git commit -m "feat(models): add preferences schema"

# Commit 3: UI changes
git add src/ui/
git commit -m "feat(ui): add preferences interface"
```

### By Change Type

Group by the type of change:

| Change Type | Commit Type | Example |
|-------------|-------------|---------|
| New feature | `feat` | Adding new functionality |
| Bug fix | `fix` | Fixing broken behavior |
| Refactoring | `refactor` | Code cleanup, no behavior change |
| Documentation | `docs` | README, comments, docs |
| Tests | `test` | Adding/updating tests |

## Using git add -p

When a file has multiple logical changes:

```bash
git add -p filename.py
```

This allows:
1. Stage specific hunks one by one
2. Review each change before staging
3. Create separate commits for each logical change

**Workflow:**
```bash
# Stage first logical change
git add -p file.py
# Select 'y' for first hunk, 'n' for others
git commit -m "feat(module): add feature X"

# Stage second logical change
git add -p file.py
# Select 'y' for second hunk
git commit -m "fix(module): handle edge case Y"
```

## Decision Tree

```
Multiple files staged?
├── Yes, same logical change?
│   └── Single commit with clear message
├── Yes, different logical changes?
│   └── Split into separate commits
└── Single file?
    ├── Single concern?
    │   └── Single commit
    └── Multiple concerns?
        ├── Changes in separate hunks?
        │   └── Use git add -p, create separate commits
        └── Changes intertwined?
            └── Single commit with detailed body
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| "Fix typo and add feature" | Two logical changes | Split into fix and feat commits |
| "Update stuff" | Vague message | Be specific about what changed |
| Huge diff in one commit | Hard to review | Split into logical commits |
| Mixing feat and fix | SemVer confusion | Separate feature and fix commits |

## Examples

### Good: Atomic Commits

```bash
# Commit 1: The fix
git commit -m "fix(cart): handle empty cart checkout"

# Commit 2: The feature
git commit -m "feat(cart): add quantity adjustment"

# Commit 3: The tests
git commit -m "test(cart): add checkout and quantity tests"
```

### Bad: Non-Atomic Commit

```bash
# Don't do this
git commit -m "fix cart bug and add quantity feature and add tests"
```

This commit:
- Mixes fix and feature (SemVer confusion)
- Is hard to review
- Can't be cleanly reverted
- Breaks git bisect