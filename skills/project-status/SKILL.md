---
name: project-status
description: |
  Project health snapshot: read TODO.md, analysis/ and reporting/, compute
  task metrics, and produce a STATUS.md report with executive summary,
  RAG status, risks and next steps. Use only on explicit request —
  "/project status", "show project status".
type: workflow
---

# Project Status

Produce a status report (`STATUS.md` in the project root) from project
artifacts. Read-only with respect to sources; only `STATUS.md` is written.

## Procedure

1. **Read sources** — TODO.md (tasks, priorities, statuses), existing
   STATUS.md (for trends), `analysis/` (planned dependencies, risks),
   `reporting/*/summary.md` (completed-task detail and dates).
2. **Compute metrics** — totals per priority (P1–P4) and per status
   (not started / in progress / blocked / done), completion rate,
   open blockers.
3. **Identify** — dependencies, blockers (stopping work), impediments
   (slowing work), risks, decisions required, overdue/over-budget tasks.
4. **Determine RAG status** —

   | Status | Condition |
   |--------|-----------|
   | 🟢 GREEN | on track, no blockers |
   | 🟡 YELLOW | risks or mitigated blockers exist |
   | 🔴 RED | critical blocker, commitments will be missed |

   If uncertain, choose YELLOW — early warning beats hiding risk.
5. **Write STATUS.md** and display the executive summary.

Trends (↑ improving / → stable / ↓ deteriorating) come from diffing the
previous STATUS.md.

## STATUS.md Structure

```markdown
# Project Status

**Generated:** YYYY-MM-DD HH:MM
**Status:** 🟢 GREEN | 🟡 YELLOW | 🔴 RED

## Executive Summary
[2–3 sentences: verdict, biggest development, immediate concern]

## Status Indicator
| Metric | Value | Trend |
|--------|-------|-------|
| Overall Status | 🟢/🟡/🔴 | ↑/→/↓ |
| Completion Rate | X% | |
| Tasks Remaining | N | |
| Blockers Active | N | |

## Task Summary
### By Priority (P1–P4: total / done / remaining) — per canonical format
### By Status (not started / in progress / blocked / done)

## Dependencies | Blockers | Risks | Decisions Required
[table rows: item, owner, status, requested action/impact, due]

## Recent Activity
[completed + in-progress tasks with dates]

## Next Steps
[immediate actions, each with an owner]
```

Adapt sections to what the project actually has: an empty table is noise —
omit sections with nothing to report. Reporting is built from artifacts,
never invented: every number traces to TODO.md, analysis/ or reporting/.

In direct mode, stay local (read files, write STATUS.md, done). Only in
managed mode add the GitHub dimension (open PRs/issues via c3:release-manager).

## Executive Summary

Two to three sentences: verdict first ("Project is 🟡 YELLOW"), then the
biggest development, then the immediate concern with a concrete ask.

## Practices

- Honest early warnings over comfortable GREENs.
- Goal progress, not activity lists.
- Every blocker, risk and decision carries an owner and a requested action.
- Track trends against the previous report; keep estimates calibrated from
  observed variance.

## Detection heuristics

- **Dependencies:** tasks noted as "depends on"/"blocked by"; external
  owners/teams; decision-gated tasks (from TODO.md) · external services or
  review/approval chains named in analysis/.
- **Blockers:** critical = work fully stopped (blocked tasks, overdue
  dependencies, failing tests, missing access); impediments = slowing
  (incomplete info, partial dependencies, tech debt).
- **Risks:** technical (unknown complexity, integration), resource
  (availability, skills), schedule (deadlines, competing priorities),
  external (vendors, regulation). Score probability × impact; high-high
  first.
- **Time-consuming tasks:** only where TODO/reporting record estimates —
  never fabricate variance.

## Related

- `project-manage` — consumes STATUS.md context for task selection
- `project-todo-refine` — follow-up on identified issues
- c3:release-manager — PR/issue state in managed mode