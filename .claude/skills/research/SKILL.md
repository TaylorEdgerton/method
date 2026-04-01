---
name: research
description: Research the active task by finding the relevant files, patterns, constraints, and open questions, then writing grounded findings and proposed answers into tasks/current.md.
disable-model-invocation: true
---

# Research

Use this skill when the active task needs a codebase reconnaissance pass before planning or implementation.

## Workflow

1. Read `tasks/current.md` to understand the active story and acceptance criteria.
2. Read `docs/scriptReferences.md` when it is relevant for quick structure context.
3. Find the files, modules, scripts, tests, docs, and configuration most relevant to the task.
4. Read enough of those files to understand:
   - current patterns
   - data flow and dependencies
   - constraints and conventions
   - likely edge cases or gotchas
5. Update the `## Research` section in `tasks/current.md` with:
   - relevant files and why they matter
   - patterns the implementation should follow
   - constraints or gotchas
   - open questions
6. For each open question, attempt a proposed answer first and record whether the question is:
   - unresolved
   - resolved by repo evidence
   - resolved by user answer
7. Update the task status fields:
   - `State: awaiting-answers` if unresolved questions remain
   - otherwise `State: ready-for-plan`
   - `Next action:` should clearly state whether the user must answer questions or run `resume`

## Rules

- Keep the research grounded in what actually exists in the repo.
- Do not write the implementation plan yet.
- Do not propose solutions beyond documenting current reality and unanswered questions.
- Do not edit the knowledge-proof, interrogation, score, remediation, or override sections during research.
