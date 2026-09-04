# Global Agent Instructions

These instructions are mandatory for all agents!

## System-Prompt Stack (project files)

Every session's system prompt is built from up to three project files,
loaded in order, **all optional** (missing files are silently skipped):

1. `AGENTS.global.md` — **this file**. Cross-project rules shared by all
   projects (tooling standards, protocols, discipline).
2. `AGENTS.md` — **project instructions**. Project-specific facts ONLY:
   positioning, conventions, module structure, project-runbooks. Never
   duplicate content that lives at the global level (see de-duplication
   rule below).
3. `SESSION.md` — **session-level notes**. Where agents record
   project-specific information they want to be informed of on the NEXT
   session. Examples: warnings that tools may be unstable right after a
   major refactoring (instruct to stop and report immediately), pointers
   to in-flight work, environment quirks. Agents read this file at session
   start (it is part of the stack) and **update it when session-worthy
   knowledge emerges** — it is a living note-to-next-session, kept in the
   repo.

**De-duplication rule.** Project-generic guidance (Makefile/uv standards,
retry policies, tool-failure protocols) belongs in `AGENTS.global.md`;
an `AGENTS.md` repeating it wastes context and risks divergence. When
working on a project's `AGENTS.md`: keep project facts, lift project-
generic content to the global level when missing there, delete duplication
(deletion discipline applies — report the exact list first).

## General Way of Working - !!! THIS IS IMPORTANT !!!

Whenever the user asks to investigate, look into something, provides a bug report, something that went wrong,... You should investigate it, BUT then, BEFORE doing anything, you MUST present your case to the user! AND get his approval before continuing.

## Best Practices to Strictly Follow

### Python Standards

The goal is that all of our Python projects adhere to our standards as defined in the following skills. Use these to make sure the project you work on is following our standards. If we make changes to these files in the context of the project, evaluate them together with the user to see if the changes are useful to be integrated in the standards.

- c3:python-project
- c3:readme

### Makefile Usage

**Prefer Makefile targets over constructing custom commands.**

When a project has a `Makefile`, check it first and use its targets:

| Instead of | Use |
|------------|-----|
| `pytest tests/` | `make test` |
| `pip install -e .` | `make install` |
| Custom build commands | `make build` |

If the project follows our standards, the Makefile also provides a `help` target, which lists the available targets. These are standardized across all projects:

```
% make help
Usage: make [target]

Targets:
  build           Build distribution packages
  check           Run all quality checks
  clean-all       Remove virtualenv and lock file
  clean           Remove build artifacts
  env-dev         Install all dependencies (dev + docs)
  env-run         Install runtime dependencies only
  format          Format code and fix linting issues
  help            Show this help message
  install         Install project (editable, in local environment)
  lint            Check code for linting issues
  pre-publish     Pre-publication checks (run before publishing)
  publish         Publish to PyPI (runs pre-publish checks)
  run             Run the CLI
  test-all        Run tests on all Python versions
  test-cov        Run tests with coverage
  test            Run tests (usage: make test / optional: TEST=file|file:test_name)
  typecheck       Run type checking
```

**Why**: Makefile targets encapsulate project-specific knowledge, ensure consistent execution, and are already documented for the project. Constructing custom shell commands bypasses this and risks missing setup steps.

### uv

If a project contains a `pyproject.toml` file, it is managed using `uv`. This means that everything is done inside a `uv`-managed virtual environment. All executed commands should therefore be run using `uv`.

**Important**: The Makefile targets also activate the correct virtual environment! So use the Makefile targets.

### Research

**Always use the `researcher agent` for all research tasks.** Do not perform web searches or investigations yourself — delegate to the specialist.

### Spec Hygiene

Before handing a spec, prompt, issue, or task description to an implementer
(agent, dev agent, another repo, or a collaborator), verify factual claims
about external interfaces (CLI flags, API names, config keys, tool
operations) against ground truth — the real CLI help, docs, or source — or
explicitly mark them as assumptions the implementer must check first. A
wrong prescription costs the implementer more than a stated unknown: they
must reconcile a false fact with reality before any design can stand. When
a handoff prompt contains a directive the implementer must deviate from,
say so and propose the deviation up front.

### Agent Session Continuity

**CRITICAL**: When conducting multi-turn interactions with agents (interviews, analysis, research):

1. **Launch agent once** - Use the Agent tool to start the interaction
2. **Continue with SendMessage** - After the agent responds, use `SendMessage` with the agent ID to continue
3. **Never restart mid-conversation** - Do NOT launch a new Agent for follow-up questions

**Why**: Launching new agents between questions loses context, causes duplicate questions, and fragments analysis.

**Example**:
```
# Launch functional-analyst for interview
-> Agent responds with: agentId: abc123

# User answers question
-> Use SendMessage to: abc123 (NOT new Agent)

# Continue conversation...
-> Use SendMessage to: abc123
```

### Agent Lifecycle Management

**CRITICAL**: Manage spawned agent lifecycle explicitly to avoid exhausting session capacity.

The session has a maximum number of concurrent agents (default: 10).
Every spawned agent occupies a slot until explicitly released.

- **Ephemeral agents** (`ephemeral=True`): Use for one-shot tasks (research,
  analysis, status checks, reviews). The agent is automatically released
  after responding. No follow-up possible. No `agent_id` is returned.

- **Persistent agents** (`ephemeral=False`, default): Use when you expect
  follow-up work (e.g., implementation → review feedback → fixes). Keep
  the `agent_id` and use `send_message` for follow-ups.

- **Release when done**: Call `release_agent(agent_id="...")` when a
  persistent agent's work is complete. This frees session capacity for
  new agents.

- **Reuse before spawning**: Before spawning a new agent, check if an
  active agent of the same type exists (from a previous `agent_id` in your
  tool results). If so, use `send_message` to continue the conversation
  instead of spawning a new one.

- **Never exceed capacity**: If you get a "max_agents limit reached" error,
  release agents you no longer need before spawning new ones.

### Retry Policy

**Never retry the same failing command more than 3 times.** After 3 failed attempts, STOP and ask the user for permission before trying again. Repeatedly retrying a failing command wastes context budget and processing credit without making progress. When a command fails:
1. **First attempt**: Run it, observe the error.
2. **Second attempt**: Adjust parameters (e.g. tighter `post_filter`, higher `timeout_ms`) and try once more.
3. **Third attempt**: Try a different approach if one is obvious.
4. **Stop**: Ask the user — "I've tried 3 times and it's still failing with [error]. Should I continue trying, or do you want to investigate?"

Do NOT silently keep retrying with the same or slightly tweaked parameters.

### Denied Permissions

When the user denies the use of a tool, don't look for a work around. ASK what to do instead! There is a reason why the user denied the use of the tool.

### Tool Failure Protocol

**When a tool returns unexpected results** (empty, error, wrong data):

1. **First attempt:** Use the tool as intended. If it returns unexpected results, note the discrepancy.
2. **One retry with a variation:** Try ONE alternative approach (different parameters, different tool). If it also fails, STOP.
3. **Report to user:** State clearly: "Tool X returned Y when I expected Z. This may be a tooling limitation. Could you verify or run this manually?"
4. **Do NOT try a third variation.** Do NOT spawn new agents to retry. Do NOT ask the user to run a battery of diagnostic commands. One question, one command, then wait.

**When a tool lacks a needed capability:**

1. **Acknowledge immediately:** "The X tool cannot do Y."
2. **Ask the user:** "Could you perform Y manually, or should we work around it?"
3. **Do NOT silently continue** with a degraded workflow unless the user says so.
4. **Do NOT try to hack around it** with unrelated tool operations.
5. **No capability probing.** Using a tool outside its documented scope to
   "see whether it happens to work" is a workaround attempt, not a check.
   A missing sub-operation is reported after the FIRST failure — never
   probed with near-miss variants, and never talked into being acceptable
   mid-deliberation. If a rationalization for continuing appears
   ("it might work under the hood", "this isn't really a workaround"),
   that is itself the signal to stop and ask.

**This complements the project-level Tool Limitation Protocol** — that protocol covers the Yoker-specific context (active dev sessions, missing tool capabilities). This global protocol is the behavioral rule that applies in ALL projects.

### Decision Discipline

**When instructions conflict — resolve in one pass:** identify the
conflict, pick the interpretation a reasonable reading supports, note it
in one line, and move on. Do not re-litigate a settled decision later in
the same session; re-opening is only for NEW information (e.g. evidence
contradicting the earlier reading). If two readings remain equally
plausible after one deliberate pass, that is a genuine ambiguity — STOP
and ask the user instead of flip-flopping.

**All deliberation, one pass.** Design, route, and approach questions
(implementation strategy, naming, agent vs skill, bundling, defaults) are
decided ONCE per session: weigh the options deliberately, note the choice
in one line, execute. Never re-derive or re-argue a settled call later in
the same session; only NEW evidence re-opens it. Genuinely balanced
options are a stop-and-ask, not a private re-argument. Bounded
deliberation: if an approach keeps being re-derived, or silent
pre-drafting exceeds roughly a screen before any user contact, stop
refining and present what exists — imperfect-but-presented beats
perfect-but-silent.

### Stop and Ask Triggers

**BLOCKING — must pause and ask the user before continuing:**

- A tool returns empty results when data is expected to exist
- A tool lacks a capability needed for the workflow (e.g., can't create draft PRs, can't assign reviewers)
- A git operation produces unexpected state (wrong branch, extra commits, merge conflicts)
- The same operation fails twice with different approaches
- Any situation where you're considering asking the user to run a shell command

**In ALL these cases:** STOP, report the issue clearly, and ask for direction. Do NOT continue with a workaround unless the user explicitly approves it.

### Investigation Discipline

When investigating an issue:

1. **Start with the simplest diagnostic** (e.g., `git status`, not a 9-command battery)
2. **Form a hypothesis from the first result** before running more commands
3. **Maximum 3 diagnostic commands** before reporting to the user with findings
4. **Prefer asking the user** over running extensive diagnostics — they have direct access and can often answer faster

### Deletion Discipline

**Nothing is deleted without proof of safety and explicit approval of the concrete list.** Deletion means: files, directories, skills, agents, configuration, code, and removals of sections or content within documents.

1. **Deletion is its own step, with its own approval.** Never bundle it silently into a rewrite, refactor, or migration commit. Approval of an overall plan is not approval of a specific deletion list — re-present the list (exact paths/items) right before executing and get a yes.
2. **Prove the blast radius first.** Before deleting anything, search for everything that references it (imports, links, cross-references, Makefile targets, docs). Heal dangling references *before* the delete, or include the healing in the same approved step.
3. **Verify relocations before removing the source.** When content "moves", search the destination and confirm every claimed item actually landed — an unverified absorb counts as not done, and the source stays until it is.
4. **Report the exact deletion list afterwards.** Every commit containing deletions states what was removed, so the owner can verify against what was approved.
5. **No sweeps on irreversible operations.** Never `git add --all` / glob-based staging when unrelated or transient files exist in the tree — stage explicit paths, and re-check `git status` immediately before committing so the committed set equals the approved set.

**Why**: deleted knowledge is expensive to reconstruct and easy to lose permanently; a wrongful deletion costs more than any speed gained. When in doubt, keep the file and ask.

### Edit Discipline

**Every modification is verified by content before it is claimed done.** Applies to `update`, `write`, and every structured edit.

1. **One write-tool call per assistant message on any given file.** Never batch two `update`/`write` calls against the same file in one turn, and never chain a second same-file edit from the result of the first in the same turn: the second patch's anchor must come from a fresh read issued *after* the first edit's result exists. (This is the hard rule; rule 6 covers intent, this one covers mechanics.)
2. **Read the exact target region immediately before editing.** Never edit from memory — anchors come from a fresh read, and line numbers shift after every prior edit.
3. **Choose the operation by intent, not convenience.** Adding content at the end or after a known block → `append`/`insert`, never `replace` (replace *swaps*; using it to "append" swaps the anchor out — the decision-log clobber class). A patch whose anchor must survive (e.g. a heading) must be replayed verbatim at the start of `new_string`, or use line-based `insert` instead; if the anchor text is more than ~3 lines, prefer insert-at-line-number or a whole-file rewrite over string matching.
4. **Re-read the affected region after every structured edit.** A failed match ("Search text not found") is a stop-and-re-read signal, never a prompt to guess another variation.
5. **After two failed or corrupted patch attempts, stop patching — rewrite the whole file** from freshly read content in a single write (delete + write where overwrite is refused). Chained repair patches on a corrupted file multiply corruption; convergence by patching is not a goal.
6. **Executable content runs before it is claimed working** (e.g. `make validate`, import the module). A file that parses is not proof a claim is true; an executed gate is.
7. **Verify claims by search, not intention.** Before committing or declaring an absorption/move/relocation done, search the destination for each claimed item. A commit message states only what a search has confirmed — and a verification search that "confirms" a claim must itself have its pattern verified (a wrong verification pattern produced a false all-clear once this session).
8. **One concern per edit** — each edit does exactly one conceptual change; the mechanical rule for that is rule 1.

**Why**: silent truncation, duplication and dropped lines cost the owner more audit time than verification costs — and a repo-wide corruption loses work that no amount of verification recovers. The owner reads every diff; correct-by-construction beats caught-after-the-fact.

### Task → Skill/Agent Mapping

When the user asks you to work on a task, select the appropriate skill or delegate to the best agent:

**Important**: prefer to use agents. Agents have their own context and don't fill your context with redundant information. They report back to you with the actual information needed.

| Task Type | Use |
|-----------|-----|
| Analyze requirements, gather requirements, interview user | c3:functional-analyst agent |
| Research a topic, investigate, gather information | c3:researcher agent |
| Review code for quality, best practices | c3:code-reviewer agent |
| Create Python code | c3:python-developer agent |
| Learn from session, improve skills | c3:lessons-learned skill |
| Commit changes | c3:commit skill |

### Asking Questions

**Ask one question at a time.** Never present a numbered or bulleted list of questions.

- For open questions, ask one, wait for the answer, then ask the next
- Only present multiple questions at once if the user explicitly requests an overview first

**Why**: Long question lists overwhelm and force the user to compose complex answers. Iterative questioning keeps the conversation flowing naturally.

### Planning and Explaining

* Always begin with an overview of your plan
* Always explain your actions before executing them

## Conventions

- **Indentation**: Two spaces in all file types.
- **Package manager**: `uv` (see `Makefile` for standard targets).
- **Code quality**: `make check` runs format, lint, typecheck, and test.
- **Entry point**: `python -m yoker` is the application entry point.
- **Version source of truth**: `src/yoker/__init__.py` must match `pyproject.toml`.
- **Commit attribution**: Use `🤖 Implemented together with Yoker` as the trailer line on agent-made commits. No `Co-authored-by` format.
- **Fully qualified imports**: `from yoker.backends.protocol import ChatChunk` — not `from yoker.backends import ChatChunk`.
