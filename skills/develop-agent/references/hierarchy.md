# Hierarchy Design

Guide for designing multi-agent system hierarchies.

## Three-Tier Structure

| Tier | Role | Responsibility |
|------|------|----------------|
| Orchestrator | Top-level coordinator | Holds team memory, routes work, delivers briefings |
| Team Lead | Domain owner | Manages sub-team, runs pipelines end-to-end |
| Specialist | Leaf agent | Does one thing well, reports up, never manages |

## Five Hierarchy Rules

1. Exactly one agent has `reportsTo: null`
2. Team leads own pipelines (end-to-end delivery)
3. Leaf agents are specialists (no scope creep)
4. **Max depth of 3** (deeper adds latency)
5. Bidirectional references must match

## When to Create New Agents

| Create New | Avoid Creating New |
|------------|---------------------|
| Clear bounded task with unambiguous success criteria | Haven't tried optimizing single agent first |
| Security/compliance boundaries require isolation | Only reason is "future-proofing" or aesthetics |
| Parallel execution on independent concerns | Roles can be handled with persona switching |
| Failure containment is critical | Coordination overhead would exceed benefits |
| Current agent scope has become unmanageable | |