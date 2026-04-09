---
name: bug-fixing
description: Systematic bug fixing with TDD approach. Use when fixing bugs, debugging issues, or investigating problems. Accepts bug descriptions in any format, coordinates analyst/reviewer agents, creates tests before fixes, produces analysis reports.
---

# Bug Fixing

A systematic, test-driven workflow for fixing software bugs with agent coordination.

## Overview

| Capability | Description |
|------------|-------------|
| Bug Intake | Accept text, issue references, or structured bug reports |
| Analysis | Root cause investigation with functional analyst review |
| TDD Approach | Failing test first, then fix implementation |
| Agent Coordination | Orchestrate functional-analyst, ui-ux-designer, code-reviewer |
| Documentation | Bug analysis reports with issue comments |

## When to Use This Skill

Use this skill when:
- User says "fix bug", "there's a bug", "debug this"
- User references an issue with fix context (e.g., "fix issue #123")
- User provides a bug report or describes unexpected behavior
- User wants to reproduce or investigate an issue

## Workflow

### Phase 1: Bug Intake

```
Parse bug description → Detect project context → Extract details → Assign ID
```

**Input Formats:**
- Free-form text: "The login button doesn't work on mobile"
- Issue reference: "#123" or "JIRA-456"
- Structured report: Path to bug report file

**Project Detection:**
| Detect | Method |
|--------|--------|
| Language | `pyproject.toml`, `package.json`, `Cargo.toml` |
| Framework | Config files (Django, React, Vue) |
| Test framework | `pytest.ini`, `jest.config.js`, `vitest.config.ts` |
| Conventions | `.prettierrc`, `pylintrc`, `ruff.toml` |

### Phase 2: Bug Analysis

**Invoke functional-analyst agent** to:
1. Review bug validity and scope
2. Confirm bug exists or reject with reason
3. Flag UI impact if applicable

**Create bug analysis report:**
- Path: `docs/bug-analysis/{bug-id}.md`
- Post as comment if issue/ticket exists

**Analyst outcomes:**
| Outcome | Action |
|---------|--------|
| Confirmed (no UI) | Proceed to Phase 3 |
| Confirmed (with UI) | Proceed, note UI review needed |
| Rejected | Document reason, close bug |

### Phase 3: Root Cause Investigation

Apply systematic debugging framework:

| Step | Action |
|------|--------|
| Isolate | Reproduce consistently, identify boundaries |
| Gather Info | Log strategically, compare working vs broken |
| Hypothesize | Specific testable hypotheses, one variable at a time |
| Validate | Run tests, document findings |

**RCA Techniques:**
- **5 Whys**: For simple/linear problems
- **Fishbone Diagram**: For complex/multi-factor issues

### Phase 4: Test Creation (TDD)

**Critical:** Create failing test BEFORE implementing fix.

1. **Determine test type:**
   | Bug Type | Test Type |
   |----------|-----------|
   | Logic/validation | Unit test |
   | Integration/API | Integration test |
   | User flow | E2E test |

2. **Create test that demonstrates bug:**
   ```python
   # Example: Test expects current (incorrect) behavior
   def test_login_button_disabled():
       result = login_button.is_enabled()
       assert result == False  # Passes, proving bug exists
   ```

3. **Run test to confirm reproduction**

### Phase 5: Fix Implementation

1. Implement minimal fix
2. Update test to expect correct behavior
3. Run all tests (fix + no regressions)
4. Invoke code-reviewer agent

### Phase 6: Agent Coordination

```
Functional Analyst Review
        ↓ Approved
UI Changes? → UI/UX Designer Review
        ↓ Approved
Code Reviewer Review
        ↓ Approved
Proceed to Phase 7
```

**Rejection Handling:**
| Scenario | Max Iterations | Escalation |
|----------|----------------|------------|
| Analyst rejects | 2 rounds | Ask user |
| Tests fail | 3 attempts | Ask user |
| Cannot reproduce | 1 request | Close bug |

### Phase 7: Documentation & Closure

- Update bug analysis report with fix summary
- Ensure regression test in codebase
- Document commit message (bug, fix, issue link)
- Close issue or mark resolved

## Bug Analysis Report Template

See `patterns/bug-analysis-template.md` for the full template.

**Key sections:**
- Summary & symptoms
- Expected vs actual behavior
- Root cause analysis
- Proposed fix approach
- Test strategy
- Risk assessment
- Lessons learned

## Platform-Specific Patterns

See `patterns/test-creation-patterns.md` for platform-specific guidance.

**Common bug categories:**

| Platform | Common Causes | Debug Focus |
|----------|---------------|-------------|
| Frontend | Async race conditions, stale state | Timeline, state changes |
| Backend | N+1 queries, connection exhaustion | Query patterns, logs |
| Mobile | Device/OS variations, memory leaks | Environment, profiling |
| Database | Missing indexes, stale statistics | Query plans, metrics |

## Out of Scope

This skill does NOT handle:
- **Security vulnerabilities** - Use specialized security workflow
- **Production incidents** - Use incident response process
- **Bug prioritization** - Project management concern
- **Upstream library fixes** - Only workarounds in scope

## Common Issues

| Issue | Solution |
|-------|----------|
| Cannot reproduce | Request more info, check environment differences |
| Tests keep failing | Analyze if fix incomplete or test incorrect |
| Multiple fix proposals | Analyst recommends, user decides |
| Agent rejects fix | Iterate with feedback (max 2 rounds) |

## Related Skills

- **commit** - Create properly formatted commit
- **develop-agent** - For complex bug investigation
- **researcher** - For researching unknown patterns
- **manage-project** - Can be invoked within manage-project for bugs in project workflow

## Related Agents

- **functional-analyst** - Bug validation, solution review
- **ui-ux-designer** - UI/UX change review (conditional)
- **code-reviewer** - Quality and pattern validation

## Pattern Files

- `patterns/bug-analysis-template.md` - Bug analysis report template
- `patterns/test-creation-patterns.md` - Platform-specific test patterns
- `patterns/rca-techniques.md` - Root cause analysis techniques