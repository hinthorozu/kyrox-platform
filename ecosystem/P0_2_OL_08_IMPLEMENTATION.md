# P0.2 OL-08 — Organization Offboarding Implementation Tracker

**Status:** IN PROGRESS — OL08-01 DONE; OL08-B decision gate OPEN  
**Decision:** OL08-A ACCEPTED 2026-09-07  
**Started:** 2026-09-07  
**Current resume point:** OL08-B — closure export obligation/contract decision  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**Readiness source:** `ecosystem/P0_2_OL_08_DECISION_READINESS.md`  
**OL08-B proposal:** `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`

## Accepted OL08-A policy

> **Organization closure execution is a Platform SuperAdmin / SYSTEM-controlled, FAIR CRM-owned durable orchestration. Core remains canonical organization lifecycle authority. Closure execution may begin only after Core reports the target organization as `SUSPENDED`; the Core organization tombstone is never the start signal and remains the final cross-repository lifecycle mutation.**

Operationally:

- closure execution authority remains Platform SuperAdmin / SYSTEM only,
- Core remains authoritative for organization lifecycle state,
- a closure execution can start only while Core reports the organization as non-deleted and `SUSPENDED`,
- closure progress is FAIR CRM-owned durable state rather than a new Core `OrganizationStatus`,
- at most one open closure execution may exist per organization,
- start/retry behavior is idempotent and restartable,
- failure/block state and audit evidence are explicit,
- Core tombstone remains prohibited until every required later phase is separately accepted, implemented and certified,
- OL08-B through OL08-G, OL-09 and OL-10 are not implicitly accepted by OL08-A/OL08-01.

## OL08-01 — Non-destructive closure execution — DONE 2026-09-07

FAIR CRM PR #255 implements the accepted OL08-A / OL08-01 non-destructive closure execution contract.

### Runtime delivered

- FAIR CRM-owned durable `organization_closure_executions` state,
- append-only closure event evidence,
- migration `0077_organization_closure_executions`,
- SYSTEM-authorized start/status/retry API,
- reuse of Core `identity.organizations.delete` SYSTEM authority without adding an assignable product destructive permission,
- live Core lifecycle re-check on start/retry,
- `SUSPENDED` precondition with fail-closed lifecycle-authority behavior,
- unique organization + idempotency identity,
- database-enforced one-open-execution constraint,
- same-key duplicate convergence,
- explicit `blocked` evidence and same-execution retry,
- canonical tenant-isolation registry coverage,
- foreign organization denial before mutation,
- transactional local audit evidence; Core audit remains supplementary/best-effort,
- no `cleanup_complete`, `ready_for_tombstone`, DELETE or Core tombstone call.

### State-machine boundary

```text
no execution
  -> in_progress              only if Core == SUSPENDED and SYSTEM-authorized
  -> blocked                  explicit recoverable evidence
  -> in_progress              idempotent retry of same execution
```

OL08-01 deliberately has no terminal cleanup-complete/tombstone-ready state.

### Exact implementation evidence

FAIR CRM PR #255 final head:

`aa34cd3e5d00ec6f7d6b7adaad4afa950319830e`

Exact-head CI:

- Development Standard Gate #707 / run `34155567277`: **SUCCESS**
  - Feature Contract / Applicability: success
  - Frontend Tests / Build / UI Governance: success through backend-only N/A path
  - Backend Quality Check: success
- Prod-Path E2E #270 / run `34155567315`: **SUCCESS**
  - database prepare + Alembic migration: success
  - KYROX Core startup: success
  - FAIR CRM startup: success
  - production-shaped lifecycle regressions: success

FAIR CRM merge commit:

`e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`

### Cross-repository certification

Platform PR #36 (`docs(p0.2): certify OL08-01 closure execution runtime`) synchronized the implementation evidence into Platform after Platform Standards CI #104 / run `34156643910` passed exact head `ea77abf48ee606ace0756303075aec518eb2c4aa`.

Platform PR #36 was squash-merged as:

`f08f3a334c56c3c1be31694af56bf65330e44fe9`

Therefore **OL08-01A through OL08-01I are complete**.

## Current baseline after OL08-01

The closure system now has a durable, auditable, restartable non-destructive execution shell. It still does **not** have authority to perform export or destructive cleanup.

Existing prerequisites remain:

- OL-07 quiescence blocks/cancels covered work while Core is non-active,
- Core organization delete is only a Core soft tombstone (`deleted_at`),
- Core delete has no product-offboarding-complete prerequisite,
- FAIR CRM lifecycle consumption remains read-only/fail-closed,
- existing feature-level exports/downloads are tenant-safe but are not a complete closure export,
- database backup/restore is database-level rather than organization-only,
- email/provider account soft-delete is not provider credential revocation or local secret purge.

## OL08-B — Closure export obligation/contract — OPEN

OL08-B must decide whether closure export is:

- always required,
- explicitly requested,
- policy-conditioned,
- or not applicable for specific classes/scenarios.

It must also define the closure export contract sufficiently to distinguish a complete closure snapshot from existing feature exports.

The current decision proposal is:

`ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`

That proposal currently recommends a **policy-conditioned `required` / `not_required` disposition** with durable reason evidence, organization/execution ownership, a versioned completeness manifest, integrity digests and explicit secret exclusion. This is a proposal only; it does not authorize runtime.

### Runtime remains blocked until OL08-B acceptance

Do not implement OL08-03 or claim closure export complete until OL08-B is explicitly accepted in ADR-0006 / this tracker.

Existing customer Excel, scraper artifact and quote/template asset paths must not be silently composed and treated as a closure-complete package.

## Still-gated OL-08 decisions

| Decision | Status | Runtime boundary |
| --- | --- | --- |
| OL08-B — closure export obligation/contract | **OPEN / proposal prepared** | No closure-complete export runtime authorized. |
| OL08-C — provider credential disposition | **OPEN** | No provider revoke or local secret purge authorized. |
| OL08-D — product-data disposition matrix | **OPEN / depends on OL-09** | No organization-wide anonymize/hard-delete authorized. |
| OL08-E — generated artifact disposition | **OPEN** | No closure-driven artifact purge authorized. |
| OL08-F — audit/security evidence retention | **OPEN / policy required** | No retention duration chosen. |
| OL08-G — backup/restore interaction | **OPEN / depends on OL-10** | No backup ageing or restore reconciliation semantics authorized. |
| OL-09 — retention/grace durations | **OPEN CHOICE** | No duration or grace window may be invented. |
| OL-10 — backup restore implications | **OPEN CHOICE** | Destructive closure cannot be certified until restore behavior is explicit. |

## Scope boundary / hard prohibitions

Until separately accepted, OL-08 work must not:

- create or claim a closure-complete export,
- revoke provider credentials,
- purge SMTP/provider secrets,
- anonymize or hard-delete organization product data,
- delete closure-driven generated files/artifacts,
- choose retention/grace durations,
- define backup ageing/restore reconciliation,
- add `cleanup_complete` / `ready_for_tombstone`,
- invoke Core organization delete/tombstone.

## Current resume point

Resolve **OL08-B — closure export obligation/contract**.

The immediate work is decision review/acceptance, not runtime. If OL08-B is accepted, the next authorized implementation slice may be **OL08-03 closure export contract/runtime** within the accepted scope. OL08-C+ and all destructive phases remain separately gated.
