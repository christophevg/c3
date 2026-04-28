# TODO

## User Input

- [x] Ensure that C3 skills and agents reference each other with the c3: plugin prefix — 2026-04-28
- [ ] add CronCreate, ScheduleWakeup tools to c3:assistant
- [ ] improve the researcher agent to always ask the user where to store the new research (if the information is not explicitly provided in the initial start-up prompt). 
- [ ] update pa-email, to use new email MCP server features to avoid deduplication logic: move message now actually (should) move the message, expunging it from the inbox, which make only unhandled messages available in the inbox, also before moving, mark messages as read, which should also be available now.
- [ ] all C3 agents should be also able to communicate in an async way. e.g. allow for an assistant agent to capture questions and provide answers - in the meantime, the assistant will return these questions to the user e.g. via email, read the replies and provide the answers back to the agents awaiting user input, but now from the assistant.
  so the interaction pattern becomes:
    user <- email -> assistant <--> agents
  a typical workflow would be:
    - user sends an email to assistant, asking to add a feature request to the TODO backlog of a project, indicating it should be processed immediately. 
    - the agent adds the feature to the TODO list of the project
    - the agent then spawns a project-management agent to manage the project
    - the project management agent sees the unsorted new feature request and spawns a functional analyst to investigate it
    - the functional analyst has additional questions and provides them as feedback
    - the feedback is returned to the assistant, who replies to the user with the functional assistant's questions
    - the user replies with his answers
    - the assistant provides the answers to the project manager who provides them to the functional analyst to continue.
    - Note: this pattern should be generic for all agents that might require input during the project-management phase

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

### P3 - Medium

- [ ] **Python style guidelines enhancement**
  - Add function length limits to python skill
  - Add guidance: avoid comments that rephrase next function call (e.g., "# start a session" before `start_session()`)
  - Create automated check workflow (integrate with ruff?)
  - Acceptance: Updated python/SKILL.md with new patterns
  - Reference: analysis/python-coding-guidelines-reference.md

- [ ] **Brainstorming agent research**
  - Research https://mcpmarket.com/tools/skills/brainstorming-design-specifier
  - Compare with existing functional-analyst agent
  - Determine if unique value or should extend existing agent
  - Acceptance: Research report with recommendation

- [ ] **Personal Assistant Agent design**
  - Review requirements from NOTES.md
  - Design dedicated PA agent (or enhance existing assistant agent)
  - Acceptance: Design document or updated agent definition

### P4 - Low

- [ ] **Research: agentskills.io**
  - Investigate skill design patterns and best practices
  - May inform future skill development
  - Acceptance: Research report in research/

- [ ] **Research: Claude Code ecosystem**
  - Investigate claude-code-system-prompts (understanding internals)
  - Investigate claude-toolshed and claude-marketplace (MCP ecosystem)
  - Batch these related research items together
  - Acceptance: Research report comparing approaches

- [ ] **Research: markitdown**
  - Evaluate Microsoft's markitdown tool
  - Potential utility for markdown processing workflows
  - Acceptance: Research report with recommendation

- [ ] **Curate python-coding-guidelines-reference.md**
  - Review and filter reference document
  - Extract actionable patterns for python skill
  - Acceptance: Updated reference or removed if not needed

- [ ] **Set up MkDocs Material documentation site for C3**
  - Already in backlog, valuable but not urgent

## Done

- [x] **c3: convert symlink installation to plugin(s)** — 2026-04-20
- [x] **c3: develop "develop-plugin" skill** — 2026-04-20 (created `plugin-development` skill)
- [x] **Email GW MCP server** — 2026-04-20 (created `email/` with 9 tools, security hardened)
