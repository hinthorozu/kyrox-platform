# FAIR CRM

**First product of the KYROX ecosystem**, built on [kyrox-core](https://github.com/kyrox/kyrox-core) **v0.4.0**.

## Overview

FAIR CRM is a customer relationship management product that validates KYROX Core in production. It exercises identity, organization membership, and platform services while delivering CRM-specific value to users.

## Repository

- **Name:** fair-crm
- **Depends on:** kyrox-core v0.4.0 (required)
- **Does not contain:** Platform-wide ADRs, roadmap, or shared backend primitives that belong in Core

Application code for FAIR CRM is implemented in **fair-crm**. Status and planning remain in **kyrox-platform**.

## Relationship to milestones

| Milestone | Relevance to FAIR CRM |
|-----------|------------------------|
| M1 Foundation | Ecosystem and repo strategy defined — ✅ |
| M2 Identity Platform | Core auth and organization — ✅ |
| M3 Platform Services | Shared services (audit, settings, jobs, notifications) — ✅ |
| M4 FAIR CRM v1 | **Active** — primary delivery milestone |

**Current phase:** FAIR CRM Integration Preparation

## kyrox-core modules available

- Authentication
- Authorization
- Organization
- Membership
- Audit Query API
- Settings Platform
- Background Jobs Platform
- Notifications Platform

kyrox-core is **frozen** except for bug fixes, security fixes, performance fixes, and CRM-driven platform needs surfaced during M4.

## Scope (M4 target)

High-level v1 goals (refined during Integration Preparation):

- Core CRM entities and workflows (contacts, deals, pipeline — exact scope TBD)
- Product UI consuming Core identity and APIs
- Organization-scoped data and permissions via Core
- Deployable v1 suitable for initial users

## Boundaries

Per [ADR-0002](../decisions/0002-core-product-separation.md):

- CRM domain logic → **fair-crm**
- Reusable auth, tenancy, notifications, platform services → **kyrox-core**
- Strategic decisions → **kyrox-platform**

## Related documents

- [M4_FAIR_CRM_V1.md](../milestones/M4_FAIR_CRM_V1.md)
- [STATUS.md](../STATUS.md)
- [ROADMAP.md](../ROADMAP.md)
- [ECOSYSTEM.md](../docs/ECOSYSTEM.md)
