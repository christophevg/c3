# Issue Workflow

## Overview

GitHub Issues track work: features, bugs, tasks. This document is the
canonical status-label protocol: taxonomy, transition table, and the Yoker
`github` operations that execute them. Orchestrating skills decide WHEN a
transition happens; this document defines HOW.

Authority: all labeling, commenting, and closing run through
`c3:release-manager`. Only the repository owner's comments decide; a
transition is never self-initiated — it executes on an owner decision or an
owner-authorized workflow step (Triage Gate, Plan Approval Gate, merge).

## Tooling

```yaml
# granted per repo in yoker.toml [tools.github] allowed_operations
github(operation="issue_list",    state="open", limit=10)
github(operation="issue_view",    number=N)
github(operation="issue_edit",    number=N, add_label="status:backlog")
github(operation="issue_edit",    number=N, remove_label="status:backlog",
                                  add_label="status:in-progress")  # the swap
github(operation="issue_edit",    number=N, state="closed")
github(operation="issue_comment", number=N, body="…")
github(operation="label_create",  label="status:backlog", description="…")
```

Pre-flight: before a phase that depends on these operations, confirm they
are granted. A missing operation is reported once (durable work lands
first); the owner labels web-side meanwhile. Never shell out to `gh`.

## Ensure labels exist

The taxonomy assumes the five `status:*` labels exist in the repo. Before
the first transition in a repository, ensure them: one `label_create` per
label — the call is idempotent; existing labels are left untouched. Report
in one line which labels had to be created. Suggested colors:
`status:backlog` 1d76db, `status:in-progress` fbca04,
`status:needs-research` 5319e7, `status:blocked` d93f0b,
`status:wont-do` cccccc.

## Taxonomy

| Label | Meaning | Issue state |
|-------|---------|-------------|
| `status:backlog` | Reviewed, accepted, recorded in TODO.md | open |
| `status:in-progress` | Work started: fix, verify, or analyze | open |
| `status:needs-research` | Evaluation/research before anything else | open |
| `status:blocked` | Waiting on an external dependency | open |
| `status:wont-do` | Decision: won't implement | closed — label remains as tombstone |

## Swap invariant

**At most one `status:*` label per issue.** Every transition removes the
current status label and adds the new one in a single `issue_edit` call.
Never stack status labels. An issue carries no status label only before
triage and after completion (closed). Non-status labels (`enhancement`,
`bug`, …) are unaffected and coexist freely.

## Transition table — canonical

| Event | Label action |
|-------|--------------|
| Triage accepted (feature, bug, dependency) | add `status:backlog` |
| Route = evaluate first (owner-approved) | add `status:needs-research` |
| Research completes → owner evaluates the outcome | swap per outcome: `status:backlog` / `status:in-progress` / `status:blocked` / `status:wont-do` (+ close) |
| Work starts (branch + draft PR, bug-flow step 1, verify/analyze) | swap current → `status:in-progress` |
| Waiting on external dependency | swap current → `status:blocked` + comment naming the blocker |
| Unblock event evaluated | swap per outcome — anything from `status:backlog` to `status:wont-do` (+ close) |
| Verification: already satisfied / already fixed | remove status label → close as completed with a reason comment |
| Won't-do decision | swap → `status:wont-do` → close with reason (label remains) |
| PR merged (post-merge cleanup) | remove whatever `status:*` label is present → close if not auto-closed |

`status:blocked` carries no memory of the previous state: when the blocker
resolves, the outcome of evaluating that event determines the next state —
nothing is auto-restored.

## Closing semantics

- A close always carries its reason in a comment: wont-do (why not),
  already-satisfied (what satisfies it), merged (PR reference).
- `status:wont-do` is applied before closing and stays on the closed issue
  as a tombstone; other status labels are removed at/before close.
- `Fixes #N` in a PR auto-closes the issue at merge; label cleanup is the
  separate post-merge step (`c3:project-post-merge` 7.5).

## Recipes

### Triage acceptance → backlog

```
github(operation="issue_edit", number=N, add_label="status:backlog")
github(operation="issue_comment", number=N,
       body="Reviewed and accepted. Added to TODO.md with priority P<n>.")
```

### Work starts → in-progress (the swap)

```
github(operation="issue_edit", number=N,
       remove_label="status:backlog", add_label="status:in-progress")
```

When the current status label is uncertain, `issue_view` shows the labels;
the swap removes whichever `status:*` label is present.

### Needs research

```
github(operation="issue_edit", number=N, add_label="status:needs-research")
```

### Blocked

```
github(operation="issue_edit", number=N,
       remove_label="<current>", add_label="status:blocked")
github(operation="issue_comment", number=N, body="Blocked by: <blocker>.")
```

### Won't-do

```
github(operation="issue_edit", number=N,
       remove_label="<current>", add_label="status:wont-do")
github(operation="issue_comment", number=N,
       body="Closing: not in scope because …")
github(operation="issue_edit", number=N, state="closed")
```

### Verification: already satisfied

```
github(operation="issue_edit", number=N, remove_label="<current>")
github(operation="issue_comment", number=N,
       body="Already satisfied: <evidence>. Closing.")
github(operation="issue_edit", number=N, state="closed")
```

### Completed via merged PR

```
github(operation="issue_edit", number=N, remove_label="<status-label>")
# close only when the PR did not auto-close the issue:
github(operation="issue_edit", number=N, state="closed")
github(operation="issue_comment", number=N, body="Closed via PR #<n>.")
```

## Reviewing new issues

Only issues without a status label are new. Triage classifies and proposes;
it never starts work — the owner decides at the Triage Gate.

```
github(operation="issue_list", state="open", limit=10)
# unreviewed = no status:* label among the returned labels
github(operation="issue_view", number=N)
```

## Issue linking in PRs

| Keyword | Effect |
|---------|--------|
| `Closes #{n}` / `Fixes #{n}` / `Resolves #{n}` | auto-closes the issue at merge |
| `Related to #{n}` / `See #{n}` | links without closing |