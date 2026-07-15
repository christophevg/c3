---
name: writing-continuity
description: |
  Check that a text holds together: references resolve, concepts are introduced
  before use, themes stay in sync, and sections link rather than jump. Flags
  continuity issues as TODO notes — never writes the missing link. Works across
  multi-part series. Examples: "check continuity across my three parts", "do
  the cross-references resolve?", "find cold terms in this draft".
---

# Writing Continuity

A developmental-level check that the text holds together. This is analysis only: every issue becomes a `TODO:` (author writes the fix) or `TODO PROPOSAL:` (a suggested direction, never the prose). The skill **never writes the missing link itself**.

## When to Use

- The author asks to "check continuity" or "do cross-references resolve?"
- The structural pass of a developmental edit
- Across a multi-part series, to verify cross-part references

## When NOT to Use

- Sentence-level mistakes → `c3:writing-mistakes`
- Voice drift / ChatGPT smell → `c3:writing-voice`
- Claim verification → `c3:writing-review`
- Argumentative craft (buried lede, false balance, non sequiturs) → `c3:writing-mistakes` category 4

## Dimensions

| Dimension | What to check | Flag as |
|-----------|---------------|---------|
| **Reference integrity** | Forward-references ("as I'll show in part 3") and back-references ("as noted above", "the workflow I described earlier") must land on real, written content. | Dangling forward-ref (target still `TODO:`/unwritten, or no target) → `TODO:`; orphaned back-ref (target cut or never existed) → `TODO:` with the dead reference located. |
| **Assumption validity** | Text that leans on prior content ("that same tension", "the approach just outlined") — verify the prior content exists and actually says what's assumed. | Misattributed or missing basis → `TODO:` citing both the claim and the absent/wrong basis. |
| **Concept introduction order** | A term or concept should be introduced before it's used as known. Flag "cold" terms — used as if established, never defined or introduced. | Cold term → `TODO:` to introduce it where first needed, or drop the jargon. |
| **Theme synchronicity** | Recurring themes/motifs should be consistent across the piece; flag themes introduced then abandoned, or referenced inconsistently later. | Dropped or inconsistent theme → `TODO:` with both locations. |
| **Flow & transitions** | Each section should connect to the next by a link, not jump cold. Flag seams with no bridge — but propose the *direction* of the link, never the prose. | Missing transition → `TODO:` ("link X to Y"); optionally `TODO PROPOSAL:` for a one-line direction. |
| **Cross-part continuity** | In a multi-part series, references across parts must resolve: "in part 1 I claimed…" must point at real content in part 1. | Cross-part dangling ref → `TODO:` naming the part and the missing target. |

## Rules

- **Never write the bridge.** A missing transition is flagged, not authored. The link itself is the author's prose.
- **Locate precisely.** Every flag cites the section, paragraph, and (for cross-part) the part number of both the reference and its target.
- **Distinguish "not yet written" from "will never be written."** A forward-ref to a `TODO:` stub is expected — flag it only if the stub is missing. A forward-ref to nothing is a real gap.
- **One issue at a time** for transitions (delayed-feedback principle); batch the inventory only when the author asks for a full continuity sweep.
- **End with "What this did NOT check."** Note what was out of scope (e.g., "did not verify external citations — that is c3:writing-review").

## Local Guardrail

This skill flags only. It never writes prose, never authors a transition or bridge, and never rewrites the author's text. Missing links become `TODO:` notes; a one-line *direction* may be offered as `TODO PROPOSAL:`, never the prose. If invoked standalone, the same rule applies.

## Related Skills

- `c3:writing-review` — claim verification and advisory reports (the broader structural pass)
- `c3:writing-mistakes` — argumentative craft and sentence-level mistakes
- `c3:writing-voice` — voice drift and ChatGPT smell