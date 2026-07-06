#!/usr/bin/env python3
"""
Claude Code Skill Usage Analytics

Analyzes Claude Code logs to detect which skills and agents are used.
Can be run periodically to track usage patterns.

Usage:
  python skill-usage.py                    # Analyze all logs
  python skill-usage.py --last 30          # Last 30 days
  python skill-usage.py --project yoker    # Specific project
  python skill-usage.py --report            # Generate markdown report
"""

import json
import os
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Optional
import argparse


def find_claude_dir() -> Path:
  """Find the Claude Code configuration directory."""
  home = Path.home()
  claude_dir = home / ".claude"
  if not claude_dir.exists():
    raise FileNotFoundError(f"Claude directory not found: {claude_dir}")
  return claude_dir


def find_log_files(claude_dir: Path, project: Optional[str] = None, last_days: Optional[int] = None) -> list[Path]:
  """Find all JSONL log files."""
  projects_dir = claude_dir / "projects"
  if not projects_dir.exists():
    return []

  log_files = []
  cutoff_date = None

  if last_days:
    cutoff_date = datetime.now() - timedelta(days=last_days)

  for project_dir in projects_dir.iterdir():
    if not project_dir.is_dir():
      continue

    project_name = project_dir.name.replace("-Users-xtof-Workspace-", "").replace("-Users-", "")

    # Filter by project if specified
    if project and project.lower() not in project_name.lower():
      continue

    for log_file in project_dir.glob("*.jsonl"):
      if cutoff_date:
        # Check file modification time
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        if mtime < cutoff_date:
          continue
      log_files.append(log_file)

  return log_files


def parse_log_file(log_file: Path) -> tuple[Counter, Counter, Counter]:
  """Parse a single log file and extract skill/agent/tool usage."""
  skill_counts = Counter()
  agent_counts = Counter()
  tool_counts = Counter()

  try:
    with open(log_file, 'r') as f:
      for line in f:
        try:
          entry = json.loads(line.strip())

          # Extract skill invocations
          if 'message' in entry and 'content' in entry['message']:
            content = entry['message']['content']
            if isinstance(content, list):
              for item in content:
                if isinstance(item, dict):
                  # Skill invocations via Skill tool
                  if item.get('type') == 'tool_use' and item.get('name') == 'Skill':
                    skill_name = item.get('input', {}).get('skill', 'unknown')
                    skill_counts[skill_name] += 1

                  # Agent invocations
                  if item.get('type') == 'tool_use' and item.get('name') == 'Agent':
                    agent_type = item.get('input', {}).get('subagent_type', 'unknown')
                    agent_counts[agent_type] += 1

                  # All tool usage
                  if item.get('type') == 'tool_use':
                    tool_name = item.get('name', 'unknown')
                    tool_counts[tool_name] += 1
        except json.JSONDecodeError:
          continue
        except Exception:
          continue

  except Exception as e:
    print(f"Warning: Error reading {log_file}: {e}", file=sys.stderr)

  return skill_counts, agent_counts, tool_counts


def find_available_skills(skills_dir: Path) -> list[str]:
  """Find all available skills from the skills directory."""
  skills = []
  if not skills_dir.exists():
    return skills

  for skill_dir in skills_dir.iterdir():
    if skill_dir.is_dir():
      # Check if it has a skill.md file
      skill_md = skill_dir / "skill.md"
      if skill_md.exists():
        skills.append(skill_dir.name)

  return sorted(skills)


def find_available_agents(agents_dir: Path) -> list[str]:
  """Find all available agents from the agents directory."""
  agents = []
  if not agents_dir.exists():
    return agents

  for agent_file in agents_dir.glob("*.md"):
    # Read frontmatter to get agent name
    try:
      with open(agent_file, 'r') as f:
        content = f.read()
        if content.startswith('---'):
          # Parse frontmatter
          end = content.find('---', 3)
          if end != -1:
            frontmatter = content[3:end]
            for line in frontmatter.split('\n'):
              if line.startswith('name:'):
                name = line.split(':', 1)[1].strip()
                agents.append(name)
                break
    except:
      pass

  return sorted(agents)


def analyze_usage(claude_dir: Path, c3_dir: Path, project: Optional[str] = None, last_days: Optional[int] = None) -> dict:
  """Analyze skill and agent usage across all logs."""

  # Find log files
  log_files = find_log_files(claude_dir, project, last_days)

  # Parse all logs
  total_skills = Counter()
  total_agents = Counter()
  total_tools = Counter()
  files_analyzed = 0

  for log_file in log_files:
    skills, agents, tools = parse_log_file(log_file)
    total_skills.update(skills)
    total_agents.update(agents)
    total_tools.update(tools)
    files_analyzed += 1

  # Find available skills and agents
  available_skills = find_available_skills(c3_dir / "skills")
  available_agents = find_available_agents(c3_dir / "agents")

  # Normalize skill/agent names (handle c3: prefix)
  # c3: prefix is 3 characters, so slice from index 3
  used_skills = set()
  for skill in total_skills.keys():
    if skill.startswith("c3:"):
      used_skills.add(skill)
      used_skills.add(skill[3:])  # Remove "c3:" (3 chars)
    else:
      used_skills.add(skill)
      used_skills.add(f"c3:{skill}")  # Add "c3:" prefix

  used_agents = set()
  for agent in total_agents.keys():
    if agent.startswith("c3:"):
      used_agents.add(agent)
      used_agents.add(agent[3:])  # Remove "c3:" (3 chars)
    else:
      used_agents.add(agent)
      used_agents.add(f"c3:{agent}")  # Add "c3:" prefix

  # Determine unused skills and agents
  unused_skills = [s for s in available_skills if s not in used_skills]
  unused_agents = [a for a in available_agents if a not in used_agents]

  # Add c3: prefix to skills for comparison
  all_used_skills = set()
  for skill in used_skills:
    if skill.startswith("c3:"):
      all_used_skills.add(skill)
    else:
      all_used_skills.add(f"c3:{skill}")

  return {
    'skills': dict(total_skills.most_common()),
    'agents': dict(total_agents.most_common()),
    'tools': dict(total_tools.most_common()),
    'available_skills': available_skills,
    'available_agents': available_agents,
    'unused_skills': unused_skills,
    'unused_agents': unused_agents,
    'files_analyzed': files_analyzed,
    'total_invocations': sum(total_skills.values()) + sum(total_agents.values()),
  }


def print_report(analysis: dict, show_tools: bool = False):
  """Print a formatted report to stdout."""

  print("=" * 70)
  print("CLAUDE CODE USAGE ANALYTICS")
  print("=" * 70)
  print(f"Files analyzed: {analysis['files_analyzed']}")
  print(f"Total invocations: {analysis['total_invocations']}")
  print()

  # Skills used
  print("SKILLS USED")
  print("-" * 70)
  if analysis['skills']:
    for skill, count in sorted(analysis['skills'].items(), key=lambda x: -x[1]):
      print(f"  {skill}: {count}")
  else:
    print("  No skill invocations found")
  print(f"\nTotal unique skills used: {len(analysis['skills'])}")
  print()

  # Agents used
  print("AGENTS USED")
  print("-" * 70)
  if analysis['agents']:
    for agent, count in sorted(analysis['agents'].items(), key=lambda x: -x[1]):
      print(f"  {agent}: {count}")
  else:
    print("  No agent invocations found")
  print(f"\nTotal unique agents used: {len(analysis['agents'])}")
  print()

  # Tools used (optional)
  if show_tools:
    print("TOOLS USED")
    print("-" * 70)
    top_tools = sorted(analysis['tools'].items(), key=lambda x: -x[1])[:20]
    for tool, count in top_tools:
      print(f"  {tool}: {count}")
    print(f"\nTotal unique tools used: {len(analysis['tools'])}")
    print()

  # Unused skills
  print("UNUSED SKILLS")
  print("-" * 70)
  if analysis['unused_skills']:
    for skill in analysis['unused_skills']:
      print(f"  {skill}")
  else:
    print("  All skills have been used")
  print(f"\nUnused: {len(analysis['unused_skills'])} / {len(analysis['available_skills'])} skills")
  print()

  # Unused agents
  print("UNUSED AGENTS")
  print("-" * 70)
  if analysis['unused_agents']:
    for agent in analysis['unused_agents']:
      print(f"  {agent}")
  else:
    print("  All agents have been used")
  print(f"\nUnused: {len(analysis['unused_agents'])} / {len(analysis['available_agents'])} agents")


def generate_markdown_report(analysis: dict, output_file: Path):
  """Generate a markdown report file."""

  with open(output_file, 'w') as f:
    f.write("# Claude Code Usage Analytics Report\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    f.write("## Summary\n\n")
    f.write(f"- **Files analyzed:** {analysis['files_analyzed']}\n")
    f.write(f"- **Total invocations:** {analysis['total_invocations']}\n")
    f.write(f"- **Skills used:** {len(analysis['skills'])} / {len(analysis['available_skills'])}\n")
    f.write(f"- **Agents used:** {len(analysis['agents'])} / {len(analysis['available_agents'])}\n\n")

    # Skills used
    f.write("## Skills Used\n\n")
    f.write("| Skill | Count |\n")
    f.write("|-------|-------|\n")
    for skill, count in sorted(analysis['skills'].items(), key=lambda x: -x[1]):
      f.write(f"| {skill} | {count} |\n")
    f.write("\n")

    # Agents used
    f.write("## Agents Used\n\n")
    f.write("| Agent | Count |\n")
    f.write("|-------|-------|\n")
    for agent, count in sorted(analysis['agents'].items(), key=lambda x: -x[1]):
      f.write(f"| {agent} | {count} |\n")
    f.write("\n")

    # Unused skills
    f.write("## Unused Skills\n\n")
    if analysis['unused_skills']:
      for skill in analysis['unused_skills']:
        f.write(f"- {skill}\n")
    else:
      f.write("All skills have been used.\n")
    f.write("\n")

    # Unused agents
    f.write("## Unused Agents\n\n")
    if analysis['unused_agents']:
      for agent in analysis['unused_agents']:
        f.write(f"- {agent}\n")
    else:
      f.write("All agents have been used.\n")
    f.write("\n")

    # Tools used (top 20)
    f.write("## Top 20 Tools Used\n\n")
    f.write("| Tool | Count |\n")
    f.write("|------|-------|\n")
    top_tools = sorted(analysis['tools'].items(), key=lambda x: -x[1])[:20]
    for tool, count in top_tools:
      f.write(f"| {tool} | {count} |\n")
    f.write("\n")

  print(f"Report written to: {output_file}")


def main():
  parser = argparse.ArgumentParser(description="Claude Code Skill Usage Analytics")
  parser.add_argument("--last", type=int, help="Analyze last N days")
  parser.add_argument("--project", type=str, help="Filter by project name")
  parser.add_argument("--report", type=str, help="Generate markdown report file")
  parser.add_argument("--tools", action="store_true", help="Show tool usage")
  parser.add_argument("--c3-dir", type=str, help="Path to c3 repository (default: current directory)")

  args = parser.parse_args()

  # Find directories
  claude_dir = find_claude_dir()
  c3_dir = Path(args.c3_dir) if args.c3_dir else Path.cwd()

  # Run analysis
  analysis = analyze_usage(claude_dir, c3_dir, args.project, args.last)

  # Output
  print_report(analysis, show_tools=args.tools)

  if args.report:
    output_path = Path(args.report)
    generate_markdown_report(analysis, output_path)


if __name__ == "__main__":
  main()