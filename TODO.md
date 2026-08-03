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

## Done

- [x] **MBI Intake Layer Implementation** — 2026-06-12
  - Approved by Christophe after research on MBI/Intake Backlog best practices
  - Research stored in: c3/research/2026-06-12-mbi-intake-backlog/
  - Memory: memory/c3-intake-backlog-mbi.md
  - Tasks:
    - [x] Create PLAN.md template in C3 (templates/PLAN.md)
    - [x] Update functional-analyst agent to ask "MBI or linear task?" during feature intake
    - [x] Create /wsjf skill for interactive WSJF scoring
    - [x] Update project-manage skill to check for PLAN.md and prioritize MBI tasks
  - Acceptance: ✅ functional-analyst can create MBIs in PLAN.md, MBI tasks scheduled at top of TODO.md

- [x] **Python style guidelines enhancement** — 2026-06-29
  - Addressed by tight-python integration into python skill
  - Added function length limits, tight code philosophy
  - Added library-first check (NIH principle)
  - Added deletion test for abstractions
  - Acceptance: ✅ Updated python/SKILL.md with new patterns

- [x] **Review end-user-documenter agent** — 2026-04-30
  - Root cause: Agent had too many conflicting instructions causing it to describe actions instead of executing tools
  - Fixed by:
    1. Simplifying instructions to "execute tools immediately"
    2. Reducing "CRITICAL REQUIREMENT" sections that created confusion
    3. Matching functional-analyst's direct tool execution pattern
  - Note: Session caches agent definitions - start new session to verify fix
  - Acceptance: Agent uses tools and creates documentation files

- [x] **Email MCP: auto-save sent messages to Sent folder** — 2026-06-17
  - The MCP `reply_email` and `send_email` tools send via SMTP but don't save a copy to the IMAP Sent folder
  - No `copy_email` tool exists to archive sent messages manually
  - Submitted feature request to `christophevg/simple-email-gw`: https://github.com/christophevg/simple-email-gw/issues/1
  - Until implemented, use the workaround: `send_email` with BCC to self, then move the copy to the Sent folder
  - **Source:** Christophe's email, 2026-06-17
  - **Acceptance:** Feature request submitted ✓

- [x] **Extract email MCP into standalone package: simple-email-gw** — 2026-05-07
  - Package published to PyPI as `simple-email-gw`
  - C3 now uses `uvx --from simple-email-gw mcp-server`
  - Local `email/` directory removed from repository
  - Acceptance: ✓ Package on PyPI, C3 uses uvx, email/ removed

- [x] **pa-email skill update for MCP server features** — 2026-05-04
  - Added "Simplified Inbox Handling" section
  - Clarified no deduplication logic required with UNSEEN workflow
  - Documented move_email expunge behavior (RFC 6851 MOVE)
  - Acceptance: ✓ Skill updated with simplified workflow

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
- [x] **Business Analyst Agent development** — 2026-04-29 (created agents/business-analyst.md with BRD templates, user journey maps, process models)
- [x] **c3: convert symlink installation to plugin(s)** — 2026-04-20
- [x] **c3: develop "develop-plugin" skill** — 2026-04-20 (created `plugin-development` skill)
- [x] **Email GW MCP server** — 2026-04-20 (created `email/` with 9 tools, security hardened)
- [x] **Scripts centralization (initial implementation)** — 2026-05-04 (migrated markdown-to-pdf to scripts/ structure)