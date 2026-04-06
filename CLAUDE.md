# Project Memory

Use repo skills for reusable workflows.

## Project

- Name: Method
- Summary: AI-assisted workflow control-plane template for structured software delivery with tasks, reviews, and understanding gates.
- Stack: Markdown, Python, Git hooks, Claude Code/Codex skills, subagents, and repository automation

## Workflow Skills

User-facing entry points:
- `init`: one-time project bootstrap — configure the control plane, populate CLAUDE.md, set up hooks
- `prepare`: activate the next or selected backlog story, run research, and capture the Task Brief
- `build`: materialize the execution plan, route work through the selected build level, and coordinate review
- `finalise`: finish, archive, and reset the active task while enforcing the scaled understanding gate

Internal helper skills:
- `research`: inspect the codebase and document findings before planning
- `plan-task`: turn the Task Brief and build configuration into an approval-ready execution plan
- `test-matrix`: define the explicit verification plan
- `checkpoint`: review progress, repo state, and next actions
- `build-level-1`: coaching-first helper for human-authored narrow seams
- `build-level-2`: structure-first helper that avoids taking over authorship
- `build-level-3`: collaborative helper for intent-first, approval-gated seams
- `build-level-4`: explicit high-autonomy helper for larger, reviewable execution
- `update-references`: refresh `docs/scriptReferences.md`
- `test-me`: run the knowledge-proof interrogation and remediation workflow
- `follow-up-triage`: turn accepted risks or deferred findings into visible follow-up work
- `compound`: capture reusable lessons from completed tasks into `docs/learnings/`
- `compound-refresh`: review and maintain the learnings knowledge base

## Repo Rules

Behavioral guardrails are enforced via `.claude/rules/`, `.githooks/pre-push`, and
`scripts/check_understanding_gate.py`. See those files for details.

Critical rules (duplicated here for belt-and-suspenders reliability):

- Do not pre-fill knowledge-proof scores or remediation before `test-me` actually questions the user.
- Do not bypass the pre-push hook with `--no-verify`.
- Do not force-push or push directly to `main` without explicit user confirmation.

Deterministic enforcement scripts:

- `.githooks/pre-push`
- `scripts/check_understanding_gate.py`
- `scripts/record_understanding.py`

## Knowledge-proof threshold

Normal ownership threshold is `8/10` equivalent.

- `>= 85%`: strong understanding
- `70-84%`: acceptable, but record gaps
- `60-69%`: remediation required before `finalise`
- `<60%`: do not finalise without an explicit override note

## Current State

- Active task: `tasks/current.md`
- Task template: `tasks/current-template.md`
- Backlog: `docs/backlog.md`
- Known issues: `issues/`
- Learnings: `docs/learnings/`
- Strict style mockup html: `docs/mockup.html`

## Reminder

Use skills for rich workflow instructions. Keep this file short and durable.
