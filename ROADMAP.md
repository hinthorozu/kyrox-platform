# KYROX Roadmap

High-level milestone sequence for the KYROX ecosystem. Live progress is summarized in [STATUS.md](STATUS.md). Detailed scope for each milestone lives in `milestones/`.

## Milestones

| Milestone | Name               | Status        | Document |
|-----------|--------------------|---------------|----------|
| **M1**    | Foundation         | ✅ Completed  | [M1_FOUNDATION.md](milestones/M1_FOUNDATION.md) |
| **M2**    | Identity Platform  | ✅ Completed  | [M2_IDENTITY.md](milestones/M2_IDENTITY.md) |
| **M3**    | Platform Services  | 🚧 Active     | [M3_PLATFORM_SERVICES.md](milestones/M3_PLATFORM_SERVICES.md) |
| **M4**    | FAIR CRM v1        | ⏳ Planned    | [M4_FAIR_CRM_V1.md](milestones/M4_FAIR_CRM_V1.md) |

## M1 — Foundation ✅

Establish repository strategy, ecosystem vision, decision workflow, and the kyrox-platform documentation hub. Define the three-repo model and Core vs product separation.

**Primary repo:** kyrox-platform  
**Outcome:** Clear structure and ADRs; team aligned on where work happens.

## M2 — Identity Platform ✅

Implement identity and access foundations in **kyrox-core**: users, organizations (account boundary), authentication, authorization, and session/token strategy suitable for multi-tenant SaaS.

Security baseline: [ADR-0003](decisions/0003-identity-security-strategy.md). Delivered in kyrox-core **v0.2.0** (74 passing tests).

**Primary repo:** kyrox-core  
**Outcome:** Products can authenticate users and scope data by organization.

## M3 — Platform Services 🚧

Extend **kyrox-core** with shared platform services consumed by all KYROX products.

| Service          | Status        |
|------------------|---------------|
| Audit            | ✅ Completed  |
| Settings         | ⬜ Planned    |
| Background Jobs  | ⬜ Planned    |
| Notifications    | ⬜ Planned    |
| File Storage     | ⬜ Planned    |

**Current sprint:** Sprint 0.4.2 — Audit Service

**Primary repo:** kyrox-core (implementation); kyrox-platform (ADRs and milestone docs)  
**Outcome:** Reusable services reduce product-specific backend work.

## M4 — FAIR CRM ⏳

Deliver the first shippable version of **fair-crm** on top of Core identity and platform services: core CRM workflows, product UI, and production readiness for initial users.

**Primary repo:** fair-crm (with dependencies on kyrox-core)  
**Outcome:** First KYROX product in production; feedback loop into Core and platform planning.

## How to use this roadmap

- **Planning and scope changes** — Update milestone docs and ADRs in kyrox-platform before large implementation shifts.
- **Implementation** — Track progress in kyrox-core and fair-crm; reference milestone IDs in commits and tags when appropriate.
- **Status updates** — When a milestone or service completes, update [STATUS.md](STATUS.md), this file, and [CHANGELOG.md](CHANGELOG.md).
- **Deferred work** — Items intentionally postponed are listed in [KNOWN_DEFERRED.md](KNOWN_DEFERRED.md).

See [docs/WORKFLOW.md](docs/WORKFLOW.md) for the end-to-end process from decision to release.
