---
name: analysis-integration
description: Use this skill after multiple domain agents complete their reviews to integrate findings and update the backlog coherently.
---

# Analysis Integration

This skill is invoked after domain-specific agents (api-architect, ui-ux-designer, etc.) complete their analysis reviews. It consolidates findings and updates the backlog in a structured way.

## When to Use

Invoke this skill when:
- Multiple domain agents have completed their analysis
- You need to consolidate findings before implementation
- TODO.md needs to be updated with integrated changes from multiple reviews

## Process

1. **Gather Documents**
   - Read `analysis/README.md` to identify all recent documents
   - Read each analysis document from the current session
   - Note the date pattern to match session documents

2. **Identify Overlaps**
   - Find issues mentioned by multiple agents
   - Note cross-domain dependencies (e.g., API endpoints needed for UI features)
   - Flag conflicting recommendations

3. **Prioritize Findings**
   - Critical issues first (security, data integrity)
   - High-impact user experience issues
   - Performance and optimization issues
   - Nice-to-have improvements

4. **Integrate into TODO.md**
   - Merge new tasks from all domain agents
   - Maintain phase organization
   - Re-number tasks if needed
   - Add cross-references between related tasks
   - Remove duplicate tasks

5. **Create Integration Summary**
   - Document in `analysis/YYYY-MM-DD-integration-summary.md`
   - List key decisions made
   - Note any conflicts resolved
   - Provide implementation priority recommendations

6. **Update Analysis Index**
   - Update `analysis/README.md` with the new integration summary

## Integration Summary Template

```markdown
# Integration Summary: [Session Scope]

**Date:** YYYY-MM-DD
**Integrated From:** [List of source documents]

## Key Decisions

| Issue | Resolution | Rationale |
|-------|------------|-----------|
| ... | ... | ... |

## Cross-Domain Dependencies

| Frontend Task | Depends on API Task | Phase |
|---------------|---------------------|-------|
| ... | ... | ... |

## Priority Order

1. [Highest priority items]
2. [...]
3. [Lowest priority items]

## Conflicts Resolved

| Conflict | Resolution |
|----------|------------|
| ... | ... |

## New Tasks Added

- [x] Phase N: Task N.X - [Description]
```

## Output

- Updated `TODO.md` with integrated tasks
- New `analysis/YYYY-MM-DD-integration-summary.md` document
- Updated `analysis/README.md` index
