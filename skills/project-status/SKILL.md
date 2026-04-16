---
name: project-status
description: Show current project status snapshot. Reads TODO.md, analysis/, and reporting/ to provide a quick overview. Use when user says "/project status" or asks "what's the project status". Examples: "/project status", "show project status".
---

# Project Status

Show a quick overview of the current project status. Reads project artifacts to provide a snapshot of work state.

## Usage

```
/project-status
/project status
```

## Behavior

1. **Read TODO.md** to get task counts and next tasks
2. **Check analysis/** for project artifacts
3. **Check reporting/** for recent summaries
4. **Summarize** in a concise report

## Output Format

```markdown
## Project Status

**TODO.md Summary:**
- Unsorted: 2 features
- P0: 0 tasks
- P1: 3 tasks
- P2: 5 tasks
- P3: 2 tasks
- Done: 12 tasks

**Next Up:**
1. [P1] Task name
2. [P1] Another task
3. [P2] Lower priority

**Project Artifacts:**
- ✅ analysis/functional.md
- ❌ analysis/api-*.md
- ✅ reporting/{last-task}/summary.md

**Recent Activity:**
- Last completed: {task-name} ({date})
```

## Files to Read

| File | Section to Extract |
|------|-------------------|
| `TODO.md` | Task counts by priority, next 3 tasks from backlog |
| `analysis/functional.md` | Existence check (created/not created) |
| `analysis/api-*.md` | Existence check for API analysis |
| `analysis/ux-*.md` | Existence check for UX analysis |
| `reporting/*/summary.md` | Last task completed, date |

## TODO.md Parsing

Parse TODO.md to extract:

1. **Unsorted Features**: Count items under `## Unsorted Features`
2. **P0 Tasks**: Count items under `### P0 - Critical`
3. **P1 Tasks**: Count items under `### P1 - High`
4. **P2 Tasks**: Count items under `### P2 - Medium`
5. **P3 Tasks**: Count items under `### P3 - Low`
6. **Done Tasks**: Count items under `## Done`
7. **Next Up**: First 3 unchecked items from prioritized backlog

## Status Indicators

Use these indicators for artifacts:

| Indicator | Meaning |
|-----------|---------|
| ✅ | File exists |
| ❌ | File missing |
| ⚠️ | File exists but may be outdated |

## Example Output

```markdown
## Project Status — MyProject

**TODO.md Summary:**
- Unsorted: 2 features
- P0: 0 tasks
- P1: 3 tasks
- P2: 5 tasks
- P3: 2 tasks
- Done: 8 tasks

**Next Up:**
1. [P1] Implement user authentication
2. [P1] Add password reset flow
3. [P2] Create user profile page

**Project Artifacts:**
- ✅ analysis/functional.md — Last updated 2026-04-10
- ✅ analysis/api-auth.md — Created 2026-04-12
- ❌ analysis/ux-*.md — Not yet created
- ✅ reporting/user-auth/summary.md

**Recent Activity:**
- Last completed: Setup project structure — 2026-04-15
- Total tasks completed: 8

**Recommendations:**
- 2 unsorted features need scoping — use `/project-feature` to detail them
- No P0 tasks — consider if priorities are correctly assigned
```

## Handling Missing Files

If TODO.md doesn't exist:
```
**TODO.md:** ❌ Not created

This project hasn't been initialized. Use `/project-manage` to start the workflow.
```

If analysis/ doesn't exist:
```
**Analysis:** ❌ No analysis folder

Project analysis not yet started. Use `/project-manage` to begin.
```

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `/project-feature` | Adds features to TODO.md |
| `/project-manage` | Picks up tasks from TODO.md and implements them |
| `/project` | Dispatcher that routes to this skill |

## Notes

- Quick read-only snapshot — no modifications
- If TODO.md is missing, suggest initialization
- If unsorted features exist, remind user to scope them
- Show last activity to give context on progress