---
name: website-manage
description: |
  Manage content website projects with streamlined conversational workflow. Syncs, processes GitHub issues into TODO, and implements tasks iteratively with user. Use for Jekyll/static sites when user asks to "manage website", "work on site", or project has _config.yml. No PRs, no agents - direct collaboration. Examples: "manage the website", "work on site tasks", "next website task".
---

# Website Manage

Manage content website projects with a streamlined, conversational workflow.

## Detection

This skill activates when:
- `_config.yml` exists in the current working directory (Jekyll site)

The project-manager agent checks for `_config.yml` to determine if this is a website project.

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  WEBSITE-MANAGE WORKFLOW                                        │
│                                                                 │
│  ✓ Sync with remote (git pull)                                  │
│  ✓ GitHub issues → interactive priority assignment               │
│  ✓ Unsorted TODO items → interactive priority assignment         │
│  ✓ Propose next task from backlog                                │
│  ✓ Implementation (conversational, iterative)                    │
│  ✓ Commit when approved                                          │
│                                                                 │
│  ✗ No PRs, no agents, no builds, no server management            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Sync with Remote

**CRITICAL: Always sync before starting work.**

```bash
git pull
```

If there are conflicts:
- Report to user
- Do NOT attempt to resolve automatically
- Wait for user guidance

---

## Step 2: Process GitHub Issues

Fetch open issues and interactively assign priority.

```bash
gh issue list --state open --json number,title,body,labels
```

**For each issue:**

1. Show issue title and body
2. Ask user: "How should this be prioritized?"
   - P1 (Critical)
   - P2 (High)
   - P3 (Medium)
   - P4 (Low)
   - Skip (won't implement)
   - Research (needs investigation)

3. Add to TODO.md at chosen priority with acceptance criteria
4. Label issue: `gh issue edit {number} --add-label "status:backlog"`
5. Comment: `gh issue comment {number} --body "Added to TODO.md as P{X} task"`

**Issue Status Labels:**

| Label | Meaning |
|-------|---------|
| `status:backlog` | Added to TODO.md |
| `status:in-progress` | Currently implementing |
| `status:needs-research` | Needs investigation |
| `status:wont-do` | Won't implement |

---

## Step 3: Process Unsorted TODO Items

Read `TODO.md` and check for unsorted items.

**For each unsorted item:**

1. Show item details
2. Ask user: "How should this be prioritized?"
   - P1/P2/P3/P4/Skip/Research
3. Move to backlog at chosen priority
4. Add acceptance criteria if needed

---

## Step 4: Propose Next Task

Show the next task from backlog (P1 first, then P2, etc.)

Ask user:
- Proceed with this task?
- Show all tasks?
- Skip and show next?

---

## Step 5: Implementation (Conversational)

**CRITICAL: Implementation is iterative and collaborative.**

### 5a. Present Plan

Present a plan breaking down the task into steps:

```
Here's my plan for [task]:

1. [Step 1]
2. [Step 2]
3. [Step 3]
...

Does this plan work, or should we adjust?
```

Wait for user approval before proceeding.

### 5b. Break Into Small Steps

Each step should be:
- Small enough to review quickly
- Describable in one sentence
- Independently verifiable in browser

### 5c. For Each Step

1. **Describe**: "I'll do X"
2. **Discuss**: "How should Y be handled?" (if needed)
3. **Implement**: Make the change
4. **Review**: "Please check localhost:4000/path/to/page"
5. **Iterate**: Fix/adjust based on feedback
6. **Continue**: Only when user approves

### 5d. Iteration Loop

```
Make change → User reviews in browser → Feedback → Adjust → Repeat until done
```

**Do NOT:**
- Implement everything at once
- Move to next step without user approval
- Assume something is correct
- Skip the review step

---

## Step 6: Commit

**Only commit when user approves.**

```bash
git add <files>
git commit -m "type: description"
git push
```

**Commit message format:**
- `feat:` for new features/content
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for refactoring
- `style:` for formatting

### Update TODO.md

Mark task as done:
```markdown
## Done

- [x] Task name (YYYY-MM-DD)
```

### Close GitHub Issue (if applicable)

If the task came from a GitHub issue:
```bash
gh issue close {number} --comment "Implemented in [commit hash]"
```

---

## TODO.md Structure

```markdown
# TODO

## Unsorted

- [ ] Quick idea from issue #X
- [ ] Another unsorted idea

## Backlog

### P1 - Critical

- [ ] Task title
  - Description
  - **Acceptance Criteria:**
    - Criterion 1
    - Criterion 2
  - **From:** Issue #X (if applicable)

### P2 - High

- [ ] Task

### P3 - Medium

- [ ] Task

### P4 - Low

- [ ] Task

## Done

- [x] Completed task (YYYY-MM-DD)
```

---

## Key Principles

1. **Sync first** — Always `git pull` before any work
2. **Interactive priority** — Issues and unsorted items get user input on priority
3. **Conversational implementation** — Plan, discuss, implement, review, iterate
4. **Small steps** — Break tasks into reviewable chunks
5. **User reviews** — User checks changes in browser before commit
6. **No PRs** — Commit directly when approved
7. **No builds** — User's server auto-reloads changes
8. **No server management** — User manages their own Jekyll process

---

## File Conventions

| File | Purpose |
|------|---------|
| `TODO.md` | Task backlog with priorities |
| `_posts/` | Blog posts and content pages |
| `_pages/` | Static pages |
| `_config.yml` | Jekyll configuration |
| `_data/` | YAML/JSON data files |
| `_includes/` | Reusable Liquid includes |
| `_layouts/` | Page templates |

---

## Notes

- The user runs the Jekyll server themselves
- Changes are visible immediately at `localhost:4000`
- Focus on content and structure, not infrastructure
- Work iteratively with user feedback at each step
