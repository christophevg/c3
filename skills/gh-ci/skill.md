---
name: gh-ci
description: Follow up on GitHub CI after pushing changes. Use after pushing to check CI status, view failures, and verify PR checks pass. Handles queued/blocked runs with proper timeouts.
---

# gh-ci

Follow up on GitHub CI after pushing changes.

## When to Use This Skill

Use this skill when:
- After pushing changes to a PR
- After creating a commit on a feature branch
- User asks to "check CI" or "wait for tests"
- User wants to verify PR status

## Overview

| Capability | Description |
|------------|-------------|
| Check CI status | See if CI is passing, failing, or pending |
| View failures | Get detailed logs for failed checks |
| Wait for completion | Poll until CI completes (with timeout) |
| PR status | View PR and its checks |

## Key Commands

### Essential Commands (Use These)

| Purpose | Command |
|---------|---------|
| Push to remote | `git push <remote> <branch>` |
| List recent runs | `gh run list --limit 3` |
| View specific run | `gh run view <id>` |
| View failed logs | `gh run view <id> --log-failed` |
| Check PR status | `gh pr view <number>` |
| List PR checks | `gh pr checks <number>` |

### Commands to Avoid

| Command | Why Avoid |
|---------|-----------|
| `gh pr checks --watch` | Blocks indefinitely if run is queued/blocked |
| `gh run watch <id>` | Blocks indefinitely if run is queued |
| Multiple `gh api` calls | Inefficient, use specific commands |

## Workflow

### 1. After Pushing Changes

```bash
# Push first
git push <remote> <branch>

# Get PR number if not known
gh pr list --head <branch> --json number --jq '.[0].number'
```

### 2. Check CI Status

**Don't use `--watch` - it blocks indefinitely on queued runs!**

Instead, poll with timeout:

```bash
# Check current status (doesn't block)
gh run list --limit 3

# Or check specific PR
gh pr checks <number>
```

### 3. If Run is Pending/Queued

Use polling with timeout (max 3 attempts, 30 seconds each):

```
Loop up to 3 times:
  1. gh run list --limit 1
  2. If status is "completed", break
  3. If status is "queued" or "in_progress", wait 30 seconds
  4. If max attempts reached, report status to user
```

### 4. If CI Failed

```bash
# Find the failed run
gh run list --limit 5

# View failure details
gh run view <id> --log-failed
```

Look for specific failure patterns:
- `ruff format --check` → formatting issue (run `make format`)
- `pytest` → test failures (run `make test`)
- `mypy` → type errors (run `make typecheck`)

### 5. After CI Passes

Report success:
- PR URL
- Check status summary
- Ask user if they want to merge (if applicable)

## Timeout Handling

**CRITICAL:** Never use commands that block indefinitely.

| Situation | Safe Command | Timeout |
|-----------|--------------|---------|
| Check status | `gh run list` | N/A |
| Check PR | `gh pr checks <n>` | N/A |
| View failures | `gh run view <id> --log-failed` | N/A |
| Wait for CI | Poll with timeout | Max 90 seconds (3 × 30s) |

## Stuck/Blocked Runs

**CRITICAL:** Sometimes GitHub workflow runs get stuck in "queued" state with 0 jobs. This is a GitHub infrastructure issue, not a code problem.

### Signs of a Stuck Run

- Run status: "queued" for extended time (>5 minutes)
- Job count: 0 (no jobs attached to the run)
- Re-run triggers: "already running" error

### Cannot Cancel

- `gh run cancel <id>` - May fail with "Cannot cancel a workflow re-run that has not yet queued"
- `gh run delete <id>` - May fail with HTTP 403 (permission denied)

### Resolution

**When a run is stuck with 0 jobs:**

1. Report to user: "CI run is stuck (queued with 0 jobs). This is a GitHub infrastructure issue."
2. Ask user: "Would you like to push another commit to trigger a fresh run, or wait?"
3. Do NOT try to cancel/delete the stuck run - it typically fails
4. User may need to cancel manually from GitHub web UI

### Example

```
CI run #26300121435 is stuck:
- Status: queued
- Jobs: 0
- Duration: 8+ minutes

This is a GitHub infrastructure issue, not a code problem.
Possible solutions:
1. Wait for GitHub to process it
2. Push another commit to trigger fresh run
3. Cancel manually from GitHub web UI
```

## Common Scenarios

### Scenario: Just Pushed, Need to Wait for CI

1. Push completed
2. Check status: `gh run list --limit 1`
3. If "queued" or "in_progress":
   - Wait 30 seconds
   - Check again (max 3 times)
4. If "completed":
   - Check conclusion: `gh run view <id> --json conclusion`
   - If "failure": `gh run view <id> --log-failed`
   - If "success": Report to user

### Scenario: CI Failed, Need to Fix

1. View failure: `gh run view <id> --log-failed`
2. Identify failure type (lint, test, typecheck)
3. Fix locally
4. Commit and push fix
5. Return to waiting workflow

### Scenario: Multiple Runs on Same Branch

1. List runs: `gh run list --branch <branch> --limit 5`
2. Identify latest by creation date
3. Check its status

## Example Output

### Success Report

```
CI passed for PR #2

✓ test (ubuntu-latest, 3.11) - passed
✓ test (macos-latest, 3.11) - passed  
✓ lint - passed
✓ typecheck - passed

PR: https://github.com/user/repo/pull/2
```

### Failure Report

```
CI failed for PR #2

✗ lint - failed
  Error: Would reformat: src/file.py
  Fix: make format

✓ test - passed
✓ typecheck - passed

Run ID: 123456
View details: gh run view 123456 --log-failed
```

## Integration with Project Manager

When invoked from `project-manage` skill:

1. After commit, push branch
2. Call this skill to verify CI
3. Only report success after CI passes
4. If CI fails, report failure with details
5. User decides next action (fix or merge)

## Related Skills

- `c3:commit` - For creating commits before CI
- `c3:git-activity-report` - For summarizing git activity