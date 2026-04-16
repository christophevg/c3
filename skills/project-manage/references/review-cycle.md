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
4. If approved: proceed to Step 9

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