---
name: project
description: Dispatcher for project management skills. Routes to appropriate project-* skill based on intent. Use when user says "/project" with any project-related content. Examples: "/project feature add auth", "/project status", "/project manage".
---

# Project

Dispatcher skill for managing projects. Routes to appropriate sub-skills based on input intent.

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
| `manage`, `workflow`, `next task` | project-manage | `/project manage` |
| `bug`, `fix`, `issue` | project-manage (bug workflow) | `/project bug login fails` |
| Any other input | project-manage | `/project start working` |

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