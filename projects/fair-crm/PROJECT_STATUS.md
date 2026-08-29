# KYROX Fair CRM — Project Status

Living status for FAIR CRM. This file records **current implementation truth only**. Detailed delivery history belongs in [CHANGELOG.md](CHANGELOG.md); the previous long-form status snapshot is preserved at [../../archive/fair-crm/status/PROJECT_STATUS_2026-07-24.md](../../archive/fair-crm/status/PROJECT_STATUS_2026-07-24.md).

| Field | Value |
|-------|-------|
| Last verified | **2026-08-29** |
| Active ecosystem milestone | **M4 — FAIR CRM v1** |
| Implementation repository | `hinthorozu/fair-crm` |
| Migration head in `main` | `0076_import_analyze_matchable_fields_optional` |
| Current work queue | [ROADMAP.md](ROADMAP.md) |
| Shared standards | [../../standards/README.md](../../standards/README.md) |

## Current capability state

| Area | Status |
|------|--------|
| Tenant isolation / SaaS P0.1 | **Certified DONE (2026-08-26)** — TI-01 through TI-09 complete across API, repository, worker, export/download and Platform Super Admin boundaries |
| Identity / SaaS onboarding P0.2 | **Public auth UI DONE through CRM-UI-01 (2026-08-29)** — Core identity runtime, thin FAIR CRM bridge and public signup/activation/forgot/reset screens are delivered; login integration/security UI remain next |
| Customers / fairs / participations | Implemented |
| Contacts / activities / todos | Implemented |
| Data integration / import engine | Implemented and actively hardened |
| Matching / preview / decision flows | Implemented; later migrations continue stabilization |
| Scraper / adapter workflows | Implemented |
| Operations / automation engine | Implemented; pause-vs-cancel behavior change remains planned |
| Bulk email / delivery flows | Implemented; provider and communication-preference backlog remains |
| Admin backup / restore | Implemented |
| Responsive shared UI / table system | Implemented |
| Permission-aware UI | Shared rule defined; full product-wide consistency audit remains active work |
| Quotation-related capabilities | Present in current implementation; documentation reconciliation required |
| Cost catalog | Current implementation includes cost-catalog schema and Core permission support; tenant isolation is certified, while broader documentation/API/UI completeness is still being reconciled |

## Current quality / documentation focus

1. **P0.2 login/security UI** — integrate account-creation/password-recovery links into login, then add authenticated password-change security settings over the delivered thin backend bridge; Core remains credential authority.
2. **Permission-controlled UI consistency** — navigation, routes, CRUD actions and non-CRUD actions must reflect effective permissions and the shared [CRUD & UI Authorization Standard](../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md). Backend authorization remains authoritative.
3. **Implementation-to-documentation reconciliation** — quotation and cost-catalog work advanced beyond the old July documentation snapshot. Record what is actually implemented; do not recreate features from stale planning notes.
4. **Status/roadmap discipline** — delivered truth stays here, future/active work stays in [ROADMAP.md](ROADMAP.md), detailed history stays in [CHANGELOG.md](CHANGELOG.md).

## SaaS tenant-isolation certification

P0.1 is complete. FAIR CRM now has deterministic fail-closed evidence for direct foreign resource IDs, nested/derived relationships, source/target mutations, mixed-tenant bulk identifiers, request-scope spoofing, organization-owned background jobs, retry/cancel/status/heartbeat, mail/SMTP ownership, export/download ownership and audit context. The canonical Platform Super Admin exception is separately certified in Core and through the FAIR CRM production-shaped integration path.

`organization` remains the canonical tenant/account boundary. No parallel Tenant model was introduced, and FAIR CRM business semantics remain product-owned rather than moving into Core.

The detailed evidence record is [P0.1 Tenant Isolation Certification](backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md).

## P0.2 identity/onboarding bridge and public UI

CRM-BE-01, CRM-BE-02 and CRM-UI-01 are delivered. FAIR CRM consumes the approved public Core identity contract through its existing auth integration boundary and now exposes public `/signup`, `/activate`, `/forgot-password` and `/reset-password` user flows without introducing product-local password policy, password hashing, action-token persistence or credential mutation.

Public auth pages run outside the authenticated product-session provider. Activation/reset action tokens are captured from the link, removed from the browser address bar after initial render and passed only to the FAIR CRM bridge/Core. The pages reuse the existing shared UI system and passed the zero-new UI-governance regression gate. Existing login/refresh/logout behavior and the Platform Super Admin manual user-management flow remain supported. FAIR CRM PR #88 delivered CRM-UI-01; the next implementation phase is login integration.

## Current implementation notes

The old July status referenced earlier migration/test snapshots and is no longer authoritative. FAIR CRM `main` now reaches migration `0076_import_analyze_matchable_fields_optional`; recent migration history includes cost-catalog tables/categories and further import-matching/decision stabilization. The P0.2 backend bridge and CRM-UI-01 required no FAIR CRM schema migration.

Exact implementation details, tests and full migration history remain source truth in the `fair-crm` code repository. This Platform document intentionally records only durable capability-level state.

## Backlog / planned behavior

Canonical queue: [ROADMAP.md](ROADMAP.md).

Supporting specifications currently include:

- [Email Communication Preferences](backlog/EMAIL_COMMUNICATION_PREFERENCES.md)
- [Mail Send Operations Backlog](backlog/MAIL_SEND_OPERATIONS_BACKLOG.md)
- [MailerSend Provider Remaining Work](backlog/PROVIDER_MAILERSEND_REMAINING.md)

These supporting files do not define priority independently of the roadmap.

## Update protocol

When a meaningful FAIR CRM capability changes:

1. Update this file only if current capability truth changed.
2. Update [CHANGELOG.md](CHANGELOG.md) with delivered history.
3. Update [ROADMAP.md](ROADMAP.md) when active/future work changes.
4. Refresh the FAIR CRM summary in [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md).
5. Keep exact test counts, transient CI details and commit SHAs out of permanent standards and roadmap documents.
