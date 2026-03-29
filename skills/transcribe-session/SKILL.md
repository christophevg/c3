---
name: transcribe-session
description: Use this skill when the user asks to "transcribe session", "create transcript", "log conversation", or wants to manually create a curated transcript of the current or recent session.
---

# Transcribe Session

This skill creates a curated transcript of the current session, following the established format in the project.

## When This Skill Applies

This skill activates when the user:
- Runs `/transcribe-session`
- Asks to "transcribe this session"
- Asks to "create a transcript"
- Wants to "log the conversation"
- Mentions "transcript" or "transcription" in the context of saving conversation history

## How to Use

1. **Ask for location**: Always ask where to save the transcript, proposing a filename based on:
   - Today's date: `YYYY-MM-DD`
   - Session name from `/rename` if set, otherwise derive from the first topic discussed
   - Existing transcript files in `conversations/transcripts/` directory

2. **Proposed filename format**: `{date}-{slug}.md`
   - Example: `2026-03-27-conversation-logging-skill.md`

3. **Wait for confirmation**: The user can edit the filename before proceeding.

## Transcript Format

### YAML Frontmatter

```yaml
---
date: ISO-timestamp
slug: session-slug
ideas:
  - related-idea-slug
summary: Brief summary of the session
actions:
  - Key action items from the session
---
```

### Content Structure

Use curated style headers:
- `## User Prompt` / `## Assistant Response` (not `## User` / `## Assistant`)
- `## Research Findings` - For investigation results
- `## Key Decisions` - For decisions made during discussion
- `## Files Modified` - For files changed
- `## Commits Made` - For commits with hashes
- `## Next Steps` - For follow-up actions

### Example Structure

```markdown
---
date: 2026-03-27T10:00:00
slug: my-session-name
ideas:
  - related-idea
summary: Brief summary of what was discussed
actions:
  - Action item 1
  - Action item 2
---

# Transcript

## User Prompt

First user message verbatim

## Assistant Response

Assistant response verbatim

## Research Findings

### Topic A

Details about topic A...

## Key Decisions

- Decision 1: Reasoning
- Decision 2: Reasoning

## Files Modified

- `path/to/file.ext` - Description of changes

## Commits Made

- `abc1234` - Commit message

## Next Steps

- Follow-up action 1
- Follow-up action 2
```

## Process

1. **Gather context**: Review the conversation history
2. **Extract exchanges**: Get verbatim user prompts and assistant responses
3. **Identify session name**: From `/rename` command or first topic
4. **Propose filename**: Ask user to confirm or edit
5. **Create transcript**: Write with proper format
6. **Add synthesis**: Include summary, decisions, files, commits, next steps
7. **Update index**: Add entry to `conversations/index.md`

## Updating the Index

After creating the transcript, ALWAYS update `conversations/index.md`:

1. Read the current index
2. Add a new row with:
   - Date: `YYYY-MM-DD`
   - Slug: Session slug (from filename)
   - Ideas: Related idea slugs (from transcript frontmatter)
   - Summary: Brief description (1 sentence)
   - Actions: Key actions taken (comma-separated list)
3. Format: `| {date} | {slug} | {ideas} | {summary} | {actions} |`

## Notes

- Always use `## User Prompt` / `## Assistant Response` headers (curated style)
- Include tool summaries with arguments (Glob patterns, Read/Edit filenames, Bash descriptions)
- Check for existing transcripts to match style
- For continued sessions, append to existing files
- Extract key information: decisions made, files modified, commits created