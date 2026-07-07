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
| Verification | Run `make check`; report the fix back to the caller for review + PR |
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
4. Run `make check` (test + typecheck + lint + format) — must pass before reporting done

**Do NOT commit, create a branch, open a PR, or run review here.** This skill
diagnoses and fixes; the caller runs the review cycle (`c3:project-review`) and
creates the PR (via `c3:release-manager` in project mode). See Phase 7.

### Phase 6: Documentation

- Update the bug analysis report with the fix summary
- Ensure the regression test is in the codebase
- Prepare a commit message (bug, fix, issue link) for the caller to use

**Do NOT close the issue.** Issue closure is handled post-merge by
`c3:project-post-merge` (via release-manager), after the owner merges the PR.

### Phase 7: Report Back to Caller

This skill does NOT run the review cycle or create the PR. Report back to the
caller (project-manage, or the main session) so it can run `c3:project-review`
and create the PR.

**Determine scope** from what the bug touched:

| Scope | When |
|-------|------|
| Backend | logic, API, data model, no UI |
| Frontend | UI/UX changes |
| Full stack | both |
| + security | auth, PII, input handling, external API, files, config |

**Report:**

```
## Bug Fix Ready for Review

**Issue:** #{number}
**Bug ID:** {bug-id}
**Summary:** {one-line}
**Root Cause:** {technical cause}

**Test Added:** {test file}:{test name}
**make check:** ✅ passing
**Files Modified:** {list}
**Scope:** {backend | frontend | full | docs} (+ security?)

**Bug Analysis Report:** docs/bug-analysis/{bug-id}.md
**Commit Message:** fix: {summary} (#{number})

Ready for c3:project-review, then PR.
```

The caller then:
1. Invokes `c3:project-review` (scoped to this bug) — functional, domain, quality, docs, `make check`.
2. On approval, creates the PR (via `c3:release-manager` in project mode).
3. On rejection (max 2 rounds), sends feedback back here to revise the fix.

**Rejection Handling** (when the caller returns feedback from `c3:project-review`):
| Scenario | Max Iterations | Escalation |
|----------|----------------|------------|
| Review rejects fix | 2 rounds | Caller escalates to owner |
| make check fails | 3 attempts | Ask user |
| Cannot reproduce | 1 request | Close bug |

### Phase 8: PR & CI (handled by the caller)

PR creation, CI follow-up, and marking ready for review are handled by the
caller (`c3:project-manage` via `c3:release-manager`), after `c3:project-review`
approves the fix — mirroring the feature workflow. This skill stops at Phase 7.

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
- **PR creation & CI** - Handled by the caller (project-manage via release-manager)
- **Issue closure** - Handled post-merge by c3:project-post-merge (owner merges)

## Common Issues

| Issue | Solution |
|-------|----------|
| Cannot reproduce | Request more info, check environment differences |
| Tests keep failing | Analyze if fix incomplete or test incorrect |
| Multiple fix proposals | Analyst recommends, user decides |
| Review rejects fix (via c3:project-review) | Caller returns feedback; iterate (max 2 rounds) |

## Related Skills

- **project-review** - Shared review cycle the caller runs on the fix (functional → domain → quality → docs → `make check`)
- **commit** - Create properly formatted commit
- **develop-agent** - For complex bug investigation
- **researcher** - For researching unknown patterns
- **manage-project** - Can be invoked within manage-project for bugs in project workflow

## Related Agents

These review the fix, invoked by `c3:project-review` (the caller runs it), not by this skill:

- **functional-analyst** - Bug validation, solution review
- **ui-ux-designer** - UI/UX change review (conditional)
- **security-engineer** - Security review (if security-related)
- **code-reviewer** - Quality and pattern validation
- **testing-engineer** - Test coverage and quality
- **end-user-documenter** - Documentation (if user-facing)

## Pattern Files

- `patterns/bug-analysis-template.md` - Bug analysis report template
- `patterns/test-creation-patterns.md` - Platform-specific test patterns
- `patterns/rca-techniques.md` - Root cause analysis techniques