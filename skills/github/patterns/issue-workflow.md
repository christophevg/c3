# Issue Workflow

## Overview

GitHub Issues are used for tracking work: features, bugs, tasks. This workflow handles reviewing, labeling, and managing issues.

## Issue Review Process

### Checking for New Issues

```bash
# List all open issues
gh issue list --limit 10 --state open

# List issues with details
gh issue list --limit 10 --state open --json number,title,labels,author

# List issues without status labels (unreviewed)
gh issue list --limit 10 --state open --json number,title,labels \
  --jq '.[] | select(.labels | length == 0)'
```

### Reviewing an Issue

For each unreviewed issue:

1. Read title and body
2. Check for status label
3. If no status: needs review

```bash
# View issue details
gh issue view {number}

# View issue body
gh issue view {number} --json body --jq '.body'
```

## Issue Status Labels

| Label | Meaning | Action |
|-------|---------|--------|
| `status:backlog` | Reviewed, added to TODO.md | Keep open, implement later |
| `status:in-progress` | Currently implementing | Keep open, track progress |
| `status:wont-do` | Decision: won't implement | Close with explanation |
| `status:needs-research` | Needs evaluation | Keep open, research first |
| `status:blocked` | Blocked by dependency | Keep open, note blocker |

## Issue Commands

### Labeling Issues

```bash
# Add label
gh issue edit {number} --add-label "status:backlog"

# Remove label
gh issue edit {number} --remove-label "status:in-progress"

# Add multiple labels
gh issue edit {number} --add-label "status:backlog,enhancement"

# Replace all labels
gh issue edit {number} --label "status:backlog,enhancement"
```

### Commenting on Issues

```bash
# Add comment
gh issue comment {number} --body "Reviewed and accepted. Added to backlog."

# Multi-line comment
gh issue comment {number} --body "$(cat <<'EOF'
Thank you for this issue.

After review, I've decided to:
1. Add it to the backlog
2. Schedule for next sprint

 ETA: Q2 2024
EOF
)"
```

### Closing Issues

```bash
# Close with comment
gh issue close {number} --comment "Closing: not in scope because..."

# Close as completed
gh issue close {number} --comment "Fixed in PR #123"

# Reopen issue
gh issue reopen {number} --comment "Reopening: issue persists"
```

## Issue Resolution Actions

### Accept Issue → Backlog

```bash
# Add status label
gh issue edit {number} --add-label "status:backlog"

# Add comment
gh issue comment {number} --body "Reviewed and accepted. Added to TODO.md."

# Add additional labels if applicable
gh issue edit {number} --add-label "enhancement"
```

### Reject Issue → Won't Do

```bash
# Add status label
gh issue edit {number} --add-label "status:wont-do"

# Close with explanation
gh issue close {number} --comment "Closing: not in scope because..."
```

### Needs Research

```bash
# Add status label
gh issue edit {number} --add-label "status:needs-research"

# Add comment
gh issue comment {number} --body "Needs evaluation for technical feasibility."
```

### Blocked by Dependency

```bash
# Add status label
gh issue edit {number} --add-label "status:blocked"

# Add comment with blocker details
gh issue comment {number} --body "Blocked by: #{blocking-issue-number}. Will proceed after blocker is resolved."
```

### Starting Implementation

```bash
# Add status label
gh issue edit {number} --add-label "status:in-progress"

# Link to branch/PR when ready
gh issue comment {number} --body "Starting work on branch feature/{number}-{description}."
```

## Issue Linking in PRs

### Auto-Close on Merge

Use these keywords in PR body:

| Keyword | Effect |
|---------|--------|
| `Closes #{number}` | Closes issue when PR merges |
| `Fixes #{number}` | Closes issue when PR merges |
| `Resolves #{number}` | Closes issue when PR merges |

### Reference Without Closing

| Keyword | Effect |
|---------|--------|
| `Related to #{number}` | Links issue without closing |
| `See #{number}` | Links issue without closing |

## Common Scenarios

### Scenario: Review New Issues

1. List unreviewed issues: `gh issue list --limit 10 --state open --json number,title,labels`
2. For each issue without status label:
   - View details: `gh issue view {number}`
   - Assess: feature request? bug? question?
   - Decide: backlog, wont-do, needs-research
   - Apply label and comment
3. Report summary to user

### Scenario: Check Issue Status

```bash
# View issue
gh issue view {number}

# Check labels
gh issue view {number} --json labels --jq '.labels'
```

### Scenario: Issue Completed via PR

1. User confirms PR merged
2. Issue should auto-close if PR body has `Closes #{number}`
3. If not auto-closed:
   ```bash
   gh issue close {number} --comment "Closed via PR #{pr-number}"
   ```

### Scenario: Issue Needs Clarification

```bash
# Ask question in comment
gh issue comment {number} --body "$(cat <<'EOF
Thank you for this issue.

Could you provide more details about:
1. Expected behavior?
2. Steps to reproduce?
3. Environment (OS, version)?
EOF
)"
```

## Issue Search

```bash
# Search by title
gh issue list --search "bug in auth"

# Search by label
gh issue list --label "bug"

# Search by assignee
gh issue list --assignee username

# Search by author
gh issue list --author username

# Combined search
gh issue list --state open --label "bug" --limit 20
```