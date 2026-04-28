# Inbox Folder Script — Detailed Design

**Created:** 2026-04-18
**Last Updated:** 2026-04-18
**Status:** Design Complete, Not Implemented
**Project:** Archiku — AI-Powered Architecture Intelligence
**Purpose:** Detailed specification for the `inbox_folder.py` script that processes files from an inbox folder

---

## Overview

The folder inbox script is the first input channel implementation. It reads files from a designated folder, normalizes them to the unified item format, and manages state by moving processed files to a `processed/` subfolder.

---

## Script Identity

| Property | Value |
|----------|-------|
| Name | `inbox_folder.py` |
| Location | `archiku/scripts/` (or similar) |
| Language | Python (recommended) |
| Input | YAML on stdin |
| Output | YAML on stdout |
| Exit Codes | 0 = success, non-zero = error |

---

## Protocol

### General Behavior

- Accepts YAML on stdin
- Returns YAML on stdout
- Errors go to stderr (human-readable) with non-zero exit code
- Success goes to stdout (YAML) with exit code 0

### Supported Actions

| Action | Purpose |
|--------|---------|
| `fetch_new` | Return unprocessed items from inbox |
| `mark_processed` | Mark items as processed (move to `processed/`) |
| `status` | Return current state summary (optional) |
| `help` | Return usage information (optional) |

---

## Action: `fetch_new`

### Purpose

Read all files from the inbox folder, parse each file's frontmatter and body, normalize to unified item format, and return as a list.

### Input Schema

```yaml
action: fetch_new
source: folder
path: inbox/                    # Optional, defaults to 'inbox/'
```

### Output Schema

```yaml
status: success
source: folder
path: inbox/
items:
  - id: <unique-identifier>
    channel: folder
    author: <from-frontmatter>
    timestamp: <file-modification-time-ISO8601>
    title: <from-frontmatter-or-null>
    body: |
      <body-content-as-markdown>
  - id: <unique-identifier>
    channel: folder
    author: <from-frontmatter>
    timestamp: <file-modification-time-ISO8601>
    title: <from-frontmatter-or-null>
    body: |
      <body-content-as-markdown>
```

### Processing Steps

1. **Read inbox folder**
   - List all files in `path` (default: `inbox/`)
   - Ignore subdirectories (only top-level files)
   - Ignore hidden files (starting with `.`)
   - Ignore files without `.md` extension (optional: configure allowed extensions)

2. **Parse each file**
   - Extract YAML frontmatter (between `---` delimiters)
   - Extract body (content after frontmatter)
   - If no frontmatter: treat entire file as body, set `author: unknown`

3. **Generate ID**
   - Options:
     - Use filename (without extension): `motor-eol.md` → `motor-eol`
     - Generate hash from content: `md5(author + timestamp + body)[:8]`
     - Sequential: `001`, `002`, etc. (based on file order)
   - Recommendation: Use filename as ID (simple, predictable, debuggable)

4. **Extract metadata**
   - `author`: from frontmatter (required in file)
   - `timestamp`: file's last modification time (filesystem `mtime`)
   - `title`: from frontmatter (optional, can be null)
   - `body`: everything after frontmatter, trimmed

5. **Return items**
   - Sort order: oldest first (by timestamp, then filename)
   - If no items: return empty `items: []`

### Example Input

```yaml
action: fetch_new
source: folder
path: inbox/
```

### Example Output

```yaml
status: success
source: folder
path: inbox/
items:
  - id: motor-eol
    channel: folder
    author: Christophe
    timestamp: 2026-04-18T10:30:00Z
    title: null
    body: |
      The Motor library is deprecated as of May 14.
      We need to migrate to PyMongo Async.

      Affected projects:
      - pageable-mongo
      - data-service
  - id: auth-issue
    channel: folder
    author: Sarah
    timestamp: 2026-04-18T11:00:00Z
    title: Authentication vulnerability
    body: |
      Found a session handling issue in the auth module.
      Sessions are not being invalidated properly on logout.
```

### Edge Cases

| Scenario | Behavior |
|----------|----------|
| Empty inbox folder | Return `items: []` with status `success` |
| File has no frontmatter | `author: unknown`, `title: null`, use file content as body |
| File has only frontmatter, no body | `body: ""` (empty string) |
| File has malformed YAML | Return error for that file, continue with others? Or fail entire operation? |
| File is binary/non-text | Skip and warn? Or fail? |
| File is locked/unreadable | Return error with details |
| Path doesn't exist | Return error: `status: error`, `message: "Path not found"` |
| Path is not a directory | Return error: `status: error`, `message: "Path is not a directory"` |

### Design Decision: Malformed Files

**Question:** How to handle files with parsing errors?

**Option A: Fail entire operation**
- Pro: Agent knows something is wrong, can report to user
- Con: One bad file blocks all others

**Option B: Skip bad files, report in output**
- Pro: Processing continues, user can fix specific files
- Con: Agent might miss information

**Option C: Return partial results with warnings**
- Pro: Agent gets valid items, also gets error details
- Con: More complex protocol

**Recommendation:** Option C — return valid items with a `warnings` field:

```yaml
status: success
source: folder
path: inbox/
items:
  - id: motor-eol
    channel: folder
    author: Christophe
    timestamp: 2026-04-18T10:30:00Z
    body: |
      ...
warnings:
  - file: malformed-file.md
    error: "Invalid YAML frontmatter: line 3: mapping values not allowed"
```

---

## Action: `mark_processed`

### Purpose

Mark specified items as processed by moving their corresponding files to a `processed/` subfolder.

### Input Schema

```yaml
action: mark_processed
source: folder
path: inbox/
processed_ids:
  - <id-1>
  - <id-2>
  - ...
```

### Output Schema

```yaml
status: success
processed_count: 2
processed_ids:
  - <id-1>
  - <id-2>
skipped_ids: []           # IDs that were not found
errors: []                # Files that couldn't be moved
```

### Processing Steps

1. **For each ID in `processed_ids`:**
   - Find corresponding file in inbox folder
   - If not found: add to `skipped_ids`
   - If found: move to `processed/` subfolder

2. **Create `processed/` subfolder if it doesn't exist**

3. **Handle file naming in processed folder:**
   - Keep original filename
   - If file with same name exists in `processed/`: append timestamp or counter
   - Option: `motor-eol.md` → `motor-eol-2026-04-18T14-00-00.md`
   - Option: `motor-eol.md` → `motor-eol-001.md` (counter)

4. **Return summary**

### Example Input

```yaml
action: mark_processed
source: folder
path: inbox/
processed_ids:
  - motor-eol
  - auth-issue
```

### Example Output

```yaml
status: success
processed_count: 2
processed_ids:
  - motor-eol
  - auth-issue
skipped_ids: []
errors: []
```

### Example Output (with issues)

```yaml
status: partial
processed_count: 2
processed_ids:
  - motor-eol
  - auth-issue
skipped_ids:
  - non-existent-id
errors:
  - id: locked-file
    error: "Permission denied: file is locked by another process"
```

### Edge Cases

| Scenario | Behavior |
|----------|----------|
| ID doesn't exist | Add to `skipped_ids`, continue with others |
| File is locked | Add to `errors` with details, continue with others |
| `processed/` folder doesn't exist | Create it automatically |
| File with same name exists in `processed/` | Append timestamp to filename |
| `processed_ids` is empty | Return success with `processed_count: 0` |
| All IDs not found | Return `status: success`, `processed_count: 0`, all in `skipped_ids` |

### Design Decision: What "Processed" Means

**For folder script:** Move to `processed/` subfolder

**Why:**
- Preserves original file for audit
- Keeps inbox clean
- Easy to see what's been processed
- Can recover if needed

**Alternative options:**
- Delete files (more destructive, no audit trail)
- Add `.processed` extension (keeps in same folder, clutter)
- Rename with `.done` suffix (same issue)

---

## Action: `status` (Optional)

### Purpose

Return current state summary without processing anything.

### Input Schema

```yaml
action: status
source: folder
path: inbox/
```

### Output Schema

```yaml
status: success
source: folder
path: inbox/
counts:
  inbox: 5
  processed: 23
oldest_item:
  id: motor-eol
  timestamp: 2026-04-18T10:30:00Z
newest_item:
  id: auth-issue
  timestamp: 2026-04-18T14:00:00Z
```

---

## Action: `help` (Optional)

### Purpose

Return usage information for the script.

### Input Schema

```yaml
action: help
```

### Output Schema

```yaml
status: success
name: inbox_folder
version: 1.0.0
description: Process files from an inbox folder and normalize to unified format
actions:
  - name: fetch_new
    description: Return unprocessed items from inbox
    input_fields:
      - name: action
        required: true
        description: Must be "fetch_new"
      - name: source
        required: true
        description: Must be "folder"
      - name: path
        required: false
        default: "inbox/"
        description: Path to inbox folder
  - name: mark_processed
    description: Mark items as processed
    input_fields:
      - name: action
        required: true
        description: Must be "mark_processed"
      - name: source
        required: true
        description: Must be "folder"
      - name: path
        required: false
        default: "inbox/"
        description: Path to inbox folder
      - name: processed_ids
        required: true
        description: List of item IDs to mark as processed
```

---

## Folder Structure

### Inbox Folder

```
inbox/
├── motor-eol.md           # Unprocessed item
├── auth-issue.md          # Unprocessed item
└── release-date.md        # Unprocessed item
```

### Processed Folder

After `mark_processed` for `motor-eol` and `auth-issue`:

```
inbox/
├── processed/
│   ├── motor-eol.md       # Processed item (original name)
│   └── auth-issue.md      # Processed item (original name)
└── release-date.md        # Still unprocessed
```

### File Naming After Processing

If a file with the same name already exists in `processed/`:

```
processed/
├── motor-eol.md                    # First processed
├── motor-eol-2026-04-18T14-00-00.md # Second time processed (same filename)
└── auth-issue.md
```

**Design Decision:** Append timestamp when filename collision occurs. This preserves history while keeping files identifiable.

---

## Input File Format

### Required Frontmatter

```yaml
---
author: Christophe
---
<body content as markdown>
```

### Optional Frontmatter

```yaml
---
author: Christophe
title: Motor EOL Announcement
timestamp: 2026-04-18T10:30:00Z
---
<body content as markdown>
```

**Note:** `timestamp` in frontmatter overrides file modification time if present. This is useful for backdated entries or when the original timestamp matters more than file metadata.

### No Frontmatter (Fallback)

```markdown
<body content as markdown>
```

Parsed as:
- `author: unknown`
- `title: null`
- `timestamp: <file modification time>`
- `body: <entire file content>`

### Design Decision: Required vs Optional Frontmatter

**Decision:** Only `author` is required in frontmatter. Everything else is optional or derived.

**Rationale:**
- `author` is genuinely new information (cannot be derived)
- `timestamp` can be derived from file metadata
- `title` can be generated by agent
- Keeps files simple for quick dumping

**Future consideration:** Allow configuration to require more fields, or make author also optional with `author: unknown` fallback.

---

## ID Generation

### Options

| Method | Example | Pros | Cons |
|--------|---------|------|------|
| Filename | `motor-eol.md` → `motor-eol` | Predictable, debuggable, user-controlled | May not be unique if user copies files |
| Content hash | `md5(author+body)[:8]` → `a3f2c891` | Guaranteed unique, content-based | Not human-readable, changes if content changes |
| Sequential | `001`, `002`, etc. | Simple, ordered | Not stable across runs, depends on order |
| Timestamp-based | `2026-04-18-motor-eol` | Ordered, includes context | Long, may not be unique |

### Recommendation

**Use filename as ID** (without extension):
- Simple and predictable
- User can control naming for clarity
- Easy to debug: `motor-eol.md` → ID `motor-eol`
- Collision handling: If duplicate filenames, append counter or timestamp

**Collision handling:**
```yaml
status: error
error: "Duplicate ID 'motor-eol' from files: motor-eol.md, motor-eol-copy.md"
message: "Filenames must be unique within inbox folder"
```

---

## Error Handling

### Error Output Format

```yaml
status: error
error: <error-type>
message: <human-readable message>
details:
  - <additional-information>
```

### Error Types

| Error Type | Description |
|------------|-------------|
| `invalid_action` | Unknown or missing action |
| `invalid_input` | YAML parsing failed or required fields missing |
| `path_not_found` | Specified path doesn't exist |
| `path_not_directory` | Specified path is not a directory |
| `permission_denied` | Cannot read/write files |
| `parse_error` | Failed to parse one or more files |
| `internal_error` | Unexpected error in script |

### Example Error Output

```yaml
status: error
error: parse_error
message: "Failed to parse 2 files"
details:
  - file: malformed.md
    line: 3
    error: "Invalid YAML: mapping values not allowed here"
  - file: another.md
    line: 1
    error: "Frontmatter must start with '---'"
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (including partial success with warnings) |
| 1 | Input error (invalid YAML, missing required fields) |
| 2 | Filesystem error (path not found, permission denied) |
| 3 | Parse error (one or more files couldn't be parsed) |
| 99 | Internal error (unexpected exception) |

---

## Configuration (Future Consideration)

The script could accept a configuration file or CLI arguments for:

| Setting | Default | Description |
|---------|---------|-------------|
| `inbox_path` | `inbox/` | Path to inbox folder |
| `processed_path` | `inbox/processed/` | Path to processed folder |
| `file_extensions` | `.md` | Allowed file extensions |
| `require_frontmatter` | `true` | Require YAML frontmatter in files |
| `author_required` | `true` | Require author in frontmatter |
| `timestamp_field` | `mtime` | Use `mtime` or `ctime` for timestamp |

---

## Testing Considerations

### Test Cases

1. **Empty inbox** — Returns empty items list
2. **Single valid file** — Returns one item with correct fields
3. **Multiple files** — Returns items sorted by timestamp
4. **File without frontmatter** — Falls back to defaults
5. **File with only frontmatter** — Returns empty body
6. **File with malformed YAML** — Returns error with details
7. **Hidden file** — Skips files starting with `.`
8. **Subdirectory** — Skips directories
9. **mark_processed all items** — Moves all to processed/
10. **mark_processed non-existent ID** — Returns in skipped_ids
11. **Path not found** — Returns error
12. **Permission denied** — Returns error
13. **Collision in processed folder** — Appends timestamp

---

## Implementation Notes

### Language Recommendation

**Python** is recommended for:
- Built-in YAML support (`pyyaml`)
- Cross-platform file handling
- Easy testing
- Integration with other Archiku tools (Python-based)

### Key Dependencies

```python
import yaml          # YAML parsing
import os            # File operations
import sys            # stdin/stdout
import datetime      # Timestamp handling
from pathlib import Path  # Path operations
```

### Pseudocode Structure

```python
def main():
    # Read YAML from stdin
    input_yaml = sys.stdin.read()
    input_data = yaml.safe_load(input_yaml)
    
    # Validate action
    action = input_data.get('action')
    if action == 'fetch_new':
        result = handle_fetch_new(input_data)
    elif action == 'mark_processed':
        result = handle_mark_processed(input_data)
    elif action == 'status':
        result = handle_status(input_data)
    elif action == 'help':
        result = handle_help()
    else:
        result = error_response('invalid_action', f'Unknown action: {action}')
    
    # Write YAML to stdout
    print(yaml.dump(result, default_flow_style=False))
    
    # Exit with appropriate code
    sys.exit(0 if result.get('status') in ['success', 'partial'] else 1)
```

---

## Open Questions

1. **Should the script support batch operations?**
   - E.g., `batch` action that does fetch + mark in one call
   - Reduces round trips but more complex

2. **Should processed files be compressed/archived?**
   - Long-term: move to dated archive folders
   - E.g., `processed/2026/04/18/motor-eol.md`

3. **Should the script support file watching?**
   - Continuous mode that watches for new files
   - Emits items as they appear

4. **How to handle very large files?**
   - Streaming the body instead of loading into memory
   - Truncation with warning?

5. **Should the script support filtering?**
   - By author, date range, filename pattern
   - Reduces data transfer for agent

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2026-04-18 | 1.0 | Initial design document |

---

## See Also

- [Inbox & Unified I/O Design](inbox-unified-io-design.md) — Overall architecture
- [Plan Learn Skill](../skills/plan-learn/SKILL.md) — Agent skill that processes unified format