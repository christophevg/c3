# Inbox & Unified I/O Design

**Created:** 2026-04-18
**Last Updated:** 2026-04-18
**Status:** Design Complete
**Project:** Archiku — AI-Powered Architecture Intelligence
**Purpose:** Design for accepting unstructured input from multiple sources into the plan management system

---

## Overview

This document defines the architecture for accepting information input from multiple channels (email, chat, folder, etc.) and unifying it for agentic processing, as well as the reverse path for sending feedback out.

---

## Architecture

```
Agent (Stateless)                    Scripts (Stateful in their domain)
       │                                    │
       │ ─── fetch_new ───────────────────►│
       │      (YAML on stdin)              │ reads from source
       │                                    │ normalizes to unified format
       │ ◄─────────────────────────────── │ returns items (YAML on stdout)
       │      items: [...]                 │
       │                                    │
       │ processes items                    │
       │                                    │
       │ ─── mark_processed ──────────────►│
       │      (YAML on stdin)              │ marks in domain-appropriate way:
       │      processed_ids: [...]         │ - folder: move/delete files
       │                                    │ - email: mark read/archive
       │ ◄─────────────────────────────── │ - chat: store IDs locally
       │      status: confirmed            │
```

**Key principle:** The agent is stateless. Each script owns state within its domain.

---

## Separation of Concerns

### Scripts (Input Pipeline)

**Responsibilities:**
- Protocol specifics (IMAP, Slack API, filesystem, etc.)
- Authentication with external services
- Data extraction from source formats
- Normalization to unified format
- **State management within their domain**
- No agentic/cognitive capabilities required

**State Management (per script):**

| Script | Mark Processed Means |
|--------|---------------------|
| `inbox_folder.py` | Move files to `processed/` subfolder or delete |
| `inbox_email.py` | Mark as read, archive, or move to IMAP folder |
| `inbox_chat.py` | Store processed message IDs in local state file |

**Examples:**
- `inbox_email.py` — Polls IMAP server, extracts messages, returns unified format
- `inbox_chat.py` — Reads Slack/Discord API, extracts messages, returns unified format
- `inbox_folder.py` — Reads folder, extracts files, returns unified format

### Scripts (Output Pipeline)

**Responsibilities:**
- Receive YAML instructions on stdin
- Route to correct destination based on channel
- Handle delivery failures and retries
- Protocol-specific formatting
- Return status on stdout

**Examples:**
- `outbox_email.py` — Receives email YAML, sends via SMTP, returns status
- `outbox_chat.py` — Receives chat YAML, posts to Slack/Discord API, returns status
- `outbox_sms.py` — Receives SMS YAML, sends via gateway, returns status

### Agent (Cognitive Processing)

**Responsibilities:**
- Call scripts to fetch new items
- Understand and classify content
- Integrate into plan (via plan-learn, plan-decision, etc.)
- Generate responses
- Call scripts to mark items processed
- **Remain stateless** — no persistent state between calls

**Critical Requirement:** The agent must be **idempotent** — if the same information appears twice (e.g., crash before marking, or duplicate across channels), it handles gracefully:
- Plan system recognizes duplicates
- No duplicate entries created
- No errors on re-processing

---

## Script Protocol

All scripts communicate via YAML on stdin/stdout. This is agent-native, handles multiline content without escaping, and creates a consistent interface.

### Input Scripts Protocol

#### Fetch New Items

**Input (stdin) — YAML:**
```yaml
action: fetch_new
source: folder
path: inbox/
```

**Output (stdout) — YAML:**
```yaml
items:
  - id: "004"
    channel: folder
    author: Christophe
    timestamp: 2026-04-18T14:00:00Z
    body: |
      This is a multiline
      body with no escaping
      issues at all
  - id: "005"
    channel: folder
    author: Sarah
    timestamp: 2026-04-18T14:30:00Z
    body: |
      Another item
```

#### Mark Processed

**Input (stdin) — YAML:**
```yaml
action: mark_processed
source: folder
path: inbox/
processed_ids:
  - "004"
  - "005"
```

**Output (stdout) — YAML:**
```yaml
status: confirmed
processed_count: 2
```

### Output Scripts Protocol

#### Send Message

**Input (stdin) — YAML:**
```yaml
action: send
to: recipient@example.com
subject: Project Update
body: |
  Hi,

  Here's the update on the project...

  Best,
  Christophe
```

**Output (stdout) — YAML:**
```yaml
status: sent
message_id: <abc123@example.com>
timestamp: 2026-04-18T15:00:00Z
```

---

## Unified Item Format

The schema for each item returned by input scripts.

### Field Specifications

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier for this input item |
| `channel` | Yes | Channel type: `email`, `chat`, `folder`, `sms`, etc. |
| `author` | Yes | Person or system that provided the information |
| `timestamp` | Yes | ISO 8601 datetime when the information was created/received |
| `body` | Yes | The actual content as markdown |
| `title` | No | Brief summary; if absent, agent generates one from body |

### Example

```yaml
id: "004"
channel: folder
author: Christophe
timestamp: 2026-04-18T14:00:00Z
title: Motor EOL May 14
body: |
  The Motor library is deprecated as of May 14.
  We need to migrate to PyMongo Async.

  Affected projects:
  - pageable-mongo
  - data-service
```

---

## Folder Input File Format

For the folder-based input channel, files in the inbox folder use minimal frontmatter:

**File structure (`inbox/<filename>.md`):**
```yaml
---
author: Christophe
---
<body content as markdown>
```

**Derived by script:**
- `id` — generated from filename or hash
- `channel` — fixed as `folder`
- `timestamp` — file's last modified time (filesystem metadata)

---

## Processing Flow

### Input Processing

```
1. Agent calls script with action: fetch_new
2. Script reads from source (folder, email, chat)
3. Script normalizes to unified format
4. Script returns items on stdout
5. Agent receives items
6. Agent processes each item:
   a. Classifies content type
   b. Generates title if missing
   c. Integrates into plan (plan-learn, plan-decision, etc.)
   d. Generates response if needed
7. Agent calls script with action: mark_processed
8. Script marks items in domain-appropriate way
9. Script returns confirmation
```

### Output Processing

```
1. Agent generates response content
2. Agent calls output script with action: send
3. Script delivers to destination
4. Script returns status
```

### Idempotency Guarantee

If the agent crashes or fails between steps 6 and 7:
- Items remain in source (not yet marked)
- Next invocation fetches same items
- Agent must handle duplicates gracefully
- No data loss, no corruption

---

## Decision Log

### 2026-04-18: YAML for stdin/stdout

**Decision:** All scripts accept YAML on stdin and return YAML on stdout.

**Rationale:**
- YAML is agent-native — LLMs produce/consume it naturally
- Multiline strings (`|` or `>`) handle any content without escaping
- Consistent protocol across all scripts (input and output)
- Easy to test manually: `echo "action: fetch_new" | script.py`
- Composable with traditional CLI arguments if needed

**Implications:**
- Scripts have bidirectional YAML I/O
- No intermediate files required for data transfer
- Script documentation must specify YAML schema

---

### 2026-04-18: Agent Stateless, Scripts Stateful

**Decision:** The agent remains stateless. Each script owns state within its domain.

**Rationale:**
- State management is domain-specific (folder: move files, email: mark read, chat: local ID storage)
- Agent doesn't need to understand domain-specific state mechanisms
- Cleaner separation: agent does cognitive work, scripts handle persistence
- Agent idempotency handles edge cases (crash before mark, duplicates)

**Implications:**
- Agent must be idempotent — handle same information multiple times gracefully
- Scripts implement `fetch_new` and `mark_processed` actions
- No state files managed by agent
- Each script may have its own state storage mechanism

---

### 2026-04-18: Minimal Schema with LLM Title Generation

**Decision:** Use a minimal item schema with id, channel, author, timestamp, body (required) and title (optional). When title is missing, agent generates a summary.

**Rationale:**
- Emails naturally have subjects, chats don't
- Maintaining two schemas adds complexity
- LLM can generate meaningful titles from body content
- Optional title keeps schema flexible for all channels

**Implications:**
- Agent skill must include title generation logic
- Title generation happens at processing time, not fetch time

---

### 2026-04-18: Folder Input with Minimal Frontmatter

**Decision:** Folder input files require only `author` in frontmatter. Script uses file modification time for timestamp.

**Rationale:**
- Keeps files simple for quick dumping
- Author is genuinely new information (not derivable)
- Timestamp is derivable from filesystem
- Temporary channel — full frontmatter not needed

**Implications:**
- Input files in `inbox/` folder have minimal structure
- Script must parse YAML frontmatter and extract body
- Script must read file modification time

---

## Implementation Priority

1. **Script Protocol** — Define YAML schemas for actions ✅
2. **Folder Inbox Script** — First input channel (simplest)
3. **Inbox Processing Skill** — Agent skill to process unified format
4. **Folder Output Script** — Write responses to files
5. **Additional Input Scripts** — Email, chat, etc.
6. **Additional Output Scripts** — Email, chat, etc.

---

## Future Enhancements

- [ ] Email input script (IMAP/POP)
- [ ] Slack input script
- [ ] Discord input script
- [ ] SMS input script (via gateway)
- [ ] Email output script (SMTP)
- [ ] Chat output scripts (Slack/Discord API)
- [ ] Bi-directional threading (link related messages)
- [ ] Attachment handling
- [ ] Rich content parsing (HTML emails, formatted chat)
- [ ] Error handling and retry protocols
- [ ] Rate limiting for external APIs