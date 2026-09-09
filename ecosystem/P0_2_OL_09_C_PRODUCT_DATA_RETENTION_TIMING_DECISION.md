# P0.2 OL-09C — Product-Data Retention Timing Decision

**Status:** ACCEPTED — NO ADDITIONAL GENERIC PRODUCT-DATA RETENTION AFTER CLOSURE GRACE  
**Accepted:** 2026-09-08  
**Parent readiness:** `ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`  
**Related grace decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**Related disposition matrix:** OL08-D — product-data disposition matrix (still open)

## Purpose

Define the timing rule for future organization product-data disposition after the accepted 30-day reversible closure grace, without choosing which FAIR CRM data classes are anonymized, hard-deleted or retained.

OL09-C is a timing decision only. OL08-D remains responsible for the actual disposition classification of product-data classes.

## Decision

There is **no additional generic product-data retention interval** after the accepted OL09-A 30-day closure grace.

The accepted rule is:

```text
Core organization -> SUSPENDED
SUSPENDED through 30 days -> reversible closure grace; irreversible product-data disposition prohibited
30-day grace satisfied   -> any OL08-D data class separately accepted as `anonymize` or `hard_delete` becomes time-eligible immediately
```

No additional `+30`, `+60`, `+90` or other generic post-grace delay is introduced by OL09-C.

This decision does not mean that all product data is automatically deleted at the 30-day boundary. It means only that **time itself imposes no further delay** once the OL09-A grace has been validly satisfied.

## Relationship to OL08-D

OL08-D remains open and must separately define the disposition action for each relevant FAIR CRM product-data class.

OL09-C does not choose:

- which classes are `hard_delete`,
- which classes are `anonymize`,
- which classes are retained,
- transformation shape for anonymization,
- referential-integrity sequencing,
- deletion order,
- runtime batch size or worker implementation.

If OL08-D later accepts a class as `anonymize` or `hard_delete`, that class has **0 days of additional generic retention after the OL09-A grace**.

A future proposal that requires a longer time-based retention period for a specific product-data class must be an explicit separately accepted exception/revision; it must not be silently introduced in runtime or inferred from implementation convenience.

## Eligibility boundary

Product-data disposition may become eligible only when all relevant guards are satisfied, including:

- the authoritative current Core suspension episode is still `SUSPENDED`,
- the authoritative suspension timestamp used for OL09-A is valid,
- the exact 30-day OL09-A grace has been satisfied,
- the closure execution belongs to the same organization and suspension episode,
- the closure execution has not been aborted or invalidated by reactivation,
- the target data class has an accepted OL08-D disposition action,
- any prerequisite export/credential/artifact/evidence obligation required by the accepted closure sequence is satisfied,
- the specific destructive/anonymization runtime has been separately authorized and implemented.

Time eligibility alone never fabricates permission to mutate a class whose OL08-D disposition remains undecided.

## Reactivation semantics

If Core transitions the organization from `SUSPENDED` back to `ACTIVE` before the 30-day grace is satisfied:

- the current closure progression is invalidated under OL09-A,
- no product-data anonymization or hard-delete becomes eligible from that suspension episode,
- a later new suspension starts a new 30-day grace from the new authoritative suspension timestamp.

A prior suspension episode or prior grace completion must not be reused to accelerate a later closure attempt.

## Pre-existing suspended organizations

Where the authoritative current-suspension timestamp cannot be established, OL09-A already fails closed.

OL09-C therefore must not fabricate product-data eligibility from:

- FAIR CRM closure creation time,
- first-observed suspension time,
- worker start time,
- UI/operator-entered timestamps,
- guessed historical dates.

Without valid OL09-A grace evidence, product-data disposition remains ineligible.

## What is outside OL09-C

The following remain separate decisions:

- **OL09-D / OL08-F:** audit, security and closure-evidence retention,
- **OL09-E / OL08-B / OL08-E:** closure-package and generated-artifact expiry/disposition,
- **OL-10 / OL08-G:** backup ageing and restore reconciliation,
- provider credential disposition and remaining MailerSend token invalidation blockers,
- final `cleanup_complete` / `ready_for_tombstone` sequencing,
- Core organization tombstone/delete.

Audit/security evidence must not be swept into product-data deletion merely because OL09-C has no extra product-data retention period.

Generated files/artifacts must not be treated as product-data rows for purposes of this timing decision.

## Runtime authorization boundary

This policy acceptance does **not** authorize organization-wide delete/anonymize runtime by itself.

A later bounded runtime slice may enforce the OL09-C timing rule only after OL08-D has accepted the relevant class disposition and the required destructive-phase engineering boundary has been separately authorized.

Any such runtime must be:

- organization-scoped,
- class-explicit rather than database-dump driven,
- idempotent and restart-safe,
- fail-closed on lifecycle/time ambiguity,
- tied to one closure execution and suspension episode,
- auditable without preserving deleted secret/customer payloads as evidence,
- safe under partial failure and retry.

## Decision summary

**OL09-C is accepted: FAIR CRM product-data classes that OL08-D later and explicitly classifies as `anonymize` or `hard_delete` have no additional generic retention period after the accepted 30-day closure grace. Once that grace is validly satisfied, those classes are time-eligible immediately, subject to their separately accepted disposition action, closure sequencing, lifecycle checks and runtime authorization. This decision does not itself select data classes or authorize deletion/anonymization.**
