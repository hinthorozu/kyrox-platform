# M3 — Platform Services

- **Status:** Active
- **Primary repository:** kyrox-core (implementation); kyrox-platform (decisions and planning)

## Goal

Extend KYROX Core with shared platform services that multiple products can reuse, reducing duplicate backend work in fair-crm and future products.

## Service sequence (M3)

| Order | Service        | Design ADR | Implementation (kyrox-core) |
|-------|----------------|------------|-----------------------------|
| 1     | **Audit**      | [ADR-0004](../decisions/0004-audit-service-strategy.md) | Sprint 0.4.2+ |
| 2     | Settings       | TBD        | Planned |
| 3     | Background Jobs| TBD        | Planned |
| 4     | Notifications  | TBD        | Planned |

Additional capabilities (files, billing hooks) may follow within M3 or later milestones.

## Sprint 0.4.1 — Audit Service Design

- **Status:** Completed (design)
- **Repository:** kyrox-platform
- **Deliverable:** [ADR-0004: Audit service strategy](../decisions/0004-audit-service-strategy.md)

### Design summary

- Central **`audit_logs`** table in kyrox-core (append-only)
- **JSONB** for `old_values`, `new_values`, `metadata`
- **Organization-aware**, **user-aware**, **session-aware** (nullable fields for system events)
- **Product-independent** — fair-crm emits events via Core; audit does not import products
- **Application-level** `AuditService` + domain repository port
- **Explicit audit calls** first; HTTP middleware deferred
- **Best-effort** writes generally; **security-critical events must not fail silently**

### Action naming (examples)

- `identity.user.login` / `identity.user.logout`
- `identity.permission.granted`
- `core.settings.updated`
- `fair_crm.company.created` — product example only (documented in ADR, not Core logic)

### Next implementation sprint (kyrox-core)

Sprint **0.4.2** — Audit persistence and `AuditService` (domain, migration, repository, tests).

## Scope (M3)

- **Audit** — append-only activity trail ([ADR-0004](../decisions/0004-audit-service-strategy.md))
- **Settings** — tenant-scoped and system-scoped configuration
- **Background Jobs** — job registration, scheduling, status
- **Notifications** — outbound notification dispatch abstraction

## Out of scope (M3)

- FAIR CRM domain features (M4)
- Audit read UI / compliance export (later sprint)
- Automatic audit middleware for all HTTP routes (deferred per ADR-0004)
- Product-specific validation inside Core settings schemas

## Dependencies

- M2 Identity completed in kyrox-core

## Success criteria

- At least one platform service (audit) is consumable by fair-crm without product-specific code in Core
- Service contracts documented via ADRs and kyrox-core module docs
- Milestone-worthy release tagged in kyrox-core when M3 services are delivered

## Related

- [ADR-0004: Audit service strategy](../decisions/0004-audit-service-strategy.md)
- [ADR-0002: Core and product separation](../decisions/0002-core-product-separation.md)
- [ROADMAP.md](../ROADMAP.md)
- [ECOSYSTEM.md](../docs/ECOSYSTEM.md)

## Next (after completion)

→ [M4 FAIR CRM v1](M4_FAIR_CRM_V1.md)
