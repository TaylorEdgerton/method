# Repo Agent Policy

This repository uses a skill-first workflow with explicit build levels.

## Runtime locations

- Claude Code skills: `.claude/skills/`
- Claude Code agents: `.claude/agents/` (markdown)
- Claude Code rules: `.claude/rules/` (glob-matched)
- Codex skills: `.agents/skills/`
- Codex subagents: `.codex/agents/` (TOML)

## Required workflow for implementation tasks

For tasks that change code, logic, automation, validation, permissions, state transitions, schema, scripts, or error handling:

1. Keep `tasks/current.md` updated during the task.
2. Use `prepare` to activate work and `build` to move it through planning, implementation, and review.
3. Choose an explicit build level before implementation begins and record the build profile in `tasks/current.md`.
4. Record review findings, verification planning, execution notes, and ownership evidence in `tasks/current.md`.
5. If the understanding result is below threshold, complete remediation or add an override note before `finalise`.
6. Run the `finalise` skill before committing or pushing final changes.
7. Treat the knowledge proof as a human interrogation step. Do not pre-fill scores, gaps, or remediation during `prepare`, `research`, or planning.

## Knowledge-proof threshold

Normal ownership threshold is `8/10` equivalent.

- `>= 85%`: strong understanding
- `70-84%`: acceptable, but record gaps
- `60-69%`: remediation required before `finalise`
- `<60%`: do not finalise without an explicit override note

## Files that matter

- Active task record: `tasks/current.md`
- Task template: `tasks/current-template.md`
- Archived completed tasks: `tasks/completed/`
- Backlog: `docs/backlog.md`
- Script references: `docs/scriptReferences.md`
- Learnings knowledge base: `docs/learnings/`
- Strict style mockup html: `docs/mockup.html`

## Workflow skills

- User-facing entry points:
  - `init`: one-time project bootstrap — configure the control plane, populate CLAUDE.md, set up hooks
  - `prepare`: activate the next or selected backlog story, run research, and capture the Task Brief
  - `build`: materialize the execution plan, route work through the selected build level, and coordinate review
  - `finalise`: finish, archive, and reset the active task while enforcing the scaled understanding gate
- Internal helper skills:
  - `research`
  - `plan-task`
  - `test-matrix`
  - `checkpoint`
  - `build-level-1`
  - `build-level-2`
  - `build-level-3`
  - `build-level-4`
  - `update-references`
  - `test-me`
  - `follow-up-triage`
  - `compound`
  - `compound-refresh`

## Deterministic enforcement

The repo uses deterministic local enforcement in `.githooks/pre-push`,
`scripts/check_understanding_gate.py`, and `scripts/record_understanding.py`.
Do not bypass these checks silently.

Claude Code users: authoritative guardrails live in `.claude/rules/` (glob-matched).
This file duplicates key rules for Codex compatibility, which does not read `.claude/rules/`.

## Subagents

Codex subagent definitions live in `.codex/agents/` as TOML files. Available agents:

- `code-reviewer`: independent code review focused on bugs and regressions
- `adversarial-referee`: destructive challenge pass on implementations
- `security-auditor`: vulnerability-focused security review
- `technical-architect`: solution design and architecture decisions
- `product-backlog-manager`: user story creation and prioritisation
- `python-feature-dev`: Python feature implementation
- `frontend-developer`: HTML/CSS/JS/Astro implementation
- `documentation-engineer`: Mermaid diagrams, ADRs, living docs
- `qa-automation`: test suite implementation
- `k8s-gitops-architect`: Kubernetes GitOps and Helm/Kustomize

Claude Code equivalents live in `.claude/agents/` as markdown files with the same names.

## Codex guardrails

- Do not pre-fill knowledge-proof scores or remediation before `test-me` questions the user.
- Do not bypass the pre-push hook with `--no-verify` or equivalent.
- Do not force-push or push directly to `main` without explicit user confirmation.
- Keep `tasks/current.md` current throughout the task.
- Record Work Configuration, Task Brief, Build Configuration, Execution Notes, and Ownership Evidence as the task progresses.
- Use the `US-XXX` format for backlog story IDs; never renumber existing stories.
- Use Mermaid syntax for all diagrams in `docs/`.
- After modifying scripts, remind the user to run `update-references`.

## Agent behaviour

Keep this file small. Use skills for the full workflow logic.
