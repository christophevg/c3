# Review Cycle Execution

This document provides detailed guidance for the implementation review cycle in Phase 4.

## Review Sequence

The review cycle follows a strict sequence to ensure quality:

```
Step 8a: Functional Review (BLOCKING)
    │
    ▼
Step 8b: Domain Reviews (PARALLEL)
    │
    ▼
Step 8c: Quality Reviews (PARALLEL)
    │
    ▼
Step 8d: Documentation (IF user-facing)
```

## Step 8a: Functional Review (Blocking)

**Purpose:** Validate that the implementation meets functional requirements.

**Agent:** `functional-analyst`

**Review Criteria:**
- All acceptance criteria from TODO.md are met
- Edge cases are handled
- User flow works as expected
- No regressions in existing functionality

**Process:**
1. Provide functional-analyst with:
   - Task definition from TODO.md
   - Implementation plan from `reporting/{task-name}/plan.md`
   - Key files modified
2. Functional-analyst reviews and approves/rejects
3. If rejected: collect feedback, return to Step 7 (implementation)
4. If approved: proceed to Step 8b

**Must pass before domain reviews.**

## Step 8b: Domain Reviews (Parallel)

**Purpose:** Validate architecture, design, and security aspects.

**Agents (invoked in parallel based on scope):**

| Scope | Agents |
|-------|--------|
| Backend only | `api-architect`, `security-engineer` (if security-related) |
| Frontend only | `ui-ux-designer` |
| Full stack | `api-architect`, `ui-ux-designer`, `security-engineer` (if security-related) |

### api-architect Review

**Review Criteria:**
- API design follows RESTful conventions
- Data models are appropriate
- Endpoints are properly named
- Request/response schemas are consistent
- Error handling is comprehensive

### ui-ux-designer Review

**Review Criteria:**
- UI follows design system
- UX flow is intuitive
- Accessibility requirements met
- Responsive design works
- Component structure is maintainable

### security-engineer Review

**Review Criteria:**
- Authentication/authorization is correct
- Input validation is comprehensive
- Sensitive data is protected
- No OWASP Top 10 vulnerabilities
- Secrets are not exposed

**Process:**
1. Invoke all applicable domain agents in parallel
2. Each agent reviews independently
3. Collect all feedback
4. If any reject: consolidate feedback, return to Step 7
5. If all approve: proceed to Step 8c

## Step 8c: Quality Reviews (Parallel)

**Purpose:** Validate code quality and test coverage.

**Agents (invoked in parallel):**
- `code-reviewer`
- `testing-engineer`

### code-reviewer Review

**Review Criteria:**
- Code follows project conventions
- No code smells or anti-patterns
- Appropriate abstractions
- No security vulnerabilities
- Maintainable structure

### testing-engineer Review

**Review Criteria:**
- Test coverage is adequate
- Tests are meaningful (not just coverage)
- Edge cases are tested
- Integration tests cover key flows
- Tests are maintainable

**Process:**
1. Invoke both agents in parallel
2. Each agent reviews independently
3. Collect all feedback
4. If any reject: consolidate feedback, return to Step 7
5. If all approve: proceed to Step 8d (if user-facing) or Step 9

## Step 8d: Documentation (If User-Facing)

**Purpose:** Ensure user-facing changes are documented.

**Agent:** `end-user-documenter`

**Review Criteria:**
- User documentation is updated
- API documentation is current
- README reflects changes
- Changelog is updated (if applicable)

**Process:**
1. Invoke end-user-documenter
2. Review created/updated documentation
3. If rejected: return to Step 7 with feedback
4. If approved: proceed to Step 8e

## Step 8e: Functional Completeness Check

**Purpose:** Ensure every commit is a functional whole.

**Principle:** Every commit must be a functional whole with:
1. Implemented functionality
2. Documentation (end-user and/or developer)
3. UI/demo (console, CLI, or web - depends on target)
4. End-to-end experience from day one

**Verification Checklist:**

| Check | Command | Requirement |
|-------|---------|-------------|
| Tests pass | `make test` | MUST pass - no exceptions |
| Type checks pass | `make typecheck` | MUST pass |
| Lint passes | `make lint` | MUST pass |
| Code style | `make format` or `make check` | MUST pass |
| Documentation complete | Manual review | README, API docs, inline docs |
| UI/demo available | Manual verification | Console, CLI, web, or test page |
| End-to-end works | Manual verification | Feature works from start to finish |

**CRITICAL:** Never authorize commit without successful `make test`.

**Process:**
1. Run `make test` - if fails, return to Step 7
2. Run `make typecheck` - if fails, return to Step 7
3. Run `make lint` - if fails, return to Step 7
4. Verify documentation is complete:
   - README updated with feature
   - API docs updated (if applicable)
   - Inline code comments added
5. Verify UI/demo exists:
   - Console/CLI: command works with `--help`
   - Web: test page or demo available
   - Library: example usage in docs
6. Verify end-to-end experience:
   - Feature works from user perspective
   - All user flows tested
   - Error handling verified

**Example - Quart Webapp:**
- ✓ Backend functionality: WebSocket endpoint, health check
- ✓ Documentation: README, API docs
- ✓ UI: Test page at `/` with WebSocket test interface
- ✓ End-to-end: User can connect to WebSocket and see messages

**If any check fails:**
- Document what's missing
- Return to Step 7 (implementation)
- Provide specific feedback on what needs to be added

**Proceed to Step 8f only when ALL checks pass.**

## Step 8f: Pre-Commit Final Verification

**Purpose:** Final check before committing to ensure quality.

**Blocking Conditions:**

| Condition | Action |
|-----------|--------|
| Tests failed | Block commit, return to Step 7 |
| Type check failed | Block commit, return to Step 7 |
| Lint failed | Block commit, return to Step 7 |
| Documentation incomplete | Block commit, add documentation |
| No UI/demo available | Block commit, add UI/demo |
| End-to-end broken | Block commit, fix functionality |

**Verification Questions for User:**

If verification status is unclear from sub-agent reports, ask:

```
Before committing, I need to verify:

1. ✓ Tests: [pass/fail] (from python-developer report)
2. ? Standard run: Did the feature work when tested?
3. ? README: Does README.md need updates for this feature?
4. ? UI/demo: Is there a way to test/experience this feature?

Please confirm or indicate what needs updating.
```

**Only proceed to Step 9 when ALL verification checks pass.**

## Rejection Handling

**Maximum iterations:** 2 rounds of rejections before escalation.

**Iteration process:**
1. Collect all rejection feedback from all agents
2. Consolidate into actionable items
3. Return to Step 7 (Implementation) with consolidated feedback
4. Re-implement addressing all issues
5. Return through review cycle

**Escalation:**
After 2 failed iterations, ask user for guidance:
- Proceed with known issues?
- Reduce scope?
- Alternative approach?

## Review Report Template

Each agent creates a review report in `reporting/{task-name}/{agent}-review.md`:

```markdown
# {Agent Name} Review — {Task Name}

**Date:** YYYY-MM-DD
**Status:** Approved | Rejected

## Summary

[Brief summary of review findings]

## Findings

### Critical
- [Critical issues that must be fixed]

### Major
- [Important issues that should be fixed]

### Minor
- [Minor improvements/suggestions]

## Recommendations

[Specific actionable recommendations]

## Decision

- [x] Approved — Ready to proceed
- [ ] Rejected — Requires changes (see findings)
```

## Parallel Execution Benefits

Invoking agents in parallel improves efficiency:
- Independent perspectives (no groupthink)
- Faster overall review time
- Clear separation of concerns

**Note:** Functional review must complete before parallel domain reviews to ensure the implementation is functionally correct before assessing architecture and quality.