# Issue Review Workflow

Detail protocol for Phase 0.3 of the managed workflow: how GitHub issues
are triaged into the backlog. Owner authority, status labels, and bug
routing are defined in the main playbook — this document covers the feature
interview and triage-completion sequence.

## Feature Issue Review

Features require review and clarification before entering the backlog.
The functional-analyst conducts it; all comments go through
c3:release-manager.

### Step 1 — Mark and Review

Release-manager adds `status:in-progress` and comments "Reviewing this
feature request". The functional-analyst assesses definition quality:

| Quality | Indicators | Action |
|---------|-----------|--------|
| Well-defined | clear problem, criteria, scope | skip to Triage Completion |
| Needs clarification | missing criteria, ambiguous scope | Clarification |
| Insufficient | no problem statement, no context | ask for a rewrite |

### Step 2 — Clarification

Post clarifying questions as an issue comment. Think through implications,
failure modes, edge cases, and alternative approaches before posting; ask
the resulting questions.

Cover: the problem and who experiences it; testable acceptance criteria;
scope boundaries and dependencies; alternatives considered.

### Step 3 — Triage Completion

Triage is complete only when all four steps are done:

1. **No more clarifying questions.** Analyst confirms understanding of
   problem, scope, edge cases.
2. **Owner confirms nothing to add.** Analyst asks "anything else you'd
   like to add or clarify?"; more info returns to step 1.
3. **Owner explicitly accepts with priority.** Owner confirms acceptance
   (e.g. "accepted, please proceed") and states priority P1–P4; if absent,
   analyst asks.
4. **Analyst reports and records.** Report "Issue #N fully triaged,
   accepted with priority X" + summary (problem, criteria, priority);
   update TODO.md with task, acceptance criteria, issue link, priority.

### Don'ts

| Don't | Why |
|-------|-----|
| Skip "anything else?" | owner may hold more context |
| Assume acceptance or priority | owner states both explicitly |
| Proceed before all steps | incomplete triage → unclear requirements |
| Treat non-owner comments as decisions | informational only |

## Integration

- functional-analyst — reviews, clarifies, records in TODO.md
- release-manager — labels, comments, git operations
- bug-fixer — bugs bypass review entirely (immediate fix flow)