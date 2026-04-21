---
name: project-status
description: Generate and maintain project status reports in STATUS.md with executive summary, task metrics, dependencies, blockers, and risks. Use when user says "/project status" or asks about project health. Examples: "/project status", "show project status", "what's the project status".
---

# Project Status

Generate comprehensive project status reports with executive summaries, metrics, dependencies, blockers, and risks. Creates and maintains a STATUS.md file in the project root.

## Usage

```
/project-status
/project status
```

## Behavior

1. **Read Project Artifacts** — TODO.md, analysis/, reporting/, existing STATUS.md
2. **Compute Metrics** — Task counts, completion rates, priority distribution
3. **Identify Issues** — Dependencies, blockers, risks, time-consuming tasks
4. **Generate Report** — Executive summary + detailed sections
5. **Write STATUS.md** — Persist status for future reference
6. **Display Summary** — Show executive summary to user

## Output Files

| File | Purpose |
|------|---------|
| `STATUS.md` | Project status report (created/updated) |
| `TODO.md` | Source of task data (read-only) |
| `analysis/*.md` | Source of analysis artifacts (read-only) |
| `reporting/*/summary.md` | Source of completed task info (read-only) |

## STATUS.md Structure

```markdown
# Project Status

**Generated:** YYYY-MM-DD HH:MM
**Status:** 🟢 GREEN | 🟡 YELLOW | 🔴 RED

---

## Executive Summary

[2-3 sentences: overall health, biggest development, immediate concerns]

---

## Status Indicator

| Metric | Value | Trend |
|--------|-------|-------|
| Overall Status | 🟢/🟡/🔴 | ↑/↓/→ |
| Completion Rate | X% | ↑/↓/→ |
| Tasks Remaining | N | ↑/↓/→ |
| Blockers Active | N | ↑/↓/→ |

---

## Task Summary

### By Priority

| Priority | Total | Done | Remaining |
|----------|-------|------|-----------|
| P0 Critical | N | N | N |
| P1 High | N | N | N |
| P2 Medium | N | N | N |
| P3 Low | N | N | N |
| Unsorted | N | — | N |

### By Status

| Status | Count |
|--------|-------|
| Not Started | N |
| In Progress | N |
| Blocked | N |
| Done | N |

---

## Dependencies

| Dependency | Owner | Status | Due Date | Impact |
|------------|-------|--------|----------|--------|
| [dependency] | [who] | waiting/progress/done | [date] | [what's blocked] |

---

## Blockers

### Critical Blockers (Stopping Work)

| Blocker | Owner | Duration | Requested Action |
|---------|-------|----------|------------------|
| [blocker] | [who] | X days | [action needed] |

### Impediments (Slowing Progress)

| Impediment | Impact | Mitigation |
|------------|--------|------------|
| [issue] | [how it slows] | [how handling it] |

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [risk] | High/Med/Low | High/Med/Low | [how addressed] |

---

## Time-Consuming Tasks

| Task | Estimated | Actual | Variance | Reason |
|------|-----------|--------|----------|--------|
| [task] | Xh | Yh | +Zh | [why longer] |

---

## Decisions Required

| Decision | Owner | Deadline | Options |
|----------|-------|----------|---------|
| [decision] | [who] | [date] | [choices] |

---

## Recent Activity

| Task | Status | Date |
|------|--------|------|
| [completed task] | ✓ | YYYY-MM-DD |
| [current task] | In Progress | — |

---

## Next Steps

1. [Immediate action 1]
2. [Immediate action 2]
3. [Immediate action 3]
```

## Status Indicators (RAG)

Use traffic light status based on project health:

| Status | Condition | Meaning |
|--------|-----------|---------|
| 🟢 **GREEN** | On track, no blockers, <20% tasks at risk | Stakeholders need not worry |
| 🟡 **YELLOW** | Risks present, blockers exist but mitigated | May need decisions, early warning |
| 🔴 **RED** | Off track, critical blockers, will miss commitments | Needs immediate intervention |

**Key Rule**: If uncertain, use YELLOW — early warnings are better than surprising stakeholders with RED.

## Trend Indicators

| Trend | Meaning |
|-------|---------|
| ↑ | Improving |
| → | Stable |
| ↓ | Deteriorating |

Compare to previous STATUS.md to determine trends.

## Executive Summary Guidelines

Write 2-3 sentences that:

1. **Lead with verdict** — "Project is GREEN/ON TRACK/YELLOW/AT RISK"
2. **Highlight biggest development** — "Completed auth feature, started API integration"
3. **Surface immediate concerns** — "Blocked on SSL certificate, need DevOps response"

**Example:**
> Project is 🟡 YELLOW. Completed authentication feature and started API integration. Blocked on SSL certificate from DevOps for 3 days; escalation needed if not resolved by Friday.

## Dependencies Detection

### From TODO.md

Look for:
- Tasks with "depends on" or "blocked by" notation
- Tasks referencing external teams/people
- Tasks requiring decisions before starting

### From Analysis

Look for:
- External dependencies mentioned in functional analysis
- API/service dependencies in technical analysis
- Review/approval dependencies

### From Conversations

Check memory files for:
- Mentioned dependencies
- External team interactions
- Waiting items

## Blockers Detection

### Critical Blockers

Issues stopping work entirely:
- Tasks marked "blocked" in TODO.md
- Dependencies past due date
- Failed tests preventing progress
- Missing approvals or access

### Impediments

Issues slowing progress:
- Incomplete information
- Partial dependencies
- Technical debt slowing development
- Context switching

## Risks Assessment

### Risk Categories

| Category | Examples |
|----------|----------|
| **Technical** | Unknown complexity, new technology, integration risks |
| **Resource** | Team availability, skill gaps, tool limitations |
| **Schedule** | Tight deadlines, competing priorities, dependencies |
| **External** | Third-party APIs, vendor delays, regulatory changes |

### Risk Scoring

| Probability | Impact | Score | Priority |
|-------------|--------|-------|----------|
| High + High | High | 9 | Critical |
| High + Medium | Medium | 6 | High |
| Any + Low | Low | 3 | Low |
| Low + Low | Minimal | 1 | Minimal |

## Time-Consuming Tasks

Track tasks that take longer than estimated:

1. **Compare estimates to actuals** — From TODO.md and reporting/
2. **Identify variance** — Tasks with >50% over estimate
3. **Document reasons** — Why did it take longer?
4. **Update future estimates** — Learn from data

## Report Generation

### Step 1: Read Source Files

```
TODO.md         → Task counts, priorities, status
STATUS.md       → Previous status for trends
analysis/       → Dependencies, risks from planning
reporting/      → Completed task details
memory/         → Project context, past decisions
```

### Step 2: Compute Metrics

```python
total_tasks = sum(all priorities)
completed_tasks = sum(done)
completion_rate = completed_tasks / total_tasks * 100
blockers = count(blocked tasks)
```

### Step 3: Determine Status

```
IF critical_blockers > 0:
    status = RED
ELIF blockers > 0 OR completion_rate < 70%:
    status = YELLOW
ELSE:
    status = GREEN
```

### Step 4: Write STATUS.md

Create/update with computed sections.

### Step 5: Display Summary

Show executive summary + status indicator to user.

## Common Patterns

### New Project

```markdown
## Executive Summary

Project is 🟢 GREEN. Initial setup complete, backlog defined. Ready to start first sprint.

**Status:** No blockers, clear path forward.
```

### Active Development

```markdown
## Executive Summary

Project is 🟡 YELLOW. On track but blocked on API specs from Platform team. Completed 8/12 tasks this sprint.

**Concerns:** API specs pending for 2 days, need escalation if not received by tomorrow.
```

### Blocked Project

```markdown
## Executive Summary

Project is 🔴 RED. Critical blocker: SSL certificate request pending for 5 days. Cannot proceed with deployment.

**Action Required:** Manager to escalate with IT Director immediately.
```

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `/project` | Dispatcher that routes to this skill |
| `/project-feature` | Adds features to TODO.md |
| `/project-manage` | Completes tasks, updates reporting/ |
| `project-manager` agent | Uses status for task selection |

## Best Practices

Based on [project status reporting best practices](https://www.atlassian.com/agile/project-management/status-report):

1. **Be honest** — Early warnings beat surprising stakeholders
2. **Focus on goals** — Report milestones, not activities
3. **Assign ownership** — Every issue has an owner
4. **Request actions** — Blockers include requested actions
5. **Track trends** — Show improvement or deterioration
6. **Automate metrics** — Pull data from TODO.md, not manual counts
7. **Two audiences** — Executive summary for leadership, details for team

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Always GREEN until disaster | Use YELLOW early, escalate proactively |
| Activity lists | Report goal progress, not daily activities |
| Burying bad news | Surface risks in Executive Summary |
| No ownership | Every blocker/decision has an owner |
| Vague status | Use specific metrics and dates |

## File Locations

| File | Location |
|------|----------|
| Status report | `STATUS.md` (project root) |
| Task source | `TODO.md` (project root) |
| Analysis | `analysis/` |
| Completed tasks | `reporting/*/summary.md` |
| Project memory | `memory/` |