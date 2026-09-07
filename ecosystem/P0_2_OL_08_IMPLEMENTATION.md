# P0.2 OL-08 — Organization Offboarding Implementation Tracker

**Status:** IN PROGRESS — OL08-A accepted; OL08-01 authorized as non-destructive closure orchestration only  
**Decision:** OL08-A ACCEPTED 2026-09-07  
**Started:** 2026-09-07  
**Current resume point:** OL08-01 — closure execution contract/state machine  
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

Core and FAIR CRM use separate persistence. Core's current `DELETE /organizations/{organization_id}` only sets `organizations.deleted_at` and does not perform product cleanup. FAIR CRM already consumes Core lifecycle through a read-only lifecycle snapshot and does not persist or own Core lifecycle status.

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

- [ ] **OL08-01B — Durable FAIR CRM execution model**
  - Add an organization-scoped closure execution record owned by FAIR CRM.
  - Persist stable execution id, target organization id, status/current phase, idempotency identity, actor/audit references and timestamps.
  - Enforce at most one open execution per organization.

- [ ] **OL08-01C — SYSTEM-authorized start/status/retry contract**
  - Expose only the minimum public product contract needed to start, inspect and retry closure execution.
  - Reuse canonical Platform SuperAdmin / SYSTEM authority; do not create organization-role destructive authority.
  - Cross-organization and ordinary-user attempts fail closed without mutation.

- [ ] **OL08-01D — Core lifecycle precondition**
  - Start/retry re-checks canonical Core lifecycle authority.
  - New closure execution requires the target organization to be `SUSPENDED` and non-deleted.
  - Core lifecycle outage, malformed response, wrong organization or any state other than `SUSPENDED` fails closed.
  - No local cached lifecycle value becomes authority.

- [ ] **OL08-01E — Idempotency / failure / restart semantics**
  - Duplicate start with the same idempotency identity returns/converges on the same execution.
  - A conflicting second open closure execution is rejected.
  - Partial internal failure is persisted as explicit execution evidence rather than silently advancing.
  - Retry resumes the same logical execution and cannot duplicate a future externally visible phase.

- [ ] **OL08-01F — Audit evidence**
  - Start, meaningful phase/status transition and retry/recovery actions produce auditable evidence.
  - Evidence identifies actor, organization, execution and transition without retaining raw credentials/tokens.

- [ ] **OL08-01G — Tombstone safety contract**
  - OL08-01 contains no call to Core organization delete.
  - No OL08-01 state can be interpreted as proof that export/provider/data/artifact/backup obligations are complete.
  - Final tombstone remains blocked until the later required OL-08/09/10 phases are accepted and certified.

- [ ] **OL08-01H — Adversarial / tenant-isolation certification**
  - ordinary organization user denied,
  - OrganizationAdmin denied,
  - foreign organization target denied,
  - lifecycle spoof/cached local state cannot bypass Core authority,
  - duplicate-start race cannot create two open executions,
  - retry after failure remains idempotent,
  - lifecycle authority outage fails closed,
  - tombstoned/missing organization cannot start or resume closure execution as if valid.

- [ ] **OL08-01I — Cross-repository certification / docs sync**
  - FAIR CRM runtime/tests green on exact final head,
  - production-shaped lifecycle integration evidence green where applicable,
  - Platform tracker/ADR/status synchronized,
  - no merge without explicit authorization.

## OL08-01 state-machine constraints

The runtime may choose concrete internal names during implementation, but the following semantic states are mandatory:

```text
no execution
  -> open/in-progress          only if Core == SUSPENDED and SYSTEM-authorized
  -> blocked/failed            explicit recoverable evidence
  -> open/in-progress          idempotent retry of same execution
```

OL08-01 intentionally has **no terminal "cleanup complete" or "ready for tombstone" transition**. Those meanings depend on later policy/implementation phases that are still blocked.

## Still-blocked OL-08 decisions

| Decision | Status | Runtime boundary |
| --- | --- | --- |
| OL08-B — closure export obligation/contract | **OPEN** | No closure-complete export implementation yet. |
| OL08-C — provider credential disposition | **OPEN** | No provider revoke or local secret purge authorized. |
| OL08-D — product-data disposition matrix | **OPEN / depends on OL-09** | No organization-wide anonymize/hard-delete authorized. |
| OL08-E — generated artifact disposition | **OPEN** | No closure-driven artifact purge authorized. |
| OL08-F — audit/security evidence retention | **OPEN / policy required** | OL08-01 may create audit evidence but does not choose retention duration. |
| OL08-G — backup/restore interaction | **OPEN / depends on OL-10** | No backup ageing or restore reconciliation semantics authorized. |
| OL-09 — retention/grace durations | **OPEN CHOICE** | No duration or grace window may be invented. |
| OL-10 — backup restore implications | **OPEN CHOICE** | Destructive closure cannot be certified until restore behavior is explicit. |

## Certified/current baseline carried into OL08-01

- OL-07 already provides deterministic quiescence while Core is non-active: covered queued work is cancelled before start, covered running work stops at safe checkpoints, and new provider handoff is blocked.
- Core organization delete is a soft tombstone (`deleted_at`), not FAIR CRM product-data deletion.
- The current Core delete endpoint has no product-offboarding-complete prerequisite; OL-08 therefore must not use it until the later final tombstone gate is implemented.
- Core lifecycle snapshot exposes current canonical lifecycle state and allows product work only for `ACTIVE` organizations.
- FAIR CRM lifecycle consumption is read-only/fail-closed and deliberately does not persist Core lifecycle authority.

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

Implement **OL08-01B through OL08-01H in FAIR CRM** as one or more independently reviewable runtime PRs. Keep every destructive/off-platform phase blocked until its governing decision is separately accepted.