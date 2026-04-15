#!/usr/bin/env python3
"""
PyEnv Preference Learning

Stores and retrieves user preferences for Python environment management.
"""

import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class PyEnvPreferences:
    """User preferences for PyEnv environment management."""

    # Version preferences
    default_python: Optional[str] = None  # e.g., "3.12.7" or "LTS"
    preferred_versions: list[str] = None  # Commonly used versions

    # Naming preferences
    naming_style: str = "project-name"  # "project-name" or ".venv"

    # Project type preferences
    package_project_detected: bool = False

    # Auto-activation
    auto_activation_enabled: bool = True

    # Tool virtualenvs created
    tool_venvs: list[str] = None

    # Metadata
    created: str = None
    updated: str = None

    def __post_init__(self):
        if self.preferred_versions is None:
            self.preferred_versions = []
        if self.tool_venvs is None:
            self.tool_venvs = []
        if self.created is None:
            self.created = datetime.now().isoformat()
        if self.updated is None:
            self.updated = datetime.now().isoformat()


def get_memory_path(project_name: Optional[str] = None) -> Path:
    """Get the path to preferences file."""
    if project_name:
        # Project memory
        return Path(".claude/memory/pyenv-preferences.md")
    else:
        # User global memory
        return Path.home() / ".claude" / "projects" / "global" / "pyenv-preferences.json"


def load_preferences(project: bool = True) -> PyEnvPreferences:
    """
    Load preferences from memory.

    Args:
        project: If True, load project-specific preferences. If False, load global.

    Returns:
        PyEnvPreferences object
    """
    path = get_memory_path(project_name="project" if project else None)

    if path.exists():
        if path.suffix == ".json":
            data = json.loads(path.read_text())
            return PyEnvPreferences(**data)
        else:
            # Handle .md format
            content = path.read_text()
            # Parse frontmatter and content
            if "---" in content:
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    # Parse YAML frontmatter (simplified)
                    return parse_md_preferences(content)

    return PyEnvPreferences()


def save_preferences(prefs: PyEnvPreferences, project: bool = True) -> None:
    """
    Save preferences to memory.

    Args:
        prefs: Preferences to save
        project: If True, save project-specific. If False, save global.
    """
    prefs.updated = datetime.now().isoformat()
    path = get_memory_path(project_name="project" if project else None)

    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix == ".md":
        # Save in markdown format with frontmatter
        content = format_md_preferences(prefs)
        path.write_text(content)
    else:
        # Save as JSON
        path.write_text(json.dumps(asdict(prefs), indent=2))


def parse_md_preferences(content: str) -> PyEnvPreferences:
    """Parse preferences from markdown format."""
    # Simple parsing - extract key values
    prefs = PyEnvPreferences()

    for line in content.split('\n'):
        if line.startswith('default_python:'):
            prefs.default_python = line.split(':', 1)[1].strip().strip('"')
        elif line.startswith('naming_style:'):
            prefs.naming_style = line.split(':', 1)[1].strip().strip('"')
        elif line.startswith('auto_activation_enabled:'):
            prefs.auto_activation_enabled = line.split(':', 1)[1].strip().lower() == 'true'

    return prefs


def format_md_preferences(prefs: PyEnvPreferences) -> str:
    """Format preferences as markdown."""
    return f"""---
name: pyenv-preferences
description: Python environment preferences for this project
type: project
---

# PyEnv Preferences

**Default Python**: {prefs.default_python or 'not set'}
**Naming Style**: {prefs.naming_style}
**Auto-Activation**: {'enabled' if prefs.auto_activation_enabled else 'disabled'}

## Preferred Versions

{chr(10).join(f'- {v}' for v in prefs.preferred_versions) if prefs.preferred_versions else 'None'}

## Tool Virtualenvs

{chr(10).join(f'- {v}' for v in prefs.tool_venvs) if prefs.tool_venvs else 'None'}

## Metadata

- Created: {prefs.created}
- Updated: {prefs.updated}
"""


def get_effective_preferences() -> PyEnvPreferences:
    """
    Get effective preferences by merging project and global preferences.

    Project preferences take precedence over global preferences.
    """
    global_prefs = load_preferences(project=False)
    project_prefs = load_preferences(project=True)

    # Project overrides global
    if project_prefs.default_python:
        global_prefs.default_python = project_prefs.default_python
    if project_prefs.naming_style:
        global_prefs.naming_style = project_prefs.naming_style
    if project_prefs.preferred_versions:
        global_prefs.preferred_versions = project_prefs.preferred_versions

    return global_prefs


def record_version_choice(version: str, project: bool = True) -> None:
    """Record a version choice for future reference."""
    prefs = load_preferences(project=project)

    if not prefs.default_python:
        prefs.default_python = version

    if version not in prefs.preferred_versions:
        prefs.preferred_versions.append(version)

    save_preferences(prefs, project=project)


def record_naming_choice(style: str, project: bool = True) -> None:
    """Record naming style preference."""
    prefs = load_preferences(project=project)
    prefs.naming_style = style
    save_preferences(prefs, project=project)


def record_tool_venv(tool_name: str, project: bool = True) -> None:
    """Record that a tool virtualenv was created."""
    prefs = load_preferences(project=project)
    if tool_name not in prefs.tool_venvs:
        prefs.tool_venvs.append(tool_name)
    save_preferences(prefs, project=project)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage PyEnv preferences")
    parser.add_argument("--show", action="store_true", help="Show current preferences")
    parser.add_argument("--reset", action="store_true", help="Reset preferences")
    parser.add_argument("--set-version", help="Set default Python version")
    parser.add_argument("--set-naming", choices=["project-name", ".venv"], help="Set naming style")

    args = parser.parse_args()

    if args.show:
        prefs = get_effective_preferences()
        print(json.dumps(asdict(prefs), indent=2))
    elif args.reset:
        save_preferences(PyEnvPreferences())
        print("✓ Preferences reset")
    elif args.set_version:
        record_version_choice(args.set_version)
        print(f"✓ Default Python set to {args.set_version}")
    elif args.set_naming:
        record_naming_choice(args.set_naming)
        print(f"✓ Naming style set to {args.set_naming}")
    else:
        parser.print_help()