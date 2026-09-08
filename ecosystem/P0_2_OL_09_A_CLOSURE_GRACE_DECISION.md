# P0.2 OL-09A — Closure Grace / Reversibility Decision

**Status:** ACCEPTED — 30-DAY CLOSURE GRACE  
**Accepted:** 2026-09-08  
**Parent readiness:** `ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-08 tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`

## Decision

A successful Core organization suspension starts a **30-day reversible closure grace period** before any irreversible organization offboarding phase may become eligible.

The accepted rule is:

```text
Core organization -> SUSPENDED at T0
T0 .. T0+30 days  -> reversible grace; irreversible closure work prohibited
T0+30 days        -> grace satisfied; separately accepted irreversible phases may become eligible
```

Grace expiry is an eligibility condition only. It never, by itself, authorizes or executes product-data deletion/anonymization, generated-artifact deletion, final credential purge, closure-package expiry, cleanup-complete/tombstone-ready state or Core organization tombstone.

## Exact duration and time semantics

- Grace duration: **30 days**.
- Runtime comparison is based on an authoritative UTC suspension timestamp.
- Deadline semantics: `grace_deadline = suspended_at + 30 days`.
- Implementations must not round the deadline to a local midnight, browser timezone or operator timezone.
- Process downtime does not extend or reset the deadline; restart computes eligibility from the durable authoritative timestamp.

## Authoritative clock origin

The grace clock starts from the **successful Core transition into the current `SUSPENDED` episode**, not from:

- FAIR CRM closure-execution creation,
- the first time FAIR CRM observes `SUSPENDED`,
- an application worker start,
- a UI timestamp,
- an operator-entered date.

Current Core product lifecycle snapshot exposes canonical status and `work_allowed`, but does not currently expose the suspension-transition timestamp. Therefore an implementation must obtain a durable Core-authoritative suspension timestamp through an accepted public contract before it can compute destructive eligibility.

If the authoritative timestamp cannot be established, the system fails closed: the organization is **not** treated as having completed the 30-day grace period.

## Suspension episodes

Each successful new transition into `SUSPENDED` defines a new suspension episode and a new grace clock.

If an organization is reactivated and later suspended again:

```text
SUSPENDED at T0
-> ACTIVE before T0+30d
-> later SUSPENDED at T1
-> new grace deadline = T1+30d
```

A prior suspension episode or prior grace expiry must not be reused to accelerate a later closure attempt.

## Reactivation during grace

The existing accepted Core reactivation authority remains unchanged: `SUSPENDED -> ACTIVE` is a Platform SuperAdmin / SYSTEM lifecycle action.

During the 30-day grace period:

- reactivation is allowed under the existing OL-06 authority and state rules,
- reactivation cancels the current closure's eligibility to progress toward irreversible phases,
- FAIR CRM must durably terminalize/abort the corresponding open closure execution before stale closure workers can later continue it,
- previously terminalized suspension-cancelled product jobs/mail are not resurrected; existing OL-07 resumption rules remain authoritative,
- any later closure attempt after a new suspension uses the new suspension episode and a fresh 30-day clock.

This decision authorizes the future bounded closure-orchestration support needed to record grace state and safely abort an open closure execution on reactivation. It does not authorize any irreversible cleanup action.

## Grace expiry semantics

At or after the exact deadline, the system may record **grace satisfied / irreversible-phase eligible** only if all of the following remain true at the point of evaluation:

- Core still reports the same organization as `SUSPENDED`,
- the authoritative suspension episode/timestamp is the one used to compute the deadline,
- the closure execution belongs to the same organization and has not been aborted/invalidated,
- no separately required lifecycle obligation is blocked,
- the downstream phase itself has been separately accepted and implemented.

A timer expiry must never bypass a live Core lifecycle re-check or phase-specific authorization/evidence.

## Pre-existing suspended organizations / closure executions

No destructive deadline is retroactively fabricated for an existing suspended organization or closure execution when the authoritative suspension-transition timestamp is unavailable or unverified.

Such cases remain blocked until a deterministic Core-authoritative timestamp/evidence path exists. FAIR CRM closure creation time or first-observed suspension time must not be substituted silently.

## Authorized engineering boundary after acceptance

After this decision is canonical, bounded implementation may add only the machinery required to enforce the accepted grace policy, including:

- Core-owned/public authoritative `suspended_at` or equivalent suspension-episode timestamp/evidence,
- FAIR CRM durable grace-policy version + suspension timestamp + computed deadline evidence tied to one organization/closure execution,
- grace status/evaluation surfaces under existing SYSTEM closure authority,
- fail-closed handling when Core time evidence is missing/malformed/stale,
- safe reactivation/closure-abort semantics that prevent stale irreversible work,
- idempotent/restart-safe deadline evaluation,
- audit evidence without secrets,
- tenant-isolation and lifecycle-race tests.

This acceptance does **not** authorize a destructive worker or any product-data/artifact/credential/backup/tombstone mutation merely because 30 days elapsed.

## Explicitly still open

OL09-A does not decide:

- **OL09-B** webhook receive-only drain criterion or duration,
- OL09-C product-data class retention timing,
- OL09-D audit/security evidence retention,
- OL09-E closure-package/generated-artifact expiry,
- OL08-D product-data disposition actions,
- OL08-E generated-artifact disposition actions,
- OL08-F evidence-retention policy,
- OL08-G / OL-10 backup ageing and restore reconciliation,
- deterministic MailerSend token targeting,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Decision summary

**OL09-A is accepted: an organization remains in a reversible closure grace period for 30 days measured from the authoritative Core transition into the current `SUSPENDED` episode. Before that deadline, irreversible closure work is prohibited. After the deadline, time alone only makes separately accepted phases eligible; it does not execute or authorize them. Reactivation during grace invalidates the closure progression and a later suspension starts a fresh 30-day clock.**
