# Git Query Patterns

Patterns for extracting commit data from git repositories.

## Get Commit List

```bash
git -C "<path>" log \
  --author="<author>" \
  --since="<period>" \
  --no-merges \
  --pretty=format:"%h|%ad|%s" \
  --date=short
```

**Output format:** `hash|date|subject`

## Get File Statistics

```bash
git -C "<path>" log \
  --author="<author>" \
  --since="<period>" \
  --no-merges \
  --numstat \
  --pretty=format:"COMMIT:%h"
```

**Output format:**
```
COMMIT:abc123
added   deleted    filename
added   deleted    filename
```

## Get Commit Details

```bash
git -C "<path>" show \
  --no-patch \
  --format="%h|%ad|%an|%s%n%b" \
  <commit-hash>
```

## Period Values

| Period Flag | `--since` Value |
|-------------|-----------------|
| `--today` | `midnight` or `2026-04-15 00:00:00` |
| `--yesterday` | `yesterday midnight` |
| `--week` | `1 week ago` |
| `--month` | `1 month ago` |

## Get Current Author

```bash
git -C "<path>" config user.name
```

## Check if Git Repository

```bash
git -C "<path>" rev-parse --git-dir 2>/dev/null
```

Returns exit code 0 if valid git repo, non-zero otherwise.

## Noise File Patterns

Files to exclude from statistics:

```bash
# Exclude patterns for file counting
package-lock.json
yarn.lock
pnpm-lock.yaml
*.min.js
*.min.css
*.generated.*
dist/*
build/*
node_modules/*
```

## Filtering Commits

**Exclude merge commits:**
```bash
--no-merges
# or
--pretty=format:"%h %P" | awk 'NF==2 {print}'  # single parent only
```

**Filter by author:**
```bash
--author="$(git config user.name)"
```

## Aggregating Statistics

**Count commits per project:**
```bash
git -C "<path>" log \
  --author="<author>" \
  --since="<period>" \
  --no-merges \
  --oneline | wc -l
```

**Sum lines changed:**
```bash
git -C "<path>" log \
  --author="<author>" \
  --since="<period>" \
  --no-merges \
  --numstat \
  --pretty=format:"" | \
  awk '{added+=$1; deleted+=$2} END {print added, deleted}'
```

**Count unique files:**
```bash
git -C "<path>" log \
  --author="<author>" \
  --since="<period>" \
  --no-merges \
  --name-only \
  --pretty=format:"" | \
  sort -u | \
  grep -v -E "(package-lock|yarn.lock|\.min\.)" | \
  wc -l
```