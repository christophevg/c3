---
name: project-post-merge
description: |
  Post-merge cleanup after the owner merges a feature-branch PR. Sequenced
  to prevent TODO.md loss: switch to the default branch and pull BEFORE any
  TODO.md edit, mark the task done, commit, clean up issue labels, then ask
  the owner: release or next task? Triggered by an owner merge report or
  routed from project-manage.
type: workflow
---

# Post-Merge Cleanup

Sub-skill of `c3:project-manage` (Phase 7), independently invokable when the
owner reports "PR #N was merged". The owner merges; this skill runs only
afterwards and never merges anything itself.

## ⛔ Sequencing Rule (loss-critical)

After a merge the session is typically still on the feature branch. TODO.md
edits made before switching branches are lost when the branch is deleted.
Therefore: **default-branch switch + pull happen BEFORE any TODO.md edit** —
no reordering, no exceptions.

## Inputs

From the caller: PR number, task id (TODO.md), issue number (if any),
project root (from the release-manager state report).

## Workflow

```
7.1  find the issue number (TODO.md entry, or release-manager from the PR)
7.2  release-manager: switch to default branch + pull    ← FIRST
7.3  functional-analyst: mark task done — REMOVE from TODO.md
       (no ## Done section; git history keeps the record)
7.4  release-manager: commit + push TODO.md    (unpushed default-branch
       commits are the fuel for branch-rides-along divergence)
7.5  release-manager: clean up issue labels / close issue
7.6  owner: release or next task?
       release → release-manager → c3:release
       next    → return to project-manage (Phase 2)
```

All git/GitHub operations go through c3:release-manager (ephemeral,
one-shot prompts — this skill never touches git or gh itself).

### 7.2 — Switch and sync

```
agent(agent_name="c3:release-manager",
      prompt="Switch to the default branch and pull latest.
              If pull reports divergence: STOP — never auto-resolve.
              Fetch, diff both sides by content, determine which side
              is authoritative, and present the owner with rebase-pull
              vs reset options.",
      ephemeral=true)
```

Then verify committed `analysis/` and `reporting/` files from the merged
work exist on the default branch; surface anything missing to the owner
before proceeding.

### 7.3 — Mark done (functional-analyst)

```
agent(agent_name="c3:functional-analyst",
      prompt="Update TODO.md: task {task-id} is complete after PR #{N}
              merge — remove the task entry entirely (no ## Done section;
              git history keeps the record).",
      ephemeral=true)
```

### 7.5 — Issue cleanup (release-manager)

Remove whatever `status:*` label the issue carries (a completed issue ends
unlabeled — the swap invariant); if the issue did not auto-close, close it
with a brief comment referencing the merged PR.

### 7.6 — Owner chooses

The owner is present (they just merged) — ask directly: release, or next
task. Report a concise summary: task done, issue closed, chosen next step.

## Reference

- [../project-manage/SKILL.md](../project-manage/SKILL.md) — the coordinator
  that resumes Phase 2 when "next task" is chosen.