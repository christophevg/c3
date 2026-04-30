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
| Deterministic output | Same input always produces same report format |
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

1. **Parse arguments** - Extract paths and time period
2. **Generate report** - Run `scripts/generate-report.py` with the arguments:
   ```bash
   scripts/generate-report.py --since "<period>" [--include-empty] <paths...>
   ```
3. **Output** - The script produces a complete markdown report

The script handles everything: path expansion, git repo validation, author detection, statistics collection, and deterministic report generation.

**For JSON output** (programmatic use):
```bash
scripts/generate-report.py --json --since "<period>" <paths...>
```

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

The script produces deterministic markdown following this structure:

```markdown
# Activity Report: [period]

**Period:** [period]
**Author:** [author]

## Summary

Activity across N projects. Most active: [project], [project], [project].

## Projects

### [Project Name]

Activity includes X new features, Y fixes, Z documentation updates.

**Commits:** X | **Files:** Y | **Lines:** +A/-B

- [Accomplishment stripped of conventional prefix]
- [Accomplishment stripped of conventional prefix]
- ...

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

- [repo] - No commits in this period

---
*Report generated on [date] for author: [author]*
```

## Script Reference

### generate-report.py

Primary script for generating complete markdown reports:

```bash
# Basic usage
scripts/generate-report.py --since "1 week ago" ~/projects/*

# Include repos with no activity
scripts/generate-report.py --include-empty --since "1 month ago" ~/work/*

# JSON output for programmatic use
scripts/generate-report.py --json --since "4 days ago" ~/code/*
```

**Output:** Deterministic markdown report (or JSON with `--json` flag).

### git-activity.py

Data collection only (outputs JSON):

```bash
scripts/git-activity.py --since "1 week ago" ~/projects/*
```

See `patterns/git-queries.md` for the underlying git commands.

## Related Skills

- `git-scripting` - Safe git command patterns for scripts