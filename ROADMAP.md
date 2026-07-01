# KYROX Roadmap

High-level milestone sequence for the KYROX ecosystem. Live progress is summarized in [STATUS.md](STATUS.md). Detailed scope for each milestone lives in `milestones/`. Application code is implemented in **kyrox-core** and **fair-crm**; this repository is the single source of truth for status and planning.

## Milestones

| Milestone | Name               | Status        | Document |
|-----------|--------------------|---------------|----------|
| **M1**    | Foundation         | ✅ Completed  | [M1_FOUNDATION.md](milestones/M1_FOUNDATION.md) |
| **M2**    | Identity Platform  | ✅ Completed  | [M2_IDENTITY.md](milestones/M2_IDENTITY.md) |
| **M3**    | Platform Services  | ✅ Completed  | [M3_PLATFORM_SERVICES.md](milestones/M3_PLATFORM_SERVICES.md) |
| **M4**    | FAIR CRM v1        | 🚧 Active     | [M4_FAIR_CRM_V1.md](milestones/M4_FAIR_CRM_V1.md) |

## kyrox-core release history

| Release | Scope |
|---------|-------|
| v0.1.0 | Foundation |
| v0.2.0 | Identity Core |
| v0.2.1 | Authorization Hardening |
| v0.3.0 | Organization & Membership Platform |
| v0.4.0 | Platform Services |

**Current:** v0.4.0 — platform baseline complete. kyrox-core is frozen except bug fixes, security fixes, performance fixes, and CRM-driven platform needs.

## M1 — Foundation ✅

Establish repository strategy, ecosystem vision, decision workflow, and the kyrox-platform documentation hub. Define the three-repo model and Core vs product separation.

**Primary repo:** kyrox-platform  
**Outcome:** Clear structure and ADRs; team aligned on where work happens.

## M2 — Identity Platform ✅

Implement identity and access foundations in **kyrox-core**: users, organizations (account boundary), authentication, authorization, and session/token strategy suitable for multi-tenant SaaS.

Security baseline: [ADR-0003](decisions/0003-identity-security-strategy.md). Delivered across kyrox-core **v0.2.0**–**v0.3.0**.

**Primary repo:** kyrox-core  
**Outcome:** Products can authenticate users and scope data by organization.

## M3 — Platform Services ✅

Extend **kyrox-core** with shared platform services consumed by all KYROX products.

| Service              | Status        |
|----------------------|---------------|
| Audit Query API      | ✅ Completed  |
| Settings Platform    | ✅ Completed  |
| Background Jobs      | ✅ Completed  |
| Notifications        | ✅ Completed  |
| File Storage         | ⬜ Planned    |

Delivered in kyrox-core **v0.4.0** (307 passed, 1 skipped; Alembic head `20260701_0024`).

**Primary repo:** kyrox-core  
**Outcome:** Reusable platform baseline ready for product integration.

## M4 — FAIR CRM v1 🚧

Deliver the first shippable version of **fair-crm** on top of Core identity and platform services: core CRM workflows, product UI, and production readiness for initial users.

**Current phase:** FAIR CRM Integration Preparation

**Primary repo:** fair-crm (with dependencies on kyrox-core)  
**Outcome:** First KYROX product in production; feedback loop into Core and platform planning.

## How to use this roadmap

- **Planning and scope changes** — Update milestone docs and ADRs in kyrox-platform before large implementation shifts.
- **Implementation** — Track progress in kyrox-core and fair-crm; reference milestone IDs in commits and tags when appropriate.
- **Status updates** — When a milestone or service completes, update [STATUS.md](STATUS.md), this file, and [CHANGELOG.md](CHANGELOG.md).
- **Deferred work** — Items intentionally postponed are listed in [KNOWN_DEFERRED.md](KNOWN_DEFERRED.md).

See [docs/WORKFLOW.md](docs/WORKFLOW.md) for the end-to-end process from decision to release.
