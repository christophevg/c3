---
name: develop-skill
description: Guide creation and refinement of Claude Code skills. Use when creating, developing, reviewing, improving, or working on skills. Examples: "create a skill for X", "review the pymongo skill", "improve the commit skill", "work on the python skill".
---

# develop-skill

Guide users through creating and refining Claude Code skills with proper structure, writing style, and validation methodology.

## Overview

| Capability | Description |
|------------|-------------|
| Context detection | Incubator (prototype) vs C3 (operational) |
| New skill workflow | 6-phase development for new skills |
| Refinement workflow | 4-phase streamlining for existing skills |
| Pattern catalog | Dispatcher, domain, workflow, utility patterns |
| Validation | Built-in quality checks throughout |

## When to Use This Skill

Use this skill when:
- User says "create a skill" or "develop a skill"
- User says "add a new skill"
- User says "reorganize skills" or "refactor skills"
- User describes a pattern that should become a skill
- Modifying existing skill structure (refinement)
- User mentions skill development in any context
- Working on skills in any capacity

## Context Detection

Before starting, detect the development context:

| Context | Indicators | Workflow |
|---------|------------|----------|
| **Incubator** | Working in `~/Workspace/agentic/incubator`, creating from scratch | Full 6-phase workflow |
| **C3 Operational** | Working in `~/Workspace/agentic/c3`, refining existing skills | Streamlined refinement workflow |

**C3 Operational context skips:**
- `ideas/{skill}/analysis/functional.md`
- `ideas/{skill}/idea.md`
- `ideas/{skill}/TODO.md`

**C3 Operational context adds:**
- Validation against existing skill patterns
- Progressive disclosure check
- Line count validation
- Immediate symlink testing

## Skill Naming Conventions

Follow these naming patterns for consistency across the skill ecosystem:

| Pattern | Format | Example |
|---------|-------|---------|
| **Standalone** | `skill-name` | `commit`, `naming` |
| **Family prefix** | `{prefix}-{subskill}` | `pa-inbox`, `pa-session`, `pa-outbox` |
| **Domain** | `{domain}` | `python`, `pymongo`, `baseweb` |

**Family Naming:**
- Use a short prefix for related skills (e.g., `pa` for personal assistant)
- Main dispatcher skill gets just the prefix (`pa`)
- Sub-skills get the prefix + descriptor (`pa-inbox`, `pa-outbox`)
- This keeps skills grouped alphabetically in listings

**Avoid:**
- `-agent` suffix (redundant — agents are in agents/ folder)
- Personal names in skill content (use placeholders or reference PERSONAL.md)
- Overly long names (keep under 20 characters)

## Common Skill Patterns

| Pattern | Example | When to Use |
|---------|---------|-------------|
| **Dispatcher** | `/project` → `/project-*` | Multiple related sub-skills |
| **Domain** | `/pymongo`, `/python` | Framework/library expertise |
| **Workflow** | `/bug-fixing`, `/commit` | Multi-step process |
| **Utility** | `/naming`, `/markdown-to-pdf` | Single-purpose tool |

### Dispatcher Pattern

When creating a dispatcher skill:

1. **Define routing table** — Map intent keywords to sub-skills
2. **Sub-skill invocation** — Can be direct OR via dispatcher
3. **Keep dispatcher minimal** — Under 100 lines
4. **Reference sub-skills** — Table with links

Example routing table:
```markdown
| Input Pattern | Routes To | Example |
|---------------|-----------|---------|
| `feature`, `add` | project-feature | `/project feature add auth` |
| `status`, `backlog` | project-status | `/project status` |
| Default | project-manage | `/project` |
```

---

## New Skill Workflow (Incubator)

Full 6-phase workflow for creating skills from scratch.

### Phase 1: Interview

Ask clarifying questions to understand the skill:

**Purpose Questions:**

1. **What does this skill help accomplish?**
2. **When should this skill trigger?** What specific user requests or contexts?
3. **Are there existing skills this relates to or could conflict with?**

Check before creating:
- `kb/patterns/` for related patterns
- `kb/references/` for research
- `.claude/skills/` for existing skills
- `ideas/` for skills in development

**Content Questions:**

4. **What guidance should the skill provide?** What would a developer need to know?
5. **Should it bundle additional resources?**
   - `patterns/` - Detailed patterns to follow
   - `templates/` - Code templates to use
   - `references/` - Documentation to reference
   - `scripts/` - Executable scripts
   - `assets/` - Static files

6. **Is there existing research to incorporate?** Point to research documents in `research/` folder.

**Scope Questions:**

7. **What should this skill NOT do?** Boundaries are important.
8. **What decisions should it make vs. ask the user?**
9. **Should it delegate to other skills or agents?**

**Testing Questions:**

10. **How will you test this skill triggers correctly?**
11. **What scenarios should it handle?**
12. **What edge cases exist?**

### Phase 2: Research Completeness Check

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

### Phase 3: Plan Skill Structure

Decide on the skill's architecture:

**Directory Structure:**

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

**Progressive Disclosure Planning:**

| Level | Content | Size Target |
|-------|---------|-------------|
| Metadata | name + description in frontmatter | ~100 words |
| Body | SKILL.md main content | <500 lines |
| Bundled | patterns/, templates/, references/ | As needed |

Plan what content goes at each level:
- **Metadata**: Only what's needed for skill discovery
- **Body**: Core guidance, patterns, common issues
- **Bundled**: Detailed references, large examples

### Phase 4: Create Analysis Document (Incubator Only)

Create `ideas/{skill-name}/analysis/functional.md`:

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

**Note:** Skip this phase in C3 operational context.

### Phase 5: Create Skill Files

Create the skill directory and files:

**Create Directory Structure:**

```bash
mkdir -p ideas/{skill-name}/artifacts/skill/{skill-name}/{patterns,templates,references,scripts,assets}
```

Only create directories that will have content.

**SKILL.md Template:**

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

**Writing Style Rules:**

| Section | Voice |
|---------|-------|
| Frontmatter `description` | Third-person ("This skill...") |
| Body content | Imperative/infinitive ("To accomplish X, do Y") |
| Instructions | Direct commands |

**Keep SKILL.md under 500 lines.** Move detailed content to `references/` or `patterns/`.

**Create idea.md (Incubator only):**

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

**Create TODO.md (Incubator only):**

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

### Phase 6: Symlink and Test

**Create Symlink:**

```bash
ln -sf ideas/{skill-name}/artifacts/skill/{skill-name} .claude/skills/{skill-name}
```

**Test Trigger Conditions:**

Verify the skill triggers correctly:
1. Test each trigger phrase from the analysis
2. Verify skill activates when expected
3. Verify skill does NOT activate inappropriately

**Test Content:**

1. **SKILL.md loads** and is well-structured
2. **Progressive disclosure works** - bundled resources load when needed
3. **Writing style is correct** - imperative in body, third-person in description

**Test Guidance:**

1. Skill provides expected guidance
2. Patterns are clear and applicable
3. Edge cases are handled

**Update Registry (Incubator only):**

Add to `.claude/REGISTRY.md`:

```markdown
| {skill-name} | incubating | ideas/{skill-name}/artifacts/skill/{skill-name} | — |
```

---

## Refinement Workflow (C3 Operational)

Streamlined 4-phase workflow for refining existing skills.

### Phase R1: Analyze Current State

1. **Read existing SKILL.md**
2. **Check line count** — Flag if >500 lines
3. **Check description format** — Single-line with inline examples?
4. **Check directory structure** — references/ needed?
5. **Identify pattern** — Dispatcher, domain, workflow, utility?

### Phase R2: Identify Improvements

1. **What's changing?** — Trigger conditions, content, or structure
2. **Progressive disclosure needed?** — Should content move to references/?
3. **Any patterns to extract?** — Large sections → reference files
4. **Description accurate?** — Reflects current triggers and purpose

### Phase R3: Implement Changes

1. **Update SKILL.md content**
2. **Create/extract reference files** if needed
3. **Update description** if triggers change
4. **Maintain existing structure** unless restructuring explicitly requested

### Phase R4: Validate

Run validation checklist (see below).

### Phase R5: Update Catalog

After creating or modifying a skill/agent, update the catalog in README.md:

1. **Extract frontmatter** from modified SKILL.md or agent.md
2. **Update README.md** Skills or Agents section
3. **Organize by category** — Project, Domain, Development, Utility
4. **Keep descriptions concise** — From frontmatter description field
5. **Verify cross-references** — CLAUDE.md links to README.md

**Catalog structure in README.md:**

```markdown
## Skills (N)

### Category Name (count)

| Skill | Description |
|-------|-------------|
| `/skill-name` | [description from frontmatter] |
```

**Note:** This ensures the catalog stays in sync with actual skills/agents. The SKILL.md and agent.md files are the source of truth.

---

## Validation Checklist

After creating/modifying any skill, validate:

**Structure:**
- [ ] **Line count** — SKILL.md under 500 lines
- [ ] **Directory structure** — Only needed directories exist
- [ ] **Symlink** — Installed via `make install`

**Description:**
- [ ] **Single-line** — No newlines in description
- [ ] **Inline examples** — Format: `Examples: "ex1", "ex2"`
- [ ] **Third-person** — "This skill..." not "You can..."

**Content:**
- [ ] **Progressive disclosure** — Large content in references/
- [ ] **Writing style** — Imperative in body
- [ ] **Pattern files** — Listed if they exist

**Functionality:**
- [ ] **Trigger test** — Skill activates when expected
- [ ] **No conflicts** — Doesn't shadow existing skills

---

## Description Writing

See `references/description-format.md` for detailed requirements on writing skill descriptions.

**Key requirements:**
- Single-line format with inline examples
- Third-person voice
- Front-load key use case

---

## Common Mistakes

See `references/common-mistakes.md` for common pitfalls and fixes.

**Key pitfalls:**
- SKILL.md over 500 lines
- Vague descriptions
- Multi-line examples in frontmatter (breaks YAML)

---

## Related Skills

- develop-agent - Complementary workflow for agent creation
- researcher - For research phase if needed
- functional-analyst - For complex skill analysis

---

## Reference Files

- `references/description-format.md` — Description writing requirements
- `references/common-mistakes.md` — Common pitfalls and fixes