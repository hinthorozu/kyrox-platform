# KYROX Fair CRM — Project Status

Living status for FAIR CRM. This file records **current implementation truth only**. Detailed delivery history belongs in [CHANGELOG.md](CHANGELOG.md); the previous long-form status snapshot is preserved at [../../archive/fair-crm/status/PROJECT_STATUS_2026-07-24.md](../../archive/fair-crm/status/PROJECT_STATUS_2026-07-24.md).

| Field | Value |
|-------|-------|
| Last verified | **2026-09-08** |
| Active ecosystem milestone | **M4 — FAIR CRM v1** |
| Implementation repository | `hinthorozu/fair-crm` |
| Migration head in `main` | `0078_closure_export_plans` |
| Current work queue | [ROADMAP.md](ROADMAP.md) |
| Shared standards | [../../standards/README.md](../../standards/README.md) |

## Current capability state

| Area | Status |
|------|--------|
| Tenant isolation / SaaS P0.1 | **Certified DONE (2026-08-26)** — TI-01 through TI-09 complete across API, repository, worker, export/download and Platform Super Admin boundaries |
| Identity / SaaS onboarding P0.2 | **Approved onboarding/credential slice DONE (2026-08-29)** — Core identity runtime, thin FAIR CRM bridge, public signup/activation/recovery, login integration, authenticated password change, Super Admin compatibility and production-shaped cross-repository lifecycle certification are complete |
| Organization suspension runtime / OL-07 | **Certified DONE (2026-09-07)** — lifecycle authority, queued/running cancellation, pre-handoff blocking, durable in-flight provider semantics and deterministic reactivation/resumption behavior are implemented/certified |
| Organization closure orchestration / OL08-01 | **Certified DONE (2026-09-07)** — durable FAIR CRM-owned non-destructive closure execution, SYSTEM start/status/retry, live Core `SUSPENDED` precondition, idempotency/race controls, blocked/retry evidence and append-only local audit evidence are merged and cross-repository certified |
| Closure quiescence / OL08-02 | **Certified DONE (2026-09-08)** — closure execution is proven not to bypass OL-07 queued/running/provider/lifecycle guards; closure start parent/event FK ordering was fixed transactionally |
| Closure export planner / OL08-03A | **Certified DONE (2026-09-08)** — durable versioned organization/execution-scoped completeness plan, explicit v1 data-class registry, organization-scoped counts, record-ID fingerprints, hard secret-source exclusions, SYSTEM metadata API, idempotency/audit/tenant-isolation evidence; no package/download or irreversible gate |
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

1. **Permission-controlled UI consistency** — navigation, routes, CRUD actions and non-CRUD actions must reflect effective permissions and the shared [CRUD & UI Authorization Standard](../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md). Backend authorization remains authoritative.
2. **Implementation-to-documentation reconciliation** — quotation and cost-catalog work advanced beyond the old July documentation snapshot. Record what is actually implemented; do not recreate features from stale planning notes.
3. **Status/roadmap discipline** — delivered truth stays here, future/active work stays in [ROADMAP.md](ROADMAP.md), detailed history stays in [CHANGELOG.md](CHANGELOG.md).

## SaaS tenant-isolation certification

P0.1 is complete. FAIR CRM now has deterministic fail-closed evidence for direct foreign resource IDs, nested/derived relationships, source/target mutations, mixed-tenant bulk identifiers, request-scope spoofing, organization-owned background jobs, retry/cancel/status/heartbeat, mail/SMTP ownership, export/download ownership and audit context. The canonical Platform Super Admin exception is separately certified in Core and through the FAIR CRM production-shaped integration path.

`organization` remains the canonical tenant/account boundary. No parallel Tenant model was introduced, and FAIR CRM business semantics remain product-owned rather than moving into Core.

The detailed evidence record is [P0.1 Tenant Isolation Certification](backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md).

## P0.2 identity/onboarding bridge and UI

The explicitly approved onboarding/credential workstream is complete. CRM-BE-01/02 and CRM-UI-01/02 delivered the thin Core transport bridge, public `/signup`, `/activate`, `/forgot-password`, `/reset-password` screens and login entry links. CRM-UI-03 added authenticated `/settings/security` self-service password change while keeping current-password verification, PasswordPolicy, hashing and credential mutation in Core. On success Core revokes prior sessions, the FAIR CRM bridge clears the refresh cookie, the frontend clears local session state and returns to `/login`.

CRM-UI-04 certified that `/admin/system/users` still preserves the existing operator-driven manual user-create path and administrator-supplied password mode. FAIR CRM still passes that password to Core unchanged and does not hash or own credentials. No unsupported setup-link mode or new Super Admin assignment path was added; such a mode remains gated on an approved Core setup-token contract.

Final FAIR CRM PR #92 added a production-shaped cross-repository certification without changing application runtime. It runs FAIR CRM against real KYROX Core and Core's real SMTP adapter with an in-process memory-only SMTP sink. The certified lifecycle is signup → activation → login → forgot/reset → login → password change → login. Activation/reset one-time replay is rejected, old passwords fail after credential changes, and pre-change access/refresh sessions are rejected. Development Standard Gate #306 and Prod-Path E2E #151 passed the final head before merge.

This completion applies only to the approved P0.2 identity/onboarding subset. ADR-0006 closure/export/retention/delete, retention/grace, billing/entitlement and backup-policy decisions remain separately gated and are not declared complete here.

## OL-07 suspension runtime state

OL07-03 established the public cross-repository lifecycle authority path: KYROX Core PR #25 exposes the dedicated product lifecycle snapshot contract, and FAIR CRM PR #249 consumes it through a reusable fail-closed lifecycle guard.

OL07-04 is complete through FAIR CRM PR #250: queued/pending organization-owned import, scraper/enrichment/data-operation and central mail-send work is lifecycle-gated before start/provider dispatch. A suspended/non-active organization cannot start that queued work; unavailable or malformed Core lifecycle state fails closed rather than assuming ACTIVE.

**OL07-05 is DONE as of 2026-09-06.** FAIR CRM PR #251 final head `523f2274a37b3876b092c34b6f761573bd13eedd` passed Backend Quality Check, Feature Contract / Applicability, Frontend Tests / Build / UI Governance and Prod-Path E2E, then squash-merged to `main` as `3b7b1552fc42e596dd5890eeef627d0e4159a968`. Already-running covered import, scraper/adapter-test/enrichment and data-operation work now observes Core lifecycle at safe checkpoints. Suspension/non-active state stops before the next safe unit, owned open transactions are rolled back where applicable, and the running job/run is terminalized as cancelled.

**OL07-06 is DONE as of 2026-09-07.** FAIR CRM PR #252 final head `d8b79e0883b2ac24f52e6c89d1a33654f211d580` passed Backend Quality Check, Feature Contract / Applicability, Frontend Tests / Build / UI Governance and Prod-Path E2E, then squash-merged to `main` as `1215d3817acedd17392a036e7227d94fe330e680`. The central `EmailDeliveryService` now performs the final Core lifecycle check immediately before real SMTP/provider dispatch. If suspension/non-active state is observed after queue claim but before provider handoff, no provider call is emitted and the claimed/synchronous mail work is terminalized as cancelled. If Core lifecycle authority is unavailable/invalid at that boundary, delivery fails closed without falsely recording explicit suspension cancellation. Provider account configuration remains active/configured and persisted secrets remain encrypted; suspension does not delete or lifecycle-deactivate credentials.

**OL07-07 is DONE as of 2026-09-07.** FAIR CRM PR #253 final head `c94be579f071deb7de8ed340690c4d88d5d71c93` passed Development Standard Gate #696 and Prod-Path E2E #261, then merged to `main` as `4f52961341bc4d80c4a576fa85525aa511d68b82`. The mail worker now persists `SENDING` durably before provider handoff. If that checkpoint commit fails, no provider call occurs, the SQLAlchemy session is recovered for worker bookkeeping and the failure remains safely retryable because no external side effect started. Once provider/SMTP handoff has started, ambiguous outcomes are terminal non-auto-retry to prevent duplicate sends; known provider acceptance remains success even if only later close/QUIT cleanup fails. Real-session commit-failure recovery and uncertain-handoff regressions are covered.

**Final reactivation/resumption certification is DONE as of 2026-09-07.** FAIR CRM PR #254 final head `e17593e49ecb25a3aef736b0ceaa1fafa14c7e77` passed Development Standard Gate #700 and Prod-Path E2E #264, then squash-merged to `main` as `18b0b638ba946c2910698e1df7c4ab5283c4958f`. Core `SUSPENDED -> ACTIVE` restores eligibility for fresh/new product work without resurrecting previously suspension-cancelled jobs/runs or mail operations. Work deferred only because lifecycle authority was temporarily unavailable remains non-terminal and may proceed once authority returns `ACTIVE`. Provider account configuration/credentials remain preserved through suspension and require no lifecycle re-enable mutation. Ambiguous provider handoff remains terminal/non-auto-retry after reactivation.

The canonical OL-07 implementation record is [P0.2 OL-07 Suspension Job / Provider Behavior Implementation Tracker](../../ecosystem/P0_2_OL_07_IMPLEMENTATION.md). **OL-07 is complete.** OL-08 closure/export/retention/delete sequencing, OL-09 retention/grace durations and OL-10 backup restore implications remain separately gated except for the accepted/implemented OL08-A / OL08-01 and bounded OL08-B engineering slices described below.

## OL08 closure orchestration and export-planning state

**OL08-01 runtime is certified complete through FAIR CRM PR #255.** Final head `aa34cd3e5d00ec6f7d6b7adaad4afa950319830e` passed Development Standard Gate #707 / run `34155567277` and Prod-Path E2E #270 / run `34155567315`, then merged to FAIR CRM `main` as `e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`. Platform PR #36 completed the cross-repository certification.

The implementation adds migration `0077_organization_closure_executions` plus a FAIR CRM-owned durable closure execution/event model. Start/status/retry is SYSTEM-authorized using the existing Core destructive organization authority boundary; start and retry re-check live Core lifecycle and require `SUSPENDED`. Same-key starts converge, conflicting open executions are rejected, database constraints close duplicate-start races, blocked/retry transitions remain on the same execution, and local append-only event evidence records actor/organization/execution/state/phase/timestamp transactionally.

**OL08-02 closure quiescence is certified complete through FAIR CRM PR #256.** Final head `bae0e7f720e29b688765999fff12deda8624dad7` passed Development Standard Gate #711 / run `34160597160` and Prod-Path E2E #273 / run `34160597182`, then merged as `00f7219c45a5c761df0861e7b30a89ad2a67652d`. The certification proves an open closure execution does not bypass the existing OL-07 pre-start, running-checkpoint, provider-handoff, ambiguous-handoff or fail-closed lifecycle guards. It also fixed closure start FK ordering by flushing the parent execution before its append-only event while retaining one transaction and rollback boundary.

**OL08-03A export manifest/completeness planning is certified complete through FAIR CRM PR #257.** Final head `6927dabea1cf46e1ee70b726d3c8ccd1ae247dcd` passed Development Standard Gate #715 / run `34163087279` and Prod-Path E2E #276 / run `34163087299`, then merged as `eac3a0793a6ea0382e3b82169a1e3c18c0accfc9`. Migration `0078_closure_export_plans` adds durable plan identity bound to organization + closure execution + schema version. The SYSTEM-only planner re-checks live Core `SUSPENDED`, enumerates the accepted v1 structured-data registry, stores organization-scoped counts and record-ID-only fingerprints, records explicit included/excluded/deferred reason evidence, forbids reusable SMTP/provider credential tables as planner sources, and is idempotent and tenant-isolated.

These slices remain intentionally non-destructive. They do not materialize/download a closure package, permit `not_required` without accepted policy evidence, revoke/purge provider credentials, delete/anonymize product data or artifacts, choose retention periods, define backup restore behavior, expose cleanup-complete/tombstone-ready state or call Core organization delete.

Canonical tracker: [P0.2 OL-08 Organization Offboarding Implementation Tracker](../../ecosystem/P0_2_OL_08_IMPLEMENTATION.md).

## Current implementation notes

The old July status referenced earlier migration/test snapshots and is no longer authoritative. FAIR CRM `main` now reaches migration `0078_closure_export_plans`; recent migration history includes cost-catalog tables/categories, import-matching/decision stabilization, OL08-01 durable closure execution/event state and OL08-03A durable export-plan metadata.

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
