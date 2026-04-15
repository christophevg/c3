#!/usr/bin/env python3
"""
PyEnv Best Practice Review

Reviews Python environment configuration against best practices.
"""

import subprocess
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


def run_cmd(cmd: str) -> tuple[int, str, str]:
    """Run a shell command."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


@dataclass
class PracticeCheck:
    """Result of a single best practice check."""
    name: str
    status: str  # "pass", "warning", "fail"
    notes: str
    recommendation: Optional[str] = None


def check_version_pinned() -> PracticeCheck:
    """Check if Python version is pinned (exact version)."""
    version_file = Path(".python-version")

    if not version_file.exists():
        return PracticeCheck(
            name="Version pinned",
            status="fail",
            notes="No .python-version file",
            recommendation="Create .python-version with exact version (e.g., 3.12.7)"
        )

    version = version_file.read_text().strip()

    # Check if exact version (e.g., 3.12.7 vs 3.12)
    parts = version.split(".")
    if len(parts) >= 3 and parts[2].isdigit():
        return PracticeCheck(
            name="Version pinned",
            status="pass",
            notes=f"Using exact version {version}"
        )
    else:
        return PracticeCheck(
            name="Version pinned",
            status="warning",
            notes=f"Using version range {version}",
            recommendation=f"Pin to exact version (e.g., {version}.0)"
        )


def check_version_committed() -> PracticeCheck:
    """Check if .python-version is committed to git."""
    version_file = Path(".python-version")

    if not version_file.exists():
        return PracticeCheck(
            name=".python-version committed",
            status="fail",
            notes="No .python-version file",
            recommendation="Create .python-version first"
        )

    # Check if in git repo
    code, _, _ = run_cmd("git rev-parse --git-dir 2>/dev/null")
    if code != 0:
        return PracticeCheck(
            name=".python-version committed",
            status="warning",
            notes="Not a git repository"
        )

    # Check if committed
    code, _, _ = run_cmd("git ls-files .python-version")
    if code == 0:
        return PracticeCheck(
            name=".python-version committed",
            status="pass",
            notes=".python-version is in git"
        )

    # Check if staged
    code, _, _ = run_cmd("git diff --cached --name-only | grep .python-version")
    if code == 0:
        return PracticeCheck(
            name=".python-version committed",
            status="warning",
            notes=".python-version is staged but not committed",
            recommendation="Commit with: git commit -m 'Add Python version'"
        )

    return PracticeCheck(
        name=".python-version committed",
        status="warning",
        notes=".python-version exists but not in git",
        recommendation="Add to git: git add .python-version"
    )


def check_env_exists() -> PracticeCheck:
    """Check if virtual environment exists."""
    # Check for .venv
    if Path(".venv").exists():
        return PracticeCheck(
            name="Virtual environment",
            status="pass",
            notes=".venv directory exists"
        )

    # Check for pyenv-virtualenv (via .python-version)
    version_file = Path(".python-version")
    if version_file.exists():
        version = version_file.read_text().strip()
        code, stdout, _ = run_cmd(f"pyenv versions --bare | grep -q '^{version}$' || pyenv versions --bare | grep -q 'envs/{version}$'")
        if code == 0:
            return PracticeCheck(
                name="Virtual environment",
                status="pass",
                notes=f"pyenv-virtualenv '{version}' exists"
            )

    return PracticeCheck(
        name="Virtual environment",
        status="fail",
        notes="No virtual environment found",
        recommendation="Create environment: pyenv virtualenv <version> <name> && pyenv local <name>"
    )


def check_auto_activation() -> PracticeCheck:
    """Check if auto-activation is configured."""
    import detect

    if detect.is_auto_activation_configured():
        return PracticeCheck(
            name="Auto-activation",
            status="pass",
            notes="pyenv-virtualenv-init in shell config"
        )
    else:
        return PracticeCheck(
            name="Auto-activation",
            status="warning",
            notes="Not configured",
            recommendation="Add to shell config: eval \"$(pyenv virtualenv-init -)\""
        )


def check_ide_detection() -> PracticeCheck:
    """Check if environment is IDE-detectable."""
    # .venv is universally detected
    if Path(".venv").exists():
        return PracticeCheck(
            name="IDE detection",
            status="pass",
            notes=".venv is auto-detected by VS Code, PyCharm, etc."
        )

    # pyenv-virtualenv is detected by some IDEs
    version_file = Path(".python-version")
    if version_file.exists():
        return PracticeCheck(
            name="IDE detection",
            status="pass",
            notes="pyenv environments detected by VS Code, PyCharm 2024.1+"
        )

    return PracticeCheck(
        name="IDE detection",
        status="warning",
        notes="Environment may not be auto-detected by IDE",
        recommendation="Use .venv for best IDE compatibility"
    )


def check_gitignore_venv() -> PracticeCheck:
    """Check if .venv is in .gitignore."""
    gitignore = Path(".gitignore")

    if not gitignore.exists():
        return PracticeCheck(
            name=".venv gitignored",
            status="warning",
            notes="No .gitignore file",
            recommendation="Add .gitignore with '.venv/' entry"
        )

    content = gitignore.read_text()
    if ".venv" in content or ".venv/" in content:
        return PracticeCheck(
            name=".venv gitignored",
            status="pass",
            notes=".venv is in .gitignore"
        )

    return PracticeCheck(
        name=".venv gitignored",
        status="warning",
        notes=".venv not in .gitignore",
        recommendation="Add '.venv/' to .gitignore"
    )


def run_best_practice_review() -> list[PracticeCheck]:
    """Run all best practice checks."""
    return [
        check_version_pinned(),
        check_version_committed(),
        check_env_exists(),
        check_auto_activation(),
        check_ide_detection(),
        check_gitignore_venv(),
    ]


def format_review_output(checks: list[PracticeCheck]) -> str:
    """Format review results for display."""
    lines = ["# PyEnv Configuration Review\n"]

    # Status counts
    passed = sum(1 for c in checks if c.status == "pass")
    warnings = sum(1 for c in checks if c.status == "warning")
    failed = sum(1 for c in checks if c.status == "fail")

    lines.append(f"**Status**: {passed} passed, {warnings} warnings, {failed} failures\n")

    # Table header
    lines.append("| Practice | Status | Notes |")
    lines.append("|----------|--------|-------|")

    # Table rows
    status_icons = {"pass": "✓", "warning": "⚠", "fail": "✗"}
    for check in checks:
        icon = status_icons.get(check.status, "?")
        lines.append(f"| {check.name} | {icon} | {check.notes} |")

    # Recommendations
    recommendations = [c.recommendation for c in checks if c.recommendation]
    if recommendations:
        lines.append("\n## Recommendations\n")
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. {rec}")

    return '\n'.join(lines)


def format_review_json(checks: list[PracticeCheck]) -> str:
    """Format review results as JSON."""
    import json
    return json.dumps([
        {
            "name": c.name,
            "status": c.status,
            "notes": c.notes,
            "recommendation": c.recommendation
        }
        for c in checks
    ], indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PyEnv best practice review")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    checks = run_best_practice_review()

    if args.json:
        print(format_review_json(checks))
    else:
        print(format_review_output(checks))