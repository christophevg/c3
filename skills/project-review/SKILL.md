---
name: project-review
description: |
  Shared implementation review cycle for project work: functional → domain →
  quality → documentation → completeness, with a hard make check gate.
  Invoked by project-manage (Phase 5.6, initial implementation) and
  project-handle-pr (Phase 6.4, PR-feedback re-validation, scoped). Never a
  user-facing entry point.
type: workflow
---

# Project Review

Shared sub-procedure invoked from `c3:project-manage` (5.6) and
`c3:project-handle-pr` (6.4). One place guarantees the same gate — including
`make check` — applies to initial implementation and PR-feedback changes
alike.

Design doctrine (RESTful, simplicity, wrapper check, owner-proposal
default) lives with the domain agents — api-architect for
architecture/design, and personas apply their own expertise in stages b/c.
This skill coordinates the cycle; it does not restate doctrine.

## Inputs

From the caller: project root, task id + acceptance criteria (TODO.md),
implementation plan (`reporting/{task}/plan.md` or the PR comment),
modified files, scope (backend | frontend | full | docs | research + security
flag), round counter (max 2).

## Workflow

Each stage writes `reporting/{task}/{agent}-review.md` (template in
[references/review-cycle.md](references/review-cycle.md)).

```
a. functional-analyst (BLOCKING) ── reject ──► back to implementer
b. domain reviews (by scope)     ── any reject ──► back to implementer
c. quality reviews: code-reviewer + testing-engineer ── any reject ──► ...
d. end-user-documenter (IF user-facing) ── reject ──► ...
e. completeness + make check (BLOCKING) ── fail ──► ...
f. pre-commit final verification ──► ALL PASS = "approved"
```

**Stage a — functional (blocking).** functional-analyst verifies all
acceptance criteria, edge cases, end-to-end flow, no regressions; confirms
the plan consulted relevant domain skills (`c3:python` for Python scopes;
docs scopes must have consulted both `c3:readme` and `c3:documentation`).
Must pass before all other stages.

**Stage b — domain reviews, by scope.**

| Scope | Agents |
|-------|--------|
| backend | api-architect (+ security-engineer if security-related) |
| frontend | ui-ux-designer |
| full | api-architect, ui-ux-designer (+ security-engineer) |

**Stage c — quality reviews.** `code-reviewer` (conventions, smells,
abstractions, maintainability) and `testing-engineer` (meaningful coverage,
edge cases, integration flows). The owner's proposal is the baseline:
reviewers quote it, verify it is satisfied, and reject unearned additions
("reviewer prefers X" is not a reason). New classes/wrappers/indirections
require earned justification — default answer: no.

**Stage d — documentation** (if user-facing): end-user-documenter verifies
README/docs/changelog sync.

**Stage e — completeness + `make check` (BLOCKING).** Run `make check`
(test + typecheck + lint + format); require green — never authorize a
commit while it fails. If the Makefile lacks `check`, run the equivalents
individually. Verify manually: docs complete, demo/CLI example works,
end-to-end works from the user's perspective.

**Stage f — final verification.** Confirm a–e passed; if a check is
unclear from sub-agent reports, ask the caller (who asks the owner):
check runs green? feature exercised? README updated? experienceable?

## Rejection handling

- Collect ALL rejection feedback across stages before returning (one fix
  pass, not one per stage).
- `rejected: <consolidated feedback>` → caller routes implementer.
- Max 2 rounds → `escalate` (owner decides: proceed / reduce scope /
  alternative).

## Scoped re-runs (PR iteration)

Called from `project-handle-pr`: stage a and stage e always run; stages
b/c/d re-run for the affected scope only; round counter shared with the
caller.

## Return value

`"approved"` · `"rejected: <feedback>"` · `"escalate"`

## Reference

- [references/review-cycle.md](references/review-cycle.md) — per-agent
  criteria, make check checklist, report template.