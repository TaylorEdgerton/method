# Review and Documentation Enforcement

When editing `tasks/current.md` or skill files that orchestrate task completion:

- Before moving a task to `awaiting-review-disposition` or `ready-to-wrap`, the
  `## Review Findings` section must include results from all three review agents:
  - `code-reviewer`
  - `adversarial-referee`
  - `security-auditor`
- Do not skip any of the three review agents. If one finds no issues, record
  "no findings" for that agent rather than omitting the section.
- Before archiving a task that changed code, the `documentation-engineer` agent
  must have been run to update relevant documentation (Mermaid diagrams, ADRs,
  API docs).
- If documentation was already current and no updates were needed, record that
  explicitly rather than silently skipping the step.
