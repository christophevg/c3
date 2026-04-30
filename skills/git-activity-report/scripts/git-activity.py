#!/usr/bin/env python3
"""
Git Activity Report Generator

Collects git activity from multiple repositories and outputs structured data
for the git-activity-report skill.

Usage:
  git-activity.py [--author AUTHOR] [--since SINCE] PATHS...

Example:
  git-activity.py --author "John Doe" --since "1 week ago" ~/projects/*
"""

import argparse
import glob
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


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
  # Exclude patterns for noise files
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
      # Skip noise files
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
      # Keep as-is if glob doesn't match (might be single file)
      paths.append(os.path.expanduser(arg))
  return paths


def main():
  parser = argparse.ArgumentParser(
    description="Collect git activity from multiple repositories"
  )
  parser.add_argument(
    "--author", "-a",
    help="Git author name (defaults to first repo's config)"
  )
  parser.add_argument(
    "--since", "-s",
    default="1 week ago",
    help='Time period (e.g., "1 week ago", "4 days ago", "midnight")'
  )
  parser.add_argument(
    "paths",
    nargs="+",
    help="Paths to check (supports globs)"
  )
  parser.add_argument(
    "--include-empty",
    action="store_true",
    help="Include repos with no activity"
  )

  args = parser.parse_args()

  # Expand paths
  paths = expand_paths(args.paths)

  # Filter to git repos
  git_paths = [p for p in paths if is_git_repo(p)]

  if not git_paths:
    print(json.dumps({"error": "No git repositories found", "paths": paths}))
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

  # Output structured data
  output = {
    "period": args.since,
    "author": author,
    "date": datetime.now().strftime("%Y-%m-%d"),
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


if __name__ == "__main__":
  main()