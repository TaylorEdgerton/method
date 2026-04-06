---
name: finalise
description: Finalise the active task, trigger the knowledge-proof gate at the right point, archive the task note, and reset tasks/current.md.
---

# Finalise

End-of-session routine for finalising the current task, ensuring implementation quality, enforcing the knowledge-proof gate when required, archiving the task note, and resetting `tasks/current.md`.

## Workflow

1. Read `tasks/current.md`, especially `## Execution Notes`, `## Ownership Evidence`, `## Verification Plan`, and `## Review Findings`.
2. Inspect `git status` when Git metadata is available. If it is not, note that limitation explicitly.
3. Confirm the task is actually ready for finalisation:
   - implementation is complete
   - review findings are resolved or explicitly dispositioned
   - verification work has been run or gaps are recorded
4. Run the relevant quality checks for the work that changed.
5. Update `tasks/current.md` so checkboxes, notes, findings, and status reflect reality.
6. Determine whether the task changed implementation behaviour.
7. If the task changed behaviour or logic:
   - ensure `## Knowledge Proof` is present
   - read `## Ownership Evidence` before triggering `test-me`
   - shorten the final proof when enough ownership evidence already exists
   - increase proof intensity for higher-risk work or more autonomous build levels
   - default to live human questioning; only use `self-test` if the user explicitly asked for a rehearsal
   - run `scripts/check_understanding_gate.py` when available
8. If the gate fails, do not silently continue. Require either:
   - a passing `test-me` result
   - an `## Override / Audit Note` that records why finalisation is still happening, who accepted the risk, and what follow-up is required
9. If accepted risks, deferred findings, or override follow-up work remain, run `follow-up-triage` before archiving.
10. Run `compound` to check for reusable lessons worth capturing in `docs/learnings/`.
11. If the task changed code, run the `documentation-engineer` agent to update or create relevant documentation.
12. If scripts, queries, handlers, or workflow assets changed, refresh `docs/scriptReferences.md`.
13. If the task is complete:
   - mark the story done in `docs/backlog.md`
   - move `tasks/current.md` into `tasks/completed/` with a timestamped filename
   - restore `tasks/current-template.md` as the new `tasks/current.md`
14. Summarise task completion status, knowledge-proof status, remediation or override details, and any residual debt.

## Knowledge-Proof Rules

- A knowledge proof is normally required for tasks that change code, logic, data flow, scripts, automation, validation, permissions, error handling, or state transitions.
- A knowledge proof is usually not required for documentation-only tasks or backlog grooming.
- When a proof is not required, record that decision briefly in `tasks/current.md` before archiving.
- Use the lightest proof that still demonstrates ownership for lower-risk Level 1 to 2 work.
- Use a stronger proof for higher-risk or more autonomous Level 3 to 4 work.

## Tools

- `scripts/check_understanding_gate.py`
- `scripts/record_understanding.py`

Prefer the deterministic helpers when they exist.

Do not invent a passing or failing knowledge-proof result without actual questioning of the human or an explicit user request for a self-test rehearsal.