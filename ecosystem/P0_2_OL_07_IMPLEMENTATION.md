# P0.2 OL-07 — Suspension Runtime Semantics Implementation Tracker

**Status:** IN PROGRESS — OL-07 accepted / implementation started  
**Decision:** OL-07 ACCEPTED 2026-09-04  
**Started:** 2026-09-04  
**Completed:** —  
**Current resume point:** OL07-02 FINALIZATION — Core PR #24 is scoped strictly to organization suspension session/refresh invalidation and suspended-user login/refresh denial. Early OL07-03 lifecycle-snapshot/token work was removed from PR #24. Finalize CI, merge Core PR #24, verify `main`, then mark OL07-02 DONE before starting OL07-03.  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Accepted policy

> **Organization suspension means immediate stop. Once an organization becomes `SUSPENDED`, no new organization-owned work or outbound side effect may start. Queued work is cancelled. Running work cooperatively cancels at the earliest safe checkpoint. Provider calls already in flight are aborted best-effort and any irreversible side effect is audited. Provider credentials remain encrypted but unusable while suspended. Reactivation never automatically restarts work cancelled because of suspension.**

## Accepted decision matrix

| Area | Accepted OL-07 behavior |
| --- | --- |
| Active sessions / refresh tokens | Revoke immediately on suspension. |
| New organization-owned work | Deny immediately. No new protected job/operation may start. |
| Queued, not-yet-started jobs | Cancel. Do not retain for automatic resume. |
| Running scraper / enrichment / import / product jobs | Cooperatively cancel at the earliest safe checkpoint. Do not leave an open transaction half-applied; do not proceed to the next batch/row/step after suspension is observed. |
| Queued outbound email | Cancel before provider dispatch. Never auto-send after reactivation. |
| In-flight SMTP/provider call | Best-effort abort. If already handed off and technically irreversible, record the resulting side effect explicitly in audit evidence. Do not start another side effect. |
| Provider credentials | Do not delete. Keep encrypted, but make lifecycle-unusable while the organization is suspended. Reactivation may make them usable again subject to their own account/config state. |
| Reactivation | Do not auto-restart or auto-requeue any job/mail cancelled by suspension. User/operator must explicitly start new work if needed. |
| Audit | Detailed per-item evidence: affected job/mail/provider operation, prior/current disposition, cancel/abort success or failure, and any in-flight/irreversible external side effect. |

## Non-negotiable implementation semantics

1. **Suspend is fail-closed for work and external effects.** If authoritative lifecycle state cannot be established at a destructive/external side-effect boundary, execution must not proceed.
2. **Tenant isolation remains separate from lifecycle eligibility.** A worker can have the correct `organization_id` and still be prohibited from executing because the organization is suspended.
3. **Core remains lifecycle authority.** FAIR CRM must not query Core tables directly or duplicate organization lifecycle state as an independent authority.
4. **FAIR CRM owns product execution semantics.** Core must not import or manipulate scraper/import/mail/provider product internals.
5. **No speculative event-bus/platform expansion.** Reuse existing public contracts and job/cancellation primitives where they satisfy the accepted behavior; add the smallest explicit cross-repository lifecycle contract necessary where they do not.
6. **No automatic resume.** OL-06 reactivation restores canonical Core organization state only; it never implies restart/requeue of OL-07-cancelled work.

## Sequencing rule

**Do not start or implement the next OL07 checklist item until the current item is fully complete: implementation + CI + merge + `main` verification + tracker update.** Research required to diagnose the current item is allowed; implementation for a later item is not.

## Certification checklist

- [x] **OL07-01 — Decision acceptance / policy lock**
  - Session behavior accepted: immediate revoke.
  - Queued jobs accepted: cancel.
  - Running work accepted: cancel at earliest safe checkpoint.
  - Queued outbound mail accepted: cancel.
  - In-flight provider behavior accepted: best-effort abort + explicit irreversible-side-effect audit.
  - Provider credentials accepted: encrypted retention + lifecycle unusable while suspended.
  - Reactivation accepted: no automatic restart/requeue.
  - Audit accepted: detailed per affected item.

- [ ] **OL07-02 — Core session invalidation on organization suspension**
  - Core PR #24: `feat/ol-07-suspension-runtime`.
  - Current scoped head before final CI: `496c0ec26d1eb34ac5dcbaa765824a01411ee6ac`.
  - Early OL07-03 product lifecycle snapshot/token changes removed from this PR.
  - Suspension invalidates active sessions/refresh tokens for normal users of the target organization.
  - Suspended organization users cannot continue with prior access token, refresh, or new login.
  - Platform SuperAdmin remains outside organization-scoped revocation.
  - Regression coverage exists in `backend/tests/modules/identity/organization/test_organization_suspension_sessions.py`.
  - Final requirements still open: latest scoped CI green, squash merge PR #24, verify merged `main` behavior/head, then check this item `[x]`.

- [ ] **OL07-03 — Cross-repository lifecycle authority contract**
  - NOT STARTED until OL07-02 is fully DONE.
  - Define the smallest public Core/product contract FAIR CRM can use to establish organization lifecycle eligibility without querying Core tables.
  - Side-effect boundaries must fail closed when lifecycle eligibility cannot be established.
  - Avoid an unbounded synchronous Core lookup for every local row operation; use explicit checkpoints/orchestration appropriate to existing architecture.

- [ ] **OL07-04 — Queued product work cancellation**
  - Scraper, enrichment, import, operations and other organization-owned queued work must be cancelled/not started after suspension.
  - Cancellation must be deterministic and organization-scoped.

- [ ] **OL07-05 — Running product work safe-checkpoint cancellation**
  - Scraper/enrichment/import/operation runners must observe lifecycle cancellation at safe checkpoints.
  - No next batch/row/step may start after suspension is observed.
  - Open transactional work must settle safely according to existing transaction boundaries.

- [ ] **OL07-06 — Outbound mail suspension enforcement**
  - Queued unsent mail must not reach a provider after suspension.
  - Suspended organizations cannot create/start new outbound delivery work.
  - Reactivation does not auto-send previously cancelled mail.

- [ ] **OL07-07 — In-flight provider best-effort abort semantics**
  - Use existing cancellation hooks where technically possible.
  - Provider calls already irreversibly handed off are not falsely reported as recalled.
  - No subsequent provider side effect starts after suspension is observed.

- [ ] **OL07-08 — Provider credential lifecycle gate**
  - Credentials remain encrypted/persisted.
  - Delivery/integration use is prohibited while organization is suspended even if the product account itself is otherwise active.
  - Reactivation restores lifecycle eligibility only; normal provider/account validity checks remain authoritative too.

- [ ] **OL07-09 — Detailed suspension disposition audit**
  - Record affected job/mail/provider item identifiers and resulting disposition.
  - Record cancellation/abort success or failure.
  - Record in-flight/irreversible external side effects explicitly.
  - Do not expose raw credentials/tokens/secrets in audit metadata.

- [ ] **OL07-10 — Reactivation non-resume regression**
  - Jobs/mail cancelled by suspension remain cancelled after reactivation.
  - No automatic requeue/restart is triggered by OL-06 reactivation.

- [ ] **OL07-11 — Core runtime certification**
  - Core changes merged with applicable CI green.

- [ ] **OL07-12 — FAIR CRM runtime certification**
  - FAIR CRM changes merged with Development Standard Gate / applicable production-shaped runtime coverage green.

- [ ] **OL07-13 — Canonical ADR / roadmap synchronization**
  - ADR-0006 records OL-07 ACCEPTED and implementation state accurately.
  - SaaS roadmap and FAIR CRM roadmap reflect OL-07 accepted/in-progress, then DONE only after runtime certification.

- [ ] **OL07-14 — Cross-repository completion**
  - Core + FAIR CRM behavior matches the accepted matrix.
  - Canonical evidence is synchronized.
  - Only then mark OL-07 DONE and advance the next decision gate to OL-08.

## Verified pre-implementation runtime gap

The existing runtime audit established that Core suspension blocks new normal permission-protected requests, but already queued/running FAIR CRM scraper, enrichment, import and mail execution generally trusts previously established organization-scoped context and does not re-check Core lifecycle state during execution. Tenant isolation remains intact; lifecycle eligibility is the gap OL-07 closes.

Known audit targets include:

- `kyrox-core/backend/app/modules/identity/application/organization/suspend_organization.py`
- `fair-crm/backend/app/modules/scraper/application/adapter_test_run_job_runner.py`
- `fair-crm/backend/app/modules/scraper/application/enrichment_run_job_runner.py`
- `fair-crm/backend/app/modules/data_integration/application/import_job_runner.py`
- `fair-crm/backend/app/modules/operations/application/start_operation.py`
- `fair-crm/backend/app/modules/operations/infrastructure/handlers/bulk_email_handler.py`
- `fair-crm/backend/app/modules/mail_send_operations/application/process_mail_send_operations_worker.py`
- `fair-crm/backend/app/modules/mail_send_operations/application/mail_send_operation_dispatcher.py`
- `fair-crm/backend/app/modules/email_delivery/application/email_delivery_service.py`

## Implementation ownership

### KYROX Core

- canonical organization `ACTIVE` / `SUSPENDED` lifecycle authority,
- suspend/reactivate APIs and lifecycle audit,
- organization suspension session/refresh invalidation,
- any reusable public lifecycle eligibility contract required by products.

### FAIR CRM

- queued product work cancellation,
- running job cooperative safe-checkpoint cancellation,
- outbound mail cancellation and execution-time lifecycle gate,
- provider credential usability gate,
- best-effort in-flight provider abort behavior,
- detailed product disposition audit evidence,
- no-auto-resume behavior after reactivation.

### KYROX Platform

- OL-07 policy/ADR,
- implementation tracker and cross-repository sequencing,
- certification evidence and roadmap synchronization.

## Scope boundary / non-goals

OL-07 does **not** decide or implement:

- OL-08 closure/export/retention/anonymization/delete sequencing,
- OL-09 retention/grace durations,
- OL-10 backup restore implications,
- hard deletion of product data or credentials,
- automatic restart of cancelled work after reactivation,
- a second product-owned organization lifecycle authority.

## Resume protocol

If implementation work or the conversation is interrupted:

1. Open this file from `kyrox-platform`.
2. Read **Current resume point** and the certification checklist.
3. Inspect the referenced Core/FAIR CRM PRs and latest CI recorded here.
4. Continue from the first unchecked implementation/certification item.
5. Update this tracker after every material implementation milestone or PR/CI state change.

This file is the canonical OL-07 implementation resume record until OL-07 is certified DONE.
