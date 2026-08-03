---
name: project-todo-refine
description: |
  Iteratively refine TODO.md topics by reviewing current state, scope, and priority. Use when refining backlog, updating TODO entries, or reviewing topic progress. Examples: "refine todo", "review backlog items", "update TODO.md scope".
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
- User says "review the backlog", "refine the TODO", "organize the backlog"

**Do NOT use for:**
- New feature intake (use `/project-feature`)
- Full implementation workflow (use `/project-manage`)
- Quick status overview (use `/project-status`)

**IMPORTANT:** Always invoke this skill explicitly when backlog refinement is requested. Do not proceed without proper skill invocation.

## Workflow

### Phase 1: TODO Overview

Read TODO.md from the current working folder and present:

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

### Phase 4: Sync with GitHub Issues

After refining the backlog, update related GitHub issues:

**Step 1: Identify affected issues**

Check TODO.md entries for issue references (e.g., `#14`, `issue #42`, `Closes #123`).

**Step 2: Determine if update is valuable**

| Situation | Update? |
|-----------|---------|
| New tasks added related to issue | ✅ Yes |
| Priority changed | ✅ Yes |
| Scope refined or clarified | ✅ Yes |
| Implementation decisions made | ✅ Yes |
| Minor formatting changes | ❌ No |
| No new information | ❌ No |

**Step 3: Post summary comment**

Use `gh issue comment` to post updates:

```bash
gh issue comment {number} --body "## 📋 Backlog Update

{summary of changes}

**Scope:** {which tasks, what's included}
**Priority:** {priority} ({reasoning})
**Estimate:** {if known}

**Key Decisions:**
- {decision 1}
- {decision 2}

**Details:** See TODO.md and analysis/ for full breakdown."
```

**Example:**

```bash
gh issue comment 14 --body "## 📋 Backlog Update

This issue has been refined and prioritized.

**Scope:** Tasks 2.1-2.3 (MVP implementation)
- Task 2.1: Skill Infrastructure (2-3h)
- Task 2.2: Package Plugin System (2-3h)
- Task 2.3: CLI --with Argument (1-2h)

**Priority:** P2 (after current P1 items: plugin-migration, mcp-server-refactor)
**Reasoning:** Foundation work must complete first; this builds on plugin infrastructure.

**Estimate:** 5-8 hours total

**Key Decisions:**
- Skills use user-level message injection (not tool wrapper)
- Namespace format: {package}:{tool|skill|agent}
- Graceful failure for non-yoker packages

**Details:** See TODO.md and analysis/backlog-refinement-2026-05-27.md"
```

**Step 4: Verify**

After posting, verify the comment was added:

```bash
gh issue view {number} --comments
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

## Documentation Update Ordering

When refining the backlog, update files in this order for proper traceability:

1. **REQUIREMENTS.md first** — Source of truth for all requirements
   - Add new requirements with unique IDs (R1, R2, ...)
   - Mark completed requirements with [x]
   - Update the "Completed" section for traceability

2. **TODO.md second** — Task breakdown and priorities
   - Add/update tasks with requirement references (Satisfies: R1, R2)
   - Organize by phase/priority
   - Mark completed tasks in "Done" section

3. **analysis/functional.md third** — Architecture details
   - Update with new patterns/components
   - Document design decisions
   - Note code quality issues

4. **User documentation (docs/usage.rst)** — User-facing docs
   - Add new use cases
   - Update API examples

5. **API documentation (docs/api.rst)** — Reference docs
   - Add new public functions
   - Update type signatures

6. **GitHub issues last** — Synchronization
   - Post updates on affected issues
   - Note scope/priority changes

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
