# P0.2 OL-08 — Organization Offboarding Implementation Tracker

**Status:** IN PROGRESS — OL08-01 DONE; OL08-B technical export contract accepted; OL08-02 is the active resume point  
**Decision:** OL08-A ACCEPTED 2026-09-07; OL08-B technical contract PARTIALLY ACCEPTED 2026-09-07  
**Started:** 2026-09-07  
**Current resume point:** OL08-02 — closure quiescence certification  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**Readiness source:** `ecosystem/P0_2_OL_08_DECISION_READINESS.md`  
**OL08-B decision:** `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`

## Accepted OL08-A policy

Organization closure execution is a Platform SuperAdmin / SYSTEM-controlled, FAIR CRM-owned durable orchestration. Core remains canonical organization lifecycle authority. Closure execution may begin only after Core reports the organization as non-deleted and `SUSPENDED`; Core tombstone remains the final cross-repository lifecycle mutation.

Operational invariants:

- closure execution authority remains Platform SuperAdmin / SYSTEM only,
- Core remains authoritative for organization lifecycle state,
- closure progress is FAIR CRM-owned durable state rather than a new Core `OrganizationStatus`,
- at most one open closure execution may exist per organization,
- start/retry behavior is idempotent and restartable,
- failure/block state and audit evidence are explicit,
- Core tombstone remains prohibited until every required later phase is separately accepted, implemented and certified.

## OL08-01 — Non-destructive closure execution — DONE 2026-09-07

FAIR CRM PR #255 implements the accepted OL08-A / OL08-01 closure execution contract.

Delivered runtime:

- durable `organization_closure_executions` state,
- append-only closure event evidence,
- migration `0077_organization_closure_executions`,
- SYSTEM-authorized start/status/retry API,
- live Core lifecycle re-check on start/retry,
- canonical `SUSPENDED` precondition and fail-closed lifecycle-authority handling,
- unique organization + idempotency identity,
- database-enforced one-open-execution constraint,
- same-key duplicate convergence,
- explicit `blocked` evidence and same-execution retry,
- canonical tenant-isolation registry coverage,
- foreign organization denial before mutation,
- transactional local audit evidence,
- no `cleanup_complete`, `ready_for_tombstone`, DELETE or Core tombstone call.

State boundary:

```text
no execution
  -> in_progress              only if Core == SUSPENDED and SYSTEM-authorized
  -> blocked                  explicit recoverable evidence
  -> in_progress              idempotent retry of same execution
```

Exact implementation evidence:

- FAIR CRM PR #255 final head `aa34cd3e5d00ec6f7d6b7adaad4afa950319830e`,
- Development Standard Gate #707 / run `34155567277`: SUCCESS,
- Prod-Path E2E #270 / run `34155567315`: SUCCESS,
- FAIR CRM merge `e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`,
- Platform PR #36 exact head `ea77abf48ee606ace0756303075aec518eb2c4aa`,
- Platform Standards CI #104 / run `34156643910`: SUCCESS,
- Platform merge `f08f3a334c56c3c1be31694af56bf65330e44fe9`.

Therefore OL08-01A through OL08-01I are complete.

## OL08-B — Closure export technical contract — PARTIALLY ACCEPTED 2026-09-07

The accepted technical architecture is policy-conditioned export disposition:

```text
required
not_required
```

A missing/unknown disposition fails closed. `not_required` requires durable evidence from a separately accepted policy source.

**Current rule:** no accepted `not_required` policy source exists, therefore no runtime may use `not_required` to satisfy export obligation.

Accepted export-contract invariants:

- export evidence belongs to one organization + one closure execution,
- the manifest is versioned and explicitly classifies included/excluded/deferred data classes,
- first-version customer-portable structured categories are enumerated rather than inferred from a database dump,
- generated/binary artifacts remain deferred to OL08-E,
- reusable provider/security credentials are always excluded,
- Core identity remains outside FAIR CRM export ownership,
- initial control remains Platform SuperAdmin / SYSTEM/operator-only,
- no export evidence may open an irreversible closure gate until package lifecycle and remaining policy are separately accepted.

Canonical detailed decision: `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`.

### Accepted v1 structured completeness registry

The first export completeness planner must classify at minimum:

- customers and customer communications,
- contacts,
- fairs and participations,
- activities, todos and follow-up/task records,
- quotes plus portable quote-template/template-content source data,
- cost-catalog product data,
- import/data-integration metadata and structured results,
- scraper/enrichment run metadata and normalized customer-owned structured results,
- operation/automation definitions, run metadata and customer-portable structured results,
- mail templates plus normalized customer communication/mail-send history/status records.

Explicitly deferred/excluded in the first version:

- generated/binary files and uploads — OL08-E,
- scraper/operation artifact files — OL08-E,
- quote/logo binary assets — OL08-E,
- provider/SMTP reusable secrets — always excluded,
- provider-side revoke/disposition behavior — OL08-C,
- Core credential/session/token data — outside FAIR CRM ownership,
- system database backups/restores — OL-10,
- derived dashboard views,
- raw provider webhook/signature/security payloads unless separately accepted later.

## OL08-02 — Closure quiescence certification — AUTHORIZED / NEXT

Before export planning is trusted, certify that the existing OL-07 runtime is sufficient for an OL08 closure execution that has started from canonical Core `SUSPENDED`.

Required evidence:

- covered queued/pending organization work cannot start,
- covered running work stops at the already-certified safe checkpoints,
- new outbound provider handoff is blocked,
- ambiguous already-started provider handoff remains terminal/non-auto-retry,
- suspension-cancelled work is not resurrected,
- lifecycle-authority outage fails closed,
- closure execution itself does not bypass these guards,
- no new generic cancellation framework is introduced if existing OL-07 behavior already satisfies the requirement.

OL08-02 may be certification-only if no runtime gap is found.

## OL08-03A — Export manifest / completeness planner — AUTHORIZED AFTER OL08-02

After OL08-02 is green, OL08-B authorizes only a non-destructive planner slice.

Authorized:

- durable export-plan identity tied to one organization + closure execution,
- versioned manifest schema,
- structured-data completeness registry,
- organization-scoped record planning/counting,
- deterministic canonical fingerprints/digests where safe without retaining package payload,
- explicit included/excluded/deferred reason evidence,
- hard secret-exclusion validation,
- SYSTEM-only plan/status/retry,
- idempotency and tenant-isolation tests,
- non-secret audit/closure evidence.

Still blocked:

- persistent/downloadable closure package materialization,
- customer-facing handover/download,
- package retention/expiry,
- `not_required` successful disposition,
- `integrity_verified` as an irreversible-phase gate,
- provider revoke/secret purge,
- organization-wide data/artifact delete/anonymize,
- `cleanup_complete` / `ready_for_tombstone`,
- Core tombstone.

## Still-gated OL-08 decisions

| Decision | Status | Runtime boundary |
| --- | --- | --- |
| OL08-B — closure export technical contract | **PARTIALLY ACCEPTED** | Planner authorized after OL08-02; package lifecycle and `not_required` policy remain gated. |
| OL08-C — provider credential disposition | **OPEN** | No provider revoke or local secret purge authorized. |
| OL08-D — product-data disposition matrix | **OPEN / depends on OL-09** | No organization-wide anonymize/hard-delete authorized. |
| OL08-E — generated artifact disposition | **OPEN** | No closure-driven artifact purge or persistent closure-package lifecycle authorized. |
| OL08-F — audit/security evidence retention | **OPEN / policy required** | No retention duration chosen. |
| OL08-G — backup/restore interaction | **OPEN / depends on OL-10** | No backup ageing or restore reconciliation semantics authorized. |
| OL-09 — retention/grace durations | **OPEN CHOICE** | No duration or grace window may be invented. |
| OL-10 — backup restore implications | **OPEN CHOICE** | Destructive closure cannot be certified until restore behavior is explicit. |

## Hard prohibitions

Until separately accepted, OL-08 work must not:

- claim a closure-complete delivered export package,
- permit `not_required` without an accepted policy source,
- revoke provider credentials,
- purge SMTP/provider secrets,
- anonymize or hard-delete organization product data,
- delete closure-driven generated files/artifacts,
- choose retention/grace durations,
- define backup ageing/restore reconciliation,
- add `cleanup_complete` / `ready_for_tombstone`,
- invoke Core organization delete/tombstone.

## Current resume point

Execute **OL08-02 closure quiescence certification** in FAIR CRM against the existing OL-07 lifecycle runtime.

If OL08-02 proves the existing guards sufficient, no application behavior change is required. After OL08-02 certification, proceed to the bounded **OL08-03A export manifest/completeness planner**. All package-lifecycle and destructive phases remain gated.
