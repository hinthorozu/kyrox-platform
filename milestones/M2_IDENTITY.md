# M2 — Identity

- **Status:** Active
- **Primary repository:** kyrox-core

## Goal

Deliver identity and access foundations in KYROX Core so products can authenticate users, manage organizations/tenants, and enforce authorization in a multi-tenant SaaS model.

## Scope (implementation in kyrox-core)

- User model and registration/authentication flows
- Organization / tenant model and membership
- Session or token strategy (e.g. JWT, refresh tokens — exact choice via implementation ADR or Core docs)
- Authorization model (roles/permissions scoped to tenant)
- APIs or modules exposed for product consumption

## Out of scope (this milestone)

- Full CRM features (fair-crm — M4)
- Complete platform services catalog (M3)
- Public docs site or client SDK repos

## Dependencies

- M1 Foundation completed (repo strategy and separation agreed)

## Success criteria

- A product (or integration test harness) can authenticate a user and operate within a tenant context using Core only
- Core remains free of fair-crm imports ([ADR-0002](../decisions/0002-core-product-separation.md))
- Milestone-worthy release tagged in kyrox-core when complete

## Planning references

- [VISION.md](../VISION.md) — Core-first, product-independent foundation
- [WORKFLOW.md](../docs/WORKFLOW.md) — Decide in platform, implement in Core
- [ROADMAP.md](../ROADMAP.md)

## Next (after completion)

→ [M3 Platform Services](M3_PLATFORM_SERVICES.md)
