#!/usr/bin/env python3
"""Gate pushes/wrap-up based on the knowledge-proof status in tasks/current.md.

The script is intentionally conservative:
- If there is no active task, it exits 0.
- If the task appears documentation-only, it exits 0.
- If implementation work appears active and a knowledge proof is required,
  it requires either:
    * a passing score at or above the threshold, or
    * an explicit override note.

This is designed as a guardrail, not a perfect forensic system.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path
from typing import List, Optional


IMPLEMENTATION_PATH_HINTS = {
    ".githooks/",
    "src/",
    "app/",
    "lib/",
    "pkg/",
    "scripts/",
    "tests/",
    "test/",
}

IMPLEMENTATION_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs",
    ".java", ".kt", ".go", ".rs", ".rb", ".php", ".cs",
    ".cpp", ".cc", ".c", ".h", ".hpp", ".swift", ".scala",
    ".sql", ".sh", ".bash", ".zsh", ".ps1", ".yaml", ".yml",
    ".toml", ".json", ".xml",
}

DOC_EXTENSIONS = {".md", ".rst", ".txt", ".adoc"}
PLACEHOLDER_MARKERS = [
    "[User story copied from backlog]",
    "- [ ] [criterion]",
    "### Phase 1: [name]",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check whether the current task satisfies the understanding gate.")
    parser.add_argument("--task-file", default="tasks/current.md")
    parser.add_argument("--threshold-percent", type=int, default=80)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--commit-range", default=None,
                        help="Git commit range (e.g. abc123..def456) to determine changed files. "
                             "When provided, uses 'git diff --name-only <range>' instead of "
                             "inspecting the working tree and staging area.")
    return parser


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def is_placeholder_task(text: str) -> bool:
    return all(marker in text for marker in PLACEHOLDER_MARKERS)


def find_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^#+\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^#{1,6}\s+", text[start:], re.MULTILINE)
    if not next_heading:
        return text[start:]
    return text[start:start + next_heading.start()]


def extract_line_value(section_text: str, label: str) -> Optional[str]:
    pattern = re.compile(rf"^-\s+{re.escape(label)}:\s*(.+?)\s*$", re.MULTILINE)
    match = pattern.search(section_text)
    return match.group(1).strip() if match else None


def parse_percent(text: str) -> Optional[int]:
    if not text:
        return None
    patterns = [
        re.compile(r"(\d{1,3})\s*/\s*100"),
        re.compile(r"(\d{1,3})\s*%"),
        re.compile(r"^\s*(\d{1,3})\s*$"),
    ]
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            value = int(match.group(1))
            if 0 <= value <= 100:
                return value
    return None


def parse_score_out_of_ten(text: str) -> Optional[float]:
    if not text:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", text)
    if not match:
        return None
    value = float(match.group(1))
    if 0.0 <= value <= 10.0:
        return value
    return None


def parse_override_present(override_section: str) -> bool:
    values = [
        extract_line_value(override_section, "Reason if wrapping up below threshold"),
        extract_line_value(override_section, "Risk accepted by"),
        extract_line_value(override_section, "Follow-up action"),
    ]
    cleaned = [value for value in values if value and not value.startswith("[")]
    return any(cleaned)


def git_changed_files(repo_root: Path, commit_range: Optional[str] = None) -> List[str]:
    changed: List[str] = []
    if commit_range:
        commands = [["git", "diff", "--name-only", commit_range]]
    else:
        commands = [
            ["git", "diff", "--name-only"],
            ["git", "diff", "--name-only", "--cached"],
        ]
    for command in commands:
        try:
            result = subprocess.run(
                command,
                cwd=repo_root,
                check=False,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            return []
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            line = line.strip()
            if line:
                changed.append(line)
    return sorted(set(changed))


def path_looks_implementation(path_text: str) -> bool:
    normalised = path_text.replace("\\", "/")
    if any(normalised.startswith(prefix) for prefix in IMPLEMENTATION_PATH_HINTS):
        return True
    return Path(normalised).suffix.lower() in IMPLEMENTATION_EXTENSIONS


def path_looks_doc(path_text: str) -> bool:
    normalised = path_text.replace("\\", "/")
    return Path(normalised).suffix.lower() in DOC_EXTENSIONS


def infer_proof_required(task_text: str, repo_root: Path, commit_range: Optional[str] = None) -> bool:
    explicit = extract_line_value(find_section(task_text, "Scope Under Test"), "Proof required")
    if explicit:
        lowered = explicit.lower()
        if lowered.startswith("no"):
            return False
        if lowered.startswith("yes"):
            return True

    changed_files = git_changed_files(repo_root, commit_range=commit_range)
    if changed_files:
        any_impl = any(path_looks_implementation(path) for path in changed_files)
        any_non_docs = any(not path_looks_doc(path) for path in changed_files)
        if any_impl or any_non_docs:
            return True
        return False

    story = find_section(task_text, "Story")
    notes = find_section(task_text, "Notes")
    knowledge_proof = find_section(task_text, "Knowledge Proof")
    content_hints = f"{story}\n{notes}\n{knowledge_proof}".lower()
    keywords = [
        "code", "script", "logic", "validation", "schema", "state", "automation",
        "permission", "error handling", "data flow", "refactor", "endpoint", "api",
    ]
    return any(keyword in content_hints for keyword in keywords)


def collect_unchecked_boxes(task_text: str) -> List[str]:
    unchecked = []
    for line in task_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [ ]") and "[criterion]" not in stripped and "[step]" not in stripped:
            unchecked.append(stripped)
    return unchecked


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).resolve()
    task_file = (repo_root / args.task_file).resolve()

    if not task_file.exists():
        print(f"PASS: task file not found at {task_file}; nothing to gate.")
        return 0

    task_text = read_text(task_file)
    if is_placeholder_task(task_text):
        print("PASS: tasks/current.md looks like a reset template; no active task detected.")
        return 0

    proof_required = infer_proof_required(task_text, repo_root, commit_range=args.commit_range)
    if not proof_required:
        print("PASS: knowledge proof not required for the active task.")
        return 0

    unchecked = collect_unchecked_boxes(task_text)
    if unchecked:
        print("WARNING: unchecked task items remain in tasks/current.md:")
        for item in unchecked:
            print(f"  - {item}")

    knowledge_score = find_section(task_text, "Understanding Score")
    override = find_section(task_text, "Override / Audit Note")

    override_present = parse_override_present(override)

    remediation_outcome = extract_line_value(find_section(task_text, "Re-Test Result"), "Pass / Fail")
    remediation_final_score = extract_line_value(find_section(task_text, "Re-Test Result"), "Final understanding score")
    remediation_final_out_of_ten = parse_score_out_of_ten(remediation_final_score or "")

    if remediation_outcome and remediation_outcome.lower() == "pass":
        print("PASS: remediation result is marked Pass.")
        return 0
    if remediation_final_out_of_ten is not None and remediation_final_out_of_ten >= 8.0:
        print(f"PASS: remediation final score is {remediation_final_out_of_ten}/10.")
        return 0

    percent_value = parse_percent(extract_line_value(knowledge_score, "Percent") or "")
    if percent_value is not None and percent_value >= args.threshold_percent:
        print(f"PASS: understanding score is {percent_value}%.")
        return 0

    if override_present:
        score_text = f"{percent_value}%" if percent_value is not None else "no score recorded"
        print(f"PASS WITH OVERRIDE: understanding gate below threshold ({score_text}) but override note is present.")
        return 0

    if percent_value is None and remediation_final_out_of_ten is None:
        print("BLOCK: knowledge proof is required but no passing score was recorded.")
    else:
        if percent_value is not None:
            print(f"BLOCK: understanding score is {percent_value}%, below the required {args.threshold_percent}% threshold.")
        else:
            print("BLOCK: remediation score is below threshold and no override note is present.")
    print("Run the test-me skill, record remediation results, or add an Override / Audit Note before pushing.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())