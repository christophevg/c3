---
name: writing-order
description: |
  Help reorder raw material (written sections + TODO stubs) into a smooth
  argument flow. Maps section roles, interviews the author for the main
  message and arc, proposes a reordering with rationale, iterates on
  feedback, and applies section moves only — never writes or rewrites
  content. Examples: "the material isn't in the right order", "help me
  structure this draft", "the flow doesn't work".
---

# Writing Order

Help the author reorder sections of a draft into a smooth argument flow. The sections are the author's content (written prose and TODO stubs) — this skill only proposes and applies reordering. Never writes, rewrites, or fills content.

## When to Use

- The author says "the material isn't in the right order" or "the flow doesn't work"
- A draft has multiple sections (mix of written prose and TODO stubs) and the structure feels wrong
- The author wants to find the argument arc before writing the TODO sections

## When NOT to Use

- Developmental review (claims, gaps, perspectives) → `c3:writing-review`
- Continuity within an existing order (dangling refs, cold terms, transitions) → `c3:writing-continuity`
- Splitting long-form into social posts → `c3:writing-split`
- Voice drift or ChatGPT smell → `c3:writing-voice`
- Sentence-level mistakes → `c3:writing-mistakes`

## Process

| Step | Detail |
|------|--------|
| 1. Map current structure | Read the draft. Annotate each section with its *role* in the argument (primer, evidence, framework, caveat, synthesis, etc.). Present the annotated map to the author. |
| 2. Interview for the arc | Ask one question at a time: what is the main message? what should the reader walk away with? Build the arc from the author's answer — the dominant takeaway determines what order the sections should follow. |
| 3. Propose reordering | Map existing sections onto the arc. Present the proposed order as persistent text in the conversation — NOT inside an `AskUserQuestion` modal. The author needs to refer back to it while giving feedback. |
| 4. Iterate | The author refines. Adjust the proposal. Repeat until the author is satisfied. |
| 5. Apply | Move sections only. No content changes, no rewriting, no prose generation. Every word of written prose and every TODO stub stays exactly as it was — only the order changes. |

## Practices

| Practice | Detail |
|----------|--------|
| Role-annotate each section | Label what function each section plays in the argument (primer, evidence, caveat, synthesis, etc.) so the author can see *why* a section belongs where it does. |
| One question at a time | Never batch questions. Ask for the main message, wait, then drill into specifics if needed. |
| Present as persistent text | Propose the reordering as a text diagram or table in the conversation body, not inside a tool modal. The author needs to see it while composing feedback. |
| Arc before order | Find the argument arc first (setup → evidence → abstraction → formalization → synthesis → messages), then map sections onto it. The arc is the author's; the sections are the material. |
| Moves only | When applying, move entire sections verbatim. Never split a section, never merge sections, never edit content within a section. |
| Respect unwritten sections | TODO stubs are sections too. They have a role in the arc and must be ordered alongside written sections. |

## Rules

- **Never write or rewrite content.** Pure section reordering. No prose, no rewrites, no filling blanks.
- **The arc is the author's.** You interview to find it; you never impose one. The author decides what the main message is and what order builds toward it.
- **Present proposals as persistent text.** Never use `AskUserQuestion` for the proposed order — the author needs to refer back to it during iteration. Use `AskUserQuestion` only for discrete choice points within the iteration.
- **Apply moves only.** When writing the reordered file, every section's content is preserved verbatim. Only the sequence changes.
- **No continuity pass after reordering.** Reordering may create new transition gaps between now-adjacent sections. Flag this as a `TODO:` for the author, or recommend a `c3:writing-continuity` pass — but do not write the transitions.
- **End with "What this did NOT check."** Note that no continuity, voice, or mistakes pass was run on the reordered result.

## Local Guardrail

This skill proposes and applies section reordering only. It never writes prose, never rewrites the author's text, never fills TODO stubs, and never edits content within a section. If invoked standalone, the same rule applies.

## Related Skills

- `c3:writing-review` — developmental review of the content within each section
- `c3:writing-continuity` — check transitions and references after reordering
- `c3:writing-voice` — voice pass after structure is settled
- `c3:writing-split` — split long-form into social posts (break apart, not reorder)