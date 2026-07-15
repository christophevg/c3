---
name: writing-idioms
description: |
  Flag misused, misquoted, mixed, or non-idiomatic idioms and proverbs in a draft
  and propose the canonical form as a TODO PROPOSAL. A sanctioned exception to the
  no-prose rule: idioms have canonical forms, so providing the correct one is a
  factual correction, not authoring prose. Examples: "check my idioms", "is this
  proverb used correctly?", "suggest a better proverb for this".
---

# Writing Idioms

Assist a non-native English speaker who loves idiomatic and proverbial expressions. This is the **one sanctioned exception** to the no-prose rule, and it is narrowly bounded: idioms and proverbs have canonical forms, so providing the correct one is a factual correction (the idiom *is* X), not authoring new prose. The skill proposes known phrases; it does not invent text, and it does not rewrite the surrounding sentence.

## When to Use

- The author asks to "check my idioms" or "is this proverb right?"
- Proactively during any read of the draft — hunt for misused/misquoted/mixed idioms
- The author wants a more fitting or vivid proverb for an intent

## When NOT to Use

- Eggcorns, malapropisms, redundancies, non-native grammar errors → `c3:writing-mistakes` (those are CANONICAL mistakes flagged as `TODO:` with the recognized form; idioms specifically propose the phrase as `TODO PROPOSAL:`)
- Voice drift → `c3:writing-voice`
- Continuity → `c3:writing-continuity`

## Functions

| Function | What the skill does |
|----------|---------------------|
| **Flag misuse** | During any read of the draft, flag idioms/proverbs that are misused, misquoted, mixed, or non-idiomatic. |
| **Provide the canonical form** | Give the correct idiom/proverb as `TODO PROPOSAL:`, with the meaning and a brief note on why the author's version is off. |
| **Suggest better proverbs** | Where the author's intent could be expressed more vividly, propose a more fitting proverb as `TODO PROPOSAL:` — never imposed. |
| **Explain when helpful** | A brief origin/meaning note when it aids the author's choice. |
| **Bounded** | Proposes only the idiom/proverb phrase itself. Does not rewrite the surrounding sentence. |

## Rules

- **Always `TODO PROPOSAL:`** — the author accepts or rejects. Never edit the author's text directly.
- **Hunt proactively** during every review; also invokable directly ("check my idioms").
- **When unsure, ask.** If it is unclear whether something is a misuse or a deliberate creative choice, ask rather than assert.
- **Respect the voice profile.** If an idiom is consistently absent from the author's corpus by habit, treat it as a style note, not an error. Conversely, the author's characteristic use of certain proverbs should be preserved, not "corrected" away.
- **Verify obscure cases.** For uncommon or disputed proverbs, delegate to `c3:researcher` (via the agent) to confirm the canonical form and origin before proposing.
- **Never impose.** The author loves these expressions but chooses each one. A proposal is a gift, not a fix.

## Local Guardrail

This skill proposes the canonical form of idioms/proverbs only, as `TODO PROPOSAL:` for the author to accept or reject. It never edits the author's text directly, never invents new phrases, and never rewrites the surrounding sentence. If invoked standalone, the same rule applies.

## Related Skills

- `c3:writing-mistakes` — eggcorns, malapropisms, and other canonical-form errors (flagged as `TODO:` with the recognized form)
- `c3:writing-voice` — voice drift and ChatGPT smell
- `c3:researcher` — verify obscure/disputed proverb origins