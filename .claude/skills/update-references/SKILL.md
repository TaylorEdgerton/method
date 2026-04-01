---
name: update-references
description: Refresh docs/scriptReferences.md by scanning the project for scripts, queries, and event handlers and writing a concise reference inventory.
disable-model-invocation: true
---

# Update References

Use this skill when scripts, handlers, queries, or repeatable workflow assets have changed and `docs/scriptReferences.md` needs to be refreshed.

## Workflow

1. Scan the project structure for relevant script files, query files, and UI event-handler files.
2. Read each relevant file and extract the best short description available from the first docstring or comment block.
3. When relevant, capture:
   - key functions and important parameters
   - SQL summary and named parameters
   - component path and event type for UI handlers
4. Rewrite `docs/scriptReferences.md`.
5. Preserve the main category structure unless the repo clearly needs a better equivalent grouping.
6. Show a concise summary of what changed.

## Rules

- Keep descriptions factual and one line where possible.
- Do not invent categories or behaviour that the code does not support.
- If a section has no entries, leave it empty or note that nothing relevant was found.
