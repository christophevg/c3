#!/usr/bin/env python
import json, sys, subprocess, os
from pathlib import Path

CYAN, GREEN, YELLOW, RED, RESET = "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[0m"

data = json.load(sys.stdin)
model = data["model"]["display_name"]

pct = int(data.get("context_window", {}).get("used_percentage", 0) or 0)
duration_ms = data.get("cost", {}).get("total_duration_ms", 0) or 0
env = ""
if Path(".python-version").exists():
  env = Path(".python-version").read_text().strip()

bar_color = RED if pct >= 90 else YELLOW if pct >= 70 else GREEN
filled = pct // 10
bar = "█" * filled + "░" * (10 - filled)

mins, secs = duration_ms // 60000, (duration_ms % 60000) // 1000

try:
  branch = subprocess.check_output(["git", "branch", "--show-current"], text=True, stderr=subprocess.DEVNULL).strip()
  branch = f" | 🌿 {branch}" if branch else ""
except:
  branch = ""

print(f"({YELLOW}{env}{RESET}) {CYAN}[{model}]{RESET} {bar_color}{bar}{RESET} {pct}% | ⏱️ {mins}m {secs}s")
