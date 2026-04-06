---
name: build-level-1
description: Coaching-first build helper for narrow seams where the human should author first and the agent should escalate help gradually.
disable-model-invocation: true
---

# Build Level 1

Use this helper when `## Build Configuration` specifies `Level: 1`.

## Workflow

1. Read `tasks/current.md`, especially `## Work Configuration`, `## Task Brief`, `## Build Configuration`, `## Execution Notes`, `## Ownership Evidence`, and the approved `## Plan`.
2. Select the smallest meaningful seam or section.
3. Ask the human to attempt the seam first or explain the intended approach before drafting.
4. Escalate assistance gradually:
	- question
	- hint
	- pseudocode or outline
	- tiny sketch
	- small patch or paragraph example
	- fuller draft only if explicitly requested
5. Update `## Execution Notes` and `## Ownership Evidence` with the active seam, assistance level reached, human-authored-first status, and any unresolved risk.
6. Pause when a new file, public interface, validation/security path, failure path, or unstated assumption makes the seam higher risk.

## Rules

- Do not lead with a full solution.
- Use research or drafting language instead of implementation-mode language for non-code deliverables.
- Keep seams small and reviewable.