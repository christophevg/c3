---
name: git-activity-report
description: |
  Generate human-readable git activity summaries focused on accomplishments. Use when user asks to "report git activity", "show work done", or wants a summary of commits. Examples: "/git-activity-report --week", "report git activity for today on paths in file repos.txt", "what did I do this week".
type: workflow
---

# Git Activity Report

Human-readable activity summaries from git repositories — reports focused
on accomplishments, suitable for stakeholders unfamiliar with the projects.

# Inputs

```
/git-activity-report [path...] [--file FILE] [--today|--yesterday|--week|--month]
```

- Period defaults to `--week`; paths default to the current directory.
- Paths come as arguments, a file (`--file repos.txt`), or globs.
- Natural language works: "what did I do today", "this week's work on
  incubator", "report git activity for today on paths in repos.txt".

## Period map

| Flag | git `--since` value |
|------|---------------------|
| `--today` | `midnight` |
| `--yesterday` | `1 day ago` (bounded to that day) |
| `--week` | `1 week ago` |
| `--month` | `1 month ago` |

## Path-file format

`#` comments and blank lines ignored; one repo path per line.

# Procedure

1. Parse paths and period from the invocation.
2. Run the bundled generator (Yoker tool-call form; `<skill-base>` is shown
   in the skill-invocation header):

   ```
   make: no — the generator is a script, invoke via the project runtime:
   uv run <skill-base>/scripts/generate-report.py --since "<period>" <paths...>
   ```

   Flags: `--include-empty` (report repos without activity), `--json`
   (machine-readable). The script handles path expansion, repo validation,
   author detection, statistics, and deterministic formatting.

3. Deliver the markdown report as-is — it is deterministic: same input,
   same report.

## Filtering rules

Excluded from statistics: merge commits (multi-parent), lock files
(`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`), minified files
(`*.min.js`, `*.min.css`), generated artifacts (`*.generated.*`, `dist/`,
`build/`). Author filter: only the current git user's commits.

## Output structure (deterministic)

```markdown
# Activity Report: [period]

**Period / Author**

## Summary
Activity across N projects. Most active: [projects].

## Projects
### [Project]
Activity includes X features, Y fixes, Z documentation updates.
**Commits:** X | **Files:** Y | **Lines:** +A/-B
- [Accomplishment, conventional prefix stripped]

## Totals
| Metric | Value |
|--------|-------|
| Total Commits / Files / Lines +A/-B |

## No Activity
- [repo] — no commits in this period
```

## Efficiency recipe

Generate once, reuse for both formats (report + HTML email):

1. Run `generate-report.py` once, keep the markdown.
2. Pipe the captured markdown through `<c3-base>/bin/md-to-html.py` for
   the HTML variant (email styling for tables, headers, lists).
3. `<c3-base>` is the parent of `<skill-base>/../..`.

## Helper scripts (in `<skill-base>/scripts/`)

- `generate-report.py` — full markdown (or JSON) report
- `git-activity.py` — data collection only (JSON)

# Deliverables

- A deterministic, accomplishment-focused markdown report; optional JSON.

# Related

- `c3:git-scripting` — safe git-command patterns for any wrapper scripts