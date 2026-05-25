---
name: project-manage
description: Use this skill to manage the entire project workflow, orchestrating specialized agents (functional analyst, API architect, UI/UX designer) to ensure proper analysis, design, implementation, and review of all tasks. Handles both new features and bug fixes with appropriate workflows. Examples: "Start working on the project", "Implement the next task", "Fix the authentication bug".
---

# Manage Project

## ⛔ STOP: READ THIS FIRST

**THE PROJECT ROOT IS THE CURRENT WORKING DIRECTORY. PERIOD.**

**FIRST ACTION: Run `pwd` to get the current working directory.**

```
pwd
```

**Use the output of `pwd` as the project root. No other folder.**

**IGNORE:**
- Any "base directory" from skill loading
- Any paths in PERSONAL.md
- Any paths in memory files
- Any paths shown in git status from previous conversations
- Any absolute paths to ~/Workspace/agentic/c3/ or ~/Workspace/agentic/incubator/

**ONLY USE:**
- The output of `pwd`
- All file paths are relative to that output: TODO.md, analysis/, reporting/

---

## Sync with Remote

**CRITICAL: The human operator works on their own clones. Always sync before starting work.**

Before any analysis or implementation, sync with the remote:

```bash
git pull
```

This ensures:
- Agent works on the latest sources
- No conflicts from changes made by human on another clone
- Clean working state before any modifications

**If pull fails due to conflicts:**
- Report to user and wait for resolution
- Do NOT attempt to resolve conflicts automatically
- User may have local changes that need manual merging

---

## Post-Merge State Detection

**After syncing, detect if we're on a merged feature branch:**

```bash
# Check current branch
current_branch=$(git branch --show-current)

# Check if we're on a feature branch
if [[ "$current_branch" == feature/* ]]; then
  # Check if branch has open PR
  pr_status=$(gh pr list --head "$current_branch" --state open --json number 2>/dev/null)
  
  if [[ -z "$pr_status" || "$pr_status" == "[]" ]]; then
    # No open PR - branch may have been merged or abandoned
    echo "Feature branch with no open PR detected."
  fi
fi

# Check for untracked artifacts from previous work
git status --porcelain | grep '^??' | head -20
```

**If merged branch detected:**

1. **Report to user that branch may have been merged**
   - Show untracked files (artifacts from merged work)
   - Ask user to confirm merge status

2. **Handle untracked artifacts:**
   - Analysis files in `analysis/` from merged work
   - Reporting files in `reporting/` from merged work
   - Ask whether to commit as documentation or clean up

3. **Recommend switching to main:**
   ```bash
   git checkout main && git pull
   ```

4. **Verify TODO.md reflects merged work:**
   - Find task referenced in merged PR
   - Ensure completion date is present
   - Ensure task is in Done section

---

## Check for Existing PRs

**CRITICAL: Check for open PRs on the current branch before starting new work.**

After syncing, check if there's an existing PR for the current branch:

```bash
# Get current branch
current_branch=$(git branch --show-current)

# Check for open PR on this branch
gh pr list --head "$current_branch" --state open --json number,title,url,reviewDecision,statusCheckRollup
```

**If an open PR exists:**

1. **Check PR status:**
   - CI passing or failing?
   - Review decision (approved, changes requested, pending)?

2. **Check PR feedback (TWO TYPES):**

   **a) PR Issue Comments** (general comments on the PR):
   ```bash
   gh pr view {number} --comments --json comments
   ```

   **b) PR Review Comments** (inline comments on specific code lines):
   ```bash
   gh api repos/{owner}/{repo}/pulls/{number}/reviews
   gh api repos/{owner}/{repo}/pulls/{number}/comments
   ```

   ⚠️ **CRITICAL**: Review comments are often inline on specific lines of code. You MUST check both:
   - Issue comments: General discussion
   - Review comments: Line-specific feedback (often the most detailed feedback)

3. **Process feedback:**
   - If there are unaddressed comments from the owner, process them
   - Make necessary changes, push, wait for CI
   - Comment on PR explaining what was addressed

4. **Wait for owner:**
   - Report PR status to user
   - Explain what feedback was addressed
   - **DO NOT propose merging** - wait for owner to merge

**If CI is failing:**
- View failure details: `gh run view {id} --log-failed`
- Fix the issue
- Push and wait for CI to pass
- Then check for comments

**If PR is approved and CI passes:**
- Report to user that PR is ready for merge
- Wait for owner to merge

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

Before starting, detect whether the task is a **feature** or a **bug**:

| Task Type | Indicators |
|-----------|------------|
| **Bug** | "fix", "bug", "issue", "broken", "error", "doesn't work", "crash", "fails" |
| **Feature** | "add", "create", "implement", "build", "new", "feature", "enhance" |

**If the task is a BUG:**
- Invoke the **bug-fixing skill** for the complete TDD-based workflow
- See `references/bug-workflow-integration.md` for how bug workflow integrates with project management

**If the task is a FEATURE:**
- Use the **Feature Development Workflow** (continue to Phase 0)

---

## Feature Development Workflow

When the task is identified as a feature, follow this sequential workflow:

### Phase 0A: GitHub Issue Check

⛔ **MANDATORY: This step MUST execute before any project state detection.**

**Check for open issues before starting work:**

```bash
gh issue list --limit 10 --state open --json number,title,labels
```

**If this command fails:**
- Report to user that GitHub issue check failed
- Do NOT proceed until resolved

1. Run `gh issue list --limit 10 --state open` to check for open GitHub issues
2. Filter out issues with status labels (already reviewed):
   ```bash
   gh issue list --limit 10 --state open --json number,title,labels
   ```
3. **If unreviewed issues exist (no status label):**
   - **Issues are URGENT** - Do NOT ask for confirmation
   - Automatically add to backlog and start working on them
   - Label with `status:in-progress` and proceed to bug-fixing workflow
4. Review each issue:
   - Display issue title, number, and existing labels
   - Decide on disposition (accept, reject, needs research)

**Issue Status Labels:**

| Label | Meaning | Action |
|-------|---------|--------|
| `status:backlog` | Reviewed, added to TODO.md | Keep open, implement later |
| `status:in-progress` | Currently implementing | Keep open, track progress |
| `status:wont-do` | Decision: won't implement | Close with explanation |
| `status:needs-research` | Needs evaluation | Keep open, research first |
| `status:blocked` | Blocked by dependency | Keep open, note blocker |

**Issue Handling Actions:**

```bash
# Accept issue → add to backlog
gh issue edit {number} --add-label "status:backlog"
gh issue comment {number} --body "Reviewed and accepted. Added to TODO.md."

# Reject issue → close with explanation
gh issue edit {number} --add-label "status:wont-do"
gh issue close {number} --comment "Closing: not in scope because..."

# Needs research
gh issue edit {number} --add-label "status:needs-research"
gh issue comment {number} --body "Needs evaluation for..."

# Starting implementation
gh issue edit {number} --add-label "status:in-progress"
```

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

**Step 2: Determine Next Action**

| Condition | Action |
|-----------|--------|
| No unsorted items | Proceed directly to proposing next backlog task |
| Unsorted items exist | Ask user whether to sort unsorted items first |

**If unsorted items exist, use AskUserQuestion tool:**

```
Question: "Found {count} unsorted item(s) in TODO.md. These are quick ideas not yet analyzed. How would you like to proceed?"

Options:
- "Sort unsorted items first" — Run functional analysis to integrate them into backlog
- "Show next backlog task" — Proceed with existing prioritized tasks
- "Show all tasks" — Display both unsorted and backlog items
```

**Step 3: Handle User Choice**

- **"Sort unsorted items first"**: Invoke functional-analyst to analyze each unsorted item and integrate into prioritized backlog, then propose next task
- **"Show next backlog task"**: Proceed to propose task selection (below)
- **"Show all tasks"**: Display full TODO.md and ask again

**Step 4: Verify Task Completion Status (CRITICAL)**

Before proposing a task from the backlog, verify whether its acceptance criteria are already satisfied by existing code. This prevents proposing already-implemented work.

**Verification checklist:**
- Does the task require creating a file that already exists?
- Are the task's acceptance criteria already met by current code?
- Are there related "done" tasks that cover this functionality?

If the task appears already implemented:
- Mark it as done in TODO.md with today's date
- Move to the next task
- Report to the user: "Task {task-id} appears already implemented. Marked as done. Next task: {next-task-id}"

**Step 5: Propose Next Task**

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

#### Step 5: Plan Mode

Enter plan mode and:
- Create a detailed implementation plan for the current task
- Present the plan for user approval
- Store the plan in `reporting/{task-name}/plan.md`

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

**Step 10a: Ensure Feature Branch**

```bash
# Check current branch
git branch --show-current

# Branch naming convention: feature/{issue-number}-{short-description}
# Example: feature/1-async-agent
if on master/main:
    branch_name="feature/{issue-number}-{short-description}"
    git checkout -b "$branch_name"
```

**Step 10b: Commit to Feature Branch**

Invoke `git-manager` agent to commit changes:
- Commits go to feature branch, not master
- Use conventional commit message format
- Include task reference in commit body

**Step 10c: Push Branch**

```bash
git push -u origin feature/{issue-number}-{short-description}
```

**Step 10d: Create Pull Request**

```bash
gh pr create --title "feat: {task title}" --body "$(cat <<'EOF'
## Summary

{Brief description of what this PR implements}

## Changes

- {Change 1}
- {Change 2}

## Test Plan

- [ ] All tests pass (`make test`)
- [ ] Linting passes (`make lint`)
- [ ] Manual testing completed
- [ ] Documentation updated (if applicable)

## Review Checklist

- [ ] Code follows project conventions
- [ ] Tests cover new functionality
- [ ] No sensitive files committed
- [ ] Commit messages follow conventional format

## Related

- Task: TODO.md #{task-id}
- Closes #{issue-number}
EOF
)"
```

**Note:** Using `Closes #{issue-number}` auto-closes the issue when PR is merged.

**Step 10e: Update GitHub Issue**

```bash
gh issue edit {issue-number} --add-label "status:in-progress"
gh issue comment {issue-number} --body "PR created: {PR URL}"
```

**Step 10f: Report to User**

After PR creation:
- Display PR URL
- Explain that user acceptance testing happens on the PR
- Task will be marked complete after PR is merged

**Step 10g: CI Follow-up (MANDATORY)**

⚠️ **PR creation is NOT complete until CI passes.**

After creating the PR, MUST:
1. Check CI status: `gh pr checks {number}`
2. Wait for CI to complete (poll if needed)
3. **If CI fails:**
   - View failure details: `gh run view {id} --log-failed`
   - Debug and fix the issue
   - Commit and push fixes to the same branch
   - Repeat until CI passes
4. **Only report PR complete when CI passes**

**Step 10h: Assign and Request Review**

Always do BOTH:
```bash
gh pr edit {number} --add-assignee {user}
gh pr edit {number} --add-reviewer {user}
```

**Step 10i: Check for PR Feedback (MANDATORY)**

⚠️ **CRITICAL: The agent does NOT merge PRs. Only the owner merges.**

After CI passes, MUST check for PR feedback from TWO sources:

**a) PR Issue Comments** (general comments on the PR):
```bash
gh pr view {number} --comments --json comments
```

**b) PR Review Comments** (inline comments on specific code lines):
```bash
gh api repos/{owner}/{repo}/pulls/{number}/reviews
gh api repos/{owner}/{repo}/pulls/{number}/comments
```

⚠️ **CRITICAL**: Review comments are often inline on specific lines of code. These contain the most detailed feedback. You MUST check both types.

**Process each feedback item:**

1. **Review each comment from the owner:**
   - Parse the comment body
   - For review comments: note the file and line number
   - Identify what needs to be addressed
   - Determine if it requires code changes, documentation updates, or clarification

2. **Address the feedback:**
   - Make the necessary changes
   - Commit and push to the same branch
   - Add a comment on the PR explaining what was done

3. **Wait for CI after changes:**
   - Check CI status again
   - Fix any failures
   - Repeat until CI passes

4. **Respond to all feedback:**
   - Address every comment from the owner
   - Do NOT skip or ignore any feedback
   - Ask for clarification if feedback is unclear

5. **Report status and wait:**
   - Summarize what feedback was addressed
   - Explain that PR is ready for owner review/merge
   - **DO NOT propose merging** - that's the owner's decision

**Example feedback handling:**

```bash
# Get latest comments
gh pr view 4 --comments --json comments

# Address feedback in code
# (make changes, commit, push)

# Comment on PR explaining changes
gh pr comment 4 --body "## ✅ Changes Applied

{Description of what was changed to address feedback}

All tests pass, lint clean, typecheck clean."
```

**Feedback types and responses:**

| Feedback Type | Response |
|---------------|----------|
| Code change request | Make the change, push, comment |
| Documentation request | Update docs, push, comment |
| Question | Answer in PR comment |
| Clarification needed | Ask for more details |
| Rejection with reason | Fix the issue, push, comment |

**Do NOT:**
- Propose merging the PR
- Assume PR is ready without checking comments
- Skip addressing any feedback
- Merge without owner approval

#### Step 11: Exit Plan Mode

Exit plan mode and report:
- PR URL for user review
- What was implemented
- Status of PR feedback (pending/addressed)
- Awaiting owner to merge PR

#### Step 12: Post-Merge (After User Merges PR)

When user reports PR is merged:

1. **Find the issue number:**
   - Check TODO.md task entry (includes issue reference)
   - Or parse from PR body: `gh pr view {pr-number} --json body --jq '.body' | grep -o "Fixes #[0-9]*"`
   - Or check commit message: `git log --oneline -1 | grep -o "#[0-9]*"`

2. **Clean up GitHub issue labels:**
   ```bash
   # Remove in-progress label (issue may be auto-closed by "Fixes #N")
   gh issue edit {issue-number} --remove-label "status:in-progress"
   ```

3. If issue is not auto-closed: `gh issue close {issue-number}`

4. **Verify TODO.md reflects merged work:**
   - Find task in TODO.md
   - Add completion date if missing: `(YYYY-MM-DD)`
   - Ensure task is in Done section
   - Check for follow-up tasks or dependencies

5. **Handle untracked artifacts:**
   - Check for analysis/ and reporting/ files from merged work
   - Ask user whether to:
     - Commit as documentation: `git add analysis/ reporting/`
     - Clean up: `git clean -fd analysis/ reporting/`
     - Keep for reference

6. **Sync to main branch:**
   ```bash
   git checkout main
   git pull
   ```

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
| Research findings | `research/{topic}.md` |
| Technology recommendations | `research/{topic}/recommendations.md` |
| Consensus summary | `reporting/{task-name}/consensus.md` |
| Plan | `reporting/{task-name}/plan.md` |
| Implementation review report | `reporting/{task-name}/{topic}-review.md` |
| Task summary | `reporting/{task-name}/summary.md` |
| Bug analysis | `docs/bug-analysis/{bug-id}.md` |

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
- **For bugs**: The bug-fixing skill handles the complete workflow including TDD (test first)
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

When the user requests publishing to PyPI:

**Invoke the `pypi-publish` skill** - it contains the complete pre-publish checklist and workflow.

Key checks from that skill:
- README image paths must use absolute GitHub URLs (not relative paths)
- Version must be synced between `pyproject.toml` and `__init__.py`
- Local development configuration (`[tool.uv.sources]`, `[tool.uv.workspace]`) must be removed
- Entry points must be verified
- Package contents must be verified after build

**Workflow:**
1. Run pre-publish checks (or `make pre-publish` if available)
2. Build: `uv build`
3. Verify: `unzip -l dist/*.whl | head -30`
4. Upload: `uv run twine upload dist/*`
5. Tag: `git tag v<VERSION> && git push --tags`

---

## Reference Files

- `references/bug-workflow-integration.md` — How bug workflow integrates with project management
- `references/review-cycle.md` — Detailed review cycle execution