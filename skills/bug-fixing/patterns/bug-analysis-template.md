# Bug Analysis Report Template

Use this template for documenting bug analysis in `docs/bug-analysis/{bug-id}.md`.

---

# Bug Analysis: {Bug Title}

**Bug ID:** {slug} (e.g., `login-timeout-error`)
**Date:** {YYYY-MM-DD}
**Status:** Analysis | Confirmed | In Progress | Fixed | Closed
**Severity:** S1-S4 (see severity matrix below)
**Priority:** P0-P5 (see priority matrix below)

---

## Summary

{2-3 sentences describing the bug in plain language}

## Symptoms

**Reported Behavior:**
{What the user reports happening}

**Expected Behavior:**
{What should happen instead}

**Impact:**
{Who is affected, how often, business impact}

## Reproduction Steps

1. {Step 1}
2. {Step 2}
3. {Step 3}
   ...
n. {Bug occurs}

**Environment:**
- Platform: {Web/Mobile/API}
- Browser/Device: {Chrome 120, iPhone 15, etc.}
- OS: {macOS 14, Windows 11, iOS 17, etc.}
- Version: {App/SDK version}

**Minimal Reproducible Example:**
{Code snippet or steps to create isolated reproduction}

## Root Cause Analysis

### Technique Used
{5 Whys | Fishbone Diagram | Both}

### Analysis

{5 Whys format:}

1. Why {symptom}?
   → {Cause 1}
2. Why {Cause 1}?
   → {Cause 2}
3. Why {Cause 2}?
   → {Cause 3}
4. Why {Cause 3}?
   → {Cause 4}
5. Why {Cause 4}?
   → **Root Cause: {Systemic issue}**

{OR Fishbone format:}

| Category | Potential Causes |
|----------|-------------------|
| Methods/Process | {List} |
| Machines/Tools | {List} |
| Materials/Data | {List} |
| People | {List} |
| Measurement | {List} |
| Environment | {List} |

### Root Cause

{Clear statement of the root cause}

**Type:**
| Type | Description |
|------|-------------|
| Logic error | Incorrect algorithm or condition |
| Data issue | Missing, invalid, or corrupted data |
| Integration | API or service communication |
| Configuration | Settings or environment |
| Performance | Scalability or speed |
| Security | Vulnerability or exposure |

## Proposed Fix

### Approach

{High-level description of fix strategy}

### Code Changes

| File | Change Type | Description |
|------|-------------|-------------|
| {path} | Modify/Add/Delete | {What changes} |

### Test Strategy

| Test Type | Framework | Description |
|-----------|-----------|-------------|
| Unit | {pytest/jest/etc.} | {What it tests} |
| Integration | {pytest/jest/etc.} | {What it tests} |
| E2E | {playwright/cypress/etc.} | {What it tests} |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | Low/Medium/High | Low/Medium/High | {How to mitigate} |

## UI/UX Impact

{Only if applicable - flagged by functional analyst}

**UI Changes Required:** Yes/No

| Change | Location | Description |
|--------|----------|-------------|
| {Change 1} | {Component/Page} | {Description} |

**UX Review Required:** Yes/No

## Implementation Notes

{Any additional context for implementer}

## Verification

### Before Fix

```bash
# Command to reproduce bug
{command}

# Expected: Bug occurs
# Actual: {What happens}
```

### After Fix

```bash
# Command to verify fix
{command}

# Expected: Bug is resolved
# Actual: {What happens}
```

### Regression Tests

- [ ] All existing tests pass
- [ ] New test added for this bug
- [ ] Edge cases covered

## Lessons Learned

{What can be done to prevent similar bugs}

### Prevention Measures

| Measure | Type | Implementation |
|---------|------|----------------|
| {Measure 1} | Test/Process/Tool | {How to implement} |

## Timeline

| Date | Action | Actor |
|------|--------|-------|
| {date} | Bug reported | {User/System} |
| {date} | Analysis started | {Analyst} |
| {date} | Root cause identified | {Developer} |
| {date} | Fix implemented | {Developer} |
| {date} | Review approved | {Reviewer} |

---

## Severity Matrix

| Level | Definition | Examples |
|-------|------------|----------|
| S1 - Critical | System crash, data loss, security breach | Payment fails, app crashes on startup |
| S2 - Major | Core feature broken, workaround exists | Search returns wrong results |
| S3 - Moderate | Feature impaired, workaround exists | Export requires extra steps |
| S4 - Minor | Cosmetic issues, low impact | Typos, misaligned buttons |

## Priority Matrix

| Level | Action | Typical SLA |
|-------|--------|-------------|
| P0 - Immediate | Fix now, block release | < 4 hours |
| P1 - Urgent/High | Fix this sprint | < 3 days |
| P2 - Medium | Fix next sprint | < 2 weeks |
| P3 - Low | Fix when capacity allows | < 2 months |
| P4/P5 - Backlog | Track but don't schedule | No SLA |

## Severity vs Priority Matrix

| Severity | High Business Impact | Medium Business Impact | Low Business Impact |
|----------|---------------------|----------------------|-------------------|
| S1 Critical | P1 Immediate | P1 Immediate | P2 High |
| S2 Major | P1 Immediate | P2 High | P3 Medium |
| S3 Moderate | P2 High | P3 Medium | P4 Low |
| S4 Minor | P3 Medium | P4 Low | P5 Backlog |