---
name: project-handle-pr
description: Handle PR feedback iteration for a project task. Fetches owner comments, delegates interpretation to functional-analyst and implementation to python-developer, then re-qualifies the change through the c3:project-review cycle (scoped) before push. Use when the user says "follow up on PR #N", "check PR #N", or project-manage routes here from an open PR with feedback.
---

# Project Handle PR

Sub-skill of `c3:project-manage`. Covers **Phase 6 — PR iteration**: processing
owner feedback on an open PR and re-validating the resulting changes before they
ship to the branch.

## Why this is a separate skill

PR-comment iteration is independently invokable ("follow up on PR #N") and has a
distinct shape from initial implementation. Critically, it **re-enters the review
cycle** before push — a change requested in a PR comment is treated as work that
must be re-qualified against the task, not just executed and pushed. This closes
the gap where the original workflow shipped developer changes straight to the
branch with no cross-validation.

## Inputs

The caller (`project-manage`) provides:

- **Project root** (from release-manager's state report)
- **PR number** and PR URL
- **Task context** — task id, acceptance criteria from TODO.md
- **Scope** — backend | frontend | full | docs | research (+ security flag)
- **Round counter** — rejection rounds already spent (carried across calls)

## ⛔ Rules

- **No Bash / git / gh directly.** Delegate all source-control and GitHub
  operations to `c3:release-manager`. This skill is a coordinator.
- **Owner is the only approver.** Non-owner comments are informational only;
  the functional-analyst must verify comment author ownership before treating
  feedback as authoritative.
- **Do not merge.** The owner merges. This skill never proposes merging.
- **Do not poll.** After posting, pause. The user re-invokes "follow up on PR #N"
  to check for new responses.

## ⚠️ Simplicity Principle — Owner's Proposal is the Default

**Slim, tight, concise is the default.** PR feedback from the owner often includes an explicit snippet, design, OR a stated worry / constraint / directive. That proposal or instruction is the default — the functional-analyst's interpretation (6.3 Step 1) MUST quote each owner-stated proposal, worry, and constraint, state whether the change satisfies it, and only propose a deviation with a specific, documented problem. "Refinement" or "reviewer prefers X" is NOT justification. Added classes/indirections/wrappers/guards not in the owner's proposal require earned justification. Ignoring the owner's snippet or stated worry without a stated reason is unacceptable.

## Workflow

```
6.1  release-manager: fetch new PR comments
6.2  no new feedback → report & wait (PAUSE)
6.3  per feedback item:
       functional-analyst interprets the comment against task criteria
       python-developer implements the change (incremental)
6.4  ★ invoke c3:project-review skill (scoped re-run)   ← THE FIX
6.5  release-manager: commit → push → comment on PR
6.6  owner approves → wait for merge → delegate to c3:project-post-merge
       more changes  → loop to 6.1
       rejected      → close PR (per owner instruction)
```

### 6.1 Fetch PR comments

Delegate to release-manager:

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Check ALL feedback channels for PR #{number}:\n1. Conversation comments: gh pr view {number} --comments\n2. Formal reviews: gh api repos/{owner}/{repo}/pulls/{number}/reviews\n3. Inline review comments: gh api repos/{owner}/{repo}/pulls/{number}/comments\n\nReport ALL feedback from the owner, including: review state (approved/commented/changes_requested), inline comment text with file and line numbers, and conversation comments. Verify each comment author is the repository owner.",
  description: "Check PR feedback (all channels)"
})
```

**GitHub PRs have three distinct feedback channels — check ALL of them:**

| Channel | What | Command |
|---------|------|---------|
| Conversation comments | General PR thread | `gh pr view {n} --comments` |
| Formal reviews | Approve/request changes/comment states | `gh api repos/{owner}/{repo}/pulls/{n}/reviews` |
| Inline review comments | Line-specific code feedback | `gh api repos/{owner}/{repo}/pulls/{n}/comments` |

A "commented" review with inline comments is easily missed by `gh pr view --comments` alone — it only shows conversation-level comments, not formal reviews or inline code feedback.

### 6.2 No new feedback

If release-manager reports no new owner comments:

- Report: `"No new feedback on PR #{number}. Waiting for owner review."`
- **Pause.** Do not poll. The user re-invokes "follow up on PR #N" later.

### 6.3 Interpret & implement each feedback item

**Owner authority check:** before acting, the functional-analyst verifies the
comment author is the repository owner. Non-owner comments are acknowledged as
informational and surfaced to the owner, but do not drive implementation.

For each owner feedback item:

**Step 1 — Functional-analyst interprets** the comment against the task's
acceptance criteria and produces a concrete change description:

```
Agent({
  subagent_type: "c3:functional-analyst",
  prompt: """
  Interpret owner feedback on PR #{number} for task {task-id}.

  Acceptance criteria: {criteria}
  Owner comment: {comment}

  Produce a concrete change description: what must change, in which files,
  and how the result still satisfies the acceptance criteria. Flag anything
  that would conflict with the task's agreed scope.
  """,
  description: "Interpret PR feedback"
})
```

Use `SendMessage` to continue with the same functional-analyst across related
items — preserve context, do not relaunch.

**Step 2 — python-developer implements** the change incrementally (one change →
test → verify; restore if broken; ask before guessing at root cause):

```
Agent({
  subagent_type: "c3:python-developer",
  prompt: """
  Implement the following change on the current feature branch.

  Change: {change_description from functional-analyst}
  Task: {task-id} — {criteria}
  Files: {files to modify}

  Follow project and global agent instructions and relevant domain skills.
  Make one change at a time and verify each. Run make check before reporting done.
  """,
  description: "Implement PR feedback change"
})
```

### 6.4 Re-qualify through the review cycle (THE FIX)

⚠️ **MANDATORY. Do not skip. Do not push without this.**

Invoke the `c3:project-review` skill in **scoped** mode. This re-validates the
developer's change against the task before it reaches the branch:

- Stage a (functional-analyst) always runs — confirms the change still satisfies
  the acceptance criteria.
- Stage e (`make check`) always runs — the gate re-applies to this round.
- Stages b/c/d re-run for the affected scope only.

```
Skill({
  skill: "c3:project-review",
  args: "scoped re-run for PR #{number}, task {task-id}, scope {scope}, round {n}, files: {files}"
})
```

**Handle the return value:**

| project-review returns | Action |
|------------------------|--------|
| `approved` | Proceed to 6.5 |
| `rejected: <feedback>` | Send developer back to 6.3 Step 2 with the consolidated feedback; increment round counter; re-run 6.4 |
| `escalate` (2 rounds exhausted) | Report to owner: proceed with known issues / reduce scope / alternative approach? Pause for owner decision. |

### 6.5 Commit, push, comment

Delegate to release-manager:

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Commit the changes with message: 'fix: address PR #{number} feedback — {summary}'. Push to the feature branch.",
  description: "Commit and push feedback fix"
})
```

Then post a comment explaining what was changed and how it maps to the owner's
feedback:

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Comment on PR #{number}: summarize the changes made in response to the owner feedback, mapped point-by-point. Note that the change passed the review cycle (functional + make check).",
  description: "Post feedback response comment"
})
```

### 6.6 Next action

| Owner signal | Action |
|--------------|--------|
| Approves (e.g. "approved", "looks good", "merge it") | Wait for the owner to merge. Do not merge. When the user later reports the PR is merged, delegate to `c3:project-post-merge`. |
| Requests more changes | Loop to 6.1. |
| Rejects entirely | Per owner instruction, delegate to release-manager to close the PR (and the related issue if applicable). Report to owner. |

After posting, **pause**. Do not poll for further feedback. The user re-invokes
"follow up on PR #N" to continue.

## Multiple PRs

If the caller is processing several PRs, after this PR is paused, return control
to the caller with a status summary so it can move to the next PR. Do not check
this PR's feedback again until the user says "follow up on PR #N".

## Reference

- [../project-review/SKILL.md](../project-review/SKILL.md) — the shared review
  cycle invoked at 6.4.
- [../project-manage/references/issue-review-workflow.md](../project-manage/references/issue-review-workflow.md)
  — owner-authority governance (applies to PR comments too).
