# Functional Analysis - C3 Plugin

**Date:** 2026-04-20
**Status:** Active Development

## Executive Summary

C3 (Christophe's Coding Crew) is a Claude Code plugin providing a comprehensive collection of reusable skills (38) and agents (11) for Python/Baseweb development projects. The plugin follows an evolutionary development philosophy where skills and agents are created through real needs, refined through use, and distributed when stable.

## Project Scope

### In Scope

1. **Skill Development** — Creating and maintaining domain expertise skills (Python, PyMongo, Baseweb, Textual, Rich, Fire)
2. **Agent Ecosystem** — Specialized agents for analysis, design, implementation, review, and documentation phases
3. **Project Management Workflow** — Structured feature intake and implementation workflow
4. **Personal Assistant Workflow** — Inbox processing, session management, and reply generation
5. **Plugin/MCP Development** — Guidance for creating Claude Code plugins and MCP servers
6. **Utility Skills** — Common development workflows (commit, bug-fixing, naming, documentation)

### Out of Scope

- Runtime execution environments (skills provide guidance, not execution)
- Third-party library maintenance (skills document patterns, not libraries)
- End-user application development (C3 is a meta-tool for developers)

## Current State

### Completed

- Plugin conversion from symlink-based installation to proper plugin distribution
- Plugin-development skill for creating new plugins
- MCP-server skill for MCP server development
- Personal Assistant workflow (pa, pa-inbox, pa-session, pa-outbox)
- Full project management workflow with specialized agent coordination

### Operational

All 38 skills and 11 agents are operational and actively used across multiple projects.

## Inbox Analysis

### New Capability Development

| Item | Description | Dependencies | Priority |
|------|-------------|--------------|----------|
| AI Overview skill | Browser + Google + AI Overview extraction | PlayWright research | P2 |
| Email GW MCP server | MCP server for email exchange | MCP-server skill | P2 |
| Brainstorming agent | Compare to functional analyst | Research MCPMarket tool | P3 |
| PA Agent design | Requirements from NOTES.md | None | P3 |

### Skill Enhancement

| Item | Description | Priority |
|------|-------------|----------|
| Python style guidelines | Function length limits, comment avoidance, check workflow | P3 |
| Python check workflow | Tooling integration (ruff?) for style enforcement | P3 |

### Research Tasks

| Item | Purpose | Priority |
|------|---------|----------|
| PlayWright (UI Mode) | Enabling technology for AI Overview skill | P2 |
| agentskills.io | Best practices for skill design | P3 |
| claude-code-system-prompts | Understanding Claude Code internals | P4 |
| markitdown | Markdown processing tool evaluation | P4 |
| claude-toolshed | MCP ecosystem research | P4 |
| claude-marketplace | MCP ecosystem research | P4 |

### Reference Material

| Item | Status |
|------|--------|
| python-coding-guidelines-reference.md | Filed, needs curation |

## Dependency Graph

```
AI Overview skill ──────► PlayWright research (P2)
                              │
                              └── Enabling technology

Python style ────────────► Research tooling (ruff?)
(check workflow)              │
                              └── Optional integration

Research items ──────────► May inform skill development
(agentskills.io, etc.)         │
                              └── No hard dependencies
```

## Recommendations

### High Priority (P2)

1. **AI Overview Skill** — High value for research workflows. Requires PlayWright research first.
2. **Email GW MCP Server** — Concrete deliverable with clear scope. Uses existing MCP-server skill.

### Medium Priority (P3)

3. **Python Style Enhancement** — Consolidate function length, comment avoidance, and check workflow into single task.
4. **Brainstorming Agent** — Compare with functional analyst role to determine unique value.
5. **PA Agent Design** — Enhance existing PA workflow with dedicated agent.

### Low Priority (P4)

6. **Research Exploration** — agentskills.io, markitdown, claude ecosystem items can be batched.
7. **Documentation Site** — Already in backlog, valuable but not urgent.

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Research items never convert to implementation | Set clear decision criteria before researching |
| Python style enforcement too opinionated | Make rules configurable via ruff |
| MCP ecosystem research duplicates effort | Check existing research index first |

## Success Metrics

- Skills and agents remain synchronized with README.md catalog
- Each new skill/agent follows the progressive disclosure pattern
- Plugin remains installable via marketplace
- Version numbers reflect actual changes (semantic versioning)