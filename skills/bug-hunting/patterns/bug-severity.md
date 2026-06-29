# Bug Severity Definitions

Framework for classifying and prioritizing bugs based on impact and urgency.

## Severity Levels

### Critical (S1)

**Definition:** System is unusable, data is at risk, or security is compromised.

**Criteria:**
- Data loss or corruption
- Security vulnerability exploitable in production
- System crash or hang in production
- No workaround exists
- Blocks all users from core functionality

**Examples:**
- Authentication bypass
- Database corruption
- Memory leak causing crash
- Remote code execution vulnerability
- Payment processing failure
- Data exposure to unauthorized users

**Action:**
- Fix immediately
- Halt release if found pre-release
- Page on-call engineer if in production
- Post-mortem required after fix

**Timeline:** Fix within hours (same day)

---

### High (S2)

**Definition:** Core feature is broken but workaround exists, or significant user impact.

**Criteria:**
- Core functionality impaired
- Workaround exists but is difficult
- Affects significant user base
- Performance severely degraded
- Data inconsistency (but no loss)

**Examples:**
- Search returns wrong results
- Export fails for large datasets
- Slow login (>30 seconds)
- Configurations not saving correctly
- Notifications not delivered
- API endpoints returning errors

**Action:**
- Fix before next release
- Communicate workaround to users
- Monitor for escalation

**Timeline:** Fix within days (current sprint)

---

### Medium (S3)

**Definition:** Feature partially broken, workaround exists and is reasonable.

**Criteria:**
- Non-critical feature broken
- Easy workaround exists
- Affects subset of users
- Performance moderately degraded
- Cosmetic data issues

**Examples:**
- Export requires extra steps
- Sorting doesn't work on one column
- Slow loading on specific pages
- Filters reset unexpectedly
- UI layout broken on one browser
- Error messages unclear

**Action:**
- Fix in next iteration
- Document workaround
- Consider for batch fix session

**Timeline:** Fix within weeks (next sprint)

---

### Low (S4)

**Definition:** Minor issue with minimal impact, cosmetic or enhancement.

**Criteria:**
- Cosmetic issue only
- Affects very few users
- No functional impact
- Enhancement request
- Documentation issue

**Examples:**
- Typos in UI text
- Minor UI misalignment
- Color inconsistency
- Unclear error message
- Missing tooltip
- Log noise

**Action:**
- Document as known issue
- Fix when convenient
- Batch with other minor fixes
- Consider for "bug bash" sessions

**Timeline:** Fix when capacity allows (backlog)

---

## Priority Matrix

Priority combines severity with business impact and urgency.

### Priority Levels

| Level | Action | Typical SLA |
|-------|--------|-------------|
| P0 - Immediate | Fix now, block release | < 4 hours |
| P1 - Urgent | Fix this sprint | < 3 days |
| P2 - High | Fix next sprint | < 2 weeks |
| P3 - Medium | Fix when capacity allows | < 1 month |
| P4 - Low | Backlog | No SLA |
| P5 - Backlog | Track but don't schedule | No SLA |

### Severity vs Priority Matrix

| Severity | High Business Impact | Medium Business Impact | Low Business Impact |
|----------|---------------------|----------------------|-------------------|
| S1 Critical | P0 Immediate | P1 Urgent | P2 High |
| S2 Major | P1 Urgent | P2 High | P3 Medium |
| S3 Moderate | P2 High | P3 Medium | P4 Low |
| S4 Minor | P3 Medium | P4 Low | P5 Backlog |

**Business Impact Assessment:**
- **High:** Affects paying customers, revenue, or critical workflows
- **Medium:** Affects active users or important features
- **Low:** Affects few users or edge cases

---

## Examples by Category

### Security Bugs

| Bug | Severity | Priority |
|-----|----------|----------|
| SQL injection in user input | Critical (S1) | P0 |
| XSS in user profile | Critical (S1) | P0 |
| Auth token in URL | High (S2) | P1 |
| Missing rate limiting | High (S2) | P2 |
| Verbose error messages | Medium (S3) | P3 |
| Missing security headers | Medium (S3) | P3 |

### Data Bugs

| Bug | Severity | Priority |
|-----|----------|----------|
| Data loss on save | Critical (S1) | P0 |
| Data corruption | Critical (S1) | P0 |
| Inconsistent data display | High (S2) | P1 |
| Missing data validation | High (S2) | P2 |
| Minor data formatting issue | Medium (S3) | P3 |
| Logging excessive data | Low (S4) | P4 |

### Performance Bugs

| Bug | Severity | Priority |
|-----|----------|----------|
| System unusable (>30s load) | Critical (S1) | P0 |
| Core feature timeout | High (S2) | P1 |
| Slow specific operation (5-30s) | Medium (S3) | P2 |
| Minor slowdown (2-5s) | Medium (S3) | P3 |
| Sub-second delay | Low (S4) | P4 |

### UI/UX Bugs

| Bug | Severity | Priority |
|-----|----------|----------|
| App crashes on load | Critical (S1) | P0 |
| Core feature inaccessible | Critical (S1) | P0 |
| UI broken on main browsers | High (S2) | P1 |
| Mobile layout broken | High (S2) | P2 |
| Minor layout issue | Medium (S3) | P3 |
| Typo or color issue | Low (S4) | P4 |

---

## Severity Determination Guide

### Questions to Ask

1. **Data Impact**
   - Can data be lost or corrupted?
   - Is data exposed to unauthorized users?
   - Are backups affected?

2. **User Impact**
   - How many users are affected?
   - Can users complete their tasks?
   - Is there a workaround?

3. **Business Impact**
   - Does it affect revenue?
   - Does it affect reputation?
   - Are there compliance implications?

4. **Frequency**
   - How often does it occur?
   - Is it reproducible?
   - What triggers it?

5. **Workaround Quality**
   - Does a workaround exist?
   - How complex is the workaround?
   - Do users know about it?

### Decision Tree

```
Is the system usable?
├─ No → Can users work around it?
│        ├─ No → Critical (S1)
│        └─ Yes, but difficult → High (S2)
└─ Yes → Is a core feature broken?
         ├─ Yes → Is there a reasonable workaround?
         │        ├─ No → High (S2)
         │        └─ Yes → Medium (S3)
         └─ No → Is it cosmetic or minor?
                  ├─ No → Medium (S3)
                  └─ Yes → Low (S4)
```

---

## Escalation Rules

### When to Escalate

- **Severity Increase:** If bug affects more users or data than initially thought
- **Priority Increase:** If business impact increases (customer complaint, deadline)
- **Blocking:** If bug blocks other work or releases
- **Security:** If security implications discovered

### Escalation Path

1. **Developer** → Team Lead (if blocked or need guidance)
2. **Team Lead** → Engineering Manager (if resource conflict)
3. **Engineering Manager** → Product Manager (if business impact changes)
4. **Product Manager** → Director (if customer/revenue impact)
5. **Director** → VP Engineering (if critical security or data loss)

---

## Tracking and Reporting

### Bug Report Fields

```markdown
## Bug Report

**ID:** [unique identifier]
**Title:** [concise description]
**Severity:** [S1-S4]
**Priority:** [P0-P5]

**Description:**
[What is wrong]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
...

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Impact:**
- Users affected: [number or percentage]
- Workaround available: [Yes/No]
- Business impact: [description]

**Environment:**
- Version: [affected versions]
- Browser/OS: [if relevant]
- Config: [if relevant]

**Attachments:**
- Screenshots
- Logs
- Test cases
```

### Metrics to Track

- **Time to Triage:** Time from report to severity assignment
- **Time to Fix:** Time from severity assignment to fix
- **Regressions:** Bugs that recur after fix
- **Severity Distribution:** Count by severity level
- **Age by Severity:** How long bugs stay at each severity

---

## Communication Templates

### Critical Bug Notification

```markdown
🚨 **CRITICAL BUG ALERT**

**Bug:** [Title]
**Severity:** S1 (Critical)
**Impact:** [Description]
**Action Required:** Fix immediately

**Status:** [Investigating/Fix in Progress/Testing]

**Updates:**
- [Time] [Update]
```

### Release Blocker

```markdown
⚠️ **RELEASE BLOCKER**

**Bug:** [Title]
**Reason:** [Why it blocks release]
**Status:** [Status]
**ETA:** [Expected fix time]

**Approval Required:** [Who needs to approve]
```

### Customer Communication

```markdown
**Known Issue: [Title]**

**Status:** [Status]
**Impact:** [What users experience]
**Workaround:** [If available]

**Next Update:** [When to expect update]
**Tracking:** [Issue link]
```