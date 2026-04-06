---
name: build-level-4
description: Autonomous build helper for explicit high-autonomy execution where speed matters more than first-draft authorship.
---

# Build Level 4

Use this helper when `## Build Configuration` specifies `Level: 4`.

## Workflow

1. Read `tasks/current.md`, especially `## Work Configuration`, `## Task Brief`, `## Build Configuration`, `## Execution Notes`, `## Ownership Evidence`, and the approved `## Plan`.
2. Work through the approved phases efficiently, using larger seams when appropriate.
3. Keep acceptance-criteria mapping and reviewability explicit even when editing multiple files.
4. Update `## Execution Notes` and `## Ownership Evidence` with the active seam, autonomy level, major tradeoffs, and unresolved risks.
5. Pause when the task crosses a trust boundary, introduces a new abstraction, changes a public interface, or depends on an unstated assumption that could materially change the outcome.

## Rules

- Level 4 must remain explicit rather than becoming the silent default.
- Keep the work reviewable and acceptance-criteria anchored.
- Increase ownership-evidence capture for higher-risk changes.