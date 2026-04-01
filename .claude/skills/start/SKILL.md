---
name: start
description: Activate the next or selected backlog story, populate tasks/current.md, run the initial research pass, and stop at the first human decision point.
disable-model-invocation: true
---

# Start

Use this skill when the user wants to begin the next backlog item or activate a specific story.

## Workflow

1. Run `python3 scripts/ensure_control_plane.py`. If exit code is **2** (not configured), tell the user to run `/init` first and stop.
2. Read `docs/backlog.md`.
3. If the user names a story ID or title, select that matching story from `docs/backlog.md`.
4. Otherwise, prefer a story already under `## In Progress`. If there is none, pick the first unchecked story in `## Backlog`.
5. Read `tasks/current-template.md` and `tasks/current.md`.
6. If `tasks/current.md` already contains real in-progress work, pause and confirm before replacing it.
7. Reset `tasks/current.md` from `tasks/current-template.md`.
8. Copy the selected story title, story statement, and acceptance criteria into `tasks/current.md`.
9. Set the task status fields:
   - `State: researching`
   - `Story ID: ...`
   - `Active entry point: start`
   - `Next action: run research and record open questions`
10. If needed, move the selected story into the `## In Progress` section of `docs/backlog.md`.
11. Immediately perform the `research` workflow and record:
   - relevant files
   - patterns
   - constraints
   - open questions
   - proposed answers
12. After research:
   - if unresolved questions remain, set `State: awaiting-answers` and stop
   - otherwise set `State: ready-for-plan` and tell the user to run `resume`

## Rules

- Preserve the knowledge-proof sections from the template.
- Keep `## Knowledge Proof`, `## Understanding Remediation`, and `## Override / Audit Note` as untouched placeholders during activation and research.
- Do not fill `### Interrogation Results`, `### Understanding Score`, or remediation fields in this skill.
- Do not draft the implementation plan or start coding in this skill.
- Do not require the user to manually move a backlog story into `## In Progress` before using `/start`. If the requested story exists, select it and move it as part of the skill.
- If multiple stories are plausible and the choice matters, present a short list and ask the user which one to activate.
