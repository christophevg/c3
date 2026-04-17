# Global Claude Code Instructions

These instructions are mandatory for all agents!

# Personal Configuration

@~/.claude/PERSONAL.md

## Best Practices to Strictly Follow

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

### Makefile Usage

**Prefer Makefile targets over constructing Bash commands.**

When a project has a `Makefile`, check it first and use its targets:

| Instead of | Use |
|------------|-----|
| `pytest tests/` | `make test` |
| `pip install -e .` | `make install` |
| Custom build commands | `make build` |

**Why**: Makefile targets encapsulate project-specific knowledge, ensure consistent execution, and are already documented for the project. Constructing Bash calls bypasses this and risks missing setup steps.

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

When the user asks you to work on a task, select the appropriate tool:

| Task Type | Use |
|-----------|-----|
| Analyze requirements, gather requirements, interview user | functional-analyst agent |
| Research a topic, investigate, gather information | researcher agent |
| Review code for quality, best practices | code-reviewer agent |
| Create Python code | python-developer agent |
| Learn from session, improve skills | lessons-learned skill |
| Commit changes | commit skill (/commit) |

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
* Ignore the `notes` folder

### Project Workflow

For project management tasks, use the `/project` dispatcher skill which routes to specialized workflows. See the `project` skill for details.