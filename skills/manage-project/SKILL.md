---
name: manage-project
description: Use this skill to manage the entire project workflow, orchestrating specialized agents (functional analyst, API architect, UI/UX designer) to ensure proper analysis, design, implementation, and review of all tasks.
---

# Manage Project

This skill is invoked by the user to manage the entire project workflow, orchestrating specialized agents (functional analyst, API architect, UI/UX designer) to ensure proper analysis, design, implementation, and review of all tasks.

## Workflow Overview

When activated, follow this sequential workflow:

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
  - Update TODO.md with API-related considerations

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

### Phase 4: Task Implementation Loop

For each task in the backlog (in order), execute the following steps:

5. **Enter plan mode**: Enter plan mode and:
  - Create a detailed implementation plan for the current task
  - Present the plan for user approval
  - Store the plan in the `reporting/`, in a subfolder with the name of the task and give it the name "plan.md".

6. **Implementation**:
  - Invoke the python-developer agent (or appropriate specialized agent) to implement the task
  - Instruct the agent to follow general agent instructions found in `AGENTS.md` and `CLAUDE.md`, as well as python, baseweb, fire and database skills.
  - **The developer agent MUST run tests and verify all pass before completing** - do not run tests yourself
  - Provide the developer with the task details from TODO.md and relevant analysis documents
  - The developer agent handles all coding work

7. **Implementation Review Cycle (MANDATORY)**:
  ⚠️ **This step is MANDATORY and cannot be skipped.**

  - Invoke functional-analyst to review the implementation for functional correctness
  - Invoke api-architect to review API design compliance
  - Invoke ui-ux-designer to review UI/UX aspects
  - Invoke code-reviewer to review coding aspects
  - If any agent finds issues, coordinate fixes by returning to step 6
  - Repeat until all three agents approve
  - Only proceed to step 8 when ALL agents have explicitly approved

8. **Task Completion**:
  - Mark the task as completed
  - Move the completed task from the "Backlog" section to the "Done" section in TODO.md
  - Ensure the `reporting/` folder exists
  - Create a summary report in `reporting/` folder, in a subfolder with the name of the task and give it the name "summary.md", including:
    - What was implemented
    - Key decisions made
    - Lessons learned
    - Files modified

9. **Commit Changes**:
  - Ask the user to commit changes or provide commit guidance
  - Use conventional commit message format

10. **Exit plan mode**: Exit plan mode.

11. **Repeat**: Continue with the next task from step 5 until all tasks are complete.

## Agent Invocation

When invoking specialized agents, use clear prompts that specify:
- The current phase of the workflow
- What documents to review (AGENTS.md, CLAUDE.md, README.md, analysis/, TODO.md)
- What deliverables are expected
- Any specific concerns or focus areas

## Communication with User

- Provide clear status updates at each phase transition
- Report any blockers or issues that require user input
- Summarize agent findings and decisions

## File Conventions

- Analysis documents: `analysis/{topic}.md`
- Consensus Summary: `reporting/{task-name}/consensus.md`
- Plan: `reporting/{task-name}/plan.md`
- Implementation review report: `reporting/{task-name}/{topic}-review.md`
- Development summary report: `reporting/{task-name}/development-summary.md`
- Implementation summary report: `reporting/{task-name}/summary.md`

## Notes

- The functional-analyst owns the TODO.md structure
- Domain agents (api-architect, ui-ux-designer) contribute to TODO.md through the functional-analyst
- Resolve conflicts between domain recommendations based on project priorities
- Ensure all tasks have verifiable acceptance criteria before implementation
