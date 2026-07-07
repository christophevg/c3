---
name: project-post-merge
description: Handle post-merge cleanup for a project task after the owner merges a PR. Sequenced to prevent TODO.md loss: switches to main and pulls BEFORE any TODO.md edit, marks the task done, commits, cleans up issue labels, and asks owner about release vs next task. Use when the user reports a PR was merged, or project-manage routes here from a merged feature branch.
---

# Project Post-Merge

Sub-skill of `c3:project-manage`. Covers **Phase 7 — post-merge**: the cleanup
that runs after the owner merges a feature-branch PR.

## Why this is a separate skill

Post-merge is independently invokable (the user reports "PR #N was merged") and
carries **loss-critical sequencing rules** worth isolating: TODO.md updates must
happen on master *after* switching branches, otherwise they sit on the feature
branch and are lost when it is deleted. Collecting these rules in one focused
skill makes the failure mode impossible to forget.

## Inputs

The caller (`project-manage`) provides:

- **Project root** (from release-manager's state report)
- **PR number** and the merged task id (from TODO.md, or found via release-manager)
- **Issue number** linked to the task (if any)

## ⛔ Rules

- **No Bash / git / gh directly.** Delegate all source-control and GitHub
  operations to `c3:release-manager`.
- **Execute the steps in SEQUENCE.** Do not reorder. Step 7.2 (switch to main)
  MUST happen before Step 7.3 (TODO.md edit) — otherwise TODO.md changes are
  made on the feature branch and lost on branch deletion.
- **The owner merges.** This skill runs only *after* the owner reports a merge.
  It never merges.

## Workflow

```
7.1  find the issue number (TODO.md entry or release-manager from PR)
7.2  release-manager: switch to main + pull           ← BEFORE any TODO edit
7.3  functional-analyst: mark task done in TODO.md + completion date
7.4  release-manager: commit TODO.md
7.5  release-manager: clean up issue labels / close issue
7.6  owner: release or next task?
       release → delegate to release-manager (c3:release)
       next    → return to project-manage Phase 2
```

### 7.1 Find the issue number

- Check the TODO.md task entry (it includes the issue reference), or
- Delegate to release-manager to find it from the merged PR.

### 7.2 Switch to main and pull (BEFORE any TODO.md edit)

⚠️ **This must happen before Step 7.3.** After a merge we are typically still on
the feature branch. TODO.md updates made before switching stay on the feature
branch and may be lost when the branch is deleted.

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Switch to main branch and pull latest.",
  description: "Sync to main"
})
```

**Handle untracked artifacts:** check for `analysis/` and `reporting/` files
from the merged work. These should already be committed to the PR. Verify they
exist on main after the switch; if anything is missing, surface it to the owner
before proceeding.

### 7.3 Mark the task done in TODO.md

The functional-analyst owns the TODO.md lifecycle. Delegate:

```
Agent({
  subagent_type: "c3:functional-analyst",
  prompt: "Update TODO.md to mark task {task-id} as complete after PR merge. Add completion date (YYYY-MM-DD), move the task to the Done section.",
  description: "Mark task complete in TODO.md"
})
```

### 7.4 Commit TODO.md

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Commit TODO.md changes with message: 'docs: mark task {task-id} as complete'",
  description: "Commit TODO.md"
})
```

### 7.5 Clean up GitHub issue labels

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Remove 'status:in-progress' label from issue #{issue-number}. If the issue is not auto-closed, close it with a brief comment referencing the merged PR.",
  description: "Clean up issue"
})
```

### 7.6 Release or next task?

The owner is present (they just merged). Ask directly:

- **Release** → delegate to release-manager to execute the release workflow
  (`c3:release` skill: version bump, changelog, pre-publish checks, build, tag,
  GitHub release, PyPI upload).
- **Next task** → return control to `c3:project-manage`, which proceeds to
  Phase 2 (task selection) for the next backlog item.

Report a concise summary to the owner: task marked done, issue closed, and the
chosen next step.

## Reference

- [../project-manage/SKILL.md](../project-manage/SKILL.md) — the coordinator
  that invokes this skill and resumes Phase 2 when "next task" is chosen.
