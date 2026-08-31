# Incubator Workflow

Additional workflow steps specific to working in the incubator project
(`~/Workspace/agentic/incubator`).

## KB Integration

Before creating, check for:
- Existing similar agents in the incubator's `agents/` folder
- Prior research in `kb/references/` and `kb/patterns/`
- Related skills in `skills/`

After creating:
- Update `kb/tools/agents/` with agent documentation
- Add to agent index if applicable
- Note any new patterns discovered
- **Update registry**: add the agent to the incubator's registry
  (`REGISTRY.md`), marking it `incubating`

## Registry Update

After creating a new agent in the incubator, update the registry:

1. Add to Agents table:
```markdown
| {agent-name} | `incubating` | `ideas/{idea}/artifacts/agent/{name}.md` | — |
```

2. Add to Update Log:
```markdown
| YYYY-MM-DD | Created | {agent-name} agent (incubating) |
```