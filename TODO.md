# TODO

## Backlog (Prioritized)

### P1 - Critical

*No critical items at this time. Plugin is operational.*

### P2 - High

- [x] **Review end-user-documenter agent** — 2026-04-30
  - Root cause: Agent had too many conflicting instructions causing it to describe actions instead of executing tools
  - Fixed by:
    1. Simplifying instructions to "execute tools immediately"
    2. Reducing "CRITICAL REQUIREMENT" sections that created confusion
    3. Matching functional-analyst's direct tool execution pattern
  - Note: Session caches agent definitions - start new session to verify fix
  - Acceptance: Agent uses tools and creates documentation files

- [ ] **pa-email skill update for MCP server features**
  - Update pa-email to use new email MCP server capabilities
  - Remove deduplication logic (move now expunges from inbox)
  - Mark messages as read before moving
  - Simplified inbox handling: only unhandled messages remain
  - Acceptance: pa-email skill updated, deduplication code removed, tests pass
  - Blocks: Async communication pattern (P3)

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

- [ ] **Document scripts centralization pattern in C3 documentation**
  - Explain distinction between:
    - `bin/` - simple shell scripts (statusline, etc.)
    - `scripts/` - self-contained Python packages with pyproject.toml
    - Skill-specific scripts - scripts bundled within skills
  - Update CLAUDE.md and README.md
  - Acceptance: Documentation clearly explains when to use each approach

- [ ] **Migrate email MCP server to scripts/**
  - Move email/ MCP server to scripts/email-mcp/
  - Update all references in skills and agents
  - Ensure plugin paths still resolve correctly
  - Acceptance: Email MCP server operational from new location

- [ ] **Improve README skill**
  - Review all README files in skills/ and agents/
  - Consolidate clean way of working for documentation
  - Create templates for consistent skill/agent documentation
  - Establish workflow guidelines for README updates
  - Acceptance: Templates created, guidelines documented, READMEs reviewed

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
  - Depends on: pa-email update (P2), CronCreate/ScheduleWakeup tools

- [ ] **CronCreate, ScheduleWakeup tools for c3:assistant**
  - Add CronCreate tool to create scheduled tasks/cron jobs
  - Add ScheduleWakeup tool to schedule agent reactivation at specific times
  - Enable assistant to handle time-based automation and follow-ups
  - Acceptance: Tool definitions integrated into assistant agent
  - Blocks: Async communication pattern follow-up handling

- [ ] **Researcher agent improvement**
  - Agent should always ask user where to store new research
  - Only skip prompt if location explicitly provided in startup prompt
  - Prevents research from being lost or misplaced
  - Acceptance: Updated agent definition with location prompt behavior

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

- [ ] **Create plugin-script skill**
  - Document centralized scripts pattern as a reusable skill
  - Include: folder structure, pyproject.toml template, uv run invocation
  - Enable other projects to follow the same pattern
  - Acceptance: Skill created with template and guidelines

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

- [x] **Report tox-uv deps/extras bug upstream** — 2026-05-04
  - Researched tox-uv behavior: uses `--no-deps` for package install
  - Created bug report draft at research/tox-uv-bug-report.md
  - Filing skipped by user choice (report ready when needed)
  - Acceptance: ✓ Research complete, report drafted

- [x] **Review scripts centralization implementation** — 2026-05-04
  - Reviewed migration to scripts/markdown-to-pdf/
  - Fixed documentation inconsistencies (H1, H2, M1, M2)
  - All references updated to correct paths
  - Acceptance: ✓ Feedback provided, documentation fixed

- [x] Ensure that C3 skills and agents reference each other with the c3: plugin prefix — 2026-04-28
- [x] **Business Analyst Agent** (processed 2026-04-29) — moved to P3 backlog
- [x] **CronCreate/ScheduleWakeup tools** (processed 2026-04-29) — moved to P3 backlog
- [x] **Researcher agent improvement** (processed 2026-04-29) — moved to P3 backlog
- [x] **pa-email update for MCP features** (processed 2026-04-29) — moved to P2 backlog
- [x] **Async communication pattern** (processed 2026-04-29) — moved to P3 backlog
- [x] **Business Analyst Agent development** — 2026-04-29 (created agents/business-analyst.md with BRD templates, user journey maps, process models)
- [x] **c3: convert symlink installation to plugin(s)** — 2026-04-20
- [x] **c3: develop "develop-plugin" skill** — 2026-04-20 (created `plugin-development` skill)
- [x] **Email GW MCP server** — 2026-04-20 (created `email/` with 9 tools, security hardened)
- [x] **Scripts centralization (initial implementation)** — 2026-05-04 (migrated markdown-to-pdf to scripts/ structure)