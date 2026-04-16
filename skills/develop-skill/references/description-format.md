# Description Format

Detailed requirements for writing skill descriptions.

## Requirements

The `description` field in skill frontmatter must follow these rules:

1. **Single-line format**: Description must be ONE line
2. **Inline examples**: Format as `Examples: "Example 1", "Example 2"`
3. **Third-person voice**: "This skill guides..." not "You can..."
4. **Include WHAT and WHEN**: What the skill does, when to use it
5. **Front-load key use case**: Descriptions are truncated at 250 characters
6. **Specific trigger phrases**: Help skill discovery

## Good Examples

```yaml
description: Extract text and tables from PDF files. Use when working with PDFs, documents, or when user mentions PDF. Examples: "Extract tables from invoice.pdf", "Read PDF content".
```

```yaml
description: Guide creation and refinement of Claude Code skills. Use when creating a new skill, developing a skill, or when user says "create a skill". Examples: "create a skill for X", "develop a skill".
```

```yaml
description: Systematic bug fixing with TDD approach. Use when fixing bugs, debugging issues, or when user says "fix bug". Examples: "fix the login bug", "there's an issue with auth".
```

## Bad Examples (DO NOT USE)

**Multi-line with newlines:**
```yaml
description: Extract text from PDFs. Examples:

<example>
user: "Extract from invoice.pdf"
</example>
```

This breaks YAML parsing - the `<example>` blocks are ignored.

**Second-person voice:**
```yaml
description: You can use this skill to fix bugs.
```

Should be: "This skill fixes bugs..."

**Missing triggers:**
```yaml
description: A bug fixing skill.
```

Should include: "Use when user says 'fix bug'..."

**Vague timing:**
```yaml
description: Helps with PDFs when needed.
```

Should include: "Use when user mentions PDF or asks to extract from documents"

## YAML Parsing Issue

Multi-line content in frontmatter causes YAML parsing failures:

❌ **Broken format:**
```yaml
---
name: my-skill
description: One-line description. Examples:

<example>
Context: ...
user: "..."
</example>

---
```

The `<example>` blocks are NOT parsed as part of the description - they're treated as unknown YAML keys and ignored.

✅ **Correct format:**
```yaml
---
name: my-skill
description: One-line description. Use when X. Examples: "Example 1", "Example 2".
---
```

## Character Limit

Descriptions are truncated at 250 characters in skill discovery. Front-load the most important information:

**Bad (key info at end):**
```
This skill provides comprehensive guidance for working with the Rich library including tables, panels, progress bars, and when the user mentions rich or console output.
```

**Good (key info at start):**
```
Guide Python Rich library usage for terminal output. Use when user mentions rich, console, or tables. Examples: "add a table", "rich progress bar".
```