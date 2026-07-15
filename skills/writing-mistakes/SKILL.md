---
name: writing-mistakes
description: |
  Flag common writing mistakes in a draft as TODO notes for the author to fix.
  Distinguishes CANONICAL errors (a correct form exists — eggcorns, redundancies,
  non-native-English errors, comma splices) from CRAFT patterns (passive overuse,
  throat-clearing, AI-tell density). Never rewrites the author's prose. Examples:
  "check my writing for common mistakes", "flag writing mistakes in this draft",
  "check for eggcorns and redundancies".
---

# Writing Mistakes

Scan a draft for recurring writing mistakes and flag each as a `TODO:` note for the author to fix. This is flagging, never fixing: name the issue and, for canonical forms, the recognized-correct form as a fact — but never rewrite the author's sentence. A canonical form is a fact, not prose.

## When to Use

- The author asks to "check my writing" or "flag writing mistakes"
- During a developmental-editing pass over a draft
- Proactively during any read, when a mistake is conspicuous

## When NOT to Use

- Idiom or proverb misuse → use `c3:writing-idioms` (canonical form as `TODO PROPOSAL:`)
- "ChatGPT smell" *vocabulary* (delve, tapestry, intricate…) → use `c3:writing-voice`
- Continuity / dangling references → use `c3:writing-continuity`
- Claim verification → use `c3:writing-review`
- Pure mechanics (serial commas, possessives, hyphenation) → out of scope; do not flag

## Two Flag Types

| Type | Meaning | Flag format |
|------|---------|-------------|
| **CANONICAL** | A correct form exists as a fact | `TODO: <error type> at <location> — recognized form is X` |
| **CRAFT** | A judgment call; no single correct form | `TODO: <pattern name> at <location> — consider whether this is intended` |

For CANONICAL items, cite the recognized form *in the `TODO:` note* — do not insert it into the draft. The author applies it.

## Categories

Representative examples below; the full per-category catalog with sources is in `references/mistakes-taxonomy.md`. Read it before a deep mistake sweep.

| Category | Representative examples | Type |
|----------|--------------------------|------|
| Eggcorns & malapropisms | "mute point"→moot, "for all intensive purposes"→intents and purposes, "escape goat"→scapegoat, "tow the line"→toe, "could care less"→couldn't | CANONICAL |
| Pleonasms / redundancies | "free gift", "end result", "past history", "added bonus", "true facts" | CANONICAL |
| Non-native English errors | article misuse ("we developed method"), prepositions ("interested on"→in), countable/uncountable ("informations", "advices"), false friends ("actual"≠current), gerund/infinitive ("enjoy to eat"→eating), collocation ("make research"→do), tense/aspect | CANONICAL |
| Misused words (Strunk) | "less/fewer", "literally" for "almost", "due to" for "because of", "claim" for "declare", "while" for "although" | CANONICAL |
| Clarity-harming mechanics | comma splice, run-on, "however splice", ambiguous pronoun reference (orphan "this"), sentence fragment | CANONICAL |
| Passive voice & nominalizations | "mistakes were made"; "conduct an investigation" (zombie nouns) | CRAFT |
| Wordiness / verbal false limbs | "due to the fact that"→because, "in order to"→to, "has the ability to"→can | CRAFT |
| Weak verbs & adverb overuse | "make a decision" (decide); "ran quickly", "completely destroyed" | CRAFT |
| Vague quantifiers & weasel words | "many", "a number of"; "actually", "basically", "really", "very", "essentially" | CRAFT |
| Overclaiming / absolutes | "always", "never", "the only way", "proves that", "completely eliminates" | CRAFT |
| Clichés / dying & mixed metaphors | worn figures used unthinkingly; clashing images | CRAFT |
| Structural craft | throat-clearing openings, buried lede, topic-sentence drift, unsupported generalizations, false balance, non sequiturs, circular reasoning, empty recap closings, curse of knowledge | CRAFT |
| AI/LLM tells (density, not lone use) | hedging stacks, summarize-and-recap, moralizing closings, generic examples, listmania, forced symmetry, rule-of-three triples, significance inflation ("plays a crucial role"), flat "Wikipedia voice", em-dash overuse | CRAFT |

## Rules

- **Never rewrite the sentence.** Even for CANONICAL items, name the recognized form in the `TODO:` note; do not insert it into the draft. The author applies it.
- **Density over lone use for AI tells.** One "furthermore" is natural; flag only when a pattern repeats enough to be a fingerprint.
- **Do not flag pure mechanics.** Serial commas, possessives, hyphenation style — out of scope. Only the clarity-harming subset above.
- **Proportionality.** Lead with clarity-harming CANONICAL errors and structural CRAFT issues; style-level CRAFT (adverbs, weasel words) is lower priority. Never flood the author.
- **Respect the voice profile.** A pattern the author uses deliberately and consistently (per `~/VOICE.md`) is a style choice, not a mistake — do not flag it.
- **Verify obscure canonical cases.** For disputed word uses or etymology, delegate to `c3:researcher` (via the agent) before asserting the recognized form.
- **Locate precisely.** Cite section and paragraph (and part number, in a multi-part series) for every flag.
- **One issue at a time** unless the author asks for a full mistake sweep.
- **End with "What this did NOT check."** Note what was out of scope (e.g., "did not verify external citations — that is c3:writing-review").

## Local Guardrail

This skill flags only. It never writes prose, never rewrites the author's sentence, and never inserts a correction into the draft. CANONICAL forms are cited as facts in `TODO:` notes for the author to accept and apply. If invoked standalone (not through the writing-assistant agent), the same rule applies.

## Reference Files

- `references/mistakes-taxonomy.md` — the full per-category catalog (5-12 examples each) with consolidated sources. Read it before a deep sweep.

## Related Skills

- `c3:writing-idioms` — idiom/proverb misuse (canonical form as `TODO PROPOSAL:`)
- `c3:writing-voice` — "ChatGPT smell" vocabulary and voice drift
- `c3:writing-continuity` — dangling references, cold terms, missing transitions
- `c3:writing-review` — claim verification and advisory reports