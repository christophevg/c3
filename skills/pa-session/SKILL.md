---
name: pa-session
description: Manage session state for personal assistant workflow continuity. Use when starting/ending inbox processing, or when user asks for session status. Examples: "/pa-session init", "/pa-session status", "what's the session status".
---

# Session State (pa-session)

Manage session state file for continuity across personal assistant iterations.

## When to Use This Skill

- Start of inbox processing session
- End of inbox processing session
- User asks for session status
- User asks "what's pending"
- Need to track open items

## State File

**Location:** `<project-root>/session-state.md`

**Format:**

```markdown
# Personal Assistant Session State

**Session Date:** YYYY-MM-DD
**Session Type:** Inbox Processing

---

## Iteration Summary

<brief summary of current iteration>

---

## Incoming Files Processed

| Iteration | File | Items | Resolved |
|-----------|------|-------|----------|
| 1 | `inbox/file.md` | N | → iteration 2 |
| 2 | `inbox/re-file.md` | N | ✓ |

---

## Actions Completed

### New Projects Created

| Project | Type | Status |
|---------|------|--------|
| ... | New/Copied/Cloned | ✓ |

### TODO.md Files Updated

| Project | Updates |
|---------|---------|
| ... | ... |

---

## Memory Created

| Memory | Content |
|--------|---------|
| ... | ... |

---

## Agentic-Level TODOs

Cross-cutting items tracked at agentic level:

1. **Item** - Description

---

## Open Items

| Item | Status | Notes |
|------|--------|-------|
| ... | Pending/Blocked | ... |

---

## Files Modified This Session

| File | Action |
|------|--------|
| ... | Created/Updated |
```

## Operations

### Initialize Session State

```
1. Check if session-state.md exists
2. If not, create with template
3. Set session date to current date
4. Set session type based on context
5. Initialize empty tables
```

### Update Session State

```
1. Read current session-state.md
2. Update iteration summary
3. Add new files to processed table
4. Add actions to completed section
5. Update open items
6. Add files modified
7. Write updated state
```

### List Open Items

```
1. Read session-state.md
2. Parse Open Items table
3. Return list of unresolved items
4. Include status (Pending/Blocked) and notes
```

### Check Session Status

```
1. Read session-state.md
2. Count:
   - Total files processed
   - Total items resolved
   - Open items remaining
3. Report summary
```

## State Transitions

| From | To | Trigger |
|------|-----|---------|
| Empty | Initialized | `/pa-session init` |
| Initialized | Active | First file processed |
| Active | Updated | Each iteration |
| Updated | Complete | All items resolved |

## Iteration Tracking

Each inbox processing iteration:

1. Increment implicit counter
2. Add entry to "Incoming Files Processed" table
3. Update "Actions Completed" section
4. Update "Open Items" table

### Iteration Flow

```
Iteration 1:
  inbox/file.md → outbox/re-file.md → inbox/archive/file.md

Iteration 2:
  inbox/re-file.md → outbox/re-re-file.md → inbox/archive/re-file.md

Iteration N:
  inbox/re-(N-1)-file.md → resolved → archive
```

## Open Items Management

### Adding Open Items

```
| Item | Status | Notes |
|------|--------|-------|
| Feature X | Pending | Needs clarification on Y |
| Project Y | Blocked | Depends on Z |
```

### Resolving Open Items

```
1. Find item in table
2. Change status to "✓ Resolved"
3. Add resolution note
4. Optionally move to "Actions Completed"
```

## Memory Integration

Session state and memory work together:

- **Session state**: Short-term, session-specific tracking
- **Memory files**: Long-term, reusable knowledge

When session reveals reusable info:

1. Create memory file (see memory skill)
2. Add to "Memory Created" section in session state
3. Update memory index

## Related Skills

- [pa-inbox](../pa-inbox/SKILL.md) — Main processing workflow
- [pa-outbox](../pa-outbox/SKILL.md) — Generate replies
- [pa](../pa/SKILL.md) — Main dispatcher