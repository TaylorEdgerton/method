#!/usr/bin/env python3
"""Update the knowledge-proof sections in tasks/current.md.

This script is intentionally markdown-first and dependency-free so it can be
called from skills, shell scripts, or CI helpers.

Examples:
  python scripts/record_understanding.py \
    --task-file tasks/current.md \
    --proof-required yes \
    --changed-files api/routes/story.py scrumteam/state.py \
    --key-flows "story lookup" "validation then write" \
    --risk-areas "partial writes" "stale repo state" \
    --interview-date 2026-03-28 \
    --interview-mode live \
    --reviewer "human + model" \
    --coverage-level high \
    --flow-accuracy 4 \
    --branch-coverage 4 \
    --failure-state-awareness 3 \
    --edge-case-awareness 4 \
    --security-misuse-awareness 3 \
    --acceptance-traceability 5 \
    --gaps-found "Missed stale state path" "Did not mention rollback"

  python scripts/record_understanding.py \
    --task-file tasks/current.md \
    --initial-understanding-score 6/10 \
    --gaps-identified "Missed fallback path" "Could not map AC2" \
    --training-questions "What happens when metadata is missing?" \
                         "Which file owns rollback?" \
    --final-understanding-score 8/10 \
    --pass-fail Pass \
    --residual-debt "Still weak on stale state recovery"
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional, Sequence, Tuple


class MarkdownTaskFile:
    def __init__(self, text: str):
        self.lines = text.splitlines()

    def _find_heading(self, heading_text: str) -> int:
        pattern = re.compile(rf"^#+\s+{re.escape(heading_text)}\s*$")
        for index, line in enumerate(self.lines):
            if pattern.match(line.strip()):
                return index
        raise ValueError(f"Heading not found: {heading_text}")

    def _heading_level(self, line: str) -> Optional[int]:
        match = re.match(r"^(#+)\s+", line.strip())
        return len(match.group(1)) if match else None

    def _section_bounds(self, heading_text: str) -> Tuple[int, int]:
        start = self._find_heading(heading_text)
        start_level = self._heading_level(self.lines[start])
        if start_level is None:
            raise ValueError(f"Not a heading line: {self.lines[start]}")
        end = len(self.lines)
        for index in range(start + 1, len(self.lines)):
            level = self._heading_level(self.lines[index])
            if level is not None and level <= start_level:
                end = index
                break
        return start, end

    def _replace_or_insert_bullet(self, heading_text: str, label: str, value: str) -> None:
        start, end = self._section_bounds(heading_text)
        bullet = f"- {label}: {value}" if value else f"- {label}:"
        prefix = f"- {label}:"
        for index in range(start + 1, end):
            if self.lines[index].strip().startswith(prefix):
                self.lines[index] = bullet
                return

        insert_at = end
        while insert_at > start + 1 and self.lines[insert_at - 1].strip() == "":
            insert_at -= 1
        self.lines.insert(insert_at, bullet)

    def _replace_list_section(self, heading_text: str, items: Sequence[str]) -> None:
        start, end = self._section_bounds(heading_text)
        content = [f"- {item}" for item in items if item.strip()]
        if not content:
            return

        insert_at = start + 1
        while insert_at < end and self.lines[insert_at].strip() == "":
            insert_at += 1

        del self.lines[insert_at:end]
        for offset, line in enumerate(content):
            self.lines.insert(insert_at + offset, line)
        self.lines.insert(insert_at + len(content), "")

    def render(self) -> str:
        return "\n".join(self.lines).rstrip() + "\n"


def clamp_score(value: Optional[int]) -> Optional[int]:
    if value is None:
        return None
    return max(0, min(5, int(value)))


def normalise_csv(items: Optional[Sequence[str]]) -> Optional[str]:
    if not items:
        return None
    clean = [item.strip() for item in items if item and item.strip()]
    return ", ".join(clean) if clean else None


def compute_total_percent(args: argparse.Namespace) -> Tuple[Optional[int], Optional[int]]:
    score_fields = [
        clamp_score(args.flow_accuracy),
        clamp_score(args.branch_coverage),
        clamp_score(args.failure_state_awareness),
        clamp_score(args.edge_case_awareness),
        clamp_score(args.security_misuse_awareness),
        clamp_score(args.acceptance_traceability),
    ]
    if any(score is None for score in score_fields):
        return None, None
    total = sum(score_fields)
    percent = round((total / 30) * 100)
    return total, percent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record knowledge-proof results in a markdown task file.")
    parser.add_argument("--task-file", default="tasks/current.md", help="Path to the markdown task file.")
    parser.add_argument("--proof-required", choices=["yes", "no"], help="Whether a knowledge proof is required.")
    parser.add_argument("--proof-reason", help="Reason when marking a proof as not required.")

    parser.add_argument("--changed-files", nargs="*", help="Changed files under test.")
    parser.add_argument("--key-flows", nargs="*", help="Key flows under test.")
    parser.add_argument("--risk-areas", nargs="*", help="Risk areas under test.")

    parser.add_argument("--interview-date", help="Interview date.")
    parser.add_argument("--interview-mode", help="Interview mode.")
    parser.add_argument("--reviewer", help="Reviewer description.")
    parser.add_argument("--coverage-level", choices=["low", "medium", "high"], help="Coverage level.")

    parser.add_argument("--flow-accuracy", type=int)
    parser.add_argument("--branch-coverage", type=int)
    parser.add_argument("--failure-state-awareness", type=int)
    parser.add_argument("--edge-case-awareness", type=int)
    parser.add_argument("--security-misuse-awareness", type=int)
    parser.add_argument("--acceptance-traceability", type=int)

    parser.add_argument("--gaps-found", nargs="*", help="List of gaps found in the main interrogation.")

    parser.add_argument("--initial-understanding-score", help="Initial remediation score, e.g. 6/10.")
    parser.add_argument("--gaps-identified", nargs="*", help="Gaps identified during remediation.")
    parser.add_argument("--training-questions", nargs="*", help="Questions asked during remediation.")
    parser.add_argument("--final-understanding-score", help="Final remediation score, e.g. 8/10.")
    parser.add_argument("--pass-fail", choices=["Pass", "Fail"], help="Final remediation outcome.")
    parser.add_argument("--residual-debt", nargs="*", help="Residual debt notes.")

    parser.add_argument("--override-reason", help="Override reason when wrapping below threshold.")
    parser.add_argument("--risk-accepted-by", help="Who accepted the risk.")
    parser.add_argument("--follow-up-action", help="Required follow-up action.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    task_path = Path(args.task_file)
    if not task_path.exists():
        parser.error(f"Task file does not exist: {task_path}")

    doc = MarkdownTaskFile(task_path.read_text(encoding="utf-8"))

    if args.proof_required:
        if args.proof_required == "no" and args.proof_reason:
            proof_value = f"no ({args.proof_reason})"
        else:
            proof_value = args.proof_required
        doc._replace_or_insert_bullet("Scope Under Test", "Proof required", proof_value)

    changed_files = normalise_csv(args.changed_files)
    key_flows = normalise_csv(args.key_flows)
    risk_areas = normalise_csv(args.risk_areas)
    if changed_files is not None:
        doc._replace_or_insert_bullet("Scope Under Test", "Changed files", changed_files)
    if key_flows is not None:
        doc._replace_or_insert_bullet("Scope Under Test", "Key flows", key_flows)
    if risk_areas is not None:
        doc._replace_or_insert_bullet("Scope Under Test", "Risk areas", risk_areas)

    if args.interview_date:
        doc._replace_or_insert_bullet("Interrogation Results", "Date", args.interview_date)
    if args.interview_mode:
        doc._replace_or_insert_bullet("Interrogation Results", "Interview mode", args.interview_mode)
    if args.reviewer:
        doc._replace_or_insert_bullet("Interrogation Results", "Reviewer", args.reviewer)
    if args.coverage_level:
        doc._replace_or_insert_bullet("Interrogation Results", "Coverage level", args.coverage_level)

    score_map = [
        ("Flow accuracy", clamp_score(args.flow_accuracy)),
        ("Branch coverage", clamp_score(args.branch_coverage)),
        ("Failure-state awareness", clamp_score(args.failure_state_awareness)),
        ("Edge-case awareness", clamp_score(args.edge_case_awareness)),
        ("Security / misuse awareness", clamp_score(args.security_misuse_awareness)),
        ("Acceptance-criteria traceability", clamp_score(args.acceptance_traceability)),
    ]
    for label, value in score_map:
        if value is not None:
            doc._replace_or_insert_bullet("Understanding Score", label, f"{value}/5")

    total, percent = compute_total_percent(args)
    if total is not None:
        doc._replace_or_insert_bullet("Understanding Score", "Total", f"{total}/30")
        doc._replace_or_insert_bullet("Understanding Score", "Percent", f"{percent}/100")
        doc._replace_or_insert_bullet("Understanding Score", "Threshold required", "8/10 equivalent")

    if args.gaps_found:
        doc._replace_list_section("Gaps Found", args.gaps_found)

    if args.initial_understanding_score:
        doc._replace_or_insert_bullet("Initial Result", "Initial understanding score", args.initial_understanding_score)
        doc._replace_or_insert_bullet("Initial Result", "Threshold required", "8/10 equivalent")
    if args.gaps_identified:
        doc._replace_list_section("Gaps Identified", args.gaps_identified)
    if args.training_questions:
        doc._replace_list_section("Training Questions Asked", args.training_questions)
    if args.final_understanding_score:
        doc._replace_or_insert_bullet("Re-Test Result", "Final understanding score", args.final_understanding_score)
    if args.pass_fail:
        doc._replace_or_insert_bullet("Re-Test Result", "Pass / Fail", args.pass_fail)
    if args.residual_debt:
        doc._replace_list_section("Residual Debt", args.residual_debt)

    if args.override_reason:
        doc._replace_or_insert_bullet("Override / Audit Note", "Reason if wrapping up below threshold", args.override_reason)
    if args.risk_accepted_by:
        doc._replace_or_insert_bullet("Override / Audit Note", "Risk accepted by", args.risk_accepted_by)
    if args.follow_up_action:
        doc._replace_or_insert_bullet("Override / Audit Note", "Follow-up action", args.follow_up_action)

    task_path.write_text(doc.render(), encoding="utf-8")

    print(f"Updated {task_path}")
    if total is not None and percent is not None:
        print(f"Recorded total score: {total}/30 ({percent}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())