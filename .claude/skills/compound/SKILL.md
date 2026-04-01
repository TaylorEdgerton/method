---
name: compound
description: After task completion, capture reusable lessons learned into docs/learnings/ for future reference.
disable-model-invocation: true
---

# Compound Learning

Use this skill after task completion to capture reusable insights that might benefit future work. This captures *knowledge*, not debt — debt and deferred work belong in `/follow-up-triage`.

## Workflow

1. Read `tasks/current.md`, focusing on:
   - `## Review Findings`
   - `## Understanding Remediation`
   - `## Override / Audit Note`
   - `## Notes`
2. Identify reusable insights:
   - patterns discovered during implementation
   - pitfalls avoided or encountered
   - architectural decisions and their rationale
   - tool or workflow usage discoveries
   - non-obvious constraints learned from the codebase
3. Filter out trivial fixes. A lesson is worth documenting if it would
   save time or prevent mistakes on a future task.
4. Check `docs/learnings/` for existing related lessons:
   - if a closely related lesson exists, update it rather than creating a duplicate
   - if a lesson partially overlaps, reference the existing one
5. Write the lesson file in `docs/learnings/` using the filename format
   `YYYY-MM-DD-short-description.md` with:
   - YAML frontmatter: `date`, `task` (story ID), `category`, `tags` (list)
   - Structured markdown sections:
     - `## Problem / Context`
     - `## Discovery`
     - `## Solution / Pattern`
     - `## Why It Works`
     - `## When To Apply`
     - `## Related` (links to other learnings, decisions, or docs)
6. If the lesson suggests an improvement to an existing skill, rule, or agent,
   note that as a `## Recommended Workflow Update` section at the end of the
   lesson file. Do not auto-edit skills or rules — surface the recommendation
   for the user to act on.
7. Check whether `CLAUDE.md` or `AGENTS.md` reference `docs/learnings/`.
   If not, note it but do not add references automatically.

## Rules

- Only document insights that have genuine reuse value.
- Do not create a lesson for every task.
- Keep lessons concise and actionable — aim for under 50 lines.
- Do not duplicate what `/follow-up-triage` captures. If it is debt, it goes
  to the backlog or issues. If it is knowledge, it goes here.
