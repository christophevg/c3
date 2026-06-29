---
name: project-manage
description: Use this skill to manage the entire project workflow, orchestrating specialized agents (functional analyst, API architect, UI/UX designer) to ensure proper analysis, design, implementation, and review of all tasks. Handles both new features and bug fixes with appropriate workflows. Examples: "Start working on the project", "Implement the next task", "Fix the authentication bug".
---

# Manage Project

## ⛔ STOP: READ THIS FIRST

**THE PROJECT ROOT IS REPORTED BY RELEASE-MANAGER.**

**FIRST ACTION: Delegate to release-manager to get project state.**

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Report project state",
  description: "Get project state"
})
```

The release-manager will report:
- **Working Directory** (project root)
- **Project Type** (Website or Software)
- Current branch
- Open PRs and their status
- Open issues
- Recent commits
- Last tag

**Use the working directory from the report as the project root.**

**IGNORE:**
- Any "base directory" from skill loading
- Any paths in PERSONAL.md
- Any paths in memory files
- Any paths shown in git status from previous conversations
- Any absolute paths to ~/Workspace/agentic/c3/ or ~/Workspace/agentic/incubator/

**ONLY USE:**
- The working directory from release-manager's report
- All file paths are relative to that output: TODO.md, analysis/, reporting/

---

## Session Start: Get Project State

**CRITICAL: Project-manager does NOT run git/gh commands directly. Always delegate to release-manager.**

**At the start of each session, delegate to release-manager to get project state:**

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Report project state",
  description: "Get project state"
})
```

The release-manager will:
- Sync with remote (git pull)
- Check current branch
- Check for open PRs
- Check for open issues
- Report recent commits and last tag

**Based on the state reported by release-manager, determine next action:**

| State | Action |
|-------|--------|
| Open PR with pending feedback | Address feedback in PR comments |
| Open PR waiting for owner | Report status, wait for owner |
| Merged PR on feature branch | Handle post-merge workflow (delegate to release-manager) |
| Clean main/master | Start new task from TODO.md |
| Open issues | Process issues (Phase 0A) |

---

## Post-Merge State Handling

**When release-manager reports a merged feature branch:**

1. **Handle untracked artifacts** (from release-manager report):
   - Analysis files in `analysis/` from merged work
   - These should already be committed to the PR

2. **Delegate to release-manager to switch to main:**
   ```
   Agent({
     subagent_type: "c3:release-manager",
     prompt: "Switch to main branch and pull latest",
     description: "Switch to main"
   })
   ```

3. **Delegate to functional-analyst to verify TODO.md:**
   - Find task referenced in merged PR
   - Ensure completion date is present
   - Ensure task is in Done section

---

## PR Status Handling

**When release-manager reports an open PR:**

The release-manager's report includes PR status. Based on that:

| PR Status | Action |
|-----------|--------|
| CI failing | Delegate to developer to fix |
| CI passing, review pending | Wait for owner |
| Changes requested | Delegate to developer to address |
| Approved | Wait for owner to merge |

**Do NOT run `gh pr checks` or `gh pr view` directly - get this info from release-manager.**

---

## Issue Processing

**When release-manager reports open issues:**

Issues are reported by release-manager. Process them based on labels:

| Label | Action |
|-------|--------|
| `status:backlog` | Already tracked, skip |
| `status:in-progress` | Continue work |
| No status label | New issue, needs triage |

**To update issue labels, delegate to release-manager:**
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Add label 'status:backlog' to issue #{number}",
  description: "Update issue label"
})
```

---

This skill is invoked by the user to manage the entire project workflow, orchestrating specialized agents to ensure proper analysis, design, implementation, and review of all tasks.

## Workflow Overview

```
User Request
    │
    ▼
Task Type Detection ──── Bug ───► Bug Fixing Workflow
    │
    ▼ Feature
GitHub Issue Check
    │
    ▼
Project State Detection
    │
    ├── New Project ───────────► Phase 1A (Analysis)
    │                                  │
    │                                  ▼
    │                             Research (conditional)
    │                                  │
    ├── Incomplete Setup ───────► Phase 1B (Review)
    │                                  │
    │                                  ▼
    │                             Research (conditional)
    │                                  │
    └── Ready for Work ─────────► Check Unsorted Items
                                       │
                                       ├── Has Unsorted ──► Ask: Sort or Skip?
                                       │                            │
                                       │                            ├── Sort ──► Functional Analysis
                                       │                            │                   │
                                       │                            └── Skip ─────────────┤
                                       │                                                │
                                       └── No Unsorted ──────────────────────────────────┤
                                                                                        │
                                                                                        ▼
                                                                                Propose Next Task
                                                                                        │
                                                                                        ▼
                                                                                Task Scope Classification
                                                                                        │
                                                                                        ▼
                                                                                Phase 2 (Domain Review)
                                                                                        │
                                                                                        ▼
                                                                                Phase 3 (Consensus)
                                                                                        │
                                                                                        ▼
                                                                                Phase 4 (Implementation)
                                                                                        │
                                                                                        ▼
                                                                                Review Cycle (parallelized)
                                                                                        │
                                                                                        ▼
                                                                            Create Feature Branch
                                                                                        │
                                                                                        ▼
                                                                            Commit to Branch
                                                                                        │
                                                                                        ▼
                                                                            Push & Create PR
                                                                                        │
                                                                                        ▼
                                                                    ┌────────────── Check PR Feedback ──────────────┐
                                                                    │                                                │
                                                                    │  Has Owner Comments?                           │
                                                                    │       │                                        │
                                                                    │       ├── Yes ──► Address Feedback            │
                                                                    │       │            │                           │
                                                                    │       │            ├── Make Changes            │
                                                                    │       │            ├── Push                     │
                                                                    │       │            ├── Wait for CI             │
                                                                    │       │            └── Comment on PR            │
                                                                    │       │                                        │
                                                                    │       └── No ──► Wait for Owner                │
                                                                    │                   │                            │
                                                                    └───────────────────┴────────────────────────────┘
                                                                                                │
                                                                                                ▼
                                                                                    ┌─── Owner Merges PR ─────┐
                                                                                    │                         │
                                                                                    ▼                         ▼
                                                                                User Merges PR       User Provides More Feedback
                                                                                    │                         │
                                                                                    ▼                         │
                                                                            Mark Task Complete ◄───────┘
```

---

## Task Type Detection

Before starting, detect whether the task is a **feature**, **bug**, or **dependency**:

| Task Type | Indicators |
|-----------|------------|
| **Bug** | "fix", "bug", "issue", "broken", "error", "doesn't work", "crash", "fails" |
| **Feature** | "add", "create", "implement", "build", "new", "feature", "enhance" |
| **Dependency** | "upgrade", "update", "bump", "dependencies", "package", "release", "version" |

**If the task is a BUG:**
- **Spawn the `c3:bug-fixer` agent** to handle the complete TDD-based workflow
- This keeps project-manager context clean
- Bug-fixer returns concise summary when complete

```python
Agent({
  subagent_type: "c3:bug-fixer",
  prompt: "Fix {issue-reference}: {bug-description}",
  description: "Fix {issue-number}"
})
```

**If the task is a DEPENDENCY:**

Determine task complexity:

| Complexity | Example | Workflow |
|------------|---------|----------|
| Simple upgrade | "Upgrade yoker to 2.1.0" | Researcher → python-developer |
| Upgrade with goal | "Upgrade yoker to simplify our codebase" | Researcher → functional-analyst |

**Workflow:**

```python
# Step 1: Spawn researcher to gather package information
# Researcher will use mcp__plugin_c3_pkgq__find_package automatically for Python packages
Agent({
  subagent_type: "c3:researcher",
  prompt: "Research Python packages: {packages}. Include: capabilities, patterns, breaking changes, migration steps.",
  description: "Research {packages}"
})

# Step 2: Collect research results

# Step 3: Route based on complexity

# For simple upgrade:
Agent({
  subagent_type: "c3:python-developer",
  prompt: """
  Upgrade {packages}.

  Research findings:
  {research_results}

  Use the migration guides to update imports and handle breaking changes.
  """,
  description: "Upgrade {package}"
})

# For upgrade with goal:
Agent({
  subagent_type: "c3:functional-analyst",
  prompt: """
  Task: {user_goal}

  Research findings:
  {research_results}

  Analyze how to use these new features to achieve the goal.
  Identify what code in our project can be simplified.
  Create TODO.md with implementation tasks.
  """,
  description: "Analyze upgrade"
})
```

**If the task is a FEATURE:**
- Use the **Feature Development Workflow** (continue to Phase 0)

---

## Feature Development Workflow

When the task is identified as a feature, follow this sequential workflow:

### Phase 0A: GitHub Issue Check

⛔ **MANDATORY: This step uses data from release-manager's project state report.**

**Issues are reported by release-manager during session start. Do NOT run gh commands directly.**

Based on the issues reported by release-manager:

1. **Review reported issues** (from release-manager's state report)
2. **Filter out issues with status labels** (already reviewed):
   - Issues without status labels are new and need triage
3. **Classify each new issue by type:**

| Issue Type | Indicators | Workflow |
|------------|------------|----------|
| **Bug** | Labels: `bug`, `error`, `crash`, `broken`, `fix` | Immediate → Bug Fixer |
| **Feature** | Labels: `enhancement`, `feature`, `new`, `add` | Review → Clarify → Backlog |
| **Question** | Labels: `question`, `help`, `discussion` | Research or close |
| **Dependencies** | Labels: `dependencies`, `upgrade` | Research → Backlog |

4. **Handle each issue type appropriately:**

#### Bug Issues (URGENT - Immediate Action)

For bugs, do NOT ask for confirmation - spawn bug-fixer immediately:

```python
# Mark as in-progress
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Add label 'status:in-progress' to issue #{number}",
  description: "Mark bug in progress"
})

# Spawn bug-fixer
Agent({
  subagent_type: "c3:bug-fixer",
  prompt: "Fix {issue-number}: {issue-title}\n\n{issue-body}",
  description: "Fix bug {issue-number}"
})
```

#### Feature Issues (REQUIRE REVIEW - Clarify First)

**CRITICAL: Feature issues must be reviewed by functional-analyst before adding to backlog.**

⚠️ **OWNER AUTHORITY: Only the repository owner can make final decisions.**
- Non-owner comments are informational only
- Only owner approval can move issue to backlog
- Functional-analyst must verify commenter ownership

For each feature issue without a status label:

**Step 1: Mark as being reviewed**

```python
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Add label 'status:in-progress' to issue #{number} and comment '🔍 Reviewing this feature request...'",
  description: "Mark issue as being reviewed"
})
```

**Step 2: Delegate to functional-analyst for review**

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
  3. Ask clarifying questions via GitHub issue comments if needed (use `gh issue comment`)
  4. CRITICAL: Only the repository owner can approve. Verify commenter ownership.
  5. Only after full agreement with the OWNER, report back with:
     - Acceptance recommendation
     - Refined acceptance criteria
     - Suggested priority
     - Confirmation that owner agreement was reached
  """,
  description: "Review feature issue #{number}"
})
```

**Step 3: After functional-analyst reports OWNER agreement**

When the functional-analyst reports that **repository owner** agreement is reached:

```python
# Accept issue → add to backlog
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Remove label 'status:in-progress' and add label 'status:backlog' to issue #{number}. Comment: '✅ Reviewed and accepted by owner. Added to TODO.md with priority {priority}.'",
  description: "Accept issue into backlog"
})

# Delegate to functional-analyst to update TODO.md
Agent({
  subagent_type: "c3:functional-analyst",
  prompt: "Add issue #{number} to TODO.md backlog with agreed acceptance criteria.",
  description: "Update TODO.md"
})
```

**Step 4: Commit and Push TODO.md Updates**

After the issue is accepted into the backlog, commit and push the TODO.md changes immediately:

```python
# Commit and push TODO.md updates
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Commit TODO.md and REQUIREMENTS.md changes with message: 'docs: add task {task-id} to TODO.md after issue #{number} triage'",
  description: "Commit triage updates"
})

Agent({
  subagent_type: "c3:release-manager",
  prompt: "Push commit to remote",
  description: "Push triage updates"
})
```

This prevents accumulating uncommitted changes during triage.

**If non-owner attempts to approve:**

The functional-analyst should respond: "Thank you for your input! However, only the repository owner can approve this issue for the backlog. I'll wait for @owner to confirm."

#### Question/Discussion Issues

```python
# Research first, then decide
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Add label 'status:needs-research' to issue #{number} and comment 'Needs evaluation for...'",
  description: "Mark for research"
})
```

#### Rejecting Issues

```python
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Add label 'status:wont-do' to issue #{number} and close with comment 'Closing: not in scope because...'",
  description: "Reject issue"
})
```

**Issue Status Labels:**

| Label | Meaning | Action |
|-------|---------|--------|
| `status:backlog` | Reviewed, accepted, added to TODO.md | Keep open, implement later |
| `status:in-progress` | Currently being reviewed or implemented | Keep open, track progress |
| `status:wont-do` | Decision: won't implement | Close with explanation |
| `status:needs-research` | Needs evaluation | Keep open, research first |
| `status:blocked` | Blocked by dependency | Keep open, note blocker |

---

### "Follow Up on Issue" Handling

**When the user says "follow up on issue #{number}" or "check issue #{number}":**

⚠️ **CRITICAL: Do NOT decide yourself. Delegate to functional-analyst.**

The project-manager should NOT:
- Check issue status directly
- Read comments and decide if answers are sufficient
- Proceed to implementation without functional-analyst confirmation

**Agent Session Continuity:**

When continuing a conversation with the same functional-analyst (e.g., after asking "follow up"), use `SendMessage` with the agent ID to preserve context from previous iterations. This avoids re-asking questions the agent already knows the answer to.

**Instead, delegate to functional-analyst:**

```python
Agent({
  subagent_type: "c3:functional-analyst",
  prompt: """
  Continue reviewing GitHub issue #{number}.

  1. Check for new comments (use `gh issue view {number} --comments`)
  2. Verify comment author is repository owner
  3. Follow the Triage Completion process:
     - Step 1: Do YOU have any more questions?
     - Step 2: Has owner confirmed nothing to add?
     - Step 3: Has owner accepted with priority?
     - Step 4: Confirm triage complete
  4. Report back with one of:
     - "Need more clarification: [what's missing]" → Post clarification questions
     - "Waiting for owner to confirm nothing to add" → Post "Is there anything else?"
     - "Waiting for owner to specify priority" → Post priority question
     - "Issue fully triaged: accepted by owner with priority X" → Ready for backlog
  """,
  description: "Continue issue review"
})
```

**Wait for functional-analyst to report.**

| Functional-analyst Reports | Action |
|---------------------------|--------|
| "Need more clarification" | Functional-analyst posts questions, workflow pauses |
| "Waiting for owner" | Functional-analyst posts question, workflow pauses |
| "Issue fully triaged" | Add to backlog, move to next issue |

**After functional-analyst posts a comment:**
- Do NOT immediately check for feedback
- Move to next issue/PR
- User will say "follow up" to check for responses later

If functional-analyst reports triage complete:
1. Delegate to release-manager to update labels (`status:backlog`)
2. Delegate to functional-analyst to update TODO.md
3. Move to next issue/PR (do not pause)

5. Continue to Phase 0B after issues are handled

---

### Phase 0B: Project State Detection

Check the project's analysis artifacts to determine the appropriate workflow:

| State | `analysis/functional.md` | `TODO.md` | Action |
|-------|--------------------------|-----------|--------|
| **New Project** | Missing | Missing | Initial Analysis (Phase 1A) |
| **Incomplete Setup** | Exists | Missing | Review and Backlog (Phase 1B) |
| **Ready for Work** | Exists | Exists | Check for Unsorted Items |

#### State Detection Steps

1. Check if `analysis/functional.md` exists
2. Check if `TODO.md` exists with prioritized tasks

---

### Phase 1A: Initial Functional Analysis (New Project)

When `analysis/functional.md` or `TODO.md` is missing:

1. **Invoke functional-analyst agent** to:
   - Review high-level functional requirements (README.md, existing documentation)
   - Review existing code structure if available
   - Interview user to clarify topics needing more information
   - Create `analysis/functional.md` with comprehensive functional analysis
   - Create `TODO.md` with prioritized backlog of atomic, well-defined tasks

2. **Conditional: Invoke researcher agent when**:
   - Functional analysis identifies gaps needing best practices proposals
   - User explicitly requests research to address functional-analyst questions
   - Technology choice needs evaluation and recommendations

   **Researcher delivers**:
   - Research findings in `research/{topic}.md`
   - Technology recommendations with pros/cons
   - Best practices proposals for identified gaps

Then proceed to **Task Scope Classification** (below).

---

### Phase 1B: Review and Backlog Creation (Existing Analysis)

When `analysis/functional.md` exists but `TODO.md` is missing:

1. **Invoke functional-analyst agent** to:
   - Review existing `analysis/functional.md`
   - Review current project state
   - Interview user to update understanding if needed
   - Create `TODO.md` with prioritized backlog

2. **Conditional: Invoke researcher agent when**:
   - Existing analysis needs technology investigation
   - User requests research for specific questions

Then proceed to **Task Scope Classification** (below).

---

### Task Scope Classification

After Phase 1A or 1B completes, classify the task scope:

| Scope | Indicators | Required Domain Agents |
|-------|------------|------------------------|
| **Backend only** | "API", "endpoint", "backend", "data model", no UI | api-architect, security-engineer* |
| **Frontend only** | "UI", "UX", "frontend", "component", "page", no backend | ui-ux-designer |
| **Full stack** | Both backend and frontend mentioned | api-architect, ui-ux-designer, security-engineer* |
| **Documentation only** | "document", "readme", "guide" | end-user-documenter |
| **Research only** | "research", "investigate", "evaluate" | researcher |

#### Security Task Detection

Include `security-engineer` when task involves:
- Authentication or authorization changes
- Sensitive data handling (PII, credentials, payments)
- External API integrations
- User input processing
- File operations
- Configuration changes affecting security

#### Ready for Work State

When both `analysis/functional.md` and `TODO.md` exist:

**Step 1: Check for Unsorted Items**

Read `TODO.md` and check for an `## Unsorted` section at the top. Unsorted items are quick ideas the user captured but haven't been analyzed and integrated into the prioritized backlog.

**Step 2: Check for Unsorted MBIs**

If `PLAN.md` exists, check for an `## Unsorted MBIs` section. These are raw MBI ideas that haven't been analyzed yet.

**Step 3: Determine Next Action**

| Condition | Action |
|-----------|--------|
| No unsorted items or MBIs | Proceed directly to proposing next task |
| Unsorted items exist | Ask user whether to sort unsorted items first |
| Unsorted MBIs exist | Ask user whether to analyze MBIs first |

**If unsorted items exist, use AskUserQuestion tool:**

```
Question: "Found {count} unsorted item(s) in TODO.md and/or {mbi_count} unsorted MBI(s) in PLAN.md. These need analysis. How would you like to proceed?"

Options:
- "Sort unsorted items first" — Run functional analysis to integrate them into backlog
- "Analyze unsorted MBIs" — Process raw MBI ideas into proper MBIs
- "Show next backlog task" — Proceed with existing prioritized tasks
- "Show all items" — Display both unsorted and backlog items
```

**Step 4: Handle User Choice**

- **"Sort unsorted items first"**: Invoke functional-analyst to analyze each unsorted item and integrate into prioritized backlog, then propose next task
- **"Analyze unsorted MBIs"**: Invoke functional-analyst to analyze each unsorted MBI and create proper MBI entries in PLAN.md
- **"Show next backlog task"**: Proceed to propose task selection (below)
- **"Show all items"**: Display full TODO.md and PLAN.md and ask again

**Step 5: Check for Active MBI**

Before proposing a task from the backlog, check for PLAN.md:

1. **Read PLAN.md** (if it exists in project root)
2. **Check for Active MBI** (section: `## Active MBI`)
3. **If Active MBI exists:**
   - Active MBI tasks take priority over non-MBI tasks
   - Propose the first incomplete task from the Active MBI
   - Report MBI context to user

**MBI Priority Rule:**

| Priority | Task Source |
|----------|-------------|
| 1 | Active MBI tasks (marked with `[MBI-XXX]` in TODO.md) |
| 2 | Fix issues (critical bugs) |
| 3 | Linear TODO.md backlog |

**Example MBI Context:**

```
Found Active MBI: MBI-001 - Bootstrap & Python API
Status: In Progress

Next task: [MBI-001] Implement bootstrap procedure
Goal: Users can start Yoker without pre-existing Ollama configuration

This task is part of an active MBI and takes priority.
```

**Step 5: Verify Task Completion Status (CRITICAL)**

Before proposing a task from the backlog, verify whether its acceptance criteria are already satisfied by existing code. This prevents proposing already-implemented work.

**Verification checklist:**
- Does the task require creating a file that already exists?
- Are the task's acceptance criteria already met by current code?
- Are there related "done" tasks that cover this functionality?

If the task appears already implemented:
- Mark it as done in TODO.md with today's date
- Move to the next task
- Report to the user: "Task {task-id} appears already implemented. Marked as done. Next task: {next-task-id}"

**Step 6: Propose Next Task**

**Use AskUserQuestion tool to propose next task:**

```
Question: "Project analysis complete. Next task from backlog: {task-id} - {task-title}. Proceed with this task?"

Options:
- "Yes, start implementation" (Recommended)
- "Show all tasks in backlog"
- "Run fresh analysis"
```

If user approves, classify task scope (see table above) and proceed to **Phase 2**.

---

### Phase 2: Cross-Domain Review

Invoke domain agents **based on task scope classification**.

#### Parallel Invocation

Domain agents run in **parallel** where independent:
- `api-architect` + `security-engineer` (both review architecture aspects)
- `ui-ux-designer` (independent from backend reviews)

#### Agent Invocation by Scope

**For Backend only:**
```
Invoke api-architect: Review API design, create analysis document
Invoke security-engineer: Review security architecture (if security-related)
```

**For Frontend only:**
```
Invoke ui-ux-designer: Review UX design, create analysis document
```

**For Full stack:**
```
Invoke api-architect: Review API design, create analysis document
Invoke ui-ux-designer: Review UX design, create analysis document
Invoke security-engineer: Review security architecture (if security-related)
```

#### Each Domain Agent:

2. **Invoke api-architect agent** (if Backend or Full stack):
   - Review the most recent functional analysis
   - Review the current backlog (TODO.md)
   - Provide API design perspective and improvements
   - **Create analysis document in `analysis/` folder** (mandatory)
   - Update TODO.md with API-related considerations

3. **Invoke ui-ux-designer agent** (if Frontend or Full stack):
   - Review the most recent functional analysis
   - Review the current backlog (TODO.md)
   - Provide UX/UI perspective and improvements
   - Update TODO.md with UI/UX-related considerations

4. **Invoke security-engineer agent** (if security-related):
   - Review the most recent functional analysis
   - Review the current backlog (TODO.md)
   - Provide security architecture perspective
   - Create analysis document in `analysis/` folder
   - Update TODO.md with security considerations

---

### Phase 3: Consensus and Backlog Finalization

5. **Facilitate agent agreement among all invoked domain agents**:
   - Collect feedback from all domain agents invoked in Phase 2
   - Coordinate resolution if agents disagree
   - Create a consensus summary report in `reporting/{task-name}/consensus.md`
   - Only proceed to implementation when all invoked agents approve

**Note:** Not all tasks require all agents. Consensus is among agents that were invoked.

---

### Phase 4: Task Implementation Loop

For each task in the backlog (in order), execute the following steps:

#### Step 5: Create PR and Present Plan

**CRITICAL: All decisions are handled through PR comments, not AskUserQuestion.**

**All git/gh operations are delegated to release-manager.**

**Step 5a: Create Feature Branch**

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Check current branch. If on main/master, create and checkout feature branch: feature/{issue-number}-{short-description}",
  description: "Create feature branch"
})
```

**Step 5b: Commit Analysis Documents**

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Stage and commit analysis documents in analysis/ and reporting/ with message: 'docs: add analysis for {task-name}'",
  description: "Commit analysis docs"
})
```

**Step 5c: Create PR (Draft)**

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Create draft PR with title 'feat: {task title}' and body describing the analysis. Include links to analysis documents.",
  description: "Create draft PR"
})
```

**Step 5d: Post Implementation Plan as PR Comment**

Delegate to release-manager to post the implementation plan:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Post PR comment with implementation plan for {task-name}. Include: approach, files to modify, implementation steps, acceptance criteria. End with 'Waiting for owner approval before proceeding.'",
  description: "Post plan as PR comment"
})
```

**Step 5e: Wait for Owner Approval (BLOCKING)**

⚠️ **CRITICAL: Implementation cannot proceed until the repository owner approves the plan.**

This is a **mandatory blocking step**, not optional. The workflow must pause until owner approval is received in the PR comments.

Delegate to release-manager to monitor PR comments:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Check PR #{number} for owner feedback. Report any comments or approval.",
  description: "Check PR feedback"
})
```

**Report to owner:**
```
Implementation plan posted as PR comment. Waiting for your approval before proceeding with implementation.

PR: {PR URL}

Please review and either:
- Approve: Comment "approved" or "looks good, proceed"
- Request changes: Comment with specific feedback

Implementation is blocked until you approve.
```

**Do NOT ask "Would you like to proceed?" — this is not optional.**

**Wait for owner response in PR comments:**
- **If owner requests changes:**
  - Delegate to functional-analyst to incorporate feedback
  - Delegate to release-manager to commit updates
  - Delegate to release-manager to post revised plan as PR comment
  - Wait again for approval (this is blocking)
- **If owner rejects entirely:**
  - Close PR
  - Close related issue (if applicable)
  - Report to owner
- **If owner approves:**
  - Proceed to Step 6

**Only proceed to Step 6 after explicit owner approval in PR comments.**

#### Step 6: Check Domain Skills

**CRITICAL**: Before exploring code or running one-off scripts, check if a domain-specific skill exists:

| Skill | When to Use |
|-------|-------------|
| `textual` | Textual TUI framework widgets and patterns |
| `rich` | Rich console output |
| `pymongo` | MongoDB database operations |
| `fire` | Fire CLI framework |
| `baseweb` / `vuetify` | Web UI frameworks |
| `python` | Python coding standards (always relevant) |

If a skill exists for the framework/domain, **invoke it first** to get API knowledge and patterns. This saves significant exploration time.

#### Step 7: Implementation

Invoke the `python-developer` agent (or appropriate specialized agent) to:
- Implement the task following the plan
- Follow general agent instructions in `AGENTS.md` and `CLAUDE.md`
- Follow domain skills (python, baseweb, fire, pymongo, etc.)
- **Run tests and verify all pass before completing**
- Provide the developer with task details from TODO.md and relevant analysis documents

**CRITICAL: Incremental Changes When Fixing Issues**

When fixing issues or making changes:
1. **Make ONE change at a time** — Don't batch multiple fixes
2. **Test after each change** — Verify each fix works before proceeding
3. **Restore if broken** — If a change breaks working code, restore to working state first
4. **Ask before guessing** — If unsure about the root cause, ask for clarification

**Anti-Patterns to Avoid:**
- Making multiple changes simultaneously
- Guessing at fixes without understanding root cause
- Continuing to add changes when already broken
- Skipping tests between changes

#### Step 8: Implementation Review Cycle

⚠️ **This step is MANDATORY and cannot be skipped.**

See `references/review-cycle.md` for detailed review sequence.

**Step 8a: Functional Review (Blocking)**
- Invoke functional-analyst to review functional correctness
- Must pass before proceeding to domain reviews
- If rejected: return to Step 7 with feedback

**Step 8b: Domain Reviews (Parallel, based on scope)**

Invoke domain agents that were invoked in Phase 2:
- `api-architect`: API design compliance (if Backend or Full stack)
- `ui-ux-designer`: UX compliance (if Frontend or Full stack)
- `security-engineer`: Security review (if security-related)

**Step 8c: Quality Reviews (Parallel)**
- `code-reviewer`: Code quality and patterns
- `testing-engineer`: Test coverage and quality

**Step 8d: Documentation (If User-Facing)**

For tasks with user-facing changes:
- Invoke `end-user-documenter` to create/update documentation
- Documentation must be synced with implementation

**Step 8e: Handle Rejections**
- Collect all rejection feedback
- Return to Step 7 with consolidated feedback (max 2 rounds)
- Only proceed to Step 9 when ALL invoked agents approve

#### Step 9: Task Completion (Pending PR Review)

- Mark the task as **pending review** (not complete until PR is merged)
- Update task in TODO.md with PR reference
- Ensure `reporting/` folder exists
- Create summary report in `reporting/{task-name}/summary.md` including:
  - What was implemented
  - Key decisions made
  - Lessons learned
  - Files modified
  - **PR link** (once created)

#### Step 10: Create Pull Request

**CRITICAL:** In project management mode, commits NEVER go directly to master/main.

**All git/gh operations are delegated to release-manager.**

**Step 10a: Ensure Feature Branch**

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Check current branch. If on main/master, create and checkout feature branch: feature/{issue-number}-{short-description}",
  description: "Ensure feature branch"
})
```

**Step 10b: Commit to Feature Branch**

Invoke `release-manager` agent to commit changes:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Commit all staged changes with message: 'feat: {description}'",
  description: "Commit changes"
})
```

Or invoke `c3:commit` skill through release-manager.

**Step 10c: Push Branch and Create PR**

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Push branch to origin and create PR with title 'feat: {task title}' and body describing changes. Include task reference #{task-id} and issue #{issue-number}.",
  description: "Push and create PR"
})
```

**Step 10d: Update GitHub Issue**

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Add label 'status:in-progress' to issue #{issue-number} and add comment 'PR created: {PR URL}'",
  description: "Update issue status"
})
```

**Step 10e: Report to User**

After PR creation:
- Display PR URL (from release-manager response)
- Explain that user acceptance testing happens on the PR
- Task will be marked complete after PR is merged

**Step 10f: CI Follow-up (MANDATORY)**

⚠️ **PR creation is NOT complete until CI passes.**

Delegate to release-manager to check CI:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Check CI status for PR #{number}. Report if passing or failing. If failing, provide failure details.",
  description: "Check CI status"
})
```

**If CI fails:**
1. Delegate to developer to fix the issue
2. Delegate to release-manager to commit and push fixes
3. Repeat until CI passes

**Step 10g: Mark PR Ready for Review**

⚠️ **CRITICAL: PR must be marked ready before owner can merge.**

After CI passes, the PR is still in draft state. Mark it ready for review:

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Mark PR #{number} as ready for review (convert from draft).",
  description: "Mark PR ready"
})
```

**Step 10h: Assign and Request Review**

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Assign PR #{number} to {owner} and request review from {owner}. Post comment: 'Implementation complete. Ready for review.'",
  description: "Assign and request review"
})
```

**Step 10i: Pause and Report**

⚠️ **CRITICAL: Do NOT check for feedback immediately. The workflow pauses here.**

Report to owner:
```
PR #{number} is ready for review.

URL: {PR URL}

Status:
- Implementation: Complete
- CI: Passing
- Review: Requested from {owner}

The PR is ready for your review. Say "follow up on PR #{number}" to check for feedback.
```

**Do NOT:**
- Check for PR feedback immediately
- Wait for owner response
- Block on feedback

**The workflow ends here for this issue.** Move to the next issue/PR or pause if all processed.

---

### Processing Multiple Issues/PRs

After processing an issue or PR:

1. **Check if there are more issues/PRs to process:**
   - New issues without status labels
   - Issues with `status:in-progress` (waiting for follow-up)
   - PRs awaiting owner feedback

2. **If more items exist:**
   - Move to the next issue/PR
   - Process it (post comment, update status, etc.)
   - Do NOT check for feedback on previous items

3. **If all items processed:**
   - Report summary: "Processed X issues/PRs. Y items waiting for feedback."
   - Pause the workflow
   - User can say "follow up" to check all waiting items

**When user says "follow up":**
- Start from Phase 0A (list issues)
- Issues with new comments will be picked up
- Continue processing

#### Step 11: Exit Plan Mode (When User Requests)

When user says "follow up on PR #{number}" or the workflow restarts:

1. **Check for new comments on PR:**
   ```
   Agent({
     subagent_type: "c3:release-manager",
     prompt: "Get all comments for PR #{number}. Report any new feedback from owner.",
     description: "Check PR feedback"
   })
   ```

2. **Process each feedback item:**
   - Review each comment from owner
   - Address feedback by delegating to developer
   - Commit and push fixes
   - Post comment explaining changes

3. **If owner approves:**
   - Wait for owner to merge (do NOT merge yourself)
   - After merge, proceed to Step 12 (Post-Merge)

4. **If no new feedback:**
   - Report: "No new feedback on PR #{number}. Waiting for owner review."
   - Pause

#### Step 12: Post-Merge (After User Merges PR)

**⚠️ CRITICAL: Execute steps in SEQUENCE to prevent data loss.**

**Why sequencing matters:** After the PR is merged, we're typically still on the feature branch. TODO.md updates must be made on master AFTER switching, otherwise they stay on the feature branch and may be lost when the branch is deleted.

When user reports PR is merged:

1. **Find the issue number:**
   - Check TODO.md task entry (includes issue reference)
   - Or ask release-manager to find it from PR

2. **Sync to main branch FIRST (before any TODO.md updates):**

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Switch to main branch and pull latest",
  description: "Sync to main"
})
```

**IMPORTANT:** This must happen before TODO.md updates. Otherwise changes are made on the feature branch and lost when it's deleted.

3. **Update TODO.md on master (AFTER switching branches):**

   **Step 3a: Delegate TODO.md update to functional-analyst:**
   ```
   Agent({
     subagent_type: "c3:functional-analyst",
     prompt: "Update TODO.md to mark task {task-id} as complete after PR merge. Add completion date (YYYY-MM-DD), move to Done section.",
     description: "Update TODO.md"
   })
   ```
   The functional-analyst owns the TODO.md lifecycle.

   **Step 3b: Commit TODO.md changes:**

   Delegate to release-manager:
   ```
   Agent({
     subagent_type: "c3:release-manager",
     prompt: "Commit TODO.md changes with message: 'docs: mark task {task-id} as complete'",
     description: "Commit TODO.md"
   })
   ```

4. **Handle untracked artifacts:**
   - Check for analysis/ and reporting/ files from merged work
   - These should already be committed to the PR
   - Verify they exist in the merged branch

5. **Clean up GitHub issue labels:**

Delegate to release-manager:
```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Remove 'status:in-progress' label from issue #{issue-number}. If issue is not auto-closed, close it.",
  description: "Clean up issue"
})
```

6. **Ask owner: prepare release or continue with next task?**
   - Use PR comment or direct question (owner is present)
   - If release: Delegate to release-manager to execute release workflow
   - If continue: Proceed with next task from TODO.md

7. Continue to next task from Step 5

---

## Review Cycle Execution Order

```
Step 1: functional-analyst     ← BLOCKING (must pass first)
    │
    ▼
Step 2: Domain Reviews         ← PARALLEL (independent perspectives)
    ├── api-architect
    ├── ui-ux-designer
    └── security-engineer
    │
    ▼
Step 3: Quality Reviews        ← PARALLEL (independent perspectives)
    ├── code-reviewer
    └── testing-engineer
    │
    ▼
Step 4: Documentation          ← IF user-facing
    └── end-user-documenter
```

---

## Agent Invocation

When invoking specialized agents, use clear prompts that specify:
- The current phase of the workflow
- What documents to review (AGENTS.md, CLAUDE.md, README.md, analysis/, TODO.md)
- What deliverables are expected
- Any specific concerns or focus areas

---

## When to Use Bug-Fixing Workflow

Use the Bug Fixing Workflow when:
- User explicitly says "fix bug", "there's a bug", "debug this"
- Task description contains bug indicators (error, crash, broken, fails)
- Issue reference is provided (e.g., "#123", "JIRA-456")
- Current behavior doesn't match expected behavior

Use the Feature Development Workflow when:
- User says "add", "create", "implement", "build new"
- Task is about new functionality
- Requirements describe desired features

---

## Communication with User

- Provide clear status updates at each phase transition
- Report any blockers or issues that require user input
- Summarize agent findings and decisions
- When project is ready for work, propose next task from backlog

### Using AskUserQuestion Tool

**CRITICAL**: When asking the user for input and there are **limited possible answers (<7)**, use the AskUserQuestion tool instead of plain text prompts.

This applies to situations like:
- **Task approval**: "Proceed with this task?" (yes/no)
- **Workflow selection**: "Which workflow to use?" (bug/feature)
- **Priority decisions**: "Which task to prioritize?" (list of tasks)
- **Conflict resolution**: "How to resolve this issue?" (finite options)
- **Branch selection**: "Which branch?" (list of branches)

---

## File Conventions

| File | Path |
|------|------|
| Functional analysis | `analysis/functional.md` |
| API analysis | `analysis/api-{topic}.md` |
| UX analysis | `analysis/ux-{topic}.md` |
| Security analysis | `analysis/security-{topic}.md` |
| Bug analysis | `analysis/bug/{bug-id}.md` |
| Consensus summary | `analysis/reporting/{task-name}/consensus.md` |
| Plan | `analysis/reporting/{task-name}/plan.md` |
| Implementation review report | `analysis/reporting/{task-name}/{topic}-review.md` |
| Task summary | `analysis/reporting/{task-name}/summary.md` |
| Research findings | `research/{topic}.md` |
| Technology recommendations | `research/{topic}/recommendations.md` |

**Note:** All analysis documents go in `analysis/` folder with sub-folders for organization.

### TODO.md Structure

```markdown
# TODO

## Unsorted

- [ ] Quick idea 1 (captured but not yet analyzed)
- [ ] Quick idea 2 (needs functional analysis)

## Backlog (Prioritized)

### P1 - Critical

- [ ] Critical task with clear acceptance criteria

### P2 - High

- [ ] High priority task

### P3 - Medium

- [ ] Medium priority task

### P4 - Low

- [ ] Low priority task

## Done

- [x] Completed task
```

**Unsorted Section Rules:**
- Placed at the top of TODO.md
- Contains items that need functional analysis before prioritization
- Items are short ideas without acceptance criteria
- When analyzed, functional-analyst moves them to appropriate priority in Backlog
- Optional section — only present when user has captured unsorted ideas

---

## Notes

- The functional-analyst owns the TODO.md structure
- Domain agents (api-architect, ui-ux-designer, security-engineer) contribute to TODO.md through the functional-analyst
- Resolve conflicts between domain recommendations based on project priorities
- Ensure all tasks have verifiable acceptance criteria before implementation
- **For bugs**: Spawn `c3:bug-fixer` agent for complete TDD workflow (keeps context clean)
- **For features**: Follow the feature development phases with domain design reviews
- **Research** is conditional - invoke when gaps identified or technology choices needed
- **Security review** is scoped to security-related tasks
- **Documentation** is part of task completion for user-facing changes
- **Parallel reviews** improve efficiency without sacrificing quality
- **User can request reanalysis**: Use "reanalyze" option when proposing next task to run fresh analysis
- **Unsorted items**: Quick ideas captured at top of TODO.md that need analysis before prioritization. Offer to sort them before working on backlog, but allow user to skip and proceed with prioritized tasks.
- **PR Ownership**: The agent creates PRs and processes feedback, but ONLY the owner merges PRs. Never propose merging.
- **TODO.md Direction is Authoritative**: When TODO.md specifies an implementation approach (e.g., "Use `prompt_async()` for async input"), follow it without asking for confirmation. TODO.md represents the project's decided direction. Only ask for clarification when genuinely ambiguous or conflicting requirements exist.

---

## Agent Quick Reference

| Agent | Phase | When to Invoke |
|-------|-------|----------------|
| functional-analyst | 1A, 1B, 4 (review) | Always |
| researcher | 1A, 1B | When gaps or tech choices |
| api-architect | 2, 4 (review) | Backend or Full stack tasks |
| ui-ux-designer | 2, 4 (review) | Frontend or Full stack tasks |
| security-engineer | 2, 4 (review) | Security-related tasks |
| python-developer | 4 (implementation) | Always for Python projects |
| code-reviewer | 4 (review) | Always |
| testing-engineer | 4 (review) | Always |
| end-user-documenter | 4 (completion) | User-facing changes |

---

## Publishing Releases

When the user requests publishing to PyPI or preparing a release:

**Delegate to release-manager:**

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Execute release workflow: determine version bump, update files, run checks, build, and publish to PyPI",
  description: "Execute release"
})
```

The release-manager will invoke the `c3:release` skill which handles:
- Version bump decision
- Updating version files (pyproject.toml, __init__.py)
- Updating changelog
- Running pre-publish checks
- Building and verifying package
- Creating tag and GitHub release
- Uploading to PyPI

Key checks (handled by release-manager):
- README image paths must use absolute GitHub URLs (not relative paths)
- Version must be synced between `pyproject.toml` and `__init__.py`
- Local development configuration (`[tool.uv.sources]`, `[tool.uv.workspace]`) must be removed
- Entry points must be verified
- Package contents must be verified after build

---

## Reference Files

- `references/bug-workflow-integration.md` — How bug workflow integrates with project management
- `references/review-cycle.md` — Detailed review cycle execution