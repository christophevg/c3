#!/usr/bin/env python3
"""
PyEnv Skill Main Script

Interactive environment management with preference learning.
"""

import json
import sys
from pathlib import Path
from typing import Optional

# Import local modules
import detect
import create_env
import preferences


def get_version_options(installed_versions: list[str]) -> list[dict]:
    """Get version options for user selection."""
    # Categorize versions - filter out environment paths
    latest = None
    lts = None
    compat = None
    other = []

    for v in installed_versions:
        # Skip environment paths (e.g., "3.11.12/envs/incubator")
        if "/envs/" in v:
            continue
        if not v.startswith("3."):
            continue
        parts = v.split(".")
        if len(parts) >= 2:
            major_minor = f"{parts[0]}.{parts[1]}"
            if major_minor == "3.13":
                latest = v
            elif major_minor == "3.12":
                lts = v
            elif major_minor == "3.10":
                compat = v
            else:
                other.append(v)

    options = []
    if latest:
        options.append({"value": latest, "label": f"{latest} (latest stable)"})
    if lts:
        options.append({"value": lts, "label": f"{lts} (LTS - recommended)"})
    if compat:
        options.append({"value": compat, "label": f"{compat} (maximum compatibility)"})
    for v in other[:2]:  # Add up to 2 other versions
        options.append({"value": v, "label": f"{v} (installed)"})
    options.append({"value": "other", "label": "Other version..."})

    return options


def get_naming_options() -> list[dict]:
    """Get naming style options."""
    return [
        {
            "value": ".venv",
            "label": ".venv (standard, project-local)",
            "description": "Official Python convention, IDE auto-detection, hidden by default"
        },
        {
            "value": "project-name",
            "label": "{project-name} (pyenv-virtualenv style)",
            "description": "Centralized in ~/.pyenv/versions/, auto-activation with pyenv-virtualenv-init"
        }
    ]


def format_detection_for_dialog(det: dict) -> str:
    """Format detection results for display in dialog."""
    lines = []

    if not det["pyenv_installed"]:
        lines.append("✗ pyenv is not installed")
        lines.append("Install from: https://pyenv.run")
        return '\n'.join(lines)

    lines.append("✓ pyenv installed")

    if det["python_version_file"]:
        lines.append(f"✓ Python version: {det['python_version_file']}")
    else:
        lines.append("○ No .python-version file")

    if det["is_package_project"]:
        lines.append("✓ Package project detected (.pypi-template)")

    if det["current_env"]:
        lines.append(f"✓ Active environment: {det['current_env']}")

    if det["auto_activation_configured"]:
        lines.append("✓ Auto-activation configured")

    return '\n'.join(lines)


def get_dialog_context(det: dict) -> dict:
    """Get context for interactive dialog."""
    return {
        "detection": det,
        "formatted_detection": format_detection_for_dialog(det),
        "version_options": get_version_options(det["installed_versions"]),
        "naming_options": get_naming_options(),
        "prefs": preferences.get_effective_preferences()
    }


def print_context_for_skill(context: dict) -> None:
    """Print context in a format the skill can use for AskUserQuestion."""
    print("---PYENV_CONTEXT---")
    print(json.dumps(context, indent=2))
    print("---END_CONTEXT---")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="PyEnv skill context generator")
    parser.add_argument("--detect", action="store_true", help="Run detection and output context")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.detect:
        # Run detection
        det = detect.detect_environment()

        # Get context for dialog
        context = get_dialog_context(det)

        if args.json:
            print(json.dumps(context, indent=2))
        else:
            print_context_for_skill(context)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()