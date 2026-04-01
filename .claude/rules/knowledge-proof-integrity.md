---
globs: tasks/**
---

# Knowledge-Proof Integrity

When editing any file in `tasks/`:

- NEVER write, update, or pre-fill the "Interrogation Result", "Understanding Scores",
  or "Understanding Remediation" sections unless the `test-me` skill is actively running
  and the human has actually answered questions.
- NEVER invent a passing or failing knowledge-proof result.
- NEVER auto-populate score values (e.g. "Flow accuracy: 4/5") without live human responses.
- The Knowledge Proof section must remain as placeholder text until `test-me` is invoked.

This rule exists because multiple skills embed this guardrail, but freeform edits
to task files can bypass skill orchestration entirely.
