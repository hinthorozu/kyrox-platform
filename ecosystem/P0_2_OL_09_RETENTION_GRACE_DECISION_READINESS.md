# P0.2 OL-09 — Retention / Grace Decision Readiness

**Status:** PARTIALLY ACCEPTED — OL09-A ACCEPTED; OL09-B1 ACCEPTED; OL09-B2 and OL09-C through OL09-E OPEN  
**Prepared:** 2026-09-08  
**OL09-A accepted:** 2026-09-08 — 30-day closure grace  
**OL09-B1 accepted:** 2026-09-08 — suspended webhook service boundary / minimum protective handling  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-08 tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**OL09-A decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**OL09-B decision:** `ecosystem/P0_2_OL_09_B_WEBHOOK_DRAIN_DECISION.md`  
**Related accepted credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Track the OL-09 timing/service-boundary choices that constrain later organization closure.

OL09-A now defines the organization-level reversible grace window. OL09-B1 now defines what MailerSend webhook work may continue while the organization is suspended. OL09-B2 still must decide the receive-only expiry criterion and final webhook-signing-secret purge timing. OL09-C through OL09-E remain open.

## Accepted OL09-A — 30-day closure grace / reversibility

The accepted policy is:

- a successful Core transition into the current `SUSPENDED` episode starts a **30-day grace period**,
- `grace_deadline = suspended_at + 30 days` using an authoritative UTC suspension timestamp,
- irreversible organization offboarding work is prohibited before that deadline,
- Core `SUSPENDED -> ACTIVE` reactivation remains allowed under existing Platform SuperAdmin / SYSTEM authority during grace,
- reactivation invalidates current closure progression and requires safe durable abort/terminalization before stale closure work can continue,
- a later new suspension starts a fresh 30-day clock,
- expiry only makes separately accepted irreversible phases eligible; it does not execute or authorize them by itself,
- live Core lifecycle and phase-specific gates still apply at the irreversible boundary.

Canonical detailed decision: `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`.

### Authoritative time evidence requirement

Current Core product lifecycle snapshot exposes organization id, lifecycle status and `work_allowed`, but not the suspension-transition timestamp.

Runtime must not substitute FAIR CRM closure creation time, first observation time, worker time, UI time or operator-entered time. If the authoritative current-suspension timestamp cannot be established, grace completion fails closed.

Pre-existing suspended organizations/closure executions without deterministic authoritative suspension time must not silently receive a retroactive destructive deadline.

## Accepted OL09-B1 — suspended webhook service boundary

A suspended organization does **not** continue receiving normal customer-facing mail analytics/service merely because delayed MailerSend webhooks still arrive.

Accepted behavior:

- normal `sent` / `delivered` / `deferred` / bounce provider-status progression is not continued as suspended customer service,
- `opened` / `clicked` engagement tracking is not continued,
- dropped normal-service events create no queue/job, dashboard/engagement work, CRM Activity or historical rescan,
- intentionally dropped valid events take a cheap successful acknowledgement path so FAIR CRM does not invite provider retries merely because it declined customer-facing processing,
- signature/account validation remains mandatory; suspended mode is not a security bypass,
- only `activity.unsubscribed` and `activity.spam_complaint` are currently accepted as the minimum protective event set because current FAIR CRM already gives them explicit consent semantics,
- those two events may only perform the minimum idempotent tenant-scoped mutation needed to set the linked customer/contact `email_allowed = false` plus minimal non-secret evidence,
- the normal CRM Activity record must not be created in the suspended protective path,
- current `hard_bounced` behavior is not promoted into a new suppression rule because current code only uses it for provider-status progression,
- no per-webhook Core network request, polling loop, historical mail scan, per-message timer or per-tenant scheduled worker is accepted for this gate.

The implementation target is a cheap local organization/account-scoped suspended receive-only decision backed by trustworthy lifecycle/closure evidence. Core remains lifecycle authority; no untrusted client flag may fabricate the suspended fast-path state.

Canonical detailed decision: `ecosystem/P0_2_OL_09_B_WEBHOOK_DRAIN_DECISION.md`.

### Why this is only partial OL09-B acceptance

OL09-B1 answers **what service may continue** after suspension. It deliberately does not answer **how long the webhook signing secret remains receive-only**.

Therefore OL09-B2 remains open and no final signing-secret purge is authorized yet.

## Why OL-09 remains open

Remaining policy still blocks or constrains:

- **OL08-C4 / OL09-B2:** final zeroization of webhook signing secrets after receive-only drain,
- **OL08-D / OL09-C:** product-data anonymization/hard-delete timing,
- **OL08-F / OL09-D:** closure/audit/security evidence retention,
- **OL08-B + OL08-E / OL09-E:** future closure-package and generated-artifact expiry,
- final sequencing before `cleanup_complete` / `ready_for_tombstone` can ever be considered.

**OL08-G / backup ageing and restore reconciliation remain OL-10 scope.** OL-09 must not silently define backup behavior.

## Verified current lifecycle facts

### 1. Closure runtime remains bounded

Certified/implemented slices currently provide:

- OL08-01 durable closure execution,
- OL08-02 quiescence certification,
- OL08-03A export manifest/completeness planning,
- OL08-04A credential disposition state/evidence foundation.

No organization-wide product-data deletion, generated-artifact purge, closure-package delivery/expiry, cleanup-complete state or Core tombstone is currently authorized.

### 2. Current webhook taxonomy and consent behavior are explicit

Current FAIR CRM MailerSend webhook handling recognizes `sent`, `delivered`, soft/hard bounce, `deferred`, `opened`, `clicked`, `unsubscribed` and `spam_complaint` event families.

Only unsubscribe and spam complaint currently invoke explicit consent mutation. Normal webhook handling also updates provider status and can create a CRM Activity for the two consent events. OL09-B1 narrows suspended-mode behavior rather than extending that normal service path.

### 3. MailerSend token disposition has a separate non-time blocker

OL08-04A classifies current-model MailerSend API tokens as `supported_unidentifiable` because deterministic exact-token targeting is not yet available.

Waiting 30 days or accepting a webhook drain rule does not solve that blocker. OL-09 must never be interpreted as MailerSend revoke success.

### 4. Product-data disposition actions remain undecided

OL08-D remains open. The 30-day grace says **when an accepted irreversible phase may become eligible**, not which FAIR CRM data classes are anonymized, hard-deleted or retained.

### 5. Audit/security evidence retention remains separate

Closure events, export-plan evidence and credential-disposition evidence are append-only/non-secret control evidence. OL08-F / OL09-D still need their own retention decision; they are not automatically deleted after 30 days.

### 6. Backup/restore remains separate

System backup/restore is database-level administration. Backup ageing, retention guarantees and restore reconciliation remain OL-10 decisions.

## Remaining decision dimensions

### OL09-B2 — receive-only expiry / final signing-secret purge — OPEN

Decide how the accepted minimum receive-only safety path ends.

Still open:

1. Is expiry fixed-time, deterministic provider evidence, or hybrid?
2. If time-based, what exact duration applies?
3. Which authoritative timestamp starts the drain clock?
4. What happens to valid but late provider events after final signing-secret purge?
5. What happens when state remains ambiguous at expiry?
6. What low-frequency global cleanup/batch cadence is acceptable if time-based purge is selected?

The OL09-A 30-day organization grace does **not** automatically set OL09-B2 to 30 days.

Until B2 is accepted, a required signing secret may remain `receive_only_pending`; elapsed OL09-A grace alone cannot mark it purged.

### OL09-C — product-data retention timing — OPEN

Coordinate with OL08-D. For each future `anonymize` / `hard_delete` class, decide whether the action is eligible immediately after accepted closure grace or follows another class-specific retention period.

No legal/compliance duration is assumed here.

### OL09-D — audit/security evidence retention — OPEN

Decide retention/transformation of:

- closure execution/event evidence,
- export completeness/disposition evidence,
- credential-disposition evidence,
- external invalidation evidence,
- later cleanup/tombstone evidence if those phases are accepted.

This period may differ from customer/product-data timing.

### OL09-E — closure package / generated artifact expiry — OPEN

This is a timing dependency only. Package/artifact ownership and deletion actions remain OL08-B / OL08-E policy.

A future acceptance must decide package/artifact clock origin and expiry semantics without silently creating package runtime.

## Cross-cutting requirements for future runtime

Any time- or lifecycle-sensitive implementation must use:

- authoritative durable lifecycle/clock evidence,
- UTC persistence/comparison for time policies,
- explicit policy version where a duration is involved,
- idempotent restart behavior,
- deterministic handling after downtime/missed schedules,
- live lifecycle re-check before irreversible mutation,
- no client/UI timer authority,
- no success solely because time elapsed while another required obligation remains blocked,
- tenant isolation and stale-reactivation regression evidence.

## OL09-A acceptance checklist — CLOSED

- [x] Scope: organization closure grace/reversibility only.
- [x] Clock start: successful Core transition into the current `SUSPENDED` episode.
- [x] Duration: 30 days; exact UTC deadline = `suspended_at + 30 days`.
- [x] Meaning: reversible grace before irreversible-phase eligibility.
- [x] Authority: existing Platform SuperAdmin / SYSTEM lifecycle authority.
- [x] Reactivation: allowed during grace; invalidates current closure progression.
- [x] Retry/restart: durable timestamp/deadline; process downtime does not reset clock.
- [x] Pre-existing executions: fail closed if authoritative suspension timestamp is unavailable/unverified.
- [x] OL-10 boundary: no backup ageing/restore behavior defined.

## OL09-B1 acceptance checklist — CLOSED

- [x] Scope: suspended MailerSend webhook service boundary only.
- [x] Normal customer-facing provider-status/engagement processing stops.
- [x] Minimum protective set is explicit: unsubscribe + spam complaint only.
- [x] Protective mutation is limited to idempotent `email_allowed = false` + minimum evidence.
- [x] Normal CRM Activity creation is excluded in suspended protective mode.
- [x] Non-protective valid events use a cheap 2xx/drop path.
- [x] No polling, historical scan, per-message timer, per-tenant scheduler or per-webhook Core call.
- [x] Security validation remains mandatory.
- [x] Reactivation/stale-state and tenant isolation must be certified by runtime.
- [x] Expiry duration/final signing-secret purge explicitly remains OL09-B2.

## Explicitly still not accepted

This document does **not** accept or authorize:

- any OL09-B2 webhook drain duration/final purge criterion,
- MailerSend revoke success for an unidentifiable token,
- final webhook signing-secret purge,
- product-data anonymization/hard delete,
- generated-artifact purge,
- closure-package creation/download/expiry runtime,
- `not_required` export success,
- audit/security evidence retention duration,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Current resume point

**OL09-A is accepted. OL09-B1 suspended webhook service boundary is accepted. Next decision discussion: OL09-B2 — receive-only expiry criterion / final signing-secret purge timing.**

Do not infer OL09-B2's answer or duration from the 30-day OL09-A closure grace.
