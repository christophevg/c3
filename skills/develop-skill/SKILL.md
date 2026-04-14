---
name: develop-skill
description: Guide creation of Claude Code skills. Use when creating a new skill, developing a skill, or when the user says "create a skill", "develop a skill", or "I need a skill that". Follows 6-phase workflow: interview, research check, plan structure, create analysis, create skill files, test.
---

# develop-skill

Guide users through creating Claude Code skills with proper structure, writing style, and testing methodology.

## Overview

| Phase | Purpose |
|-------|---------|
| 1. Interview | Clarify purpose, triggers, content, scope |
| 2. Research Check | Verify research completeness (if applicable) |
| 3. Plan Structure | Decide directory structure and progressive disclosure |
| 4. Create Analysis | Document functional analysis |
| 5. Create Files | Build SKILL.md and bundled resources |
| 6. Test | Symlink and validate |

## When to Use This Skill

Use this skill when:
- User wants to create a new Claude Code skill
- User says "create a skill" or "develop a skill"
- User describes needing a skill for a specific purpose
- User has completed research and wants to create a skill from it

## Phase 1: Interview

Ask clarifying questions to understand the skill:

### Purpose Questions

1. **What does this skill help accomplish?**
2. **When should this skill trigger?** What specific user requests or contexts?
3. **Are there existing skills this relates to or could conflict with?**

Check the KB before creating:
- `kb/patterns/` for related patterns
- `kb/references/` for research
- `.claude/skills/` for existing skills
- `ideas/` for skills in development

### Content Questions

4. **What guidance should the skill provide?** What would a developer need to know?
5. **Should it bundle additional resources?**
   - `patterns/` - Detailed patterns to follow
   - `templates/` - Code templates to use
   - `references/` - Documentation to reference
   - `scripts/` - Executable scripts
   - `assets/` - Static files

6. **Is there existing research to incorporate?** Point to research documents in `research/` folder.

### Scope Questions

7. **What should this skill NOT do?** Boundaries are important.
8. **What decisions should it make vs. ask the user?**
9. **Should it delegate to other skills or agents?**

### Testing Questions

10. **How will you test this skill triggers correctly?**
11. **What scenarios should it handle?**
12. **What edge cases exist?**

## Phase 2: Research Completeness Check

If the skill is based on research in `research/`, verify completeness:

```markdown
## Research Completeness Checklist

- [ ] All cataloged items have detailed documentation
- [ ] No gaps between catalog and documented items
- [ ] All examples are complete and functional
- [ ] Cross-references are valid
- [ ] No "TODO" or placeholder content
```

If research is incomplete, either:
1. Complete the research first, OR
2. Explicitly note gaps in the skill's limitations

## Phase 3: Plan Skill Structure

Decide on the skill's architecture:

### Directory Structure

```
skill-name/
├── SKILL.md           (required - overview + core guidance)
├── patterns/          (optional - detailed patterns)
│   └── *.md
├── templates/         (optional - code templates)
│   └── *.md
├── references/        (optional - detailed docs)
│   └── *.md
├── scripts/           (optional - executable scripts)
│   └── *.sh
└── assets/            (optional - static files)
    └── *
```

### Progressive Disclosure Planning

| Level | Content | Size Target |
|-------|---------|-------------|
| Metadata | name + description in frontmatter | ~100 words |
| Body | SKILL.md main content | <500 lines |
| Bundled | patterns/, templates/, references/ | As needed |

Plan what content goes at each level:
- **Metadata**: Only what's needed for skill discovery
- **Body**: Core guidance, patterns, common issues
- **Bundled**: Detailed references, large examples

### Description Writing

Requirements for the `description` field:
- **Single-line format**: Description must be ONE line. Use inline examples like `Examples: "Example 1", "Example 2"`.
- Use third-person ("This skill guides...")
- Include WHAT and WHEN
- Front-load key use case (descriptions truncated at 250 characters)
- Use specific trigger phrases

Good example:
```yaml
description: Extract text and tables from PDF files. Use when working with PDFs, documents, or when user mentions PDF. Examples: "Extract tables from invoice.pdf", "Read PDF content".
```

Bad example (multi-line - DO NOT USE):
```yaml
description: Extract text from PDFs. Examples:

<example>
user: "Extract from invoice.pdf"
</example>
```

This breaks YAML parsing - the `<example>` blocks are ignored.

## Phase 4: Create Analysis Document

Always create `ideas/{skill-name}/analysis/functional.md`:

```markdown
# {Skill Name} - Functional Analysis

**Date:** YYYY-MM-DD

## Purpose

[One paragraph describing what the skill does and why]

## Scope

### In Scope
- [Guidance task 1]
- [Guidance task 2]

### Out of Scope
- [What the skill should NOT do]

## Triggers

| Trigger Phrase | Context | Expected Activation |
|----------------|---------|---------------------|
| [phrase 1] | [context] | [behavior] |

## Resources

| Resource Type | Purpose | Content |
|---------------|---------|---------|
| patterns/ | [purpose] | [files] |

## Progressive Disclosure

| Content | Level | Location |
|---------|-------|----------|
| [Content 1] | Metadata | frontmatter |
| [Content 2] | Body | SKILL.md |

## Related Skills/Agents

- [skill1] - [relationship]
```

## Phase 5: Create Skill Files

Create the skill directory and files:

### Create Directory Structure

```bash
mkdir -p ideas/{skill-name}/artifacts/skill/{skill-name}/{patterns,templates,references,scripts,assets}
```

Only create directories that will have content.

### SKILL.md Template

```markdown
---
name: {skill-name}
description: {Third-person description. Include WHAT and WHEN. Use when {trigger conditions}.}
---

# {Skill Name}

{2-3 sentence overview of what this skill does}

## Overview

| Capability | Description |
|------------|-------------|
| {Capability 1} | {Description} |
| {Capability 2} | {Description} |

## When to Use This Skill

Use this skill when:
- {Trigger condition 1}
- {Trigger condition 2}

## {Main Section}

{Core guidance content}

## Pattern Files

{If applicable, list pattern files}

- `patterns/{file1}.md` - {Description}

## Common Patterns

### {Pattern 1}

{Description and example}

## Common Issues

| Issue | Solution |
|-------|----------|
| {Issue 1} | {Solution 1} |

## Related Skills

- {skill1} - {relationship}
```

### Writing Style Rules

| Section | Voice |
|---------|-------|
| Frontmatter `description` | Third-person ("This skill...") |
| Body content | Imperative/infinitive ("To accomplish X, do Y") |
| Instructions | Direct commands |

**Keep SKILL.md under 500 lines.** Move detailed content to `references/` or `patterns/`.

### Create idea.md

```markdown
# {skill-name}

## Status

`in-progress`

## Description

{Brief description}

## Tags

`skill` `{tag1}` `{tag2}`

## Created

YYYY-MM-DD
```

### Create TODO.md

```markdown
# {skill-name} TODO

## Tasks

- [x] Create idea.md
- [x] Create analysis/functional.md
- [x] Create SKILL.md
- [ ] Symlink for testing
- [ ] Test skill triggers correctly
- [ ] Update registry
```

## Phase 6: Symlink and Test

### Create Symlink

```bash
ln -sf ideas/{skill-name}/artifacts/skill/{skill-name} .claude/skills/{skill-name}
```

### Test Trigger Conditions

Verify the skill triggers correctly:
1. Test each trigger phrase from the analysis
2. Verify skill activates when expected
3. Verify skill does NOT activate inappropriately

### Test Content

1. **SKILL.md loads** and is well-structured
2. **Progressive disclosure works** - bundled resources load when needed
3. **Writing style is correct** - imperative in body, third-person in description

### Test Guidance

1. Skill provides expected guidance
2. Patterns are clear and applicable
3. Edge cases are handled

### Update Registry

Add to `.claude/REGISTRY.md`:

```markdown
| {skill-name} | incubating | ideas/{skill-name}/artifacts/skill/{skill-name} | — |
```

## Common Mistakes to Avoid

| Mistake | Problem | Fix |
|---------|---------|-----|
| SKILL.md over 500 lines | Context bloat | Move to references/ |
| Vague description | Skill doesn't trigger | Add specific trigger phrases |
| Second-person in description | Discovery problems | Use third-person |
| Everything in one file | No progressive disclosure | Split by domain |
| Deep nesting | Files not read | Keep references one level |
| Windows paths | Errors on Unix | Use forward slashes |
| Multi-line examples in frontmatter | YAML parsing fails | Use inline examples |

**IMPORTANT: YAML Frontmatter Format**

The frontmatter `description` field must be a **single line**. Multi-line content (like `<example>` blocks) breaks YAML parsing:

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

## Related Skills

- develop-agent - Complementary workflow for agent creation
- promote-skill - Copy skill to global C3 after testing
- researcher - For research phase if needed
- functional-analyst - For complex skill analysis