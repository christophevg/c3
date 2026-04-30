---
name: git-activity-report
description: Generate human-readable git activity summaries focused on accomplishments. Use when user asks to "report git activity", "show work done", or wants a summary of commits. Examples: "/git-activity-report --week", "report git activity for today on paths in file repos.txt", "what did I do this week".
---

# Git Activity Report

Generate human-readable activity summaries from git repositories. The skill produces non-technical reports focused on accomplishments, suitable for sharing with stakeholders unfamiliar with the projects.

## Overview

| Capability | Description |
|------------|-------------|
| Multi-repo queries | Aggregate activity across multiple repositories |
| Time-based filtering | Filter by today, yesterday, week, or month |
| AI narrative | Generate accomplishment-focused summaries |
| Path flexibility | Direct paths, file input, or glob patterns |

## When to Use This Skill

Use this skill when:
- User invokes `/git-activity-report` command
- User asks to "report git activity" or "show work done"
- User wants a summary of their commits over a period
- User mentions paths in a file (e.g., "repos.txt")

## Skill Interface

```
/git-activity-report [path...] [--file FILE] [--today|--yesterday|--week|--month]
```

**Defaults:**
- Period: `--week` if not specified
- Paths: Current directory (`.`) if not specified

**Examples:**
```bash
/git-activity-report --today
/git-activity-report ~/Workspace/agentic/* --week
/git-activity-report --file repos.txt --month
```

**Natural language examples:**
- "report git activity for today on paths in file repos.txt"
- "show me this week's work on incubator"
- "what did I do today"

## Workflow

1. **Parse arguments** - Extract paths, `--file` reference, and time period
2. **Collect data** - Run the `scripts/git-activity.py` script with the resolved arguments:
   ```bash
   scripts/git-activity.py --since "<period>" <paths...>
   ```
   The script handles path expansion, git repo validation, author detection, and statistics collection in a single invocation.
3. **Parse JSON output** - The script returns structured data with commits, stats, and totals
4. **Generate narrative** - Write accomplishment-focused summary using the template
5. **Output** - Print formatted markdown to console

## Time Periods

| Flag | Git `--since` value |
|------|---------------------|
| `--today` | `midnight` or `0am` |
| `--yesterday` | `1 day ago` (limit to yesterday) |
| `--week` | `1 week ago` |
| `--month` | `1 month ago` |

## Path File Format

```
# Comments start with #
~/Workspace/agentic/incubator
~/Workspace/agentic/christophe.vg

# Blank lines are ignored
~/Workspace/agentic/c3
```

## Filtering Rules

**Exclude from statistics:**
- Merge commits (commits with >1 parent)
- Lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- Minified files: `*.min.js`, `*.min.css`
- Generated files: `*.generated.*`, `dist/`, `build/`

**Author filter:**
- Only include commits by current git user (`git config user.name`)

## Output Structure

See `templates/report.md` for the complete template structure:

```markdown
# Activity Report: [Period]

## Summary

[AI-generated narrative of accomplishments across all projects]

## Projects

### [Project Name]

[AI-generated narrative for this project]

**Commits:** X | **Files:** Y | **Lines:** +A/-B

- [Human-readable commit description]
- [Human-readable commit description]

### [Project Name]

...

## Totals

| Metric | Value |
|--------|-------|
| **Total Commits** | X |
| **Total Files** | Y |
| **Lines Added** | +A |
| **Lines Removed** | -B |

## No Activity

- [repo-path] - No commits in this period
```

## Narrative Generation Guidelines

When generating the narrative:

1. **Focus on accomplishments** - What was achieved, not how
2. **Use present tense** - "Add authentication system" not "Added"
3. **Strip conventional prefixes** - Show "Add feature" not "feat: Add feature"
4. **Group related commits** - Combine "Add login" + "Add logout" → "Implement authentication"
5. **Avoid jargon** - No commit hashes, no branch names
6. **Quantify when helpful** - "Fixed 3 bugs", "Updated 5 components"

## Script Reference

The `scripts/git-activity.py` script handles all git operations:

```bash
# Basic usage
scripts/git-activity.py --since "1 week ago" ~/projects/*

# With explicit author
scripts/git-activity.py --author "John Doe" --since "4 days ago" ~/work/*

# Include repos with no activity
scripts/git-activity.py --include-empty --since "midnight" ~/code/*
```

**Output:** JSON with `projects`, `commits`, `stats`, `totals`, and `empty_repos` fields.

See `patterns/git-queries.md` for the underlying git commands.

## Related Skills

- `git-scripting` - Safe git command patterns for scripts