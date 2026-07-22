# M4 — FAIR CRM v1

- **Status:** Active
- **Current phase:** Active product delivery
- **Primary code repository:** fair-crm
- **Documentation:** [projects/fair-crm/](./)

> Historical note: Early M4 drafts said the next technical target was “Canonical Import Schema → Import Batch/Preview/Merge.” That pipeline has since shipped (Fair CRM sprints 09.0–09.2). Live detail: [PROJECT_STATUS.md](PROJECT_STATUS.md).

## Goal

Ship the first production-ready version of FAIR CRM on KYROX Core identity (M2) and platform services (M3).

Application code lives in **fair-crm**. Documentation and decisions live in **kyrox-platform**. kyrox-core remains frozen except bug/security/performance fixes and CRM-driven reusable platform needs.

## Prerequisites (met)

- [x] M2 Identity Platform — kyrox-core v0.2.0 through v0.3.0
- [x] M3 Platform Services — kyrox-core v0.4.0
- [x] Core product-integration APIs: authorization check, audit write, settings, jobs, notifications

## Current delivery snapshot

Summary only — canonical detail in [PROJECT_STATUS.md](PROJECT_STATUS.md):

- Customer, Fair, Participation, Contacts, Activities foundations completed
- Adapter management, linked fairs, Run v2 + JSON handoff completed
- Data Integration / Import Engine / merge / preview completed
- Universal Source Adapter Framework + Excel adapter completed
- Admin database backups MVP completed
- Responsive UniversalDataTable standard completed
- **Next planned sprint:** CSV Source Adapter (09.3)

## Scope

- Core CRM workflows and domain model
- Product UI integrated with Core auth and organization scoping
- Configuration and deployment for initial users
- Product-specific integrations not belonging in Core
- Data-integration pipeline (preview, duplicate detection, merge decisions) — largely shipped; remaining adapters and ops hardening continue under M4

## Dependencies

- kyrox-core **v0.4.0** (frozen baseline)
- [README.md](README.md)

## Success criteria

- FAIR CRM v1 deployable and usable by target initial users
- No reverse dependency from kyrox-core to fair-crm
- Status / roadmap / changelog kept current under this documentation hub
- CRM-driven Core gaps implemented in kyrox-core only when reusable across products ([ADR-0002](../../ecosystem/decisions/0002-core-product-separation.md))

## Related

- [PROJECT_STATUS.md](PROJECT_STATUS.md)
- [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md)
- [../../ecosystem/ROADMAP.md](../../ecosystem/ROADMAP.md)
- [../../ecosystem/WORKFLOW.md](../../ecosystem/WORKFLOW.md)
