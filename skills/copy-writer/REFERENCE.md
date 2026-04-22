# Copy Writer - Platform Quick Reference

Quick reference card for platform specifications and best practices.

## Platform Limits

| Platform | Char Limit | Hook Zone | Sweet Spot | Key Signal |
|----------|------------|-----------|------------|------------|
| Twitter/X | 280 | First 180 | 150-220/post | Bookmark rate |
| LinkedIn | 3,000 | First 210 | 1,300-2,500 | Comments |
| Mastodon | 500 | First 50 | N/A | N/A (chronological) |
| Newsletter | 33 (subject) | First 33 | 2-4 words | Open rate |
| Blog | N/A | Title + first 100 | 150-160 meta | SEO + AI |

## Character Limits Detail

### Twitter/X

| Content | Limit | Notes |
|---------|-------|-------|
| Standard post | 280 | URLs = 23 chars |
| X Premium post | 25,000 | Rich formatting |
| Direct Message | 10,000 | |
| Bio | 160 | |
| Display Name | 50 | |
| Username | 15 | |

**Thread Best Practices**:
- Optimal length: 7-10 posts
- Hook post: <180 chars, declarative (not question)
- Content posts: 150-220 chars
- Number posts: 1/10, 2/10, etc.
- Hashtags: 1-2 max

### LinkedIn

| Content | Limit | Optimal |
|---------|-------|---------|
| Post | 3,000 | 1,300-2,500 |
| Article | ~125,000 | 1,500-3,000 words |
| Headline | 220 | 60-100 front-loaded |
| About | 2,600 | Full use |

**Engagement by Length**:
| Chars | Median Engagement |
|-------|------------------|
| 1-400 | 2.10% |
| 401-700 | 2.24% |
| 701-1,000 | 2.31% |
| 1,001-1,300 | 2.44% |
| **1,301-2,000** | **2.61%** |
| **2,001-2,500** | **2.67%** |

**Content Framework**: 40% expertise, 40% engagement, 20% promotional

### Mastodon

| Content | Limit | Notes |
|---------|-------|-------|
| Default post | 500 | Instance-configurable |
| Links | 23 | Regardless of length |
| Mentions | Username only | Domain doesn't count |

**Key Differences**:
- No algorithmic timeline (chronological)
- Hashtags at end on separate line
- Content warnings optional
- No quote tweets (boost/feature instead)

### Newsletter

| Metric | Best Practice |
|--------|---------------|
| Subject line | 33 chars guaranteed mobile |
| Gmail mobile | 37-48 chars visible |
| Gmail desktop | ~88 chars visible |
| Optimal words | 2-4 words |

**Avoid**:
- ALL CAPS + excessive punctuation (+40-60% spam score)
- Fake Re:/Fwd: prefixes
- Subject-content mismatch (30.4% of unsubscribes)

### Blog/Website

| Element | Limit | Notes |
|---------|-------|-------|
| Title tag | 50-60 chars | 580-600px |
| Meta description | 150-160 chars | 120 on mobile |
| H1 | One per page | Mirror title tag |

**AI Optimization (2026)**:
- Self-contained answer blocks: 134-167 words
- Question-based headings
- Schema markup (JSON-LD)
- /llms.txt for AI crawlers

## Tone Profiles by Platform

| Platform | Tone | Key Adaptations |
|----------|------|-----------------|
| Twitter | Casual, punchy | Short sentences, personality-driven |
| LinkedIn | Professional | Lead with impact, use metrics, 150-300 words |
| Mastodon | Community, authentic | Longer-form ok, hashtag-friendly |
| Newsletter | Personal, direct | One CTA, front-load value |
| Blog | Authoritative, educational | Long-form, research-backed |

## Hashtag Guidelines

| Platform | Quantity | Placement |
|----------|----------|-----------|
| Twitter | 1-2 | End or inline |
| LinkedIn | 3-5 | End |
| Mastodon | As needed | End, separate line |
| Instagram | 5-10 | End |
| Blog | N/A | Tags in metadata |

## CTA Best Practices

| Platform | CTA Approach |
|----------|--------------|
| Twitter | Engagement question ("Which...?"), thread indicator |
| LinkedIn | Question for comments, "Full breakdown: [link]" |
| Newsletter | One clear CTA, 150-200 words before CTA |
| Blog | Multiple CTAs (inline, end), question headings |

## What to Avoid

### Twitter/X
- Questions in hook (22% fewer clicks)
- More than 2 hashtags per thread (-14% engagement)
- Threads over 20 posts (70%+ drop-off)

### LinkedIn
- "I'm excited/thrilled to announce..." (lowest-performing opener)
- Engagement bait ("Like if you agree")
- More than 5 hashtags
- Buzzwords: "guru", "ninja", "synergy"

### Newsletter
- ALL CAPS + excessive punctuation
- Fake Re:/Fwd:
- Subject-content mismatch

### All Platforms
- AI-typical vocabulary: "tapestry", "delve", "palpable", "camaraderie", "embark", "realm", "underscore"
- Vague intensifiers: "very", "really", "extremely"
- Passive constructions (prefer active voice)
- Hedging: "It is important to note"

## Accessibility Quick Check

- Grade 9 reading level or below
- Active voice ("We recommend" not "It is recommended")
- Descriptive link text (not "click here")
- Alt text for images (<125 chars, describe meaning not appearance)
- Plain language for technical terms

## Voice Preservation Checklist

When adapting content, preserve:

- [ ] Characteristic vocabulary terms
- [ ] Sentence rhythm patterns
- [ ] Transition phrases
- [ ] Organization structure
- [ ] Formality level
- [ ] Voice characteristics (authoritative, humble, reflective)

Apply tone shift (+/- 20%):

- [ ] Platform-appropriate tone adjustments
- [ ] Character limit compliance
- [ ] Platform-specific CTAs
- [ ] Hashtag conventions
- [ ] Hook optimization