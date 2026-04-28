# Git Safety

- NEVER use `--no-verify` on any git command. The pre-push hook runs
  `check_understanding_gate.py` and must not be bypassed.
- NEVER force-push (`git push --force` or `git push -f`).
- NEVER push directly to `main` without explicit user confirmation.
- NEVER amend a published commit (one that has been pushed).
- If the understanding gate blocks a push, do not retry with `--no-verify`.
  Instead, address the gate failure: run `/test-me` or add an Override/Audit Note
  in `tasks/current.md`.
