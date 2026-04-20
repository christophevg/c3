---
name: pa
description: Main dispatcher for personal assistant workflow. Processes unstructured input into actionable TODOs. Use when user says "process inbox", "handle my input", or files exist in inbox/. Examples: "/pa", "process my inbox", "handle these files".
---

# Personal Assistant (pa)

Main dispatcher skill for the personal assistant workflow. Routes to specialized sub-skills for inbox processing, session management, and reply generation.

## When to Use This Skill

- User says "process inbox"
- User says "handle my input"
- Files exist in inbox/ directory
- User provides unstructured input to organize

## Workflow

### Step 1: Check Inbox

```
1. List files in inbox/ (excluding archive/)
2. If empty, report "Inbox is empty"
3. If files exist, proceed to Step 2
```

### Step 2: Initialize Session

```
1. Invoke pa-session skill to init/update state
2. Record start of new iteration
```

### Step 3: Process Inbox

```
1. Invoke pa-inbox skill
2. For each file:
   a. Read and parse content
   b. Categorize items
   c. Execute actions or generate questions
3. Collect all actions and questions
```

### Step 4: Generate Replies

```
1. Invoke pa-outbox skill
2. Create reply files in outbox/
3. Archive processed files
```

### Step 5: Update Session State

```
1. Invoke pa-session skill to update
2. Record actions completed
3. Record files processed
4. Update open items
```

### Step 6: Report Summary

```
Report to user:
- Files processed: N
- Actions taken: N
- Questions pending: N
- Memory created: Y/N
- Inbox status: Empty/N files remaining
```

## Routing Logic

| User Input | Routes To |
|------------|-----------|
| "process inbox" | Full workflow |
| "session status" | pa-session |
| "what's pending" | pa-session |
| "open items" | pa-session |
| "archive inbox" | pa-outbox |
| Unstructured input | pa-inbox |

## Sub-Skills

| Skill | Purpose |
|-------|---------|
| [pa-inbox](../pa-inbox/SKILL.md) | Process and categorize items |
| [pa-session](../pa-session/SKILL.md) | Manage session continuity |
| [pa-outbox](../pa-outbox/SKILL.md) | Generate replies, archive files |

## Example Session

```
User: /pa

1. Checking inbox... 3 files found
2. Processing file 1: coding_guidelines.md
   - Categorized: reference material
   - Action: Store in c3/analysis/
3. Processing file 2: more-apps.md
   - Categorized: 8 projects
   - Actions: Created 3 new projects, copied 3 old projects
   - Questions: 1 (maaltafels location)
4. Processing file 3: NOTES.md
   - Categorized: 20 actionable, 18 need clarification
   - Actions: Added to 6 project TODO.md files
   - Created 2 memory files
5. Generating replies... 3 files in outbox/
6. Archiving processed files... done

Summary:
- Files processed: 3
- Actions taken: 25
- Questions pending: 1
- Memory created: 2
- Inbox: Empty
```

## Iteration Pattern

The workflow supports multiple clarification rounds:

```
Iteration 1:
  inbox/item.md → process → outbox/re-item.md → archive

Iteration 2 (user creates reply):
  inbox/re-item.md → process → outbox/re-re-item.md → archive

Iteration 3 (final):
  inbox/re-re-item.md → process → all resolved → archive
```

## Memory Integration

During processing, create memory files for:

1. **Project knowledge** — Where projects live, how to access
2. **Workflow patterns** — Reusable process patterns
3. **User preferences** — How user likes things done

Memory files are stored in:
- `~/.claude/projects/{project-slug}/memory/`

## State Management

Session state is maintained in:
- `<project-root>/session-state.md`

Memory is maintained in:
- `memory/*.md` files

Both persist across conversations and iterations.

## Related Skills

- [pa-inbox](../pa-inbox/SKILL.md) — Item processing
- [pa-session](../pa-session/SKILL.md) — State tracking
- [pa-outbox](../pa-outbox/SKILL.md) — Reply generation

## Related Agents

- [assistant](../../agents/assistant.md) — Orchestration agent with memory