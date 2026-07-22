# KYROX Core Roadmap

This roadmap describes KYROX Core as a reusable SaaS platform service. Core provides platform capabilities that products consume through public APIs. Product domain logic does not belong in this repository.

## Current Status

| Area | Status |
|------|--------|
| Current release | v0.4.0 |
| Platform baseline | Completed |
| Repository mode | Frozen except bug fixes, security fixes, performance fixes, and CRM-driven reusable platform needs |
| Alembic head | `20260701_0025` |
| Test count | 307 passed, 1 skipped |

## Guiding Rule

Design before implementation. Documentation and architectural decisions precede backend code. Core remains product-agnostic; product services integrate through public HTTP APIs and documented contracts.

## Completed Platform Milestones

| Milestone | Status | Scope |
|-----------|--------|-------|
| Sprint 0.1 | Completed - v0.1.0 | Architecture and repository documentation |
| Sprint 0.2 | Completed - v0.1.0 | Backend foundation, tooling, health checks |
| Sprint 0.2.5 | Completed | Backend architecture standards |
| Sprint 0.3 | Completed | Identity platform design |
| Sprint 0.3.2 | Completed - v0.2.0 | Identity persistence |
| Sprint 0.3.3 | Completed - v0.2.0 | Authentication core |
| Sprint 0.3.4 | Completed - v0.2.0/v0.2.1 | Authorization core and hardening |
| Sprint 0.3.5 | Completed - v0.3.0 | Organization and membership platform |
| Sprint 0.4.0 | Completed - v0.4.0 | Platform services |

## Platform Services Baseline

| Service | Status | Notes |
|---------|--------|-------|
| Audit Query API | Completed | Org-scoped audit log listing |
| Audit Event Write API | Completed | Product integration API for append-only audit events |
| Settings Platform | Completed | Org and system scoped settings |
| Background Jobs Platform | Completed | Enqueue and status APIs |
| Notifications Platform | Completed | Async notification dispatch via jobs |
| Product Authorization Check API | Completed | Products check current-user permissions through Core |
| FAIR CRM permission seeds | Completed | Core migration `20260701_0025` seeds customer permissions |
| File Storage | Planned | Future platform capability |

## Product Integration Baseline

The original Sprint 1.0 FAIR CRM product delivery is active; Core integration APIs are available. The reusable Core pieces needed by the first product integration are available as public APIs and documented in [Product Integration Guide](integrations/PRODUCT_INTEGRATION_GUIDE.md).

Current integration capabilities:

- Login, refresh, and logout APIs
- Organization and membership APIs
- Product authorization check API: `POST /api/v1/organizations/{organization_id}/authorization/check`
- Audit event write API: `POST /api/v1/organizations/{organization_id}/audit-events`
- Audit query API
- Settings APIs
- Background jobs APIs
- Notifications APIs
- Product permission seed baseline for FAIR CRM customers in migration `20260701_0025`

Core does not contain FAIR CRM entities, CRM workflows, adapter logic, import pipeline logic, or product UI behavior.

## Active Core Policy During FAIR CRM M4

kyrox-core is frozen except for:

- Bug fixes
- Security fixes
- Performance fixes
- Reusable platform needs discovered during FAIR CRM delivery

Reusable platform needs must remain product-agnostic. If a requested change contains CRM domain behavior, it belongs in `fair-crm`, not `kyrox-core`.

## Future Platform Work

Future work is not scheduled here unless accepted through KYROX planning/ADR flow:

- File storage service
- Webhooks and event bus for product notifications
- Billing and subscription hooks at platform level
- Advanced admin and impersonation policies
- Performance and scaling hardening

Updates to this roadmap should be reflected here and in ADRs when scope or priorities change.
