---
name: develop-agent
description: Develop new Claude Code agents. Use when creating, developing, reviewing, improving, or working on agents. Examples: "create an agent for X", "review the researcher agent", "improve the code-reviewer agent", "work on the python-developer agent".
---

# Develop Agent Skill

Guides the complete workflow for developing new Claude Code agents, from initial description to tested, documented agent ready for use.

## Overview

| Step | Description |
|------|-------------|
| 1. Interview | Clarify scope, tools, constraints |
| 2. Analyze | Create analysis document |
| 3. Design | Define agent structure |
| 4. Create | Write agent definition |
| 5. Test | Symlink and validate |

## Research Foundation

This skill incorporates best practices from comprehensive research on AI agent development (see research/2026-04-08-ai-agent-development-best-practices/):

- **Task-specific design** over role-based agents
- **Five-section system prompt** framework
- **Least-privilege tool access** for security
- **Verification criteria** as highest-leverage practice

## When to Use

- User says "create an agent that..."
- User runs `/develop-agent "description"`
- User describes wanting a specialized agent for a task
- User wants to formalize a workflow into an agent

## Workflow

### Step 1: Initial Interview

Ask these agent-specific questions to clarify scope:

**Scope & Purpose:**
- What is the primary function of this agent?
- What problem does it solve?
- Who will use it (developer, analyst, end user)?

**Input & Output:**
- What inputs will the agent receive?
- What outputs should it produce?
- What format should outputs be in?

**Tools & Capabilities:**
- What tools does it need? (Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch, Skill)
- Should it spawn other agents?
- Any tools it should NOT have?

**Constraints:**
- What should it NOT do?
- Any scope boundaries?
- What decisions should it make vs. ask the user?

**Narrow Scope Validation:**

Apply the **Three Tests for Narrow Scope**:

1. **Trigger Test**: Does this agent have exactly one trigger condition?
   - If writing "when X or when Y," you have two agents in one
   - Each agent should have ONE specific situation

2. **Action Test**: Does this agent produce exactly one type of output?
   - If actions can fire independently, they should be separate agents
   - One output type per agent

3. **Failure Test**: If one part fails, does the rest still make sense?
   - Independent failure modes indicate separate agents
   - Contained failure scope

**Complexity Detection:**

If answers reveal complex functionality (multiple workflows, intricate logic, many edge cases):
- Spawn functional-analyst for deep requirements analysis
- Wait for functional-analyst to complete
- Continue with its analysis document

If straightforward (clear, focused task):
- Continue with the interview and create analysis directly

### Step 2: Create Analysis Document

**ALWAYS create an analysis document** in the idea folder:

```
ideas/{agent-name}/analysis/functional.md
```

Analysis document structure:

```markdown
# {Agent Name} - Functional Analysis

**Date:** YYYY-MM-DD
**Analyst:** [skill or functional-analyst]

## Purpose

[One paragraph describing what the agent does and why]

## Scope

### In Scope
- [Task 1]
- [Task 2]

### Out of Scope
- [Excluded task 1]
- [Excluded task 2]

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| [input1] | [type] | [description] |

## Outputs

| Output | Type | Location |
|--------|------|----------|
| [output1] | [type] | [path] |

## Tools Required

| Tool | Usage | Risk Level |
|------|-------|------------|
| [tool1] | [what it's used for] | [read/modify/delete] |

## Constraints

- [Constraint 1]
- [Constraint 2]

## Workflow

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Example Scenarios

### Scenario 1: [Name]
**Input:** ...
**Expected Output:** ...

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| [decision] | [why] |

## Related Agents

- [agent1] - [relationship]
- [agent2] - [relationship]

## Scope Validation

- Trigger Test: [single trigger condition]
- Action Test: [single output type]
- Failure Test: [contained failure scope]
```

### Step 3: Design Agent Structure

#### Color Selection

| Color | Agent Types |
|-------|-------------|
| `green` | Development, implementation |
| `blue` | Analysis, research |
| `cyan` | Documentation, knowledge |
| `yellow` | Coordination, planning |
| `magenta` | Testing, validation |
| `red` | Security, review |

### Step 4: Create Agent Definition

Create the agent file:

```
ideas/{agent-name}/artifacts/agent/{agent-name}.md
```

#### Five-Section System Prompt Framework

See `references/system-prompt.md` for the complete framework. Every agent must include:
1. Identity and Role
2. Capabilities and Constraints
3. Tool Instructions
4. Output Format
5. Guardrails and Error Handling

#### Agent Frontmatter Template

```markdown
---
name: {agent-name}
description: [One-line purpose]. Use when [trigger conditions]. Examples: "[Example request 1]", "[Example request 2]", "[Example request 3]".
model: inherit
color: [blue|cyan|green|yellow|magenta|red]
tools: [list of tools]
---

# {Agent Name}

[Five-section system prompt following framework above]
```

**IMPORTANT: YAML Frontmatter Format**

The frontmatter must use **single-line descriptions** with inline examples. Multi-line content breaks YAML parsing:

✅ **Correct format:**
```yaml
---
name: my-agent
description: One-line description. Use when X. Examples: "Example 1", "Example 2", "Example 3".
tools: Read, Grep
color: blue
---
```

❌ **Broken format (DO NOT USE):**
```yaml
---
description: One-line description. Examples:

<example>
Context: ...
user: "..."
</example>

tools: Read
---
```

The `<example>` blocks are NOT parsed as part of the description field - they're treated as unknown YAML keys and ignored.

#### Description Best Practices

The description field is **critical**—Claude uses it to decide when to delegate.

1. **Single-line format**: Description must be ONE line. Use inline examples.
   ```yaml
   description: Reviews code for quality. Use after implementation. Examples: "Review src/auth/", "Check PR #42".
   ```
2. Include specific conditions: "Use proactively after code changes"
3. Add trigger examples: "When reviewing Python files"
4. Be precise: Avoid vague descriptions like "helpful assistant"
5. Mention limitations: "Read-only, does not modify files"

### Step 5: Symlink and Validate

#### Security Validation

Apply **Least-Privilege Tool Access**:

| Risk Level | Tools | When to Use |
|------------|-------|-------------|
| **Read-only** | Read, Grep, Glob | Analysis, review, exploration |
| **Modify** | Read, Grep, Glob, Edit, Write | Implementation, fixes |
| **Execute** | Bash, Read, Grep | Test execution, commands |
| **Full** | All tools | Only when necessary |

**Tool Access by Use Case:**

| Use Case | Recommended Tools |
|----------|------------------|
| Read-only analysis | Read, Grep, Glob |
| Test execution | Bash, Read, Grep |
| Code modification | Read, Edit, Write, Grep, Glob |
| Full access | Omit tools field (inherits all) |

**High-Risk Actions Requiring Approval:**

- Anything touching payroll, HR, legal, or medical content
- Exports
- Deletions
- Permission changes
- Refunds
- Billing changes
- Public posting
- External emails

#### Symlink Creation

1. Symlink to local agents folder:
```bash
ln -sf ideas/{agent-name}/artifacts/agent/{agent-name}.md .claude/agents/{agent-name}.md
```

2. Verify the agent is detected by checking system reminders

3. Create documentation:
- README.md with usage examples
- Add to project's agent index if applicable

#### Testing Framework

**Test Suite Components:**

| Test Type | Purpose |
|-----------|---------|
| Happy path cases | Normal expected inputs |
| Edge cases | Boundary conditions |
| Error cases | Invalid inputs |
| Adversarial cases | Deliberately misleading inputs |

**Testing Checklist:**

- [ ] Agent triggers correctly from description examples
- [ ] Produces expected output format
- [ ] Handles edge cases gracefully
- [ ] Respects tool restrictions
- [ ] Does not exceed scope constraints
- [ ] Error handling works as specified

## Proven Agent Patterns

See `references/patterns.md` for the complete pattern catalog including:
- Role + Constraints
- Chain of Verification
- Structured Output Enforcement
- Tool Selection Heuristics
- Error Recovery Instructions
- Context Window Management
- Guard Rails Pattern
- Progressive Disclosure
- Memory Integration
- Self-Evaluation Loop

Also includes common agent mistakes to avoid.

## Hierarchy Design

See `references/hierarchy.md` for multi-agent system design including:
- Three-tier structure (Orchestrator, Team Lead, Specialist)
- Five hierarchy rules
- When to create new agents vs. avoid creating them

## Incubator Workflow

When working in the incubator project (`~/Workspace/agentic/incubator`), see `references/incubator-workflow.md` for additional steps:
- KB Integration (checking and updating knowledge base)
- Registry Update (maintaining `.claude/REGISTRY.md`)

## Example Workflow

**User:** "Create an agent to analyze API responses"

**Skill Response:**

1. **Interview:**
   - "What kind of APIs? (REST, GraphQL, gRPC)"
   - "What analysis? (performance, structure, errors, security)"
   - "What output format? (report, JSON, markdown)"
   - "Should it read local files or make HTTP requests?"

2. **Scope Validation (Three Tests):**
   - Trigger Test: "When user asks to analyze API responses" ✓
   - Action Test: Produces analysis report ✓
   - Failure Test: If analysis fails, report issue and stop ✓

3. **Create Analysis:**
   - Document scope, inputs, outputs, tools
   - Define workflow steps
   - Add example scenarios

4. **Design:**
   - Color: `blue` (analysis)
   - Tools: Read, Glob, Grep, Write (for report)
   - Apply five-section framework

5. **Create Agent:**
   - Write agent definition with all five sections
   - Add examples in description
   - Define output format
   - Add error handling

6. **Symlink and Document:**
   - Create symlink
   - Add README with usage
   - Update registry

## Related Skills

- develop-skill - Complementary workflow for skill creation
- functional-analyst - Deep requirements analysis for complex agents
- researcher - Research before agent creation
- code-reviewer - Review agent implementations