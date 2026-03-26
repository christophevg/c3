# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Claude Code configuration harness** that provides reusable skills, agents, and settings for Python/Baseweb development projects. The configuration is designed to be symlinked into `~/.claude/` for use across multiple projects.

## Installation

```bash
make install
```

This symlinks the `agents/`, `skills/`, `bin/`, and `settings.json` into `~/.claude/`.

## Project Structure

```
c3/
├── agents/           # Specialized agent definitions
├── skills/           # Reusable skill definitions
├── bin/              # Utility scripts (statusline)
├── settings.json     # Claude Code configuration
└── Makefile          # Installation commands
```

## Skills

Skills are invoked via `/skill-name` and provide specialized guidance:

| Skill | Purpose |
|-------|---------|
| `/python` | Python coding standards and testing patterns |
| `/database` | MongoDB access code patterns and security |
| `/baseweb` | Baseweb/Vue/Vuetify best practices |
| `/fire` | Python Fire CLI patterns |
| `/manage-project` | Orchestrates multi-agent workflow |
| `/start-baseweb-project` | Bootstrap new Baseweb projects |
| `/analysis-integration` | Consolidate findings from domain agents |
| `/lessons-learned` | Review session for improvements |

## Agents

Specialized agents for structured project development:

- **functional-analyst**: Translates requirements into tasks, owns TODO.md
- **api-architect**: Designs RESTful APIs and data models
- **ui-ux-designer**: Designs user interfaces and user flows
- **python-developer**: Implements code following project conventions
- **code-reviewer**: Reviews code for quality and best practices

## Project Management Workflow

The `/manage-project` skill orchestrates a structured workflow:

1. **Functional Analysis** - functional-analyst reviews requirements and creates TODO.md
2. **Cross-Domain Review** - api-architect and ui-ux-designer provide perspective
3. **Consensus** - Agents agree on backlog before implementation
4. **Implementation Loop** - For each task:
   - Plan → Implement → Review cycle
   - All agents must approve before task completion
   - Reports stored in `reporting/` folder

## Key Conventions

### Indentation
- **Always use two spaces** for indentation in all file types

### Testing Patterns (pytest)
- Use `monkeypatch` fixture for environment variables
- Use `unittest.mock.patch` and `MagicMock` for mocking
- Use `autouse=True` fixtures for test setup
- Group related tests in classes
- Test both success and error paths

### Database Security (MongoDB)
- Never log connection URIs (may contain credentials)
- Use `bson.errors.InvalidId` for ObjectId validation
- Escape regex input with `re.escape()` to prevent ReDoS
- Use environment variables for pool sizes

### API Endpoints (Baseweb/Flask)
- Use `endpoint="api.name"` to avoid route name collisions
- Use `@server.authenticated("permission.name")` decorator
- Catch specific exceptions before generic ones

### Error Handling
```python
try:
  # database operation
except NotFoundError:
  raise  # re-raise domain exceptions
except PyMongoError as e:
  logger.error(f"Database error: {e}\n{traceback.format_exc()}")
  raise DatabaseError(f"Failed: {e}")
```

## File Conventions

- `analysis/` - Functional, API, UI/UX analysis documents
- `reporting/{task-name}/` - Task-specific reports (plan.md, summary.md, review files)
- `TODO.md` - Backlog with phase-organized tasks
- `CLAUDE.md` - This file (project-specific guidance)
- `AGENTS.md` - Agent instructions for target projects

## Status Line

The status line script (`bin/statusline.py`) displays:
- Model name
- Context window usage percentage
- Session duration
- Rate limit percentages
- Current git branch