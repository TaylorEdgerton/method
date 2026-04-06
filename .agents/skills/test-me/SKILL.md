---
name: test-me
description: Run the knowledge-proof workflow on the active task, score human understanding against the implementation, and record remediation when needed.
---

# Test Me

Run the knowledge-proof workflow on the current task so the human must demonstrate operational understanding of the implementation before finalise.

## Workflow

1. Read `tasks/current.md`, the active story, the acceptance criteria, the current diff, and the changed files.
2. Read the `## Verification Plan`, `## Review Findings`, `## Build Configuration`, and `## Ownership Evidence` sections when they exist.
3. Identify the most important implementation flows, trust boundaries, edge cases, failure states, and any open findings the human should be able to explain.
4. Decide whether this task needs a knowledge proof.

A knowledge proof is required when the task changes any of the following:

- code
- logic
- data flow
- automation
- schema
- scripts
- validation
- permissions
- error handling
- state transitions

If the task is documentation-only or otherwise non-implementation work, record that in `tasks/current.md` and stop.

5. Populate or update the `## Knowledge Proof` section in `tasks/current.md` with:

- proof required yes or no
- changed files
- key flows under test
- main risk areas

6. Default to live human interrogation, but scale intensity to the selected build level and the risk areas still unresolved after reviewing `## Ownership Evidence`.

Use `Interview mode: self-test` only if the user explicitly asked for a solo rehearsal or dry run.

Do not answer the questions on the human's behalf, and do not write scores, pass or fail outcomes, or remediation results until you have actually asked questions and received answers.

7. Interrogate the human with targeted questions based on the real implementation and diff, not just the user story.

Use short, direct questions. Prefer one question at a time.

Question types should include:

- main data or control flow
- key branches and fallback paths
- edge cases and malformed input
- failure states and recovery paths
- trust boundaries and misuse or security risks
- mapping between acceptance criteria and implementation
- likely bug or regression points
- change-impact reasoning such as "what breaks if this guard is removed?"

Do not ask the user to recite code line by line.

8. For higher-risk work, optionally run a referee-assisted pass:
   - use a second model or session with an adversarial brief
   - ask it for breakages, security bypasses, contradictions, and failure cases
   - turn the strongest findings into follow-up questions

9. Score the human against this rubric:

- Flow accuracy: 0-5
- Branch coverage: 0-5
- Failure-state awareness: 0-5
- Edge-case awareness: 0-5
- Security or misuse awareness: 0-5
- Acceptance-criteria traceability: 0-5

10. Then calculate:

- Total score: `/30`
- Percent score: `/100`
- Equivalent pass threshold: `8/10`

11. Interpret the result as:

- `85-100%`: strong understanding, pass
- `70-84%`: acceptable but gaps must be recorded
- `60-69%`: fail, remediation required before wrap-up
- `<60%`: fail with strong warning, remediation required and likely unsafe to wrap up without override

When reporting the result, also state whether the score is above or below the `8/10` equivalent threshold.

12. If the human scores below the threshold:

1. Do not proceed straight to wrap-up.
2. Enter remediation mode.
3. Tell the human exactly what they missed.
4. Allow them to ask questions about the codebase and implementation.
5. Answer in a teaching mode focused on:
   - intent
   - flow
   - branch logic
   - failure behaviour
   - recovery behaviour
   - acceptance-criteria mapping
6. Do not simply dump a line-by-line paraphrase of the code unless needed to resolve a specific gap.
7. Re-test using varied questions covering the same implementation from different angles.
8. Record the initial score, gaps, training questions asked, final score, and residual debt in the `## Understanding Remediation` section.

## Anti-Bluff Guidance

Do not claim to detect AI-generated answers with high confidence.

Instead, reduce bluffing value by using:

- live follow-up questions
- localised questions tied to changed files
- mutation questions such as "what changes if this guard is removed?"
- acceptance-criteria-to-code mapping questions
- varied re-test questions rather than repeating the same prompts

The goal is not to prove the user avoided AI help. The goal is to verify that the user can still demonstrate operational understanding under questioning.

## Tools

- Use `scripts/record_understanding.py` when possible instead of hand-editing fragile score sections.
- This skill supplements tests, linting, and quality checks rather than replacing them.

## Output

Update `tasks/current.md` with:

- `## Knowledge Proof`
- `## Understanding Remediation` if needed
- scores
- gaps found
- pass or fail outcome
- residual understanding debt

Then provide a concise summary including:

- whether the user passed
- the score
- the most important gaps
- whether remediation is required before `finalise`
- any review findings or verification gaps that materially affected the score

## Behaviour Rules

- Be firm but constructive.
- Prefer grounded, implementation-specific questioning.
- Do not let a polished generic explanation count as a pass.
- Do not treat a model-authored summary as evidence that the human understands the change.
- Do not mark the knowledge proof as passed unless the human shows enough understanding to safely own the change.
- Use the lightest proof that still demonstrates ownership for lower-risk Level 1 to 2 work, and a stronger proof for higher-risk or more autonomous Level 3 to 4 work.
