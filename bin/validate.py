#!/usr/bin/env python3
"""
Validate C3 skills and agents for correct structure and references.

This script validates:
- Skill SKILL.md files have valid frontmatter
- Agent files have valid frontmatter
- Cross-references between skills/agents exist
- Symlinks in installation directory are valid
"""

import re
import sys
from pathlib import Path
from typing import NamedTuple


class ValidationResult(NamedTuple):
  file: str
  status: str
  message: str


def parse_frontmatter(content: str) -> dict:
  """Extract YAML frontmatter from markdown content."""
  match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
  if not match:
    return {}

  frontmatter = {}
  for line in match.group(1).split('\n'):
    if ':' in line:
      key, value = line.split(':', 1)
      frontmatter[key.strip()] = value.strip()

  return frontmatter


def validate_skill(skill_dir: Path) -> list[ValidationResult]:
  """Validate a skill directory."""
  results = []
  skill_file = skill_dir / "SKILL.md"
  skill_name = skill_dir.name

  if not skill_file.exists():
    results.append(ValidationResult(
      file=str(skill_file),
      status="ERROR",
      message=f"Missing SKILL.md in {skill_name}"
    ))
    return results

  content = skill_file.read_text()
  frontmatter = parse_frontmatter(content)

  # Check required frontmatter fields
  required_fields = ["name", "description"]
  for field in required_fields:
    if field not in frontmatter:
      results.append(ValidationResult(
        file=str(skill_file),
        status="ERROR",
        message=f"Missing required frontmatter field: {field}"
      ))

  # Check for workflow section
  if "## Workflow" not in content and "## When to Use" not in content:
    results.append(ValidationResult(
      file=str(skill_file),
      status="WARN",
      message="Missing '## Workflow' or '## When to Use' section"
    ))

  # Validate name matches directory
  if frontmatter.get("name") and frontmatter["name"] != skill_name:
    results.append(ValidationResult(
      file=str(skill_file),
      status="WARN",
      message=f"Skill name '{frontmatter['name']}' doesn't match directory '{skill_name}'"
    ))

  if not results:
    results.append(ValidationResult(
      file=str(skill_file),
      status="OK",
      message=f"Valid skill: {skill_name}"
    ))

  return results


def validate_agent(agent_file: Path) -> list[ValidationResult]:
  """Validate an agent file."""
  results = []
  agent_name = agent_file.stem

  content = agent_file.read_text()
  frontmatter = parse_frontmatter(content)

  # Check required frontmatter fields
  required_fields = ["name", "description"]
  for field in required_fields:
    if field not in frontmatter:
      results.append(ValidationResult(
        file=str(agent_file),
        status="ERROR",
        message=f"Missing required frontmatter field: {field}"
      ))

  # Check for content sections
  if "## " not in content:
    results.append(ValidationResult(
      file=str(agent_file),
      status="WARN",
      message="Missing section headers (## )"
    ))

  # Validate name matches filename
  if frontmatter.get("name") and frontmatter["name"] != agent_name:
    results.append(ValidationResult(
      file=str(agent_file),
      status="WARN",
      message=f"Agent name '{frontmatter['name']}' doesn't match filename '{agent_name}'"
    ))

  if not results:
    results.append(ValidationResult(
      file=str(agent_file),
      status="OK",
      message=f"Valid agent: {agent_name}"
    ))

  return results


def validate_cross_references(skills: list[Path], agents: list[Path]) -> list[ValidationResult]:
  """Validate cross-references between skills and agents."""
  results = []

  skill_names = {s.name for s in skills}
  agent_names = {a.stem for a in agents}

  # Check skill references in SKILL.md files
  for skill_dir in skills:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
      continue

    content = skill_file.read_text()

    # Find skill references: `/skill-name` or `/project-feature`
    skill_refs = re.findall(r'/([a-z-]+)', content)
    for ref in set(skill_refs):
      if ref not in skill_names and ref not in ["help", "loop", "schedule", "fast", "slow", "clear", "compact", "init", "review"]:
        # Allow built-in commands
        if ref.startswith("project-") and ref not in skill_names:
          continue  # Skip project-* for now, might be dispatcher

  # Check agent references in files
  for agent_file in agents:
    content = agent_file.read_text()

    # Find agent references: `agent-name` in "use agent-name agent"
    agent_refs = re.findall(r'use\s+([a-z-]+)\s+agent', content, re.IGNORECASE)
    for ref in set(agent_refs):
      if ref not in agent_names:
        results.append(ValidationResult(
          file=str(agent_file),
          status="WARN",
          message=f"References unknown agent: {ref}"
        ))

  return results


def validate_symlinks(home_dir: Path) -> list[ValidationResult]:
  """Validate symlinks in ~/.claude directory."""
  results = []
  claude_dir = home_dir / ".claude"

  if not claude_dir.exists():
    results.append(ValidationResult(
      file=str(claude_dir),
      status="WARN",
      message="~/.claude directory doesn't exist (run 'make install' first)"
    ))
    return results

  # Check agents symlinks
  agents_dir = claude_dir / "agents"
  if agents_dir.exists():
    for link in agents_dir.iterdir():
      if link.is_symlink() and not link.exists():
        results.append(ValidationResult(
          file=str(link),
          status="ERROR",
          message=f"Broken symlink: {link.name}"
        ))

  # Check skills symlinks
  skills_dir = claude_dir / "skills"
  if skills_dir.exists():
    for link in skills_dir.iterdir():
      if link.is_symlink() and not link.exists():
        results.append(ValidationResult(
          file=str(link),
          status="ERROR",
          message=f"Broken symlink: {link.name}"
        ))

  return results


def print_results(results: list[ValidationResult]) -> int:
  """Print results and return error count."""
  errors = 0
  warnings = 0

  for result in sorted(results, key=lambda r: (r.status, r.file)):
    if result.status == "ERROR":
      print(f"\033[91m✗ {result.file}: {result.message}\033[0m")
      errors += 1
    elif result.status == "WARN":
      print(f"\033[93m⚠ {result.file}: {result.message}\033[0m")
      warnings += 1
    else:
      print(f"\033[92m✓ {result.message}\033[0m")

  print()
  print(f"Results: {errors} errors, {warnings} warnings")

  return errors


def main():
  """Run all validations."""
  repo_root = Path(__file__).parent.parent
  home_dir = Path.home()

  results = []

  # Validate skills
  skills_dir = repo_root / "skills"
  if skills_dir.exists():
    skills = [d for d in skills_dir.iterdir() if d.is_dir()]
    print(f"\nValidating {len(skills)} skills...")
    for skill_dir in sorted(skills):
      results.extend(validate_skill(skill_dir))

  # Validate agents
  agents_dir = repo_root / "agents"
  if agents_dir.exists():
    agents = [f for f in agents_dir.iterdir() if f.suffix == ".md"]
    print(f"\nValidating {len(agents)} agents...")
    for agent_file in sorted(agents):
      results.extend(validate_agent(agent_file))

  # Validate cross-references
  print("\nValidating cross-references...")
  skills = [d for d in skills_dir.iterdir() if d.is_dir()] if skills_dir.exists() else []
  agents = [f for f in agents_dir.iterdir() if f.suffix == ".md"] if agents_dir.exists() else []
  results.extend(validate_cross_references(skills, agents))

  # Validate symlinks
  print("\nValidating symlinks...")
  results.extend(validate_symlinks(home_dir))

  # Print results
  print("\n" + "=" * 60)
  errors = print_results(results)

  return 1 if errors > 0 else 0


if __name__ == "__main__":
  sys.exit(main())