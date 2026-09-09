# P0.2 OL-09 — Retention / Grace Decision Readiness

**Status:** ACCEPTED — OL09-A THROUGH OL09-E TIMING POLICY COMPLETE; RUNTIME/ACTION MATRICES REMAIN SEPARATELY GATED  
**Prepared:** 2026-09-09  
**OL09-A accepted:** 2026-09-08 — 30-day closure grace  
**OL09-B accepted:** 2026-09-08 — zero-retention webhook cutoff at authoritative Core `SUSPENDED`  
**OL09-C accepted:** 2026-09-08 — no additional generic product-data retention after closure grace  
**OL09-D accepted:** 2026-09-09 — 12-month minimal non-secret audit/security evidence retention after terminal closure  
**OL09-E accepted:** 2026-09-09 — no additional generic product-artifact retention after grace; future closure package 30 days from durable availability  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-08 tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**OL09-A decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**OL09-B decision:** `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`  
**OL09-C decision:** `ecosystem/P0_2_OL_09_C_PRODUCT_DATA_RETENTION_TIMING_DECISION.md`  
**OL09-D decision:** `ecosystem/P0_2_OL_09_D_AUDIT_SECURITY_RETENTION_DECISION.md`  
**OL09-E decision:** `ecosystem/P0_2_OL_09_E_ARTIFACT_EXPIRY_DECISION.md`  
**Related accepted credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Track and close the OL-09 time/grace choices needed by organization offboarding.

OL09-A through OL09-E are now accepted as timing policy. This does **not** mean organization offboarding is implementation-complete. OL08-D still owns relational product-data disposition actions, OL08-E still owns artifact-class disposition/package lifecycle actions, credential blockers remain where provider targeting is unresolved, and OL-10 still owns backup ageing/restore reconciliation.

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
- missing/unverified authoritative suspension time fails closed,
- expiry is eligibility only and does not execute or independently authorize irreversible work.

Canonical decision: `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`.

## Accepted OL09-B — immediate webhook cutoff / zero signing-secret retention

The successful authoritative Core transition into `SUSPENDED` is also the effective MailerSend webhook security boundary.

Rules:

- all MailerSend webhook processing that could mutate tenant state ends at suspension,
- webhook signing-secret post-suspension retention is **0 days**,
- there is no suspended receive-only/protective drain interval,
- signing-secret use becomes unauthorized at the suspension boundary even if physical purge must be retried,
- suspended-period webhook events are not replayed/backfilled after reactivation,
- reactivation does not resurrect a zeroized secret,
- OL09-A's separate 30-day organization grace does not extend webhook/signing-secret retention.

Canonical decision: `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`.

## Accepted OL09-C — product-data timing

There is **no additional generic product-data retention interval** after the OL09-A 30-day closure grace.

```text
Core organization -> SUSPENDED
SUSPENDED through 30 days -> irreversible product-data disposition prohibited
30-day grace satisfied    -> OL08-D classes accepted as anonymize/hard_delete become time-eligible
```

Rules:

- no generic `+30`, `+60`, `+90` or other post-grace product-data delay,
- eligibility does not automatically delete/anonymize anything,
- OL08-D must separately classify each relevant product-data class,
- undecided classes remain ineligible regardless of elapsed time,
- longer class-specific retention requires explicit separate acceptance,
- lifecycle/closure/phase-specific gates remain mandatory.

Canonical decision: `ecosystem/P0_2_OL_09_C_PRODUCT_DATA_RETENTION_TIMING_DECISION.md`.

## Accepted OL09-D — audit/security evidence retention

Eligible minimal non-secret closure/audit/security evidence is retained for **12 months after the closure reaches a separately accepted durable terminal closure milestone**.

```text
closure in progress
  -> minimum non-secret evidence retained

terminal closure milestone
  -> 12-month evidence-retention clock starts

12 months elapsed
  -> eligible evidence may be deterministically purged or irreversibly de-identified
```

Rules:

- the clock does not start from `SUSPENDED`, the 30-day grace boundary or closure-execution creation,
- a blocked/unresolved closure does not consume its post-closure evidence-retention period,
- without a trustworthy accepted terminal milestone/timestamp the clock has not started,
- secrets, customer/product records, message bodies, raw webhook payloads/signatures, generated binaries, closure-package content and backups are excluded,
- expiry is eligibility only; evidence cleanup runtime remains separately gated,
- backups remain OL-10.

Canonical decision: `ecosystem/P0_2_OL_09_D_AUDIT_SECURITY_RETENTION_DECISION.md`.

## Accepted OL09-E — closure package / generated artifact expiry

OL09-E uses **two timing classes** rather than one shared artifact clock.

### Existing product/generated artifacts

For artifact classes that OL08-E later explicitly accepts for delete/expiry:

```text
Core organization -> SUSPENDED
SUSPENDED through 30 days -> irreversible artifact deletion prohibited
30-day grace satisfied    -> accepted OL08-E delete/expire classes become time-eligible
```

There is no additional generic post-grace artifact retention interval.

Time eligibility does not authorize deletion by itself. Source artifacts must remain while an accepted required export/package completeness or integrity obligation still depends on them, and OL08-E must separately authorize the class/action and destructive ordering.

### Future persistent closure package

If OL08-B / OL08-E later authorizes persistent closure-package materialization:

```text
canonical package becomes durably available at P0
P0 .. P0 + 30 days -> authorized package availability window
P0 + 30 days       -> package expires and becomes purge-eligible
```

Rules:

- package retention duration is **30 days**,
- clock origin is the durable UTC timestamp when the canonical package first reaches the accepted available/ready-for-authorized-retrieval state,
- the clock does not start from suspension, grace expiry, planning, generation start, first download or last download,
- downloads/access do not reset the clock,
- process downtime does not reset or extend the clock,
- no materialized package means no package expiry clock,
- at expiry the package must no longer be presented as available and its bytes become purge-eligible,
- physical purge remains a separately implemented idempotent action,
- an expired package is not silently regenerated/resurrected,
- minimal non-secret package lifecycle evidence remains governed by OL09-D rather than the package-retention period.

Canonical decision: `ecosystem/P0_2_OL_09_E_ARTIFACT_EXPIRY_DECISION.md`.

## OL-09 timing policy summary

| Slice | Accepted timing rule |
| --- | --- |
| OL09-A | 30-day reversible grace from authoritative Core `SUSPENDED`. |
| OL09-B | Webhook signing-secret post-suspension retention = 0 days; effective cutoff at `SUSPENDED`. |
| OL09-C | No generic extra product-data retention after the 30-day grace; accepted OL08-D irreversible classes become time-eligible then. |
| OL09-D | Minimal non-secret audit/security evidence retained 12 months from accepted durable terminal closure milestone. |
| OL09-E / product artifacts | No generic extra retention after the 30-day grace; OL08-E action/export dependencies still gate deletion. |
| OL09-E / closure package | Future persistent package retained 30 days from durable canonical availability/readiness. |

## Verified closure/runtime boundary

Certified/implemented slices currently provide:

- OL08-01 durable closure execution,
- OL08-02 quiescence certification,
- OL08-03A export manifest/completeness planning,
- OL08-04A credential disposition state/evidence foundation.

OL09 timing acceptance does **not** by itself authorize:

- organization-wide product-data anonymization/hard-delete,
- product/generated-artifact deletion,
- persistent closure-package materialization or customer-facing delivery,
- audit-evidence purge runtime,
- cleanup-complete / ready-for-tombstone,
- Core tombstone.

Current-model MailerSend API-token disposition also retains its separate `supported_unidentifiable` blocker until deterministic exact-token targeting exists; OL09-B signing-secret zeroization does not fabricate API-token revoke success.

## Remaining non-OL09 decision/implementation gates

### OL08-D — product-data disposition matrix

Still open. OL09-C fixes timing only. OL08-D must decide which relational product-data classes are anonymized, hard-deleted, retained, or otherwise transformed and must define integrity/deletion ordering.

### OL08-E — artifact disposition / package lifecycle

Still open as an action/ownership contract. OL09-E fixes timing only. OL08-E must classify uploads/generated artifacts/assets/results, define actual purge handlers, and separately accept any closure-package materialization/availability/delivery lifecycle.

### Provider credential completion

MailerSend exact API-token invalidation remains blocked while the exact reusable provider token cannot be deterministically targeted.

### OL-10 — backup ageing / restore reconciliation

Still open separate scope. Database backup retention, ageing, restore behavior and post-restore reconciliation remain OL08-G / OL-10 decisions.

## Cross-cutting requirements for later time-based/destructive runtime

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

## Acceptance checklists — CLOSED

### OL09-A

- [x] Successful Core `SUSPENDED` starts the 30-day grace.
- [x] Irreversible closure work is prohibited during grace.
- [x] Reactivation invalidates the current closure progression.
- [x] Missing authoritative timestamp fails closed.
- [x] Grace expiry is eligibility only.

### OL09-B

- [x] Core `SUSPENDED` is the webhook cutoff boundary.
- [x] Signing-secret post-suspension retention is 0 days.
- [x] No receive-only/protective webhook drain remains.
- [x] Physical purge retry cannot reopen webhook authorization.
- [x] OL09-A grace remains separate.

### OL09-C

- [x] No additional generic product-data retention after grace.
- [x] OL08-D irreversible classes become time-eligible after valid grace completion.
- [x] OL08-D still owns class/action selection.
- [x] Undecided classes remain ineligible.

### OL09-D

- [x] Retention duration is 12 months.
- [x] Scope is minimal non-secret closure/audit/security evidence only.
- [x] Clock starts from separately accepted durable terminal closure milestone.
- [x] Customer/product data, secrets, artifacts/packages and backups are excluded.
- [x] Expiry does not itself execute purge/de-identification.

### OL09-E

- [x] Existing OL08-E delete/expire artifact classes receive no generic post-grace retention extension.
- [x] Required export/package dependencies gate source-artifact destruction.
- [x] Future persistent closure-package retention is 30 days.
- [x] Package clock starts from durable canonical package availability/readiness.
- [x] Downloads/access do not reset package expiry.
- [x] No package object means no package clock.
- [x] Expired package becomes unavailable and purge-eligible; physical purge remains separately gated.
- [x] Backups remain OL-10.

## Explicitly still not accepted/authorized

This OL09 acceptance does not authorize:

- any OL08-D product-data class disposition matrix or destructive runtime,
- any OL08-E product-artifact purge handler solely because timing is accepted,
- persistent closure-package creation/download/delivery runtime,
- `not_required` export success without an accepted policy source,
- MailerSend API-token revoke success for an unidentifiable token,
- an audit-evidence purge worker solely because OL09-D duration is accepted,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Current resume point

**OL09-A through OL09-E timing decisions are accepted. OL09 retention/grace decision-readiness is complete. Resume organization-offboarding policy work at the remaining action/ownership gates: OL08-D product-data disposition matrix, OL08-E artifact/package lifecycle, unresolved provider credential targeting, and OL-10 backup ageing/restore reconciliation.**
