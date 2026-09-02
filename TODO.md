# TODO

## Unsorted

## Backlog (Prioritized)

### P1 - Critical

*No critical items at this time.*

### P2 - High

- [ ] **Shorten PR-feedback roundtrip**
  - Owner's PR comment currently travels: release-manager → project-manager → handle-pr skill → release-manager re-fetches
  - Enhancement: release-manager hands the feedback digest directly to the interpretation step (or a persistent release-manager session carries it)
  - Acceptance: one delegation hop; the feedback text arrives at interpretation once

- [ ] **Slim down bug-fix workflow**
  - Recent rework aligned the bug-fix flow with the full managed workflow, making it heavy and time-consuming
  - Define a slimmed-down fast path for day-to-day bug fixes; keep the full flow for managed projects
  - Acceptance: c3:bug-fixing supports a lightweight day-to-day mode

- [ ] **Genericize skill output locations**
  - develop-skill and by extension all skills hardcode output paths
  - Replace hardcoded paths with sensible defaults plus explicit user decision at invocation
  - Acceptance: no hardcoded output paths in skills; defaults documented and overridable

- [ ] **Split agents/skills into workflow vs optional sets**
  - Split the current flat set into: workflow-required and optional standalone (not workflow-related)
  - Enables fine-grained injection into the system prompt
  - Avoids unused agents/skills polluting the context
  - Acceptance: per-profile injection configured in yoker.toml; unused agents/skills stay out of context

- [ ] **AI Overview skill**
  - Create skill for browser-based Google search with AI Overview extraction
  - Enables research workflows with synthesized answers
  - Acceptance: Skill triggers on "AI Overview", "search with AI summary"
  - Depends on: PlayWright research (below)

- [ ] **PlayWright (UI Mode) research**
  - Investigate PlayWright UI Mode capabilities
  - Document patterns for browser automation
  - Acceptance: Research report in research/ with examples
  - Blocks: AI Overview skill
  - Research and compare to other solutions, e.g. Agent Browser (https://github.com/vercel-labs/agent-browser)

- [ ] **C3 agents async communication pattern**
  - Enable all C3 agents to communicate asynchronously with users
  - Interaction pattern: user <- email -> assistant <--> agents
  - Typical workflow:
    - User emails assistant with feature request
    - Agent adds to TODO, spawns project-management agent
    - Project manager spawns functional analyst
    - Functional analyst has questions → assistant emails user
    - User replies → assistant provides answers to agents
  - Pattern must be generic for all agents requiring input during project-management
  - Acceptance: Documented async pattern with implementation guide
  - Depends on: Scheduling/wakeup tool support in Yoker

- [ ] **C3 memory system (deferred from migration)**
  - Dedicated memory system for agents/skills, deferred from the migration
  - Valuable memory content that surfaced during the migration was incorporated into skills and the backlog

### P3 - Medium

- [ ] **Unified pyproject.toml configuration**
  - All projects need consistent ruff, type checking, testing configuration
  - Example ruff config provided (email input, 2026-05-14)
  - After approval: Update python-project skill and apply to all projects

- [ ] **Standardization compliance skill**
  - New skill to check standardization application across projects
  - Produces reports like git-activity-report
  - Report on demand when asked

- [ ] **Testing-engineer improvement**
  - Current: Produces too detailed unit tests, creating maintenance burden
  - Research better guidelines for focused testing
  - Implement in testing-engineer agent

- [ ] **Convert bash code blocks to Yoker tool calls in skills & agents**
  - Replace bash instructions to agents with Yoker tool call equivalents
  - Categories to convert: agent instructions (git, file ops, search, make)
  - Categories to keep as-is: user terminal commands, CI config, Makefile snippets, example output
  - Approach: start with `commit` skill as reference, then high-impact skills, then agents

- [ ] **Vuetify ×4 merge review (deferred from migration)**
  - Review merging vuetify-v1..v4 into one skill, owner-deferred until real use
  - Re-evaluate after real-world use of the four versioned skills

### P4 - Low

- [ ] **Document scripts centralization pattern in C3 documentation**
  - Explain distinction between: `bin/` (simple shell scripts), `scripts/` (self-contained Python packages), skill-specific scripts

- [ ] **Improve README skill**
  - Review all README files in skills/ and agents/
  - Create templates for consistent skill/agent documentation

- [ ] **Researcher agent improvement**
  - Agent should always ask user where to store new research
  - Only skip prompt if location explicitly provided in startup prompt

- [ ] **Brainstorming agent research**
  - Compare with existing functional-analyst agent
  - Determine if unique value or should extend existing agent

- [ ] **Personal Assistant Agent design**
  - Review requirements from NOTES.md
  - Design dedicated PA agent (or enhance existing assistant agent)

- [ ] **Research: agentskills.io**
  - Investigate skill design patterns and best practices
  - May inform future skill development

- [ ] **Create plugin-script skill**
  - Document centralized scripts pattern as a reusable skill
