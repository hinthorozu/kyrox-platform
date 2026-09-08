# P0.2 OL-09 — Retention / Grace Decision Readiness

**Status:** PARTIALLY ACCEPTED — OL09-A ACCEPTED; OL09-B1 ACCEPTED; OL09-B2 + OL09-C through OL09-E OPEN  
**Prepared:** 2026-09-08  
**OL09-A accepted:** 2026-09-08 — 30-day closure grace  
**OL09-B1 accepted:** 2026-09-08 — suspended webhook service boundary / minimum protective processing  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-08 tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**OL09-A decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**OL09-B decision:** `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`  
**Related accepted credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Track the OL-09 retention/grace policy choices that block later organization-closure phases.

OL09-A and the OL09-B1 suspended-service boundary are now accepted narrowly. OL09-B2 final receive-only expiry and OL09-C through OL09-E remain open and must not be inferred from those accepted slices.

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

## Accepted OL09-B1 — suspended webhook service boundary

The accepted behavior is:

- the authoritative Core transition into `SUSPENDED` ends normal tenant-facing mail webhook service immediately,
- the 30-day OL09-A grace is **not** 30 additional days of mail analytics/service,
- during receive-only drain, only the minimum protective MailerSend event set may continue:
  - `activity.unsubscribed`,
  - `activity.spam_complaint`,
  - `activity.hard_bounced`,
- normal delivery/engagement events (`sent`, `delivered`, `soft_bounced`, `deferred`, `opened`, `opened_unique`, `clicked`, `clicked_unique`) are acknowledged and dropped on an early low-cost path,
- dropped events do not perform provider-status/analytics work, create CRM activities, enqueue jobs or create a replay backlog,
- suspended-period analytics are not backfilled after reactivation,
- there is no tenant-wide scan, per-message scheduler or per-tenant polling loop.

Canonical detailed decision: `ecosystem/P0_2_OL_09_B_WEBHOOK_SERVICE_BOUNDARY_DECISION.md`.

### Runtime signal remains an implementation gate

OL08-04A `receive_only_pending` is created when credential disposition starts; it is not itself the exact Core suspension-transition signal. The existing Core lifecycle guard is intentionally live/uncached and a network call per webhook would violate the accepted low-load goal.

Therefore OL09-B1 accepts the service behavior but does not yet authorize a speculative synchronization mechanism. Before a runtime slice is authorized, the implementation must define a deterministic, fail-closed and low-cost way for webhook ingress to honor authoritative Core `SUSPENDED` without creating unbounded per-webhook Core traffic or fabricating local lifecycle authority.

## Why OL-09 remains open

OL09-A answers the **organization-level reversible grace window**. OL09-B1 answers **what webhook work may continue while suspended**. Neither decides the final receive-only secret expiry or the remaining retention clocks.

Remaining policy still materially blocks or constrains:

- **OL08-C4 / OL09-B2:** final zeroization of webhook signing secrets after receive-only drain,
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

### 2. Current MailerSend webhook path has a meaningful cost boundary

Current MailerSend ingress is synchronous and DB-backed. For supported activity events, normal handling can resolve the email account, provider config/signing secret, mail-send operation and provider-status transition. `unsubscribed` / `spam_complaint` can additionally mutate communication consent and create an activity.

OL09-B1 therefore intentionally prevents normal delivery/engagement events from reaching those tenant-service side effects while suspended.

### 3. MailerSend token disposition has a separate non-time blocker

OL08-04A classifies current-model MailerSend API tokens as `supported_unidentifiable` because deterministic exact-token targeting is not yet available.

Waiting 30 days or completing webhook drain does not solve that blocker. OL09 must never be interpreted as MailerSend revoke success.

### 4. Product-data disposition actions remain undecided

OL08-D remains open. The 30-day grace says **when an accepted irreversible phase may become eligible**, not which FAIR CRM data classes are anonymized, hard-deleted or retained.

### 5. Audit/security evidence retention remains separate

Closure events, export-plan evidence and credential-disposition evidence are append-only/non-secret control evidence. OL08-F / OL09-D still need their own retention decision; they are not automatically deleted after 30 days.

### 6. Backup/restore remains separate

System backup/restore is database-level administration. Backup ageing, retention guarantees and restore reconciliation remain OL-10 decisions.

## Remaining decision dimensions

### OL09-B2 — final webhook receive-only drain expiry — OPEN

The allowed suspended-event set is now decided by OL09-B1. What remains is the criterion for leaving `receive_only_pending` and finally zeroizing the webhook signing secret.

Still-open policy shapes:

- fixed maximum elapsed-time window,
- provider-specific deterministic terminal-event criterion,
- hybrid terminal evidence or maximum elapsed-time ceiling,
- accepted no-drain case when no signing secret exists.

Questions still open:

1. If time-based, what exact duration applies?
2. What authoritative timestamp starts that drain clock?
3. What happens to delayed protective webhooks after final secret purge?
4. What happens when provider state remains ambiguous at expiry?
5. Is one ecosystem-wide rule sufficient or must some providers have bounded provider-specific rules?

OL09-A's 30-day organization grace does **not** automatically set OL09-B2 to 30 days.

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

## OL09-B1 acceptance checklist — CLOSED

- [x] Normal tenant mail webhook service ends at authoritative Core `SUSPENDED`.
- [x] Protective suspended set: unsubscribe, spam complaint, hard bounce only.
- [x] Sent/delivery/soft-bounce/deferred/open/click processing is dropped while suspended.
- [x] Dropped events create no analytics/status/activity/job/replay workload.
- [x] No historical-message scan or per-tenant/per-message polling.
- [x] No backfill of suspended-period analytics after reactivation.
- [x] Final signing-secret expiry/duration remains explicitly open.
- [x] Cheap authoritative lifecycle signal mechanism remains an implementation gate; no local lifecycle fabrication is accepted.

## Explicitly still not accepted

This document does **not** accept or authorize:

- any OL09-B2 webhook signing-secret drain duration/expiry criterion,
- a speculative local/cached lifecycle authority mechanism,
- final webhook signing-secret purge,
- MailerSend revoke success for an unidentifiable token,
- product-data anonymization/hard delete,
- generated-artifact purge,
- closure-package creation/download/expiry runtime,
- `not_required` export success,
- audit/security evidence retention duration,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Current resume point

**OL09-A is accepted. OL09-B1 suspended webhook service behavior is accepted. Next decision discussion: OL09-B2 — final receive-only signing-secret expiry/clock and the bounded low-cost lifecycle signal needed to enforce B1 safely.**

Do not infer OL09-B2's answer or duration from the 30-day OL09-A closure grace.
