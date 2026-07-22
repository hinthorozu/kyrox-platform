# AGENTS.md

Guidance for AI agents and automation working in the `kyrox-platform` repository.

## Repository Role

`kyrox-platform` is the KYROX ecosystem management repository. It is the source of truth for roadmap, milestones, product planning, ecosystem ADRs, status, deferred work, and cross-repository coordination.

This repository is not an application repository. Do not add backend, frontend, migrations, tests, or deployable service code here.

## Repository Boundaries

| Repository | Responsibility |
|------------|----------------|
| `kyrox-platform` | Ecosystem strategy, roadmap, status, ADRs, milestones, product planning |
| `kyrox-core` | Reusable SaaS platform services |
| `fair-crm` | CRM product domain, product UI, product database, product data integration |

Core remains product-agnostic. FAIR CRM domain behavior belongs in `fair-crm`.

## Required Reading

Before changing planning or status documents, read:

1. `README.md`
2. `STATUS.md`
3. `ROADMAP.md`
4. `KNOWN_DEFERRED.md`
5. `AI_WORKFLOW.md`
6. Relevant files under `milestones/`, `products/`, and `decisions/`

## Current Product State

FAIR CRM is active in development. It is not "not started".

Current delivery snapshot:

- Customer/Fair/Participation foundation modules exist.
- Adapter Management is completed.
- Linked Fairs are completed.
- Fair -> Adapter relationship is completed.
- Adapter CRUD is completed.
- Run v2 + JSON Handoff is completed.
- Current technical target: Canonical Import Schema.
- Next target: Import Batch / Preview / Duplicate / Merge pipeline.

## Agent Rules

- Update existing canonical documents instead of creating duplicates.
- Keep status, roadmap, milestone, and product files consistent with each other.
- Do not add application code to this repository.
- Do not modify `kyrox-core` or `fair-crm` from inside this repository unless the user explicitly scopes cross-repo documentation work.
- Do not put CRM domain logic into `kyrox-core` planning as platform work.
- Record reusable platform needs as Core candidates only when they are product-agnostic.
- Never mark a milestone complete unless the relevant status and changelog documents are updated.

## Documentation Safety

- Prefer concise status updates over large rewrites.
- Preserve historical context only when it helps; label stale information as historical.
- If a document conflicts with live product status, update the canonical status first, then align roadmap and milestone docs.
- For agent-specific workflow changes, update this file and `AI_WORKFLOW.md`.

## Git Safety

- Do not commit or push unless the user explicitly approves.
- Never revert user changes unless explicitly requested.
- Keep generated artifacts and local outputs out of commits.
