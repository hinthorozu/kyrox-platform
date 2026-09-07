# P0.2 OL-08 — Organization Offboarding Implementation Tracker

**Status:** IN PROGRESS — OL08-01 runtime implemented/merged; cross-repository certification pending  
**Decision:** OL08-A ACCEPTED 2026-09-07  
**Started:** 2026-09-07  
**Current resume point:** OL08-01I — cross-repository certification / docs sync  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**Readiness source:** `ecosystem/P0_2_OL_08_DECISION_READINESS.md`

## Accepted OL08-A policy

> **Organization closure execution is a Platform SuperAdmin / SYSTEM-controlled, FAIR CRM-owned durable orchestration. Core remains canonical organization lifecycle authority. Closure execution may begin only after Core reports the target organization as `SUSPENDED`; the Core organization tombstone is never the start signal and remains the final cross-repository lifecycle mutation. OL08-01 is non-destructive: it may create, read and retry durable closure execution state and audit evidence, but it may not export closure data, revoke or purge credentials, anonymize/delete product data or artifacts, choose retention/grace periods, define backup restore behavior, or invoke the Core tombstone.**

Operationally:

- closure execution authority remains Platform SuperAdmin / SYSTEM only; no organization role gains destructive lifecycle authority,
- Core remains authoritative for organization lifecycle state and FAIR CRM must fail closed when that authority cannot be established,
- a closure execution can start only while the Core organization is non-deleted and `SUSPENDED`, reusing the OL-07 quiesced/no-new-work state rather than inventing a new Core lifecycle status,
- closure progress is product-owned durable state in FAIR CRM; it is not encoded into Core `OrganizationStatus` and does not mutate Core lifecycle state,
- one target organization may have at most one open closure execution at a time,
- a stable execution identifier plus idempotency semantics must make repeated start/retry requests converge on the same logical execution rather than duplicate side effects,
- execution state must expose an explicit failure/block condition and enough phase/timestamp evidence to restart safely,
- every successful lifecycle-orchestration mutation must be auditable with actor, target organization, execution id, phase/state and timestamp without storing secrets,
- Core tombstone is prohibited until all later required product phases are separately accepted, implemented and certified complete,
- OL08-01 itself must not provide a transition that can falsely certify destructive cleanup complete or make the execution tombstone-ready,
- OL08-B through OL08-G remain open; OL-09 retention/grace and OL-10 backup/restore policy remain open choices.

## Why the product owns closure execution state

Core and FAIR CRM use separate persistence. Core's current `DELETE /organizations/{organization_id}` only sets `organizations.deleted_at` and does not perform product cleanup. FAIR CRM consumes Core lifecycle through a read-only lifecycle snapshot and does not persist or own Core lifecycle status.

Putting closure progress into Core `OrganizationStatus` would mix product-specific offboarding phases into the reusable lifecycle authority. Using the Core tombstone as the start signal would also destroy the canonical organization lookup before product cleanup has proven complete. The accepted split therefore is:

```text
Core: canonical account lifecycle authority
  ACTIVE -> SUSPENDED

FAIR CRM: durable product offboarding execution
  start/retry/status/phase evidence
  ...later separately accepted product phases...

Core: final tombstone only after certified product completion
  deleted_at = timestamp
```

## OL08-01 implementation checklist

- [x] **OL08-01A — Decision/scope acceptance**
  - OL08-A accepted as the narrow non-destructive closure-orchestration slice.
  - OL08-B through OL08-G, OL-09 and OL-10 remain unresolved and are not implicitly accepted.

- [x] **OL08-01B — Durable FAIR CRM execution model**
  - FAIR CRM PR #255 adds durable organization-scoped closure execution and append-only closure event records.
  - Migration `0077_organization_closure_executions` persists execution id, organization id, idempotency key, state/phase, actor references, failure evidence and timestamps.
  - Database constraints enforce one open execution per organization and unique organization + idempotency identity.

- [x] **OL08-01C — SYSTEM-authorized start/status/retry contract**
  - Public product contract is limited to start, status and retry under `/api/v1/system-admin/organizations/{organization_id}/closure-executions`.
  - It reuses Core `identity.organizations.delete` SYSTEM authority; no assignable FAIR CRM destructive permission was introduced.
  - Cross-organization context mismatch and ordinary/non-SYSTEM authority fail closed before mutation.

- [x] **OL08-01D — Core lifecycle precondition**
  - Start and retry perform a live Core lifecycle snapshot check.
  - The target must be canonical Core `SUSPENDED`; any other lifecycle state is rejected.
  - Lifecycle authority outage/invalid response fails closed; no local cached lifecycle value becomes authority.

- [x] **OL08-01E — Idempotency / failure / restart semantics**
  - Duplicate start with the same idempotency identity converges on the same execution.
  - A conflicting second open closure execution is rejected, including through the database race constraint.
  - Blocked state retains explicit failure code/message evidence.
  - Retry resumes the same logical execution and increments attempt evidence rather than creating a replacement execution.

- [x] **OL08-01F — Audit evidence**
  - FAIR CRM stores transactional append-only local closure event evidence for start/block/retry state changes.
  - Evidence includes actor, organization, execution, transition/phase and timestamp without raw credentials/tokens.
  - Core audit remains supplementary/best-effort and cannot erase the local transactional evidence requirement.

- [x] **OL08-01G — Tombstone safety contract**
  - OL08-01 contains no Core organization delete/tombstone call.
  - Public API exposes no complete/delete/tombstone transition.
  - Current state machine contains no `cleanup_complete` or `ready_for_tombstone` semantic state.

- [x] **OL08-01H — Adversarial / tenant-isolation certification**
  - ordinary/organization-role authority is denied,
  - foreign organization path context is denied before mutation,
  - lifecycle authority outage and non-`SUSPENDED` state fail closed,
  - duplicate-start races cannot create two open executions,
  - retry remains on the same execution and re-checks live lifecycle authority,
  - `organization_closure` is registered in the canonical FAIR CRM tenant-isolation evidence registry.

- [ ] **OL08-01I — Cross-repository certification / docs sync**
  - FAIR CRM PR #255 final head `aa34cd3e5d00ec6f7d6b7adaad4afa950319830e` passed Development Standard Gate #707 / run `34155567277`.
  - The same head passed Prod-Path E2E #270 / run `34155567315`, including DB prepare/migration and real Core + FAIR CRM startup.
  - PR #255 merged to FAIR CRM `main` as `e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`.
  - Platform tracker/status synchronization is in progress on the dedicated certification PR.
  - OL08-01I becomes complete only after that Platform certification PR merges.

## FAIR CRM implementation evidence

FAIR CRM PR #255 (`feat(ol08): add non-destructive closure execution state machine`) is the OL08-01 runtime implementation.

Certified exact head:

`aa34cd3e5d00ec6f7d6b7adaad4afa950319830e`

Merge commit:

`e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`

Exact-head CI:

- Development Standard Gate #707 / run `34155567277`: **SUCCESS**
  - Feature Contract / Applicability: success
  - Frontend Tests / Build / UI Governance: success through the backend-only N/A path
  - Backend Quality Check: success
- Prod-Path E2E #270 / run `34155567315`: **SUCCESS**
  - DB prepare and Alembic migration: success
  - KYROX Core startup: success
  - FAIR CRM startup: success
  - production-shaped gate and existing lifecycle regressions: success

The first full-suite run exposed one governance omission rather than a runtime defect: the new `organization_closure` module had not yet been registered in FAIR CRM's canonical tenant-isolation evidence registry. The final head fixes that omission and the full backend suite then passed.

## OL08-01 state-machine constraints

The implemented OL08-01 runtime uses the accepted semantics:

```text
no execution
  -> in_progress              only if Core == SUSPENDED and SYSTEM-authorized
  -> blocked                  explicit recoverable evidence
  -> in_progress              idempotent retry of the same execution
```

OL08-01 intentionally has **no terminal `cleanup_complete` or `ready_for_tombstone` transition**. Those meanings depend on later policy/implementation phases that are still blocked.

## Still-blocked OL-08 decisions

| Decision | Status | Runtime boundary |
| --- | --- | --- |
| OL08-B — closure export obligation/contract | **OPEN** | No closure-complete export implementation yet. |
| OL08-C — provider credential disposition | **OPEN** | No provider revoke or local secret purge authorized. |
| OL08-D — product-data disposition matrix | **OPEN / depends on OL-09** | No organization-wide anonymize/hard-delete authorized. |
| OL08-E — generated artifact disposition | **OPEN** | No closure-driven artifact purge authorized. |
| OL08-F — audit/security evidence retention | **OPEN / policy required** | OL08-01 creates audit evidence but does not choose retention duration. |
| OL08-G — backup/restore interaction | **OPEN / depends on OL-10** | No backup ageing or restore reconciliation semantics authorized. |
| OL-09 — retention/grace durations | **OPEN CHOICE** | No duration or grace window may be invented. |
| OL-10 — backup restore implications | **OPEN CHOICE** | Destructive closure cannot be certified until restore behavior is explicit. |

## Certified/current baseline carried into OL08-01

- OL-07 provides deterministic quiescence while Core is non-active: covered queued work is cancelled before start, covered running work stops at safe checkpoints, and new provider handoff is blocked.
- Core organization delete is a soft tombstone (`deleted_at`), not FAIR CRM product-data deletion.
- The current Core delete endpoint has no product-offboarding-complete prerequisite; OL-08 therefore must not use it until the later final tombstone gate is implemented.
- Core lifecycle snapshot exposes current canonical lifecycle state and allows product work only for `ACTIVE` organizations.
- FAIR CRM lifecycle consumption is read-only/fail-closed and deliberately does not persist Core lifecycle authority.
- OL08-01 now supplies the missing FAIR CRM-owned durable non-destructive closure execution state, but it deliberately does not advance into destructive/export phases.

## Scope boundary / non-goals

OL08-01 does **not** authorize or implement:

- closure-complete customer export,
- provider-side credential revocation,
- local SMTP/provider secret destruction,
- customer/contact/business data anonymization or hard delete,
- generated file/artifact deletion,
- retention/grace periods,
- backup ageing or restore reconciliation,
- Core tombstone invocation,
- a new Core lifecycle status,
- reactivation semantics beyond the already-certified OL-07 contract.

## Current resume point

Complete **OL08-01I cross-repository certification/docs sync**. After that, the next lifecycle decision gate is **OL08-B — closure export obligation/contract**. OL08-B remains **OPEN** until separately accepted; do not implement export or any destructive phase merely because OL08-01 is complete.