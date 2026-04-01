---
name: test-matrix
description: Define the explicit verification plan for the active task by mapping acceptance criteria and risk areas to checks, manual validation, and known gaps.
---

# Test Matrix

Use this skill after research or planning to make verification explicit before wrap-up.

## Workflow

1. Read `tasks/current.md`, including:
   - acceptance criteria
   - research findings
   - plan
   - risk areas
2. Update `## Verification Plan` with:
   - required automated checks
   - required manual checks
   - edge cases to verify
   - known gaps or intentionally untested areas
3. Tie checks back to the plan and the highest-risk parts of the implementation.
4. If a task has weak or missing test coverage, say so clearly.

## Rules

- This skill is for planning and documentation, not deterministic enforcement.
- Do not claim that checks passed unless they have actually been run.
- Prefer a small, actionable verification plan over an exhaustive list.
