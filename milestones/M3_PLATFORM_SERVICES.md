# M3 — Platform Services

- **Status:** Planned
- **Primary repository:** kyrox-core

## Goal

Extend KYROX Core with shared platform services that multiple products can reuse, reducing duplicate backend work in fair-crm and future products.

## Scope (indicative — refine before M3 start)

- Notification delivery hooks (email, in-app — exact channels TBD)
- File or object storage integration patterns
- Audit logging and activity trail conventions
- Billing/subscription integration points (webhooks, entitlements)
- Other cross-cutting services identified during M2

## Dependencies

- M2 Identity completed and tagged in kyrox-core

## Success criteria

- At least one platform service is consumable by fair-crm (or a Core integration test) without product-specific code in Core
- Service contracts documented for product teams
- Milestone-worthy release tagged in kyrox-core when complete

## Related

- [ROADMAP.md](../ROADMAP.md)
- [ECOSYSTEM.md](../docs/ECOSYSTEM.md)

## Next (after completion)

→ [M4 FAIR CRM v1](M4_FAIR_CRM_V1.md)
