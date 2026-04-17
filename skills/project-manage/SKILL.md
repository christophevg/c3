---
name: project-manage
description: Use this skill to manage the entire project workflow, orchestrating specialized agents (functional analyst, API architect, UI/UX designer) to ensure proper analysis, design, implementation, and review of all tasks. Handles both new features and bug fixes with appropriate workflows. Examples: "Start working on the project", "Implement the next task", "Fix the authentication bug".
---

# Manage Project

This skill is invoked by the user to manage the entire project workflow, orchestrating specialized agents to ensure proper analysis, design, implementation, and review of all tasks.

## Workflow Overview

```
User Request
    │
    ▼
Task Type Detection ──── Bug ───► Bug Fixing Workflow
    │
    ▼ Feature
Project State Detection
    │
    ├── New Project ───────────► Phase 1A (Analysis)
    │                                  │
    │                                  ▼
    │                             Research (conditional)
    │                                  │
    ├── Incomplete Setup ───────► Phase 1B (Review)
    │                                  │
    │                                  ▼
    │                             Research (conditional)
    │                                  │
    └── Ready for Work ─────────► Check Unsorted Items
                                       │
                                       ├── Has Unsorted ──► Ask: Sort or Skip?
                                       │                            │
                                       │                            ├── Sort ──► Functional Analysis
                                       │                            │                   │
                                       │                            └── Skip ─────────────┤
                                       │                                                │
                                       └── No Unsorted ──────────────────────────────────┤
                                                                                        │
                                                                                        ▼
                                                                                Propose Next Task
                                                                                        │
                                                                                        ▼
                                                                                Task Scope Classification
                                                                                        │
                                                                                        ▼
                                                                                Phase 2 (Domain Review)
                                                                                        │
                                                                                        ▼
                                                                                Phase 3 (Consensus)
                                                                                        │
                                                                                        ▼
                                                                                Phase 4 (Implementation)
                                                                                        │
                                                                                        ▼
                                                                                Review Cycle (parallelized)
                                                                                        │
                                                                                        ▼
                                                                                    Commit
```

---

## Task Type Detection

Before starting, detect whether the task is a **feature** or a **bug**:

| Task Type | Indicators |
|-----------|------------|
| **Bug** | "fix", "bug", "issue", "broken", "error", "doesn't work", "crash", "fails" |
| **Feature** | "add", "create", "implement", "build", "new", "feature", "enhance" |

**If the task is a BUG:**
- Invoke the **bug-fixing skill** for the complete TDD-based workflow
- See `references/bug-workflow-integration.md` for how bug workflow integrates with project management

**If the task is a FEATURE:**
- Use the **Feature Development Workflow** (continue to Phase 0)

---

## Feature Development Workflow

When the task is identified as a feature, follow this sequential workflow:

### Phase 0: Project State Detection

Check the project's analysis artifacts to determine the appropriate workflow:

| State | `analysis/functional.md` | `TODO.md` | Action |
|-------|--------------------------|-----------|--------|
| **New Project** | Missing | Missing | Initial Analysis (Phase 1A) |
| **Incomplete Setup** | Exists | Missing | Review and Backlog (Phase 1B) |
| **Ready for Work** | Exists | Exists | Check for Unsorted Items |

#### State Detection Steps

1. Check if `analysis/functional.md` exists
2. Check if `TODO.md` exists with prioritized tasks

---

### Phase 1A: Initial Functional Analysis (New Project)

When `analysis/functional.md` or `TODO.md` is missing:

1. **Invoke functional-analyst agent** to:
   - Review high-level functional requirements (README.md, existing documentation)
   - Review existing code structure if available
   - Interview user to clarify topics needing more information
   - Create `analysis/functional.md` with comprehensive functional analysis
   - Create `TODO.md` with prioritized backlog of atomic, well-defined tasks

2. **Conditional: Invoke researcher agent when**:
   - Functional analysis identifies gaps needing best practices proposals
   - User explicitly requests research to address functional-analyst questions
   - Technology choice needs evaluation and recommendations

   **Researcher delivers**:
   - Research findings in `research/{topic}.md`
   - Technology recommendations with pros/cons
   - Best practices proposals for identified gaps

Then proceed to **Task Scope Classification** (below).

---

### Phase 1B: Review and Backlog Creation (Existing Analysis)

When `analysis/functional.md` exists but `TODO.md` is missing:

1. **Invoke functional-analyst agent** to:
   - Review existing `analysis/functional.md`
   - Review current project state
   - Interview user to update understanding if needed
   - Create `TODO.md` with prioritized backlog

2. **Conditional: Invoke researcher agent when**:
   - Existing analysis needs technology investigation
   - User requests research for specific questions

Then proceed to **Task Scope Classification** (below).

---

### Task Scope Classification

After Phase 1A or 1B completes, classify the task scope:

| Scope | Indicators | Required Domain Agents |
|-------|------------|------------------------|
| **Backend only** | "API", "endpoint", "backend", "data model", no UI | api-architect, security-engineer* |
| **Frontend only** | "UI", "UX", "frontend", "component", "page", no backend | ui-ux-designer |
| **Full stack** | Both backend and frontend mentioned | api-architect, ui-ux-designer, security-engineer* |
| **Documentation only** | "document", "readme", "guide" | end-user-documenter |
| **Research only** | "research", "investigate", "evaluate" | researcher |

#### Security Task Detection

Include `security-engineer` when task involves:
- Authentication or authorization changes
- Sensitive data handling (PII, credentials, payments)
- External API integrations
- User input processing
- File operations
- Configuration changes affecting security

#### Ready for Work State

When both `analysis/functional.md` and `TODO.md` exist:

**Step 1: Check for Unsorted Items**

Read `TODO.md` and check for an `## Unsorted` section at the top. Unsorted items are quick ideas the user captured but haven't been analyzed and integrated into the prioritized backlog.

**Step 2: Determine Next Action**

| Condition | Action |
|-----------|--------|
| No unsorted items | Proceed directly to proposing next backlog task |
| Unsorted items exist | Ask user whether to sort unsorted items first |

**If unsorted items exist, use AskUserQuestion tool:**

```
Question: "Found {count} unsorted item(s) in TODO.md. These are quick ideas not yet analyzed. How would you like to proceed?"

Options:
- "Sort unsorted items first" — Run functional analysis to integrate them into backlog
- "Show next backlog task" — Proceed with existing prioritized tasks
- "Show all tasks" — Display both unsorted and backlog items
```

**Step 3: Handle User Choice**

- **"Sort unsorted items first"**: Invoke functional-analyst to analyze each unsorted item and integrate into prioritized backlog, then propose next task
- **"Show next backlog task"**: Proceed to propose task selection (below)
- **"Show all tasks"**: Display full TODO.md and ask again

**Step 4: Propose Next Task (when no unsorted items or user chose to skip)**

**Use AskUserQuestion tool to propose next task:**

```
Question: "Project analysis complete. Next task from backlog: {task-id} - {task-title}. Proceed with this task?"

Options:
- "Yes, start implementation" (Recommended)
- "Show all tasks in backlog"
- "Run fresh analysis"
```

If user approves, classify task scope (see table above) and proceed to **Phase 2**.

---

### Phase 2: Cross-Domain Review

Invoke domain agents **based on task scope classification**.

#### Parallel Invocation

Domain agents run in **parallel** where independent:
- `api-architect` + `security-engineer` (both review architecture aspects)
- `ui-ux-designer` (independent from backend reviews)

#### Agent Invocation by Scope

**For Backend only:**
```
Invoke api-architect: Review API design, create analysis document
Invoke security-engineer: Review security architecture (if security-related)
```

**For Frontend only:**
```
Invoke ui-ux-designer: Review UX design, create analysis document
```

**For Full stack:**
```
Invoke api-architect: Review API design, create analysis document
Invoke ui-ux-designer: Review UX design, create analysis document
Invoke security-engineer: Review security architecture (if security-related)
```

#### Each Domain Agent:

2. **Invoke api-architect agent** (if Backend or Full stack):
   - Review the most recent functional analysis
   - Review the current backlog (TODO.md)
   - Provide API design perspective and improvements
   - **Create analysis document in `analysis/` folder** (mandatory)
   - Update TODO.md with API-related considerations

3. **Invoke ui-ux-designer agent** (if Frontend or Full stack):
   - Review the most recent functional analysis
   - Review the current backlog (TODO.md)
   - Provide UX/UI perspective and improvements
   - Update TODO.md with UI/UX-related considerations

4. **Invoke security-engineer agent** (if security-related):
   - Review the most recent functional analysis
   - Review the current backlog (TODO.md)
   - Provide security architecture perspective
   - Create analysis document in `analysis/` folder
   - Update TODO.md with security considerations

---

### Phase 3: Consensus and Backlog Finalization

5. **Facilitate agent agreement among all invoked domain agents**:
   - Collect feedback from all domain agents invoked in Phase 2
   - Coordinate resolution if agents disagree
   - Create a consensus summary report in `reporting/{task-name}/consensus.md`
   - Only proceed to implementation when all invoked agents approve

**Note:** Not all tasks require all agents. Consensus is among agents that were invoked.

---

### Phase 4: Task Implementation Loop

For each task in the backlog (in order), execute the following steps:

#### Step 5: Plan Mode

Enter plan mode and:
- Create a detailed implementation plan for the current task
- Present the plan for user approval
- Store the plan in `reporting/{task-name}/plan.md`

#### Step 6: Check Domain Skills

**CRITICAL**: Before exploring code or running one-off scripts, check if a domain-specific skill exists:

| Skill | When to Use |
|-------|-------------|
| `textual` | Textual TUI framework widgets and patterns |
| `rich` | Rich console output |
| `database` | MongoDB database operations |
| `fire` | Fire CLI framework |
| `baseweb` / `vuetify` | Web UI frameworks |
| `python` | Python coding standards (always relevant) |

If a skill exists for the framework/domain, **invoke it first** to get API knowledge and patterns. This saves significant exploration time.

#### Step 7: Implementation

Invoke the `python-developer` agent (or appropriate specialized agent) to:
- Implement the task following the plan
- Follow general agent instructions in `AGENTS.md` and `CLAUDE.md`
- Follow domain skills (python, baseweb, fire, database, etc.)
- **Run tests and verify all pass before completing**
- Provide the developer with task details from TODO.md and relevant analysis documents

#### Step 8: Implementation Review Cycle

⚠️ **This step is MANDATORY and cannot be skipped.**

See `references/review-cycle.md` for detailed review sequence.

**Step 8a: Functional Review (Blocking)**
- Invoke functional-analyst to review functional correctness
- Must pass before proceeding to domain reviews
- If rejected: return to Step 7 with feedback

**Step 8b: Domain Reviews (Parallel, based on scope)**

Invoke domain agents that were invoked in Phase 2:
- `api-architect`: API design compliance (if Backend or Full stack)
- `ui-ux-designer`: UX compliance (if Frontend or Full stack)
- `security-engineer`: Security review (if security-related)

**Step 8c: Quality Reviews (Parallel)**
- `code-reviewer`: Code quality and patterns
- `testing-engineer`: Test coverage and quality

**Step 8d: Documentation (If User-Facing)**

For tasks with user-facing changes:
- Invoke `end-user-documenter` to create/update documentation
- Documentation must be synced with implementation

**Step 8e: Handle Rejections**
- Collect all rejection feedback
- Return to Step 7 with consolidated feedback (max 2 rounds)
- Only proceed to Step 9 when ALL invoked agents approve

#### Step 9: Task Completion

- Mark the task as completed
- Move the completed task from "Backlog" to "Done" section in TODO.md
- Ensure `reporting/` folder exists
- Create summary report in `reporting/{task-name}/summary.md` including:
  - What was implemented
  - Key decisions made
  - Lessons learned
  - Files modified

#### Step 10: Commit Changes

- Ask user to commit changes or provide commit guidance
- Use conventional commit message format

#### Step 11: Exit Plan Mode

Exit plan mode.

#### Step 12: Repeat

Continue with next task from Step 5 until all tasks complete.

---

## Review Cycle Execution Order

```
Step 1: functional-analyst     ← BLOCKING (must pass first)
    │
    ▼
Step 2: Domain Reviews         ← PARALLEL (independent perspectives)
    ├── api-architect
    ├── ui-ux-designer
    └── security-engineer
    │
    ▼
Step 3: Quality Reviews        ← PARALLEL (independent perspectives)
    ├── code-reviewer
    └── testing-engineer
    │
    ▼
Step 4: Documentation          ← IF user-facing
    └── end-user-documenter
```

---

## Agent Invocation

When invoking specialized agents, use clear prompts that specify:
- The current phase of the workflow
- What documents to review (AGENTS.md, CLAUDE.md, README.md, analysis/, TODO.md)
- What deliverables are expected
- Any specific concerns or focus areas

---

## When to Use Bug-Fixing Workflow

Use the Bug Fixing Workflow when:
- User explicitly says "fix bug", "there's a bug", "debug this"
- Task description contains bug indicators (error, crash, broken, fails)
- Issue reference is provided (e.g., "#123", "JIRA-456")
- Current behavior doesn't match expected behavior

Use the Feature Development Workflow when:
- User says "add", "create", "implement", "build new"
- Task is about new functionality
- Requirements describe desired features

---

## Communication with User

- Provide clear status updates at each phase transition
- Report any blockers or issues that require user input
- Summarize agent findings and decisions
- When project is ready for work, propose next task from backlog

### Using AskUserQuestion Tool

**CRITICAL**: When asking the user for input and there are **limited possible answers (<7)**, use the AskUserQuestion tool instead of plain text prompts.

This applies to situations like:
- **Task approval**: "Proceed with this task?" (yes/no)
- **Workflow selection**: "Which workflow to use?" (bug/feature)
- **Priority decisions**: "Which task to prioritize?" (list of tasks)
- **Conflict resolution**: "How to resolve this issue?" (finite options)
- **Branch selection**: "Which branch?" (list of branches)

---

## File Conventions

| File | Path |
|------|------|
| Functional analysis | `analysis/functional.md` |
| API analysis | `analysis/api-{topic}.md` |
| UX analysis | `analysis/ux-{topic}.md` |
| Security analysis | `analysis/security-{topic}.md` |
| Research findings | `research/{topic}.md` |
| Technology recommendations | `research/{topic}/recommendations.md` |
| Consensus summary | `reporting/{task-name}/consensus.md` |
| Plan | `reporting/{task-name}/plan.md` |
| Implementation review report | `reporting/{task-name}/{topic}-review.md` |
| Task summary | `reporting/{task-name}/summary.md` |
| Bug analysis | `docs/bug-analysis/{bug-id}.md` |

### TODO.md Structure

```markdown
# TODO

## Unsorted

- [ ] Quick idea 1 (captured but not yet analyzed)
- [ ] Quick idea 2 (needs functional analysis)

## Backlog (Prioritized)

### P1 - Critical

- [ ] Critical task with clear acceptance criteria

### P2 - High

- [ ] High priority task

### P3 - Medium

- [ ] Medium priority task

### P4 - Low

- [ ] Low priority task

## Done

- [x] Completed task
```

**Unsorted Section Rules:**
- Placed at the top of TODO.md
- Contains items that need functional analysis before prioritization
- Items are short ideas without acceptance criteria
- When analyzed, functional-analyst moves them to appropriate priority in Backlog
- Optional section — only present when user has captured unsorted ideas

---

## Notes

- The functional-analyst owns the TODO.md structure
- Domain agents (api-architect, ui-ux-designer, security-engineer) contribute to TODO.md through the functional-analyst
- Resolve conflicts between domain recommendations based on project priorities
- Ensure all tasks have verifiable acceptance criteria before implementation
- **For bugs**: The bug-fixing skill handles the complete workflow including TDD (test first)
- **For features**: Follow the feature development phases with domain design reviews
- **Research** is conditional - invoke when gaps identified or technology choices needed
- **Security review** is scoped to security-related tasks
- **Documentation** is part of task completion for user-facing changes
- **Parallel reviews** improve efficiency without sacrificing quality
- **User can request reanalysis**: Use "reanalyze" option when proposing next task to run fresh analysis
- **Unsorted items**: Quick ideas captured at top of TODO.md that need analysis before prioritization. Offer to sort them before working on backlog, but allow user to skip and proceed with prioritized tasks.

---

## Agent Quick Reference

| Agent | Phase | When to Invoke |
|-------|-------|----------------|
| functional-analyst | 1A, 1B, 4 (review) | Always |
| researcher | 1A, 1B | When gaps or tech choices |
| api-architect | 2, 4 (review) | Backend or Full stack tasks |
| ui-ux-designer | 2, 4 (review) | Frontend or Full stack tasks |
| security-engineer | 2, 4 (review) | Security-related tasks |
| python-developer | 4 (implementation) | Always for Python projects |
| code-reviewer | 4 (review) | Always |
| testing-engineer | 4 (review) | Always |
| end-user-documenter | 4 (completion) | User-facing changes |

---

## Reference Files

- `references/bug-workflow-integration.md` — How bug workflow integrates with project management
- `references/review-cycle.md` — Detailed review cycle execution