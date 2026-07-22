# KYROX Roadmap

High-level milestone sequence for the KYROX ecosystem. Live progress is summarized in [STATUS.md](STATUS.md). Detailed scope for each milestone lives in `milestones/`. Application code is implemented in **kyrox-core** and **fair-crm**; this repository is the single source of truth for status and planning.

## Milestones

| Milestone | Name | Status | Document |
|-----------|------|--------|----------|
| **M1** | Foundation | Completed | [M1_FOUNDATION.md](milestones/M1_FOUNDATION.md) |
| **M2** | Identity Platform | Completed | [M2_IDENTITY.md](milestones/M2_IDENTITY.md) |
| **M3** | Platform Services | Completed | [M3_PLATFORM_SERVICES.md](../archive/milestones/M3_PLATFORM_SERVICES.md) |
| **M4** | FAIR CRM v1 | Active | [M4_FAIR_CRM_V1.md](milestones/M4_FAIR_CRM_V1.md) |

## kyrox-core Release History

| Release | Scope |
|---------|-------|
| v0.1.0 | Foundation |
| v0.2.0 | Identity Core |
| v0.2.1 | Authorization Hardening |
| v0.3.0 | Organization & Membership Platform |
| v0.4.0 | Platform Services and product integration baseline |

**Current:** v0.4.0 - platform baseline complete. kyrox-core is frozen except bug fixes, security fixes, performance fixes, and CRM-driven reusable platform needs.

## M1 - Foundation

Establish repository strategy, ecosystem vision, decision workflow, and the kyrox-platform documentation hub. Define the three-repo model and Core vs product separation.

**Primary repo:** kyrox-platform  
**Outcome:** Clear structure and ADRs; team aligned on where work happens.

## M2 - Identity Platform

Implement identity and access foundations in **kyrox-core**: users, organizations, authentication, authorization, and session/token strategy suitable for multi-tenant SaaS.

Security baseline: [ADR-0003](decisions/0003-identity-security-strategy.md). Delivered across kyrox-core **v0.2.0** through **v0.3.0**.

**Primary repo:** kyrox-core  
**Outcome:** Products can authenticate users and scope data by organization.

## M3 - Platform Services

Extend **kyrox-core** with shared platform services consumed by KYROX products.

| Service | Status |
|---------|--------|
| Audit Query API | Completed |
| Audit Event Write API | Completed |
| Product Authorization Check API | Completed |
| Settings Platform | Completed |
| Background Jobs | Completed |
| Notifications | Completed |
| FAIR CRM permission seeds | Completed |
| File Storage | Planned |

Delivered in kyrox-core **v0.4.0** with Alembic head `20260701_0025`.

**Primary repo:** kyrox-core  
**Outcome:** Reusable platform baseline ready for product integration.

## M4 - FAIR CRM v1

Deliver the first shippable version of **fair-crm** on top of Core identity and platform services: CRM workflows, product UI, data integration workflows, and production readiness for initial users.

**Current phase:** Active FAIR CRM product delivery and data-integration pipeline hardening.  
**Primary repo:** fair-crm (with dependencies on kyrox-core)  
**Outcome:** First KYROX product in production; feedback loop into Core and platform planning.

### Current FAIR CRM Delivery Snapshot

- FAIR CRM is active in development.
- Customer, Fair, and Participation foundation modules exist.
- Adapter Management is completed.
- Linked Fairs are completed.
- Fair -> Adapter relationship is completed.
- Adapter CRUD is completed.
- Run v2 + JSON Handoff is completed.
- Next technical target: Canonical Import Schema.
- Following target: Import Batch / Preview / Duplicate / Merge pipeline.

## How To Use This Roadmap

- **Planning and scope changes** - update milestone docs and ADRs in kyrox-platform before large implementation shifts.
- **Implementation** - track code progress in kyrox-core and fair-crm; reference milestone IDs in commits and tags when appropriate.
- **Status updates** - when a milestone or service completes, update [STATUS.md](STATUS.md), this file, and [CHANGELOG.md](CHANGELOG.md).
- **Deferred work** - items intentionally postponed are listed in [KNOWN_DEFERRED.md](KNOWN_DEFERRED.md).

See [../WORKFLOW.md](../WORKFLOW.md) for the end-to-end process from decision to release.
