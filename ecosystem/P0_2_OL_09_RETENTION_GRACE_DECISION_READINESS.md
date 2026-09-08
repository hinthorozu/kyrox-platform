# P0.2 OL-09 — Retention / Grace Decision Readiness

**Status:** DECISION READINESS — NOT ACCEPTED  
**Prepared:** 2026-09-08  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-08 tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Related accepted credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Prepare the unresolved OL-09 retention/grace policy choices that now block later organization-closure phases.

This document is **readiness only**. It does not select a number of hours/days, does not authorize a purge scheduler, does not authorize product-data/artifact destruction, and does not change Core organization lifecycle behavior.

## Why OL-09 is now the next safe decision gate

The bounded OL08-A/B/C runtime has established non-destructive orchestration, quiescence, export completeness planning and credential-disposition evidence. The remaining irreversible work cannot safely infer time policy from implementation convenience.

OL-09 now materially blocks or constrains:

- **OL08-C4:** final zeroization of a webhook signing secret when the accepted receive-only drain criterion is time-based,
- **OL08-D:** product-data anonymization/hard-delete timing,
- **OL08-F:** retention of closure/audit/security evidence,
- **OL08-B / OL08-E:** expiry/retention semantics for any future closure package and generated/binary artifacts,
- final closure sequencing before `cleanup_complete` / `ready_for_tombstone` can ever be considered.

**OL08-G / backup ageing and restore reconciliation remain OL-10 scope.** OL-09 must not silently define backup behavior.

## Verified current lifecycle facts

### 1. No retention/grace duration is currently accepted

ADR-0006 keeps OL-09 open. Existing OL08 contracts explicitly prohibit inventing hours/days in runtime.

Therefore a duration appearing only in code, a worker schedule, an environment variable, provider documentation or an implementation default would **not** constitute accepted policy.

### 2. Closure begins only from Core `SUSPENDED`

The current FAIR CRM closure execution may start only while live Core lifecycle authority reports a non-deleted `SUSPENDED` organization.

The closure execution is durable FAIR CRM state; Core remains lifecycle authority and Core tombstone remains the final cross-repository mutation.

### 3. Current OL08 closure runtime is still intentionally non-destructive

Certified/implemented slices currently provide:

- OL08-01 durable closure execution,
- OL08-02 quiescence certification against OL-07 runtime guards,
- OL08-03A export manifest/completeness planning only,
- OL08-04A credential disposition state/evidence foundation.

No organization-wide product-data deletion, artifact purge, closure-package delivery/expiry, cleanup-complete state or Core tombstone is authorized.

### 4. Credential disposition has an explicit time-policy dependency

OL08-C accepts receive-only webhook handling after outbound disablement.

A webhook signing secret may remain `receive_only_pending` only to verify delayed events belonging to previously handed-off work. Final signing-secret zeroization is mandatory before full credential disposition can complete.

If the drain criterion depends on elapsed time, **OL-09 must define that criterion/duration**. OL08-C deliberately did not invent one.

### 5. Current-model MailerSend token disposition has a separate non-time blocker

OL08-04A currently classifies MailerSend API tokens as `supported_unidentifiable` because the existing model does not have deterministic validated targeting for the exact provider token. That problem does **not** become solved by waiting a grace period.

OL-09 must not turn an unresolved provider-targeting problem into time-based success.

### 6. Product-data disposition is not yet accepted

OL08-D remains open. No current policy says which FAIR CRM data classes are anonymized, hard-deleted, retained, or retained for different periods after closure.

A grace duration therefore cannot by itself authorize product-data destruction; OL08-D must still define the class-level disposition matrix.

### 7. Audit/security evidence retention is a separate policy concern

Closure execution events, export-plan evidence and credential-disposition evidence are intentionally append-only/non-secret control evidence. OL08-F remains open and no accepted retention duration currently exists for that evidence.

Product-data retention and security/audit evidence retention must not be assumed to use the same duration.

### 8. Backup/restore timing remains separate

Existing system backup/restore capability is database-level administration, not organization closure export or tenant rollback.

OL-09 may define live/product-store timing, but backup ageing, backup-retention guarantees and restoration reconciliation remain OL-10 decisions.

## Decision dimensions that must be resolved

### OL09-A — closure grace / reversibility policy

Decide whether an accepted grace period exists between closure initiation and the first irreversible product-data/artifact phase.

Questions:

1. Is there a reversible grace window at all?
2. If yes, what event starts the clock?
   - Core transition to `SUSPENDED`,
   - FAIR CRM closure-execution creation,
   - a separately recorded closure-request/approval timestamp,
   - another explicit lifecycle event.
3. Which authority may cancel/abort closure during the grace window?
4. Is Core `SUSPENDED -> ACTIVE` reactivation allowed while a closure execution is open?
5. If reactivation is allowed, what durable transition closes/aborts the FAIR CRM closure execution and prevents later stale cleanup from running?
6. If grace expires, does expiry merely make later phases **eligible**, or does it automatically execute them?

**Recommended safety rule for decision:** elapsed time should only make an accepted phase eligible; it should not by itself bypass phase-specific authorization, lifecycle re-checks or failure evidence.

### OL09-B — webhook receive-only drain criterion

Decide how OL08-C4 leaves `receive_only_pending`.

Possible policy shapes to choose between include:

- a fixed maximum elapsed-time window,
- a provider-specific deterministic terminal-event criterion,
- a hybrid criterion: terminal evidence **or** maximum elapsed-time ceiling,
- an explicitly accepted no-drain case for credential classes where no signing secret exists.

Questions:

1. Is the criterion provider-specific or ecosystem-wide?
2. If time-based, what exact duration applies?
3. What timestamp starts the drain clock?
4. Do delayed webhooks after the final purge become ignored, logged as unverifiable, or handled through another non-secret mechanism?
5. What happens when provider state remains ambiguous at expiry?

The criterion must not permit new outbound provider use.

### OL09-C — product-data retention/grace timing

Timing must be defined separately from OL08-D's class-level disposition action.

For each OL08-D class that eventually becomes `anonymize` or `hard_delete`, decide:

- immediate eligibility after accepted closure/grace conditions,
- one common grace duration,
- class-specific retention duration,
- permanent/longer retention where separately justified by an accepted policy.

No legal/compliance duration is assumed by this readiness document. If KVKK/GDPR, tax, contractual or litigation requirements materially affect a class, the maintainer must supply/accept that requirement explicitly rather than the implementation inventing it.

### OL09-D — audit/security evidence retention

Decide whether control evidence follows a retention period distinct from customer/product data.

Evidence classes include at least:

- closure execution/event evidence,
- export completeness/disposition evidence,
- credential-disposition evidence,
- external invalidation evidence,
- final cleanup/tombstone evidence when those phases are later accepted.

Questions:

1. How long is each evidence class retained?
2. Is actor identity retained verbatim, reduced, pseudonymized or otherwise transformed after a period?
3. Which non-secret identifiers must remain to prove closure correctness?
4. Does evidence survive product-data deletion?

### OL09-E — closure package / generated artifact expiry timing

This is only a timing dependency; package/artifact ownership and deletion actions remain OL08-B / OL08-E policy.

Questions:

1. If a future closure package is materialized, how long is it retrievable?
2. Is package expiry measured from creation, successful handover, first download, or closure completion?
3. Are generated/binary product artifacts deleted on the same schedule as structured product data or separately?
4. How are failed/partial artifact deletions retried and evidenced?

OL-09 must not create a package lifecycle that OL08-B has not yet accepted.

## Cross-cutting clock/state requirements

Any accepted time-based policy should define at minimum:

- authoritative timestamp/event that starts each clock,
- UTC persistence and comparison semantics,
- policy version recorded with durable execution/evidence,
- idempotent restart behavior after process downtime,
- behavior when the scheduled execution was missed,
- lifecycle re-check immediately before an irreversible mutation,
- no reliance on a client/UI timer,
- no transition to success solely because a timer elapsed when another required obligation is blocked.

Existing closure executions created before a policy version is accepted also require explicit migration/backfill semantics; they must not silently receive a retroactive destructive deadline.

## Recommended decision decomposition

OL-09 does not need to be accepted as one monolithic duration. A safer acceptance order is:

1. **OL09-A — closure grace/reversibility and clock origin**,
2. **OL09-B — webhook receive-only drain criterion**,
3. **OL09-C — product-data retention timing**, coordinated with OL08-D,
4. **OL09-D — audit/security evidence retention**, coordinated with OL08-F,
5. **OL09-E — package/artifact expiry timing**, coordinated with OL08-B / OL08-E.

This decomposition allows a narrow decision to unblock a narrow runtime without implicitly authorizing unrelated destructive behavior.

## Acceptance checklist

Before any OL-09 subsection becomes accepted, record explicitly:

- [ ] exact policy scope/data or credential class,
- [ ] clock-start event,
- [ ] exact criterion or duration if time-based,
- [ ] reversible vs irreversible meaning,
- [ ] permitted authority/actor,
- [ ] interaction with Core reactivation,
- [ ] retry/restart semantics,
- [ ] audit/evidence requirements,
- [ ] treatment of pre-existing closure executions,
- [ ] explicit boundary against OL-10 backups,
- [ ] exact runtime slice authorized by that acceptance.

## Explicitly not accepted by this readiness document

This document does **not** accept or authorize:

- any specific hours/days/months/years,
- automatic closure completion merely because time elapsed,
- MailerSend revoke success for an unidentifiable token,
- final webhook signing-secret purge,
- product-data anonymization/hard delete,
- generated artifact purge,
- closure-package creation/download/expiry runtime,
- `not_required` export success,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Current recommendation

The next policy action should be a **narrow OL09-A / OL09-B acceptance discussion**, because closure reversibility and webhook drain are the earliest timing questions already blocking accepted lifecycle semantics.

No retention/grace runtime should be implemented until the relevant subsection is explicitly accepted.
