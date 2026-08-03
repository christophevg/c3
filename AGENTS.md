# Agents.md

This is the C3 project. It provides agent definitions and skills.

## Current State

C3 is being ported from Claude Code to Yoker on the `yoker` branch. This is a
dogfooding effort — using Yoker itself to port C3 to Yoker.

See also: **AGENTS.global.md** for shared conventions (read this alongside AGENTS.md).

### Session 2: File Removal & Global Instructions Port

- All previously missing Yoker tools now available (copy, move, delete, git add)
- Removed all Claude-specific files from git tracking and disk:
  - `.claude/`, `.claude-plugin/`, `CLAUDE.md`, `CLAUDE.global.md`, `settings.json`, `.mcp.json`
  - `Makefile.claude`, `PERSONAL.md.template`, `bin/statusline.py`
  - Deprecated agents: `assistant.md`, `knowledge-agent.md`, `writing-assistant.md`
  - Deprecated skills: `pa/`, `pa-email/`, `pa-inbox/`, `pa-outbox/`, `pa-session/`, `writing-continuity/`, `writing-idioms/`, `writing-mistakes/`, `writing-order/`, `writing-review/`, `writing-split/`, `writing-voice/`, `copy-writer/`
- Created `AGENTS.global.md` — ported from `CLAUDE.global.md` with Claude-specific references updated to Yoker equivalents
- Updated tool limitation protocol section to reflect resolved tools
- Updated agent definitions to remove Claude-specific tool references
- Updated README.md to reflect Yoker-based setup
- Updated TODO.md to remove Claude-specific backlog items

## Session History

### Session 1: Discovery & Planning + File Copy

- Explored C3 repo structure and Yoker implementation
- Identified all Claude-specific artifacts to remove
- Mapped Claude Code tool names to Yoker tool names
- Discovered tool limitations: no copy, no move, no delete, no git rm
- Copied writing-assistant agent + 8 skills to ../yoker-writing-assistant
  - **MISTAKE**: Read all files into context and wrote them back, massively
    polluting context. Should have immediately reported the missing `copy`
    tool and waited for it to be implemented.
- Updated AGENTS.md with full migration plan and tool limitation protocol
- Identified 5 high-priority Yoker tool improvements needed

## Migration Plan

See the full migration plan in the session transcript. Key decisions:

1. **MCP removed** — Yoker is Python-first, no MCP support (by design)
2. **No Bash tool** — Yoker uses dedicated tools (make, git, github, etc.)
3. **No AskUserQuestion** — Rely on basic UI interactivity for now
4. **Plugin distribution** — Via yoker.toml config, not Claude marketplace
5. **CLAUDE.global.md → AGENTS.global.md** — Renamed, Claude-specific content removed
6. **Makefile.claude targets → Makefile.yoker** — With TODO for pending prompt support

## Deprecated Agents (removed from C3)

- **assistant** — moved to separate project/package
- **writing-assistant** — moved to `../yoker-writing-assistant` (files copied)
- **knowledge-agent** — experiment that didn't work out

## Deprecated Skills (removed from C3)

- **pa, pa-email, pa-inbox, pa-outbox, pa-session** — moved with assistant agent
- **writing-continuity, writing-idioms, writing-mistakes, writing-order,
  writing-review, writing-split, writing-voice** — moved with writing-assistant
- **copy-writer** — moved with writing-assistant

## Tool Name Mapping (Claude Code → Yoker)

| Claude Code | Yoker | Notes |
|-------------|-------|-------|
| Read | read | |
| Glob | list | |
| Grep | search | |
| Write | write | |
| Edit | update | |
| Bash | *(remove)* | Use make, git, github tools instead |
| WebSearch | websearch | |
| WebFetch | webfetch | |
| Skill | skill | |
| Agent | agent | |
| AskUserQuestion | *(remove)* | Built-in interactivity |
| PushNotification | *(remove)* | No equivalent |
| CronCreate/Delete | *(remove)* | No equivalent |
| mcp__* | *(remove)* | No MCP in Yoker |

## Files Removed (Session 2)

All files listed below have been removed from git tracking and disk:

- ~~`.claude/` directory~~ ✅ Removed
- ~~`.claude-plugin/` directory~~ ✅ Removed
- ~~`CLAUDE.md`~~ ✅ Removed (content reviewed/merged into AGENTS.md)
- ~~`settings.json`~~ ✅ Removed
- ~~`.mcp.json`~~ ✅ Removed
- ~~`Makefile.claude`~~ ✅ Removed
- ~~`PERSONAL.md.template`~~ ✅ Removed
- ~~`bin/statusline.py`~~ ✅ Removed
- ~~`agents/assistant.md`, `agents/knowledge-agent.md`, `agents/writing-assistant.md`~~ ✅ Removed
- ~~`skills/pa*/`, `skills/writing-*/`, `skills/copy-writer/`~~ ✅ Removed

## Files to Remove from Git Tracking (keep on disk)

- `analysis/` — already gitignored
- `reporting/` — already gitignored

## Validation Script

`bin/validate.py` — keep but remove symlink validation (Claude-specific).
Generic skill/agent structure validation is still useful.

## Tool Limitation Protocol

**STOP AND REPORT — do NOT work around missing tool capabilities with costly
operations.**

Yoker is in active development. Tools may be missing or incomplete. When you
encounter a limitation, you have two choices:

1. **Report it and wait** — Tell the user what tool/feature you need, what you
   were trying to do, and what your workaround would cost (context pollution,
   round-trips, risk of error). The user can often implement the missing
   tool in an active Yoker dev session, and a simple session resume gives you
   the improved tool.

2. **Propose a minimal workaround** — Only if the user agrees the workaround
   is acceptable given its cost. Never silently choose a costly workaround.

### The principle

Context is precious. Every byte of file content you read into context
displaces your capacity to reason about the actual task. A tool that saves
10KB of context is worth asking for. A workaround that costs 50KB of context
is worth refusing.

**When in doubt: report the limitation, explain the cost, and let the user
decide.** Never silently absorb the cost of a missing tool.

### Previously Missing Tools — RESOLVED

All tools that were missing during Session 1 have since been implemented in
Yoker:

- ✅ **`copy` tool** — Available via `file` tool with `copy` operation
- ✅ **`move` tool** — Available via `file` tool with `move` operation
- ✅ **`delete` tool** — Available via `file` tool with `delete` operation
- ✅ **`git rm` support** — Not yet in git tool's allowed commands, but file
  deletion + `git add --all` achieves the same result
- ✅ **`write` with `create_parents`** — Available via `write` tool with
  `create_parents: true`
## IMPORTANT

We are doing this using Yoker itself. This is part of the dogfooding phase
we're currently in. The goal is to iron out the last wrinkles in the Yoker
implementation, to make it a valid replacement for Claude Code as soon as
possible.

This means that due to Yoker, you will run into problems. These are mostly
tool-related. Tools might still have bugs, and mostly they lack options that
make some operations difficult.

Don't overthink things, if tools seem to make things difficult. Simply
explain that the current setup limits you too much and propose improvements.
There is always an active development session ongoing with Yoker, so these
improvements can be implemented on the go. A simple resume of our C3 porting
session, can offer you an improved tool, instead of over-complicating things.
