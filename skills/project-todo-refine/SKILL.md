---
name: project-todo-refine
description: |
  Iteratively refine TODO.md entries with the owner: review scope, priority,
  and dependencies topic by topic, on explicit request only (e.g. "refine
  todo", "review backlog"). Not for feature intake (project-feature), full
  workflow (project-manage), or status overview (project-status).
type: workflow
---

# Project TODO Refine

Iterative backlog refinement with owner feedback: update scope, priority,
and dependencies of TODO.md entries — not a full functional analysis.

## Workflow

### Phase 1 — Overview

Read TODO.md (current working folder) and present the overview:

- total topics, per-priority counts, per-section state
- topics needing attention, with the reason each:
  vague or incomplete descriptions · stale entries (no progress for 2+
  weeks) · unresolved blockers · topics flagged in previous refinements

### Phase 2 — Per-topic loop (repeat until done)

For each topic needing attention:

1. **Introduce** — current text, priority, dependencies, related context
   (analysis docs, recent commits touching the area).
2. **Recommend** — a concrete action with rationale: clarify scope / adjust
   priority / split / merge / add dependency / drop.
3. **Ask** — present recommendation and options to the owner in one go;
   the owner decides (direct mode: chat; managed mode: issue comments).
4. **Revise** — apply the decision to TODO.md: clarify the description,
   keep scope atomic (split broad topics, merge overlapping ones), update
   priority and dependencies.

Move to the next topic without re-litigating decided ones.

### Phase 3 — Summary

Report: topics reviewed / updated / completed / split, key changes, and
recommended next steps.

## GitHub sync (managed mode only)

When refined entries reference GitHub issues, delegate to
c3:release-manager — never invoke gh-style tools directly — to post one
summary comment per affected issue (scope, priority + reasoning, key
decisions, pointer to TODO.md). Skip when the change is cosmetic.

Priority order when several artifacts need updating — top-down, each one
place: TODO.md first (tasks + priorities), then analysis/ (patterns,
decisions), then issue sync (one summary comment per affected issue: scope,
priority + reasoning, key decisions, pointer to TODO.md). User/API docs
only when the refinement changed documented behavior. Commit via
release-manager in managed mode; local only in direct mode.

## TODO.md format

Use the canonical structure (see c3:project-manage Conventions):
`## Unsorted` → `## Backlog` (P1–P4). No `## Done` section — completed
tasks are removed (git history keeps the record). Entries are concise,
action-oriented, and cross-reference issues and acceptance criteria.

## Related

- `project-feature` — intake of new features (this skill refines, that one captures)
- `project-status` — state overview
- `project-manage` — consumes the refined backlog
- functional-analyst — deep analysis when a topic outgrows refinement