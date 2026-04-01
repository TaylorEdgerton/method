#!/usr/bin/env python3
"""Check that the project control plane is configured.

Exit codes:
    0 — fully configured, ready to work
    1 — unexpected error during checks
    2 — not configured at all (user should run /init)
    3 — partially configured (some items still need attention)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
BACKLOG = REPO_ROOT / "docs" / "backlog.md"
TASK_TEMPLATE = REPO_ROOT / "tasks" / "current-template.md"
HOOKS_DIR = REPO_ROOT / ".githooks"

PLACEHOLDERS = [
    "[PROJECT_NAME]",
    "[Brief description of this project]",
    "[Primary languages, frameworks, and tools]",
]


def hooks_configured() -> bool:
    """Return True if core.hooksPath points to .githooks."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0 and ".githooks" in result.stdout.strip()
    except FileNotFoundError:
        return False


def claude_md_populated() -> bool:
    """Return True if CLAUDE.md exists and has no template placeholders."""
    if not CLAUDE_MD.exists():
        return False
    text = CLAUDE_MD.read_text(encoding="utf-8")
    return not any(ph in text for ph in PLACEHOLDERS)


def backlog_exists() -> bool:
    """Return True if the backlog file exists."""
    return BACKLOG.exists()


def task_template_exists() -> bool:
    """Return True if the task template exists."""
    return TASK_TEMPLATE.exists()


def main() -> int:
    try:
        checks = {
            "CLAUDE.md populated": claude_md_populated(),
            "Git hooks configured": hooks_configured(),
            "Backlog file exists": backlog_exists(),
            "Task template exists": task_template_exists(),
        }

        passed = sum(1 for v in checks.values() if v)
        total = len(checks)

        if passed == total:
            print("Control plane: fully configured.")
            return 0

        if passed == 0:
            print("Control plane: not configured. Run /init to set up the project.")
            for name, ok in checks.items():
                print(f"  {'✓' if ok else '✗'} {name}")
            return 2

        print("Control plane: partially configured. Some items need attention.")
        for name, ok in checks.items():
            print(f"  {'✓' if ok else '✗'} {name}")
        return 3

    except Exception as exc:
        print(f"Control plane check error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
