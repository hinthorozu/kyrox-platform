# P0.2 OL-08-07 — Terminal Closure / Core Tombstone Runtime Acceptance

**Status:** RUNTIME ACCEPTED / CERTIFIED  
**Accepted:** 2026-09-11  
**Canonical policy:** `ecosystem/P0_2_OL_08_07_TERMINAL_CLOSURE_MILESTONE_DECISION.md`  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Product-data runtime dependency:** `ecosystem/P0_2_OL_08_D_RUNTIME_ACCEPTANCE.md`  
**Artifact/package runtime dependency:** `ecosystem/P0_2_OL_08_E2_RUNTIME_ACCEPTANCE.md`  
**Evidence-retention authority:** `ecosystem/P0_2_OL_09_D_AUDIT_SECURITY_RETENTION_DECISION.md`

## Purpose

Record runtime acceptance for the FAIR CRM terminal closure finalizer that implements the accepted OL08-07 terminal milestone and final Core organization tombstone contract.

This acceptance establishes the durable terminal timestamp needed by the accepted OL09-D 12-month retained-evidence clock. It does **not** implement OL08-F retained-evidence purge/de-identification; OL08-F is the next executable runtime slice.

## Accepted FAIR CRM runtime

FAIR CRM PR #270 implements the terminal closure orchestration after Core conditional tombstone support landed:

- migration `0083` expands closure execution state with durable terminal `completed`,
- closure execution responses expose authoritative `closed_at`,
- closure start/retry rejects an organization already tombstoned by Core,
- Core deletion uses the conditional suspension-episode contract through `X-Kyrox-Expected-Suspension-Updated-At`,
- the finalizer requires the exact current OL08-D 19/19 product-cleanup plan to be complete with zero residuals and one suspension episode,
- every applicable OL08-C credential disposition must be terminal,
- canonical package integrity evidence must exist,
- the accepted package availability period must have ended and strict package purge/non-existence evidence must be present,
- registered managed artifacts must have terminal cleanup/non-existence evidence,
- the first Core tombstone is allowed only while the same authoritative suspension episode remains current,
- after Core delete, FAIR re-reads Core lifecycle authority and derives `closed_at` only from authoritative Core `deleted_at`,
- a crash/restart after Core success but before FAIR completion reconciles from the already-tombstoned Core state without a second delete,
- repeated successful finalization is idempotent and does not emit another Core DELETE or duplicate terminal event,
- lifecycle authority outage, tombstone authority outage, episode drift, incomplete prerequisites and conflicting terminal state all fail closed.

## Terminal timestamp contract

The accepted runtime preserves one clock authority:

```text
Core tombstone succeeds
  -> Core lifecycle snapshot reports is_deleted = true
  -> Core lifecycle snapshot reports deleted_at = T_terminal
  -> FAIR closure execution records closed_at = T_terminal
  -> OL09-D retained-evidence clock starts at T_terminal
```

FAIR does not substitute request time, worker time, package time or a local wall clock for `closed_at`.

## Same-episode / restart reconciliation

The finalizer distinguishes a first tombstone attempt from reconciliation after a partial cross-repository failure.

For a first tombstone attempt it requires current, non-deleted, same-episode `SUSPENDED` authority and passes the expected suspension timestamp to Core's conditional deletion primitive.

If Core already completed the tombstone but FAIR did not commit terminal evidence, a later retry re-reads Core and may reconcile only when:

- Core reports `is_deleted = true`,
- Core reports authoritative non-null `deleted_at`,
- the FAIR closure execution and all required terminal prerequisites still identify a valid completed closure path.

The reconciliation path stores the exact existing Core timestamp; it does not manufacture a new terminal instant and does not issue a second Core delete.

## Pre-tombstone gate enforcement

The runtime enforces the accepted gate set before the final cross-repository mutation:

- SYSTEM / Platform SuperAdmin authority through the existing organization-delete permission boundary,
- current closure execution identity,
- live Core lifecycle authority,
- exact current suspension-episode continuity,
- complete OL08-D product-data cleanup evidence,
- terminal OL08-C credential evidence,
- canonical OL08-E1 package integrity evidence,
- terminal OL08-E2 managed-artifact evidence,
- package deadline completion plus strict package purge and positive non-existence evidence.

Package `expired` without successful physical purge is not accepted as terminal evidence. Product-data deletion alone is not accepted as provider invalidation or artifact cleanup proof.

## Post-tombstone behavior

After authoritative Core tombstone reconciliation:

- the FAIR closure execution is `completed`,
- terminal phase is `core_tombstone_completed`,
- `closed_at` mirrors exact Core `deleted_at`,
- a new closure execution cannot be started for the deleted organization,
- ordinary destructive pre-terminal APIs cannot treat the retained lifecycle status string as sufficient authority when `is_deleted = true`,
- the canonical package is already unavailable and strictly purged,
- minimal non-secret retained closure/audit/security evidence remains eligible for OL08-F only after the accepted 12-month period from `closed_at`.

## Regression / gate repair on final head

The first Development Standard run on the PR head exposed test-contract drift rather than a production-guard defect:

- older closure test doubles returned lifecycle snapshots with only `status`, while the accepted terminal guard correctly requires `is_deleted`,
- terminal test seeding inserted an artifact-inventory child before explicitly flushing its closure-package parent, which was unsafe under SQLite FK enforcement.

The final head fixes those regressions by aligning test lifecycle fixtures with the canonical snapshot shape (`is_deleted = false`) and explicitly flushing the package parent before inventory insertion.

The production tombstone/lifecycle guard was **not** weakened with a permissive `getattr(..., false)` fallback.

## Exact runtime evidence

Core prerequisite:

- Kyrox Core PR #30 was already merged on `main` at `5af3231dbf986ed79fed64c91644e93e2f1221d9`, providing the conditional tombstone primitive required by this runtime.

FAIR CRM PR #270:

- final head: `628c098ff2ddbfebaa5330aee94836089c54a304`,
- Development Standard Gate #769 / run `34574144876`: **SUCCESS**,
- Prod-Path E2E #313 / run `34574144891`: **SUCCESS**,
- FAIR CRM squash merge: `0c2f00649dccd217bd0affdb8fb95fc7de1ba462`,
- FAIR CRM `main` verified at that exact merge commit after merge.

## Explicitly not accepted by OL08-07 runtime

This acceptance does not authorize or certify:

- OL08-F purge/de-identification before the accepted 12-month deadline,
- retention of customer/product payloads or reusable secrets as closure evidence,
- secret-derived hashes/fingerprints as retained evidence,
- bypass of legal/security hold policy if a separately accepted hold contract applies,
- deletion of Core-owned or global system evidence outside FAIR's accepted owner scope,
- `not_required` export success without separate accepted policy authority,
- tombstone of an organization while any required FAIR terminal prerequisite is incomplete or blocked.

## Result

The accepted OL08-07 terminal milestone is now runtime-covered:

> **Core `deleted_at` is the authoritative terminal closure timestamp, FAIR `closed_at` mirrors it exactly, and final Core tombstone occurs only after the complete accepted FAIR closure gate set is satisfied.**

The next executable OL08 runtime slice is **OL08-F retained minimal closure/audit/security evidence purge/de-identification after 12 calendar months from the authoritative terminal `closed_at` / Core `deleted_at` timestamp**.