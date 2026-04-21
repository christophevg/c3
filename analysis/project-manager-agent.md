# Project Manager Agent - Functional Analysis

**Date:** 2026-04-21
**Analyst:** develop-agent skill (interview-based)

## Purpose

The Project Manager agent orchestrates project workflow by delegating to specialized skills and tracking progress across multiple tasks. It maintains minimal context at the project level while delegating implementation details to specialized agents via skills. It can process multiple tasks from a TODO.md in sequence, with configurable task limits and stopping conditions.

## Scope

### In Scope
- Orchestrating project workflow via project-* skills
- Processing multiple tasks from TODO.md with configurable limits
- Tracking project state and progress across tasks
- Accepting optional instructions (task limits, priority filters, specific tasks)
- Stopping on blockers (failed tests, review rejection, implementation errors)
- Maintaining session state for active work
- Creating persistent memory for project knowledge
- Reporting progress after each task or batch

### Out of Scope
- Direct implementation of code (delegated to python-developer)
- Direct functional analysis (delegated to functional-analyst via project-manage)
- Direct domain analysis (delegated to domain agents via project-manage)
- Manual code review (delegated to code-reviewer via project-manage)
- Test execution (delegated to python-developer via project-manage)
- Bug fixing workflow (delegated to bug-fixing skill via project-manage)

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| Initial request | User message | "manage project", "start project workflow", or direct agent invocation |
| Optional instructions | User message | Task limits, priority filters, specific tasks to work on |
| TODO.md | File | Prioritized backlog of tasks |
| Project state | Files | analysis/, reporting/, memory/ |

## Outputs

| Output | Type | Location |
|--------|------|----------|
| Task progress | Conversation | Reports after each task |
| Session state | File | session-state.md |
| Memory updates | Files | memory/*.md |
| Consensus reports | Files | reporting/{task}/consensus.md (via project-manage) |

## Tools Required

| Tool | Usage | Risk Level |
|------|-------|------------|
| Read | Read TODO.md, analysis/, session-state.md, memory/ | read |
| Write | Create session-state.md, memory files, reporting/ | modify |
| Edit | Update session-state.md, TODO.md | modify |
| Glob | Find project files | read |
| Grep | Search project files | read |
| Skill | Invoke project-* skills | read (delegates to modify) |
| Agent | Invoke specialized agents for cross-domain coordination | read (delegates to modify) |
| AskUserQuestion | Ask for confirmation, clarification | read |

## Constraints

- Does NOT directly invoke domain agents (api-architect, ui-ux-designer, security-engineer) - delegates to project-manage skill
- Does NOT directly invoke python-developer for implementation - delegates to project-manage skill
- Does NOT directly invoke reviewers - delegates to project-manage skill
- MUST stop on blockers (failed tests, review rejection, implementation errors)
- MUST report progress after each task completion
- MUST respect user-configured task limits
- MUST maintain minimal context (project-level, not implementation details)

## Workflow

### Phase 1: Initialize

1. Parse optional instructions (task limits, priority filters, specific tasks)
2. Read TODO.md to understand current backlog
3. Read or create session-state.md
4. Read relevant memory files for project context
5. Determine task selection based on instructions or TODO.md priority

### Phase 2: Task Selection

1. Apply filters from optional instructions
2. Select next task from TODO.md
3. Check if task limit reached
4. If no tasks or limit reached, report status and exit

### Phase 3: Execute Task

1. Invoke project-manage skill with task details
2. Monitor for blockers
3. If blocker: stop and report to user
4. If success: record progress in session-state.md

### Phase 4: Memory Update

1. Create/update memory files for decisions made
2. Update session-state.md with completed task
3. Mark task as done in TODO.md

### Phase 5: Continue or Stop

1. Check stopping conditions:
   - User-configured task limit reached
   - Blocker encountered
   - User explicitly stopped
   - TODO.md empty
2. If continuing: return to Phase 2
3. If stopping: report final status to user

## Example Scenarios

### Scenario 1: Basic Multi-Task Execution

**Input:** "Manage project, work on top 3 priority tasks"

**Expected Output:**
1. Reads TODO.md, identifies 3 highest priority tasks
2. Executes task 1 via project-manage
3. Reports completion, updates session-state.md
4. Executes task 2 via project-manage
5. Reports completion, updates session-state.md
6. Executes task 3 via project-manage
7. Reports completion, updates session-state.md
8. Reports final summary: 3 tasks completed

### Scenario 2: Blocker Encountered

**Input:** "Manage project"

**Expected Output:**
1. Reads TODO.md, identifies next task
2. Executes task via project-manage
3. project-manage reports: tests failed
4. Stops and reports to user: "Task X blocked: tests failed"
5. Updates session-state.md with blocker status

### Scenario 3: Specific Task

**Input:** "Manage project, implement task 1.2"

**Expected Output:**
1. Reads TODO.md, finds task 1.2
2. Executes task 1.2 via project-manage
3. Reports completion
4. Asks if user wants to continue with next task

### Scenario 4: Session Continuation

**Input:** "Manage project, continue"

**Expected Output:**
1. Reads session-state.md
2. Identifies last completed task
3. Resumes with next task in TODO.md
4. Continues until blocker or task limit

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Delegate to skills, not agents | Keeps context minimal, follows existing pattern from Assistant agent |
| Stop on blockers | Prevents cascading failures, allows user intervention |
| User-configurable task limits | Flexible for different use cases (quick fix vs sprint) |
| Both session state and memory | Session for active work, memory for cross-session knowledge |
| Explicit request trigger | Prevents unintended agent invocation, matches Assistant pattern |

## Related Agents

- **assistant** - Similar orchestration pattern for PA workflow
- **functional-analyst** - Invoked via project-manage for requirements
- **api-architect** - Invoked via project-manage for API design
- **ui-ux-designer** - Invoked via project-manage for UX design
- **python-developer** - Invoked via project-manage for implementation
- **code-reviewer** - Invoked via project-manage for code review

## Related Skills

- **project** - Dispatcher that routes to project-* skills
- **project-feature** - Captures new features
- **project-status** - Shows project status snapshot
- **project-manage** - Full implementation workflow (main delegate)

## Scope Validation

- **Trigger Test**: Single trigger condition - explicit request to manage project ✓
- **Action Test**: Single output type - orchestrates project workflow, delegates to skills ✓
- **Failure Test**: Contained failure scope - stops on blocker, doesn't cascade ✓