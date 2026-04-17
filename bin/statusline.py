#!/usr/bin/env python

# Status line generator for Claude Code
# See: https://code.claude.com/docs/en/statusline

import json
import subprocess
from pathlib import Path

# Color codes
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"


def get_context_bar(percentage):
  """Generate a visual progress bar for context window usage."""
  bar_color = RED if percentage >= 90 else YELLOW if percentage >= 70 else GREEN
  filled = percentage // 10
  return bar_color, "█" * filled + "░" * (10 - filled)


def format_duration(duration_ms):
  """Convert milliseconds to minutes and seconds."""
  mins = duration_ms // 60000
  secs = (duration_ms % 60000) // 1000
  return mins, secs


def get_git_branch():
  """Get current git branch name, or None if not in a repo."""
  try:
    return subprocess.check_output(
      ["git", "branch", "--show-current"],
      text=True,
      stderr=subprocess.DEVNULL
    ).strip() or None
  except (subprocess.CalledProcessError, FileNotFoundError):
    return None


def get_pyenv_version():
  """Get Python version from .python-version file, or None if not present."""
  python_version_file = Path(".python-version")
  if not python_version_file.exists():
    return None

  lines = python_version_file.read_text().strip().splitlines()
  if not lines:
    return None

  version = lines[0]
  if len(lines) > 1:
    version += f" (+{len(lines) - 1})"
  return version


def main():
  data = json.load(sys.stdin)

  # Extract model info
  model = data["model"]["display_name"]

  # Extract context window usage
  context_pct = int(data.get("context_window", {}).get("used_percentage", 0) or 0)
  bar_color, bar = get_context_bar(context_pct)

  # Extract duration
  duration_ms = data.get("cost", {}).get("total_duration_ms", 0) or 0
  mins, secs = format_duration(duration_ms)

  # Build line 1: model, context bar, duration
  line1_stats = [
    f"{CYAN}{model}:{RESET} {bar_color}{bar}{RESET} {context_pct}%",
    f"⏱️ {mins}m {secs}s"
  ]

  # Build line 2: folder, branch, pyenv (in that order)
  line2_stats = []

  # Current folder
  cwd = Path.cwd().name
  if cwd:
    line2_stats.append(f"📁 {cwd}")

  # Git branch
  branch = get_git_branch()
  if branch:
    line2_stats.append(f"🌿 {branch}")

  # Pyenv environment
  pyenv_version = get_pyenv_version()
  if pyenv_version:
    line2_stats.append(f"🐍 {pyenv_version}")

  # Output
  print(" | ".join(line1_stats))
  if line2_stats:
    print(" | ".join(f"{YELLOW}{s}{RESET}" for s in line2_stats))


import sys

if __name__ == "__main__":
  main()