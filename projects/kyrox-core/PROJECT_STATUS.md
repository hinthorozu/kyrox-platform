# KYROX Core — Project Status

Living status for KYROX Core. Ecosystem summary: [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md). Future work: [ROADMAP.md](ROADMAP.md).

| Field | Value |
|-------|-------|
| Last verified | **2026-08-19** |
| Repository mode | Stable platform baseline; fixes and reusable product-driven changes continue |
| Active ecosystem milestone | M4 — FAIR CRM v1 |
| Migration head in `main` | `20260817_0059_repair_organization_admin_permissions` |
| Main CI | Green at latest repository verification |

## Current capability state

| Area | Status |
|------|--------|
| Identity and authentication | Implemented |
| Authorization | Implemented |
| Organization and user management | Implemented |
| Roles and permissions | Implemented and evolved through later migrations |
| Audit | Implemented |
| Settings | Implemented |
| Background jobs | Implemented |
| Notifications | Implemented |
| Product authorization integration | Implemented |
| FAIR CRM permission catalog support | Implemented, including quotation and cost-catalog permissions |
| File storage | Planned |
| Caching | Demand-driven candidate |
| Observability | Demand-driven candidate |

## Migration status

The former documentation baseline at `20260701_0025` is obsolete. The current Core migration tree reaches `20260817_0059_repair_organization_admin_permissions` and includes later FAIR CRM product permissions, organization/user-role governance changes, permission consolidation/scope changes and cost-catalog permissions.

The code repository is the implementation source for complete migration history. This document records the verified current head and capability-level state only.

## Integration contract

Products integrate with Core through public HTTP APIs. Product domain implementation stays in the product repository.

Canonical contract: [integrations/PRODUCT_INTEGRATION_GUIDE.md](integrations/PRODUCT_INTEGRATION_GUIDE.md).

## Update protocol

When Core changes materially:

1. Update this file with current capability truth and migration head when useful.
2. Update [CHANGELOG.md](CHANGELOG.md) for delivered history.
3. Refresh the summary in [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md).
4. Keep exact test counts and commit SHAs out of permanent standards and roadmap documents.
