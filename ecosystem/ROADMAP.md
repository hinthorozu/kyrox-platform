# KYROX Ecosystem Roadmap

High-level milestone sequence. Live progress: [STATUS.md](STATUS.md). Product sprint detail: [fair-crm ROADMAP](../projects/fair-crm/ROADMAP.md) and [Core ROADMAP](../projects/kyrox-core/ROADMAP.md).

## Milestones

| Milestone | Name | Status | Document |
|-----------|------|--------|----------|
| **M1** | Foundation | Completed | [archive](../archive/milestones/M1_FOUNDATION.md) |
| **M2** | Identity Platform | Completed | [archive](../archive/milestones/M2_IDENTITY.md) |
| **M3** | Platform Services | Completed | [archive](../archive/../archive/milestones/M3_PLATFORM_SERVICES.md) |
| **M4** | FAIR CRM v1 | **Active** | [MILESTONE_M4](../projects/fair-crm/MILESTONE_M4.md) |

## kyrox-core release history

| Release | Scope |
|---------|-------|
| v0.1.0 | Foundation |
| v0.2.0 | Identity Core |
| v0.2.1 | Authorization Hardening |
| v0.3.0 | Organization & Membership Platform |
| v0.4.0 | Platform Services and product integration baseline |

**Current:** v0.4.0 — platform baseline complete. kyrox-core is frozen except bug fixes, security fixes, performance fixes, and CRM-driven reusable platform needs.

## M1 — Foundation (completed)

Establish repository strategy, ecosystem vision, decision workflow, and the kyrox-platform documentation hub. Define the three-repo model and Core vs product separation.

## M2 — Identity Platform (completed)

Identity and access foundations in kyrox-core: users, organizations, authentication, authorization, session/token strategy. Security baseline: [ADR-0003](decisions/0003-identity-security-strategy.md). Delivered across kyrox-core v0.2.0–v0.3.0.

## M3 — Platform Services (completed)

Shared platform services in kyrox-core: audit, settings, background jobs, notifications, product authorization check, FAIR CRM permission seeds. Delivered in kyrox-core v0.4.0 (Alembic head `20260701_0025`). File Storage remains planned.

## M4 — FAIR CRM v1 (active)

Ship the first KYROX product on Core identity and platform services.

**Primary repo:** `fair-crm`  
**Canonical product status:** [projects/fair-crm/PROJECT_STATUS.md](../projects/fair-crm/PROJECT_STATUS.md)

### Delivery snapshot (do not duplicate sprint tables)

- Customer, Fair, Participation, Contacts, Activities foundations completed
- Adapter management, linked fairs, Run v2 + JSON handoff completed
- Import / Data Integration engine, merge, preview, Excel source adapter completed
- Admin database backups MVP completed
- Responsive UI / UniversalDataTable standard completed
- **Next planned product sprint:** CSV Source Adapter (09.3), then customer emails / admin backup operations tracks

### Planned after M4 (indicative)

- Production hardening and feedback into Core
- Core File Storage and other deferred platform capabilities when product demand requires them ([KNOWN_DEFERRED.md](KNOWN_DEFERRED.md))

## Related

- [STATUS.md](STATUS.md)
- [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md)
- [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md)
