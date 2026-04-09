# Root Cause Analysis Techniques

Methods for identifying the true cause of bugs.

## Overview

| Technique | Best For | Approach |
|-----------|----------|----------|
| 5 Whys | Simple to moderate problems | Deep, vertical drilling |
| Fishbone Diagram | Complex, multi-factor issues | Broad, horizontal brainstorming |

**Pro Tip:** Use Fishbone to brainstorm all possible causes, then apply 5 Whys to drill down into the most promising ones.

## 5 Whys Technique

### When to Use

- Simple to moderate complexity bugs
- Linear causal chains
- Quick analysis needed
- Individual or small group analysis

### Process

1. Start with the symptom/problem
2. Ask "Why?" five times
3. Each answer becomes the next "Why?" question
4. Stop when you reach a systemic root cause

### Example: Payment Bug

```
1. Why is "Place Order" button disabled?
   → JavaScript validation error

2. Why is validation failing?
   → Undefined value for discount calculation

3. Why is value undefined?
   → API response missing "discountAmount" field

4. Why is field missing?
   → Backend schema change not communicated

5. Why wasn't it communicated?
   → **Root Cause: No formal process for API contract documentation**
```

### Guidelines

| Do | Don't |
|----|-------|
| Ask "Why?" not "Who?" | Stop at symptoms |
| Go beyond first answer | Accept "because it is" |
| Involve people with context | Blame individuals |
| Document each step | Skip steps |
| Identify systemic causes | Stop too early |

### Anti-Patterns

- **Stopping too soon**: First "why" usually reveals symptoms
- **Blame language**: "Why did John break this?" vs "Why did the system allow this?"
- **Assumptions**: Verify each answer with evidence
- **Single path**: Some problems have multiple causes

## Fishbone Diagram (Ishikawa)

### When to Use

- Complex problems with multiple factors
- Team brainstorming sessions
- Need to explore all possibilities
- First time investigating an issue

### Process

1. Write the problem at the "head" of the fish
2. Draw main "bones" for each category
3. Brainstorm causes under each category
4. Identify most likely causes
5. Verify with data or testing

### Categories (6 Ms)

| Category | Focus | Examples |
|----------|-------|----------|
| **Methods/Process** | How work is done | Testing protocols, code review processes, deployment steps |
| **Machines/Tools** | Software, hardware | CI/CD pipeline, databases, IDEs, monitoring tools |
| **Materials/Data** | Inputs | Test data, API contracts, requirements documents |
| **People** | Skills, communication | Training, documentation, knowledge sharing |
| **Measurement** | Metrics | Test coverage, performance baselines, validation criteria |
| **Environment** | Runtime context | Servers, networks, configurations, time zones |

### Example: Slow Page Load

```
Problem: Page loads in 45+ seconds
├── Methods/Process
│   ├── No caching strategy
│   ├── Missing code review for performance
│   └── Incomplete testing checklist
├── Machines/Tools
│   ├── Database server underpowered
│   ├── No CDN for static assets
│   └── Monitoring not configured
├── Materials/Data
│   ├── Large unoptimized images
│   ├── Missing database indexes
│   └── Bloated API responses
├── People
│   ├── Team unfamiliar with ORM
│   ├── No performance training
│   └── Siloed frontend/backend teams
├── Measurement
│   ├── No performance baselines
│   ├── Missing load testing
│   └── No user metrics tracking
└── Environment
    ├── Production traffic spike
    ├── Regional server latency
    └── Third-party API slowdown
```

### Guidelines

| Do | Don't |
|----|-------|
| Involve diverse perspectives | Limit to one team |
| Use sticky notes for brainstorming | Critique during brainstorming |
| Group similar items | Leave items uncategorized |
| Vote on most likely causes | Assume all causes equal |
| Verify with data | Rely only on opinions |

## Combining Techniques

### Workflow: Fishbone → 5 Whys

1. **Use Fishbone first** to brainstorm all possible causes
2. **Vote or prioritize** the most likely causes
3. **Apply 5 Whys** to each top cause
4. **Document root causes** and action items

### Example: Combined Approach

**Phase 1: Fishbone Brainstorm**
- Team identifies 12 potential causes across 6 categories
- Top 3 causes by vote:
  1. Missing database indexes
  2. No caching strategy
  3. Large unoptimized images

**Phase 2: 5 Whys Deep Dive**
```
Why are indexes missing?
→ Developer didn't know to add them
Why didn't they know?
→ No performance training
Why no training?
→ Performance not prioritized
Why not prioritized?
→ Root Cause: No performance review process
```

## Root Cause Documentation Template

```markdown
### Root Cause Analysis

**Technique:** 5 Whys | Fishbone Diagram | Both

**Analysis:**
{5 Whys chain or Fishbone categories}

**Root Cause:**
{Clear statement of the systemic cause}

**Type:** Logic | Data | Integration | Configuration | Performance | Security

**Contributing Factors:**
- {Factor 1}
- {Factor 2}

**Evidence:**
{How the root cause was verified}
```

## Common Root Causes by Platform

### Frontend

| Symptom | Common Root Causes |
|---------|-------------------|
| Intermittent failures | Async race conditions, stale state |
| Wrong display | State mutation, missing dependencies |
| Performance | Unnecessary re-renders, memory leaks |

### Backend

| Symptom | Common Root Causes |
|---------|-------------------|
| Slow queries | Missing indexes, N+1 queries, stale statistics |
| Timeouts | Connection pool exhaustion, uncommitted transactions |
| Errors | Missing validation, incorrect error handling |

### Mobile

| Symptom | Common Root Causes |
|---------|-------------------|
| Crashes | Unhandled edge cases, memory leaks |
| UI issues | Device/OS variations, threading issues |
| Performance | Main thread blocking, excessive network calls |

### Database

| Symptom | Common Root Causes |
|---------|-------------------|
| Slow queries | Missing indexes, full table scans |
| Deadlocks | Lock ordering, long transactions |
| Data corruption | Missing constraints, concurrent writes |

## Blameless Postmortem Connection

Root cause analysis should feed into blameless postmortems:

| RCA Element | Postmortem Section |
|-------------|-------------------|
| Root Cause | "Root Cause" |
| Contributing Factors | "Contributing Factors" |
| Evidence | "Timeline" |
| Prevention | "Action Items" |

**Key Principle:** Focus on "How did the system allow this?" not "Who made the mistake?"

## Verification Checklist

After identifying root cause:

- [ ] Root cause explains all symptoms
- [ ] Root cause can be verified (not just assumed)
- [ ] Fix addresses root cause, not just symptoms
- [ ] Similar bugs are checked for same root cause
- [ ] Prevention measures are documented
- [ ] Action items have owners and deadlines