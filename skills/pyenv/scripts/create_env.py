#!/usr/bin/env python3
"""
PyEnv Environment Creation

Creates Python virtual environments with PyEnv.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


def run_cmd(cmd: str, check: bool = False) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def install_python_version(version: str) -> bool:
    """Install a Python version if not already installed."""
    code, _, _ = run_cmd(f"pyenv install -s {version}")
    return code == 0


def create_venv_standard(version: str, project_name: str) -> bool:
    """Create a standard .venv virtual environment."""
    # Install Python if needed
    if not install_python_version(version):
        print(f"✗ Failed to install Python {version}")
        return False

    # Create venv
    code, _, err = run_cmd(f"python -m venv .venv")
    if code != 0:
        print(f"✗ Failed to create .venv: {err}")
        return False

    # Set Python version
    Path(".python-version").write_text(f"{version}\n")

    print(f"✓ Created .venv with Python {version}")
    return True


def create_venv_pyenv(version: str, project_name: str) -> bool:
    """Create a pyenv-virtualenv virtual environment."""
    # Install Python if needed
    if not install_python_version(version):
        print(f"✗ Failed to install Python {version}")
        return False

    # Create virtualenv
    code, _, err = run_cmd(f"pyenv virtualenv {version} {project_name}")
    if code != 0:
        print(f"✗ Failed to create virtualenv: {err}")
        return False

    # Set local version
    code, _, err = run_cmd(f"pyenv local {project_name}")
    if code != 0:
        print(f"✗ Failed to set local version: {err}")
        return False

    print(f"✓ Created {project_name} (Python {version}) with pyenv-virtualenv")
    return True


def create_tool_venv(version: str, tool_name: str, packages: list[str]) -> bool:
    """Create a tool virtualenv for skills/agents."""
    env_name = f"{tool_name}-tool"

    # Install Python if needed
    if not install_python_version(version):
        print(f"✗ Failed to install Python {version}")
        return False

    # Create virtualenv
    code, _, err = run_cmd(f"pyenv virtualenv {version} {env_name}")
    if code != 0:
        print(f"✗ Failed to create virtualenv: {err}")
        return False

    # Install packages
    for pkg in packages:
        code, _, err = run_cmd(f"pyenv activate {env_name} && pip install {pkg}")
        if code != 0:
            print(f"✗ Failed to install {pkg}: {err}")
            return False

    print(f"✓ Created {env_name} with packages: {', '.join(packages)}")
    return True


def create_package_test_envs(project_name: str, versions: list[str]) -> bool:
    """Create test virtualenvs for package projects."""
    created = []
    for version in versions:
        # Get major.minor from version
        parts = version.split('.')
        short_version = '.'.join(parts[:2]) if len(parts) >= 2 else version

        env_name = f"{project_name}-test-{short_version}"

        # Install Python if needed
        if not install_python_version(version):
            print(f"✗ Failed to install Python {version}")
            continue

        # Create test virtualenv
        code, _, err = run_cmd(f"pyenv virtualenv {version} {env_name}")
        if code != 0:
            print(f"✗ Failed to create {env_name}: {err}")
            continue

        created.append(env_name)

    if created:
        print(f"✓ Created test environments: {', '.join(created)}")
        return True
    return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create PyEnv environments")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Standard venv
    std_parser = subparsers.add_parser("standard", help="Create .venv style environment")
    std_parser.add_argument("version", help="Python version")
    std_parser.add_argument("--project", help="Project name")

    # Pyenv-virtualenv
    pyenv_parser = subparsers.add_parser("pyenv", help="Create pyenv-virtualenv style environment")
    pyenv_parser.add_argument("version", help="Python version")
    pyenv_parser.add_argument("project", help="Project name")

    # Tool venv
    tool_parser = subparsers.add_parser("tool", help="Create tool virtualenv")
    tool_parser.add_argument("version", help="Python version")
    tool_parser.add_argument("name", help="Tool name")
    tool_parser.add_argument("--packages", nargs="+", help="Packages to install")

    # Test venvs
    test_parser = subparsers.add_parser("test", help="Create test environments for package projects")
    test_parser.add_argument("project", help="Project name")
    test_parser.add_argument("--versions", nargs="+", required=True, help="Python versions")

    args = parser.parse_args()

    if args.command == "standard":
        project = args.project or Path.cwd().name
        success = create_venv_standard(args.version, project)
    elif args.command == "pyenv":
        success = create_venv_pyenv(args.version, args.project)
    elif args.command == "tool":
        success = create_tool_venv(args.version, args.name, args.packages or [])
    elif args.command == "test":
        success = create_package_test_envs(args.project, args.versions)
    else:
        print(f"Unknown command: {args.command}")
        success = False

    sys.exit(0 if success else 1)