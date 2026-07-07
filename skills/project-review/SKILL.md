---
name: project-review
description: Shared implementation review cycle for project work. Runs functional → domain → quality → documentation → completeness reviews with a hard `make check` gate. Invoked by project-manage (Phase 5.6, initial implementation) and project-handle-pr (Phase 6.4, PR-feedback re-validation). Use when implementation or a PR-feedback change needs to be qualified before commit/push.
---

# Project Review

This is a **shared sub-procedure**, not a user-facing entry point. It is invoked from:

- `c3:project-manage` — Phase 5.6, after the python-developer implements a task
- `c3:project-handle-pr` — Phase 6.4, after the python-developer implements a PR-feedback change

**Why it exists as a skill:** the review cycle runs in two contexts. Keeping it in one place guarantees the same gate (including `make check`) applies to both initial implementation and PR-comment-driven changes — the latter previously bypassed review entirely.

## Inputs

The caller must provide:

- **Project root** (from release-manager's state report)
- **Task context** — task id, acceptance criteria from TODO.md
- **Implementation plan** — `reporting/{task-name}/plan.md` (initial) or the PR comment being addressed (iteration)
- **Files modified** by the developer
- **Scope** — backend | frontend | full | docs | research (+ security flag)
- **Round counter** — how many rejection rounds have already run (max 2)

## Workflow

The review runs in strict sequence. Each stage writes a report to
`reporting/{task-name}/{agent}-review.md` using the template in
[references/review-cycle.md](references/review-cycle.md).

```
a. functional-analyst        (BLOCKING) ── reject ──► back to implementer
        │ approve
        ▼
b. domain reviews (PARALLEL, by scope)
        ├── api-architect       (backend / full)
        ├── ui-ux-designer      (frontend / full)
        └── security-engineer   (if security-related)
        │ any reject ──► back to implementer
        ▼
c. quality reviews (PARALLEL)
        ├── code-reviewer
        └── testing-engineer
        │ any reject ──► back to implementer
        ▼
d. end-user-documenter       (IF user-facing)
        │ reject ──► back to implementer
        ▼
e. functional completeness + make check   (BLOCKING)
        │ fail ──► back to implementer
        ▼
f. pre-commit final verification
        ▼
   ALL PASS ──► return "approved" to caller
```

### Stage a — Functional Review (BLOCKING)

Invoke `functional-analyst`:

- All acceptance criteria from TODO.md are met
- Edge cases handled
- User flow works end-to-end
- No regressions

**Must pass before any domain/quality review.** On reject, return consolidated feedback to the caller — the caller sends the developer back to implementation.

### Stage b — Domain Reviews (parallel)

Invoke the agents that match the task scope (the same set the caller invoked in Phase 2/3):

| Scope | Agents |
|-------|--------|
| Backend only | `api-architect`, `security-engineer` (if security-related) |
| Frontend only | `ui-ux-designer` |
| Full stack | `api-architect`, `ui-ux-designer`, `security-engineer` (if security-related) |

Per-agent criteria are in [references/review-cycle.md](references/review-cycle.md).

### Stage c — Quality Reviews (parallel)

Always invoke both:

- `code-reviewer` — conventions, smells, abstractions, maintainability
- `testing-engineer` — coverage, meaningful tests, edge cases, integration flows

### Stage d — Documentation (if user-facing)

Invoke `end-user-documenter`: README, API docs, inline docs, changelog updated and synced with implementation.

### Stage e — Functional Completeness + `make check` (BLOCKING)

Every commit must be a functional whole: implementation + docs + UI/demo + end-to-end experience.

**Hard gate — run `make check` and require it to pass.** `make check` runs the full quality suite (test + typecheck + lint + format). No commit is authorized while `make check` fails. If the project's Makefile does not provide `make check`, run `make test`, `make typecheck`, `make lint`, and `make format` (or `make check`'s documented equivalents) individually and require all to pass.

Also verify manually:

- Documentation complete (README, API docs, inline)
- UI/demo available (console / CLI `--help` / web test page / library example)
- End-to-end experience works from the user perspective

On any failure, return to the caller with specific feedback.

### Stage f — Pre-Commit Final Verification

Confirm stages a–e all passed. If any verification status is unclear from the sub-agent reports, ask the caller (who can ask the owner) to confirm:

1. Tests / checks: pass? (from `make check`)
2. Standard run: did the feature work when exercised?
3. README: does it need updates for this change?
4. UI/demo: is there a way to experience this change?

Only return `"approved"` when every check passes.

## Rejection Handling

- Collect **all** rejection feedback from all stages (do not stop at the first reject — gather the full picture so the developer can fix everything in one pass).
- Consolidate into actionable items.
- Return to the caller, which routes the developer back to implementation with the consolidated feedback.
- **Maximum 2 rejection rounds.** After 2 failed rounds, return `"escalate"` to the caller — the caller asks the owner how to proceed (proceed with known issues / reduce scope / alternative approach).

## Scoped Re-runs (PR iteration, Phase 6.4)

When invoked from `project-handle-pr`, the cycle is **scoped** to the change:

- Stage a (functional-analyst) always runs — confirms the change still satisfies the task's acceptance criteria. This is the core fix: PR-comment changes are re-validated against the task, not just executed.
- Stage e (`make check`) always runs — the gate re-applies to every feedback round.
- Stages b/c/d re-run for the **affected scope only** (e.g., a backend-only tweak does not re-invoke `ui-ux-designer`).
- The round counter is shared with the caller — escalation after 2 rounds.

## Return Value

Report back to the caller with one of:

- `"approved"` — all stages passed, ready to commit/push
- `"rejected: <consolidated feedback>"` — return to implementer (caller increments round counter)
- `"escalate"` — 2 rounds exhausted, caller involves the owner

## Reference

- [references/review-cycle.md](references/review-cycle.md) — per-agent review criteria, the `make check` verification checklist, and the review report template.
