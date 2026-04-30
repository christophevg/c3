---
name: pa-email
aliases:
  - email-inbox
description: Process emails via MCP email server as a personal assistant inbox. Check for new messages, process actionable items, reply to sender, and archive. Use when user says "check email", "process emails", "email inbox", or when running a loop to poll for messages.
---

# Email Inbox Processor (pa-email)

Process incoming emails via the MCP email server, turning them into actionable TODOs, memory, and replies — just like the file-based `pa-inbox`/`pa-outbox` workflow, but using email as the transport.

## When to Use This Skill

- User says "check my email", "process emails", "email inbox"
- Running in a loop to poll for new messages
- User sends an email that contains tasks, ideas, or questions
- Need to reply to an email and archive it

## Prerequisites

- MCP email server configured with at least one account
- Account name known (default is usually `default`)
- Sender identity established as **Eira** (calm, thoughtful, personal assistant)

## Email Account

**Default account:** `default` (`eira_vg@icloud.com`)

**Folders:**
- `INBOX` — Incoming messages to process
- `Archive` — Processed messages moved here
- `Deleted Messages` — Trash

## Workflow

### Step 1: Check for New Emails

```
1. Search INBOX for ALL messages (not just UNSEEN)
2. Retrieve list of message IDs
3. If no messages, report "No new emails" and exit
```

> **Note:** Some email servers do not update UNSEEN flags immediately or may cache search results. Always search `ALL` and use the deduplication strategy below.

### Step 2: Deduplication (Critical)

Before processing any message, check if it has already been handled:

```
1. Fetch all messages in INBOX (get full content: subject, from, date, body)
2. Fetch all messages in Archive (get full content)
3. For each message, create a signature: subject + "|" + from + "|" + date
4. Compare INBOX signatures against Archive signatures
5. Skip any INBOX message whose signature matches an Archive message
```

> **Why:** Message IDs are folder-local, not globally unique. Message `2` in INBOX is a different message than message `2` in Archive. Additionally, some email servers cache search results, so a moved message may still appear in INBOX. Content-based deduplication (subject + sender + date) is reliable.

### Step 3: Read Each New Email

For each unprocessed message in INBOX:

```
1. Fetch full email content (subject, from, to, date, body)
2. Extract the sender's name and email address
3. Parse the body as markdown/plain text
4. Identify items:
   - Lines starting with "- " or "* " (list items)
   - Numbered items
   - Paragraphs describing tasks or questions
   - Inline replies or thread context
```

### Step 4: Categorize Content

For each item extracted from the email body, categorize just like `pa-inbox`:

| Category | Criteria | Action |
|----------|----------|--------|
| **Actionable** | Clear target project, clear action | Add to project TODO.md |
| **Needs Clarification** | Missing project, unclear action | Include question in reply |
| **Cross-Cutting** | Affects multiple projects | Track as agentic-level TODO |
| **Information** | General info to remember | Create/update memory file |
| **Greeting/Context** | Social, no action needed | Acknowledge in reply |

### Step 5: Execute Actions

For actionable items:

```
1. Find target project (explicit name, known project, or create new)
2. Add to project's TODO.md under "## Email Input (YYYY-MM-DD)"
3. Create projects if needed
4. Update session-state.md if applicable
```

For information items:
```
1. Create memory file in memory/ directory
2. Update memory/MEMORY.md index
```

### Step 6: Generate and Send Reply

Compose a reply email to the sender:

**Reply format:**

```
Subject: Re: <original subject>
To: <original sender>
In-Reply-To: <original message ID>
```

**Body structure:**

```markdown
Hi <sender name>,

I've processed your email and here's what I did:

## Actions Taken

| Item | Action | Status |
|------|--------|--------|
| ... | ... | ✓ / ⏳ |

## Memory Created

| Memory | Content |
|--------|---------|
| ... | ... |

## Status: Complete | Pending Questions

<Any questions that need clarification>

---

Eira
```

**Tone guidelines:**
- Warm, calm, and personal — this is Eira speaking
- Use first person ("I processed", "I added")
- Be concise but thorough
- Match the sender's energy — if they're brief, be brief; if detailed, be detailed
- Sign off as "Eira"

**Markdown to HTML Conversion:**

When the reply contains Markdown formatting (tables, lists, headers), convert to HTML for proper email rendering:

```bash
echo "<markdown content>" | bin/md-to-html.py
```

Use `bin/md-to-html.py` to convert Markdown to styled HTML. Always provide both:
- `body` — Plain text fallback
- `html_body` — Styled HTML for email clients

**Send via:** `reply_email` MCP tool (preferred) or `send_email` with `In-Reply-To` header.

### Step 7: Archive the Original Email

```
1. Move the original message from INBOX to Archive folder
2. Verify the message appears in Archive
```

Use `move_email` with:
- `source_folder`: INBOX
- `dest_folder`: Archive
- `message_id`: <original message ID>

> Do NOT delete the email — archiving preserves the record and enables deduplication.

### Step 8: Report Summary

After processing all messages, report:

```markdown
**Email Processing Complete**

| Metric | Count |
|--------|-------|
| Emails checked | N |
| New emails processed | N |
| Actions taken | N |
| Replies sent | N |
| Pending questions | N |
```

## Deduplication Rules

1. **Primary method:** Content-based — compare `subject|from|date` signatures between INBOX and Archive
2. **Secondary method:** If a message cannot be moved (error), do NOT retry processing it in the same session
3. **Tertiary method:** Track processed signatures in session state or memory to guard against edge cases

## Loop Integration

To run this skill in a recurring loop:

```
/loop 30m /pa-email
```

**Recommended intervals:**
- **Active use:** 15-30 minutes
- **Background monitoring:** 1-2 hours
- **Overnight/weekend:** 2-4 hours

**Loop behavior:**
- If no new emails, report silently or with minimal output
- If emails processed, send reply and report summary
- Never error on empty inbox — this is normal

## Content Parsing Guidelines

### Subject Line Hints

The subject line may indicate the intent:

| Pattern | Interpretation |
|---------|----------------|
| "project: ..." | Action for specific project |
| "idea: ..." | Information/memory item |
| "question: ..." | Needs clarification or research |
| "re: ..." | Reply to previous thread |
| No pattern | Parse body for items |

### Body Parsing

Treat the email body like an inbox file:

```
- Lines starting with "- " are items
- Blank lines separate items
- Paragraphs may contain single items
- Code blocks are context, not actions
- Signatures and quoted replies are ignored
```

## Error Handling

| Error | Action |
|-------|--------|
| Cannot connect to email server | Report error, do not retry immediately |
| Message fetch fails | Log the message ID, skip it, continue with others |
| Reply send fails | Do NOT archive the message; retry reply in next iteration |
| Move/archive fails | If reply was sent, note it; do not reprocess unless confirmed duplicate |
| Unknown sender | Process normally, but be cautious about creating projects |

## Example Session

**User email:**
```
Subject: c3: add new skill for email processing

Hi Eira,

Can you add a skill to c3 for processing emails via MCP?
It should work like the inbox processor but use email.

Also, I'm thinking about a new project for tracking sailing trips.

Thanks!
```

**Eira's processing:**
1. Categorize: "add skill to c3" → actionable (project: c3)
2. Categorize: "new project for sailing trips" → actionable (new project)
3. Add to c3/TODO.md: "Add pa-email skill for email inbox processing"
4. Create `sailing-tracker/` project with TODO.md
5. Send reply with actions taken
6. Archive original email

## Related Skills

- `pa-inbox` — File-based inbox processing
- `pa-outbox` — File-based reply generation
- `pa-session` — Session state management
- `pa` — Main personal assistant dispatcher
- `git-activity-report` — Generate activity reports (uses md-to-html for email)