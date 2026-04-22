# Copy Writer Skill

Transform technical content into marketing-ready articles adapted for multiple platforms while maintaining personal voice consistency.

## Overview

The copy-writer skill transforms existing content into platform-specific adaptations. It preserves the author's personal voice while optimizing for each platform's conventions, character limits, and audience expectations.

## Core Capabilities

### Content Transformation
- **Input**: Markdown files or plain text
- **Output**: Platform-adapted content in multiple formats (plain text, platform-specific, JSON)
- **Transformation Depth**: Light touch (80% preserve) with platform-aware adjustments (20%)
- **Languages**: English and Dutch

### Supported Platforms

| Platform | Char Limit | Hook Zone | Key Features |
|----------|------------|-----------|--------------|
| Twitter/X | 280 | First 180 | Threads (7-10 posts), hashtags (1-2), threads indicator |
| LinkedIn | 3,000 | First 210 | Professional tone, 40/40/20 content mix, documents/carousels |
| Mastodon | 500 | First 50 | Community focus, hashtags at end, chronological feed |
| Newsletter | 33 (subject) | First 33 | Subject line optimization, one clear CTA |
| Blog/Website | N/A | Title + meta | SEO optimization, 150-160 char meta descriptions |
| GitHub README | N/A | First 100 | Technical focus, code examples, clear structure |
| Documentation | N/A | First 100 | Technical accuracy, heading hierarchy |

### Style Integration

The skill integrates with the `style-profile` skill:

1. **Invocation**: Uses `/style-profile check` to load the author's writing style
2. **Voice Preservation**: Maintains characteristic vocabulary, sentence structure, and tone
3. **Anti-Pattern Enforcement**: Avoids AI-typical words (tapestry, delve, palpable, camaraderie)
4. **Tone Adaptation**: Applies 80% personal voice + 20% platform-specific adjustments

## Invocation Patterns

### Command-Based

```
/copy-writer adapt {file} for {platform}
/copy-writer adapt {file} for {platform1}, {platform2}, {platform3}
/copy-writer check {file} against style-profile
/copy-writer headlines for {file}
/copy-writer seo-suggestions for {file}
```

### Natural Language

```
"Help me adapt this article for Twitter and LinkedIn"
"Turn this blog post into a newsletter"
"Make this content suitable for GitHub README"
"Suggest improvements for this LinkedIn post"
```

### Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `{file}` | Input content file path | Markdown or plain text file |
| `{platform}` | Target platform | twitter, linkedin, mastodon, newsletter, blog, github, docs |
| `--output` | Output format | text, markdown, json |
| `--style-profile` | Style profile path | Default: ask for location |
| `--language` | Target language | en, nl |

## Workflow

### Primary Platform First

The skill follows a priority-based workflow:

```
1. Load style profile (invoke /style-profile check)
2. Parse input content and detect content type
3. Ask for primary platform if not specified
4. Generate content for primary platform
5. Present draft for review
6. Iterate based on feedback
7. Offer adaptations for secondary platforms
8. Save approved drafts to project folder
```

### Interactive Refinement

```
Draft → User Feedback → Refine → User Feedback → ... → Final Approval
```

Each iteration maintains context of previous versions and feedback.

### Platform-Specific Adaptation

When adapting for multiple platforms:

1. **Primary Content**: Generate for user-specified primary platform first
2. **Review**: User reviews and approves primary content
3. **Secondary Offer**: Skill offers adaptations for other platforms
4. **Selective Generation**: User chooses which secondary platforms to generate
5. **Parallel Output**: All selected platforms generated from approved primary

## Output Conventions

### File Naming

Platform adaptations use suffix naming:

```
my-article.md           (original)
my-article-twitter.md   (Twitter thread)
my-article-linkedin.md  (LinkedIn post)
my-article-newsletter.md (newsletter version)
```

### Output Formats

#### Plain Text / Markdown

Standard formatted content ready for copy-paste or further editing.

#### Platform-Specific

Optimized for direct platform posting with:
- Character limit compliance
- Platform-appropriate hashtags/mentions
- Platform-aware CTAs
- Formatting conventions applied

#### JSON/Structured

```json
{
  "original_file": "my-article.md",
  "platform": "linkedin",
  "headline": "Optional headline",
  "body": "Platform-optimized content...",
  "hashtags": ["#tech", "#programming"],
  "character_count": 1247,
  "suggestions": [
    "Consider adding an image to increase engagement"
  ],
  "seo": {
    "keywords": ["python", "automation", "productivity"],
    "meta_description": "Learn how to automate..."
  }
}
```

## Platform-Specific Behaviors

### Twitter/X

- **Character Limit**: 280 per post
- **Thread Support**: Detects when content exceeds 280 chars, proposes thread structure
- **Thread Length**: Optimal 7-10 posts (warns if <5 or >20)
- **Hashtags**: 1-2 maximum, placed at end
- **Hook**: First 180 chars critical for engagement
- **CTA**: Engagement questions ("Which mistake is your team making?")
- **Tone**: Casual, conversational, punchy

### LinkedIn

- **Character Limit**: 3,000 (optimal: 1,300-2,500)
- **Hook Zone**: First 210 chars before "See more"
- **Hashtags**: 3-5 maximum, professional tone
- **Content Mix**: 40% expertise, 40% engagement, 20% promotional
- **CTA**: Questions for comments, or "Full breakdown: [link]"
- **Tone**: Professional, polished, outcome-focused
- **Avoid**: "I'm excited/thrilled to announce" (lowest-performing opener)

### Mastodon

- **Character Limit**: 500 (instance-dependent)
- **Hashtags**: Placed at end of post on separate line
- **Tone**: Community-focused, authentic, less promotional
- **No Algorithm**: Chronological feed, no engagement gaming
- **Content Warnings**: Optional for sensitive content

### Newsletter (Email)

- **Subject Line**: 33 chars guaranteed mobile visibility
- **Personalization**: Use recipient name when available
- **CTA**: One clear call-to-action per email
- **Timing**: Tuesday-Thursday, 8-11am recipient timezone
- **Avoid**: ALL CAPS, fake Re:/Fwd:, subject-content mismatch
- **Tone**: Personal, direct, valuable

### Blog/Website

- **Title**: 50-60 characters (580-600px)
- **Meta Description**: 150-160 chars desktop, 120 mobile
- **Heading Structure**: Single H1, H2 for sections, H3 for subsections
- **SEO**: Question-based headings, self-contained answer blocks
- **AI Optimization**: /llms.txt file, schema markup
- **Alt Text**: Describe meaning, <125 chars, no "image of" prefix
- **Tone**: Authoritative, educational, thorough

### GitHub README / Documentation

- **Structure**: Clear heading hierarchy
- **Code Examples**: Syntax-highlighted blocks
- **Links**: Descriptive link text
- **Tone**: Technical, precise, clear
- **Focus**: Accuracy over engagement

## Style Profile Application

### Voice Preservation

When adapting content, preserve from style profile:

| Element | Preservation |
|---------|---------------|
| Vocabulary | Characteristic terms, technical language |
| Sentence Rhythm | Length distribution, complexity patterns |
| Tone | Formality level, emotional range |
| Transitions | How sections connect |
| Organization | Section structure, explanation approach |

### Tone Adaptation (20%)

Apply platform-specific tone shifts while preserving voice:

| Platform | Tone Shift |
|----------|------------|
| Twitter | +casual, +concise, +conversational |
| LinkedIn | +professional, +polished, +outcome-focused |
| Mastodon | +community, +authentic, -promotional |
| Newsletter | +personal, +direct, +intimate |
| Blog | Full voice, longer-form storytelling |

### Anti-Patterns

Always avoid from style profile's AI-Warning Patterns:

- AI-typical vocabulary: "tapestry", "delve", "palpable", "camaraderie", "embark", "realm", "underscore"
- Passive constructions (where style prefers active)
- Vague intensifiers: "very", "really", "extremely"
- Hedging: "It is important to note"

## Content Type Handling

### Technical Tutorials

- Clear step-by-step structure
- Code examples preserved or adapted
- Prerequisites clearly stated
- Troubleshooting tips included

### Personal Stories

- Narrative flow maintained
- Emotional engagement preserved
- Anecdotes adapted for platform length
- Personal voice emphasized

### Announcements

- Key points highlighted first
- Concise, informative format
- Relevant links included
- Project-specific hashtags added

## Quality Assurance

### Self-Check Against Style Profile

Before presenting any draft:

1. **Vocabulary Check**: Flag AI-typical words
2. **Sentence Structure**: Compare against profile metrics
3. **Tone Consistency**: Verify matches voice characteristics
4. **Platform Compliance**: Check character limits, formatting
5. **CTA Appropriateness**: Verify platform-aware CTAs

### Accessibility Suggestions

Optional suggestions (not auto-applied):

- Inclusive language alternatives
- Readability level (Grade 9 target)
- Alt text for referenced images
- Plain language for technical terms

### SEO Suggestions

Optional suggestions (not auto-applied):

- Keywords relevant to content
- Meta description proposals
- Title/heading improvements
- Internal/external linking opportunities

## Error Handling

### Edge Cases

| Situation | Behavior |
|-----------|----------|
| Empty/short input | Flag issue, ask for more content |
| Platform unrecognized | Ask user to specify platform |
| Content exceeds platform limit | Propose thread/split strategy |
| Style profile unavailable | Ask for profile location or proceed without |
| Conflicting requirements | Ask user for guidance |

### Recovery

- Always ask user before making assumptions
- Provide clear explanation of the issue
- Offer actionable options for resolution
- No automatic workarounds

## Language Support

### English (Default)

- Primary language for most content
- Full platform support

### Dutch

- For regional/local audiences
- Platform conventions may differ
- User specifies target language in request

### Cross-Language

- Can translate English → Dutch or Dutch → English
- Maintains voice characteristics across languages
- Platform-specific terms adapted appropriately

## Limitations

### What Copy-Writer Does NOT Do

1. **No Original Creation**: Only transforms existing content
2. **No Media Generation**: Suggests where media could go, doesn't create/sourcing
3. **No Publishing**: Produces drafts only, user handles publishing
4. **No URL Fetching**: Cannot fetch content from URLs
5. **No Templates**: Each piece is unique, no templating system
6. **No Version Control**: User manages git/versioning manually

### Scope Boundaries

- Input must be provided (file or text)
- Output goes to files only
- Style profile must exist or be provided
- User reviews all drafts before use

## Examples

### Basic Adaptation

```
User: /copy-writer adapt articles/my-post.md for linkedin

Skill:
1. Loads style profile
2. Reads article content
3. Detects content type (technical tutorial)
4. Generates LinkedIn adaptation (1,500 words, professional tone)
5. Adds platform-appropriate hashtags
6. Suggests headline: "How I Automated My Workflow with Python"
7. Saves to articles/my-post-linkedin.md
8. Presents draft for review

Draft:
[Headline] How I Automated My Workflow with Python
[Body] In my latest article, I explored how Python scripting...
[Hashtags] #python #automation #productivity
[Char count] 1,247 / 3,000

Would you like to review and provide feedback?
```

### Multi-Platform with Priority

```
User: "Help me adapt articles/release-notes.md for my newsletter first, then Twitter"

Skill:
1. Loads style profile
2. Asks: "What's the key announcement you want to highlight?"
3. User: "The new API endpoint for webhooks"
4. Generates newsletter version (focus: webhook announcement)
5. Presents draft for review
6. After approval: "Would you like the Twitter adaptation now?"
7. Generates Twitter thread (3 posts, focused on webhook)
8. Saves both versions
```

### Iterative Refinement

```
User: "Make it more casual for Twitter"

Skill:
Refined draft:
[Thread 1/3] Been working on something cool - webhooks are now live!
[Thread 2/3] Here's what you can do with them...
[Thread 3/3] Check out the docs and let me know what you build 🚀
[Hashtags] #webhooks #API

Is this better? Would you like to adjust the tone further?
```

## File Structure

```
project/
├── articles/
│   ├── my-article.md           (original)
│   ├── my-article-linkedin.md  (LinkedIn adaptation)
│   ├── my-article-twitter.md   (Twitter thread)
│   └── my-article-newsletter.md (newsletter)
└── .claude/
    └── style-profiles/
        └── christophe-vg.md    (style profile)
```

## Dependencies

- **style-profile skill**: For voice consistency checking
- **No external dependencies**: All processing is internal

## See Also

- [Functional Analysis](analysis/functional.md) - Full requirements
- [Domain Research](research/README.md) - Platform specifications and best practices
- [Style Profile Skill](../personal-writing-style-skill/) - Voice definition