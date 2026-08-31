---
name: bug-fixing
description: Systematic bug fixing with TDD approach. Use when fixing bugs, debugging issues, or investigating problems. Accepts bug descriptions in any format, coordinates analyst/reviewer agents, creates tests before fixes, produces analysis reports.
type: workflow
---

# Bug Fixing

Systematic, test-driven bug fixing with agent coordination. This skill
diagnoses and fixes; the caller owns the review cycle and PR.

## Triggering

- "fix bug", "there's a bug", "debug this" — any bug phrasing
- an issue reference with fix context ("fix issue #123")
- a bug report path or a description of unexpected behavior

Bug descriptions land in any format: free text, `#123`/ticket reference,
structured report file. The authorized description IS the approval to
proceed through the workflow.

## Workflow

### Phase 1 — Intake

Parse the description into: symptoms, expected vs actual behavior,
environment, reproduction steps. Detect project context (language,
framework, test runner, conventions) from `pyproject.toml` / config files.
Assign a bug ID `{bug-id}`.

### Phase 2 — Analysis

Engage `c3:functional-analyst` to review validity and scope: confirm the
bug exists (or reject with reason), flag UI impact if present.

Create the analysis report at `docs/bug-analysis/{bug-id}.md` (template in
`patterns/bug-analysis-template.md`) and, if the bug came from an issue,
report the analysis to the caller for posting.

Outcomes: confirmed → proceed (note UI review if UI-touched); rejected →
document the reason and stop.

### Phase 3 — Root cause

Isolate (reproduce consistently, find boundaries) → gather info (log,
compare working vs broken) → hypothesize (one variable at a time) →
validate. RCA techniques in `patterns/rca-techniques.md` (5 Whys for linear
problems; fishbone for multi-factor).

### Phase 4 — Failing test first (TDD)

Create the test that demonstrates the bug BEFORE the fix exists:

| Bug type | Test type |
|----------|-----------|
| Logic/validation | unit |
| Integration/API | integration |
| User flow | E2E |

Run it to confirm it reproduces the bug (fails now, passes after the fix).
Platform-specific patterns: `patterns/test-creation-patterns.md`.

### Phase 5 — Fix, then exact-gate verification

1. Implement the minimal fix.
2. Update the test to expect the correct behavior.
3. Run the full suite (fix + no regressions).
4. Run `make check` — must pass before reporting done. **Verify against
   the exact gate that failed**: if the bug surfaced in a specific gate
   (CI's multi-version matrix, one interpreter, a platform-specific test),
   re-run *that* gate — an equivalent-but-narrower check does not verify
   (a 3.10-only failure is invisible to a local single-version run; A1).
   Per-version runs use the project's own make targets; the agent never
   invents new ones. If the exact gate is not runnable locally, report that
   gap explicitly rather than claiming verified.

No commit, branch, or PR here. This skill diagnoses and fixes; the caller
runs review (Phase 7).

### Phase 6 — Documentation

Update the analysis report with the fix summary; confirm the regression
test is in the codebase; prepare a commit message for the caller
(`fix: {summary} (#{number})`). Do not close the issue — closure is
`c3:project-post-merge`'s job after the owner merges.

### Phase 7 — Report back

This skill stops here; it never opens the PR. Report format:

```
## Bug Fix Ready for Review

Issue #{n} · Bug ID · one-line summary · root cause
Test: {file}:{test} — make check ✅ (or: exact-gate gap reported)
Files modified · Scope (backend | frontend | full, + security?)
Analysis report path · proposed commit message
```

Scope from what the bug touched: backend | frontend | full (+ security
when auth, PII, input handling, external APIs, files, config are touched).

The caller then runs `c3:project-review` (scoped), and on approval creates
the PR. Rejection feedback (max 2 rounds) returns here for revision;
`make check` failures: 3 attempts, then ask the owner.

# Deliverables

- Failing test → fix → green suite; updated analysis report; the Phase-7
  report for the caller.

# Related

- `c3:project-review` — the review cycle the caller runs on the fix
- `c3:commit` — commit conventions for the prepared message
- `c3:project-manage` — managed-mode caller
- Agents (engaged for review, not by this skill): `c3:functional-analyst`,
  `ui-ux-designer` (UI changes), `security-engineer` (security-adjacent),
  `code-reviewer`, `testing-engineer`, `end-user-documenter` (user-facing)

## Never

- Do not run review, create PRs, or commit — the caller owns those steps.
- Do not close issues; closure belongs to post-merge.
- Security vulnerabilities, production incidents, prioritization, and
  upstream library fixes are out of scope — route them accordingly.