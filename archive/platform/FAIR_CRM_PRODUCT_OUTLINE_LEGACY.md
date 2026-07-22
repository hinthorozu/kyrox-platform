# FAIR CRM

**First product of the KYROX ecosystem**, built on [kyrox-core](https://github.com/kyrox/kyrox-core) **v0.4.0**.

## Overview

FAIR CRM is a customer relationship management product that validates KYROX Core in production. It exercises identity, organization membership, and platform services while delivering CRM-specific value to users.

FAIR CRM is active in development. It is no longer in a "not started" or pure integration-preparation state.

## Repository

- **Name:** fair-crm
- **Depends on:** kyrox-core v0.4.0 (required)
- **Does not contain:** Platform-wide ADRs, roadmap, or shared backend primitives that belong in Core

Application code for FAIR CRM is implemented in **fair-crm**. Status and planning remain coordinated through **kyrox-platform**.

## Relationship To Milestones

| Milestone | Relevance to FAIR CRM |
|-----------|------------------------|
| M1 Foundation | Ecosystem and repo strategy defined |
| M2 Identity Platform | Core auth and organization complete |
| M3 Platform Services | Shared services complete |
| M4 FAIR CRM v1 | **Active** - primary delivery milestone |

**Current phase:** Active product delivery and data-integration pipeline hardening.

## Current Delivery Status

Completed or present in the product track:

- Customer, Fair, and Participation foundation modules
- Adapter Management
- Linked Fairs
- Fair -> Adapter relationship
- Adapter CRUD
- Run v2 + JSON Handoff

Current technical target:

- Canonical Import Schema

Next target:

- Import Batch / Preview / Duplicate / Merge pipeline

## kyrox-core Modules Available

- Authentication
- Authorization
- Organization
- Membership
- Audit Query API
- Audit Event Write API
- Product Authorization Check API
- Settings Platform
- Background Jobs Platform
- Notifications Platform

kyrox-core is **frozen** except for bug fixes, security fixes, performance fixes, and CRM-driven reusable platform needs surfaced during M4.

## Scope (M4 Target)

- Core CRM entities and workflows
- Product UI consuming Core identity and APIs
- Organization-scoped data and permissions via Core
- Data-integration and import workflows with preview, duplicate detection, and merge decisions
- Deployable v1 suitable for initial users

## Boundaries

Per [ADR-0002](../decisions/0002-core-product-separation.md):

- CRM domain logic -> **fair-crm**
- Reusable auth, tenancy, notifications, platform services -> **kyrox-core**
- Strategic decisions -> **kyrox-platform**

## Related Documents

- [M4_FAIR_CRM_V1.md](../../projects/fair-crm/MILESTONE_M4.md)
- [STATUS.md](../STATUS.md)
- [ROADMAP.md](../ROADMAP.md)
- [ECOSYSTEM.md](../../REPOSITORY_STRATEGY.md)
