# Issue Review Workflow

This document describes how GitHub issues are processed before entering the backlog.

## Owner Authority Principle

⚠️ **CRITICAL: Only the repository owner can make final decisions.**

This is a governance constraint that must be enforced:

| Actor | Can | Cannot |
|-------|-----|--------|
| **Repository Owner** | Approve/reject issues, Add to backlog, Change labels, Close issues | — |
| **Non-owners (contributors, users)** | Post comments, Provide information, Make suggestions | Approve/reject, Trigger backlog additions, Change labels, Close issues |

**Repository Owner Definition:**
- The user who owns the repository (e.g., `username` in `github.com/username/repo`)
- Organization owners for org-owned repositories
- Users explicitly listed as maintainers in repository settings

**Enforcement:**
- Functional-analyst must verify comment author ownership before treating feedback as authoritative
- Non-owner comments are informational only
- When in doubt, ask: "Are you the repository owner?"

## Overview

Issues are classified and processed differently based on their type:

| Issue Type | Workflow |
|------------|----------|
| **Bug** | Immediate → Bug Fixer |
| **Feature** | Review → Clarify → Agree → Backlog |
| **Question** | Research or close |
| **Dependency** | Research → Backlog |

## Bug Workflow

Bugs are treated as URGENT and processed immediately:

1. **Detect** → Release-manager reports issue with `bug` label
2. **Mark** → Add `status:in-progress` label
3. **Spawn** → Bug-fixer agent handles complete TDD workflow
4. **Return** → Summary to project-manager after fix

No clarification needed - bugs need immediate fixing.

## Feature Workflow

Features REQUIRE review and clarification before entering the backlog:

### Step 1: Detection & Marking

```python
# Project-manager detects new feature issue
# Marks as being reviewed
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Add label 'status:in-progress' to issue #{number} and comment '🔍 Reviewing this feature request...'",
  description: "Mark issue as being reviewed"
})
```

### Step 2: Functional Analyst Review

Project-manager spawns functional-analyst to review:

```python
Agent({
  subagent_type: "c3:functional-analyst",
  prompt: """
  Review GitHub issue #{number} for acceptance into the backlog.
  
  Issue: {issue-title}
  Description: {issue-body}
  Labels: {issue-labels}
  
  Follow the GitHub Issue Review Workflow:
  1. Assess if the issue is well-defined
  2. Identify missing information or ambiguities
  3. Ask clarifying questions via GitHub issue comments if needed
  4. Only after full agreement with the issue owner, report back with:
     - Acceptance recommendation
     - Refined acceptance criteria
     - Suggested priority
  """,
  description: "Review feature issue #{number}"
})
```

### Step 3: Clarification Process

The functional-analyst follows the **GitHub Issue Review Workflow**:

#### Phase 1: Initial Assessment

Assess the quality of the issue definition:

| Quality Level | Indicators | Action |
|---------------|------------|--------|
| **Well-defined** | Clear problem, clear acceptance criteria, clear scope | Skip to Phase 3 |
| **Needs clarification** | Missing acceptance criteria, ambiguous scope, unclear problem | Proceed to Phase 2 |
| **Insufficient** | Missing problem statement, no context, cannot understand | Ask for complete rewrite |

#### Phase 2: Clarification

The functional-analyst posts clarification questions directly to GitHub using `gh issue comment`.

**Mindset:** Think through implications and possibilities before posting. Consider what could go wrong, what edge cases exist, and what alternatives might be better.

**Questions to ask:**

1. **Problem Statement**
   - "What problem does this solve?"
   - "Who is experiencing this problem?" (user personas)
   - "How often does this problem occur?"

2. **Acceptance Criteria**
   - "How will we know when this is complete?"
   - "What are the specific, testable requirements?"
   - "What edge cases should be considered?"

3. **Scope & Boundaries**
   - "What is explicitly out of scope?"
   - "Are there dependencies or blockers?"
   - "Is this a minimal viable solution or full solution?"

4. **Implications & Possibilities** (internal consideration, ask resulting questions)
   - Consider: What could go wrong? → Ask about error handling
   - Consider: Are there alternatives? → Ask about considered approaches
   - Consider: What edge cases exist? → Ask about specific scenarios

**Example command:**

```bash
gh issue comment {issue-number} --body "## 🔍 Issue Review

Thank you for this feature request. Before adding it to the backlog, I'd like to clarify a few things:

### Questions

1. **Problem**: Can you describe the specific problem this solves? Who is experiencing it?

2. **Acceptance Criteria**: What would you consider a complete implementation? What specific functionality should work?

3. **Scope**: Are there any edge cases or constraints we should consider?

4. **Alternatives**: Have you considered alternative approaches?"
```

#### Phase 3: Triage Completion

⚠️ **CRITICAL: Do NOT proceed to backlog until ALL steps are confirmed.**

**Triage is complete only when all 4 steps are done:**

##### Step 1: Analyst Has No More Clarifying Questions

After reviewing owner's answers:
- "Is anything still unclear?"
- "Are there edge cases not addressed?"
- "Do I understand the full scope?"

| Condition | Action |
|-----------|--------|
| More questions needed | Post them, return to Phase 2 |
| Satisfied | Proceed to Step 2 |

##### Step 2: Owner Confirms Nothing to Add

**Analyst must ask:** "Is there anything else you'd like to add or clarify?"

| Owner Response | Action |
|----------------|--------|
| Adds more information | Return to Step 1 |
| "Nothing else" / "That's all" | Proceed to Step 3 |

##### Step 3: Owner Explicitly Accepts with Priority

**Owner must confirm acceptance AND provide priority.**

**Acceptance confirmation:**
- "Looks good, let's do it"
- "Accepted, please proceed"
- "Approved for backlog"

**Priority specification:**
- Can be explicit: "Priority: P1"
- Can be implicit from context

**If owner accepts without priority:**
Ask: "What priority should this have? (P1=Critical, P2=High, P3=Medium, P4=Low)"

##### Step 4: Analyst Confirms Triage Complete

**Only after Steps 1-3:**

1. Report to project-manager:
   - "Issue #{number} fully triaged. Accepted by owner with priority {X}."
   - Summary: problem, acceptance criteria, priority

2. Update TODO.md:
   - Add task with acceptance criteria
   - Link to GitHub issue
   - Mark with agreed priority

---

## Example Triage Conversation

```
Analyst: [Posts clarification questions]
    ↓
Owner: [Answers questions]
    ↓
Analyst: [Reviews answers, has follow-up] "What about error handling?"
    ↓
Owner: [Answers follow-up]
    ↓
Analyst: [Satisfied] "Is there anything else you'd like to add?"
    ↓
Owner: "No, that's all. Looks good."
    ↓
Analyst: "What priority should this have?"
    ↓
Owner: "P1 - Critical"
    ↓
Analyst: Reports to project-manager: "Issue fully triaged. Accepted by owner with priority P1."
    ↓
Analyst: Updates TODO.md
    ↓
Project-manager: Continues with next backlog item
```

---

## What NOT to Do

| Don't | Why |
|-------|-----|
| Skip "anything else?" | Owner may have more context |
| Assume acceptance | Owner must explicitly confirm |
| Assume priority | Owner must specify |
| Proceed before all 4 steps | Incomplete triage leads to unclear requirements |

## Key Principles

1. **Owner authority** - Only repository owner can approve/reject issues
2. **Bugs are urgent** - No clarification, immediate action
3. **Features need clarity** - Always review before backlog
4. **Ask questions first** - Better to over-clarify than under-clarify
5. **Agreement required** - Only add to backlog after **owner** agreement
6. **Document decisions** - Clear acceptance criteria before implementation
7. **Non-owners are informational** - Their input is valuable but not authoritative

## Status Labels

| Label | Meaning | Action |
|-------|---------|--------|
| `status:backlog` | Reviewed, accepted, added to TODO.md | Keep open, implement later |
| `status:in-progress` | Currently being reviewed or implemented | Keep open, track progress |
| `status:wont-do` | Decision: won't implement | Close with explanation |
| `status:needs-research` | Needs evaluation | Keep open, research first |
| `status:blocked` | Blocked by dependency | Keep open, note blocker |

## Integration Points

- **Project-manager** → Coordinates the workflow
- **Functional-analyst** → Reviews and clarifies feature requests (posts comments directly)
- **Release-manager** → Updates labels, handles git operations
- **Bug-fixer** → Handles bugs immediately (no review needed)