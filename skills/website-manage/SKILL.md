---
name: website-manage
description: |
  Manage content website projects with streamlined conversational workflow. Syncs, processes GitHub issues into TODO, and implements tasks iteratively with user. Use for Jekyll/static sites when user asks to "manage website", "work on site tasks", or project has _config.yml. No PRs, no agents - direct collaboration. Examples: "manage the website", "work on site tasks", "next website task".
type: workflow
---

# Website Manage

Conversational management of content website projects (Jekyll/static):
sync, issue intake into TODO.md, then small-step iterative implementation
with the owner. No PRs, no agent engagement — direct collaboration with
the owner in chat.

## Triggering

- a `_config.yml` in the working directory (Jekyll site)
- "manage the website", "work on site tasks", "next website task"

# Inputs

Website repo checked out locally; TODO.md in canonical structure; the
owner present and reviewing in browser (`localhost:4000`).

## Workflow

### 1 — Sync first

`git(operation="pull")` before any work. Conflicts: report, never resolve
automatically, await owner guidance.

### 2 — Process open issues

`github(operation="issue_list", state="open", limit=10)` and, per issue:
show title/body → owner assigns P1–P4, Skip (won't implement), or
Research → add to TODO.md at that priority with acceptance criteria →
label `status:backlog` / `status:needs-research` / `status:wont-do`.

Known limitation: the Yoker github tool has no issue comment/edit/close —
labeling and commenting steps run only when those operations exist; report
the gap and let the owner do the labeling in the web UI meanwhile.

### 3 — Process unsorted TODO items

Read TODO.md `## Unsorted`; per item the owner assigns P1–P4 / Skip /
Research; move to backlog with acceptance criteria.

### 4 — Propose the next task

Present the highest-priority backlog item (P1 first). Owner: proceed /
show all / skip to next.

### 5 — Conversational implementation

Plan first, owner approves the plan, then small steps: describe → discuss
(if an open question) → implement → owner reviews in browser (localhost:
4000) → iterate on feedback → next step only on approval. Never implement
everything at once, never skip the browser-review step.

### 6 — Commit when approved

Stage the files explicitly, commit `type: description` (feat/fix/docs/
refactor/style), push. Direct commits — no PRs in this mode.

Update TODO.md per the canonical model: **remove the completed task**.
There is no `## Done` section — git history is the record.

Issue-sourced tasks: the implementing commit references `#N` so GitHub
auto-closes the issue at push; comment/label cleanup happens web-side
(the Yoker github tool cannot close or comment on issues).

# Deliverables

- Synced repo, sorted TODO.md, implemented and committed tasks with the
  removed-from-TODO convention, one-line per-item reports.

## Related

- `c3:commit` — commit message conventions
- `c3:project-status` — when the owner wants a health snapshot instead

## Never

- Open PRs or engage agents — this workflow is deliberately direct.
- Commit without the owner's browser-verified approval.
- Resolve merge conflicts automatically.
- Manage builds or the Jekyll server — the owner runs their own.