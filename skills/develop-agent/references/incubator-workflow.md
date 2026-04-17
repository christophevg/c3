# Incubator Workflow

Additional workflow steps specific to working in the incubator project (`~/Workspace/agentic/incubator`).

## KB Integration

Before creating, check for:
- Existing similar agents in `.claude/agents/`
- Prior research in `kb/references/` and `kb/patterns/`
- Related skills in `.claude/skills/`

After creating:
- Update `kb/tools/agents/` with agent documentation
- Add to agent index if applicable
- Note any new patterns discovered
- **Update registry**: Add entry to `.claude/REGISTRY.md`

## Registry Update

After creating a new agent in the incubator, update `.claude/REGISTRY.md`:

1. Add to Agents table:
```markdown
| {agent-name} | `incubating` | `ideas/{idea}/artifacts/agent/{name}.md` | — |
```

2. Add to Update Log:
```markdown
| YYYY-MM-DD | Created | {agent-name} agent (incubating) |
```