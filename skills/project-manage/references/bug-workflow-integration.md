# Bug Workflow Integration

This document explains how the bug-fixing workflow integrates with project management.

## When Bugs Are Detected

When the project-manage skill detects a bug (via task type detection), it delegates to the bug-fixing skill for the specialized workflow.

## Integration Points

### Task Type Detection

| Indicator | Examples |
|-----------|----------|
| "fix", "bug", "issue" | "fix the login bug", "there's an issue with auth" |
| "broken", "error" | "the button is broken", "getting an error" |
| "doesn't work", "crash", "fails" | "login doesn't work", "app crashes on startup" |

### Bug-Fixing Skill Invocation

The project-manage skill invokes the bug-fixing skill which handles:

1. **Bug Intake** — Parse description, detect project context
2. **Bug Analysis** — Functional-analyst validates and scopes
3. **Root Cause** — Systematic debugging investigation
4. **Test Creation** — TDD approach (failing test first)
5. **Fix Implementation** — Minimal fix with test update
6. **Review Cycle** — Functional → Domain → Quality reviews
7. **Documentation** — Bug analysis report, commit message

### Review Cycle for Bugs

The review cycle mirrors the feature workflow but is scoped to the bug:

```
Functional Analyst Review (BLOCKING)
        ↓
Domain Reviews (if applicable)
    ├── ui-ux-designer (if UI changes)
    └── security-engineer (if security-related)
        ↓
Quality Reviews (PARALLEL)
    ├── code-reviewer
    └── testing-engineer
        ↓
Documentation (if user-facing)
```

## Handoff from Bug-Fixing to Project-Manage

After the bug-fixing skill completes:

1. **Task completion** — Bug marked complete in TODO.md
2. **Summary report** — Created in `reporting/{bug-id}/summary.md`
3. **Return to project-manage** — Continue with next task from backlog

## Key Differences from Feature Workflow

| Aspect | Feature | Bug |
|--------|---------|-----|
| Starting point | TODO.md backlog | Bug description |
| Analysis | Full domain review | Bug-specific analysis |
| Test creation | After implementation | Before implementation (TDD) |
| Scope | Often larger | Typically smaller, focused |

## See Also

- [bug-fixing skill](../../bug-fixing/SKILL.md) — Complete bug-fixing workflow
- [review-cycle.md](review-cycle.md) — Detailed review execution