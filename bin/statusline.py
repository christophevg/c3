#!/usr/bin/env python

# See: https://code.claude.com/docs/en/statusline

import json, sys, subprocess
from pathlib import Path

CYAN, GREEN, YELLOW, RED, RESET = "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[0m"

data = json.load(sys.stdin)
model = data["model"]["display_name"]
pct = int(data.get("context_window", {}).get("used_percentage", 0) or 0)
duration_ms = data.get("cost", {}).get("total_duration_ms", 0) or 0

bar_color = RED if pct >= 90 else YELLOW if pct >= 70 else GREEN
filled = pct // 10
bar = "█" * filled + "░" * (10 - filled)

mins, secs = duration_ms // 60000, (duration_ms % 60000) // 1000

line1_stats = [
  f"{CYAN}{model}:{RESET} {bar_color}{bar}{RESET} {pct}%",
  f"⏱️ {mins}m {secs}s"
]

line2_stats = []

if Path(".python-version").exists():
  line2_stats.append(f"🐍 {Path('.python-version').read_text().strip()}")

try:
  branch = subprocess.check_output(["git", "branch", "--show-current"], text=True, stderr=subprocess.DEVNULL).strip()
  if branch:
    line2_stats.append(f"🌿 {branch}")
except:
  pass

cwd = Path.cwd().name
if cwd:
  line2_stats.append(f"📁 {cwd}")

print(" | ".join(line1_stats))
if line2_stats:
  print(" | ".join(f"{YELLOW}{s}{RESET}" for s in line2_stats))

# p = Path("local/")
# p.mkdir(parents=True, exist_ok=True)
# (p / "last-stats.json").write_text(json.dumps(data, indent=2))
