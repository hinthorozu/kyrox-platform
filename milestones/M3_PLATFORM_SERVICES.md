# M3 — Platform Services

- **Status:** Completed
- **Primary repository:** kyrox-core (implementation); kyrox-platform (decisions and planning)
- **Delivered in:** kyrox-core **v0.4.0** (commit `c4544b6`, Alembic head `20260701_0024`)

## Goal

Extend KYROX Core with shared platform services that multiple products can reuse, reducing duplicate backend work in fair-crm and future products.

## Delivered services

| Service              | Status        | Notes |
|----------------------|---------------|-------|
| Audit Query API      | ✅ Completed  | Append-only audit trail with query surface |
| Settings Platform    | ✅ Completed  | Tenant-scoped and system-scoped configuration |
| Background Jobs      | ✅ Completed  | Job registration, scheduling, status |
| Notifications        | ✅ Completed  | Outbound notification dispatch abstraction |
| File Storage         | ⬜ Planned    | Deferred beyond v0.4.0 baseline |

## kyrox-core releases (M2–M3)

| Release | Scope |
|---------|-------|
| v0.2.0 | Identity Core |
| v0.2.1 | Authorization Hardening |
| v0.3.0 | Organization & Membership Platform |
| v0.4.0 | Platform Services (M3 complete) |

**Test count at completion:** 307 passed, 1 skipped.

## Platform baseline

Platform baseline is **complete**. kyrox-core is **frozen** except for:

- Bug fixes
- Security fixes
- Performance fixes
- CRM-driven platform needs identified during M4

## Design references

- [ADR-0004: Audit service strategy](../decisions/0004-audit-service-strategy.md)
- [ADR-0002: Core and product separation](../decisions/0002-core-product-separation.md)

## Out of scope (deferred)

- File Storage, Caching, Observability, DevOps — see [KNOWN_DEFERRED.md](../KNOWN_DEFERRED.md)
- FAIR CRM domain features (M4)
- Audit read UI / compliance export (later sprint)
- Automatic audit middleware for all HTTP routes (deferred per ADR-0004)

## Success criteria

- [x] Platform services consumable by fair-crm without product-specific code in Core
- [x] Service contracts documented via ADRs and kyrox-core module docs
- [x] Milestone-worthy release tagged in kyrox-core (**v0.4.0**)

## Related

- [STATUS.md](../STATUS.md)
- [ROADMAP.md](../ROADMAP.md)
- [ECOSYSTEM.md](../docs/ECOSYSTEM.md)

## Next

→ [M4 FAIR CRM v1](M4_FAIR_CRM_V1.md) (active — FAIR CRM Integration Preparation)
