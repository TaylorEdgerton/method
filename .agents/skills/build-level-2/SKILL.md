---
name: build-level-2
description: Structure-first build helper that provides outlines and implementation framing without taking over authorship of the final artifact.
---

# Build Level 2

Use this helper when `## Build Configuration` specifies `Level: 2`.

## Workflow

1. Read `tasks/current.md`, especially `## Work Configuration`, `## Task Brief`, `## Build Configuration`, `## Execution Notes`, `## Ownership Evidence`, and the approved `## Plan`.
2. Select the next smallest meaningful seam or section.
3. Provide structure rather than a near-final artifact:
   - pseudocode
   - outlines
   - branch shape
   - invariants
   - edge cases
   - section framing
4. Leave local implementation or prose choices to the human, then review the human's work.
5. Update `## Execution Notes` and `## Ownership Evidence` with the active seam, assistance level reached, human-authored-first status, and any unresolved risk.
6. Pause on new files, interface changes, security-sensitive flows, failure handling changes, or unstated assumptions.

## Rules

- Do not provide full production-ready code or full polished prose first.
- Use research or drafting language for non-code deliverables.
- Keep seams small and reviewable.