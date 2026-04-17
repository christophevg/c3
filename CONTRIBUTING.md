# Contributing to C3

Thank you for your interest in contributing to C3! This document outlines the workflow and conventions for contributing skills, agents, and improvements.

## Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Submit a pull request

## Development Workflow

### Branch Naming

Use conventional commit prefixes:

| Prefix | Purpose |
|--------|---------|
| `feat/` | New feature or skill/agent |
| `fix/` | Bug fix |
| `docs/` | Documentation changes |
| `refactor/` | Code restructuring |
| `chore/` | Maintenance tasks |

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `chore`

**Scopes**: `skills`, `agents`, `bin`, `settings`, `docs`

**Examples**:
```
feat(skills): add ollama skill for LLM integration
fix(statusline): show count of extra Python versions
docs(readme): add requirements section
```

## Adding a New Skill

1. Use the `/develop-skill` skill in Claude Code for guided creation
2. Create directory: `skills/<skill-name>/`
3. Add required files:

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition with frontmatter and workflow |
| `patterns/` | Optional: Pattern files for common approaches |
| `templates/` | Optional: Template files for generation |
| `REFERENCE.md` | Optional: Reference documentation |

### SKILL.md Structure

```markdown
---
name: skill-name
description: One-line description
tools: Read, Glob, Grep, Write, Edit  # Optional
color: blue  # Optional
---

# Skill Name

Brief description and when to use.

## Workflow

### Phase 1: Name

| Step | Action |
|------|--------|
| 1 | First step |
| 2 | Second step |

## Related Skills

- other-skill — How it relates
```

## Adding a New Agent

1. Use the `/develop-agent` skill in Claude Code for guided creation
2. Create file: `agents/<agent-name>.md`

### Agent Structure

```markdown
---
name: agent-name
description: One-line description
model: sonnet  # or opus, haiku
tools: Read, Glob, Grep, Write, Edit  # Specify available tools
color: blue  # Optional
---

You are a specialist in [domain]. Your role is to...

## Responsibilities

- Responsibility 1
- Responsibility 2

## Workflow

1. Step one
2. Step two

## Output Format

[Expected output format]
```

## Testing

Currently, C3 relies on manual testing through usage. When contributing:

1. **Test your skill/agent** in a real Claude Code session
2. **Document edge cases** in the skill's SKILL.md
3. **Add examples** in the workflow steps

## Style Guidelines

### Indentation

Use **2 spaces** for indentation in all file types (Python, Markdown, YAML).

### Documentation

- Write clear, concise descriptions
- Use tables for structured information
- Include example commands in code blocks

### File Organization

```
skills/
├── skill-name/
│   ├── SKILL.md        # Required
│   ├── patterns/       # Optional
│   ├── templates/      # Optional
│   └── REFERENCE.md    # Optional

agents/
└── agent-name.md       # Single file per agent
```

## Installation Testing

Before submitting:

```bash
# Clean install test
make uninstall
make install

# Verify symlinks
ls -la ~/.claude/agents/
ls -la ~/.claude/skills/
ls -la ~/.claude/bin/
```

## Pull Request Process

1. **Update documentation** if changing functionality
2. **Add changelog entry** to CHANGELOG.md
3. **Test installation** with `make install`
4. **Link related issues** in PR description

## Getting Help

- Open an issue for questions
- Reference existing skills/agents as examples
- Use `/develop-skill` or `/develop-agent` for guided creation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
