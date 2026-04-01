---
globs: docs/**
---

# Diagram Documentation

When creating or updating documentation in `docs/`:

- Use Mermaid syntax for all diagrams (class, sequence, flowchart, state, ER).
  Do not use image-based diagrams or external diagram tool links.
- Keep each diagram under 20 nodes. Split complex systems into multiple
  focused diagrams (e.g., separate component overview from detailed class hierarchy).
- Add a one-line prose description above each diagram explaining what it shows.
- Use naming conventions that match actual codebase identifiers
  (class names, function names, file paths).
- When code changes materially alter architecture (new components, changed
  data flow, modified class hierarchies), remind the user to update
  relevant diagrams in `docs/`.
