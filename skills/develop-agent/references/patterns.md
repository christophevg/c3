# Proven Agent Patterns

Reference guide for established agent design patterns.

## Pattern Reference

| Pattern | Core Idea | When to Use |
|---------|-----------|-------------|
| Role + Constraints | Define who agent is AND what it cannot do | Always (baseline) |
| Chain of Verification | Agent checks output against specific checklist | Output used without human review |
| Structured Output Enforcement | Explicit JSON schema, no deviations | Pipeline outputs consumed programmatically |
| Tool Selection Heuristics | Priority rules for when to use each tool | Agents with 2+ similar tools |
| Error Recovery Instructions | Recoverable vs unrecoverable error protocols | Any agent with tool access |
| Context Window Management | Rules for keep/summarize/discard | Multi-step agents processing large data |
| Guard Rails Pattern | Hard limits on cost, scope, external actions | Always (especially autonomous agents) |
| Progressive Disclosure | Phase-gated instructions, detail on demand | Complex multi-phase workflows |
| Memory Integration | Explicit read/write rules for persistent files | Recurring agents needing cross-session state |
| Self-Evaluation Loop | Agent scores own output against criteria | Content generation, quality-sensitive outputs |

## Common Agent Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Vague description | Include specific trigger conditions with examples |
| Too many tools | Restrict to minimum needed (least privilege) |
| Missing examples | Add 2-4 example blocks in frontmatter |
| Overly broad scope | Focus on one task (apply three tests) |
| No constraints | Define what it should NOT do |
| Ambiguous output format | Specify exact JSON/schema structure |
| No error handling | Add explicit error recovery instructions |
| Missing negative instructions | LLMs are eager to please—tell them what NOT to do |