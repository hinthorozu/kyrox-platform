# P0.2 OL-08-07 — Terminal Closure Milestone / Core Tombstone Decision

**Status:** ACCEPTED — TERMINAL MILESTONE AND FINAL CORE TOMBSTONE CONTRACT ACCEPTED; RUNTIME STILL GATED  
**Accepted:** 2026-09-10  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Readiness source:** `ecosystem/P0_2_OL_08_DECISION_READINESS.md`  
**Product-data runtime acceptance:** `ecosystem/P0_2_OL_08_D_RUNTIME_ACCEPTANCE.md`  
**Artifact/package runtime acceptance:** `ecosystem/P0_2_OL_08_E2_RUNTIME_ACCEPTANCE.md`  
**Evidence-retention authority:** `ecosystem/P0_2_OL_09_D_AUDIT_SECURITY_RETENTION_DECISION.md`  
**Package-retention authority:** `ecosystem/P0_2_OL_09_E_ARTIFACT_EXPIRY_DECISION.md`

## Purpose

Define the missing durable terminal closure milestone and the conditions under which FAIR CRM may invoke the final Core organization tombstone.

This decision closes the clock-source dependency left intentionally open by OL09-D. It does **not** implement the tombstone runtime or the later OL08-F evidence purge. It defines the only milestone from which the accepted 12-month retained-evidence clock may start.

## Accepted terminal milestone

The authoritative durable terminal closure milestone is:

> **the successful Core organization tombstone, evidenced by Core's authoritative non-null `deleted_at` timestamp for the organization after every required FAIR closure obligation has been satisfied.**

The timestamp authority is Core.

FAIR CRM must not manufacture a terminal timestamp from its own wall clock. After the final tombstone, FAIR's closure execution `closed_at` must equal the exact authoritative Core `deleted_at` instant, normalized to UTC without changing the instant.

Therefore OL09-D becomes operationally anchored as:

```text
all accepted FAIR closure obligations complete
  -> final Core organization tombstone succeeds
  -> Core lifecycle snapshot reports is_deleted = true
  -> Core lifecycle snapshot reports deleted_at = T_terminal
  -> FAIR durably records closure closed_at = T_terminal
  -> OL09-D 12-month retained-evidence clock starts at T_terminal
```

No earlier timestamp starts that clock.

## Why Core `deleted_at` is the authority

Core is already the canonical organization lifecycle authority and owns the organization tombstone.

The current Core implementation provides the required deterministic primitive:

- organization deletion is a soft tombstone recorded in Core,
- the tombstone writes Core-owned `deleted_at`,
- the product lifecycle snapshot reads organizations including deleted rows,
- the snapshot exposes `is_deleted`, `deleted_at`, `status`, `work_allowed` and `updated_at`,
- FAIR can therefore re-read the authoritative terminal state after the mutation and after a partial cross-repository failure.

Using FAIR request time, worker time, package expiry time or operator-entered time would create a second lifecycle clock and is rejected.

## Tombstone is the final cross-repository lifecycle mutation

The Core organization tombstone remains the **last lifecycle mutation** in the closure sequence.

FAIR CRM may not invoke Core deletion merely because the organization has been suspended for 30 days or because OL08-D product rows have been removed.

Immediately before the first tombstone request, the finalizer must re-evaluate current durable closure evidence and fail closed unless every applicable prerequisite below is satisfied.

## Accepted pre-tombstone gate set

### 1. Closure execution identity

- the target FAIR closure execution exists for the target organization,
- it is still the open/current execution,
- it has not already been terminalized under a conflicting milestone,
- the caller has Platform SuperAdmin / SYSTEM authority through the existing `identity.organizations.delete` permission boundary.

### 2. Current Core lifecycle / episode continuity

Before issuing a first Core delete request:

- Core lifecycle authority must be reachable and valid,
- the organization must not already be deleted unless this is a reconciliation of a previously attempted terminalization,
- for a first tombstone request the organization must still be `SUSPENDED`,
- the completed OL08-D product-cleanup evidence must belong to the same authoritative current suspension episode.

A reactivation/new-suspension cycle may never reuse completed destructive evidence from an older suspension episode to authorize a tombstone.

### 3. Required export/package obligation

The required canonical closure package must have been successfully materialized and integrity-verified under the accepted OL08-E1 contract.

A planning manifest alone is not sufficient.

### 4. Managed source-artifact obligation

Every registered current-model artifact inventory item must be in its accepted terminal disposition before tombstone:

- managed file artifacts: `purged` or positively reconciled `already_absent`,
- embedded import bytes: positively reconciled `already_absent` after OL08-D relational deletion,
- external references: `not_applicable` and never remote-deleted by FAIR.

No `pending`, `blocked` or `relational_delete_required` artifact may pass the final gate.

### 5. Provider credential obligation

Every credential disposition applicable to the closure execution must be terminal under OL08-C.

A still-blocked MailerSend exact-secret verification, generic SMTP operator requirement, retained reusable send secret or unresolved provider invalidation obligation blocks final tombstone.

Product-row deletion is not provider invalidation proof.

### 6. Product-data obligation

The complete accepted OL08-D current-model dependency plan must be complete:

- all 19 registered product-data classes have terminal successful hard-delete evidence,
- no class is pending or blocked,
- current residual-row checks passed,
- the evidence belongs to the authoritative current suspension episode.

### 7. Closure-package availability and strict purge

The final Core tombstone must not shorten the accepted OL09-E package availability window.

Current package retrieval requires live Core `SUSPENDED` plus an open closure execution. Therefore a normal successful terminal closure must wait until:

- the canonical package has reached its accepted `ready_at + 30 days` retrieval deadline,
- retrieval authorization has ended,
- the package has then been strictly purged under OL08-E2,
- package non-existence has been positively verified,
- the durable package record is `purged` with valid purge evidence.

`expired` alone is not sufficient final-closure evidence. A failed physical purge remains blocked.

This gate is specific to the currently accepted SYSTEM/operator-only package delivery model. A future delivery model may revise the interaction only through a new explicit policy decision.

### 8. Backup/restore boundary

OL10 backup ageing and restore reconciliation remain separate system-level obligations. The tombstone does not claim that every historical disaster-recovery image has already aged out.

A restore that reintroduces a tombstoned organization remains governed by the accepted OL10 fail-closed lifecycle reconciliation contract.

## Cross-repository terminalization protocol

The accepted runtime shape is deliberately reconciliation-first and restart-safe.

### First attempt

```text
FAIR validates every pre-tombstone gate
  -> FAIR re-reads Core and confirms current same-episode SUSPENDED / not deleted
  -> FAIR invokes Core DELETE for that exact organization under SYSTEM authority
  -> FAIR re-reads Core product lifecycle snapshot
  -> require is_deleted = true and deleted_at != null
  -> FAIR stores closed_at = exact Core deleted_at
  -> FAIR records bounded terminal evidence
```

The Core DELETE response by itself is not the terminal timestamp authority. The post-delete authoritative lifecycle snapshot is.

### Partial failure / retry

A cross-repository transaction cannot be atomic, so the accepted recovery contract is:

- if Core tombstone succeeded but FAIR failed before storing terminal evidence, retry must **not** fabricate a new timestamp or require a second lifecycle episode,
- retry re-reads Core including deleted organizations,
- if `is_deleted = true` and `deleted_at` is present, FAIR may reconcile `closed_at` to that exact Core timestamp **only after revalidating that the FAIR closure prerequisites are complete and identify the same closure execution**, 
- repeated successful reconciliation is idempotent,
- conflicting pre-existing FAIR terminal evidence fails closed rather than being overwritten.

If Core is already deleted but FAIR prerequisites are incomplete, the finalizer must not falsely declare successful closure. That condition is an explicit blocked/manual-reconciliation state, because the final lifecycle mutation occurred outside the accepted ordering.

## FAIR terminal state

The runtime should make terminal closure explicit rather than leaving a closed execution labeled as ordinary in-progress work.

Accepted semantics:

- terminal successful execution status: `completed`,
- terminal phase: `core_tombstone_completed`,
- `closed_at`: exact authoritative Core `deleted_at`,
- `updated_at`: may record FAIR persistence time but is not the retention-clock authority,
- terminal evidence must include organization id, closure execution id, policy/version identifiers and bounded outcome metadata only.

No customer/product payload, reusable secret, raw credential material or secret-derived fingerprint may be added to terminal evidence.

## Post-tombstone behavior

After authoritative Core deletion:

- the organization cannot be reactivated through the normal lifecycle path,
- a new FAIR closure execution for the same deleted organization must not be created,
- destructive pre-terminal closure APIs must not treat the retained Core status value alone as sufficient `SUSPENDED` authority; `is_deleted = true` is terminal,
- package retrieval is already over because strict package purge is a pre-tombstone gate,
- retained minimal non-secret closure/audit/security evidence remains available for its accepted OL09-D period,
- OL08-F may later purge/de-identify that evidence only after 12 months from the exact terminal `deleted_at`/`closed_at` milestone.

## OL08-F clock binding

This decision supplies the separately accepted milestone required by OL09-D.

The only accepted OL08-F retention deadline is:

```text
T_terminal = authoritative Core deleted_at
retention_deadline = T_terminal + 12 calendar months
```

The implementation must use exact UTC-aware timestamps and deterministic calendar-month arithmetic consistent with the accepted OL09-D policy.

The clock must not be substituted with:

- suspension `updated_at`,
- suspension grace completion,
- package `ready_at`, `expires_at` or `purged_at`,
- OL08-D completion time,
- closure execution `created_at`,
- worker observation time,
- operator input.

## Failure semantics

Final tombstone is fail-closed.

The finalizer must not:

- force Core deletion around an unavailable lifecycle authority,
- accept a different suspension episode,
- ignore incomplete/blocked credential dispositions,
- ignore incomplete artifact inventory,
- accept partial OL08-D completion,
- tombstone while the canonical package is still within its 30-day retrieval window,
- accept package `expired` without successful strict purge/non-existence evidence,
- manufacture `closed_at` before observing Core `deleted_at`,
- mark a prematurely externally tombstoned organization as cleanly completed when FAIR prerequisites were not satisfied.

## Explicitly not implemented by this decision

This policy acceptance does not itself implement:

- the FAIR terminal-finalizer endpoint/service,
- the Core DELETE client adapter,
- FAIR execution status-constraint expansion for `completed`,
- start-path hardening for already-deleted Core organizations,
- OL08-F 12-month evidence purge/de-identification,
- legal/security hold runtime beyond separately accepted policy,
- deletion of Core-owned or system-global audit material outside the accepted owner scope.

## Result

The missing terminal closure timestamp authority is now defined:

> **Core tombstone `deleted_at` is the terminal closure milestone, and FAIR `closed_at` must mirror that exact instant after every accepted FAIR closure gate is complete.**

The next executable runtime slice is **OL08-07 final Core tombstone orchestration / terminal milestone reconciliation**. After that runtime is certified, OL08-F evidence purge can be implemented against the now-defined 12-month clock.