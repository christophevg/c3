# Conventional Commits Pattern

## Format

```
type(scope): description

[optional body]

[optional footer(s)]
```

## Components

### Type (Required)

The type indicates the category of change:

| Type | Usage | SemVer Impact |
|------|-------|---------------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `refactor` | Code restructuring (no behavior change) | - |
| `perf` | Performance improvement | - |
| `test` | Adding/updating tests | - |
| `docs` | Documentation changes | - |
| `style` | Formatting (no logic change) | - |
| `chore` | Build, deps, tooling | - |
| `ci` | CI/CD pipeline changes | - |
| `build` | Build system changes | - |

### Scope (Optional)

The scope indicates what part of the codebase is affected:

```bash
feat(api): add user endpoint
fix(ui): resolve button alignment
docs(readme): update installation steps
```

Common scopes:
- Module names: `api`, `ui`, `models`, `auth`
- Component names: `button`, `modal`, `form`
- Feature names: `checkout`, `search`, `profile`

### Description (Required)

- Use imperative mood: "Add feature" not "Added feature"
- Don't capitalize first letter
- No period at the end
- Maximum 50 characters
- Describe what, not how

**Good:**
```
feat(api): add user preferences endpoint
fix(cart): handle empty cart checkout
docs: update installation steps
```

**Bad:**
```
Added user preferences endpoint.
Fixed the cart bug.
Updated docs.
```

### Body (Optional)

Use body for:
- Explaining why the change was made
- Describing complex changes
- Breaking changes

Format:
- Separate from subject with blank line
- Wrap at 72 characters
- Explain what and why, not how

### Footer (Optional)

Use footer for:
- Breaking changes
- Issue references
- Co-authors

```bash
feat(api)!: change user endpoint response format

BREAKING CHANGE: /api/users now returns firstName and lastName
instead of name. Clients must update accordingly.

Closes #123
```

## Breaking Changes

Indicate breaking changes with `!` after scope:

```bash
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: Removed /api/v1/* endpoints. Use /api/v2/* instead.
```

## Seven Rules of Great Commit Messages

1. **Separate subject from body with a blank line**
2. **Limit subject to 50 characters**
3. **Capitalize the subject line**
4. **Don't end with a period**
5. **Use imperative mood**
6. **Wrap body at 72 characters**
7. **Explain what and why, not how**

## Examples

### Simple Feature

```bash
feat(search): add fuzzy matching

Implement fuzzy search algorithm for better typo tolerance.
Users can now find products even with minor spelling errors.
```

### Bug Fix

```bash
fix(checkout): handle empty cart

Return early with appropriate message when cart is empty
instead of throwing null pointer exception.
```

### Breaking Change

```bash
feat(api)!: rename user endpoints

BREAKING CHANGE: All /user/* endpoints renamed to /users/*
- GET /user/:id → GET /users/:id
- POST /user → POST /users
- PUT /user/:id → PUT /users/:id

Migration: Update all API calls in client code.
```

### With Issue Reference

```bash
fix(auth): resolve token expiration

The JWT token was expiring after 1 hour due to incorrect
timestamp calculation. Fixed by using UTC timestamps.

Fixes #456
```

### Multiple Paragraphs

```bash
feat(dashboard): add export functionality

Add CSV and JSON export options to the dashboard.

The export includes:
- All visible columns
- Applied filters
- Date range selection

Users can access export via the new button in the toolbar.

Closes #123
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `Added feature` | Past tense | Use imperative: "Add feature" |
| `Add feature.` | Period at end | Remove period |
| `fix stuff` | Lowercase type | Capitalize: "Fix stuff" |
| `feat(FIX): add X` | Capitalized scope | Use lowercase: `feat(fix)` |
| `feat: add user endpoint with validation and error handling` | Too long | Keep under 50 chars, use body |
| Missing type | Non-standard | Always use type prefix |

## Automation Benefits

Conventional commits enable:

1. **Automatic changelog generation**
   - `feat` → Features section
   - `fix` → Bug fixes section
   - `BREAKING CHANGE` → Breaking changes

2. **Semantic versioning**
   - `feat` → Bump MINOR
   - `fix` → Bump PATCH
   - `BREAKING CHANGE` → Bump MAJOR

3. **Release notes**
   - Group commits by type
   - Filter for user-facing changes

4. **Git history analysis**
   - `git log --oneline --grep "^feat"`
   - `git log --oneline --grep "^fix"`