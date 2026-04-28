# Control Plane Hygiene

If `CLAUDE.md` still contains template placeholders (`[PROJECT_NAME]`,
`[Brief description of this project]`, or `[Primary languages, frameworks, and tools]`),
or if `git config core.hooksPath` does not point to `.githooks`:

- Direct the user to run `/init` before proceeding with any task work.
- Do not attempt to auto-configure the control plane outside of the `/init` skill.
