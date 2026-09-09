# P0.2 OL-09E — Closure Package / Generated Artifact Expiry Decision

**Status:** ACCEPTED — BOUNDED ARTIFACT TIMING POLICY  
**Accepted:** 2026-09-09  
**Parent readiness:** `ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`  
**Related export contract:** `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`  
**Related offboarding readiness:** `ecosystem/P0_2_OL_08_DECISION_READINESS.md`  
**Related grace decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`

## Purpose

Define the timing policy for FAIR CRM generated/product artifacts and for any future persistent closure package without silently authorizing artifact deletion, package materialization, customer-facing download, or Core tombstone.

OL09-E decides **when an artifact class may expire**. OL08-B / OL08-E remain responsible for **what artifact exists, who owns it, whether it must be exported, and what destructive action is permitted**.

## Verified boundary

The existing OL08-B contract deliberately does not authorize a persistent/downloadable closure package. It only authorizes the manifest/completeness planning layer and explicitly defers generated/binary artifacts to OL08-E.

The offboarding readiness scope identifies product-file classes including:

- uploads,
- generated exports,
- scraper/enrichment artifacts,
- quote/logo assets,
- operation/automation result artifacts,
- other generated product files.

These are distinct from relational product-data rows, credentials/secrets, audit/security evidence and database backups.

## Decision

OL09-E accepts **two separate timing rules**.

### A. Existing product/generated artifact classes

For an artifact class that OL08-E later explicitly classifies for irreversible deletion/expiry, there is **no additional generic retention interval after the OL09-A 30-day closure grace**.

```text
Core organization -> SUSPENDED
SUSPENDED through 30 days -> irreversible artifact deletion prohibited
30-day grace satisfied    -> OL08-E delete/expire classes become time-eligible
```

This is timing eligibility only.

An artifact must not be deleted merely because the 30-day grace elapsed. Before mutation, the implementation must still prove that:

- OL08-E explicitly authorizes the disposition for that artifact class,
- the closure execution is still valid for the same organization/suspension episode,
- any required closure-export/package completeness obligation no longer depends on the artifact,
- any required package materialization/integrity step that needs the artifact has completed,
- no separately accepted class-specific retention exception applies,
- phase-specific sequencing and authorization gates are satisfied.

There is no generic `+30`, `+60`, `+90` or other post-grace delay for these product artifact classes.

### B. Future persistent closure package

If a future OL08-B / OL08-E decision authorizes materializing a persistent closure package, that package receives a **30-day availability/retention window**.

The package clock starts from the first durable UTC timestamp at which the canonical package for that closure execution reaches the separately accepted **available/ready-for-authorized-retrieval** state.

Canonical policy:

```text
closure package becomes durably available at P0
P0 .. P0 + 30 days -> package may remain available to authorized retrieval paths
P0 + 30 days       -> package expires and becomes purge-eligible
```

The clock does **not** start from:

- Core `SUSPENDED`,
- the OL09-A 30-day grace deadline,
- closure-execution creation,
- export planning,
- package generation start,
- first download,
- last download,
- an operator-entered date.

This prevents a package from consuming its retrieval window before it actually exists while still placing a deterministic upper bound on persistent sensitive package storage.

## Package clock semantics

The package availability timestamp must be:

- durable,
- UTC,
- bound to one organization + closure execution + canonical package identity/version,
- created only by the accepted package lifecycle implementation,
- immutable for that canonical package version.

Normal download/access does not extend or reset the 30-day deadline.

Process downtime does not extend or reset the deadline.

A retry that reproduces the same canonical package does not silently create a new 30-day period.

If an accepted package lifecycle later permits replacement of an invalid/corrupt canonical package with a new canonical version, that replacement must carry explicit supersession/integrity evidence. Any new availability clock must be tied to that separately accepted replacement semantics rather than inferred from storage rewrite time.

## Expiry behavior

At or after the exact package expiry deadline:

- the expired package must no longer be presented as an authorized downloadable/available closure artifact,
- package bytes become eligible for deterministic purge through the separately implemented OL08-E/package lifecycle,
- expiry alone must not be recorded as successful physical deletion when storage cleanup has not completed,
- purge retry must be idempotent and restart-safe,
- an expired package must not be silently regenerated or resurrected merely because a later access request arrives,
- minimal non-secret package lifecycle evidence may remain only under the separately accepted OL09-D audit/security retention policy.

The package itself is not OL09-D audit evidence and is not retained for 12 months under OL09-D.

## Relationship to existing product artifacts

The future closure package and pre-existing product/generated artifacts are not the same retention class.

A source artifact may become time-eligible after the 30-day closure grace, while the closure package created from accepted export inputs may have its own later 30-day package-availability window.

Therefore implementations must not infer:

```text
package available for 30 days
=> all original source artifacts must also remain for 30 additional days
```

Original artifacts remain only as long as their separately accepted OL08-E disposition and unresolved export/package dependencies require them.

Conversely, source artifacts must not be destroyed before an accepted required package/export process has captured and verified everything it is obligated to preserve.

## Reactivation semantics

Before the OL09-A 30-day grace is satisfied, reactivation invalidates irreversible artifact-cleanup eligibility from that suspension episode under OL09-A.

OL09-E does not authorize destruction during the reversible grace.

If a package has not been authorized/materialized, reactivation does not create an artifact or an expiry clock.

Any future behavior for an already-materialized closure package when closure is cancelled/reactivated must be explicitly handled by the package lifecycle contract. OL09-E does not invent a customer-facing package after reactivation.

## Unmaterialized and deferred artifacts

- No package object means no package expiry clock exists.
- A manifest/export plan is not a package and must not receive a fabricated package availability timestamp.
- Deferred artifact classes remain blocked until OL08-E assigns their disposition.
- Missing or unverified time evidence fails closed; runtime must not fabricate an expiry deadline from first observation or operator input.

## Relationship to closure completion

OL09-E does not itself decide whether package expiry is a prerequisite for terminal closure or Core tombstone.

That sequencing belongs to the complete OL08-B / OL08-E / OL08-07 closure contract.

This decision only guarantees that if a persistent closure package is accepted, its storage lifetime is bounded to 30 days from durable availability, and if existing product artifact classes are accepted for deletion/expiry, they do not receive an additional generic post-grace retention period.

## Explicitly outside OL09-E

This decision does not authorize or decide:

- creation/materialization of a closure package,
- package format or package contents,
- customer-facing download/handover,
- `not_required` export success,
- OL08-E artifact-class disposition actions,
- OL08-D relational product-data actions,
- audit/security evidence retention beyond OL09-D,
- credentials/secrets retention,
- database backup ageing or restore reconciliation,
- cleanup-complete / ready-for-tombstone,
- Core organization tombstone.

## Acceptance checklist

- [x] Existing OL08-E delete/expire artifact classes receive no generic post-grace retention extension.
- [x] Existing artifact deletion remains prohibited during OL09-A's 30-day reversible grace.
- [x] Required export/package dependencies must be satisfied before source-artifact destruction.
- [x] Future persistent closure package retention is 30 days.
- [x] Package clock starts from durable canonical package availability/readiness, not suspension/grace/generation/download time.
- [x] Package access/download does not reset the clock.
- [x] Package expiry removes authorization to present the package and makes bytes purge-eligible; physical purge remains separately implemented.
- [x] No package materialization means no package expiry clock.
- [x] Expired package is not silently regenerated/resurrected.
- [x] Minimal non-secret package lifecycle evidence remains governed by OL09-D, not by package retention.
- [x] Backups remain OL-10.

## Decision summary

**OL09-E is accepted. Product/generated artifact classes that OL08-E later approves for delete/expiry become time-eligible immediately after the valid OL09-A 30-day closure grace, with no additional generic retention period, subject to unresolved export/package dependencies and all phase-specific gates. A future persistent closure package, if separately authorized and materialized, may remain available for 30 days measured from its durable canonical available/ready timestamp; downloads do not reset that clock. At expiry the package becomes unavailable and purge-eligible, while physical purge/runtime, package materialization/delivery and artifact-class disposition remain separately gated.**
