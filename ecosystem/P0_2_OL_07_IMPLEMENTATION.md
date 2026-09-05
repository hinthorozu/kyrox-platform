# P0.2 OL-07 — Suspension Runtime Semantics Implementation Tracker

**Status:** IN PROGRESS — OL-07 accepted / implementation started  
**Decision:** OL-07 ACCEPTED 2026-09-04  
**Started:** 2026-09-04  
**Completed:** —  
**Current resume point:** OL07-05 IN PROGRESS / MERGE-READY. FAIR CRM PR #251 (`feat/ol07-05-running-work-checkpoints`) is open from OL07-04-complete `main` (`a01b9de53090e42ddfa5f9c88a19655cc830c4b2`). Final candidate head `523f2274a37b3876b092c34b6f761573bd13eedd` implements Core-authoritative safe-checkpoint cancellation for already-running import, scraper/adapter-test/enrichment, and data-operation work. Final-head Development Standard Gate #688 SUCCESS (including Backend Quality Check) and Prod-Path E2E #255 SUCCESS; no unresolved PR review threads were present at verification. OL07-05 remains unchecked until explicit merge authorization, PR merge, FAIR CRM `main` verification, and tracker completion. Do not start OL07-06.  
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
2. **Tenant isolation remains separate from lifecycle eligibility.** Correct `organization_id` does not imply execution eligibility.
3. **Core remains lifecycle authority.** FAIR CRM must not query Core tables directly or maintain an independent lifecycle authority.
4. **FAIR CRM owns product execution semantics.** Core must not manipulate scraper/import/mail/provider internals.
5. **No speculative event-bus/platform expansion.** Add only the smallest explicit cross-repository contract necessary.
6. **No automatic resume.** OL-06 reactivation restores Core organization state only; cancelled work remains cancelled.

## Sequencing rule

**Do not start or implement the next OL07 checklist item until the current item is fully complete: implementation + CI + merge + `main` verification + tracker update.**

## Certification checklist

- [x] **OL07-01 — Decision acceptance / policy lock**
  - Immediate session revoke, queued-work cancel, running-work safe-checkpoint cancel, queued mail cancel, best-effort in-flight provider abort, encrypted-but-unusable credentials, no automatic resume, detailed audit all accepted.

- [x] **OL07-02 — Core session invalidation on organization suspension**
  - Core PR #24 merged via squash.
  - Final scoped PR head: `496c0ec26d1eb34ac5dcbaa765824a01411ee6ac`.
  - Final CI: Core CI #101 SUCCESS.
  - Merge commit: `5e120ca4f911690c1f6e5217d6530b18f2e4fa83`.
  - `main` verified: target organization normal-user sessions/refresh tokens are revoked; old access/refresh and new login are denied; Platform SuperAdmin remains unaffected.
  - OL07-03 lifecycle contract code was excluded from OL07-02 before merge.

- [x] **OL07-03 — Cross-repository lifecycle authority contract**
  - **Core PR #25** merged via squash from `feat/ol07-03-product-lifecycle-contract`.
  - Final scoped Core PR head: `f2973f1f5f9396604eac7524b6f4e831ea33d9dd`.
  - Final Core PR CI: CI #104 SUCCESS.
  - Core merge commit: `5ad6da0459da640893e4339a87f5528e93271161`.
  - Core `main` verified: dedicated-credential, read-only `GET /api/v1/organizations/{organization_id}/lifecycle-snapshot` is registered and returns canonical `organization_id`, lifecycle `status`, and `work_allowed`.
  - Only canonical `ACTIVE` maps to `work_allowed=true`; missing/wrong lifecycle credential is rejected; the contract does not use user JWTs, provider credentials, FAIR CRM tables, or product-owned lifecycle state.
  - **FAIR CRM PR #249** merged via squash from `feat/ol07-03-lifecycle-guard`.
  - Final scoped FAIR CRM PR head: `6c871222af1fee839a65d278f1f2c063463abd3b`.
  - Final FAIR CRM PR gates: Development Standard Gate #669 SUCCESS; Prod-Path E2E #238 SUCCESS on clean rerun.
  - FAIR CRM merge commit: `52ecbbae2bf295f6b79eb4e89a4ac0100c0e145e`.
  - FAIR CRM `main` verified: reusable `OrganizationLifecycleGuard` and dedicated lifecycle client/configuration are present; organization identity, known status, boolean `work_allowed`, and status/work consistency are validated.
  - Core unreachable/non-200/malformed/inconsistent/wrong-organization responses fail closed; canonical non-active state raises explicit work-not-allowed denial.
  - FAIR CRM `main` push Development Standard Gate #670 SUCCESS, including Backend Quality Check.
  - Cross-repository Prod-Path E2E paired FAIR CRM with the matching Core candidate and a randomized shared lifecycle credential; the live ACTIVE lifecycle snapshot assertion passed.
  - No scraper/import/mail/provider execution path was wired in OL07-03; those remain OL07-04+ scope.

- [x] **OL07-04 — Queued product work cancellation**
  - FAIR CRM PR #250 squash-merged from `feat/ol07-04-queued-work-cancellation`.
  - Final scoped PR head: `38124b9c2a59126977fb22b094a01850e4a315f3`.
  - Shared pre-start gate recognizes the explicit queued product entrypoints for import analyze/apply/bulk-decision, fair scraper, adapter-test scraper, enrichment and data-operation jobs; unknown functions are not silently treated as lifecycle-owned work.
  - Import runner public entrypoints independently apply the gate before any `mark_running()` path, closing direct-runner bypasses.
  - Explicit non-active Core lifecycle snapshots terminalize queued work organization-scope only; lifecycle unavailable/invalid fails closed without guessing a terminal lifecycle disposition.
  - Queued analyze cancellation terminalizes its job and returns `ANALYSIS_QUEUED` batch state to retryable `ANALYSIS_FAILED`; queued apply cancellation terminalizes both the job and its already-`APPLYING` batch so no false active batch remains.
  - Scraper/enrichment history uses the existing local `RUNNING` queue-time sentinel; pre-start cancellation now uses a transition that refuses to rewrite an already terminal scraper run, covering the pre-start race.
  - Data-operation cancellation maps through to parent OperationRun `CANCELLED` where orchestration identifiers are present.
  - Central mail worker checks lifecycle per candidate before queue claim/provider dispatch. Non-active queued mail is cancelled; Core lifecycle outage defers without provider dispatch; candidate-scoped decisions preserve Organization A/B isolation.
  - Lifecycle-deferred mail is not counted as worker `picked_count`, preventing the background drain loop from retrying the same unverifiable queued row up to its drain-round limit.
  - Mail rows cancelled for lifecycle reasons are not accepted by the normal retry use-case, which supports only `FAILED`; reactivation therefore does not implicitly requeue them.
  - Focused tests cover active/suspended/unavailable decisions, organization isolation, import public-runner ordering, apply batch terminalization, mail defer/pick semantics, and scraper terminal-state race protection.
  - Final PR CI: Development Standard Gate #681 SUCCESS and Prod-Path E2E #249 SUCCESS on `38124b9c2a59126977fb22b094a01850e4a315f3`.
  - Merge commit: `a01b9de53090e42ddfa5f9c88a19655cc830c4b2`.
  - FAIR CRM `main` verified at `a01b9de53090e42ddfa5f9c88a19655cc830c4b2`; OL07-04 queued-work lifecycle enforcement is present on `main`.
  - FAIR CRM `main` push Development Standard Gate #682 SUCCESS, including Backend Quality Check.

- [ ] **OL07-05 — Running product work safe-checkpoint cancellation — IN PROGRESS / MERGE-READY**
  - FAIR CRM PR #251 is open on `feat/ol07-05-running-work-checkpoints`; final candidate head `523f2274a37b3876b092c34b6f761573bd13eedd`.
  - Shared running-work checkpoint reads fresh Core lifecycle state; explicit non-active state raises a cancellation signal while lifecycle unavailable/invalid remains a distinct fail-closed authority error.
  - Import analyze checkpoints chunk/persistence boundaries; apply and bulk-decision checkpoint row/mutation boundaries and completion. Running cancellation rolls back the open transaction before terminal state persistence; import job `RUNNING -> CANCELLED` and apply batch cancellation are covered.
  - Existing scraper/adapter-test/enrichment cooperative cancellation hooks observe Core lifecycle in production runners, preserving page/candidate safe checkpoints. Scraper cooperative-cancel control flow was hardened so broad adapter `except Exception` handlers cannot convert an observed suspension into a generic scrape failure.
  - Data-operation dataset writes, per-customer assignment, destructive delete boundaries and completion are lifecycle-checkpointed; suspension prevents the next dataset/mutation/destructive step and rolls back the active transaction before terminal cancellation is persisted.
  - Focused tests cover active/suspended/unavailable checkpoint semantics, scraper cancellation-signal propagation, RUNNING -> CANCELLED domain transitions, import runner rollback/cancellation, import row checkpoint ordering, and data-operation no-next-step behavior.
  - Final PR CI on `523f2274a37b3876b092c34b6f761573bd13eedd`: Development Standard Gate #688 SUCCESS, including Backend Quality Check; Prod-Path E2E #255 SUCCESS.
  - PR review verification found no unresolved review threads; PR is mergeable.
  - Pending: explicit user merge authorization, PR merge, FAIR CRM `main` verification, then this checkbox may become `[x]`. OL07-06 must not start before that sequence completes.

- [ ] **OL07-06 — Outbound mail suspension enforcement**
  - Queued unsent mail must not reach a provider after suspension.
  - Suspended organizations cannot create/start new outbound delivery work.
  - Reactivation does not auto-send previously cancelled mail.

- [ ] **OL07-07 — In-flight provider best-effort abort semantics**
  - Use existing cancellation hooks where technically possible.
  - Irreversibly handed-off provider calls are not falsely reported as recalled.
  - No subsequent provider side effect starts after suspension is observed.

- [ ] **OL07-08 — Provider credential lifecycle gate**
  - Credentials remain encrypted/persisted.
  - Credential use is prohibited while organization is suspended.
  - Reactivation restores lifecycle eligibility only; provider/account validity checks remain authoritative too.

- [ ] **OL07-09 — Detailed suspension disposition audit**
  - Record affected job/mail/provider identifiers and resulting disposition.
  - Record cancellation/abort success/failure and irreversible external effects.
  - Never expose raw credentials/tokens/secrets in audit metadata.

- [ ] **OL07-10 — Reactivation non-resume regression**
  - Jobs/mail cancelled by suspension remain cancelled after reactivation.
  - OL-06 reactivation triggers no automatic requeue/restart.

- [ ] **OL07-11 — Core runtime certification**
  - All OL-07 Core changes merged with applicable CI green.

- [ ] **OL07-12 — FAIR CRM runtime certification**
  - FAIR CRM changes merged with Development Standard Gate / production-shaped runtime coverage green.

- [ ] **OL07-13 — Canonical ADR / roadmap synchronization**
  - ADR-0006 records OL-07 ACCEPTED and implementation state accurately.
  - SaaS roadmap and FAIR CRM roadmap reflect OL-07 state.

- [ ] **OL07-14 — Cross-repository completion**
  - Core + FAIR CRM behavior matches accepted matrix; canonical evidence synchronized; then mark OL-07 DONE and advance to OL-08.

## Ownership

### KYROX Core
- canonical organization lifecycle authority,
- suspend/reactivate API and lifecycle audit,
- organization suspension session/refresh invalidation,
- product-consumable lifecycle eligibility contract.

### FAIR CRM
- lifecycle contract consumer/guard,
- queued/running product-work cancellation,
- mail/provider/credential enforcement,
- detailed product disposition audit,
- no-auto-resume behavior.

### KYROX Platform
- canonical OL-07 decision and sequencing,
- resume tracker,
- cross-repository certification evidence.

## Resume protocol

If work or the conversation is interrupted:

1. Open this file from `kyrox-platform` branch `docs/ol-07-suspension-runtime-semantics`.
2. Read **Current resume point** and the first unchecked checklist item.
3. Inspect the PRs/head SHAs/CI runs recorded there.
4. Continue only that checklist item until implementation + CI + merge + `main` verification are complete.
5. Update this tracker before advancing to the next item.

This file is the canonical OL-07 implementation resume record until OL-07 is certified DONE.
