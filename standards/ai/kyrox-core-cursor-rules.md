# KYROX Core AI Entry Point

This file is an entry point for AI agents working on `kyrox-core`. It is **not** an independent rule set.

## Required canonical sources

1. [`../../ecosystem/WORKFLOW.md`](../../ecosystem/WORKFLOW.md) — execution workflow, ambiguity gate, Git behavior and verification.
2. [`../backend/BACKEND_ARCHITECTURE_STANDARDS.md`](../backend/BACKEND_ARCHITECTURE_STANDARDS.md) — Core backend architecture, layering, repository pattern and testing expectations.
3. [`../../projects/kyrox-core/README.md`](../../projects/kyrox-core/README.md) — Core project entry point.
4. Relevant Core ADRs and integration contracts under [`../../projects/kyrox-core/`](../../projects/kyrox-core/).

## Rule

Do not duplicate or override architecture, repository, mapper, testing, workflow, Git or output-format rules here. If Core needs a new permanent technical rule, add it to the appropriate canonical backend/Core document. If the requirement is ambiguous or changes product/platform behavior, follow the ambiguity gate in `ecosystem/WORKFLOW.md` and ask before implementation.
