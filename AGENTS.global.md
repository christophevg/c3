# Global Agent Instructions

These instructions are mandatory for all agents!

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

**This complements the project-level Tool Limitation Protocol** — that protocol covers the Yoker-specific context (active dev sessions, missing tool capabilities). This global protocol is the behavioral rule that applies in ALL projects.

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

### Style and Formatting

* Always use two spaces for indentation in all file types

### Things to Ignore

* Ignore the `local` folder
* Ignore files with `.local` extension
