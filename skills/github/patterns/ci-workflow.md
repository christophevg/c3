# CI Workflow

## Overview

GitHub Actions (or other CI) runs automated checks on every push and PR. This workflow handles checking status, viewing failures, and managing stuck runs.

## Key Commands

### Essential Commands

| Purpose | Command | Notes |
|---------|---------|-------|
| List recent runs | `gh run list --limit 3` | One-shot, no blocking |
| View specific run | `gh run view {id}` | Shows job summary |
| View failure logs | `gh run view {id} --log-failed` | Failed jobs only |
| Check PR status | `gh pr checks {number}` | One-shot, no blocking |
| View run jobs | `gh run view {id} --json jobs` | JSON output |

### Commands to Avoid

| Command | Why Avoid |
|---------|-----------|
| `gh pr checks --watch` | Blocks indefinitely if run is queued |
| `gh run watch {id}` | Blocks indefinitely if run is queued |

## Timeout Handling

**CRITICAL:** Never use commands that block indefinitely.

### Polling Pattern

```bash
# Check current status (one-shot)
gh run list --limit 3

# If pending or in_progress, poll with timeout
# Max: 3 attempts × 30 seconds = 90 seconds total

for i in 1 2 3; do
  status=$(gh run list --limit 1 --json status --jq '.[0].status')
  if [ "$status" = "completed" ]; then
    break
  fi
  sleep 30
done

# Check final result
gh run list --limit 1 --json status,conclusion --jq '.[0]'
```

**Note:** Polling requires permission each time. Future improvement: investigate MCP server for webhook-based CI notifications.

## Failure Patterns

When CI fails, identify the failure type:

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Formatting | `ruff format --check`, `black --check` | `make format` |
| Linting | `ruff check`, `flake8`, `pylint` | `make lint` (or fix manually) |
| Type errors | `mypy`, `pyright` | `make typecheck` |
| Tests | `pytest failed`, `FAILED` | `make test` (then fix failing tests) |
| Build | `build failed`, `compilation error` | Fix build errors |

### Viewing Failures

```bash
# Get run ID from list
gh run list --limit 5

# View failure details
gh run view {id} --log-failed

# View specific job
gh run view {id} --json jobs --jq '.jobs[] | select(.conclusion == "failure")'

# Get failure step
gh run view {id} --log-failed | grep -A5 "Error:"
```

## Stuck Runs

### Signs of a Stuck Run

- Run status: "queued" for extended time (>5 minutes)
- Job count: 0 (no jobs attached)
- Re-run triggers: "already running" error

### Why Runs Get Stuck

GitHub infrastructure issues, not code problems:
- Runner not available
- Workflow concurrency limits
- GitHub Actions queue backlog

### Resolution

**When a run is stuck with 0 jobs:**

1. **Report to user:**
   ```
   CI run #{id} is stuck:
   - Status: queued
   - Jobs: 0
   - Duration: X minutes

   This is a GitHub infrastructure issue, not a code problem.
   ```

2. **Ask user:**
   ```
   Would you like to:
   1. Push another commit to trigger a fresh run
   2. Wait for GitHub to process it
   3. Cancel manually from GitHub web UI
   ```

3. **Do NOT try to cancel/delete** - These commands typically fail on stuck runs

### If User Chooses to Retry

```bash
# Push empty commit to trigger new run
git commit --allow-empty -m "ci: trigger fresh run"
git push
```

### If User Cancels from Web UI

Wait for user confirmation, then:
```bash
# Check if new run started
gh run list --limit 1
```

## Workflow After Push

### 1. Push Changes

```bash
git push origin feature/42-branch
```

### 2. Check CI Status (Immediate)

```bash
gh run list --limit 1
```

### 3. If Queued or In Progress

Poll with timeout (max 3 × 30s):
```bash
for i in 1 2 3; do
  status=$(gh run list --limit 1 --json status --jq '.[0].status')
  if [ "$status" = "completed" ]; then
    break
  fi
  sleep 30
done
```

### 4. If Completed, Check Result

```bash
gh run list --limit 1 --json conclusion --jq '.[0]'
```

- `conclusion: "success"` → Report success
- `conclusion: "failure"` → View failures: `gh run view {id} --log-failed`

### 5. If Timed Out (Still Not Completed)

Report to user:
```
CI is still running after 90 seconds.
Run ID: {id}
Status: {status}

Check status: gh run view {id}
```

## Common Scenarios

### Scenario: Just Pushed, Need CI Status

1. Push completed
2. Check status: `gh run list --limit 1`
3. If "queued" or "in_progress": poll (max 3 × 30s)
4. If "completed": check conclusion
5. Report to user

### Scenario: CI Failed, Need to Fix

1. View failure: `gh run view {id} --log-failed`
2. Identify failure type (lint, test, typecheck)
3. Fix locally
4. Run local checks: `make test && make lint && make typecheck`
5. Commit fix: `git commit -m "fix: resolve CI failure"`
6. Push: `git push`
7. Return to monitoring workflow

### Scenario: Multiple Runs on Same Branch

1. List runs: `gh run list --branch {branch} --limit 5`
2. Identify latest by creation date
3. Check its status
4. Older runs can be ignored (superseded)

### Scenario: Need to Re-run CI

```bash
# User can re-run from GitHub web UI or:
gh run rerun {id}

# Note: This may fail if run is stuck
```

## Success/Failure Reports

### Success Report Format

```
CI passed for PR #{number}

✓ test (ubuntu-latest, 3.11) - passed
✓ test (macos-latest, 3.11) - passed
✓ lint - passed
✓ typecheck - passed

PR: https://github.com/{owner}/{repo}/pull/{number}
```

### Failure Report Format

```
CI failed for PR #{number}

✗ {job-name} - failed
  Error: {error-message}
  Fix: {suggested-fix}

✓ {passed-job} - passed

Run ID: {id}
View details: gh run view {id} --log-failed
```