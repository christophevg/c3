#!/usr/bin/env python3
"""Validate C3 agents and skills against BLUEPRINT.md.

Enforcement model:
- Global checks apply to every definition file: forbidden vocabulary (§1.7.3),
  duplicate H1 sections (fenced code blocks stripped first), cross-reference
  resolution (c3:<name>, agents/<name>.md, skills/<name>/ paths).
- Template checks (frontmatter, sections, tool grants, trigger class) apply
  strictly to files in KNOWN_YOKER. Other files are template-exempt until
  their migration batch promotes them; coverage prints on every run.
"""

import re
import sys
from pathlib import Path
from typing import NamedTuple


class Finding(NamedTuple):
  file: str
  status: str
  message: str


YOKER_TOOLS = {
  "existence", "read", "list", "search", "skill",
  "write", "update", "mkdir", "file",
  "git", "github", "make",
  "agent", "send_message", "release_agent", "sleep",
  "notify", "webfetch", "websearch",
}

ALL_AGENTS = {
  "api-architect", "bug-fixer", "business-analyst", "code-reviewer",
  "end-user-documenter", "functional-analyst", "project-manager",
  "python-developer", "release-manager", "researcher",
  "security-engineer", "testing-engineer", "ui-ux-designer",
}

ALLOWED_EXTERNAL_REFS = {
  "plan", "wsjf", "project", "analysis-integration", "lessons-learned",
  "transcribe-session", "website-manage", "python", "python-project",
  "python-testing", "baseweb", "vue", "vue-form-generator", "vuetify",
  "textual", "rich", "fire", "ollama", "pymongo", "readme", "documentation",
  "naming", "quart-webapp", "api-design", "prepare-for-exam",
  "help", "init", "compact", "loop", "schedule",
}

KNOWN_YOKER = {
  "agents": {
    "api-architect", "bug-fixer", "business-analyst", "code-reviewer",
    "end-user-documenter", "functional-analyst", "project-manager",
    "python-developer", "release-manager", "researcher",
    "security-engineer", "testing-engineer", "ui-ux-designer",
  },
  "skills": {
    "api-design", "project", "project-feature", "project-manage",
    "project-handle-pr", "project-post-merge", "project-review",
    "project-status", "project-todo-refine",
    "analysis-integration", "baseweb", "documentation", "fire",
    "lessons-learned", "naming", "ollama", "plan",
    "prepare-for-exam", "pymongo", "python", "python-comments",
    "python-project", "python-testing", "quart-webapp", "readme",
    "research", "rich",
    "textual", "transcribe-session", "vue", "vue-form-generator",
    "vuetify-v1", "vuetify-v2", "vuetify-v3", "vuetify-v4", "wsjf",
  },
}

FORBIDDEN_PATTERNS = [
  ("legacy tool Bash(", r"\bBash\("),
  ("legacy tool Task(", r"\bTask\("),
  ("legacy dispatch subagent_type", r"\bsubagent_type\b"),
  ("claude vocabulary", r"\bclaude\b"),
  (".claude paths", r"\.claude"),
  ("CLAUDE docs", r"\bCLAUDE\b"),
  (".claude-plugin manifest", r"\.claude-plugin"),
]

AGENT_SECTIONS = ["Persona", "Engaged when", "How I work", "I deliver", "I never"]

def strip_code_blocks(text: str) -> str:
  """Remove fenced code blocks from markdown text."""
  lines = []
  in_fence = False
  for line in text.split("\n"):
    if line.lstrip().startswith("```"):
      in_fence = not in_fence
      continue
    if in_fence:
      continue
    lines.append(line)
  return "\n".join(lines)


def strip_inline_code(text: str) -> str:
  return re.sub(r"`[^`\n]*`", "", text)


def parse_frontmatter(content: str):
  """Return (frontmatter_text or None, body)."""
  match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", content, re.DOTALL)
  if not match:
    return None, content
  return match.group(1), match.group(2)


def parse_fm_fields(fm_text: str) -> dict:
  fields = {}
  for line in fm_text.split("\n"):
    if not line or line.startswith((" ", "\t", "#")):
      continue
    if ":" not in line:
      continue
    key, value = line.split(":", 1)
    fields[key.strip()] = value.strip()
  return fields


def check_forbidden_vocab(path_str: str, content: str, findings: list):
  body = strip_inline_code(strip_code_blocks(content))
  for label, pattern in FORBIDDEN_PATTERNS:
    hit_lines = [i for i, line in enumerate(body.split("\n"), 1)
                 if re.search(pattern, line, re.IGNORECASE)]
    if not hit_lines:
      continue
    shown = ", ".join(f"L{i}" for i in hit_lines[:4])
    more = f" (+{len(hit_lines) - 4} more)" if len(hit_lines) > 4 else ""
    findings.append(Finding(path_str, "ERROR",
      f"forbidden vocabulary [{label}]: {shown}{more}"))


def check_duplicate_headers(path_str: str, content: str, findings: list):
  body = strip_code_blocks(content)
  seen = {}
  for i, line in enumerate(body.split("\n"), 1):
    m = re.match(r"^(#{1,3}) (.+)$", line)
    if not m:
      continue
    title = m.group(2).strip()
    if title in seen:
      findings.append(Finding(path_str, "ERROR",
        f"duplicate heading '{title}' at L{i} (first at L{seen[title]})"))
    else:
      seen[title] = i


def check_cross_references(path_str: str, content: str, skill_names: set,
                           findings: list):
  body = strip_inline_code(strip_code_blocks(content))
  refs = set()
  refs.update(("skill", m) for m in re.findall(r"\bc3:([a-z0-9-]+)", body))
  refs.update(("agent", m) for m in re.findall(r"\bagents/([a-z0-9-]+)\.md\b", body))
  for kind, name in sorted(refs):
    if kind == "agent":
      if name not in ALL_AGENTS:
        findings.append(Finding(path_str, "ERROR",
          f"unresolvable agent reference: {name}"))
    elif name not in skill_names and name not in ALL_AGENTS \
        and name not in ALLOWED_EXTERNAL_REFS:
      findings.append(Finding(path_str, "ERROR",
        f"unresolvable reference: c3:{name} (or skills/{name}/)"))


def check_tool_grants(path_str: str, fm_text: str, findings: list):
  in_tools = False
  for line in fm_text.split("\n"):
    if re.match(r"^tools\s*:", line):
      in_tools = True
      continue
    if in_tools:
      stripped = line.strip()
      if not stripped or stripped.startswith("#"):
        continue
      if stripped.startswith("- "):
        tool = stripped[2:].strip()
        if tool not in YOKER_TOOLS:
          findings.append(Finding(path_str, "ERROR",
            f"non-Yoker tool in frontmatter grants: '{tool}'"))
        continue
      in_tools = False


def check_agent_template(path_str: str, fm_text: str, body: str, findings: list):
  fields = parse_fm_fields(fm_text)
  for field in ("name", "description", "color", "tools"):
    if field not in fields:
      findings.append(Finding(path_str, "ERROR",
        f"missing frontmatter field: {field}"))
  check_tool_grants(path_str, fm_text, findings)
  if fields.get("name") and fields["name"] != Path(path_str).stem:
    findings.append(Finding(path_str, "ERROR",
      f"name '{fields['name']}' does not match filename '{Path(path_str).stem}'"))
  for section in AGENT_SECTIONS:
    if not re.search(rf"^# {re.escape(section)}\s*$", body, re.MULTILINE):
      findings.append(Finding(path_str, "ERROR",
        f"missing required section: # {section}"))


def check_skill_template(path_str: str, body: str, fields: dict,
                         dir_name: str, findings: list):
  for field in ("name", "description", "type"):
    if field not in fields:
      findings.append(Finding(path_str, "ERROR",
        f"missing frontmatter field: {field}"))
  stype = fields.get("type", "").strip().strip("'\"")
  if stype not in ("workflow", "knowledge"):
    findings.append(Finding(path_str, "ERROR",
      "missing/invalid 'type: workflow|knowledge'"))
    stype = None
  if fields.get("name") and fields["name"] != dir_name:
    findings.append(Finding(path_str, "ERROR",
      f"name '{fields['name']}' does not match directory '{dir_name}'"))
  if fields.get("description") in (None, ""):
    findings.append(Finding(path_str, "ERROR",
      "description must be a non-empty trigger surface"))
  if stype == "workflow":
    if re.search(r"auto-?trigger|triggers automatically|fires automatically",
                 body, re.IGNORECASE):
      findings.append(Finding(path_str, "ERROR",
        "workflow skill must never auto-trigger"))
  if not re.search(r"^##+ ", body, re.MULTILINE):
    findings.append(Finding(path_str, "ERROR", "no '## ' section headers"))
  if not re.search(r"^## (Related|Reference|Sub-skills)\b", body, re.MULTILINE):
    findings.append(Finding(path_str, "ERROR", "missing '## Related' section (Related/Reference/Sub-skills)"))


def validate_agent(path: Path, findings: list):
  content = path.read_text()
  path_str = str(path)
  check_forbidden_vocab(path_str, content, findings)
  check_duplicate_headers(path_str, content, findings)
  fm_text, _ = parse_frontmatter(content)
  if path.stem not in KNOWN_YOKER["agents"]:
    return
  if fm_text is None:
    findings.append(Finding(path_str, "ERROR", "missing YAML frontmatter"))
    return
  clean_body = strip_code_blocks(parse_frontmatter(content)[1])
  check_agent_template(path_str, fm_text, clean_body, findings)


def validate_skill(path: Path, skill_names: set, findings: list):
  content = path.read_text()
  path_str = str(path)
  dir_name = path.parent.name
  check_forbidden_vocab(path_str, content, findings)
  check_duplicate_headers(path_str, content, findings)
  check_cross_references(path_str, content, skill_names, findings)
  fm_text, raw_body = parse_frontmatter(content)
  if dir_name not in KNOWN_YOKER["skills"]:
    return
  if fm_text is None:
    findings.append(Finding(path_str, "ERROR", "missing YAML frontmatter"))
    return
  fields = parse_fm_fields(fm_text)
  check_skill_template(path_str, strip_code_blocks(raw_body), fields,
                       dir_name, findings)


def main() -> int:
  repo_root = Path(__file__).parent.parent
  agents_dir = repo_root / "agents"
  skills_dir = repo_root / "skills"

  agent_files = sorted(agents_dir.glob("*.md")) if agents_dir.exists() else []
  skill_files = sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.exists() else []
  # reference/bundled markdown: vocabulary scan applies too
  skill_ref_files = sorted(
    p for p in skills_dir.rglob("*.md") if p.name != "SKILL.md"
  ) if skills_dir.exists() else []
  skill_names = {p.parent.name for p in skill_files}
  findings = []

  for path in agent_files:
    validate_agent(path, findings)
  for path in skill_files:
    validate_skill(path, skill_names, findings)
  for path in skill_ref_files:
    content = path.read_text()
    check_forbidden_vocab(str(path), content, findings)

  errors = [f for f in findings if f.status == "ERROR"]
  warns = [f for f in findings if f.status == "WARN"]

  print(f"Validated {len(agent_files)} agents, {len(skill_files)} skills.")
  print(f"Blueprint template coverage: {len(KNOWN_YOKER['agents'])}/{len(ALL_AGENTS)} agents, "
        f"{len(KNOWN_YOKER['skills'])} skills strict")
  for f in sorted(findings, key=lambda x: (x.file, x.message)):
    if f.status == "ERROR":
      print(f"\033[91m✗ {f.file}: {f.message}\033[0m")
    else:
      print(f"\033[93m⚠ {f.file}: {f.message}\033[0m")
  print()
  print(f"Results: {len(errors)} errors, {len(warns)} warnings")
  return 1 if errors else 0


if __name__ == "__main__":
  sys.exit(main())