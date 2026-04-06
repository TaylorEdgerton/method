---
name: plan-task
description: Turn the researched task into an implementation plan with phases, approval state, blockers, and next actions before coding begins.
disable-model-invocation: true
---

# Plan Task

Use this skill after research is complete and before implementation begins.

## Workflow

1. Read `tasks/current.md`, especially:
   - story
   - acceptance criteria
   - `## Work Configuration`
   - `## Task Brief`
   - `## Build Configuration`
   - research findings
   - open questions and proposed answers
2. Check `docs/learnings/` for lessons with categories or tags relevant to the current task. Note any applicable prior solutions or pitfalls to incorporate into the plan.
3. If unresolved open questions remain that materially affect implementation, do not write a final plan. Record what is blocked and return control to the user.
4. If `Level:` is missing in `## Build Configuration`, do not write a final execution plan. Record that the human must choose a build level and return control to the user.
5. Draft the level-aware execution plan in `## Plan`:
   - split work into small phases
   - map each phase to the relevant acceptance criteria
   - align phase shape with the selected build level and build profile
   - include expected tests or checks where helpful
   - call out risky steps and rollback-sensitive areas
6. Update plan metadata:
   - `Plan status: awaiting approval`
   - `User approval note:` should remain blank until the user responds
7. Update the task status:
   - `State: awaiting-plan-approval`
   - `Active entry point: build`
   - `Next action: user approves, revises, or rejects the plan`

## Rules

- Do not start implementation in this skill.
- Treat the `## Plan` section as the execution plan derived from the Task Brief and build configuration.
- Keep phases concrete and checkable.
- Prefer one coherent plan over a long list of optional ideas.
