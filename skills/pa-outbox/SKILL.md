---
name: pa-outbox
description: Generate formatted outbox replies and manage archive. Use after processing inbox files to create user-facing replies. Examples: "/pa-outbox", "create reply", "archive processed files".
---

# Outbox Processor (pa-outbox)

Generate formatted outbox replies and manage the archive workflow.

## When to Use This Skill

- After processing inbox files
- Need to create user-facing reply
- Need to archive processed files
- User asks to "archive inbox"

## Output Directory

**Location:** `<project-root>/outbox/`

**Archive Location:** `<project-root>/inbox/archive/`

## Reply Format

### Standard Reply

```markdown
# Reply: <original-filename>

**Original:** `inbox/<filename>`
**Date:** YYYY-MM-DD

---

## Actions Taken

### Category Name (optional)

| Item | Action | Status |
|------|--------|--------|
| ... | ... | ✓ / ⏳ |

### Additional Actions

- Description of other actions

---

## Memory Created

| Memory | Content |
|--------|---------|
| filename | Brief description |

---

## Status: Complete | Pending Questions

**Pending:** <questions if any, one per line>
```

### Clarification Reply

```markdown
# Reply: <original-filename>

**Original:** `inbox/<filename>`
**Date:** YYYY-MM-DD

---

## Actions Taken

**None yet.** The following items need clarification:

### Item Requiring Clarification

> Original item text

**Questions:**
1. Question text?
2. Question text?

---

## Status: Pending Questions

**Pending:** <summary of what's needed>
```

### Resolution Reply

```markdown
# Reply: <original-filename>

**Original:** `inbox/<filename>`
**Date:** YYYY-MM-DD

---

## Actions Taken

| Item | Action | Status |
|------|--------|--------|
| ... | ... | ✓ |

---

## Status: Complete

All items resolved.
```

## Naming Convention

| Type | Filename Pattern |
|------|-----------------|
| Original file | `item.md` |
| First reply | `re-item.md` |
| Second reply | `re-re-item.md` |
| Third reply | `re-re-re-item.md` |

**Pattern:** `re-` prefix for each clarification round.

## Workflow

### Step 1: Determine Reply Type

| Situation | Reply Type |
|-----------|------------|
| All items actionable | Resolution |
| Some items unclear | Clarification |
| Mix of both | Standard |

### Step 2: Generate Reply Content

```
1. Include reference to original file
2. Add date stamp
3. List actions taken (table format)
4. Note memory created
5. Add status indicator
6. Include pending questions if any
```

### Step 3: Write Reply File

```
1. Determine filename: re-<original>
2. If reply already exists: re-re-<original>
3. Write to outbox/
4. Verify file created
```

### Step 4: Archive Original Files

```
1. List processed inbox files
2. Move each to inbox/archive/
3. Verify archive contains files
4. Verify inbox/ is empty
```

## Table Formatting

### Action Table

| Column | Content |
|--------|---------|
| Item | Brief item description |
| Action | What was done |
| Status | ✓ (done) or ⏳ (pending) |

### Memory Table

| Column | Content |
|--------|---------|
| Memory | Memory filename |
| Content | Brief description |

## Status Indicators

| Status | Meaning |
|--------|---------|
| Complete | All items resolved |
| Pending Questions | Needs user response |
| Partially Complete | Some done, some pending |

## Archive Management

### Before Archiving

Verify:
- [ ] All files have been processed
- [ ] Reply files created in outbox/
- [ ] Session state updated
- [ ] Memory files created (if needed)

### Archive Process

```
for each file in processed_files:
  move file to inbox/archive/
  verify file in archive/
verify inbox/ empty (except archive/)
```

### After Archiving

Report:
- Number of files archived
- Current inbox status (empty)
- Reply files in outbox

## Inline Reply Processing

When file contains user prefix lines:

```
1. Extract lines with user prefix
2. These are user's responses to previous questions
3. Match to original questions from session state
4. Process responses as new input
5. Continue with actions
```

## Related Skills

- [pa-inbox](../pa-inbox/SKILL.md) — Main processing workflow
- [pa-session](../pa-session/SKILL.md) — Track session progress
- [pa](../pa/SKILL.md) — Main dispatcher