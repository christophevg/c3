---
name: develop-agent
description: |
  Develop new agents. Use when creating, developing, reviewing, improving, or working on agents. Examples: "create an agent for X", "review the researcher agent", "improve the code-reviewer agent", "work on the python-developer agent".
type: workflow
---

# Develop Agent

Blueprint-aware workflow for creating and improving C3 agent definitions,
from intent to validated persona ready for engagement.

## Triggering

- "create an agent for X", "review the researcher agent", "improve the
  code-reviewer agent"
- formalizing a recurring workflow into an agent
- explicit invocation on any agent-definition work

# Inputs

The intent for the agent: what it does, when it engages, what it produces.
For complex scope, engage `c3:functional-analyst` first and build on its
analysis.

## Development workflow

### 1 — Interview

Clarify: primary function and the problem it solves · inputs and outputs
(with format) · Yoker tools it needs and must NOT get · boundaries and
what it decides vs. asks the owner.

### 2 — Scope validation (three tests)

1. **Trigger test** — one trigger condition; "when X or when Y" is two
   agents in one.
2. **Action test** — one output type; independently-firable actions are
   separate agents.
3. **Failure test** — if one part fails, the rest must still make sense;
   independent failure modes mean separate agents.

Complex, multi-workflow answers → narrow the agent or split it.

### 3 — Design against BLUEPRINT.md

The persona follows the BLUEPRINT §2 template — this is normative:

```
---
name: <name>
description: <when to engage — explicit, precise; the trigger surface>
color: <color>
tools:
  - <Yoker tool names only>
---

# Persona        — who I am, 3–5 sentences, zero procedure
# Engaged when   — by whom, with what input
# How I work     — skills invoked; agents engaged, and why
# I deliver      — outputs and artifacts
# I never        — few, absolute boundaries
```

- Least-privilege `tools:` grants: base read set (existence, read, list,
  search, skill), write set (write, update) only when it modifies files,
  specialist tools as the role demands, engagement/sleep only for
  orchestrators. Per-agent grants ARE the static-permission model.
- `description` is the trigger surface: precise conditions + examples
  ("use when…", concrete request examples), never vague ("helpful
  assistant"). State limitations ("read-only").
- Yoker names only — never Bash/Read/Edit/Task vocabulary. The validator
  (`make validate`) enforces this mechanically.
- Rules live in exactly one place (highest owning layer); no scar-tissue
  patches; no implicit forks where one behavior suffices.
- Agent content is generic: no personal names, no user-specific formats,
  no hardcoded paths. Personalization belongs to higher instruction layers
  and session context, never to the persona.
- Reference knowledge the persona needs daily lives with it; encyclopedic
  reference material goes to a knowledge skill the persona loads.

### 4 — Create and validate

Write `agents/<name>.md`. Then validate:
`make validate` must stay green (frontmatter, sections, tool-name lint).
Restart a session to load new/changed definitions — activation is at
session start, not file write.

Testing checklist before sign-off: triggers from its description
examples; produces the declared deliverables; respects tool grants and
"never" boundaries; failure behavior is defined (report and stop, not
improvise).

## Pattern references

`references/system-prompt.md` (persona-writing framework),
`references/patterns.md` (verification chains, structured output,
guardrails, context management), `references/hierarchy.md` — note: C3 is
flat (no orchestrator/sub-agent hierarchy; peers engage peers); read
`hierarchy.md` for the underlying principles only.

# Deliverables

- A validated agent definition (frontmatter per BLUEPRINT, five persona
  sections, minimal tool grants), plus usage documentation and validation
  results.

# Related

- `c3:develop-skill` — the complementary skill-creation workflow
- `c3:functional-analyst` — deep requirements for complex agents
- `c3:researcher` — research before designing an agent
- `c3:code-reviewer` — review of the drafted persona
- BLUEPRINT.md §2 — the template this workflow instantiates

# Never

- Grant write tools or network access without a concrete need.
- Hardcode personal data, names, or user-specific behavior in a persona.
- Create an agent with two trigger conditions — that is two agents.
- Promise parallel tool execution in definitions.