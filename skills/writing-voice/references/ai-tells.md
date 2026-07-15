# AI-Tell Vocabulary ("ChatGPT Smell")

Reference list of vocabulary and phrasing typical of LLM-generated prose. The `writing-voice` skill flags these when they appear in the author's draft, citing the exact entry. The author's own corpus (per `~/VOICE.md`) is the arbiter — a word the author genuinely uses is not a tell.

## Single-word tells

| Word | Note |
|------|------|
| delve | "Let's delve into…" — the canonical AI tell |
| intricate | generic complexity marker |
| tapestry | "a rich tapestry of…" |
| realm | "in the realm of…" |
| palpable | overused intensifier |
| embark | "embark on a journey…" |
| underscore | "this underscores…" |
| landscape | "the evolving landscape of…" |
| testament | "stands as a testament…" |
| pivotal / vital / crucial | significance inflation |
| vibrant / rich / profound | generic praise, flat affect |
| showcase / exemplify / boast | promotional register |
| nestled | ad-like placement |
| groundbreaking / renowned | promotional inflation |
| multifaceted / nuanced | complexity signaling without substance |
| garner | "garnered attention" |
| fosters / cultivates | vague causal verbs |
| navigate | "navigating the complexities of…" |

## Phrase tells

- "It is important to note that…"
- "It's worth considering that…"
- "It is essential to recognize…"
- "In today's fast-paced world…"
- "In the ever-evolving landscape of…"
- "plays a crucial role in shaping"
- "stands as / serves as a testament"
- "setting the stage for"
- "leaves an indelible mark"
- "deeply rooted in"
- "at the forefront of"
- "a testament to"

## Overuse patterns (density, not lone use)

- "moreover" / "furthermore" / "additionally" stacked across a section
- "ultimately" / "overall" / "essentially" / "practically" as hedging tic
- Rule-of-three adjective triples: "rich, vibrant, and profound"
- Forced balance: "not just X, but also Y"; "On one hand… on the other hand…" as a reflex
- Summarize-and-recap: "In conclusion…", "In summary…", section-end recaps
- Moralizing closings: "it's essential for parents, educators, and policymakers to…"

## Structural tells (flag lightly, only when they harm clarity)

- Em-dash overuse (density signal — 2026 data: ~18.5% of AI inputs vs ~7.1% humanized)
- Inline-header vertical lists everywhere (bold header + colon + description)
- Mechanical boldface of every key term
- Thematic breaks (`---`) before every heading
- Listmania — every point becomes a bulleted list

## Note on density

Individual phrases aren't the problem — density is. One "furthermore" is natural; four or five hedge/transition/recap phrases in a 500-word section is a fingerprint. Flag clusters, not lone uses. The structural/pattern AI tells (hedging stacks, recap closings, listmania, forced symmetry) overlap with `c3:writing-mistakes` category 5 — that skill owns the *patterns*; this reference owns the *vocabulary*.