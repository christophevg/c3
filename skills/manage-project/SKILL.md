---
name: manage-project
description: Use this skill to manage the entire project workflow, orchestrating specialized agents (functional analyst, API architect, UI/UX designer) to ensure proper analysis, design, implementation, and review of all tasks. Handles both new features and bug fixes with appropriate workflows.
---

# Manage Project

This skill is invoked by the user to manage the entire project workflow, orchestrating specialized agents (functional analyst, API architect, UI/UX designer) to ensure proper analysis, design, implementation, and review of all tasks.

## Task Type Detection

Before starting, detect whether the task is a **feature** or a **bug**:

| Task Type | Indicators |
|-----------|------------|
| **Bug** | "fix", "bug", "issue", "broken", "error", "doesn't work", "crash", "fails" |
| **Feature** | "add", "create", "implement", "build", "new", "feature", "enhance" |

**If the task is a BUG:**
- Use the **Bug Fixing Workflow** (see below)
- Invoke the **bug-fixing skill** for the specialized workflow

**If the task is a FEATURE:**
- Use the **Feature Development Workflow** (continue to Phase 0)

---

## Bug Fixing Workflow

When the task is identified as a bug, invoke the **bug-fixing skill** for the complete workflow:

### Phase B1: Bug Intake

1. **Parse bug description** from:
   - Free-form text
   - Issue reference (e.g., "#123")
   - Bug report file path

2. **Detect project context**:
   - Language and framework
   - Test infrastructure
   - Coding conventions

### Phase B2: Bug Analysis

3. **Invoke functional-analyst agent** to:
   - Review bug validity and scope
   - Confirm bug exists or reject with reason
   - Flag if UI changes are involved

4. **Create bug analysis report**:
   - Path: `docs/bug-analysis/{bug-id}.md`
   - Post as comment if issue/ticket exists

### Phase B3: Root Cause Investigation

5. Apply systematic debugging:
   - Isolate, gather information, form hypotheses
   - Use 5 Whys (simple) or Fishbone (complex)
   - Document root cause

### Phase B4: Test Creation (TDD)

6. **Create failing test first**:
   - Determine test type (unit/integration/E2E)
   - Test demonstrates bug (passes with incorrect behavior)

### Phase B5: Fix Implementation

7. **Invoke python-developer agent** to:
   - Implement minimal fix
   - Update test to expect correct behavior
   - Run all tests

### Phase B6: Implementation Review Cycle

8. **Invoke review agents** (MANDATORY):
   - functional-analyst: Functional correctness
   - ui-ux-designer: UI changes (if flagged)
   - code-reviewer: Code quality and patterns

9. **Handle rejections**:
   - Iterate with feedback (max 2 rounds)
   - Return to Phase B5 if fixes needed

### Phase B7: Documentation & Closure

10. **Complete bug fix**:
    - Update bug analysis report
    - Ensure regression test in codebase
    - Document commit message
    - Close issue or mark resolved

---

## Feature Development Workflow

When the task is identified as a feature, follow this sequential workflow:

### Phase 0: Analysis Cache Check

Before running analysis phases, check for valid cached analysis:

#### Cache Validation Steps

1. **Check for session file**: Look for `analysis/.session`

2. **Verify completeness**: All required analyst documents exist:
   - `analysis/functional.md` (required)
   - `analysis/api.md` (required for API work)
   - `analysis/ui-ux.md` (required for UI work)

3. **Verify freshness**: Session created within threshold
   - Default: Same calendar day (00:00 to 23:59)
   - Check `created` timestamp in session file

4. **Verify integrity**: Source files unchanged since analysis:
   - Compute checksum of `README.md`
   - Compute checksum of `TODO.md`
   - Compare with checksums in session file

#### If Valid Cache Exists

Report to user:
```
Recent analysis found (created: {timestamp}).
Analysts completed: {list}
Source files unchanged: README.md, TODO.md

Skip re-analysis and proceed to implementation?
- "yes" or "skip" — Skip analysis, proceed to Phase 4
- "no" or "run" — Run fresh analysis (Phase 1)
- "show" — Show cached analysis summary
```

**User responses:**
- **yes/skip**: Skip to Phase 4, load cached analysis context
- **no/run**: Proceed with Phase 1 (fresh analysis)
- **show**: Display summary of cached analysis, then ask again

#### If Invalid/Missing Cache

Proceed with Phase 1 (fresh analysis).

**Invalid cache conditions:**
- Session file missing
- Required analyst documents missing
- Source file checksums mismatch
- Session created on different calendar day

#### Force/Skip Flags

Support explicit user control:
- `/manage-project --skip-analysis` — Skip analysis (use cached, no confirmation)
- `/manage-project --force-analysis` — Force re-analysis (ignore cache)

---

### Phase 1: Functional Analysis

1. **Invoke the functional-analyst agent** to:
  - Review requirements in README.md
  - Review previous functional analysis reports in `analysis/` folder
  - Validate if tasks in TODO.md are up-to-date and cover all requirements
  - Interview the user to clarify aspects if needed
  - Create or update the functional analysis document in `analysis/`
  - Update the backlog (TODO.md) with atomic, well-defined tasks

### Phase 2: Cross-Domain Review

2. **Invoke api-architect agent** to:
  - Review the most recent functional analysis
  - Review the current backlog (TODO.md)
  - Provide API design perspective and improvements
  - **Create analysis document in `analysis/` folder** (mandatory)
  - Update TODO.md with API-related considerations

  **Note**: The api-architect MUST be invoked for ANY task involving:
  - API endpoints (creating, modifying, extending)
  - Data models and schemas
  - Authentication/authorization design
  - API refactoring

3. **Invoke ui-ux-designer agent** to:
  - Review the most recent functional analysis
  - Review the current backlog (TODO.md)
  - Provide UX/UI perspective and improvements
  - Update TODO.md with UI/UX-related considerations

### Phase 3: Consensus and Backlog Finalization

4. **Facilitate agent agreement**:
  - Ask all three agents (functional-analyst, api-architect, ui-ux-designer) to confirm the backlog is valid
  - If agents disagree, coordinate resolution until consensus is reached
  - Create a consensus summary report in the `reporting/` folder, in a subfolder with the name of the task and give it the name "consensus.md".
  - Only proceed to implementation when all agents agree

5. **Create analysis session file**:

After consensus is reached, create `analysis/.session`:

```yaml
created: {ISO timestamp}
project: {project name from README.md or directory}
analysts:
  - functional-analyst
  - api-architect
  - ui-ux-designer
checksums:
  README.md: {sha256 hash}
  TODO.md: {sha256 hash}
consensus: {path to consensus.md}
tasks:
  - {task-1.1}
  - {task-1.2}
  - ...
```

This session file enables cache validation in future invocations.

---

### Phase 4: Task Implementation Loop

For each task in the backlog (in order), execute the following steps:

5. **Enter plan mode**: Enter plan mode and:
  - Create a detailed implementation plan for the current task
  - Present the plan for user approval
  - Store the plan in the `reporting/`, in a subfolder with the name of the task and give it the name "plan.md".

6. **Check for domain-specific skills** (BEFORE implementation):
  - **CRITICAL**: Before exploring code or running one-off scripts, check if a domain-specific skill exists:
    - `textual` - Textual TUI framework widgets and patterns
    - `rich` - Rich console output
    - `database` - MongoDB database operations
    - `fire` - Fire CLI framework
    - `baseweb` / `vuetify` - Web UI frameworks
  - If a skill exists for the framework/domain, **invoke it first** to get API knowledge and patterns
  - This saves significant exploration time by providing consolidated knowledge

7. **Implementation**:
  - Invoke the python-developer agent (or appropriate specialized agent) to implement the task
  - Instruct the agent to follow general agent instructions found in `AGENTS.md` and `CLAUDE.md`, as well as python, baseweb, fire and database skills.
  - **If the task involves API work**: First invoke api-architect to design/review the API, ensure analysis document is created
  - **The developer agent MUST run tests and verify all pass before completing** - do not run tests yourself
  - Provide the developer with the task details from TODO.md and relevant analysis documents
  - The developer agent handles all coding work

8. **Implementation Review Cycle (MANDATORY)**:
  ⚠️ **This step is MANDATORY and cannot be skipped.**

  - Invoke functional-analyst to review the implementation for functional correctness
  - Invoke api-architect to review API design compliance
  - Invoke ui-ux-designer to review UI/UX aspects
  - Invoke code-reviewer to review coding aspects
  - If any agent finds issues, coordinate fixes by returning to step 7
  - Repeat until all three agents approve
  - Only proceed to step 9 when ALL agents have explicitly approved

9. **Task Completion**:
  - Mark the task as completed
  - Move the completed task from the "Backlog" section to the "Done" section in TODO.md
  - Ensure the `reporting/` folder exists
  - Create a summary report in `reporting/` folder, in a subfolder with the name of the task and give it the name "summary.md", including:
    - What was implemented
    - Key decisions made
    - Lessons learned
    - Files modified

10. **Commit Changes**:
  - Ask the user to commit changes or provide commit guidance
  - Use conventional commit message format

11. **Exit plan mode**: Exit plan mode.

12. **Repeat**: Continue with the next task from step 5 until all tasks are complete.

---

## Session File Format

The `analysis/.session` file tracks analysis state for cache validation:

```yaml
created: 2026-04-09T10:30:00Z
project: my-project
analysts:
  - functional-analyst
  - api-architect
  - ui-ux-designer
checksums:
  README.md: sha256:abc123def456...
  TODO.md: sha256:789abc012def...
consensus: reporting/my-task/consensus.md
tasks:
  - task-1.1
  - task-1.2
  - task-2.1
```

### Fields

| Field | Description |
|-------|-------------|
| created | ISO timestamp when analysis was completed |
| project | Project name (from README.md or directory) |
| analysts | List of agents that completed analysis |
| checksums | SHA256 hashes of source files |
| consensus | Path to consensus document |
| tasks | List of task IDs from TODO.md |

### Checksum Calculation

Use SHA256 hash of file content:
```bash
sha256sum README.md
sha256sum TODO.md
```

Store as: `sha256:{hash}`

---

## Cache Invalidation

The analysis cache is invalidated when:

| Condition | Reason |
|-----------|--------|
| Session file missing | No previous analysis |
| Analyst document missing | Incomplete analysis |
| README.md checksum mismatch | Requirements changed |
| TODO.md checksum mismatch | Tasks changed |
| Different calendar day | Stale analysis |
| User requests `--force-analysis` | Explicit override |

### Handling Invalidation

When cache is invalid:
1. Delete the session file if it exists
2. Proceed with Phase 1 (fresh analysis)
3. Create new session file after Phase 3

---

## Agent Invocation

When invoking specialized agents, use clear prompts that specify:
- The current phase of the workflow
- What documents to review (AGENTS.md, CLAUDE.md, README.md, analysis/, TODO.md)
- What deliverables are expected
- Any specific concerns or focus areas

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

## Communication with User

- Provide clear status updates at each phase transition
- Report any blockers or issues that require user input
- Summarize agent findings and decisions
- When cached analysis found, report details and ask for confirmation

## File Conventions

| File | Path |
|------|------|
| Analysis documents | `analysis/{topic}.md` |
| Analysis session | `analysis/.session` |
| Consensus Summary | `reporting/{task-name}/consensus.md` |
| Plan | `reporting/{task-name}/plan.md` |
| Implementation review report | `reporting/{task-name}/{topic}-review.md` |
| Development summary report | `reporting/{task-name}/development-summary.md` |
| Implementation summary report | `reporting/{task-name}/summary.md` |
| Bug analysis | `docs/bug-analysis/{bug-id}.md` |

## Notes

- The functional-analyst owns the TODO.md structure
- Domain agents (api-architect, ui-ux-designer) contribute to TODO.md through the functional-analyst
- Resolve conflicts between domain recommendations based on project priorities
- Ensure all tasks have verifiable acceptance criteria before implementation
- **For bugs**: The bug-fixing skill handles the complete workflow including TDD (test first)
- **For features**: Follow the feature development phases with API/UX design reviews
- Both workflows end with the implementation review cycle (functional, API/UX, code)
- **Analysis cache**: When valid cache exists, offer to skip re-analysis for efficiency
- **When in doubt**: Run fresh analysis. Cost of re-analysis is time; cost of stale analysis is wrong implementations.

## Documentation Updates

After completing a batch of tasks (e.g., a phase), update documentation:

1. **Update API reference** in `docs/api/` for new public APIs
2. **Update changelog** in `docs/development/changelog.md`
3. **Update showcase** if features were demonstrated
4. **Ask user to update screenshot** if showcase changed:
   - Run `make screenshot` to capture current showcase
   - Verify screenshot shows new features
   - Copy to `docs/_static/` for documentation

### Documentation Skill

For comprehensive documentation setup and maintenance, use the `documentation` skill:
- Sets up Sphinx for readthedocs.org
- Creates API reference pages
- Maintains changelog and guides