# AI Development Entry Point

This file is an entry point only. It does **not** define a second set of development rules.

## Canonical sources

AI agents and human developers must follow these sources in precedence order for the work they are performing:

1. [`ecosystem/DOCUMENT_GOVERNANCE.md`](../../ecosystem/DOCUMENT_GOVERNANCE.md) — documentation ownership and single-source-of-truth rules.
2. [`ecosystem/WORKFLOW.md`](../../ecosystem/WORKFLOW.md) — human/AI execution process, ambiguity gate, Git behavior, verification and documentation sync.
3. [`standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md`](../backend/BACKEND_ARCHITECTURE_STANDARDS.md) — backend architecture and layering.
4. Owning project constitution, architecture, ADRs and project-specific standards under `projects/<project>/`.
5. Task-specific instructions explicitly approved by the user, provided they do not silently contradict an unchanged canonical rule.

## Rule

Do not restate workflow, Git, architecture, testing, naming, or project rules in this file. If a rule changes, update its canonical owner above.
