# P0.2 OL-09 — Retention / Grace Decision Readiness

**Status:** PARTIALLY ACCEPTED — OL09-A ACCEPTED; OL09-B through OL09-E OPEN  
**Prepared:** 2026-09-08  
**OL09-A accepted:** 2026-09-08 — 30-day closure grace  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-08 tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**OL09-A decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**Related accepted credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Track the OL-09 retention/grace policy choices that block later organization-closure phases.

OL09-A is now accepted narrowly. The remaining OL09-B through OL09-E choices are still open and must not be inferred from OL09-A.

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

## Why OL-09 remains open after OL09-A

OL09-A answers only the **organization-level reversible grace window**. It does not answer other retention/drain clocks.

Remaining policy still materially blocks or constrains:

- **OL08-C4 / OL09-B:** final zeroization of webhook signing secrets after receive-only drain,
- **OL08-D / OL09-C:** product-data anonymization/hard-delete timing,
- **OL08-F / OL09-D:** closure/audit/security evidence retention,
- **OL08-B + OL08-E / OL09-E:** future closure-package and generated-artifact expiry,
- final sequencing before `cleanup_complete` / `ready_for_tombstone` can ever be considered.

**OL08-G / backup ageing and restore reconciliation remain OL-10 scope.** OL09-A does not define backup behavior.

## Verified current lifecycle facts

### 1. Closure runtime remains bounded

Certified/implemented slices currently provide:

- OL08-01 durable closure execution,
- OL08-02 quiescence certification,
- OL08-03A export manifest/completeness planning,
- OL08-04A credential disposition state/evidence foundation.

No organization-wide product-data deletion, generated-artifact purge, closure-package delivery/expiry, cleanup-complete state or Core tombstone is currently authorized.

### 2. MailerSend token disposition has a separate non-time blocker

OL08-04A classifies current-model MailerSend API tokens as `supported_unidentifiable` because deterministic exact-token targeting is not yet available.

Waiting 30 days does not solve that blocker. OL09-A must never be interpreted as MailerSend revoke success.

### 3. Product-data disposition actions remain undecided

OL08-D remains open. The 30-day grace says **when an accepted irreversible phase may become eligible**, not which FAIR CRM data classes are anonymized, hard-deleted or retained.

### 4. Audit/security evidence retention remains separate

Closure events, export-plan evidence and credential-disposition evidence are append-only/non-secret control evidence. OL08-F / OL09-D still need their own retention decision; they are not automatically deleted after 30 days.

### 5. Backup/restore remains separate

System backup/restore is database-level administration. Backup ageing, retention guarantees and restore reconciliation remain OL-10 decisions.

## Remaining decision dimensions

### OL09-B — webhook receive-only drain criterion — OPEN

Decide how OL08-C4 leaves `receive_only_pending`.

Possible policy shapes:

- fixed maximum elapsed-time window,
- provider-specific deterministic terminal-event criterion,
- hybrid terminal evidence or maximum elapsed-time ceiling,
- accepted no-drain case when no signing secret exists.

Questions still open:

1. Is the criterion provider-specific or ecosystem-wide?
2. If time-based, what exact duration applies?
3. What timestamp starts the drain clock?
4. What happens to delayed webhooks after final secret purge?
5. What happens when provider state remains ambiguous at expiry?

OL09-A's 30-day organization grace does **not** automatically set OL09-B to 30 days.

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

## Explicitly still not accepted

This document does **not** accept or authorize:

- any OL09-B webhook drain duration/criterion,
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

**OL09-A is accepted. Next decision discussion: OL09-B — webhook receive-only drain criterion.**

Do not infer OL09-B's answer or duration from the 30-day OL09-A closure grace.
