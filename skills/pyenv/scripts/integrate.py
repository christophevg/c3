#!/usr/bin/env python3
"""
PyEnv Skill - Claude Code Integration

Main entry point for the PyEnv skill that orchestrates detection,
interactive dialogs, and environment creation.

This module provides the skill interface that Claude Code will invoke.
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

import detect
import create_env
import preferences
import review
from skill_context import get_dialog_context


def get_dialog_questions(context: dict) -> list[dict]:
    """
    Generate AskUserQuestion format dialog questions based on context.

    Args:
        context: Detection context from skill_context.py

    Returns:
        List of question dictionaries for AskUserQuestion
    """
    questions = []
    det = context["detection"]
    prefs = context["prefs"]

    # If pyenv not installed, offer to show installation instructions
    if not det["pyenv_installed"]:
        return [{
            "header": "PyEnv",
            "question": "pyenv is not installed. Would you like installation instructions?",
            "options": [
                {"label": "Show instructions", "description": "Display pyenv installation guide"},
                {"label": "Skip", "description": "I'll install pyenv manually"}
            ],
            "multiSelect": False
        }]

    # If environment already configured, offer review or management
    if det["python_version_file"] and det["current_env"]:
        return [{
            "header": "Environment",
            "question": f"Environment '{det['current_env']}' is active (Python {det['python_version_file']}). What would you like to do?",
            "options": [
                {"label": "Review best practices", "description": "Check configuration against best practices"},
                {"label": "Recreate environment", "description": "Delete and recreate the virtual environment"},
                {"label": "Manage test venvs", "description": "Create/remove test environments for package projects"},
                {"label": "Exit", "description": "Environment is ready, nothing to do"}
            ],
            "multiSelect": False
        }]

    # Package project detection
    if det["is_package_project"]:
        questions.append({
            "header": "Project Type",
            "question": "Package project detected (.pypi-template found). Configure for package development?",
            "options": [
                {"label": "Use shared pypi-template", "description": "Use globally shared pypi-template virtualenv"},
                {"label": "Create test venvs", "description": "Create test environments for multiple Python versions"},
                {"label": "Both", "description": "Use pypi-template and create test venvs"},
                {"label": "Skip", "description": "Configure manually"}
            ],
            "multiSelect": False
        })
        return questions

    # New project - version selection
    version_opts = context["version_options"]
    questions.append({
        "header": "Python Version",
        "question": "Python version for this project:",
        "options": version_opts,
        "multiSelect": False
    })

    # Naming style selection
    naming_opts = context["naming_options"]
    questions.append({
        "header": "Naming",
        "question": "Virtual environment naming:",
        "options": naming_opts,
        "multiSelect": False
    })

    # Auto-activation (only if not configured)
    if not det["auto_activation_configured"]:
        questions.append({
            "header": "Auto-activation",
            "question": "Enable automatic environment activation?",
            "options": [
                {"label": "Yes", "description": "Add pyenv-virtualenv-init to shell config"},
                {"label": "No", "description": "I'll activate manually when needed"}
            ],
            "multiSelect": False
        })

    return questions


def process_answers(answers: dict, context: dict) -> dict:
    """
    Process user answers and return actions to take.

    Args:
        answers: User's answers from AskUserQuestion
        context: Detection context

    Returns:
        Dictionary of actions to take
    """
    actions = {
        "create_env": False,
        "version": None,
        "naming_style": None,
        "enable_auto_activation": False,
        "show_review": False,
        "manage_test_venvs": False,
        "commands": []
    }

    det = context["detection"]

    # Handle pyenv not installed
    if not det["pyenv_installed"]:
        if answers.get("PyEnv") == "Show instructions":
            actions["commands"].append({
                "type": "info",
                "message": "Install pyenv from: https://pyenv.run\n\nAfter installation:\n1. Add to shell config: eval \"$(pyenv init -)\"\n2. Restart shell\n3. Run /pyenv again"
            })
        return actions

    # Handle existing environment
    if det["python_version_file"] and det["current_env"]:
        choice = answers.get("Environment", "")
        if choice == "Review best practices":
            actions["show_review"] = True
        elif choice == "Recreate environment":
            actions["create_env"] = True
            actions["version"] = det["python_version_file"]
            actions["naming_style"] = "project-name"  # Assume pyenv-virtualenv style
        elif choice == "Manage test venvs":
            actions["manage_test_venvs"] = True
        return actions

    # Handle package project
    if det["is_package_project"]:
        choice = answers.get("Project Type", "")
        if choice == "Use shared pypi-template":
            actions["commands"].append({
                "type": "info",
                "message": "Using shared pypi-template virtualenv for package development."
            })
        elif choice == "Create test venvs":
            actions["manage_test_venvs"] = True
        elif choice == "Both":
            actions["commands"].append({
                "type": "info",
                "message": "Using shared pypi-template and creating test venvs."
            })
            actions["manage_test_venvs"] = True
        return actions

    # New project setup
    version_answer = answers.get("Python Version", "")
    # Extract version from answer (format: "3.12.7 (LTS - recommended)")
    if "(" in version_answer:
        actions["version"] = version_answer.split("(")[0].strip()
    else:
        actions["version"] = version_answer

    naming_answer = answers.get("Naming", "")
    if naming_answer.startswith(".venv"):
        actions["naming_style"] = ".venv"
    else:
        actions["naming_style"] = "project-name"

    auto_answer = answers.get("Auto-activation", "")
    actions["enable_auto_activation"] = auto_answer == "Yes"
    actions["create_env"] = True

    return actions


def execute_actions(actions: dict, context: dict) -> list[str]:
    """
    Execute the actions determined from user answers.

    Returns:
        List of messages to display to user
    """
    messages = []
    det = context["detection"]
    project_name = det["project_name"]

    # Show info messages
    for cmd in actions.get("commands", []):
        if cmd["type"] == "info":
            messages.append(cmd["message"])

    # Show best practice review
    if actions.get("show_review"):
        checks = review.run_best_practice_review()
        messages.append(review.format_review_output(checks))

    # Create environment
    if actions.get("create_env"):
        version = actions["version"]
        naming = actions["naming_style"]

        if naming == ".venv":
            success = create_env.create_venv_standard(version, project_name)
        else:
            success = create_env.create_venv_pyenv(version, project_name)

        if success:
            # Record preference
            preferences.record_version_choice(version)
            preferences.record_naming_choice(naming)

    # Enable auto-activation
    if actions.get("enable_auto_activation"):
        messages.append("\nTo enable auto-activation, add to your shell config (~/.zshrc):")
        messages.append('  eval "$(pyenv virtualenv-init -)"')
        messages.append("\nThen restart your shell or run: source ~/.zshrc")

    # Manage test venvs
    if actions.get("manage_test_venvs"):
        installed = det["installed_versions"]
        # Extract unique major.minor versions
        versions = set()
        for v in installed:
            if v.startswith("3.") and not "/" in v:
                parts = v.split(".")
                if len(parts) >= 2:
                    versions.add(".".join(parts[:2]))

        messages.append(f"\nAvailable Python versions for test venvs: {sorted(versions)}")
        messages.append("\nTo create test venvs, run:")
        for v in sorted(versions):
            messages.append(f"  pyenv virtualenv {v} {project_name}-test-{v}")

    return messages


def format_questions_for_skill(questions: list[dict]) -> str:
    """Format questions for the skill to use with AskUserQuestion."""
    return json.dumps(questions, indent=2)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="PyEnv skill integration")
    parser.add_argument("--context", action="store_true", help="Get context for dialogs")
    parser.add_argument("--questions", action="store_true", help="Get questions for AskUserQuestion")
    parser.add_argument("--review", action="store_true", help="Run best practice review")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.context:
        det = detect.detect_environment()
        ctx = get_dialog_context(det)
        if args.json:
            print(json.dumps(ctx, indent=2))
        else:
            print(format_questions_for_skill(ctx))

    elif args.questions:
        det = detect.detect_environment()
        ctx = get_dialog_context(det)
        questions = get_dialog_questions(ctx)
        print(format_questions_for_skill(questions))

    elif args.review:
        checks = review.run_best_practice_review()
        if args.json:
            print(review.format_review_json(checks))
        else:
            print(review.format_review_output(checks))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()