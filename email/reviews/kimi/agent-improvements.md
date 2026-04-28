# Proposed Improvements to c3:code-reviewer Agent

**Date**: 2026-04-28
**Context**: Email MCP Server baseline review revealed significant duplication and dead code that the initial review pass missed.

---

## Problem Statement

The code-reviewer agent performed a thorough security and functional review of the email MCP server but missed several categories of structural quality issues:

1. **DRY violations** - `move_message()` duplicated `delete_message()` logic; `server.py` tools duplicated identical exception handling ladders
2. **Dead code** - `tools/definitions.py` was never imported; `use_ssl` config field was never read
3. **Near-duplicate factory methods** - `get_imap_client()` and `get_smtp_client()` in `connections/pool.py`
4. **Type safety bugs** - `MIMEMultipart` passed where `EmailMessage` was typed

These are exactly the kinds of issues that **static analysis catches reliably** but **manual review misses easily**.

---

## Proposed Agent Improvements

### 1. Add Structural Quality Checklist Section

Add an explicit "Structural Quality & Duplication" section to the review checklist, with mandatory checks:

```markdown
### Structural Quality & Duplication (Mandatory)

- [ ] **Cross-file import analysis** — Run `grep -rn "from X import\|import X"` for each module to identify dead code
- [ ] **Function-level DRY** — Review each public method for duplicated logic that could be delegated to an existing method
- [ ] **Exception handling patterns** — Check for identical `try/except` ladders repeated across multiple functions
- [ ] **Factory method deduplication** — Look for near-identical creation methods that differ only by type
- [ ] **Configuration field usage** — Verify every config field is actually read by at least one consumer
- [ ] **Type hint accuracy** — Check that parameter types accept all values actually passed at call sites
```

### 2. Add Cross-File Analysis Step to Workflow

Insert a new step between "Map Structure" and "Prioritize Areas" in the baseline review workflow:

```markdown
2b. **Cross-File Dependency Analysis**
   - For each module, run `grep -rn "from <module> import\|import <module>"` to find consumers
   - Flag modules with zero imports as potential dead code
   - Flag exported classes/functions with zero call sites
   - Check for configuration fields never referenced outside their definition file
```

### 3. Add Grep-Based Pattern Checks

Add explicit grep commands the agent should run before completing a review:

| Pattern | Purpose | Command |
|---------|---------|---------|
| Duplicate exception handling | Find repeated `except` ladders | `grep -n "except ValueError:" file.py` then check if the surrounding context is identical across functions |
| Dead code | Find modules never imported | `grep -rn "from <module> import\|import <module>" src/` |
| Unused config fields | Find fields never read | `grep -rn "field_name" src/` (should appear in both definition and consumer files) |
| Duplicate method bodies | Find similar code blocks | `grep -A 5 "def method_name" file.py` and compare |
| Type hint mismatches | Find `isinstance()` checks that reveal type lies | `grep -rn "isinstance.*MIMEMultipart\|isinstance.*EmailMessage" src/` |

### 4. Add Framework-Specific Knowledge

Include a "Framework Patterns" section in the agent definition that notes:

- **FastMCP 3.x** infers schemas from annotated function signatures — `TOOL_SCHEMAS` dicts and Pydantic input/output classes are unnecessary unless explicitly used for external consumers
- **Pydantic Settings** fields without any consumer in the codebase are dead configuration
- **Asyncio locks** should guard the entire operation, not just connection establishment, for sequential protocols like IMAP

### 5. Strengthen the "Why These Were Missed" Reflection

Add a mandatory reflection section to every review document:

```markdown
## Review Limitations

| Category | Coverage | Method |
|----------|----------|--------|
| Security vulnerabilities | Full | Manual + pattern matching |
| Functional correctness | Full | Manual + test review |
| Structural duplication | Partial | Grep-based cross-file analysis (add if missing) |
| Dead code | Partial | Import analysis (add if missing) |
| Type safety | Partial | Static analysis (limited without mypy) |
```

### 6. Specific Prompt Template Addition

Add a template prompt for catching duplication:

```markdown
### Prompt: Check for Duplication

Before completing your review, answer these questions:

1. **Method delegation**: Does any method inline logic that already exists in another method? 
   (Example: `method_A` does X+Y+Z; does `method_B` do X+Y inline instead of calling `method_A`?)

2. **Boilerplate duplication**: Are there identical `try/except`, `if/else`, or setup blocks repeated across functions?
   (Look for 3+ lines that are copy-pasted with only variable names changed.)

3. **Factory duplication**: Are there multiple methods that create instances of different types using the same pattern?
   (Look for methods that differ only in: class name, dictionary key, error message string.)

4. **Dead definitions**: Are there classes, functions, or variables exported but never imported?
   (Run `grep -rn "from module import name\|import name"` for each definition.)

5. **Config orphans**: Are there configuration fields defined but never read?
   (Search for the field name across the entire `src/` tree; it should appear in at least one consumer.)
```

---

## Rationale

The initial review focused on **runtime safety** (security, concurrency, error handling) because those are the most dangerous issues. But **structural quality** (DRY, dead code, type safety) compounds maintenance cost over time. The agent needs explicit prompts to look for these, because:

1. **Boilerplate blindness** — When reading code incrementally, repeated patterns look correct in each individual function
2. **Dead code invisibility** — A well-structured file that looks plausible in isolation may be entirely unused
3. **Cross-file analysis is expensive** — It requires deliberate grep commands, not just reading files sequentially
4. **Framework assumptions** — Reviewers unfamiliar with FastMCP/Pydantic may not recognize unnecessary schema definitions

By adding explicit grep-based checks and a structural quality checklist, the agent can catch these issues without relying on the reviewer's memory or familiarity with the entire codebase.

---

## Implementation Priority

| Priority | Improvement | Effort | Impact |
|----------|-------------|--------|--------|
| **P1** | Add structural quality checklist to review template | Low | High |
| **P1** | Add cross-file import analysis step to workflow | Low | High |
| **P2** | Add grep-based pattern checks to review workflow | Low | High |
| **P2** | Add framework-specific knowledge (FastMCP, Pydantic) | Medium | Medium |
| **P3** | Add mandatory "Review Limitations" reflection section | Low | Medium |
| **P3** | Add duplication-check prompt template | Low | High |
