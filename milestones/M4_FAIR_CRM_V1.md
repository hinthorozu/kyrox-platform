# M4 — FAIR CRM v1

- **Status:** Planned
- **Primary repository:** fair-crm

## Goal

Ship the first production-ready version of FAIR CRM on top of KYROX Core identity (M2) and platform services (M3).

## Scope (indicative — refine before M4 start)

- Core CRM workflows and domain model
- Product UI integrated with Core auth and tenant scoping
- Configuration and deployment for initial users
- Product-specific integrations not belonging in Core

## Dependencies

- M2 Identity completed in kyrox-core
- M3 Platform Services completed (or agreed minimal subset for v1)
- [FAIR CRM product outline](../products/FAIR_CRM.md)

## Success criteria

- FAIR CRM v1 deployable and usable by target initial users
- No reverse dependency from kyrox-core to fair-crm
- Milestone-worthy tag on fair-crm; ROADMAP and CHANGELOG updated in kyrox-platform

## Boundaries

Per [ADR-0002](../decisions/0002-core-product-separation.md), gaps found during FAIR CRM build that are reusable across products should be implemented in kyrox-core first, then consumed by fair-crm.

## Related

- [products/FAIR_CRM.md](../products/FAIR_CRM.md)
- [ROADMAP.md](../ROADMAP.md)
- [WORKFLOW.md](../docs/WORKFLOW.md)
