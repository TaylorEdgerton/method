---
name: wrap-up
description: Finalise the active task, trigger the knowledge-proof gate at the right point, archive the task note, and reset tasks/current.md.
---

# Wrap Up

End-of-session routine for finalising the current task, ensuring implementation quality, enforcing the knowledge-proof gate when required, archiving the task note, and resetting `tasks/current.md`.

## Workflow

1. Read `tasks/current.md` and inspect `git status`.
2. Confirm the task is actually ready for wrap-up:
   - implementation is complete
   - review findings are resolved or explicitly dispositioned
   - verification work has been run or gaps are recorded
3. Run the relevant quality checks for the work that changed.
4. Update `tasks/current.md` so checkboxes, notes, findings, and status reflect reality.
5. Determine whether the task changed implementation behaviour.
6. If the task changed behaviour or logic:
   - ensure `## Knowledge Proof` is present
   - trigger `test-me` if no acceptable understanding result is already recorded
   - default to live human questioning; only use `self-test` if the user explicitly asked for a rehearsal
   - run `scripts/check_understanding_gate.py` when available
7. If the gate fails, do not silently continue. Require either:
   - a passing `test-me` result
   - an `## Override / Audit Note` that records why wrap-up is still happening, who accepted the risk, and what follow-up is required
8. If accepted risks, deferred findings, or override follow-up work remain, run `follow-up-triage` before archiving.
9. Run `compound` to check for reusable lessons worth capturing in `docs/learnings/`. The skill will exit early if nothing is worth documenting.
10. If the task changed code, run the `documentation-engineer` agent to update or create relevant documentation:
    - Mermaid diagrams in `docs/` reflecting new or changed architecture
    - Architecture Decision Records in `docs/decisions/` for significant design choices
    - API or module documentation where public interfaces changed
11. If scripts, queries, handlers, or workflow assets changed, refresh `docs/scriptReferences.md`.
12. If the task is complete:
   - mark the story done in `docs/backlog.md`
   - move `tasks/current.md` into `tasks/completed/` with a timestamped filename
   - restore `tasks/current-template.md` as the new `tasks/current.md`
13. Summarise:
   - task completion status
   - commit status
   - knowledge-proof status
   - understanding score
   - remediation or override details
   - any residual debt or follow-up work

## Knowledge-Proof Rules

A knowledge proof is normally required for tasks that change:

- code
- logic
- data flow
- scripts
- automation
- validation
- permissions
- error handling
- state transitions

A knowledge proof is usually not required for:

- documentation-only tasks
- backlog grooming only
- research-only tasks with no implementation changes

When a proof is not required, record that decision briefly in `tasks/current.md` before archiving.

## Tools

- `scripts/check_understanding_gate.py`
- `scripts/record_understanding.py`

Prefer the deterministic helpers when they exist.

Do not invent a passing or failing knowledge-proof result without actual questioning of the human or an explicit user request for a self-test rehearsal.
