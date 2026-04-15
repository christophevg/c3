---
name: plan-review
description: Review cross-project priorities and manage master PLAN.md. Use when starting a session in ~/Workspace/agentic, asking what to work on, or updating project status. Examples: "What should I work on?", "Review the plan", "Update PLAN.md".
---

# Plan Review

Review the master project plan to understand priorities, blockers, and recommended next work. Use at session start to orient yourself and the user.

## Overview

| Capability | Description |
|------------|-------------|
| Read PLAN.md | Load and parse master project plan |
| Report P0 Blockers | Identify critical blockers and deadlines |
| Recommend Work | Suggest next work based on priority and dependencies |
| Update Plan | Track progress and update PLAN.md after work |
| Add Projects | Capture new projects in the landscape |

## When to Use This Skill

Use this skill when:
- Starting a session in `~/Workspace/agentic`
- User asks "What should I work on?"
- User asks to "review the plan" or "update the plan"
- Adding a new project to track
- Checking deadline status

## Workflow

### Step 1: Read PLAN.md

Read `~/Workspace/agentic/PLAN.md` at session start.

**Key sections to extract:**
- Priority Work Queue (P0, P1, P2, P3)
- Deadline Tracking
- Interdependency Graph
- Project Landscape table
- Decision Log

### Step 2: Report Status

Generate a status report with:

```
## Plan Status (YYYY-MM-DD)

### P0 Critical Blockers
[Table of P0 items with project, deadline, status]

### Deadline Status
[Items approaching deadline with days remaining]

### Recommended Next Work
[Ordered list based on priority and blockers]

What would you like to work on?
```

### Step 3: Provide Context

When recommending work, explain:
- Why it's priority (blockers, dependencies, deadlines)
- What's blocking it (if anything)
- What it unblocks (downstream work)

### Step 4: Track Progress

During work, track:
- Tasks completed
- New tasks discovered
- Blockers encountered

### Step 5: Update PLAN.md

After completing work:
1. Move completed tasks to "Done" section
2. Update project status in tables
3. Add new tasks discovered
4. Update interdependency graph if needed
5. Add decisions to Decision Log

## Interdependency Graph

Use the dependency graph to:
- Identify what's blocking a project
- Find what a project unblocks
- Recommend parallel work (no dependencies)
- Flag serial work (has dependencies)

**Graph traversal:**
```
c3 → incubator → [produces skills]
     ↓
baseweb ← pageable-mongo
    ↑      ← restful-mongo
    │
    └──→ applications (letmelearn, dashboard)
```

## Priority Rules

| Priority | Meaning | Action |
|----------|---------|--------|
| P0 | Critical, blocking | Must do now |
| P1 | High, soon | Do next |
| P2 | Medium | Schedule |
| P3 | Future | Backlog |

## Deadline Status Codes

| Status | Symbol | Days Left |
|--------|--------|-----------|
| Overdue | ⚠️ OVERDUE | < 0 |
| Critical | 🔴 | < 7 |
| Warning | 🟡 | 7-30 |
| OK | ✅ | > 30 |

## Common Patterns

### Starting a Session

1. Read `~/Workspace/agentic/PLAN.md`
2. Generate status report
3. Highlight P0 blockers
4. Ask user for direction

### After Completing Work

1. Identify what was completed
2. Check if it unblocks downstream work
3. Update PLAN.md tables
4. Move tasks to Done section
5. Suggest next priority

### Adding a New Project

1. Ask for project name, location, description
2. Determine project type (infrastructure, app, framework)
3. Identify dependencies
4. Add to Project Landscape table
5. Add to Interdependency Graph
6. Create initial P1/P2 tasks

## Reference Files

- `references/plan-structure.md` - PLAN.md format reference

## Related Skills

- **manage-project** - Project-level orchestration
- **develop-skill** - Creating new skills in incubator
- **promote-skill** - Moving skills from incubator to C3