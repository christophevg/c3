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
- All file paths are relative to that output: TODO.md, PLAN.md, analysis/, reporting/

---

## Role of this skill

`project-manage` is a **coordinator**. It never touches Bash, git, or `gh`
directly — all source-control and GitHub operations are delegated to
`c3:release-manager` (the controlled Bash funnel). It detects what kind of work
this is, routes it to the right sub-workflow, and drives a feature through
analysis → design → consensus → implementation → review → PR.

It owns Phases 0–5. Three phases are delegated to dedicated sub-skills:

| Phase | Sub-skill | Trigger |
|-------|-----------|---------|
| 6 — PR iteration | `c3:project-handle-pr` | "follow up on PR #N" or open PR with feedback |
| 7 — Post-merge | `c3:project-post-merge` | Owner reports a PR was merged |
| Review cycle (5.6, 6.4) | `c3:project-review` | Invoked during implementation and PR iteration |

A hard rule runs through the whole skill: **the repository owner is the only
human decision-maker.** The agent proposes; the owner approves via PR comments
(not AskUserQuestion); only the owner merges.

## ⚠️ Simplicity Principle — Owner's Proposal is the Default

**Slim, tight, concise is the default.** Avoid indirections, wrappers, and
redundant work. Less is the default unless there is no other way.

When the owner provides an explicit proposal or snippet, OR states a worry / constraint / directive (in the issue, PR comments, or interview):
1. **It is the default.** Implement/endorse it as-is unless there is a
   specific, documented problem.
2. **Any deviation must** (i) quote the owner's proposal, (ii) state the
   specific problem with it, (iii) justify why the added complexity is earned.
3. **"Reviewer prefers X" or "refinement" is NOT justification.**
4. **Ignoring the owner's proposal without a stated reason is unacceptable.**
5. **Owner-stated worries and constraints are binding.** The implementation plan (Phase 5.2) MUST enumerate every owner-stated proposal, worry, and constraint (from the issue, PR comments, or interview) and explicitly respond to each — quote it, state whether the plan satisfies it. An owner instruction left as background context (no explicit response in the plan) blocks plan approval.

**PM Simplicity Gate (applies at Phase 3, 4, 5.2, 5.6):** before forwarding any
reviewer recommendation that diverges from the owner's explicit proposal, the
project-manager must (a) quote the owner's proposal, (b) state the specific
problem with it, (c) only forward if the problem is real and the added
complexity is earned. Do NOT rubber-stamp reviewer recommendations that add
classes/indirections/wrappers/guards not in the owner's proposal without
earned justification.

---

## Workflow Overview

```
═══════════════════════════════════════════════════════════════════════
PHASE 0 — Session Start & Triage
═══════════════════════════════════════════════════════════════════════
 0.1  release-manager → project state report (project root = its wd)
 0.2  branch on state:
        open PR w/ feedback    → delegate to c3:project-handle-pr
        open PR waiting        → report & wait
        merged feature branch  → delegate to c3:project-post-merge
        open issues            → 0.3 issue triage
        clean main/master      → Phase 1
 0.3  issue triage (by type/label — all gh ops via release-manager):
        bug        → Bug Implementation Flow (bug-fixer → project-review → PR)
        feature    → functional-analyst review → owner approves → backlog
        question   → researcher
        dependency → researcher → backlog
        reject     → close

═══════════════════════════════════════════════════════════════════════
PHASE 1 — Analysis (conditional)
═══════════════════════════════════════════════════════════════════════
 1A  no analysis/functional.md → functional-analyst: interview,
     create analysis/functional.md + TODO.md + (optional) PLAN.md (MBIs)
 1B  analysis exists, no TODO  → functional-analyst: review,
     create prioritized TODO.md (+ PLAN.md MBIs if needed)
     (researcher conditional: gaps / tech choices; see c3:plan for MBIs)

═══════════════════════════════════════════════════════════════════════
PHASE 2 — Task Selection
═══════════════════════════════════════════════════════════════════════
 2.1  unsorted items (TODO.md ## Unsorted) & unsorted MBIs
      (PLAN.md ## Unsorted MBIs) → ask: sort / analyze / skip
 2.2  PRIORITY (first-class):
        1. Active MBI tasks   (PLAN.md ## Active MBI, tagged [MBI-XXX])
        2. Fix issues          (critical bugs)
        3. Linear TODO.md backlog
 2.3  verify task not already implemented (acceptance-criteria check)
 2.4  propose next task (AskUserQuestion) → approved → 2.5
 2.5  task scope classification:
        backend | frontend | full | docs | research
        (+ security-engineer if auth / PII / external API / input / files / config)

═══════════════════════════════════════════════════════════════════════
PHASE 3 — Cross-Domain Design Review (parallel, by scope)
═══════════════════════════════════════════════════════════════════════
 3.1  api-architect + security-engineer   (backend / full)
 3.2  ui-ux-designer                       (frontend / full)
      each writes analysis/*.md; TODO.md updates flow via functional-analyst

═══════════════════════════════════════════════════════════════════════
PHASE 4 — Consensus
═══════════════════════════════════════════════════════════════════════
 4.1  reporting/{task}/consensus.md — all invoked domain agents approve

═══════════════════════════════════════════════════════════════════════
PHASE 5 — Implementation
═══════════════════════════════════════════════════════════════════════
 5.1  release-manager: feature branch + commit analysis docs + draft PR
 5.2  post implementation plan as PR comment
 5.3  ◆ PLAN APPROVAL GATE (BLOCKING — owner in PR comments)
 5.4  check domain skills first (textual / pymongo / baseweb / python …)
 5.5  python-developer implements (incremental: one change → test → verify)
 5.6  ★ invoke c3:project-review skill
 5.7  mark pending-review + write reporting/{task}/summary.md
 5.8  release-manager: commit → push → PR → CI (fix until green)
 5.9  release-manager: mark ready → assign / request owner review
 5.10 PAUSE (do not poll for feedback)

 → "follow up on PR #N" → delegate to c3:project-handle-pr
 → "PR merged"          → delegate to c3:project-post-merge
```

The review cycle detail (Stage a–f, the `make check` gate, rejection handling)
lives in the `c3:project-review` skill, invoked at 5.6 and again (scoped) at
Phase 6.4 of `c3:project-handle-pr`.

---

## Session Start: Get Project State

**CRITICAL: Project-manager does NOT run git/gh commands directly. Always delegate to release-manager.**

```
Agent({
  subagent_type: "c3:release-manager",
  prompt: "Report project state",
  description: "Get project state"
})
```

Based on the state reported, determine the next action (Phase 0.2):

| State | Action |
|-------|--------|
| Open PR with pending feedback | Delegate to `c3:project-handle-pr` |
| Open PR waiting for owner | Report status, wait for owner |
| Merged PR on feature branch | Delegate to `c3:project-post-merge` |
| Clean main/master | Start new task from TODO.md (Phase 1) |
| Open issues | Process issues (Phase 0.3) |

### PR Status Handling

The release-manager's report includes PR status. Based on that:

| PR Status | Action |
|-----------|--------|
| CI failing | Delegate to developer to fix |
| CI passing, review pending | Wait for owner |
| Changes requested | Delegate to `c3:project-handle-pr` |
| Approved | Wait for owner to merge |

**Do NOT run `gh pr checks` or `gh pr view` directly — get this from release-manager.**

---

## Task Type Detection

Before starting, detect whether the task is a **feature**, **bug**, or **dependency**:

| Task Type | Indicators |
|-----------|------------|
| **Bug** | "fix", "bug", "issue", "broken", "error", "doesn't work", "crash", "fails" |
| **Feature** | "add", "create", "implement", "build", "new", "feature", "enhance" |
| **Dependency** | "upgrade", "update", "bump", "dependencies", "package", "release", "version" |

### If the task is a BUG

Follow the **Bug Implementation Flow** below — bugs go through the same review
(`c3:project-review`) and PR funnel (`c3:release-manager`) as features, but skip
the Plan Approval Gate (bugs are urgent and owner-decided). See
[references/bug-workflow-integration.md](references/bug-workflow-integration.md).

#### Bug Implementation Flow

```
1. Mark in-progress + create feature branch   (release-manager)
2. Spawn c3:bug-fixer                          (diagnose + TDD + fix + make check → reports back)
3. Invoke c3:project-review (scoped to bug)    ← review re-entry, same as features
4. Commit, push, PR, CI                        (release-manager)
5. Mark ready, request owner review            (release-manager)
6. PAUSE                                       (do not poll)
   → "PR merged" → c3:project-post-merge
```

**Step 1 — Mark in-progress + create branch** (release-manager):

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Add label 'status:in-progress' to issue #{number}. If on main/master, create and checkout feature branch: feature/{issue-number}-{short-description}.",
  description: "Mark bug in progress + branch" })
```

**Step 2 — Spawn bug-fixer** (diagnose + TDD + fix + `make check`; reports back,
does NOT create a PR or run review):

```python
Agent({ subagent_type: "c3:bug-fixer",
  prompt: "Fix {issue-number}: {issue-title}\n\n{issue-body}",
  description: "Fix bug {issue-number}" })
```

**Step 3 — Review the fix** (invoke the shared review skill, scoped to the bug,
using the scope/files from bug-fixer's report):

```
Skill({ skill: "c3:project-review",
  args: "bug fix, issue #{number}, scope {scope}, round 0, files: {from report}" })
```

| `c3:project-review` returns | Action |
|------------------------------|--------|
| `approved` | Proceed to Step 4 |
| `rejected: <feedback>` | Re-spawn bug-fixer (Step 2) with the feedback to revise; increment round; re-run Step 3 |
| `escalate` | Ask owner: proceed with known issues / reduce scope / alternative? |

**Step 4 — Commit, push, PR, CI** (release-manager, same as Phase 5.8):

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Commit the fix with message: 'fix: {summary} (#{issue-number})'. Push and create PR titled 'fix: {title}' referencing issue #{number}.",
  description: "Commit, push, create PR" })
Agent({ subagent_type: "c3:release-manager",
  prompt: "Check CI status for PR #{number}. If failing, report details.",
  description: "Check CI" })
```

If CI fails, re-spawn bug-fixer to fix, then release-manager commits/pushes again.

**Step 5 — Mark ready, request owner review** (release-manager, same as Phase 5.9).

**Step 6 — Pause** (same as Phase 5.10). On "PR merged" → delegate to
`c3:project-post-merge`.

### If the task is a DEPENDENCY

Determine complexity, then route:

| Complexity | Example | Workflow |
|------------|---------|----------|
| Simple upgrade | "Upgrade yoker to 2.1.0" | Researcher → python-developer |
| Upgrade with goal | "Upgrade yoker to simplify our codebase" | Researcher → functional-analyst |

```python
# Step 1: researcher gathers package information (uses pkgq for Python packages)
Agent({
  subagent_type: "c3:researcher",
  prompt: "Research Python packages: {packages}. Include: capabilities, patterns, breaking changes, migration steps.",
  description: "Research {packages}"
})

# Step 2: route based on complexity
#   simple upgrade  → c3:python-developer (apply migration)
#   upgrade w/ goal → c3:functional-analyst (analyze simplification, create TODO.md)
```

### If the task is a FEATURE

Use the **Feature Development Workflow** — continue to Phase 0.3 / Phase 1.

---

## Phase 0.3 — Issue Triage

⛔ **MANDATORY: uses data from release-manager's project state report. Do NOT run gh commands directly.**

Issues are reported by release-manager during session start. Filter out issues
with status labels (already reviewed); issues without status labels are new and
need triage. Classify each new issue:

| Issue Type | Labels / Indicators | Workflow |
|------------|---------------------|----------|
| **Bug** | `bug`, `error`, `crash`, `broken`, `fix` | Bug Implementation Flow (bug-fixer → project-review → PR) |
| **Feature** | `enhancement`, `feature`, `new`, `add` | Review → Clarify → Backlog |
| **Question** | `question`, `help`, `discussion` | Research or close |
| **Dependencies** | `dependencies`, `upgrade` | Research → Backlog |

Detailed triage (owner authority, clarification process, triage completion) is
in [references/issue-review-workflow.md](references/issue-review-workflow.md).

### Bug issues (URGENT — immediate action)

Do NOT ask for confirmation. Follow the **Bug Implementation Flow** (see "If the
task is a BUG" above): mark in-progress + create branch (release-manager) →
spawn `c3:bug-fixer` → `c3:project-review` → commit/push/PR/CI (release-manager)
→ mark ready → pause. Bugs no longer stop at the bug-fixer; they continue
through the same review + PR funnel as features.

### Feature issues (REQUIRE review — clarify first)

⚠️ **Only the repository owner can approve an issue into the backlog.**
Non-owner comments are informational only. Functional-analyst must verify
commenter ownership. Full process in
[references/issue-review-workflow.md](references/issue-review-workflow.md).

1. Mark as being reviewed (release-manager adds `status:in-progress` + comment).
2. Delegate to functional-analyst for review (clarify via `gh issue comment`).
3. After functional-analyst reports **owner** agreement:
   - release-manager: remove `status:in-progress`, add `status:backlog`, comment.
   - functional-analyst: add issue to TODO.md backlog with agreed criteria.
4. Commit and push TODO.md/REQUIREMENTS.md updates immediately via release-manager
   (prevents accumulating uncommitted changes during triage).

### Question / discussion issues

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Add label 'status:needs-research' to issue #{number} and comment 'Needs evaluation for...'",
  description: "Mark for research" })
```

### Rejecting issues

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Add label 'status:wont-do' to issue #{number} and close with comment 'Closing: not in scope because...'",
  description: "Reject issue" })
```

### Issue status labels

| Label | Meaning | Action |
|-------|---------|--------|
| `status:backlog` | Reviewed, accepted, added to TODO.md | Keep open, implement later |
| `status:in-progress` | Currently being reviewed or implemented | Keep open, track progress |
| `status:wont-do` | Decision: won't implement | Close with explanation |
| `status:needs-research` | Needs evaluation | Keep open, research first |
| `status:blocked` | Blocked by dependency | Keep open, note blocker |

### "Follow up on issue #N"

⚠️ **Do NOT decide yourself. Delegate to functional-analyst.** Use `SendMessage`
with the existing functional-analyst agent to preserve context — do not relaunch.

The functional-analyst checks for new comments, verifies ownership, and reports
one of: needs clarification / waiting for owner / fully triaged. After triage is
complete, update labels and TODO.md via release-manager + functional-analyst, then
move to the next issue (do not pause for feedback).

Continue to Phase 1 after issues are handled.

---

## Phase 1 — Analysis (conditional)

Detect the project state from analysis artifacts:

| State | `analysis/functional.md` | `TODO.md` | Action |
|-------|--------------------------|-----------|--------|
| **New Project** | Missing | Missing | Phase 1A |
| **Incomplete Setup** | Exists | Missing | Phase 1B |
| **Ready for Work** | Exists | Exists | Phase 2 |

### Phase 1A — Initial Functional Analysis (new project)

Invoke `functional-analyst` to:

- Review high-level functional requirements (README.md, existing docs)
- Review existing code structure if available
- Interview the user to clarify topics needing more information
- Create `analysis/functional.md` with comprehensive functional analysis
- Create `TODO.md` with a prioritized backlog of atomic, well-defined tasks
- **Optionally create `PLAN.md`** with Minimal Business Increments (MBIs) when
  the work benefits from MBI-level slicing. Use the `c3:plan` skill for MBI
  creation, scoring (WSJF), and structure.

**Conditional: invoke `c3:researcher` when:**
- Functional analysis identifies gaps needing best-practice proposals
- The user explicitly requests research to address functional-analyst questions
- A technology choice needs evaluation and recommendations

Researcher delivers: findings in `research/{topic}.md`, technology
recommendations with pros/cons, best-practice proposals for identified gaps.

### Phase 1B — Review and Backlog Creation (existing analysis)

Invoke `functional-analyst` to:

- Review existing `analysis/functional.md`
- Review current project state
- Interview the user to update understanding if needed
- Create a prioritized `TODO.md`
- **Create/update `PLAN.md`** with MBIs if the work warrants MBI slicing

**Conditional: invoke researcher** when existing analysis needs technology
investigation or the user requests research.

Then proceed to **Task Scope Classification** (Phase 2.5).

---

## Phase 2 — Task Selection

### 2.1 Check for unsorted items and MBIs

- Read `TODO.md` — check for a `## Unsorted` section (quick ideas captured but
  not yet analyzed).
- If `PLAN.md` exists, check for `## Unsorted MBIs` (raw MBI ideas not yet
  analyzed).

| Condition | Action |
|-----------|--------|
| No unsorted items or MBIs | Proceed to 2.2 |
| Unsorted items / MBIs exist | Ask the user (AskUserQuestion): sort / analyze / skip / show all |

Choices:
- **Sort unsorted items first** → functional-analyst integrates them into the backlog
- **Analyze unsorted MBIs** → functional-analyst creates proper MBI entries in PLAN.md
- **Show next backlog task** → proceed to 2.2
- **Show all items** → display TODO.md and PLAN.md, ask again

### 2.2 Priority (MBI is first-class)

| Priority | Task Source |
|----------|-------------|
| 1 | Active MBI tasks (PLAN.md `## Active MBI`, tagged `[MBI-XXX]` in TODO.md) |
| 2 | Fix issues (critical bugs) |
| 3 | Linear TODO.md backlog |

If an Active MBI exists, propose its first incomplete task and report the MBI
context to the user (e.g. "Found Active MBI: MBI-001 — Bootstrap. Next task: …").
Active MBI tasks take priority over non-MBI tasks.

### 2.3 Verify task completion status (CRITICAL)

Before proposing a task, verify whether its acceptance criteria are already
satisfied by existing code — this prevents proposing already-implemented work.

- Does the task require creating a file that already exists?
- Are the acceptance criteria already met by current code?
- Are there related "done" tasks covering this functionality?

If the task appears already implemented: mark it done in TODO.md with today's
date, move to the next task, and report to the user.

### 2.4 Propose next task (AskUserQuestion)

```
Question: "Project analysis complete. Next task from backlog: {task-id} - {task-title}. Proceed with this task?"
Options:
- "Yes, start implementation" (Recommended)
- "Show all tasks in backlog"
- "Run fresh analysis"
```

If approved, proceed to 2.5.

### 2.5 Task scope classification

| Scope | Indicators | Required Domain Agents |
|-------|------------|------------------------|
| **Backend only** | "API", "endpoint", "backend", "data model", no UI | api-architect, security-engineer* |
| **Frontend only** | "UI", "UX", "frontend", "component", "page", no backend | ui-ux-designer |
| **Full stack** | Both backend and frontend mentioned | api-architect, ui-ux-designer, security-engineer* |
| **Documentation only** | "document", "readme", "guide" | end-user-documenter |
| **Research only** | "research", "investigate", "evaluate" | researcher |

\* Include `security-engineer` when the task involves: authentication or
authorization changes, sensitive data (PII, credentials, payments), external API
integrations, user input processing, file operations, or security-affecting
configuration changes.

Then proceed to Phase 3.

---

## Phase 3 — Cross-Domain Design Review

Invoke domain agents based on scope. Run them **in parallel** where independent.

**Backend / Full stack:** `api-architect` (+ `security-engineer` if security-related)
**Frontend / Full stack:** `ui-ux-designer`

Each domain agent:
- Reviews the most recent functional analysis and the current backlog (TODO.md)
- Provides its perspective and improvements
- **Creates an analysis document in `analysis/`** (mandatory for api-architect
  and security-engineer)
- Updates TODO.md with domain considerations (flowing through functional-analyst)

---

## Phase 4 — Consensus and Backlog Finalization

- Collect feedback from all domain agents invoked in Phase 3
- Coordinate resolution if agents disagree
- Create a consensus summary in `reporting/{task-name}/consensus.md`
- **Only proceed to implementation when all invoked agents approve**

Not all tasks require all agents — consensus is among the agents that were
invoked.

---

## Phase 5 — Implementation

### 5.1 Create feature branch + commit analysis docs + draft PR

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Check current branch. If on main/master, create and checkout feature branch: feature/{issue-number}-{short-description}",
  description: "Create feature branch" })
Agent({ subagent_type: "c3:release-manager",
  prompt: "Stage and commit analysis documents in analysis/ and reporting/ with message: 'docs: add analysis for {task-name}'",
  description: "Commit analysis docs" })
Agent({ subagent_type: "c3:release-manager",
  prompt: "Create draft PR with title 'feat: {task title}' and body describing the analysis. Include links to analysis documents.",
  description: "Create draft PR" })
```

### 5.2 Post implementation plan as PR comment

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Post PR comment with implementation plan for {task-name}. Include: approach, files to modify, implementation steps, acceptance criteria. End with 'Waiting for owner approval before proceeding.'",
  description: "Post plan as PR comment" })
```

### 5.3 ◆ Plan Approval Gate (BLOCKING)

⚠️ **Implementation cannot proceed until the repository owner approves the plan
in PR comments. This is mandatory and blocking — not optional, not an
AskUserQuestion.**

Delegate to release-manager to monitor PR comments:

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Check PR #{number} for owner feedback. Report any comments or approval.",
  description: "Check PR feedback" })
```

Report to the owner:
```
Implementation plan posted as PR comment. Waiting for your approval before proceeding.
PR: {PR URL}
Please review and either:
- Approve: comment "approved" or "looks good, proceed"
- Request changes: comment with specific feedback
Implementation is blocked until you approve.
```

| Owner response | Action |
|----------------|--------|
| Requests changes | functional-analyst incorporates → release-manager commits → re-post plan → wait again |
| Rejects entirely | Close PR (+ related issue if applicable) → report to owner |
| Approves | Proceed to 5.4 |

**Only proceed to 5.4 after explicit owner approval in PR comments.**

### 5.4 Check domain skills

Before exploring code or running one-off scripts, check for a domain skill:

| Skill | When to use |
|-------|-------------|
| `textual` | Textual TUI widgets and patterns |
| `rich` | Rich console output |
| `pymongo` | MongoDB operations |
| `fire` | Fire CLI framework |
| `baseweb` / `vuetify` | Web UI frameworks |
| `python` | Python coding standards (always relevant) |

Invoke the matching skill first to get API knowledge and patterns — saves
exploration time.

### 5.5 Implement

Invoke `c3:python-developer` (or appropriate specialized agent) to:
- Implement the task following the plan
- Follow `AGENTS.md` and `CLAUDE.md`
- Follow domain skills (python, baseweb, fire, pymongo, etc.)
- Run `make check` and verify all pass before reporting done
- Receive task details from TODO.md and relevant analysis documents

**Incremental changes when fixing issues:**
1. Make ONE change at a time — don't batch multiple fixes
2. Test after each change — verify each fix works
3. Restore if broken — if a change breaks working code, restore first
4. Ask before guessing — if unsure about root cause, ask for clarification

**Anti-patterns:** making multiple changes simultaneously; guessing without
understanding root cause; continuing to add changes when already broken; skipping
checks between changes.

### 5.6 Review cycle

⚠️ **MANDATORY. Do not skip.** Invoke the shared review skill:

```
Skill({
  skill: "c3:project-review",
  args: "initial implementation, task {task-id}, scope {scope}, round 0, files: {files}"
})
```

`c3:project-review` runs functional → domain → quality → documentation →
`make check` → pre-commit verification, with rejection handling (max 2 rounds,
then escalate). Handle its return value:

| `c3:project-review` returns | Action |
|------------------------------|--------|
| `approved` | Proceed to 5.7 |
| `rejected: <feedback>` | Send developer back to 5.5 with consolidated feedback; increment round; re-run 5.6 |
| `escalate` | Ask owner: proceed with known issues / reduce scope / alternative approach? |

### 5.7 Mark pending-review + summary

- Mark the task **pending review** (not complete until PR is merged)
- Update the task in TODO.md with the PR reference
- Ensure `reporting/{task-name}/` exists
- Create `reporting/{task-name}/summary.md`: what was implemented, key decisions,
  lessons learned, files modified, PR link

### 5.8 Commit, push, create PR, CI

⚠️ **In project management mode, commits NEVER go directly to master/main.**

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Check current branch. If on main/master, create and checkout feature branch: feature/{issue-number}-{short-description}",
  description: "Ensure feature branch" })
Agent({ subagent_type: "c3:release-manager",
  prompt: "Commit all staged changes with message: 'feat: {description}'",
  description: "Commit changes" })
Agent({ subagent_type: "c3:release-manager",
  prompt: "Push branch to origin and create PR with title 'feat: {task title}' and body describing changes. Include task reference #{task-id} and issue #{issue-number}.",
  description: "Push and create PR" })
Agent({ subagent_type: "c3:release-manager",
  prompt: "Add label 'status:in-progress' to issue #{issue-number} and add comment 'PR created: {PR URL}'",
  description: "Update issue status" })
```

**CI follow-up (MANDATORY):** PR creation is NOT complete until CI passes.

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Check CI status for PR #{number}. Report if passing or failing. If failing, provide failure details.",
  description: "Check CI status" })
```

If CI fails: delegate to developer to fix → release-manager commits and pushes →
repeat until CI passes.

### 5.9 Mark PR ready, assign, request review

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Mark PR #{number} as ready for review (convert from draft).",
  description: "Mark PR ready" })
Agent({ subagent_type: "c3:release-manager",
  prompt: "Assign PR #{number} to {owner} and request review from {owner}. Post comment: 'Implementation complete. Ready for review.'",
  description: "Assign and request review" })
```

### 5.10 Pause and report

⚠️ **Do NOT check for feedback immediately. The workflow pauses here.**

Report to the owner:
```
PR #{number} is ready for review.
URL: {PR URL}
Status:
- Implementation: Complete
- CI: Passing
- Review: Requested from {owner}
The PR is ready for your review. Say "follow up on PR #{number}" to check for feedback.
```

**Do NOT:** check for PR feedback immediately; wait for owner response; block on
feedback.

The workflow ends here for this task. Move to the next issue/PR or pause.

---

## Delegating to sub-skills

After Phase 5.10, control returns to the owner. Two triggers delegate onward:

| Trigger | Delegation |
|---------|------------|
| "follow up on PR #N" / "check PR #N" | `Skill({ skill: "c3:project-handle-pr", args: "PR #N, task {task-id}, scope {scope}" })` |
| Owner reports PR merged | `Skill({ skill: "c3:project-post-merge", args: "PR #N, task {task-id}, issue #{number}" })` |

`c3:project-handle-pr` re-enters the review cycle (scoped) on every feedback
round before push — closing the gap where PR-comment changes previously shipped
without cross-validation. `c3:project-post-merge` runs the sequenced cleanup and
returns control here (Phase 2) for the next task, or delegates to release for a
release.

### Processing multiple issues/PRs

After processing an issue or PR:
1. Check for more items (new issues without status labels; in-progress issues;
   PRs awaiting feedback).
2. If more exist, move to the next and process it — do not check feedback on
   previous items.
3. If all are processed, report a summary ("Processed X issues/PRs. Y items
   waiting for feedback.") and pause. The user says "follow up" to resume.

---

## Publishing Releases

When the user requests publishing to PyPI or preparing a release, delegate to
release-manager (which invokes the `c3:release` skill): version bump decision,
updating version files, changelog, pre-publish checks, build, tag, GitHub
release, PyPI upload.

```python
Agent({ subagent_type: "c3:release-manager",
  prompt: "Execute release workflow: determine version bump, update files, run checks, build, and publish to PyPI",
  description: "Execute release" })
```

Key checks (handled by release-manager): README image paths use absolute GitHub
URLs; version synced between `pyproject.toml` and `__init__.py`; local dev
config (`[tool.uv.sources]`, `[tool.uv.workspace]`) removed; entry points
verified; package contents verified after build.

---

## Agent Quick Reference

| Agent | Phase | When to invoke |
|-------|-------|----------------|
| functional-analyst | 1, 2, 3, 4, 5.6 | Always |
| researcher | 1 | When gaps or tech choices |
| api-architect | 3, 5.6 (via project-review) | Backend or Full stack |
| ui-ux-designer | 3, 5.6 (via project-review) | Frontend or Full stack |
| security-engineer | 3, 5.6 (via project-review) | Security-related |
| python-developer | 5.5 | Always for Python projects |
| end-user-documenter | 5.6 (via project-review) | User-facing changes |
| code-reviewer | 5.6 (via project-review) | Always |
| testing-engineer | 5.6 (via project-review) | Always |
| release-manager | 0, 5, 6 (via sub-skill), 7 (via sub-skill) | All git/gh operations |
| bug-fixer | 0.3, task-type detection | Bug tasks |

## Sub-skills

| Sub-skill | Phase | Purpose |
|-----------|-------|---------|
| `c3:project-review` | 5.6, 6.4 | Shared review cycle with `make check` gate |
| `c3:project-handle-pr` | 6 | PR feedback iteration with review re-entry |
| `c3:project-post-merge` | 7 | Sequenced post-merge cleanup |

## File Conventions

| File | Path |
|------|------|
| Functional analysis | `analysis/functional.md` |
| API analysis | `analysis/api-{topic}.md` |
| UX analysis | `analysis/ux-{topic}.md` |
| Security analysis | `analysis/security-{topic}.md` |
| Bug analysis | `analysis/bug/{bug-id}.md` |
| Consensus summary | `reporting/{task-name}/consensus.md` |
| Plan | `reporting/{task-name}/plan.md` |
| Implementation review report | `reporting/{task-name}/{agent}-review.md` |
| Task summary | `reporting/{task-name}/summary.md` |
| Research findings | `research/{topic}.md` |
| Technology recommendations | `research/{topic}/recommendations.md` |
| MBIs | `PLAN.md` (managed via `c3:plan`) |

All analysis documents go in `analysis/` with sub-folders for organization.

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

**Unsorted section rules:** placed at the top; short ideas without acceptance
criteria; functional-analyst moves them into the prioritized Backlog when
analyzed; optional — only present when the user has captured unsorted ideas.

## Notes

- The functional-analyst owns the TODO.md structure; domain agents contribute
  through it.
- Resolve conflicts between domain recommendations based on project priorities.
- Ensure all tasks have verifiable acceptance criteria before implementation.
- **Bugs** → Bug Implementation Flow: `c3:bug-fixer` (diagnose + TDD + fix +
  `make check`, reports back) → `c3:project-review` (scoped) → PR via
  `c3:release-manager`. Same review + PR funnel as features, no Plan Approval Gate.
- **Features** → follow the phases with domain design reviews.
- **Research** is conditional — invoke when gaps identified or technology choices
  needed.
- **MBIs** are first-class: Active MBI tasks take priority over the linear
  backlog. Use `c3:plan` to create/score them.
- **Security review** is scoped to security-related tasks.
- **Documentation** is part of task completion for user-facing changes.
- **Parallel reviews** improve efficiency without sacrificing quality.
- **User can request reanalysis**: use the "Run fresh analysis" option when
  proposing the next task.
- **PR ownership**: the agent creates PRs and processes feedback, but ONLY the
  owner merges PRs. Never propose merging.
- **TODO.md direction is authoritative**: when TODO.md specifies an approach,
  follow it without asking for confirmation. Only ask for clarification when
  genuinely ambiguous or conflicting requirements exist.
- **`make check` is the quality gate**: never authorize a commit while
  `make check` fails. The gate applies to initial implementation (5.6) and to
  every PR-feedback round (6.4 via `c3:project-handle-pr`).

## Communication with the User

- Provide clear status updates at each phase transition
- Report blockers or issues requiring user input
- Summarize agent findings and decisions
- When the project is ready for work, propose the next task from the backlog

### Using AskUserQuestion

**CRITICAL**: when asking the user for input and there are **limited possible
answers (<7)**, use the AskUserQuestion tool instead of plain text prompts. This
applies to task approval, workflow selection, priority decisions, conflict
resolution, branch selection — but **never** to owner-approval gates, which
happen in PR comments.

## Reference Files

- [references/issue-review-workflow.md](references/issue-review-workflow.md) — GitHub issue triage, owner authority, clarification process
- [references/bug-workflow-integration.md](references/bug-workflow-integration.md) — How the bug workflow integrates with project management
- [../project-review/SKILL.md](../project-review/SKILL.md) — Shared review cycle (Stage a–f, `make check` gate)
- [../project-handle-pr/SKILL.md](../project-handle-pr/SKILL.md) — Phase 6: PR feedback iteration
- [../project-post-merge/SKILL.md](../project-post-merge/SKILL.md) — Phase 7: post-merge cleanup