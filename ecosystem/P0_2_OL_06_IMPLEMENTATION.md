# P0.2 OL-06 — Organization Reactivation Implementation Tracker

**Status:** DONE — OL-06 certified 2026-09-04  
**Decision:** OL-06 ACCEPTED 2026-09-03  
**Started:** 2026-09-03  
**Completed:** 2026-09-04  
**Current resume point:** COMPLETE — OL-06 certified; next decision gate is OL-07 suspension job/provider behavior.  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Accepted policy

> **Organization reactivation is a Platform SuperAdmin-controlled SYSTEM lifecycle operation. Reactivation is valid only for a non-deleted organization in `SUSPENDED` state and transitions it to `ACTIVE`. Successful reactivation must be auditable. Reactivation does not revive `PENDING_ACTIVATION`, already `ACTIVE`, `ARCHIVED`, or soft-deleted organizations, and it does not define queued/running job, provider-credential, or side-effect resumption semantics; those remain OL-07 scope.**

Operationally:

- reactivation authority is Platform SuperAdmin / SYSTEM only,
- `OrganizationAdmin` and normal organization users cannot execute reactivation,
- the canonical state transition is strictly `SUSPENDED -> ACTIVE`,
- successful reactivation creates lifecycle audit evidence identifying actor, target organization, transition and timestamp,
- non-suspended source states are rejected without state mutation or successful-reactivation audit evidence,
- soft-deleted/tombstoned organizations are not revived through reactivation,
- Core owns the canonical lifecycle mutation; product job/provider resumption remains separately gated by OL-07.

## Certification checklist

- [x] **OL06-01 — Decision acceptance / scope boundary**
  - Reactivation is accepted as a Platform SuperAdmin-controlled SYSTEM action.
  - OL-07 queued/running job, provider credential and side-effect semantics are explicitly excluded from OL-06.

- [x] **OL06-02 — Existing domain transition verified**
  - Core provides `Organization.reactivate()`.
  - The domain transition permits only `SUSPENDED -> ACTIVE` and rejects any other organization status.

- [x] **OL06-03 — SYSTEM permission migration**
  - KYROX Core PR #23 added `identity.organizations.reactivate` as SYSTEM-scoped and non-assignable.
  - Migration repair logic removes any pre-existing organization-role association/exclusion for the permission.
  - Core PR #23 merged to `main` as `f24089cbb29f38b42270d0d9edb2235aa7815719` after CI #88 passed.

- [x] **OL06-04 — Explicit Core reactivation API**
  - Core exposes `POST /organizations/{organization_id}/reactivate`.
  - The endpoint uses the existing Core domain transition rather than duplicating lifecycle state logic.
  - Runtime implementation is merged on Core `main` through PR #23.

- [x] **OL06-05 — Authorization matrix**
  - Anonymous access is denied.
  - Normal organization users are denied.
  - Cross-organization spoof attempts are denied.
  - Platform SuperAdmin succeeds for a suspended organization.
  - Rejected requests do not mutate organization state.
  - The final Core PR #23 head passed CI #88 before merge.

- [x] **OL06-06 — Source-state safety matrix**
  - `SUSPENDED -> ACTIVE` succeeds.
  - `ACTIVE`, `PENDING_ACTIVATION`, and `ARCHIVED` reactivation attempts are rejected.
  - Soft-deleted/tombstoned organizations cannot be revived through reactivation.
  - Rejected transitions do not create successful-reactivation audit evidence.
  - The final Core PR #23 head passed CI #88 before merge.

- [x] **OL06-07 — Lifecycle audit evidence**
  - Successful reactivation emits `identity.organization.reactivated` audit evidence.
  - Audit persistence uses the same lifecycle request transaction pattern certified in OL-05.
  - The implementation is merged on Core `main` through PR #23.

- [x] **OL06-08 — FAIR CRM/product boundary audit**
  - Current FAIR CRM `main` verification found no product-owned `reactivate` or `suspend` organization lifecycle action/endpoint that widens the Core SYSTEM boundary.
  - No OL-06 FAIR CRM runtime behavior was added.
  - Queued/running jobs, provider credentials, outbound mail and other side-effect resumption remain untouched and explicitly remain OL-07 scope.

- [x] **OL06-09 — Cross-repository certification**
  - KYROX Core runtime implementation and tests are merged/green through Core PR #23 / CI #88.
  - FAIR CRM boundary is audited without widening reactivation authority.
  - KYROX Platform completion evidence is synchronized through Platform PR #28.

- [x] **OL06-10 — ADR / roadmap status synchronization**
  - ADR-0006 records OL-06 as accepted and implementation-certified.
  - SaaS and FAIR CRM roadmaps record OL-06 as DONE.
  - The next lifecycle decision gate is OL-07.

## Certified matrix

```text
Platform SuperAdmin -> SUSPENDED -> ACTIVE              ALLOW
OrganizationAdmin -> reactivate                         DENY
Normal organization user -> reactivate                  DENY
Cross-organization spoof -> reactivate                  DENY
ACTIVE -> ACTIVE via reactivate                          DENY
PENDING_ACTIVATION -> ACTIVE via reactivate              DENY
ARCHIVED -> ACTIVE via reactivate                        DENY
Soft-deleted/tombstoned -> ACTIVE via reactivate         DENY
Successful reactivation -> audit evidence                REQUIRED
Reactivation -> product job/provider resumption          NOT OL-06 / OL-07
```

## Scope boundary / non-goals

OL-06 defines **who may reactivate an organization and the canonical Core state transition**. It does not decide or implement:

- OL-07 queued/running job cancellation, pause, drain or restart behavior,
- OL-07 provider credential usability or outbound side-effect resumption,
- OL-08 closure/export/retention/anonymization/delete sequencing,
- OL-09 retention/grace durations,
- OL-10 backup restore implications,
- a generic restore mechanism for archived or deleted organizations.

## Completion evidence

- KYROX Core PR #23 (`feat(identity): implement OL-06 organization reactivation`) final head `655b61155e0ad799d7381d21858c9fd1d5b3a0f7` passed CI #88 and was squash-merged to Core `main` as `f24089cbb29f38b42270d0d9edb2235aa7815719`.
- The merged Core contract includes the SYSTEM/non-assignable reactivation permission, explicit API, domain transition reuse, lifecycle audit evidence, authorization matrix, invalid source-state rejection, soft-delete rejection and migration coverage.
- FAIR CRM current-main verification found no alternate product-owned organization reactivation/suspension authority, and OL-06 introduced no product job/provider/mail resumption behavior.
- KYROX Platform PR #28 records the accepted decision, this completion tracker, ADR synchronization and roadmap synchronization.

## Completion statement

OL-06 is **DONE as of 2026-09-04**. The supported organization reactivation contract is now explicit, SYSTEM-scoped, auditable and implemented on KYROX Core `main`. Full P0.2 remains open because OL-07 through OL-10 are unresolved. The next decision gate is **OL-07 — suspension job/provider behavior**.