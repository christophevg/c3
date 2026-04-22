---
name: project-todo-refine
description: Iteratively refine TODO.md topics by reviewing current state, scope, and priority. Use when refining backlog, updating TODO entries, or reviewing topic progress. Examples: "refine todo", "review backlog items", "update TODO.md scope".
---

# Project TODO Refine

Guide iterative refinement of TODO.md topics with user feedback. Focus on updating scope, priority, and integration—not full functional analysis.

## Overview

| Capability | Description |
|------------|-------------|
| TODO overview | Show current TODO.md state and topics needing work |
| Topic introduction | Present each topic with context and current status |
| Recommendation | Suggest course of action for each topic |
| User feedback loop | Gather feedback and revise topics |
| Backlog integration | Update TODO.md with refined entries |

## When to Use This Skill

Use this skill when:
- User wants to refine or update TODO.md entries
- User asks to review backlog items
- User wants to iterate through topics and update scope/priority
- Topics need refinement before functional analysis

**Do NOT use for:**
- New feature intake (use `/project-feature`)
- Full implementation workflow (use `/project-manage`)
- Quick status overview (use `/project-status`)

## Workflow

### Phase 1: TODO Overview

Read TODO.md and present:

```markdown
## TODO.md Overview

**Total Topics:** {count}
**Phases:** {phase list}

| Phase | Topics | Status |
|-------|--------|--------|
| {phase} | {count} | {summary} |

**Topics Requesting Attention:**
1. {topic} - {reason}
2. {topic} - {reason}
...
```

**Identify topics needing work by checking:**
- Topics marked as "needs refinement", "blocked", or unclear scope
- Topics with stale timestamps (older than 2 weeks without progress)
- Topics flagged for review in previous sessions
- Topics with incomplete or vague descriptions

### Phase 2: Iterative Topic Refinement

For each topic requiring attention:

**Step 1: Introduce Topic**

```markdown
## Topic: {topic-name}

**Current State:** {from TODO.md}
**Phase:** {phase}
**Priority:** {priority if specified}
**Dependencies:** {any blocking/blocked topics}

**Context:**
{relevant context from project files, commits, or related work}

**Progress Indicators:**
- {indicator 1}
- {indicator 2}
```

**Step 2: Recommend Course of Action**

Provide a clear recommendation:

```markdown
**Recommendation:** {specific action}

**Rationale:** {why this action makes sense}

**Suggested Updates:**
- Priority: {suggested change}
- Scope: {suggested refinement}
- Dependencies: {suggested additions}
```

**Step 3: Ask for User Feedback**

Use AskUserQuestion tool with targeted questions:

1. **Scope validity** — "Is the scope still valid, or does it need adjustment?"
2. **Priority alignment** — "Is the current priority appropriate?"
3. **Scope changes** — "What aspects would you like to update?"
4. **Integration** — "How should this integrate with other topics?"

**Question format:**

```markdown
{topic introduction}

{recommendation}

What would you like to do with this topic?
```

**Step 4: Revise Topic**

Based on user feedback, update the topic in TODO.md:

- Refine description for clarity
- Update priority level
- Add or remove dependencies
- Split into sub-topics if scope expanded
- Merge with related topics if appropriate
- Mark as complete if no longer needed

### Phase 3: Summary and Integration

After refining topics, provide:

```markdown
## Refinement Summary

**Topics Reviewed:** {count}
**Topics Updated:** {count}
**Topics Completed:** {count}
**Topics Split:** {count}

**Key Changes:**
- {change 1}
- {change 2}

**Recommended Next Steps:**
1. {next step 1}
2. {next step 2}
```

## Topic Status Indicators

When analyzing topics, look for:

| Indicator | Meaning |
|-----------|---------|
| `needs-refinement` | Topic scope unclear, needs discussion |
| `blocked` | Waiting on external dependency |
| `in-progress` | Actively being worked on |
| `pending` | Queued but not started |
| `review` | Needs review before proceeding |
| No status | Assume `pending` |

## Reading Context

For each topic, gather context from:

1. **TODO.md** — Current state and metadata
2. **Related files** — Check `analysis/` for functional analysis
3. **Git history** — Recent commits touching related areas
4. **Project files** — Implementation files if topic is in progress

## Common Refinement Actions

| Action | When to Apply |
|--------|---------------|
| Clarify scope | Description is vague or ambiguous |
| Raise priority | Dependencies are ready, high impact |
| Lower priority | Blocked, low urgency, or deferred |
| Split topic | Scope too broad for single task |
| Merge topics | Overlapping scope, should be combined |
| Mark complete | Work finished, no longer needed |
| Add dependency | Discovered blocking relationship |
| Remove dependency | Blocker resolved or irrelevant |

## Writing to TODO.md

Maintain TODO.md format consistency:

```markdown
## Phase: {phase-name}

### {topic-name}

**Status:** {status}
**Priority:** {priority}
**Description:** {clear description}
**Dependencies:** {comma-separated list}
**Notes:** {optional context}

**Tasks:**
- [ ] {task 1}
- [ ] {task 2}
```

**Keep entries:**
- Concise but complete
- Action-oriented
- Clearly scoped
- Properly cross-referenced

## Related Skills

- `/project-feature` — Capture new feature ideas (full functional analysis)
- `/project-status` — Quick overview of project state
- `/project-manage` — Full implementation workflow
- `/functional-analyst` — Deep analysis of requirements

## Integration with Project Workflow

```
User Request → Refine TODO
     ↓
TODO Overview (Phase 1)
     ↓
For each topic:
  Introduce → Recommend → Ask → Update (Phase 2)
     ↓
Summary and Next Steps (Phase 3)
```

**Position in workflow:**
- Before `/project-feature` — Refine vague ideas into actionable topics
- After `/project-status` — Follow up on identified issues
- Before `/project-manage` — Prepare backlog for implementation