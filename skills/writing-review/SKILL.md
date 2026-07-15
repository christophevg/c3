---
name: writing-review
description: |
  Developmental-editing review methodology: extract and classify claims, verify
  factual claims against authoritative sources, analyze gaps and perspectives,
  handle the author's opinions, and produce a structured advisory report. Every
  recommendation becomes a TODO or TODO PROPOSAL — never prose. Examples:
  "review this draft", "verify the claims in my article", "produce an advisory
  report on part 1".
---

# Writing Review

The analytical engine for developmental editing and research validation. Extracted and adapted from the `writing-reviewer` incubator effort, with all "rewrites" converted to `TODO PROPOSAL:` and all "suggestions" to `TODO:`. **Every recommendation becomes a marker — never prose.**

## When to Use

- The author requests a review or advisory report
- Verifying factual claims in a draft
- Analyzing coverage gaps and missing perspectives
- Framing research findings (paired with `c3:researcher`)

## When NOT to Use

- Continuity / dangling references → `c3:writing-continuity`
- Sentence-level mistakes → `c3:writing-mistakes`
- Voice drift → `c3:writing-voice`
- Idiom misuse → `c3:writing-idioms`

## Claim Extraction & Classification

From a draft, extract explicit and implicit claims and classify them:

| Type | Treatment |
|------|-----------|
| **Factual** | Verify against authoritative sources (min 2, cross-validated). |
| **Opinion** | Validate framing — is it mainstream / controversial / fringe? Flag if presented as fact. |
| **Prediction** | Surface assumptions and prior art. Note uncertainty. |
| **Definition** | Check consistency with established usage and the author's own prior definitions. |

Only flag claims at high confidence. Marginal or uncertain extractions are ignored to reduce noise.

## Verification Standards

| Element | Standard |
|---------|---------|
| Cross-validation | Minimum 2 independent sources for factual claims, preferably from different organizations. |
| Source hierarchy | Primary > Official > Secondary > Expert commentary > Tertiary (use with caution). |
| Discrepancies | Note when sources conflict; surface the conflict, do not resolve it for the author. |
| Unverifiable | Mark as unverifiable with the reason. Suggest how to present it (as opinion, as assumption) — as `TODO:`. |
| Currency | Prefer recent sources for fast-moving topics; note source dates. |

Research itself is delegated to `c3:researcher` (via the agent). This skill frames the questions and interprets the findings; it never searches the web directly.

## Gap Analysis

| Dimension | What to look for |
|-----------|------------------|
| **Topic depth** | Surface mention vs. substantive coverage. Flag shallow treatment. |
| **Missing perspectives** | Counterarguments and alternative viewpoints not represented. |
| **Missing prerequisites** | What the reader needs to understand but is not provided. |
| **Related topics** | What a reader would expect that is absent. |
| **Coverage balance** | Whether related topics are covered proportionately. |

## Perspective Analysis

Identify the main viewpoints presented, the viewpoints not covered, the balance of coverage, and the counterarguments the author should address. This feeds the steelman responsibility (build the strongest opposition to each major argument; present it; let the author defeat or accept it).

## Opinion Handling

The author holds strong opinions. Treat them with care:

- Validate the framing — do notable sources share or disagree?
- Determine whether the opinion is mainstream, controversial, or fringe.
- Flag any opinion presented as fact.
- Never debate the opinion's correctness. Challenge its framing, evidence, and presentation only.

## Advisory Report Structure

When the author requests a review, produce a structured advisory report. **Every recommendation becomes a `TODO:` or `TODO PROPOSAL:` — never prose.**

```
Review Report: {Title}
├── Executive summary (2-3 sentences)
├── Critical issues          → TODO: per issue, with location + evidence
├── Recommended improvements → TODO: per issue, with location + rationale
├── Coverage analysis        → table of topics × depth; missing topics as TODO:
├── Claim verification       → verified / disputed / unverifiable, with sources
├── Perspective analysis     → missing viewpoints as TODO: for the author
├── Voice drift candidates   → TODO: citing exact profile rules (→ c3:writing-voice)
├── Optional enhancements    → TODO PROPOSAL: for the author to consider
└── What this did NOT check  → explicit scope limits
```

Artifacts (when the author wants them persisted): `CLAIMS.md`, `GAPS.md`, `REVIEW.md`, plus the researcher's `SOURCES.md` and `fetched/` — all relative to the artifact root folder (default: current working directory, or a folder the author names).

## Rules

- **Never prose.** Every recommendation is a `TODO:` or `TODO PROPOSAL:`. Never a rewrite, never a "starting point."
- **Surface, do not conclude.** Return findings, contradictions, and tradeoffs. The author decides what they mean.
- **Proportionality.** Critical (factual/structural errors) → recommended improvements → optional enhancements → voice notes. Never lead with style.
- **Link to locations.** Pinpoint section and paragraph for every finding.
- **End with "What this did NOT check."** Every report ends with its scope limits.

## Local Guardrail

This skill produces analysis and `TODO:`/`TODO PROPOSAL:` markers only. It never writes prose, never rewrites the author's text, and never draws conclusions for the author. If invoked standalone, the same rule applies.

## Related Skills

- `c3:researcher` — performs the actual research and source verification
- `c3:writing-continuity` — structural continuity (often run alongside a review)
- `c3:writing-voice` — voice drift candidates cited in the report
- `c3:writing-mistakes` — sentence-level and craft mistakes