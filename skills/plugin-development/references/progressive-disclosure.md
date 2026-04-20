# Progressive Disclosure for Skills

**Reference for:** `plugin-development` skill

---

## The Principle

Skills use a three-level loading system to manage context efficiently:

```
┌─────────────────────────────────────────────────────────────┐
│ Level 1: Metadata (always loaded)                          │
│ ~100 words: name + description                              │
│ Determines WHEN to load the skill                          │
├─────────────────────────────────────────────────────────────┤
│ Level 2: SKILL.md body (when triggered)                     │
│ <5,000 words: core instructions                            │
│ WHAT to do once the skill is activated                     │
├─────────────────────────────────────────────────────────────┤
│ Level 3: Bundled resources (as needed)                      │
│ Unlimited: references/, examples/, scripts/                 │
│ Additional context loaded on demand                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Level 1: Metadata (Always Loaded)

### Purpose

Determines when to activate the skill. Must be specific enough to trigger correctly but concise enough to fit in limited context.

### Best Practices

- **Third person format:** "This skill should be used when..."
- **Specific trigger phrases:** Include exact phrases users would say
- **Concrete scenarios:** List specific use cases
- **Target length:** ~100 words

### Examples

#### Good Description

```yaml
---
name: hook-development
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", "validate tool use", "implement prompt-based hooks", "set up event handlers", or mentions hook events (PreToolUse, PostToolUse, Stop). Provides comprehensive hooks API guidance.
---
```

#### Bad Description

```yaml
---
name: hook-development
description: Use this skill when working with hooks.  # Wrong person, vague
---

---
name: hook-development
description: Provides hook guidance.  # No trigger phrases
---

---
name: hook-development
description: This skill helps with hooks, events, automation, triggers, and various related topics.  # Too vague
---
```

---

## Level 2: SKILL.md Body (When Triggered)

### Purpose

Provides core instructions for using the skill. Loaded only when the skill is activated.

### Content Guidelines

| Include | Keep Brief or Move |
|---------|-------------------|
| Core concepts | Detailed API documentation |
| Essential procedures | Comprehensive examples |
| Quick reference tables | Edge cases |
| Pointers to references | Troubleshooting guides |
| Most common use cases | Historical context |

### Target Length

- **Ideal:** 1,500-2,000 words
- **Maximum:** 5,000 words
- **If longer:** Move content to references/

### Structure

```markdown
# Skill Name

Brief overview paragraph.

## Overview

Table of capabilities or key points.

## When to Use

Specific trigger conditions.

## Instructions

Step-by-step guidance for most common cases.

## Additional Resources

### Reference Files

For detailed patterns and techniques:
- **`references/patterns.md`** - Detailed patterns
- **`references/advanced.md`** - Advanced use cases

### Examples

Working examples in `examples/`:
- **`examples/basic.sh`** - Basic usage
```

---

## Level 3: Bundled Resources (As Needed)

### Purpose

Provides unlimited additional context loaded only when Claude determines it's needed.

### Resource Types

#### references/

Documentation and reference material for deeper understanding.

**When to include:**
- Detailed patterns and techniques
- Comprehensive API documentation
- Migration guides
- Edge cases and troubleshooting
- Extended examples with commentary

**Format:** Markdown files, typically 2,000-5,000+ words each

**Best practice:** If files are large (>10k words), include grep search patterns in SKILL.md

#### examples/

Working code examples users can copy and adapt.

**When to include:**
- Complete, runnable scripts
- Configuration files
- Template files
- Real-world usage examples

**Format:** Actual code files (not markdown)

**Best practice:** Include comments explaining key decisions

#### scripts/

Utility scripts for deterministic operations.

**When to include:**
- Validation tools
- Testing helpers
- Parsing utilities
- Automation scripts

**Format:** Executable scripts with documentation

**Best practice:** Should work without modification

---

## Decision Matrix

| Content Type | Level | Location | Size |
|-------------|-------|----------|------|
| Trigger phrases | 1 | SKILL.md frontmatter | ~100 words |
| Core concepts | 2 | SKILL.md body | 1.5-2k words |
| Essential procedures | 2 | SKILL.md body | Part of body |
| Quick reference | 2 | SKILL.md body | Part of body |
| Detailed patterns | 3 | references/*.md | 2-5k words each |
| API documentation | 3 | references/*.md | Unlimited |
| Working examples | 3 | examples/* | Unlimited |
| Utility scripts | 3 | scripts/* | Unlimited |
| Edge cases | 3 | references/*.md | Part of file |

---

## Anti-Patterns

### Anti-Pattern 1: Everything in SKILL.md

❌ **Bad:**
```
skill-name/
└── SKILL.md  (8,000 words - everything in one file)
```

**Why bad:** Bloats context when skill loads, detailed content always loaded.

✅ **Good:**
```
skill-name/
├── SKILL.md  (1,800 words - core essentials)
└── references/
    ├── patterns.md (2,500 words)
    └── advanced.md (3,700 words)
```

**Why good:** Progressive disclosure, detailed content loaded only when needed.

---

### Anti-Pattern 2: Weak Trigger Description

❌ **Bad:**
```yaml
description: Provides guidance for working with hooks.
```

**Why bad:** Vague, no specific trigger phrases, not third person.

✅ **Good:**
```yaml
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", "validate tool use", or mentions hook events. Provides comprehensive hooks API guidance.
```

**Why good:** Third person, specific phrases, concrete scenarios.

---

### Anti-Pattern 3: Missing Resource References

❌ **Bad:**
```markdown
# SKILL.md

[Core content]

[No mention of references/ or examples/]
```

**Why bad:** Claude doesn't know resources exist.

✅ **Good:**
```markdown
# SKILL.md

[Core content]

## Additional Resources

### Reference Files

- **`references/patterns.md`** - Detailed patterns
- **`references/advanced.md`** - Advanced techniques

### Examples

- **`examples/basic.sh`** - Working example
```

**Why good:** Claude knows where to find additional information.

---

## Example Skill Structure

### Minimal Skill

```
skill-name/
└── SKILL.md
```

Good for: Simple knowledge, no complex resources needed.

### Standard Skill (Recommended)

```
skill-name/
├── SKILL.md
├── references/
│   └── detailed-guide.md
└── examples/
    └── working-example.sh
```

Good for: Most plugin skills with detailed documentation.

### Complete Skill

```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── examples/
│   ├── example1.sh
│   └── example2.json
└── scripts/
    └── validate.sh
```

Good for: Complex domains with validation utilities.

---

## Validation Checklist

Before finalizing a skill:

**Level 1 - Metadata:**
- [ ] Frontmatter has `name` and `description` fields
- [ ] Description uses third person ("This skill should be used when...")
- [ ] Includes specific trigger phrases users would say
- [ ] Lists concrete scenarios
- [ ] Not vague or generic
- [ ] Target ~100 words

**Level 2 - SKILL.md Body:**
- [ ] Uses imperative/infinitive form
- [ ] Focuses on core concepts and procedures
- [ ] Target 1,500-2,000 words (max 5,000)
- [ ] References supporting files clearly
- [ ] No duplicated content from references

**Level 3 - Resources:**
- [ ] Detailed content in references/
- [ ] Working examples in examples/
- [ ] Utility scripts in scripts/
- [ ] All referenced files actually exist
- [ ] Examples are complete and correct