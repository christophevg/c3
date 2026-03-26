#!/usr/bin/env python

# See: https://code.claude.com/docs/en/statusline

import json, sys, subprocess, os
from pathlib import Path

CYAN, GREEN, YELLOW, RED, RESET = "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[0m"

data = json.load(sys.stdin)
model = data["model"]["display_name"]
pct = int(data.get("context_window", {}).get("used_percentage", 0) or 0)
duration_ms = data.get("cost", {}).get("total_duration_ms", 0) or 0

try:
  session_limit = data["rate_limits"]["five_hour"]["used_percentage"]
  week_limit    = data["rate_limits"]["seven_day"]["used_percentage"]
except KeyError:
  session_limit = 0
  week_limit = 0

env = ""
if Path(".python-version").exists():
  env = Path(".python-version").read_text().strip() + " | "

bar_color = RED if pct >= 90 else YELLOW if pct >= 70 else GREEN
filled = pct // 10
bar = "█" * filled + "░" * (10 - filled)

mins, secs = duration_ms // 60000, (duration_ms % 60000) // 1000

try:
  branch = subprocess.check_output(["git", "branch", "--show-current"], text=True, stderr=subprocess.DEVNULL).strip()
  branch = f"🌿 {branch}" if branch else ""
except:
  branch = ""

print(f"{CYAN}[{model}]{RESET} {bar_color}{bar}{RESET} {pct}% | ⏱️ {mins}m {secs}s | {session_limit}%/{week_limit}%")
print(f"{YELLOW}{env}{RESET}{YELLOW}{branch}{RESET}")

p = Path("local/")
p.mkdir(parents=True, exist_ok=True)
(p / "last-stats.json").write_text(json.dumps(data, indent=2))
