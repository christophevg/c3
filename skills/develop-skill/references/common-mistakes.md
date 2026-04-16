# Common Mistakes to Avoid

When creating or refining skills, avoid these common pitfalls.

## Structure Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| SKILL.md over 500 lines | Context bloat, slow loading | Move detailed content to references/ |
| Everything in one file | No progressive disclosure | Split by domain/topic |
| Deep nesting | Files not read | Keep references one level deep |
| Empty directories | Wasted structure | Only create needed directories |

## Description Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Vague description | Skill doesn't trigger | Add specific trigger phrases |
| Second-person voice | Discovery problems | Use third-person: "This skill..." |
| Multi-line examples | YAML parsing fails | Use inline: `Examples: "ex1", "ex2"` |
| Missing triggers | Skill not discovered | Add "Use when..." with trigger phrases |
| Key info at end | Truncated before visible | Front-load key use case |

## Content Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| No progressive disclosure | Large context consumption | Extract to references/, patterns/ |
| Wrong voice in body | Inconsistent tone | Use imperative: "To do X, do Y" |
| Missing validation step | Quality issues | Add validation checklist |
| No related skills | Isolated guidance | Link to complementary skills |

## Path Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Windows paths (`\`) | Errors on Unix | Use forward slashes (`/`) |
| Absolute paths | Not portable | Use relative paths where possible |
| Spaces in filenames | Shell issues | Use hyphens: `skill-name.md` |

## Workflow Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Skipping validation | Quality issues | Always run validation checklist |
| Wrong context workflow | Unnecessary overhead | Detect incubator vs C3 context |
| Not testing triggers | Skill doesn't activate | Test with trigger phrases |
| Forgetting symlink | Skill not installed | Run `make install` after changes |

## YAML Frontmatter Format

The frontmatter `description` field must be a **single line**:

✅ **Correct format:**
```yaml
---
name: my-skill
description: One-line description. Use when X. Examples: "Example 1", "Example 2".
---
```

❌ **Broken format (DO NOT USE):**
```yaml
---
description: One-line description. Examples:

<example>
Context: ...
user: "..."
</example>

---
```

The `<example>` blocks are NOT parsed as part of the description - they're treated as unknown YAML keys and ignored.

## Validation Checklist

Always validate after creating/modifying skills:

**Structure:**
- [ ] Line count under 500
- [ ] Only needed directories exist
- [ ] Symlink installed

**Description:**
- [ ] Single-line, no newlines
- [ ] Inline examples format
- [ ] Third-person voice

**Content:**
- [ ] Progressive disclosure used
- [ ] Imperative voice in body
- [ ] Pattern files listed

**Functionality:**
- [ ] Triggers correctly
- [ ] No conflicts with existing skills