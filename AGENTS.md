# Agents.md

This is the C3 project. It provides agent definitions and skills.

See also: **AGENTS.global.md** for shared conventions (read this alongside AGENTS.md).

## History

C3 was originally developed for Claude Code. It has been ported to Yoker —
the porting work was done as a dogfooding effort, using Yoker itself to
perform the migration. The `master` branch retains the last Claude
Code-compatible state; the `yoker` branch is the active development branch.

Key changes during the port:
- `CLAUDE.md` → `AGENTS.md`, `CLAUDE.global.md` → `AGENTS.global.md`
- All Claude-specific files removed (`.claude/`, `.claude-plugin/`, `settings.json`, `.mcp.json`, `Makefile.claude`, etc.)
- MCP removed — Yoker is Python-first, Python functions are first-class tools
- Deprecated agents/skills extracted to separate projects (assistant, writing-assistant, knowledge-agent)
- Plugin configuration via `yoker.toml`

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