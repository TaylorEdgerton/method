---
name: checkpoint
description: Review progress on the active task, reconcile tasks/current.md with the actual repo state, and update task state and the next workflow step.
---

# Checkpoint

Use this skill during implementation to keep `tasks/current.md` honest and current.

## Workflow

1. Read `tasks/current.md`.
2. Check repo state with `git status` and inspect diffs when needed.
3. Compare the documented plan and acceptance criteria against the observed changes.
4. Update checkboxes in `tasks/current.md` only when the work is actually complete.
5. Summarise:
   - what has been completed
   - what remains
   - any blockers or decisions that need attention
6. If there are uncommitted changes, suggest a commit message.
7. Report context usage if the runtime exposes it. If it does not, say that context usage is unavailable.
8. Update the status fields so the task note reflects the real next step:
   - `implementing`
   - `awaiting-review-disposition`
   - `awaiting-knowledge-proof`
   - `ready-to-wrap`
9. If implementation work is effectively done, point to the next step:
   - `resume` when review passes still need to run or findings need disposition
   - `wrap-up` when the task is ready for the understanding gate and closure

## Rules

- Do not mark boxes complete just because the intent is clear; use repo evidence.
- Keep summaries concise and anchored to the actual task file.
