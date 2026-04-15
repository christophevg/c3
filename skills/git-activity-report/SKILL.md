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
2. **Resolve paths**:
   - If `--file FILE`: read paths from file (one per line, `#` comments, blank lines ignored)
   - If glob pattern (`*`): expand via shell
   - Otherwise: use provided paths directly
3. **Validate paths** - Check each is a git repository, skip non-git silently
4. **Get current author** - Run `git config user.name` from first valid repo
5. **Query git logs** - For each valid path, collect commits and stats
6. **Aggregate data** - Combine commits, filter merge commits and noise
7. **Generate narrative** - Write accomplishment-focused summary
8. **Output** - Print formatted markdown to console

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

## Git Commands Reference

See `patterns/git-queries.md` for the exact git commands used.

## Related Skills

- `git-scripting` - Safe git command patterns for scripts