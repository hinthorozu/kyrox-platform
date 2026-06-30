# FAIR CRM

**First product of the KYROX ecosystem**, built on [kyrox-core](https://github.com/kyrox/kyrox-core).

## Overview

FAIR CRM is a customer relationship management product that validates KYROX Core in production. It exercises identity, multi-tenancy, and platform services while delivering CRM-specific value to users.

## Repository

- **Name:** fair-crm
- **Depends on:** kyrox-core (required)
- **Does not contain:** Platform-wide ADRs, roadmap, or shared backend primitives that belong in Core

## Relationship to milestones

| Milestone | Relevance to FAIR CRM |
|-----------|------------------------|
| M1 Foundation | Ecosystem and repo strategy defined |
| M2 Identity | Core auth/tenancy FAIR CRM will consume |
| M3 Platform Services | Shared services FAIR CRM will use |
| M4 FAIR CRM v1 | **Primary delivery milestone** for this product |

Current platform focus is **M2 Identity** in kyrox-core; FAIR CRM implementation accelerates in **M4** once Core foundations are ready.

## Scope (M4 target — planned)

High-level v1 goals (to be refined in milestone doc and ADRs as M4 approaches):

- Core CRM entities and workflows (contacts, deals, pipeline — exact scope TBD in M4 planning)
- Product UI consuming Core identity and APIs
- Tenant-scoped data and permissions via Core
- Deployable v1 suitable for initial users

## Boundaries

Per [ADR-0002](../decisions/0002-core-product-separation.md):

- CRM domain logic → **fair-crm**
- Reusable auth, tenancy, notifications, billing hooks → **kyrox-core**
- Strategic decisions → **kyrox-platform**

## Related documents

- [M4_FAIR_CRM_V1.md](../milestones/M4_FAIR_CRM_V1.md)
- [ROADMAP.md](../ROADMAP.md)
- [ECOSYSTEM.md](../docs/ECOSYSTEM.md)
