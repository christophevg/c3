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

## MCP Tools Available

| Tool | Purpose |
|------|---------|
| `list_accounts` | List configured email accounts |
| `list_folders` | List folders for an account |
| `search_emails` | Search for messages (supports `UNSEEN`, `ALL`, etc.) |
| `get_email` | Fetch full message content |
| `send_email` | Send new email |
| `reply_email` | Reply to existing thread |
| `move_email` | Move message between folders |
| `mark_email_read` | Mark message as read (sets `\Seen` flag) |
| `delete_email` | Delete message |

## Workflow

### Step 1: Check for New Emails

```bash
search_emails(account="default", folder="INBOX", criteria="UNSEEN")
```

Use `criteria="UNSEEN"` to get only unread/unprocessed messages. This eliminates the need for deduplication — unseen messages are by definition new.

If no messages, report "No new emails" and exit.

### Step 2: Read Each New Email

For each message ID returned by search:

```bash
get_email(account="default", message_id="<id>", folder="INBOX")
```

Extract:
- Sender name and email address
- Subject
- Date
- Body content (plain text or HTML)
- Attachments (if any)

### Step 3: Categorize Content

For each item extracted from the email body, categorize just like `pa-inbox`:

| Category | Criteria | Action |
|----------|----------|--------|
| **Actionable** | Clear target project, clear action | Add to project TODO.md |
| **Needs Clarification** | Missing project, unclear action | Include question in reply |
| **Cross-Cutting** | Affects multiple projects | Track as agentic-level TODO |
| **Information** | General info to remember | Create/update memory file |
| **Greeting/Context** | Social, no action needed | Acknowledge in reply |

### Step 4: Execute Actions

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

### Step 5: Generate and Send Reply

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

### Step 6: Mark as Read and Archive

After successful reply:

```bash
# Mark message as read
mark_email_read(account="default", message_id="<id>", folder="INBOX")

# Move to Archive
move_email(account="default", message_id="<id>", source_folder="INBOX", dest_folder="Archive")
```

**Order matters:** Mark as read first, then move. This ensures the message has the `\Seen` flag before archiving.

> **Why both?** Marking as read ensures the message won't appear in future UNSEEN searches. Moving to Archive keeps the INBOX clean.

### Step 7: Report Summary

After processing all messages, report:

```markdown
**Email Processing Complete**

| Metric | Count |
|--------|-------|
| Emails processed | N |
| Actions taken | N |
| Replies sent | N |
| Pending questions | N |
```

## Error Handling

| Error | Action |
|-------|--------|
| Cannot connect to email server | Report error, do not retry immediately |
| Message fetch fails | Log the message ID, skip it, continue with others |
| Reply send fails | Do NOT mark as read or archive; retry in next iteration |
| Move/archive fails | If reply was sent and marked read, note it; message won't reappear in UNSEEN search |
| Unknown sender | Process normally, but be cautious about creating projects |

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
- If no new emails (UNSEEN returns empty), report silently or with minimal output
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
6. Mark as read and archive original email

## Related Skills

- `pa-inbox` — File-based inbox processing
- `pa-outbox` — File-based reply generation
- `pa-session` — Session state management
- `pa` — Main personal assistant dispatcher
- `git-activity-report` — Generate activity reports (uses md-to-html for email)