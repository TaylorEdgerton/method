---
name: init
description: One-time control-plane bootstrap for a project — validate configuration, populate project identity files, ask about domain skills, and set up git hooks.
disable-model-invocation: true
---

# Init

Use this skill when binding the template control plane to a real project after cloning the
template. It validates the target repo, fills in the project identity files, and configures
the control plane so that `/prepare`, `/build`, and `/finalise` can function correctly.

## Pre-flight

1. Run `python3 scripts/ensure_control_plane.py`.
2. If exit code is **0**, tell the user the project is already configured and stop.
3. If exit code is **2** or **3**, proceed with the bootstrap steps below.

## Workflow

1. **Project identity** — ask the user for:
   - Project name
   - Short description (1–2 sentences)
   - Primary stack (languages, frameworks, tools)
2. **Populate CLAUDE.md** — replace the placeholder values with the consuming
   project's identity:
   - `[PROJECT_NAME]` → user-provided name
   - `[Brief description of this project]` → user-provided description
   - `[Primary languages, frameworks, and tools]` → user-provided stack
3. **Populate README.md** — replace the placeholder values with the consuming
   project's identity:
   - `[Project Name]` → user-provided name
   - `[Short description]` → user-provided description
4. **Configure git hooks** — run `git config core.hooksPath .githooks`.
5. **Domain skills** — list the domain-specific skills currently in `.claude/skills/`
   (e.g., `ignition-scada`) and ask the user:
   - Which domain skills to keep
   - Whether to remove any that don't apply to their project
   Remove any skill directories the user chooses to discard (from both
   `.claude/skills/` and `.agents/skills/`).
6. **Agent review** — list the specialist agents in `.claude/agents/` and ask
   the user whether any should be removed for their project.
7. **Verify** — run `python3 scripts/ensure_control_plane.py` again and confirm
   exit code is **0**.
8. Summarise what was configured and tell the user to run `/prepare` when ready.

## Rules

- This skill is idempotent — running it again should detect what's already done
  and only prompt for missing items.
- Do not modify workflow skills (`prepare`, `build`, `finalise`, etc.) — only
  domain skills and project identity files.
- Do not create git commits or push. The user decides when to commit.
- If the user wants to skip a step (e.g., keep all agents), respect that.
