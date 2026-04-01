---
name: compound-refresh
description: Periodically review docs/learnings/ to prune stale lessons, consolidate overlapping ones, and keep the knowledge base current.
disable-model-invocation: true
---

# Compound Refresh

Use this skill periodically to maintain the quality of the learnings knowledge base.

## Workflow

1. Scan all files in `docs/learnings/` (excluding `archived/`).
2. For each lesson, assess:
   - Is it still relevant to the current codebase and workflow?
   - Has it been outdated by newer work, skill changes, or rule changes?
   - Does it overlap substantially with another lesson?
   - Has the recommendation (if any) been actioned into a skill or rule update?
3. Classify each lesson into one of:
   - **keep**: still accurate and useful, no changes needed
   - **update**: correct but needs revision (e.g., new context, better example)
   - **consolidate**: merge with one or more overlapping lessons
   - **archive**: no longer relevant; move to `docs/learnings/archived/`
   - **delete**: factually wrong or completely superseded
4. Present findings to the user in a summary table before making any changes.
5. Only proceed with changes after user approval.
6. For archived lessons, move them to `docs/learnings/archived/`
   (create the directory if it does not exist).
7. Commit changes with a descriptive message noting what was refreshed.

## Rules

- Never delete or archive lessons without user confirmation.
- When consolidating, preserve the most useful content from each source lesson.
- Maintain the filename format and frontmatter structure for all updated or
  consolidated lessons.
- If a lesson's recommendation has been actioned, note that in the lesson
  before archiving it.
