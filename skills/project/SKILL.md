---
name: project
description: |
  Dispatcher for project management skills. Routes to appropriate project-* skill based on intent. Use when user says "/project" with any project-related content. Examples: "/project feature add auth", "/project status", "/project manage".
---

# Project

Dispatcher skill for managing projects. Routes to appropriate sub-skills based on input intent.

## When to Use

Use this skill when the user says `/project` with any project-related intent. It parses the input and routes to the appropriate `project-*` sub-skill; it does no work itself.

## Usage

```
/project <input>
```

## Routing Logic

Parse user input and route to appropriate skill:

| Input Pattern | Routes To | Example |
|---------------|-----------|---------|
| `feature`, `add`, `new feature` | project-feature | `/project feature user authentication` |
| `status`, `backlog`, `what's next` | project-status | `/project status` |
| `refine`, `update todo`, `review backlog` | project-todo-refine | `/project refine todo` |
| `follow up on pr`, `check pr`, `pr #` | project-handle-pr | `/project follow up on PR #5` |
| `pr merged`, `merge pr` | project-post-merge | `/project PR #5 was merged` |
| `manage`, `workflow`, `next task` | project-manage | `/project manage` |
| `bug`, `fix`, `issue` | project-manage (bug workflow) | `/project bug login fails` |
| Any other input | project-manage | `/project start working` |

> **Note:** `project-handle-pr` and `project-post-merge` are sub-skills of
> `project-manage`. Routing to them directly skips the full state-detection in
> `project-manage` Phase 0 — use when the user explicitly references a specific
> PR. "follow up on *issue*" does NOT route here — it stays on `project-manage`
> (issue triage). For ambiguous input, default to `project-manage`.

## Behavior

1. **Parse** the user input for intent keywords
2. **Route** to the appropriate sub-skill
3. **Invoke** the sub-skill with the full input
4. **Report** the result back to user

## Intent Detection

```
IF input contains "feature" OR "add" OR starts with "new":
  → invoke project-feature with full input

ELSE IF input contains "status" OR "backlog" OR "what's next":
  → invoke project-status (no args needed)

ELSE IF input contains "refine" OR "update todo" OR "review backlog":
  → invoke project-todo-refine with full input

ELSE IF input references a PR explicitly — contains "pr #" OR "check pr" OR ("follow up" AND "pr"):
  → invoke project-handle-pr with full input (PR feedback iteration)

ELSE IF input contains "pr merged" OR "merge pr" OR ("merged" AND "pr"):
  → invoke project-post-merge with full input (post-merge cleanup)

ELSE IF input contains "bug" OR "fix" OR "issue" OR "broken":
  → invoke project-manage (will detect bug and use bug-fixing workflow)

ELSE:
  → invoke project-manage with full input
```

## Sub-Skills Available

- [project-feature](../project-feature/SKILL.md) — Capture and scope new features
- [project-status](../project-status/SKILL.md) — Show project status snapshot
- [project-todo-refine](../project-todo-refine/SKILL.md) — Iteratively refine TODO.md topics
- [project-manage](../project-manage/SKILL.md) — Full project workflow (features and bugs)
- [project-handle-pr](../project-handle-pr/SKILL.md) — PR feedback iteration (sub-skill of project-manage)
- [project-post-merge](../project-post-merge/SKILL.md) — Post-merge cleanup (sub-skill of project-manage)

## Examples

```
User: /project feature add user authentication
→ Routes to project-feature
→ Captures feature, asks for details if needed
→ Adds to TODO.md

User: /project status
→ Routes to project-status
→ Shows TODO.md summary and next tasks

User: /project refine todo
→ Routes to project-todo-refine
→ Shows TODO overview, iterates through topics for refinement

User: /project manage
→ Routes to project-manage
→ Starts full project workflow

User: /project bug login fails with error
→ Routes to project-manage
→ Detects bug, invokes bug-fixing workflow

User: /project follow up on PR #5
→ Routes to project-handle-pr
→ Fetches PR comments, re-validates changes via project-review, pushes

User: /project PR #5 was merged
→ Routes to project-post-merge
→ Switches to main, marks task done, cleans up issue

User: /project
→ Routes to project-manage
→ Starts project workflow (default)
```

## Integration with Other Skills

The project dispatcher works alongside these related skills:

- **bug-fixing** — Used by project-manage for bug workflows
- **start-baseweb-project** — Bootstrap new projects (separate from project-*)

## Related Agents

- **project-manager** — Orchestrates multi-task sessions with progress tracking. Use when you need to execute multiple tasks from TODO.md in sequence. Examples: "manage project", "work on top 5 priority tasks".
