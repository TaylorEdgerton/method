---
globs: scripts/**
---

# Script Change Hygiene

After modifying, adding, or removing any file in `scripts/`:

- Remind the user to run `/update-references` to refresh `docs/scriptReferences.md`.
- If the change alters CLI arguments, environment variables, or behavioral contracts
  of a script, note this explicitly so the user can verify downstream consumers
  (e.g., `.githooks/pre-push` calls `check_understanding_gate.py` with specific flags).
