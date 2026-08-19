# AGENTS.md — KYROX knowledge entry

This file is the mandatory entry point for AI agents and a concise routing guide for humans working anywhere in the KYROX ecosystem.

## Fundamental rule

> **Humans and AI agents learn KYROX from `kyrox-platform`. Application repositories are implementation and verification layers.**

Do not treat documentation, chat history, local conventions or tool-specific rule files in `fair-crm` / `kyrox-core` as independent sources of truth. Human-readable rules belong here.

## Required reading order

1. [ecosystem/DOCUMENT_GOVERNANCE.md](ecosystem/DOCUMENT_GOVERNANCE.md)
2. [standards/README.md](standards/README.md)
3. [ecosystem/WORKFLOW.md](ecosystem/WORKFLOW.md)
4. Open the owning project entry:
   - Fair CRM → [projects/fair-crm/README.md](projects/fair-crm/README.md)
   - Core → [projects/kyrox-core/README.md](projects/kyrox-core/README.md)
5. If the task changes current state or planned work, also read:
   - [ecosystem/STATUS.md](ecosystem/STATUS.md)
   - [ecosystem/ROADMAP.md](ecosystem/ROADMAP.md)

## How to decide what to read

- **Reusable behavior across products** → `standards/` first.
- **Fair CRM-only behavior/domain/UI** → `projects/fair-crm/` after applicable shared standards.
- **Core-only architecture/API behavior** → `projects/kyrox-core/` after applicable shared standards.
- **Cross-repo strategy/workflow/ownership** → `ecosystem/`.
- **Historical material** → `archive/`; never use it as a live rule unless a canonical document explicitly says so.

For CRUD, permission-driven UI visibility, route/action gating and backend authorization, read [standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md](standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md) before any product-specific UI document.

## Precedence

When documents appear to overlap:

1. Shared standard governs reusable semantics.
2. Project document may add product-specific detail but must not silently redefine the shared rule.
3. An explicit, documented project exception may override a shared default only for that project and must link back to the shared standard.
4. Archive and chat history never override live canonical documents.

## Hard rules

- This repository contains the human/AI knowledge base; do not add application code here.
- Do not duplicate human-readable documentation into `fair-crm` or `kyrox-core`.
- One topic has one canonical source. Merge duplicate rules; use links for context instead of copied normative text.
- Reusable rules go to `standards/`; product-only rules go to `projects/<name>/`.
- Machine-readable contracts needed by CI/runtime may stay in code repositories, but they are not a second human documentation system.
