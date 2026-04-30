#!/usr/bin/env python3
"""
Git Activity Report Generator

Generates a deterministic markdown report from git activity data.
Uses the same formatting rules every time for consistent output.

Usage:
  generate-report.py [--author AUTHOR] [--since SINCE] PATHS...

Output:
  Complete markdown report ready for display or email.
"""

import argparse
import glob
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


# Conventional commit prefixes for grouping
PREFIX_GROUPS = [
  "feat", "feature",
  "fix", "bugfix",
  "docs", "documentation",
  "refactor",
  "test", "tests",
  "chore",
  "style",
  "perf", "performance",
  "build",
  "ci",
]


def is_git_repo(path: str) -> bool:
  """Check if path is a git repository."""
  try:
    result = subprocess.run(
      ["git", "-C", path, "rev-parse", "--git-dir"],
      capture_output=True,
      text=True
    )
    return result.returncode == 0
  except Exception:
    return False


def get_author(path: str) -> str:
  """Get git author name from a repository."""
  result = subprocess.run(
    ["git", "-C", path, "config", "user.name"],
    capture_output=True,
    text=True
  )
  return result.stdout.strip()


def get_commits(path: str, author: str, since: str) -> list[dict]:
  """Get commits from a repository."""
  result = subprocess.run(
    [
      "git", "-C", path, "log",
      f"--author={author}",
      f"--since={since}",
      "--no-merges",
      "--pretty=format:%h|%ad|%s",
      "--date=short"
    ],
    capture_output=True,
    text=True
  )

  commits = []
  for line in result.stdout.strip().split("\n"):
    if "|" in line:
      parts = line.split("|", 2)
      if len(parts) == 3:
        commits.append({
          "hash": parts[0],
          "date": parts[1],
          "subject": parts[2]
        })
  return commits


def get_stats(path: str, author: str, since: str) -> dict:
  """Get file and line statistics for a repository."""
  exclude_patterns = [
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    ".min.js", ".min.css", ".generated.",
    "dist/", "build/", "node_modules/"
  ]

  result = subprocess.run(
    [
      "git", "-C", path, "log",
      f"--author={author}",
      f"--since={since}",
      "--no-merges",
      "--numstat",
      "--pretty=format:"
    ],
    capture_output=True,
    text=True
  )

  added = 0
  deleted = 0
  files = set()

  for line in result.stdout.strip().split("\n"):
    if not line.strip():
      continue
    parts = line.split("\t")
    if len(parts) == 3:
      a, d, filename = parts
      if any(p in filename for p in exclude_patterns):
        continue
      if a != "-":
        added += int(a)
      if d != "-":
        deleted += int(d)
      files.add(filename)

  return {
    "added": added,
    "deleted": deleted,
    "files": len(files)
  }


def expand_paths(path_args: list[str]) -> list[str]:
  """Expand path arguments, handling globs."""
  paths = []
  for arg in path_args:
    expanded = glob.glob(os.path.expanduser(arg))
    if expanded:
      paths.extend(expanded)
    else:
      paths.append(os.path.expanduser(arg))
  return paths


def parse_commit_subject(subject: str) -> tuple[str, str]:
  """
  Parse a commit subject into prefix and description.

  Returns:
    (prefix, description) where prefix may be empty
  """
  # Check for conventional commit format: "prefix: description" or "prefix(scope): description"
  for prefix in PREFIX_GROUPS:
    if subject.lower().startswith(prefix + ":"):
      return prefix, subject[len(prefix)+1:].strip()
    if subject.lower().startswith(prefix + "("):
      # Find closing paren
      idx = subject.find("):")
      if idx > 0:
        return prefix, subject[idx+2:].strip()

  return "", subject


def format_accomplishment(subject: str) -> str:
  """
  Format a commit subject as an accomplishment.

  - Strip conventional prefixes
  - Convert to present tense (simple heuristic)
  - Capitalize first letter
  """
  prefix, description = parse_commit_subject(subject)

  # Simple present tense conversion
  desc = description
  if desc:
    # Capitalize first letter
    desc = desc[0].upper() + desc[1:]

  return desc


def group_commits_by_prefix(commits: list[dict]) -> dict[str, list[str]]:
  """Group commits by their conventional commit prefix."""
  groups = defaultdict(list)

  for commit in commits:
    prefix, description = parse_commit_subject(commit["subject"])
    accomplishment = format_accomplishment(commit["subject"])
    groups[prefix if prefix else "other"].append(accomplishment)

  return dict(groups)


def generate_project_narrative(commits: list[dict], project_name: str) -> str:
  """
  Generate a deterministic narrative for a project.

  Groups commits by prefix and lists accomplishments.
  """
  if not commits:
    return "No activity in this period."

  groups = group_commits_by_prefix(commits)

  # Count by type
  feat_count = len(groups.get("feat", [])) + len(groups.get("feature", []))
  fix_count = len(groups.get("fix", [])) + len(groups.get("bugfix", []))
  docs_count = len(groups.get("docs", [])) + len(groups.get("documentation", []))
  refactor_count = len(groups.get("refactor", []))
  test_count = len(groups.get("test", [])) + len(groups.get("tests", []))
  chore_count = len(groups.get("chore", []))

  # Build summary sentence
  parts = []
  if feat_count > 0:
    parts.append(f"{feat_count} new feature{'s' if feat_count > 1 else ''}")
  if fix_count > 0:
    parts.append(f"{fix_count} fix{'es' if fix_count > 1 else ''}")
  if docs_count > 0:
    parts.append(f"{docs_count} documentation update{'s' if docs_count > 1 else ''}")
  if refactor_count > 0:
    parts.append(f"{refactor_count} refactoring change{'s' if refactor_count > 1 else ''}")
  if test_count > 0:
    parts.append(f"{test_count} test improvement{'s' if test_count > 1 else ''}")
  if chore_count > 0:
    parts.append(f"{chore_count} maintenance task{'s' if chore_count > 1 else ''}")

  other_count = len(groups.get("other", []))
  if other_count > 0 and not parts:
    parts.append(f"{other_count} change{'s' if other_count > 1 else ''}")

  if parts:
    summary = f"Activity includes {', '.join(parts)}."
  else:
    summary = f"{len(commits)} commits."

  return summary


def generate_accomplishment_list(commits: list[dict], max_items: int = 15) -> list[str]:
  """
  Generate a list of accomplishments from commits.

  Groups similar items, limits output, strips prefixes.
  """
  groups = group_commits_by_prefix(commits)

  # Order: feat, fix, docs, refactor, test, chore, other
  order = ["feat", "feature", "fix", "bugfix", "docs", "documentation",
           "refactor", "test", "tests", "chore", "style", "perf", "performance",
           "build", "ci", "other"]

  accomplishments = []

  for prefix in order:
    if prefix in groups:
      for acc in groups[prefix][:max_items - len(accomplishments)]:
        if len(accomplishments) >= max_items:
          break
        accomplishments.append(acc)
    if len(accomplishments) >= max_items:
      break

  return accomplishments


def generate_report(author: str, since: str, date: str, projects: list[dict],
                   empty_repos: list[str], totals: dict) -> str:
  """Generate the complete markdown report."""

  lines = []

  # Header
  lines.append(f"# Activity Report: {since}")
  lines.append("")
  lines.append(f"**Period:** {since}")
  lines.append(f"**Author:** {author}")
  lines.append("")

  # Summary
  lines.append("## Summary")
  lines.append("")

  # Generate overall summary
  total_projects = len(projects)
  active_projects = [p for p in projects if len(p["commits"]) > 0]

  # Find top projects by commits
  sorted_projects = sorted(projects, key=lambda p: len(p["commits"]), reverse=True)
  top_projects = sorted_projects[:5]

  if top_projects:
    top_names = [p["name"] for p in top_projects]
    lines.append(f"Activity across {total_projects} projects. Most active: {', '.join(top_names[:3])}.")
  else:
    lines.append(f"No activity in this period.")
  lines.append("")

  # Projects section
  lines.append("## Projects")
  lines.append("")

  # Sort projects by commit count (descending)
  for project in sorted_projects:
    if len(project["commits"]) == 0:
      continue

    name = project["name"]
    commits = project["commits"]
    stats = project["stats"]

    lines.append(f"### {name}")
    lines.append("")

    # Narrative
    narrative = generate_project_narrative(commits, name)
    lines.append(narrative)
    lines.append("")

    # Stats line
    lines.append(f"**Commits:** {len(commits)} | **Files:** {stats['files']} | **Lines:** +{stats['added']}/-{stats['deleted']}")
    lines.append("")

    # Accomplishments
    accomplishments = generate_accomplishment_list(commits)
    for acc in accomplishments:
      lines.append(f"- {acc}")

    lines.append("")

  # Totals
  lines.append("## Totals")
  lines.append("")
  lines.append("| Metric | Value |")
  lines.append("|--------|-------|")
  lines.append(f"| **Total Commits** | {totals['commits']} |")
  lines.append(f"| **Total Files** | {totals['files']} |")
  lines.append(f"| **Lines Added** | +{totals['added']} |")
  lines.append(f"| **Lines Removed** | -{totals['deleted']} |")
  lines.append("")

  # No Activity
  if empty_repos:
    lines.append("## No Activity")
    lines.append("")
    for repo in sorted(empty_repos):
      lines.append(f"- {repo} - No commits in this period")
    lines.append("")

  # Footer
  lines.append("---")
  lines.append(f"*Report generated on {date} for author: {author}*")

  return "\n".join(lines)


def main():
  parser = argparse.ArgumentParser(
    description="Generate a deterministic git activity report"
  )
  parser.add_argument("--author", "-a", help="Git author name")
  parser.add_argument("--since", "-s", default="1 week ago", help="Time period")
  parser.add_argument("paths", nargs="+", help="Paths to check")
  parser.add_argument("--include-empty", action="store_true", help="Include repos with no activity")
  parser.add_argument("--json", action="store_true", help="Output JSON instead of markdown")

  args = parser.parse_args()

  # Expand paths
  paths = expand_paths(args.paths)

  # Filter to git repos
  git_paths = [p for p in paths if is_git_repo(p)]

  if not git_paths:
    print("No git repositories found", file=sys.stderr)
    sys.exit(1)

  # Get author
  author = args.author or get_author(git_paths[0])

  # Collect data
  projects = []
  empty_repos = []

  for path in git_paths:
    repo_name = os.path.basename(path)
    commits = get_commits(path, author, args.since)

    if commits:
      stats = get_stats(path, author, args.since)
      projects.append({
        "name": repo_name,
        "path": path,
        "commits": commits,
        "stats": stats
      })
    elif args.include_empty:
      empty_repos.append(repo_name)

  # Calculate totals
  total_commits = sum(len(p["commits"]) for p in projects)
  total_files = sum(p["stats"]["files"] for p in projects)
  total_added = sum(p["stats"]["added"] for p in projects)
  total_deleted = sum(p["stats"]["deleted"] for p in projects)

  date = datetime.now().strftime("%Y-%m-%d")

  if args.json:
    # Output JSON for programmatic use
    output = {
      "period": args.since,
      "author": author,
      "date": date,
      "projects": projects,
      "empty_repos": empty_repos,
      "totals": {
        "commits": total_commits,
        "files": total_files,
        "added": total_added,
        "deleted": total_deleted
      }
    }
    print(json.dumps(output, indent=2))
  else:
    # Output markdown report
    totals = {
      "commits": total_commits,
      "files": total_files,
      "added": total_added,
      "deleted": total_deleted
    }
    report = generate_report(author, args.since, date, projects, empty_repos, totals)
    print(report)


if __name__ == "__main__":
  main()