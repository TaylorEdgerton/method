# Semi-Formal Reasoning for Code Review

Based on Meta's "Agentic Code Reasoning" research (arXiv:2603.01896), all code
review findings must use semi-formal reasoning — a structured evidence chain
that prevents unsupported claims and surface-level pattern matching.

## Principle

Every review finding (from any agent, skill, or freeform review) must include:

1. **Premises**: Explicitly stated code facts with file:line citations.
   No assumptions, no guesses — only verifiable evidence from the codebase.
2. **Execution Trace**: Step-by-step tracing of the concrete code path
   that demonstrates the issue. Follow actual function calls and data flows
   rather than guessing behavior from naming conventions.
3. **Conclusion**: A determination derived *only* from the stated premises
   and traced paths. Must include a confidence level and explain why this
   is not a false positive.

## When This Applies

- Agent-driven reviews (`code-reviewer`, `adversarial-referee`, `security-auditor`)
- Freeform "review this diff" requests
- Any skill that produces review findings
- Inline review comments during implementation

## Anti-Patterns (do NOT do these)

- "This looks like it could be a bug" without tracing the actual code path
- "Function X might not handle Y" without citing the function body
- Flagging a risk based on naming conventions without verifying behavior
- Conclusions that reference code not shown in premises

## Why

Semi-formal reasoning reduced code review errors by nearly half in Meta's
evaluation, improving accuracy from 78% to 88-93%. The structured format
makes findings auditable — reviewers can verify each premise independently.
