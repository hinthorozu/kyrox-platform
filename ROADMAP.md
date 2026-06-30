# KYROX Roadmap

High-level milestone sequence for the KYROX ecosystem. Detailed scope for each milestone lives in `milestones/`.

## Milestones

| Milestone | Name               | Status      | Document |
|-----------|--------------------|-------------|----------|
| **M1**    | Foundation         | **Completed** | [M1_FOUNDATION.md](milestones/M1_FOUNDATION.md) |
| **M2**    | Identity           | **Active**    | [M2_IDENTITY.md](milestones/M2_IDENTITY.md) |
| **M3**    | Platform Services  | Planned     | [M3_PLATFORM_SERVICES.md](milestones/M3_PLATFORM_SERVICES.md) |
| **M4**    | FAIR CRM v1        | Planned     | [M4_FAIR_CRM_V1.md](milestones/M4_FAIR_CRM_V1.md) |

## M1 — Foundation (completed)

Establish repository strategy, ecosystem vision, decision workflow, and the kyrox-platform documentation hub. Define the three-repo model and Core vs product separation.

**Primary repo:** kyrox-platform  
**Outcome:** Clear structure and ADRs; team aligned on where work happens.

## M2 — Identity (active)

Implement identity and access foundations in **kyrox-core**: users, organizations (account boundary), authentication, authorization model, and session/token strategy suitable for multi-tenant SaaS.

Security baseline defined in [ADR-0003](decisions/0003-identity-security-strategy.md): Argon2id passwords, JWT access tokens (15 min), hashed rotating refresh tokens (30 days), email verification, token revocation, and multi-device sessions. MFA deferred to a future ADR.

**Primary repo:** kyrox-core  
**Outcome:** Products can authenticate users and scope data by organization.

## M3 — Platform Services (planned)

Extend **kyrox-core** with shared platform services: notifications, file storage hooks, audit/logging patterns, billing integration points, and other cross-product capabilities identified during M2.

**Primary repo:** kyrox-core  
**Outcome:** Reusable services reduce product-specific backend work.

## M4 — FAIR CRM v1 (planned)

Deliver the first shippable version of **fair-crm** on top of Core identity and platform services: core CRM workflows, product UI, and production readiness for initial users.

**Primary repo:** fair-crm (with dependencies on kyrox-core)  
**Outcome:** First KYROX product in production; feedback loop into Core and platform planning.

## How to use this roadmap

- **Planning and scope changes** — Update milestone docs and ADRs in kyrox-platform before large implementation shifts.
- **Implementation** — Track progress in kyrox-core and fair-crm; reference milestone IDs in commits and tags when appropriate.
- **Status updates** — When a milestone completes, update this file and [CHANGELOG.md](CHANGELOG.md).

See [docs/WORKFLOW.md](docs/WORKFLOW.md) for the end-to-end process from decision to release.
