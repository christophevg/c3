# Project Manager Agent - Functional Analysis

**Date:** 2026-04-28
**Updated:** 2026-04-28
**Analyst:** Refactored from skill delegation to direct agent orchestration

## Purpose

The Project Manager agent orchestrates project workflow by delegating to specialized agents. It is a **pure coordinator** - it never implements code, runs tests, or performs analysis directly. All specialized work is delegated to domain-specific agents.

## Scope

### In Scope
- Orchestrating project workflow phases
- Detecting project state (new, incomplete, ready)
- Invoking specialized agents for each phase
- Coordinating consensus between domain agents
- Tracking progress across multiple tasks
- Managing session state for active work
- Creating persistent memory for project knowledge
- Handling blockers and stopping conditions

### Out of Scope
- Direct implementation of code (delegated to python-developer)
- Direct functional analysis (delegated to functional-analyst)
- Direct domain analysis (delegated to api-architect, ui-ux-designer, security-engineer)
- Direct code review (delegated to code-reviewer)
- Direct test execution (delegated to python-developer)
- Direct test review (delegated to testing-engineer)
- Direct documentation (delegated to end-user-documenter)

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| Initial request | User message | "manage project", "start project workflow", or agent invocation |
| Optional instructions | User message | Task limits, priority filters, specific tasks |
| TODO.md | File | Prioritized backlog of tasks |
| Project state | Files | analysis/, reporting/, memory/ |

## Outputs

| Output | Type | Location |
|--------|------|----------|
| Task progress | Conversation | Reports after each task |
| Session state | File | session-state.md |
| Memory updates | Files | memory/*.md |
| Consensus reports | Files | reporting/{task}/consensus.md |

## Tools Required

| Tool | Usage |
|------|-------|
| Read | Read TODO.md, analysis/, session-state.md, memory/ |
| Write | Create session-state.md, memory files, reporting/ |
| Edit | Update session-state.md, TODO.md |
| Glob | Find project files |
| Grep | Search project files |
| Agent | Invoke specialized agents (primary tool) |
| AskUserQuestion | Ask for confirmation, clarification, blockers |

## Agent Delegation

All specialized work is delegated via the Agent tool:

| Phase | Agent Invoked |
|-------|---------------|
| Initial analysis | functional-analyst |
| Research | researcher |
| API design | api-architect |
| UX design | ui-ux-designer |
| Security review | security-engineer |
| Implementation | python-developer |
| Functional review | functional-analyst |
| Code review | code-reviewer |
| Test review | testing-engineer |
| Documentation | end-user-documenter |

## Workflow Phases

1. **Phase 0: Project State Detection** — Check analysis/functional.md, TODO.md
2. **Phase 1A/1B: Analysis** — Invoke functional-analyst
3. **Phase 1C: Task Selection** — Read TODO.md, propose task
4. **Phase 2: Cross-Domain Review** — Invoke domain agents (api-architect, ui-ux-designer, security-engineer)
5. **Phase 3: Consensus** — Collect feedback, create consensus report
6. **Phase 4: Implementation** — Invoke python-developer
7. **Phase 5: Review Cycle** — Sequential reviews (functional → domain → quality → docs)
8. **Phase 6: Completion** — Update TODO.md, create summary
9. **Phase 7: Continue/Stop** — Check conditions, loop or exit

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Direct agent invocation | Agents execute independently, true delegation |
| Pure coordinator role | Keeps context clean, no implementation details |
| Mandatory review cycle | Quality gate before completion |
| Parallel agent invocation | Efficiency for independent reviews |
| Stop on blockers | Prevents cascading failures |
| Session state + memory | Active work state + cross-session knowledge |

## Relationship to Skills

The `project-manage` skill contains the workflow logic as instructions for the main agent. This agent is an alternative entry point that delegates to specialized agents for true independent execution. Both can coexist during the transition period.

## Scope Validation

- **Trigger Test**: Explicit request to manage project ✓
- **Action Test**: Orchestrates via agent delegation, never implements directly ✓
- **Failure Test**: Stops on blockers, doesn't cascade ✓
- **Separation Test**: All specialized work delegated to appropriate agents ✓