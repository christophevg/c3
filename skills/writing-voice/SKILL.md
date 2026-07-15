---
name: writing-voice
description: |
  Check a draft against the author's voice profile and flag drift, including
  "ChatGPT smell" vocabulary. The profile is a measurement instrument, never a
  generation template — the skill flags drift as TODO notes, never rewrites.
  Examples: "check this draft against my voice", "flag ChatGPT smell in my
  draft", "do a voice drift check".
---

# Writing Voice

Preserve the author's voice. The voice profile is a **measurement instrument, not a generation template** — it describes the author; it is never used to generate prose "in the author's voice." Drift is flagged as `TODO:` notes; the author rewrites.

## When to Use

- The author asks to "check my voice" or "flag ChatGPT smell"
- The voice pass of a developmental edit (after the structural pass is settled)
- A quarterly drift check against recently published posts

## When NOT to Use

- Sentence-level mistake flagging (eggcorns, redundancies, non-native errors) → `c3:writing-mistakes`
- AI-tell *patterns/density* (hedging stacks, recap closings, listmania) → `c3:writing-mistakes` category 5
- Idiom/proverb misuse → `c3:writing-idioms`
- Structural/continuity issues → `c3:writing-continuity`

## The Voice Profile

| Setting | Behavior |
|---------|----------|
| **Default location** | `VOICE.md` in the user's home directory. **Read the file directly** at the path `$HOME/VOICE.md` using the `Read` tool — do not use `Glob` to search for it (the path is known, not something to discover). If `Read` fails or the file is absent, **skip voice checks and tell the author** — do not assume a profile or substitute another. |
| **Configurable** | The author may name a specific profile path in the prompt; that overrides the default. |
| **Read-only** | Never edit the profile. The author owns it. |

## Rules

1. **Cite the exact rule.** Every voice concern references the specific profile entry it draws from (e.g., "AI-Warning Patterns: 'delve' not found in your corpus — you used it twice in §3").
2. **Flag drift, never fix it.** Surface drift candidates as `TODO:` notes. Do not rewrite the offending passage.
3. **Quarterly drift check.** Re-read the author's most recent published posts; surface "candidate drift" patterns as `TODO PROPOSAL:` for the author to consider updating the profile. Never edit the profile.
4. **Flag "ChatGPT smell."** Call out AI-typical vocabulary by name — see `references/ai-tells.md` for the list (delve, intricate, tapestry, realm, palpable, embark, underscore, "it is important to note", moreover/furthermore overuse, passive voice, nominalizations).
5. **Never generate "in the author's voice."** The profile describes the author; it is not a template to fill. Using it to produce prose would violate the core rule.
6. **Density over lone use.** One "furthermore" is natural; flag only when AI-tell vocabulary clusters.
7. **Respect deliberate choices.** A word the author genuinely and consistently uses (per the profile) is not a tell — do not flag it.
8. **Future skill delegation.** A mature `style-profile` checking skill (incubator Phase 2) can be delegated to once it matures. Until then, apply the profile rules directly.

## Local Guardrail

This skill flags only. It never writes prose, never rewrites the author's text, and never uses the profile to generate "in the author's voice." Drift and ChatGPT-smell hits become `TODO:` / `TODO PROPOSAL:` notes for the author. If invoked standalone, the same rule applies.

## Reference Files

- `references/ai-tells.md` — the ChatGPT-smell vocabulary and phrase list, with the density rule.

## Related Skills

- `c3:writing-mistakes` — AI-tell *patterns/density* and other common writing mistakes
- `c3:writing-idioms` — idiom/proverb misuse
- `c3:writing-continuity` — structural and continuity checks