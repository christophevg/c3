#!/usr/bin/env python3
"""
Version management script for C3 plugin.

Usage:
    python version.py <command>

Commands:
    current     Show current version
    bump        Bump version (requires --part major|minor|patch)
    release     Prepare for release (bump version, update docs)

Options:
    --part      Version part to bump (major, minor, patch)
    --dry-run   Show what would change without making changes
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import date


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


def read_plugin_json():
    """Read plugin.json."""
    plugin_path = get_project_root() / ".claude-plugin" / "plugin.json"
    with open(plugin_path) as f:
        return json.load(f)


def write_plugin_json(data):
    """Write plugin.json."""
    plugin_path = get_project_root() / ".claude-plugin" / "plugin.json"
    with open(plugin_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def read_changelog():
    """Read CHANGELOG.md."""
    changelog_path = get_project_root() / "CHANGELOG.md"
    with open(changelog_path) as f:
        return f.read()


def write_changelog(content):
    """Write CHANGELOG.md."""
    changelog_path = get_project_root() / "CHANGELOG.md"
    with open(changelog_path, "w") as f:
        f.write(content)


def parse_version(version_str):
    """Parse version string into tuple."""
    parts = version_str.split(".")
    return tuple(int(p) for p in parts)


def format_version(version_tuple):
    """Format version tuple as string."""
    return ".".join(str(p) for p in version_tuple)


def bump_version(version_str, part):
    """Bump version by the specified part."""
    major, minor, patch = parse_version(version_str)

    if part == "major":
        return format_version((major + 1, 0, 0))
    elif part == "minor":
        return format_version((major, minor + 1, 0))
    elif part == "patch":
        return format_version((major, minor, patch + 1))
    else:
        raise ValueError(f"Invalid part: {part}")


def update_changelog(new_version):
    """Update CHANGELOG.md with new version."""
    changelog = read_changelog()
    today = date.today().strftime("%Y-%m-%d")

    # Check if there's an [Unreleased] section with content
    unreleased_match = re.search(
        r"## \[Unreleased\]\n\n(###.*?)(?=\n## |\Z)",
        changelog,
        re.DOTALL
    )

    if not unreleased_match:
        print("Warning: No content in [Unreleased] section")
        unreleased_content = ""
    else:
        unreleased_content = unreleased_match.group(1)

    # Create new version section
    new_section = f"## [{new_version}] - {today}\n\n{unreleased_content}"

    # Replace [Unreleased] with new version
    if "## [Unreleased]\n\n" in changelog:
        new_changelog = changelog.replace(
            "## [Unreleased]\n\n",
            f"## [Unreleased]\n\n### Added\n\n*Nothing yet*\n\n{new_section}\n\n",
            1
        )
    else:
        # Insert after the header
        header_end = changelog.find("## [Unreleased]") + len("## [Unreleased]")
        new_changelog = (
            changelog[:header_end] +
            f"\n\n### Added\n\n*Nothing yet*\n\n{new_section}\n\n" +
            changelog[header_end:]
        )

    return new_changelog


def cmd_current(args):
    """Show current version."""
    plugin = read_plugin_json()
    print(f"Current version: {plugin['version']}")


def cmd_bump(args):
    """Bump version."""
    if not args.part:
        print("Error: --part is required for bump command")
        sys.exit(1)

    plugin = read_plugin_json()
    current = plugin["version"]
    new_version = bump_version(current, args.part)

    if args.dry_run:
        print(f"Would bump version: {current} → {new_version}")
        return

    plugin["version"] = new_version
    write_plugin_json(plugin)
    print(f"Bumped version: {current} → {new_version}")


def cmd_release(args):
    """Prepare for release."""
    if not args.part:
        print("Error: --part is required for release command")
        sys.exit(1)

    plugin = read_plugin_json()
    current = plugin["version"]
    new_version = bump_version(current, args.part)

    if args.dry_run:
        print(f"Would bump version: {current} → {new_version}")
        print(f"Would update CHANGELOG.md")
        print(f"Would update plugin.json")
        return

    # Update version
    plugin["version"] = new_version
    write_plugin_json(plugin)
    print(f"Bumped version: {current} → {new_version}")

    # Update changelog
    new_changelog = update_changelog(new_version)
    write_changelog(new_changelog)
    print(f"Updated CHANGELOG.md for version {new_version}")


def main():
    parser = argparse.ArgumentParser(
        description="Version management for C3 plugin"
    )
    parser.add_argument(
        "command",
        choices=["current", "bump", "release"],
        help="Command to execute"
    )
    parser.add_argument(
        "--part",
        choices=["major", "minor", "patch"],
        help="Version part to bump"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without making changes"
    )

    args = parser.parse_args()

    commands = {
        "current": cmd_current,
        "bump": cmd_bump,
        "release": cmd_release,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()