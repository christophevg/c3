# PLAN.md Structure Reference

Reference for understanding the master PLAN.md format.

## Required Sections

### Project Landscape

Table of all projects with:
- Project name
- Location (path)
- Status (✅ Active, 🟡 In Progress, 🔴 Needs Work)
- Priority/Description

```markdown
| Project | Location | Status | Priority |
|---------|----------|--------|----------|
| baseweb | ~/Workspace/baseweb | 🔴 Needs Work | Flask + Vue |
```

### Priority Work Queue

Four priority levels:
- **P0**: Critical (Must Do Now)
- **P1**: High Priority (Next Up)
- **P2**: Medium Priority
- **P3**: Future

Each with table of tasks:
```markdown
| Task | Project | Blockers | Notes |
|------|---------|----------|-------|
| Vue 2 → 3 | baseweb | None | Vue 2 EOL |
```

### Interdependency Graph

ASCII diagram showing project dependencies:
```
baseweb ← pageable-mongo
    ↑      ← restful-mongo
    │
    └──→ applications
```

### Deadline Tracking

```markdown
| Item | Deadline | Status |
|------|----------|--------|
| Vue 2 EOL | Dec 2024 | ⚠️ OVERDUE |
```

### Decision Log

Record of key decisions:
```markdown
### YYYY-MM-DD: Decision Title

**Decision:** What was decided
**Rationale:** Why
**Reference:** Link to supporting doc
```

### Done Section

Completed work with date:
```markdown
### YYYY-MM-DD
- [x] Task completed
```

## Status Symbols

| Symbol | Meaning |
|--------|---------|
| ✅ | Active, healthy |
| 🟡 | In progress, needs attention |
| 🔴 | Critical, blocking |
| ⚠️ | Warning, overdue |

## File Location

`~/Workspace/agentic/PLAN.md`