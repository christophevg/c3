# README Maintenance Workflow

This pattern defines how to keep READMEs synchronized with project evolution.

## The Problem

READMEs drift from reality because:
- Version numbers become stale
- Installation instructions break
- Badges show outdated status
- Features added but not documented
- Commands change but README not updated

## Maintenance Approaches

### Approach 1: Manual Updates

**When**: Small projects, infrequent changes.

**Process**:
1. Before each release, review README
2. Check all commands still work
3. Update version numbers
4. Verify badge links
5. Update feature list

**Checklist**:
- [ ] Version numbers current
- [ ] Installation commands work
- [ ] Badge URLs valid
- [ ] Links not broken
- [ ] New features documented

---

### Approach 2: HTML Comment Markers

**When**: Projects with automated sections.

**Purpose**: Isolate sections that can be auto-updated.

**Format**:
```markdown
<!-- PROJECT_STATS_START -->
![Stars](https://img.shields.io/github/stars/user/repo)
![Issues](https://img.shields.io/github/issues/user/repo)
<!-- PROJECT_STATS_END -->

Manual content here remains untouched.
```

**How it works**:
1. Mark sections with unique identifiers
2. Automation reads README
3. Finds markers
4. Updates only content between markers
5. Preserves manual content

**Common markers**:
- `PROJECT_STATS_START/END` - Badge/stats sections
- `INSTALL_START/END` - Installation instructions
- `CHANGELOG_START/END` - Version history

---

### Approach 3: GitHub Actions Sync

**When**: Projects with related repos or automated stats.

**Pull Pattern** (recommended):
- Target repo reads from source via API
- Uses `GITHUB_TOKEN` (no PAT management)
- Always has write access to own repo

**Workflow**:
```yaml
name: Sync README Stats
on:
  schedule:
    - cron: '30 9 * * *'  # Daily at 09:30 UTC
permissions:
  contents: write
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update stats
        run: python scripts/update_readme_stats.py
      - name: Commit changes
        run: |
          git config user.name "github-actions[bot]"
          git commit -am "chore: sync README stats" || exit 0
          git push
```

**Timing**:
- If source updates at 09:00, sync at 09:30+
- Stagger schedules to avoid conflicts

---

### Approach 4: Pre-Commit Hooks

**When**: All projects for quality assurance.

**Hooks**:

**markdownlint** (syntax validation):
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: v0.12.0
    hooks:
      - id: markdownlint-cli2
        args: ['--fix', 'README.md']
```

**lychee** (dead link detection):
```yaml
  - repo: https://github.com/lycheeverse/lychee
    rev: v0.14.0
    hooks:
      - id: lychee
        args: ['README.md']
```

**Badge validation**:
```yaml
  - repo: local
    hooks:
      - id: check-badges
        name: Check badge URLs
        entry: python scripts/check_badges.py
        language: python
        files: 'README.md'
```

---

## Maintenance Checklist by Project Type

### Python Packages

**Before each release**:
- [ ] Version number in badges matches pyproject.toml
- [ ] Installation command works (`pip install package==version`)
- [ ] Quick Start example still works
- [ ] Dependencies listed match current requirements
- [ ] Changelog link points to latest

**Monthly**:
- [ ] Badge URLs still valid
- [ ] Documentation links work
- [ ] Coverage badge reflects current state

---

### Web Applications

**Before each deploy**:
- [ ] Environment variables documented
- [ ] Deployment instructions current
- [ ] Tech stack versions updated
- [ ] Screenshots current

**Monthly**:
- [ ] Deploy badge shows current status
- [ ] Demo links work
- [ ] CI badge accurate

---

### Config/Tools

**After each significant change**:
- [ ] Installation commands work
- [ ] File list matches current structure
- [ ] Configuration options documented
- [ ] Uninstall instructions valid

---

### Documentation Repositories

**Weekly**:
- [ ] Status tracking accurate
- [ ] Links between docs valid
- [ ] TODO.md reflects current tasks
- [ ] Index matches actual files

---

### Jekyll Sites

**After content changes**:
- [ ] Local build works
- [ ] Deployment successful
- [ ] Images load correctly
- [ ] Links valid

---

## Validation Scripts

### Check All Links

```python
#!/usr/bin/env python3
"""Validate all links in README.md"""

import re
import requests

def check_readme_links(readme_path):
    with open(readme_path) as f:
        content = f.read()

    # Find all URLs
    urls = re.findall(r'https?://[^\s\)]+', content)

    broken = []
    for url in urls:
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code >= 400:
                broken.append(url)
        except Exception as e:
            broken.append(f"{url} ({e})")

    if broken:
        print("Broken links:")
        for url in broken:
            print(f"  - {url}")
        return False
    return True

if __name__ == "__main__":
    import sys
    sys.exit(0 if check_readme_links("README.md") else 1)
```

---

### Check Badge Images

```python
#!/usr/bin/env python3
"""Validate all badge images in README.md"""

import re
import requests

def check_badges(readme_path):
    with open(readme_path) as f:
        content = f.read()

    # Find badge URLs (shields.io, badgen, etc.)
    badges = re.findall(r'!\[.*?\]\((https://img\.shields\.io/[^)]+)\)', content)

    broken = []
    for badge_url in badges:
        try:
            response = requests.head(badge_url, timeout=5)
            if response.status_code != 200:
                broken.append(badge_url)
        except Exception as e:
            broken.append(f"{badge_url} ({e})")

    if broken:
        print("Broken badges:")
        for url in broken:
            print(f"  - {url}")
        return False
    return True

if __name__ == "__main__":
    import sys
    sys.exit(0 if check_badges("README.md") else 1)
```

---

### Extract Version from pyproject.toml

```python
#!/usr/bin/env python3
"""Get version from pyproject.toml for README badges"""

import tomllib

def get_version():
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    version = data.get("project", {}).get("version", "unknown")
    print(version)

if __name__ == "__main__":
    get_version()
```

---

## Common Maintenance Tasks

### Update Version in Badges

**Manual approach**:
1. Find version in pyproject.toml
2. Search README for old version
3. Replace with new version

**Automated approach**:
```python
import re

def update_version_in_readme(new_version):
    with open("README.md", "r+") as f:
        content = f.read()

        # Update PyPI badge
        content = re.sub(
            r'pip install \w+==[\d.]+',
            f'pip install package=={new_version}',
            content
        )

        f.seek(0)
        f.write(content)
        f.truncate()
```

---

### Update Badge URLs

**When moving to new CI system, coverage service, etc.**

```python
def update_badge_urls(old_domain, new_domain):
    with open("README.md", "r+") as f:
        content = f.read()
        content = content.replace(old_domain, new_domain)
        f.seek(0)
        f.write(content)
        f.truncate()
```

---

### Regenerate Table of Contents

```python
def generate_toc():
    with open("README.md") as f:
        lines = f.readlines()

    toc = ["## Table of Contents\n\n"]
    for line in lines:
        if line.startswith("## ") and not "Table of Contents" in line:
            section = line[3:].strip()
            anchor = section.lower().replace(" ", "-")
            toc.append(f"- [{section}](#{anchor})\n")

    # Insert after title
    # ... implementation
```

---

## Best Practices Summary

1. **Review before releases** - Always check README before publishing
2. **Use markers** - Isolate auto-updated sections with HTML comments
3. **Automate validation** - Pre-commit hooks for links and badges
4. **Keep it current** - Better to update frequently than let it rot
5. **Test commands** - Actually run the installation commands
6. **Link validation** - Monthly check for dead links
7. **Badge accuracy** - Badges should reflect current state