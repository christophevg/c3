# Global Claude Code Instructions

These instructions are mandatory for all agents!

## Best Practices to Strictly Follow

### Python Standards

The goal is that all of our Python projects adhere to our standards as defined in the following skills. Use these to make sure the project you work on is following our standards. If we make changes to these files in the context of the project, evaluate them together with the user to see if the changes are useful to be integrated in the standards.

- c3:python-project
- c3:readme

### Makefile Usage

**Prefer Makefile targets over constructing custom Bash commands.**

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
  lint            Check code for linting issues
  pre-publish     Pre-publication checks (run before publishing)
  publish         Publish to PyPI (runs pre-publish checks)
  run             Run the CLI
  test-all        Run tests on all Python versions
  test-cov        Run tests with coverage
  test            Run tests (usage: make test / optional: TEST=file|file:test_name)
  typecheck       Run type checking
```

**Why**: Makefile targets encapsulate project-specific knowledge, ensure consistent execution, and are already documented for the project. Constructing Bash calls bypasses this and risks missing setup steps.

### uv

If a project contains a `pyproject.toml` file, it is managed using `uv`. This means that everything is done inside a `uv`-managed virtual environment. All executed commands should therefore be run using `uv`.

**Important**: The Makefile targets also activate the correct virtual environment! So use the Makefile targets.

### Tool Selection

**NEVER use Bash for file operations when a dedicated tool exists** — this is not negotiable:

| Operation | Use | Never |
|-----------|-----|-------|
| Search for files | Glob | `find`, `ls` |
| Search file contents | Grep | `grep`, `rg` |
| Read files | Read | `cat`, `head`, `tail` |
| Edit existing files | Edit | `sed`, `awk` |
| Create new files | Write | `echo >`, `cat >`, heredocs |
| Fetch web content | WebFetch | `curl`, `wget` (for simple fetches) |
| Search the web | WebSearch | manual browser lookup |

**Why**: Dedicated tools provide structured output, proper permission handling, and make your actions transparent and reviewable. Bash commands bypass these controls.

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
→ Agent responds with: agentId: abc123

# User answers question
→ Use SendMessage to: abc123 (NOT new Agent)

# Continue conversation...
→ Use SendMessage to: abc123
```

### Task → Skill/Agent Mapping

When the user asks you to work on a task, select the appropriate skill or delegate to the best agent:

**Important**: prefer to use agents. Agents have their own context and don't fill your context with redundant information. They report back to you with the actual information needed.

| Task Type | Use |
|-----------|-----|
| Analyze requirements, gather requirements, interview user | functional-analyst agent |
| Research a topic, investigate, gather information | c3:researcher agent |
| Review code for quality, best practices | c3:code-reviewer agent |
| Create Python code | c3:python-developer agent |
| Learn from session, improve skills | lessons-learned skill (/c3:lessons-learned) |
| Commit changes | commit skill (/c3:commit) |

### Asking Questions

**Ask one question at a time.** Never present a numbered or bulleted list of questions.

- Use the **AskUserQuestion tool** for choice-based questions — it provides a clean selection menu with an "Other" option for custom input
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

