# P0.2 OL-07 — Suspension Runtime Semantics Implementation Tracker

**Status:** IN PROGRESS — OL-07 accepted / implementation started  
**Decision:** OL-07 ACCEPTED 2026-09-04  
**Started:** 2026-09-04  
**Completed:** —  
**Current resume point:** OL07-03 IN PROGRESS. Core PR #25 (`feat/ol07-03-product-lifecycle-contract`, head `3dda5b6854a6720e1ab7e17b31b8aeb732e62587`) and FAIR CRM PR #249 (`feat/ol07-03-lifecycle-guard`, head `748427f5b7f5a8431b333e45bd9aa3158e360f08`) are open. Core CI #102, FAIR Development Standard Gate #663 and Prod-Path E2E #232 are running. Scope is restricted to the Core read-only lifecycle snapshot contract and FAIR reusable fail-closed lifecycle guard. Do not start OL07-04 until OL07-03 has CI green, merge, `main` verification and this tracker is checked `[x]`.  
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

- [ ] **OL07-03 — Cross-repository lifecycle authority contract**
  - **Core PR #25** — `feat/ol07-03-product-lifecycle-contract`; head `3dda5b6854a6720e1ab7e17b31b8aeb732e62587`.
  - Core exposes dedicated-credential, read-only `GET /api/v1/organizations/{organization_id}/lifecycle-snapshot` returning canonical `organization_id`, lifecycle `status`, and `work_allowed`.
  - Only canonical `ACTIVE` maps to `work_allowed=true`.
  - Core contract does not use a user JWT, provider credential, FAIR CRM table, or product-owned lifecycle state.
  - Core regression covers dedicated credential enforcement and ACTIVE/SUSPENDED response behavior.
  - **FAIR CRM PR #249** — `feat/ol07-03-lifecycle-guard`; head `748427f5b7f5a8431b333e45bd9aa3158e360f08`.
  - FAIR has a reusable `OrganizationLifecycleGuard` and dedicated lifecycle client/configuration.
  - Guard validates returned organization identity, known lifecycle status, boolean `work_allowed`, and status/work consistency.
  - Core unreachable/non-200/malformed/inconsistent/wrong-organization responses fail closed.
  - Canonical non-active state raises explicit work-not-allowed denial.
  - No scraper/import/mail/provider execution path is wired yet; that belongs to OL07-04+.
  - **Pending certification:** Core CI #102 + FAIR Development Standard Gate #663 + Prod-Path E2E #232 must be green; then both PRs require merge, `main` verification and tracker `[x]` before OL07-04 starts.

- [ ] **OL07-04 — Queued product work cancellation**
  - NOT STARTED until OL07-03 is DONE.
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
