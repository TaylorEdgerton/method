---
name: plan-task
description: Turn the researched task into an implementation plan with phases, approval state, blockers, and next actions before coding begins.
---

# Plan Task

Use this skill after research is complete and before implementation begins.

## Workflow

1. Read `tasks/current.md`, especially:
   - story
   - acceptance criteria
   - research findings
   - open questions and proposed answers
2. Check `docs/learnings/` for lessons with categories or tags relevant to the current task. Note any applicable prior solutions or pitfalls to incorporate into the plan.
3. If unresolved open questions remain that materially affect implementation, do not write a final plan. Record what is blocked and return control to the user.
4. Draft the implementation plan in `## Plan`:
   - split work into small phases
   - map each phase to the relevant acceptance criteria
   - include expected tests or checks where helpful
   - call out risky steps and rollback-sensitive areas
5. Update plan metadata:
   - `Plan status: awaiting approval`
   - `User approval note:` should remain blank until the user responds
6. Update the task status:
   - `State: awaiting-plan-approval`
   - `Active entry point: resume`
   - `Next action: user approves, revises, or rejects the plan`

## Rules

- Do not start implementation in this skill.
- Keep phases concrete and checkable.
- Prefer one coherent plan over a long list of optional ideas.
