---
name: build-level-3
description: Collaborative build helper that proposes small concrete seams with intent-first explanations and approval pauses.
disable-model-invocation: true
---

# Build Level 3

Use this helper when `## Build Configuration` specifies `Level: 3`.

## Workflow

1. Read `tasks/current.md`, especially `## Work Configuration`, `## Task Brief`, `## Build Configuration`, `## Execution Notes`, `## Ownership Evidence`, and the approved `## Plan`.
2. Select the next smallest meaningful seam or section.
3. Before each step, explain:
	- the sub-problem being solved
	- the file or section being changed
	- the acceptance criterion or objective being targeted
	- the main tradeoff
4. Propose one small concrete patch, section, or revision at a time.
5. Wait for approval before continuing to the next seam.
6. Update `## Execution Notes` and `## Ownership Evidence` with the active seam, assistance level reached, human review checkpoints, and any unresolved risk.
7. Pause on new files, interface changes, security-sensitive paths, failure handling changes, or unstated assumptions.

## Rules

- Keep changes small, coherent, and reviewable.
- Use research or drafting language for non-code deliverables.
- Do not silently batch unrelated seams together.