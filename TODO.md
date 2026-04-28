# TODO

## Inbox Input

*Empty — all items from 2026-04-20 session have been processed.*

## Email Input (2026-04-24)

- [ ] **Update pa-email skill with better error handling**
  - Fix deduplication: message IDs are folder-local, not global
  - Use content-based deduplication (subject + from + date hash)
  - Add graceful handling of MCP server errors
  - Source: Email from Christophe

- [ ] **Improve MCP server to allow marking messages as read and moving to archive (not just copy)**
  - Current behavior may be copying instead of moving
  - Need to verify move_email actually removes from source folder
  - Consider adding mark-as-read capability to email MCP server
  - Source: Email from Christophe

- [ ] **Write access test** — *verified at 2026-04-24 session*

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