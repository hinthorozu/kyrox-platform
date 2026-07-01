# M4 — FAIR CRM v1

- **Status:** Active
- **Current phase:** FAIR CRM Integration Preparation
- **Primary repository:** fair-crm

## Goal

Ship the first production-ready version of FAIR CRM on top of KYROX Core identity (M2) and platform services (M3).

Application code for FAIR CRM lives in **fair-crm**. Platform decisions and status remain in **kyrox-platform**. kyrox-core is frozen except for bug fixes, security fixes, performance fixes, and CRM-driven platform needs.

## Prerequisites (met)

- [x] M2 Identity Platform — kyrox-core v0.2.0–v0.3.0
- [x] M3 Platform Services — kyrox-core v0.4.0 (platform baseline complete)
- [x] Core modules available: Authentication, Authorization, Organization, Membership, Audit Query API, Settings, Background Jobs, Notifications

## Scope (indicative — refine during Integration Preparation)

- Core CRM workflows and domain model
- Product UI integrated with Core auth and organization scoping
- Configuration and deployment for initial users
- Product-specific integrations not belonging in Core
- Integration patterns against kyrox-core v0.4.0 APIs

## Dependencies

- kyrox-core **v0.4.0** (frozen baseline)
- [FAIR CRM product outline](../products/FAIR_CRM.md)

## Success criteria

- FAIR CRM v1 deployable and usable by target initial users
- No reverse dependency from kyrox-core to fair-crm
- Milestone-worthy tag on fair-crm; ROADMAP and CHANGELOG updated in kyrox-platform
- CRM-driven Core gaps implemented in kyrox-core only when reusable across products ([ADR-0002](../decisions/0002-core-product-separation.md))

## Boundaries

Per [ADR-0002](../decisions/0002-core-product-separation.md), gaps found during FAIR CRM build that are reusable across products should be implemented in kyrox-core first, then consumed by fair-crm.

## Related

- [products/FAIR_CRM.md](../products/FAIR_CRM.md)
- [STATUS.md](../STATUS.md)
- [ROADMAP.md](../ROADMAP.md)
- [WORKFLOW.md](../docs/WORKFLOW.md)
