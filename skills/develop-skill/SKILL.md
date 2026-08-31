---
name: develop-skill
description: |
  Guide creation and refinement of skills. Use when creating, developing, reviewing, improving, or working on skills. Examples: "create a skill for X", "review the pymongo skill", "improve the commit skill", "work on the python skill".
type: workflow
---

# Develop Skill

Guide the creation and refinement of skills — structure, frontmatter,
trigger surface, and validation — against the BLUEPRINT §3 template.

## Triggering

- "create a skill", "develop a skill", "add a new skill"
- "refactor/reorganize skills", or a pattern that should become a skill
- any work on an existing skill's structure or content

# Inputs

The skill concept, its intended trigger surface, and (for refinement) the
existing `skills/<name>/` directory.

## Skill anatomy

```
skill-name/
├── SKILL.md           required — the workflow/knowledge definition
├── patterns/          optional — detailed patterns
├── templates/         optional — code templates
├── references/        optional — deeper docs
├── scripts/           optional — executable helpers
└── assets/            optional — static files
```

SKILL.md frontmatter: `name`, `description` (the trigger surface), and
`type: workflow | knowledge` — knowledge skills may auto-trigger on domain
mention; workflow skills require explicit invocation and must never promise
auto-triggering. Body under 500 lines; more in `references/`, `patterns/`,
`templates/` (progressive disclosure). Only create directories that will
hold content.

Naming: standalone (`commit`), family prefix with sub-skills
(`{prefix}-{name}`), or domain (`python`, `pymongo`). No `-agent` suffix,
no personal names, under ~20 characters.

## New-skill workflow

1. **Interview**: what does it accomplish, when does it trigger, what
   related/conflicting skills exist (check `skills/` and BLUEPRINT §3),
   what stays out of scope, what decisions belong to the owner.
2. **Research completeness** (when research-based): no gaps between
   catalog and documented items, complete examples, valid cross-references,
   no placeholder content — or gaps explicitly noted as limitations.
3. **Plan structure**: what lives in frontmatter (discovery), what in the
   body (core guidance, < 500 lines), what in `patterns/`/`templates/`/
   `references/`/`scripts/`.
4. **Write SKILL.md** per BLUEPRINT §3: frontmatter (`name`,
   `description`, `type`), then `## When` / `## Inputs` / procedure /
   `# Deliverables` / `## Related`. Third-person description; imperative
   body.
5. **Validate**: `make validate` green (frontmatter, type, Related,
   vocabulary, references resolve). Trigger test: activates on the
   intended requests, stays silent otherwise. Session restart loads the
   new skill.

## Refinement workflow (existing skills)

1. **Analyze**: read SKILL.md; line count (>500 → extract); description
   accuracy; pattern classification.
2. **Identify improvements**: what changes — triggers, content, or
   structure; content to relocate (knowledge → knowledge skill, reference
   → the one owning place); description drift.
3. **Implement**: content changes, extractions, description updates;
   proposal to the owner before applying (definitions are live — owners
   read every diff).
4. **Validate**: `make validate` green; trigger test; no shadowing of
   existing skills.
5. **Update the catalog**: extract frontmatter → update the README.md
   skills table (the catalog mirrors `skills/` — source of truth is the
   SKILL.md files); verify AGENTS.md ↔ README links.

## Description writing

The description IS trigger control: single-line or block scalar, explicit
conditions, inline example requests, third person, front-loaded use case.
Details in `references/description-format.md`; pitfalls (vague triggers,
line-count creep, broken YAML) in `references/common-mistakes.md`.

# Deliverables

- A validated SKILL.md (frontmatter with type, precise trigger surface,
  canonical sections), bundled references where needed, validation results.

# Related

- `c3:develop-agent` — the complementary agent-creation workflow
- `c3:researcher` — research phase when the skill needs grounding
- `c3:functional-analyst` — complex-skill analysis
- BLUEPRINT.md §3 — the skill template and trigger-class rules

# Never

- Ship a SKILL.md over 500 lines — extract to references/patterns.
- Multi-line examples in the description body of frontmatter other than a
  proper block scalar.
- Leave a workflow skill wording that promises auto-triggering.