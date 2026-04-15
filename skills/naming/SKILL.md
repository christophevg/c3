---
name: naming
description: Guides the process of choosing a name for a project, product, agent, or entity — from trait identification through research to shortlisting and decision.
triggers:
  - name
  - naming
  - choose a name
  - pick a name
  - name for
---

# Naming Skill

Guides the process of choosing a name for a project, product, agent, or entity — from trait identification through research to shortlisting and decision.

## When to Use

- User asks to "name" something
- User asks to "choose a name" or "pick a name"
- User wants to name a new agent, project, feature, product, or entity
- User wants to evaluate name candidates

## Workflow

### Phase 1: Trait Identification

1. **Ask what is being named**: Project, product, agent, feature, or other entity
2. **Gather trait requirements**: What qualities should the name embody? Ask the user for:
   - Core traits (3-5 minimum)
   - The relationship the name should convey (e.g., "trusted advisor", "steady companion", "creative partner")
   - Any constraints (cultural, linguistic, length, pronunciation)
3. **Expand traits with research**: Use the researcher agent to identify additional traits from domain experts, literature, or precedent. For a personal assistant, research what makes an outstanding PA. For a product, research what names resonate in that market.
4. **Organize traits into clusters**: Group related traits together (e.g., Trust & Faithfulness, Warmth & Friendship, Wisdom & Judgment). Each cluster should have a core feeling statement.

### Phase 2: Name Research

1. **Use the researcher agent** to find names that embody the identified trait clusters. Instruct the researcher to:
   - Cover multiple cultural traditions (Greek, Latin, Nordic, Sanskrit, Celtic, etc.)
   - Provide thorough etymological research for each candidate (not just surface meanings)
   - Include at least 10-15 candidates with trait alignment, cultural depth, and practical considerations
   - Check for AI association/slop issues (has the name become a default AI-generated name?)
   - Include a near-miss tier alongside top recommendations
2. **Require provenance**: Every name must have documented etymological sources, not just popular name-site claims

### Phase 3: Shortlisting

1. **Produce a shortlist of 3-5 names** with detailed reasoning for each:
   - Etymological meaning and cultural depth
   - Which trait clusters it embodies and how
   - Historical bearers (real people who embodied the traits)
   - Practical considerations (pronunciation, international use, nickname potential)
   - Potential drawbacks (negative associations, popularity, AI connections)
2. **Include a near-miss tier** of 2-3 candidates that ranked just below the cutoff
3. **Create a comparison table** showing how each name maps to trait clusters

### Phase 4: Deep Dives

1. If the user asks about a specific name not on the shortlist, or wants deeper analysis on a shortlisted name, **use the researcher agent** for a deep dive
2. Deep dives should cover:
   - Full etymological and linguistic analysis (with scholarly sources, not just popular sites)
   - Mythological, historical, and cultural significance
   - Historical bearers and what they embodied
   - International pronounceability and name perception data
   - AI association check (has the name become an AI default?)
   - Honest assessment of potential drawbacks
3. **If a name is ruled out, document why explicitly** — don't just drop it

### Phase 5: Decision

1. Present the final shortlist with clear differentiation (each name represents a different vision of the relationship)
2. Help the user evaluate trade-offs: depth vs. practicality, distinctiveness vs. accessibility, meaning vs. sound
3. Support the user's final choice without pushing a preference

## Key Principles

- **Meaning over sound**: A name should carry real etymological meaning that maps to the entity's purpose, not just sound pleasant
- **Honesty over flattery**: If a popular meaning is folk etymology, say so. If a mythology is dark, say so. If a name is AI slop, say so.
- **Completeness**: Every search must be accounted for in SOURCES.md. Never silently drop research.
- **Near-miss tiers**: Always include candidates that ranked just below the shortlist so users can make their own trade-offs.
- **Practical depth balance**: Consider both philosophical depth AND daily-use practicality. A 4-syllable name with profound meaning may be less usable than a 2-syllable name with slightly less depth.

## Output Location

Store all research and shortlists in the relevant idea folder:

```
ideas/{idea-slug}/
├── shortlist.md          # Current shortlist with comparisons
└── research references in project research/ folder
```

## Checklist

Before finalizing a shortlist:
- [ ] Traits identified and organized into clusters
- [ ] Research covers multiple cultural traditions
- [ ] Each name has documented etymological sources (not just popular sites)
- [ ] AI association check performed for each candidate
- [ ] Practical considerations addressed (pronunciation, nicknames, international use)
- [ ] Drawbacks honestly assessed for each candidate
- [ ] Near-miss tier included
- [ ] Comparison table maps names to trait clusters
- [ ] All research documented with provenance in SOURCES.md