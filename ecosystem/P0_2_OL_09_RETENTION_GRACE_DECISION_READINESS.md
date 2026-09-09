# P0.2 OL-09 — Retention / Grace Decision Readiness

**Status:** PARTIALLY ACCEPTED — OL09-A + OL09-B + OL09-C + OL09-D ACCEPTED; OL09-E OPEN  
**Prepared:** 2026-09-09  
**OL09-A accepted:** 2026-09-08 — 30-day closure grace  
**OL09-B accepted:** 2026-09-08 — zero-retention webhook cutoff at authoritative Core `SUSPENDED`  
**OL09-C accepted:** 2026-09-08 — no additional generic product-data retention after closure grace  
**OL09-D accepted:** 2026-09-09 — 12-month minimal non-secret audit/security evidence retention after terminal closure  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-08 tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**OL09-A decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**OL09-B decision:** `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`  
**OL09-C decision:** `ecosystem/P0_2_OL_09_C_PRODUCT_DATA_RETENTION_TIMING_DECISION.md`  
**OL09-D decision:** `ecosystem/P0_2_OL_09_D_AUDIT_SECURITY_RETENTION_DECISION.md`  
**Related accepted credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Track the OL-09 retention/grace policy choices that block later organization-closure phases.

OL09-A through OL09-D are accepted. OL09-E remains open. OL08-D still owns the actual product-data disposition matrix; OL09-C only fixes timing for classes later accepted as irreversible disposition targets.

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
- signing-secret use is unauthorized from the suspension boundary even if physical zeroization must be retried after infrastructure failure,
- suspended-period webhook events are not replayed/backfilled after reactivation,
- reactivation does not resurrect a zeroized secret.

The separate OL09-A 30-day organization grace does not extend webhook or signing-secret retention.

Canonical decision: `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`.

## Accepted OL09-C — product-data timing

There is **no additional generic product-data retention interval** after the OL09-A 30-day closure grace.

```text
Core organization -> SUSPENDED
SUSPENDED through 30 days -> irreversible product-data disposition prohibited
30-day grace satisfied    -> OL08-D classes accepted as anonymize/hard_delete become time-eligible immediately
```

Rules:

- no generic `+30`, `+60`, `+90` or other post-grace product-data delay,
- this is eligibility only; it does not automatically delete/anonymize anything at the 30-day boundary,
- OL08-D must separately and explicitly classify each relevant product-data class,
- classes whose OL08-D disposition remains undecided remain ineligible regardless of elapsed time,
- a future longer class-specific time retention exception requires explicit separate acceptance/revision,
- lifecycle, closure-execution, sequencing and phase-specific authorization checks still apply before irreversible mutation,
- reactivation before grace completion cancels eligibility from that suspension episode,
- if authoritative suspension time/grace evidence is unavailable, product-data eligibility fails closed.

Canonical decision: `ecosystem/P0_2_OL_09_C_PRODUCT_DATA_RETENTION_TIMING_DECISION.md`.

## Accepted OL09-D — audit/security evidence retention

Eligible closure/audit/security evidence is retained for **12 months after the closure reaches a separately accepted durable terminal closure milestone**.

This is a post-closure evidence-retention rule, not a customer-data rule.

```text
closure in progress
  -> minimal non-secret evidence retained

terminal closure milestone
  -> 12-month evidence-retention clock starts

12 months elapsed
  -> eligible evidence may be deterministically purged or irreversibly de-identified
```

Rules:

- the clock does not start from `SUSPENDED`, from the 30-day grace boundary or from closure-execution creation,
- a closure that remains blocked does not consume its post-closure evidence-retention period,
- if no separately accepted durable terminal closure milestone/timestamp exists yet, the clock has not started,
- evidence is bounded to minimum non-secret identifiers/status/reason/policy/timestamp/outcome metadata needed to prove closure/control actions,
- API tokens, signing secrets, SMTP passwords, reusable credential material, customer/product records, message bodies, raw webhook payloads/signatures, generated binaries, closure-package content and backups are excluded,
- expiry is eligibility only; destructive evidence cleanup requires a separately implemented deterministic retention action,
- process downtime does not reset or extend the retention deadline,
- backup ageing/restore remains OL-10.

Canonical decision: `ecosystem/P0_2_OL_09_D_AUDIT_SECURITY_RETENTION_DECISION.md`.

## Verified closure/runtime boundary

Certified/implemented slices currently provide:

- OL08-01 durable closure execution,
- OL08-02 quiescence certification,
- OL08-03A export manifest/completeness planning,
- OL08-04A credential disposition state/evidence foundation.

No organization-wide product-data anonymization/hard-delete worker, generated-artifact purge, closure-package delivery/expiry, cleanup-complete state, terminal closure milestone implementation or Core tombstone is authorized merely by OL09-A/B/C/D acceptance.

Current-model MailerSend API-token disposition also retains its separate `supported_unidentifiable` blocker until deterministic exact-token targeting exists; OL09-B signing-secret zeroization does not fabricate token revoke success.

## Remaining decision dimensions

### OL09-E — closure package / generated artifact expiry — OPEN

Decide timing semantics for future closure packages and generated artifacts while keeping ownership/deletion actions in OL08-B / OL08-E.

A future acceptance must identify:

- which generated/package artifact classes receive an expiry clock,
- authoritative clock origin,
- duration,
- expiry behavior,
- handling of unmaterialized/deferred artifacts,
- interaction with closure completion without creating an implicit package/download runtime.

### OL08-D — product-data disposition matrix — OPEN SEPARATE POLICY

OL09-C does not select product-data actions. OL08-D must still decide which classes are anonymized, hard-deleted or retained and must define destructive ordering/integrity behavior before product-data cleanup runtime is authorized.

### OL-10 — backup ageing / restore reconciliation — OPEN SEPARATE SCOPE

System backup retention, ageing, restore behavior and reconciliation remain OL-10 / OL08-G scope. OL09-A/B/C/D do not define backup deletion or post-restore cleanup semantics.

## Cross-cutting requirements for future time-based/destructive runtime

Any later implementation must use:

- authoritative durable lifecycle/time evidence,
- UTC persistence/comparison,
- explicit policy version,
- organization + closure-execution identity,
- idempotent/restart-safe behavior,
- deterministic handling after missed schedules/downtime,
- live lifecycle re-check where lifecycle authority remains relevant,
- fail-closed handling of missing/malformed/stale authority evidence,
- no client/UI/operator-entered timer authority,
- no success solely because time elapsed while another required obligation remains blocked,
- no copying secrets or customer payloads into long-lived evidence before source deletion.

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
- [x] OL08-D anonymize/hard_delete classes become time-eligible immediately after valid grace completion.
- [x] Eligibility does not automatically execute deletion/anonymization.
- [x] OL08-D still owns data-class disposition selection.
- [x] Undecided classes remain ineligible.
- [x] Longer class-specific time exceptions require explicit separate acceptance.
- [x] Audit/security evidence, artifacts and backups remain outside OL09-C.

## OL09-D acceptance checklist — CLOSED

- [x] Retention duration: 12 months.
- [x] Scope: minimum non-secret closure/audit/security evidence only.
- [x] Clock origin: separately accepted durable terminal closure milestone/timestamp.
- [x] Clock does not run while closure remains unresolved/blocked.
- [x] Customer/product data, secrets, message bodies, raw webhook payloads, artifacts/packages and backups are excluded.
- [x] Historical closures without trustworthy terminal time fail closed; no fabricated deadline.
- [x] Retention expiry is eligibility only; purge/de-identification runtime remains separately gated.
- [x] Backup ageing/restore remains OL-10.

## Explicitly still not accepted

This document does **not** accept or authorize:

- any OL08-D product-data class disposition matrix or destructive runtime,
- MailerSend API-token revoke success for an unidentifiable token,
- generated-artifact purge,
- closure-package creation/download/expiry runtime,
- `not_required` export success without an accepted policy source,
- an evidence-purge worker merely because OL09-D duration is accepted,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Current resume point

**OL09-A through OL09-D are accepted. Next decision discussion: OL09-E — closure-package / generated-artifact expiry timing. OL08-D remains separately open for the actual product-data disposition matrix.**
