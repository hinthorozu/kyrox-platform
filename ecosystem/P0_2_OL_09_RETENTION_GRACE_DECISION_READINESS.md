# P0.2 OL-09 — Retention / Grace Decision Readiness

**Status:** PARTIALLY ACCEPTED — OL09-A + OL09-B ACCEPTED; OL09-C through OL09-E OPEN  
**Prepared:** 2026-09-08  
**OL09-A accepted:** 2026-09-08 — 30-day closure grace  
**OL09-B accepted:** 2026-09-08 — zero-retention webhook cutoff at authoritative Core `SUSPENDED`  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-08 tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**OL09-A decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**OL09-B decision:** `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`  
**Related accepted credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Track the OL-09 retention/grace policy choices that block later organization-closure phases.

OL09-A and OL09-B are now accepted. OL09-C through OL09-E remain open and must not be inferred from those accepted slices.

## Accepted OL09-A — closure grace / reversibility

The accepted policy is:

- a successful Core transition into the current `SUSPENDED` episode starts a **30-day grace period**,
- `grace_deadline = suspended_at + 30 days` using an authoritative UTC suspension timestamp,
- irreversible organization offboarding work is prohibited before that deadline,
- Core `SUSPENDED -> ACTIVE` reactivation remains allowed under the existing Platform SuperAdmin / SYSTEM authority during grace,
- reactivation invalidates the current closure progression and requires the corresponding FAIR CRM closure execution to be durably aborted/terminalized before stale closure work can continue,
- a later new suspension starts a fresh 30-day clock,
- expiry only makes separately accepted irreversible phases eligible; it does not execute or authorize them by itself,
- live Core lifecycle and phase-specific gates still apply at the irreversible boundary.

Canonical detailed decision: `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`.

### Authoritative time evidence requirement

Current Core product lifecycle snapshot exposes organization id, lifecycle status and `work_allowed`, but not the suspension-transition timestamp.

Therefore runtime must not use FAIR CRM closure creation time, first observation time, worker time, UI time or operator-entered time as a substitute. If the authoritative current-suspension timestamp cannot be established, grace completion fails closed.

Pre-existing suspended organizations/closure executions without deterministic authoritative suspension time must not silently receive a retroactive destructive deadline.

## Accepted OL09-B — immediate webhook cutoff / zero signing-secret retention

The accepted behavior is:

- the successful authoritative Core transition into `SUSPENDED` ends all MailerSend webhook processing that could mutate tenant state,
- the same lifecycle boundary is the effective expiry of the MailerSend webhook signing secret,
- webhook signing-secret retention after `SUSPENDED` is **0 days**,
- there is no suspended receive-only drain window,
- there is no provider-terminal-event criterion and no `SUSPENDED + N days` drain deadline,
- the earlier partial-B1 protective exception for `activity.unsubscribed`, `activity.spam_complaint`, and `activity.hard_bounced` is superseded,
- all recognized MailerSend events received after suspension must be prevented from provider-status, consent/suppression, analytics, CRM Activity, dashboard or other tenant-state mutation,
- suspended-period webhook events are never backfilled after reactivation,
- reactivation does not restore the purged signing secret; a valid webhook verification configuration must exist again through an accepted configuration path before webhook processing can resume.

Canonical detailed decision: `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`.

### Effective boundary versus physical purge

Core and FAIR CRM are separate runtime boundaries, so the policy does not claim an impossible same-millisecond cross-service transaction.

The authoritative Core `SUSPENDED` transition is the **effective security/lifecycle boundary**. From that point the signing secret is no longer authorized for webhook verification. Physical zeroization must be triggered through a deterministic, fail-closed, idempotent credential-disposition path and retried if infrastructure failure prevents immediate completion.

A temporarily still-present secret caused by purge failure must not be treated as authorization to continue webhook processing.

### Relationship to the 30-day grace

OL09-A's 30-day grace remains independent:

```text
Core -> SUSPENDED
  -> OL09-B webhook processing ends immediately
  -> OL09-B signing-secret authority ends immediately
  -> OL09-A reversible organization grace continues for 30 days
```

The 30-day organization grace is not a webhook-drain or signing-secret-retention period.

## Why OL-09 remains open

OL09-A answers the organization-level reversible grace window. OL09-B answers the MailerSend webhook/signing-secret boundary. Remaining policy still materially blocks or constrains:

- **OL08-D / OL09-C:** product-data anonymization/hard-delete timing,
- **OL08-F / OL09-D:** closure/audit/security evidence retention,
- **OL08-B + OL08-E / OL09-E:** future closure-package and generated-artifact expiry,
- final sequencing before `cleanup_complete` / `ready_for_tombstone` can ever be considered.

**OL08-G / backup ageing and restore reconciliation remain OL-10 scope.** OL09 decisions do not define backup behavior.

## Verified current lifecycle facts

### 1. Closure runtime remains bounded

Certified/implemented slices currently provide:

- OL08-01 durable closure execution,
- OL08-02 quiescence certification,
- OL08-03A export manifest/completeness planning,
- OL08-04A credential disposition state/evidence foundation.

No organization-wide product-data deletion, generated-artifact purge, closure-package delivery/expiry, cleanup-complete state or Core tombstone is currently authorized.

### 2. Current MailerSend webhook path is signature-dependent

Current MailerSend webhook processing resolves the email account/provider config and reads `webhook_signing_secret` to verify incoming signatures before provider-status/consent processing.

Because OL09-B now makes the signing secret unavailable from the authoritative `SUSPENDED` boundary, suspended webhook processing cannot rely on the previous receive-only model. The runtime implementation must enforce the accepted cutoff before any tenant-state mutation.

### 3. MailerSend token disposition has a separate non-time blocker

OL08-04A classifies current-model MailerSend API tokens as `supported_unidentifiable` because deterministic exact-token targeting is not yet available.

Immediate webhook signing-secret purge does not solve that blocker. OL09 must never be interpreted as MailerSend API-token revoke success.

### 4. Product-data disposition actions remain undecided

OL08-D remains open. The 30-day grace says **when an accepted irreversible phase may become eligible**, not which FAIR CRM data classes are anonymized, hard-deleted or retained.

### 5. Audit/security evidence retention remains separate

Closure events, export-plan evidence and credential-disposition evidence are append-only/non-secret control evidence. OL08-F / OL09-D still need their own retention decision; they are not automatically deleted after 30 days.

### 6. Backup/restore remains separate

System backup/restore is database-level administration. Backup ageing, retention guarantees and restore reconciliation remain OL-10 decisions.

## Remaining decision dimensions

### OL09-C — product-data retention timing — OPEN

Coordinate with OL08-D. For each future `anonymize` / `hard_delete` class, decide whether the action is eligible immediately after the accepted closure grace or follows another class-specific retention period.

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

## Cross-cutting requirements for future time-based runtime

Any time-based implementation must use:

- authoritative durable timestamp/event,
- UTC persistence/comparison,
- explicit policy version,
- idempotent restart behavior,
- deterministic handling after missed schedules/downtime,
- live lifecycle re-check before irreversible mutation,
- no client/UI timer authority,
- no success solely because time elapsed while another required obligation remains blocked.

## OL09-A acceptance checklist — CLOSED

- [x] Scope: organization closure grace/reversibility only.
- [x] Clock start: successful Core transition into the current `SUSPENDED` episode.
- [x] Duration: 30 days; exact UTC deadline = `suspended_at + 30 days`.
- [x] Meaning: reversible grace before irreversible-phase eligibility.
- [x] Authority: existing Platform SuperAdmin / SYSTEM lifecycle authority; no new organization-role authority.
- [x] Reactivation: allowed during grace; invalidates current closure progression.
- [x] Retry/restart: durable timestamp/deadline; process downtime does not reset clock.
- [x] Evidence: policy version + authoritative suspension episode/time + deadline + lifecycle re-check.
- [x] Pre-existing executions: fail closed if authoritative suspension timestamp is unavailable/unverified.
- [x] OL-10 boundary: no backup ageing/restore behavior defined.
- [x] Runtime boundary: only grace clock/evidence/evaluation and safe closure-abort support; no destructive action authorized by time alone.

## OL09-B acceptance checklist — CLOSED

- [x] Authoritative boundary: successful Core transition into `SUSPENDED`.
- [x] Normal tenant mail webhook processing ends at that boundary.
- [x] Protective suspended webhook exception removed/superseded.
- [x] Signing-secret post-suspension retention: 0 days.
- [x] No receive-only drain interval or provider-terminal criterion.
- [x] Secret use is unauthorized from the suspension boundary even if physical purge retry is still pending.
- [x] Physical purge must be deterministic, fail-closed, idempotent and retry-safe.
- [x] Suspended webhook events create no tenant-state mutation or replay/backfill workload.
- [x] Reactivation does not restore zeroized secret material.
- [x] OL09-A 30-day organization grace remains separate and unchanged.

## Explicitly still not accepted

This document does **not** accept or authorize:

- a speculative local lifecycle authority mechanism,
- MailerSend API-token revoke success for an unidentifiable token,
- product-data anonymization/hard delete,
- generated-artifact purge,
- closure-package creation/download/expiry runtime,
- `not_required` export success without an accepted policy source,
- audit/security evidence retention duration,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Current resume point

**OL09-A is accepted. OL09-B is accepted with immediate webhook cutoff and zero post-suspension signing-secret retention. Next decision discussion: OL09-C — product-data retention timing coordinated with OL08-D.**
