---
name: project-feature
description: |
  Feature intake: capture a new feature idea and either store it unsorted or
  scope it with the functional-analyst (and register an MBI in PLAN.md when
  it delivers user-facing value). Triggered by explicit request, e.g.
  "/project feature …" or "add feature X". Implementation always happens
  through project-manage, never here.
type: workflow
---

# Project Feature

Intake for feature ideas — from one-line captures to fully scoped backlog
entries. Intake only: this skill adds to TODO.md/PLAN.md; it never
implements (that is `c3:project-manage`).

## Workflow

```
feature description
  → MBI? (user-facing value, releasable, complete)
      yes → c3:plan MBI workflow (PLAN.md)
      no  → linear task path
  → description detailed enough?
      minimal → offer: scope now (functional-analyst) / capture unsorted
      detailed → scope via functional-analyst
  → add to TODO.md (canonical structure)
```

### 1 — MBI or linear task?

Ask the owner once: "Is this feature an MBI (delivers user-facing value) or
a linear task (internal improvement)?" Offer "unsure — help me decide"
(explain: MBI = end-user value, complete functionality, independently
releasable; internal refactoring and tech-debt cleanup are linear tasks).

**MBI path:** delegate to `c3:plan` for creation, structure, and WSJF
scoring — this skill does not duplicate the MBI workflow. On return: if the
MBI is Active, tag its tasks `[MBI-xxx]` in TODO.md and place them on top.

**Linear path:** continue below.

### 2 — Completeness check

| Description | Action |
|---|---|
| Minimal (a sentence, no criteria) | ask: scope now with functional-analyst, or capture unsorted? |
| Detailed (requirements / acceptance criteria / context) | scope via functional-analyst directly |

Owner declines scoping → capture verbatim in TODO.md `## Unsorted` and
confirm; refinement happens later (project-manage Phase 2.1 or
project-todo-refine).

### 3 — Scoping (functional-analyst, ephemeral engagement)

Interview the owner on the feature; deliver: specification, acceptance
criteria, priority recommendation, dependencies. Record the result in TODO.md
under the recommended priority — description, acceptance criteria, dependencies,
issue reference if managed-mode intake.

## TODO.md

Canonical structure only (c3:project-manage Conventions): `## Unsorted` →
`## Backlog` (P1–P4). No `## Done` — completed tasks are removed. "Unsorted
Features" is a legacy name — write `## Unsorted`.

## Related

- `project-manage` — Phase 2 picks the feature up for implementation
- `plan` / `wsjf` — when the feature is MBI-shaped
- functional-analyst — scoping interviews; owns TODO.md structure