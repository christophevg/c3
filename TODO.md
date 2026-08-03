# TODO

## Email Input (2026-05-14)

From: Christophe VG (contact@christophe.vg)

Topics for cross-project standardization:

1. **Unified pyproject.toml configuration**
   - All projects need consistent ruff, type checking, testing configuration
   - Example ruff config provided
   - Action: Create session in C3 with agent to analyze all projects
   - After approval: Update python-project skill and apply to all projects

2. **Standardization compliance skill**
   - New skill to check standardization application across projects
   - Produces reports like git-activity-report
   - Report on demand when asked

3. **Testing-engineer improvement**
   - Current: Produces too detailed unit tests, creating maintenance burden
   - Action: Research better guidelines for focused testing
   - Implement in testing-engineer agent

## Backlog (Prioritized)

### P1 - Critical

*No critical items at this time. Plugin is operational.*

### P2 - High

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

### P3 - Medium

- [ ] **Document scripts centralization pattern in C3 documentation**
  - Explain distinction between:
    - `bin/` - simple shell scripts (statusline, etc.)
    - `scripts/` - self-contained Python packages with pyproject.toml
    - Skill-specific scripts - scripts bundled within skills
  - Update AGENTS.md and README.md
  - Acceptance: Documentation clearly explains when to use each approach

- [ ] **Improve README skill**
  - Review all README files in skills/ and agents/
  - Consolidate clean way of working for documentation
  - Create templates for consistent skill/agent documentation
  - Establish workflow guidelines for README updates
  - Acceptance: Templates created, guidelines documented, READMEs reviewed

- [ ] **Researcher agent improvement**
  - Agent should always ask user where to store new research
  - Only skip prompt if location explicitly provided in startup prompt
  - Prevents research from being lost or misplaced
  - Acceptance: Updated agent definition with location prompt behavior

- [ ] **Brainstorming agent research**
  - Research https://mcpmarket.com/tools/skills/brainstorming-design-specifier
  - Compare with existing functional-analyst agent
  - Determine if unique value or should extend existing agent
  - Acceptance: Research report with recommendation

- [ ] **Personal Assistant Agent design**
  - Review requirements from NOTES.md
  - Design dedicated PA agent (or enhance existing assistant agent)
  - Acceptance: Design document or updated agent definition

- [ ] **Research: agentskills.io**
  - Investigate skill design patterns and best practices
  - May inform future skill development
  - Acceptance: Research report in research/

### P4 - Low

- [ ] **Create plugin-script skill**
  - Document centralized scripts pattern as a reusable skill
  - Include: folder structure, pyproject.toml template, uv run invocation
  - Enable other projects to follow the same pattern
  - Acceptance: Skill created with template and guidelines
