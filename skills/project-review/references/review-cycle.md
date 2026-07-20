# Review Cycle Execution

This document provides detailed guidance for the review cycle performed by the
`c3:project-review` skill. It is invoked from:

- `c3:project-manage` Phase 5.6 — initial implementation
- `c3:project-handle-pr` Phase 6.4 — PR-feedback re-validation (scoped)

## Review Sequence

The review cycle follows a strict sequence to ensure quality:

```
Stage a: Functional Review (BLOCKING)
    │
    ▼
Stage b: Domain Reviews (PARALLEL, by scope)
    │
    ▼
Stage c: Quality Reviews (PARALLEL)
    │
    ▼
Stage d: Documentation (IF user-facing)
    │
    ▼
Stage e: Functional Completeness + make check (BLOCKING)
    │
    ▼
Stage f: Pre-Commit Final Verification
```

## Stage a: Functional Review (Blocking)

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
   - Implementation plan from `reporting/{task-name}/plan.md` (initial) or the
     PR comment being addressed (iteration)
   - Key files modified
2. Functional-analyst reviews and approves/rejects
3. If rejected: collect feedback, return to implementation
4. If approved: proceed to Stage b

**Must pass before domain reviews.**

## Stage b: Domain Reviews (Parallel)

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
4. If any reject: consolidate feedback, return to implementation
5. If all approve: proceed to Stage c

## Stage c: Quality Reviews (Parallel)

**Purpose:** Validate code quality and test coverage.

**Agents (invoked in parallel):**
- `code-reviewer`
- `testing-engineer`

### code-reviewer Review

**Review Criteria:**
- Code follows project conventions
- No code smells or anti-patterns
- **Simplicity Check (MANDATORY):** enumerate every owner-stated proposal, worry, and constraint; respond to each (quote → state whether the implementation satisfies it). Flag every new class/indirection/wrapper/field/guard not in the owner's proposal or that violates a stated worry. **Wrapper/Pass-Through Test:** does any class/module only delegate to another class with no added logic (no orchestration, no multi-call-site coordination, no swappable implementation, no state the dependency lacks)? If yes, reject; callers should use the dependency directly. Reject reason: `"simplicity: thin wrapper — delegates without adding value; call the dependency directly."` Plus the existing Deletion Test, Abstraction Test, Library-First Test.
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
4. If any reject: consolidate feedback, return to implementation
5. If all approve: proceed to Stage d (if user-facing) or Stage e

## Stage d: Documentation (If User-Facing)

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
3. If rejected: return to implementation with feedback
4. If approved: proceed to Stage e

## Stage e: Functional Completeness + `make check` (Blocking)

**Purpose:** Ensure every commit is a functional whole and passes all quality checks.

**Principle:** Every commit must be a functional whole with:
1. Implemented functionality
2. Documentation (end-user and/or developer)
3. UI/demo (console, CLI, or web - depends on target)
4. End-to-end experience from day one

**Hard gate — `make check`:**

`make check` is the umbrella target that runs the full quality suite — test,
typecheck, lint, and format. It MUST pass before a commit is authorized.

| Check | Command | Requirement |
|-------|---------|-------------|
| All quality checks | `make check` | MUST pass — no exceptions |
| Documentation complete | Manual review | README, API docs, inline docs |
| UI/demo available | Manual verification | Console, CLI, web, or test page |
| End-to-end works | Manual verification | Feature works from start to finish |

**If the project Makefile does not provide `make check`**, run the equivalents
individually and require all to pass: `make test`, `make typecheck`, `make lint`,
`make format` (or `make check`'s documented equivalents).

**CRITICAL:** Never authorize commit without successful `make check`.

**Process:**
1. Run `make check` — if it fails, return to implementation
2. Verify documentation is complete:
   - README updated with feature
   - API docs updated (if applicable)
   - Inline code comments added
3. Verify UI/demo exists:
   - Console/CLI: command works with `--help`
   - Web: test page or demo available
   - Library: example usage in docs
4. Verify end-to-end experience:
   - Feature works from user perspective
   - All user flows tested
   - Error handling verified

**Example — Quart Webapp:**
- ✓ Backend functionality: WebSocket endpoint, health check
- ✓ Documentation: README, API docs
- ✓ UI: Test page at `/` with WebSocket test interface
- ✓ End-to-end: User can connect to WebSocket and see messages
- ✓ `make check` passes

**If any check fails:**
- Document what's missing
- Return to implementation
- Provide specific feedback on what needs to be added

**Proceed to Stage f only when ALL checks pass.**

## Stage f: Pre-Commit Final Verification

**Purpose:** Final check before committing to ensure quality.

**Blocking Conditions:**

| Condition | Action |
|-----------|--------|
| `make check` failed | Block commit, return to implementation |
| Documentation incomplete | Block commit, add documentation |
| No UI/demo available | Block commit, add UI/demo |
| End-to-end broken | Block commit, fix functionality |

**Verification Questions for the Caller/Owner:**

If verification status is unclear from sub-agent reports, ask:

```
Before committing, I need to verify:

1. ✓ make check: [pass/fail]
2. ? Standard run: Did the feature work when tested?
3. ? README: Does README.md need updates for this feature?
4. ? UI/demo: Is there a way to test/experience this feature?

Please confirm or indicate what needs updating.
```

**Only return "approved" when ALL verification checks pass.**

## Scoped Re-runs (PR Iteration, Phase 6.4)

When invoked from `project-handle-pr`, the cycle is scoped to the change:

- **Stage a always runs** — the functional-analyst confirms the change still
  satisfies the task's acceptance criteria. This is the core fix: PR-comment
  changes are re-validated against the task, not just executed and pushed.
- **Stage e always runs** — `make check` re-applies to every feedback round.
- **Stages b/c/d re-run for the affected scope only** — a backend-only tweak
  does not re-invoke `ui-ux-designer`; a non-user-facing change skips Stage d.

## Rejection Handling

**Maximum iterations:** 2 rounds of rejections before escalation.

**Iteration process:**
1. Collect all rejection feedback from all stages (gather the full picture,
   do not stop at the first reject)
2. Consolidate into actionable items
3. Return to implementation with consolidated feedback
4. Re-implement addressing all issues
5. Return through the review cycle

**Escalation:**
After 2 failed iterations, return `"escalate"` so the caller asks the owner:
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

**Note:** Functional review (Stage a) must complete before parallel domain
reviews to ensure the implementation is functionally correct before assessing
architecture and quality.
