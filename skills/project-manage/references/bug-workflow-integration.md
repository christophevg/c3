# Bug Workflow Integration

This document explains how the bug-fixing workflow integrates with project management.

## Issue Processing Overview

Issues are processed differently based on type:

| Issue Type | Workflow | Reference |
|------------|----------|------------|
| **Bug** | Bug Implementation Flow (bug-fixer → project-review → PR) | This document |
| **Feature** | Review → Clarify → Agree → Backlog | [issue-review-workflow.md](issue-review-workflow.md) |
| **Question** | Research or close | - |
| **Dependency** | Research → Backlog | - |

## When Bugs Are Detected

When project-manage detects a bug (via task type detection or Phase 0.3 issue
triage), it runs the **Bug Implementation Flow**: the bug-fixer diagnoses and
fixes, then project-manage runs the shared review cycle and creates the PR via
release-manager — the same funnel as features, minus the Plan Approval Gate.

## Integration Points

### Task Type Detection

| Indicator | Examples |
|-----------|----------|
| "fix", "bug", "issue" | "fix the login bug", "there's an issue with auth" |
| "broken", "error" | "the button is broken", "getting an error" |
| "doesn't work", "crash", "fails" | "login doesn't work", "app crashes on startup" |

### Bug-Fixing Skill Invocation

project-manage invokes `c3:bug-fixer` (which runs the `c3:bug-fixing` skill) to
do ONLY the diagnostic + fix work:

1. **Bug Intake** — Parse description, detect project context
2. **Bug Analysis** — Functional-analyst validates and scopes
3. **Root Cause** — Systematic debugging investigation
4. **Test Creation** — TDD approach (failing test first)
5. **Fix Implementation** — Minimal fix; run `make check` until passing
6. **Documentation** — Update bug analysis report, prepare commit message
7. **Report Back** — Return fix summary + scope to project-manage (no PR, no review)

The bug-fixer does NOT create a PR, run review, or close the issue. It reports
back; project-manage continues the flow.

### Review Cycle for Bugs

The review cycle is **not** duplicated here. After the bug-fixer reports back,
project-manage invokes the shared [project-review](../../project-review/SKILL.md)
skill, scoped to the bug:

- Stage a (functional-analyst) confirms the fix satisfies the bug's acceptance
  criteria (reproduction eliminated, no regressions).
- Stage e (`make check`) re-applies as the gate.
- Stages b/c/d run for the affected scope only (e.g., UI bug → ui-ux-designer;
  security bug → security-engineer; user-facing → end-user-documenter).

Rejection handling (max 2 rounds → escalate to owner) is identical to the
feature path. See [project-review/references/review-cycle.md](../../project-review/references/review-cycle.md)
for the per-agent criteria.

## Handoff from Bug-Fixing to Project-Manage

After the bug-fixer reports back, project-manage:

1. **Review** — Invokes `c3:project-review` (scoped to the bug).
2. **PR** — On approval, release-manager commits, pushes, creates the PR, follows CI.
3. **Ready** — release-manager marks the PR ready and requests owner review.
4. **Pause** — Wait for the owner. On "PR merged" → `c3:project-post-merge`
   (switches to main, marks the bug task done, closes the issue).

If `c3:project-review` rejects, project-manage re-spawns the bug-fixer with the
consolidated feedback (max 2 rounds).

## Key Differences from Feature Workflow

| Aspect | Feature | Bug |
|--------|---------|-----|
| Starting point | TODO.md backlog / Active MBI | Bug description / issue |
| Plan Approval Gate | Yes (BLOCKING, before implementation) | No (bugs are urgent, owner-decided) |
| Test creation | After implementation | Before implementation (TDD) |
| Review cycle | `c3:project-review` (full) | `c3:project-review` (scoped to the bug) |
| PR + CI | release-manager | release-manager (same funnel) |
| Post-merge | `c3:project-post-merge` | `c3:project-post-merge` (same) |

## See Also

- [bug-fixing skill](../../bug-fixing/SKILL.md) — Diagnostic + TDD + fix workflow (reports back, no PR)
- [project-review skill](../../project-review/SKILL.md) — Shared review cycle (functional → domain → quality → docs → `make check`)