---
name: pa-inbox
description: Process inbox files and categorize items into actionable TODOs or clarification requests. Use when user says "process inbox", "handle inbox", or files exist in inbox/. Examples: "/pa-inbox", "process my inbox".
---

# Inbox Processor (pa-inbox)

Process unstructured input from inbox files and categorize items into actionable TODOs, clarification requests, or cross-cutting concerns.

## When to Use This Skill

- User says "process inbox" or "handle inbox"
- Files exist in `inbox/` directory
- User provides unstructured input to be processed

## Prerequisites

The following directories must exist (create if needed):
- `inbox/` — Input files location
- `inbox/archive/` — Processed files archive
- `outbox/` — Reply files location
- `memory/` — Memory files location (typically `~/.claude/projects/{project-slug}/memory/`)

## Workflow

### Step 1: List Inbox Files

```
1. List all files in inbox/ (excluding archive/ subdirectory)
2. If no files, report "Inbox is empty" and exit
3. Sort files by modification time (oldest first)
```

### Step 2: Process Each File

For each file in inbox:

```
1. Read file content
2. Parse YAML frontmatter (if present):
   - author: Who created the input
   - date: When it was created
   - title: Optional title
3. Extract items:
   - Lines starting with "- " (list items)
   - Lines starting with "1. " (numbered items)
   - Lines with inline replies (user prefix)
   - Section headings (for context)
```

### Step 3: Categorize Each Item

For each extracted item, determine category:

| Category | Criteria | Action |
|----------|----------|--------|
| **Actionable** | Clear target project, clear action | Add to project TODO.md |
| **Needs Clarification** | Missing project, unclear action | Add question to outbox |
| **Cross-Cutting** | Affects multiple projects | Track as agentic-level TODO |
| **Information** | General info to remember | Create/update memory file |
| **Reply to Previous** | File name starts with "re-" | Process as clarification response |

### Step 4: Execute Actions

For actionable items:

```
1. Find target project:
   - Item explicitly names project (e.g., "c3: add skill")
   - Item matches known project (check CLAUDE.md files)
   - Item is new project (create folder + TODO.md)

2. Add to TODO.md:
   - Add to "## Inbox Input (YYYY-MM-DD)" section
   - Create section if doesn't exist
   - Format: "- <item text>"

3. Create projects if needed:
   - New projects: Create folder in agentic space
   - Old projects: Copy from ~/Workspace or clone from GitHub
```

### Step 5: Generate Outbox Reply

Create reply file in outbox:

```
Filename: re-<original-filename> or re-re-<original-filename>

Content:
# Reply: <original-filename>

**Original:** `inbox/<filename>`
**Date:** YYYY-MM-DD

---

## Actions Taken

| Item | Action | Status |
|------|--------|--------|
| ... | ... | ✓ / ⏳ |

## Memory Created

| Memory | Content |
|--------|---------|
| ... | ... |

## Status: Complete | Pending Questions

**Pending:** <questions if any>
```

### Step 6: Archive Processed Files

```
1. Move processed files to inbox/archive/
2. Verify archive contains all processed files
3. Verify inbox/ is empty (except archive/)
```

### Step 7: Update Session State

Update `session-state.md` in project root:

```
1. Increment iteration count
2. Add files processed to table
3. Update actions completed
4. Update open items
5. List files modified
```

## Item Categorization Rules

### Project Detection

Look for project indicators in item text. Common patterns include explicit prefixes or context from surrounding content.

### Clarity Indicators

**Clear (Actionable):**
- Explicit project mentioned
- Specific action verb (add, create, fix, update)
- Single, well-defined task

**Unclear (Needs Clarification):**
- Missing project context
- Ambiguous action
- Multiple interpretations possible
- Feature without details

### Cross-Cutting Patterns

Items are cross-cutting if they:
- Affect multiple projects
- Are research items
- Are architectural decisions
- Are "agentic-level" TODOs

## File Format Reference

### Inbox File Format

```yaml
---
author: AuthorName
date: YYYY-MM-DD
title: Optional Title
---
<markdown content with items>
```

### Inline Reply Format

```
USER_PREFIX: <response to previous item>
```

### Threaded Reply Naming

- Original: `inbox/item.md`
- First reply: `inbox/re-item.md`
- Second reply: `inbox/re-re-item.md`
- etc.

## Memory Integration

When processing reveals reusable information:

1. Create memory file in `memory/` directory
2. Use appropriate type: `project`, `feedback`, or `reference`
3. Update `memory/MEMORY.md` index

## Related Skills

- [pa-session](../pa-session/SKILL.md) — Manage session state
- [pa-outbox](../pa-outbox/SKILL.md) — Generate replies
- [pa](../pa/SKILL.md) — Main dispatcher