---
globs: docs/learnings/**
---

# Learnings File Format

When creating or editing files in `docs/learnings/`:

- Use the filename format: `YYYY-MM-DD-short-description.md`
- Each lesson file must include YAML frontmatter with:
  - `date`: the date the lesson was captured (YYYY-MM-DD)
  - `task`: the story ID or task that produced the lesson
  - `category`: a short category label (e.g., architecture, testing, tooling, security)
  - `tags`: a list of keyword tags
- Each lesson must include these structured sections:
  - `## Problem / Context`
  - `## Discovery`
  - `## Solution / Pattern`
  - `## Why It Works`
  - `## When To Apply`
  - `## Related`
- Keep lessons concise. If a lesson exceeds ~50 lines, consider splitting it.
- Created by `/compound` or manually — either way, same format.
