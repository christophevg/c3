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

## Critical Guardrails

### Use Skills, Not Manual Commands

When a skill exists for a task, **use it immediately** — do not run manual commands:

| Task | Use | NOT |
|------|-----|-----|
| Git activity report | `c3:git-activity-report` skill | `git log`, `git diff` |
| Project status | `c3:project-status` skill | manual file reads |
| Commit changes | `c3:commit` skill | `git commit` |

**Why:** Skills encapsulate correct behavior, handle edge cases, and produce consistent output.

### Email Operations: MCP Tools ONLY

**NEVER** access email servers directly (no curl, no imap libraries, no direct API calls).

**ALWAYS** use the MCP email tools listed below. They handle authentication, protocol details, and error handling correctly.

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

### Message ID Warning

The `id` field returned by `search_emails` and `get_email` is a **simplified internal ID** (e.g., `"1"`), NOT the RFC 2822 Message-ID header.

**For `mark_email_read` and `move_email`:** Use the simplified `id` directly.

**For `reply_email`:** Requires the actual Message-ID header (with angle brackets). The MCP `id` field is NOT this value. If you don't have the Message-ID header, use `send_email` instead:

```python
# SAFE: Use send_email with clear reply subject
send_email(account="default", to=[sender], subject=f"Re: {subject}", body=...)

# RISKY: reply_email requires actual Message-ID header, not the MCP id
# If you get "Message-ID must be angle-bracketed" error, use send_email instead
```

## Simplified Inbox Handling

The MCP email server provides a clean workflow that eliminates the need for any deduplication tracking:

| Step | Action | Result |
|------|--------|--------|
| 1. Search | `UNSEEN` criteria | Only new/unprocessed messages returned |
| 2. Process | Read and act on each message | Actions taken, reply generated |
| 3. Mark Read | `mark_email_read` | Message gets `\Seen` flag |
| 4. Archive | `move_email` | Message removed from INBOX |

**After processing:** The INBOX only contains unhandled messages. No state tracking, no seen-IDs list, no deduplication logic needed.

**How it works:**
- `UNSEEN` criteria filters out any message with the `\Seen` flag
- `mark_email_read` sets the `\Seen` flag
- `move_email` physically removes the message from INBOX (using RFC 6851 MOVE or COPY+EXPUNGE fallback)
- Result: Next UNSEEN search returns only truly new messages

This is simpler than file-based inbox processing because IMAP flags and folder moves provide built-in state management.

## Workflow

### Step 1: Check for New Emails

```bash
search_emails(account="default", folder="INBOX", criteria="UNSEEN")
```

Use `criteria="UNSEEN"` to get only unread/unprocessed messages. **No deduplication logic is required** — the UNSEEN flag naturally filters out any messages you've already processed. This is the core principle of simplified inbox handling.

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
# Paths are relative to the skill base directory shown in command header
# For c3 plugin:
# - <c3-base> is the parent of skills directory (e.g., /Users/xtof/Workspace/agentic/c3)
# - git-activity-report skill: <c3-base>/skills/git-activity-report/scripts/generate-report.py
# - md-to-html: <c3-base>/bin/md-to-html.py

# For git-activity-report (capture once, use twice)
REPORT_MD=$(<c3-base>/skills/git-activity-report/scripts/generate-report.py --since "midnight" ~/Workspace/agentic/*)
REPORT_HTML=$(echo "$REPORT_MD" | <c3-base>/bin/md-to-html.py)
# Use REPORT_MD for body (plain text) and REPORT_HTML for html_body
```

Use `<c3-base>/bin/md-to-html.py` to convert Markdown to styled HTML. Always provide both:
- `body` — Plain text fallback (use original markdown)
- `html_body` — Styled HTML for email clients

**Efficiency tip:** When generating reports, capture the markdown output once and convert to HTML. Never run the report generator twice.

**Send via:** Use `send_email` (reliable) or `reply_email` (requires actual Message-ID header).

> **Warning:** `reply_email` requires the RFC Message-ID header value (e.g., `<ABC123@mail.example.com>`), NOT the simplified MCP `id` field. If you only have the MCP `id`, use `send_email` instead with subject `"Re: {original_subject}"`.

### Step 6: Mark as Read and Archive

After successful reply:

```bash
# Mark message as read
mark_email_read(account="default", message_id="<id>", folder="INBOX")

# Move to Archive
move_email(account="default", message_id="<id>", source_folder="INBOX", dest_folder="Archive")
```

**Order matters:** Mark as read first, then move. This ensures the message has the `\Seen` flag before archiving.

> **Why both?** Marking as read ensures the message won't appear in future UNSEEN searches. Moving to Archive keeps the INBOX clean. The `move_email` operation removes the message from the source folder (using RFC 6851 MOVE extension if available, or COPY+EXPUNGE fallback), so the INBOX only contains unprocessed messages.

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