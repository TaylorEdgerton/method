---
globs: tasks/**
---

# Task File Discipline

When editing `tasks/current.md`:

- Always update the **Status** field to reflect the current phase when making changes.
  Valid statuses: `not-started`, `researching`, `awaiting-answers`, `ready-for-plan`,
  `awaiting-plan-approval`, `implementing`, `awaiting-review-disposition`,
  `awaiting-knowledge-proof`, `wrapping-up`, `done`.
- Never delete or blank out existing sections — only append or update content.
- Never check off acceptance-criteria boxes unless the work is verifiably complete
  in the repo (commits exist, files changed). Use repo evidence, not intent.
- When archiving to `tasks/completed/`, the filename must include the story ID
  (e.g., `US-003-feature-name.md`).
