---
name: resume
description: Resume the active task from its current state, draft the plan when ready, drive implementation after approval, and coordinate review before wrap-up.
disable-model-invocation: true
---

# Resume

Use this skill to resume the active task after `start`, after user answers to open questions, after plan approval, or after review findings need disposition.

## Workflow

1. Read `tasks/current.md`.
2. Read the `## Status` section first and infer the next action from `State:` and `Next action:`.
3. Branch by task state:
   - `awaiting-answers`
     - review the user's answers
     - update the open-question statuses
     - if questions are now resolved, run `plan-task` and `test-matrix`
     - set `State: awaiting-plan-approval`
     - stop for approval
   - `ready-for-plan`
     - run `plan-task`
     - run `test-matrix`
     - set `State: awaiting-plan-approval`
     - stop for approval
   - `awaiting-plan-approval`
     - if the user has not approved the plan, summarise the plan and ask for approval or guidance
     - if the user approved it, set `State: implementing` and begin the next approved phase
   - `implementing`
     - execute the approved plan phase by phase
     - update `tasks/current.md` as work completes
     - update references or docs when relevant
     - when implementation is complete, run these review agents in parallel:
       - `code-reviewer`: independent diff review for bugs, regressions, and test gaps
       - `adversarial-referee`: destructive challenge pass for failure paths and unsafe assumptions
       - `security-auditor`: vulnerability review for injection, credentials, OWASP, and dependency risks
     - **important**: when spawning each agent, instruct it to use semi-formal reasoning
       (see `.claude/rules/semi-formal-reasoning.md`). Every finding must include
       Premises (with file:line citations), Execution/Attack/Counter Trace, and
       Conclusion. Findings without this structure should be rejected or reworked.
     - record all findings in `## Review Findings` of `tasks/current.md`
   - `awaiting-review-disposition`
     - present review findings
     - record whether each item is fixed, accepted, or deferred
     - if items are fixed, continue implementation as needed
     - if all findings are dispositioned, set `State: awaiting-knowledge-proof` or `ready-to-wrap`
   - `awaiting-knowledge-proof`
     - direct the user to `wrap-up`, which will trigger `test-me` at the right point
4. Keep the `## Status`, `## Verification Plan`, and `## Review Findings` sections current throughout.

## Rules

- Do not skip plan approval.
- Do not start coding if unresolved open questions would materially change the plan.
- Before `wrap-up`, do not populate interrogation results, understanding scores, or remediation fields unless the user explicitly asked for an early practice `test-me` run.
- Prefer modular helper workflows:
  - `plan-task`
  - `test-matrix`
  - `checkpoint`
  - `update-references`
- Always run all three review agents (`code-reviewer`, `adversarial-referee`, `security-auditor`) before wrap-up. Do not skip any.
