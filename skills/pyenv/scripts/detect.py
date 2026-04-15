#!/usr/bin/env python3
"""
PyEnv Environment Detection

Detects Python environment configuration for a project.
"""

import os
import subprocess
import json
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


def is_pyenv_installed() -> bool:
    """Check if pyenv is installed."""
    code, _, _ = run_cmd("which pyenv")
    return code == 0


def get_installed_versions() -> list[str]:
    """Get list of installed Python versions."""
    code, stdout, _ = run_cmd("pyenv versions --bare")
    if code != 0:
        return []
    versions = [v for v in stdout.split('\n') if v and not v.startswith('envs/')]
    return sorted(versions, reverse=True)


def get_python_version_file() -> Optional[str]:
    """Check for .python-version file and return its content."""
    version_file = Path(".python-version")
    if version_file.exists():
        return version_file.read_text().strip()
    return None


def is_package_project() -> bool:
    """Check if this is a Python package project (has .pypi-template)."""
    return Path(".pypi-template").exists()


def get_current_env() -> Optional[str]:
    """Get the currently active pyenv environment."""
    code, stdout, _ = run_cmd("pyenv version-name")
    if code == 0 and stdout:
        return stdout
    return None


def env_exists(env_name: str) -> bool:
    """Check if a virtual environment exists."""
    code, stdout, _ = run_cmd("pyenv versions --bare")
    if code != 0:
        return False
    return env_name in stdout.split('\n')


def is_auto_activation_configured() -> bool:
    """Check if pyenv-virtualenv-init is in shell config."""
    shell_configs = [
        Path.home() / ".zshrc",
        Path.home() / ".bashrc",
        Path.home() / ".bash_profile",
    ]
    for config in shell_configs:
        if config.exists():
            content = config.read_text()
            if "pyenv virtualenv-init" in content:
                return True
    return False


def detect_environment() -> dict:
    """
    Detect current Python environment configuration.

    Returns:
        dict with detection results
    """
    result = {
        "pyenv_installed": False,
        "installed_versions": [],
        "python_version_file": None,
        "current_env": None,
        "env_exists": False,
        "is_package_project": False,
        "auto_activation_configured": False,
        "project_name": None,
    }

    # Get project name from current directory
    result["project_name"] = Path.cwd().name

    # Check pyenv installation
    result["pyenv_installed"] = is_pyenv_installed()
    if not result["pyenv_installed"]:
        return result

    # Get installed versions
    result["installed_versions"] = get_installed_versions()

    # Check .python-version
    version = get_python_version_file()
    result["python_version_file"] = version

    # Check if package project
    result["is_package_project"] = is_package_project()

    # Get current environment
    current = get_current_env()
    result["current_env"] = current

    # Check if env exists (for the version in .python-version)
    if version:
        result["env_exists"] = env_exists(version) or env_exists(f"envs/{version}")

    # Check auto-activation
    result["auto_activation_configured"] = is_auto_activation_configured()

    return result


def format_detection_output(detection: dict) -> str:
    """Format detection results for display."""
    lines = []

    if not detection["pyenv_installed"]:
        lines.append("✗ pyenv not installed")
        lines.append("  Install from: https://pyenv.run")
        return '\n'.join(lines)

    lines.append("✓ pyenv installed")

    if detection["python_version_file"]:
        lines.append(f"✓ Python version: {detection['python_version_file']}")
    else:
        lines.append("○ No .python-version file")

    if detection["is_package_project"]:
        lines.append("✓ Package project detected (.pypi-template)")

    if detection["current_env"]:
        lines.append(f"✓ Active environment: {detection['current_env']}")
    else:
        lines.append("○ No active environment")

    if detection["auto_activation_configured"]:
        lines.append("✓ Auto-activation configured")
    else:
        lines.append("○ Auto-activation not configured")

    return '\n'.join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Detect PyEnv environment")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    detection = detect_environment()

    if args.json:
        print(json.dumps(detection, indent=2))
    else:
        print(format_detection_output(detection))