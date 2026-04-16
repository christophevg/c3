---
name: project-feature
description: Capture and scope new features for a project. Use when user wants to add a new feature or says "/project feature". Can handle minimal descriptions (adds to unsorted backlog) or detailed descriptions (full scoping with functional-analyst). Examples: "add user authentication", "new feature: export to PDF".
---

# Project Feature

Capture and scope new features for a project. This skill handles the intake workflow for feature ideas, from quick captures to fully scoped requirements.

## Usage

```
/project-feature <feature description>
/project feature <feature description>
```

## Purpose

This skill is for **feature intake**, not implementation. It:
- Captures new feature ideas from the user
- Optionally scopes and prioritizes them via functional-analyst interview
- Adds features to TODO.md (prioritized or unsorted section)

**Implementation** happens via `/project-manage`, not this skill.

## Workflow

```
User provides feature description
        │
        ▼
   Is description
   detailed enough?
        │
   ┌────┴────┐
   No         Yes
   │          │
   ▼          ▼
Ask user   Proceed to
to detail   scoping
now?        │
   │          │
   ┌─┴─┐      │
   No Yes     │
   │  │       │
   ▼  ▼       ▼
Add to   Invoke
unsorted functional-
section  analyst
of       │
TODO.md  ▼
         Full scope
         & prioritize
         │
         ▼
         Add to
         TODO.md
```

## Behavior

### Step 1: Receive Feature Description

Parse the user's feature description. This can be:
- A single sentence: "add user authentication"
- A detailed description: "add user authentication with email/password, OAuth providers (Google, GitHub), and session management"
- A feature name with context

### Step 2: Analyze Completeness

Determine if the description is **detailed enough** for proper scoping:

| Completeness | Indicators |
|--------------|------------|
| **Minimal** | Single sentence, no context, no acceptance criteria |
| **Partial** | Has context but missing acceptance criteria or technical details |
| **Detailed** | Clear requirements, acceptance criteria, and/or technical context |

### Step 3: Ask to Detail (If Minimal)

If the description is minimal or partial, ask the user:

```
Use AskUserQuestion tool:

Question: "Would you like to provide more details for this feature now?"

Options:
- "Yes, let's scope it properly" — Invoke functional-analyst for full scoping
- "No, just capture it for now" — Add to unsorted section
- "Cancel" — Abort feature capture
```

### Step 4A: Add to Unsorted Section (If Declined)

If the user declines detailed scoping:

1. Read TODO.md (create if missing)
2. Add to **"Unsorted Features"** section at the top:

```markdown
# TODO

## Unsorted Features

- [ ] [Feature description - needs scoping]
- [ ] [Another quick capture]

## Backlog (Prioritized)

### P0 - Critical
...
```

3. Confirm to user: "Added to unsorted features. Use `/project-manage` when ready to scope and implement."

### Step 4B: Invoke Functional-Analyst (If Accepted or Detailed)

If the user accepts or the description is already detailed:

1. **Invoke functional-analyst agent** with:
   - The feature description
   - Request to interview user for full requirements
   - Instruction to create acceptance criteria

2. **Functional-analyst delivers**:
   - Comprehensive feature specification
   - Acceptance criteria
   - Priority recommendation (P0-P3)
   - Dependencies on other features

3. **Add to TODO.md** in the appropriate priority section:

```markdown
## Backlog (Prioritized)

### P1 - High

- [ ] **Feature: User Authentication**
  - Email/password login with validation
  - OAuth providers: Google, GitHub
  - Session management with 7-day expiry
  - Password reset via email
  - **Acceptance Criteria:**
    - User can register with email/password
    - User can login with OAuth providers
    - Session persists for 7 days
    - Password reset email sent within 30 seconds
  - **Dependencies:** None
```

4. **Confirm to user**:
   - Summary of the scoped feature
   - Priority assigned
   - Any dependencies identified

## TODO.md Structure

When creating or updating TODO.md, use this structure:

```markdown
# TODO

## Unsorted Features

- [ ] [Minimal description - needs scoping]
- [ ] [Another quick capture]

## Backlog (Prioritized)

### P0 - Critical
- [ ] [Critical task]

### P1 - High
- [ ] [High priority task]

### P2 - Medium
- [ ] [Medium priority task]

### P3 - Low
- [ ] [Low priority task]

## Done

- [x] [Completed task] — YYYY-MM-DD
```

## File Conventions

| File | Purpose |
|------|---------|
| `TODO.md` | Project backlog with unsorted and prioritized sections |
| `analysis/functional.md` | Created by functional-analyst during scoping |

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `/project-manage` | Picks up features from TODO.md and implements them |
| `/project-status` | Shows TODO.md summary and next tasks |
| `/project` | Dispatcher that routes to this skill |

## Examples

### Example 1: Minimal Feature (Quick Capture)

```
User: /project-feature add dark mode

Agent: The feature description is minimal. Would you like to provide more details now?

User: No, just capture it for now

Agent: Added to unsorted features:
- [ ] Dark mode - needs scoping

Use /project-manage when ready to scope and implement.
```

### Example 2: Detailed Feature (Full Scoping)

```
User: /project-feature add user authentication with email/password, OAuth (Google, GitHub), session management

Agent: This is a detailed feature description. I'll invoke the functional-analyst to scope it properly.

[Invokes functional-analyst]

[Functional-analyst interviews user and creates specification]

Agent: Feature added to backlog:
- Priority: P1 - High
- Acceptance criteria defined
- No dependencies

Ready to implement? Use /project-manage to start the workflow.
```

### Example 3: Via Dispatcher

```
User: /project feature add export to PDF

Agent: [Routes to project-feature]
[Parses feature description]
[Asks about scoping or proceeds based on detail level]
```

## Notes

- This skill is for **intake only** — implementation is handled by `/project-manage`
- The functional-analyst owns the TODO.md structure and acceptance criteria
- Unsorted features are processed during `/project-manage` Phase 1B
- Priority levels: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- Dependencies are tracked and can block feature start