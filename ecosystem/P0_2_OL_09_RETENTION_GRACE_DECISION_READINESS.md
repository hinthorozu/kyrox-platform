# P0.2 OL-09 — Retention / Grace Decision Readiness

**Status:** PARTIALLY ACCEPTED — OL09-A + OL09-B + OL09-C ACCEPTED; OL09-D + OL09-E OPEN  
**Prepared:** 2026-09-08  
**OL09-A accepted:** 2026-09-08 — 30-day closure grace  
**OL09-B accepted:** 2026-09-08 — zero-retention webhook cutoff at authoritative Core `SUSPENDED`  
**OL09-C accepted:** 2026-09-08 — no additional generic product-data retention after closure grace  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-08 tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**OL09-A decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**OL09-B decision:** `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`  
**OL09-C decision:** `ecosystem/P0_2_OL_09_C_PRODUCT_DATA_RETENTION_TIMING_DECISION.md`  
**Related accepted credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Track the OL-09 retention/grace policy choices that block later organization-closure phases.

OL09-A, OL09-B and OL09-C are accepted. OL09-D and OL09-E remain open. OL08-D remains responsible for deciding which product-data classes are anonymized, hard-deleted or retained; OL09-C only fixes the timing rule for classes later accepted as irreversible disposition targets.

## Accepted OL09-A — closure grace / reversibility

A successful authoritative Core transition into the current `SUSPENDED` episode starts a **30-day reversible closure grace**.

```text
Core organization -> SUSPENDED
SUSPENDED through 30 days -> reversible grace; irreversible closure work prohibited
30-day grace satisfied    -> separately accepted irreversible phases may become eligible
```

Rules:

- exact deadline is `suspended_at + 30 days` using authoritative UTC suspension time,
- reactivation before grace completion invalidates the current closure progression,
- a later new suspension starts a fresh 30-day grace,
- process downtime does not reset or extend the clock,
- if the authoritative suspension timestamp cannot be established, grace completion fails closed,
- expiry only establishes time eligibility; it does not execute or independently authorize an irreversible phase.

Canonical decision: `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`.

## Accepted OL09-B — immediate webhook cutoff / zero signing-secret retention

The successful authoritative Core transition into `SUSPENDED` is also the effective MailerSend webhook security boundary.

Rules:

- all MailerSend webhook processing that could mutate tenant state ends at suspension,
- webhook signing-secret post-suspension retention is **0 days**,
- there is no suspended receive-only drain interval,
- the previous protective-event exception for unsubscribe, spam complaint and hard bounce is superseded,
- signing-secret use is unauthorized from the suspension boundary even if physical zeroization must be retried after an infrastructure failure,
- suspended-period webhook events are not replayed/backfilled after reactivation,
- reactivation does not resurrect a zeroized secret.

The separate OL09-A 30-day organization grace does not extend webhook or signing-secret retention.

Canonical decision: `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`.

## Accepted OL09-C — product-data timing

There is **no additional generic product-data retention interval** after the OL09-A 30-day closure grace.

```text
Core organization -> SUSPENDED
SUSPENDED through 30 days -> irreversible product-data disposition prohibited
30-day grace satisfied    -> OL08-D classes accepted as `anonymize` or `hard_delete` become time-eligible immediately
```

Rules:

- no generic `+30`, `+60`, `+90` or other post-grace product-data delay is introduced,
- this is eligibility only; it does not automatically delete/anonymize anything at the 30-day boundary,
- OL08-D must separately and explicitly classify each relevant product-data class,
- classes whose OL08-D disposition remains undecided remain ineligible regardless of elapsed time,
- a future longer time-based retention exception for a specific product-data class requires explicit separate acceptance/revision; runtime must not invent it,
- lifecycle, closure-execution, sequencing and phase-specific authorization checks still apply before irreversible mutation,
- reactivation before grace completion cancels eligibility from that suspension episode,
- if authoritative suspension time/grace evidence is unavailable, product-data eligibility fails closed.

Canonical decision: `ecosystem/P0_2_OL_09_C_PRODUCT_DATA_RETENTION_TIMING_DECISION.md`.

## What OL09-C does not decide

OL09-C does not choose:

- which customer/contact/fair/activity/quote/import/automation/mail or other product-data classes are anonymized,
- which classes are hard-deleted,
- which classes are retained,
- anonymization transformation shape,
- referential-integrity/deletion ordering,
- destructive worker implementation,
- audit/security evidence retention,
- generated-file/artifact expiry,
- backup ageing/restore reconciliation.

Those remain in OL08-D, OL09-D, OL09-E and OL-10 as applicable.

## Verified closure/runtime boundary

Certified/implemented slices currently provide:

- OL08-01 durable closure execution,
- OL08-02 quiescence certification,
- OL08-03A export manifest/completeness planning,
- OL08-04A credential disposition state/evidence foundation.

No organization-wide product-data anonymization/hard-delete worker, generated-artifact purge, closure-package delivery/expiry, cleanup-complete state or Core tombstone is authorized merely by OL09-A/B/C acceptance.

Current-model MailerSend API-token disposition also retains its separate `supported_unidentifiable` blocker until deterministic exact-token targeting exists; OL09-B signing-secret zeroization does not fabricate token revoke success.

## Remaining decision dimensions

### OL09-D — audit/security evidence retention — OPEN

Decide retention/transformation of non-secret control/security evidence including:

- closure execution/event evidence,
- export completeness/disposition evidence,
- credential-disposition evidence,
- external invalidation evidence,
- later cleanup/tombstone evidence if those phases are accepted.

Audit/security evidence is not product data for purposes of OL09-C and is not automatically deleted when the 30-day product-data eligibility boundary is reached.

### OL09-E — closure package / generated artifact expiry — OPEN

Decide timing semantics for future closure packages and generated artifacts while keeping ownership/deletion actions in OL08-B / OL08-E.

A future acceptance must identify the clock origin and expiry behavior without silently creating package/download or artifact-purge runtime.

### OL-10 — backup ageing / restore reconciliation — OPEN SEPARATE SCOPE

System backup retention, ageing, restore behavior and reconciliation remain OL-10 / OL08-G scope. OL09-A/B/C do not define backup deletion or post-restore cleanup semantics.

## Cross-cutting requirements for any future time-based/destructive runtime

Any later implementation must use:

- authoritative durable lifecycle/time evidence,
- UTC persistence/comparison,
- explicit policy version,
- organization + closure-execution + suspension-episode identity,
- idempotent/restart-safe behavior,
- deterministic handling after missed schedules/downtime,
- live lifecycle re-check before irreversible mutation,
- fail-closed handling of missing/malformed/stale authority evidence,
- no client/UI/operator-entered timer authority,
- no success solely because time elapsed while another required obligation remains blocked.

## OL09-A acceptance checklist — CLOSED

- [x] Successful Core `SUSPENDED` starts the grace.
- [x] Grace duration is 30 days using authoritative UTC suspension time.
- [x] Irreversible closure work is prohibited during grace.
- [x] Reactivation invalidates the current closure progression.
- [x] Later suspension starts a fresh grace.
- [x] Missing authoritative timestamp fails closed.
- [x] Grace expiry is eligibility only, not automatic execution.

## OL09-B acceptance checklist — CLOSED

- [x] Authoritative Core `SUSPENDED` is the webhook cutoff boundary.
- [x] Signing-secret post-suspension retention is 0 days.
- [x] No receive-only/protective webhook drain remains.
- [x] Secret use becomes unauthorized immediately at suspension.
- [x] Physical purge retry cannot reopen webhook authorization.
- [x] No suspended webhook replay/backfill after reactivation.
- [x] OL09-A 30-day grace remains separate.

## OL09-C acceptance checklist — CLOSED

- [x] No additional generic product-data retention after OL09-A grace.
- [x] OL08-D `anonymize` / `hard_delete` classes become time-eligible immediately after valid grace completion.
- [x] Eligibility does not automatically execute deletion/anonymization.
- [x] OL08-D still owns data-class disposition selection.
- [x] Undecided classes remain ineligible.
- [x] Longer class-specific time exceptions require explicit separate acceptance.
- [x] Reactivation/new-suspension semantics reuse OL09-A authority and clock rules.
- [x] Audit/security evidence, artifacts and backups remain outside OL09-C.

## Explicitly still not accepted

This document does **not** accept or authorize:

- any OL08-D product-data class disposition matrix or destructive runtime,
- MailerSend API-token revoke success for an unidentifiable token,
- audit/security evidence retention duration,
- generated-artifact purge,
- closure-package creation/download/expiry runtime,
- `not_required` export success without an accepted policy source,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Current resume point

**OL09-A, OL09-B and OL09-C are accepted. Next decision discussion: OL09-D — audit/security evidence retention. OL08-D remains separately open for the actual product-data disposition matrix.**
