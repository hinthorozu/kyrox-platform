# P0.2 OL-06 — Organization Reactivation Implementation Tracker

**Status:** IN PROGRESS — Core implementation PR open  
**Decision:** OL-06 ACCEPTED 2026-09-03  
**Started:** 2026-09-03  
**Completed:** —  
**Current resume point:** KYROX Core PR #23 implements the accepted reactivation contract; CI must remain green and cross-repository certification/status synchronization must complete before OL-06 is marked DONE.  
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
  - Core already provides `Organization.reactivate()`.
  - The domain transition permits only `SUSPENDED -> ACTIVE` and rejects any other organization status.

- [ ] **OL06-03 — SYSTEM permission migration**
  - KYROX Core PR #23 adds `identity.organizations.reactivate` as SYSTEM-scoped and non-assignable.
  - Migration repair logic removes any pre-existing organization-role association/exclusion for the permission.
  - Complete when PR #23 is merged to Core `main` with green CI.

- [ ] **OL06-04 — Explicit Core reactivation API**
  - KYROX Core PR #23 adds `POST /organizations/{organization_id}/reactivate`.
  - The endpoint uses the existing Core domain transition rather than duplicating lifecycle state logic.
  - Complete when PR #23 is merged to Core `main`.

- [ ] **OL06-05 — Authorization matrix**
  - Anonymous access is denied.
  - Normal organization users are denied.
  - Cross-organization spoof attempts are denied.
  - Platform SuperAdmin succeeds for a suspended organization.
  - Rejected requests must not mutate organization state.
  - Complete when PR #23 is merged and CI is green.

- [ ] **OL06-06 — Source-state safety matrix**
  - `SUSPENDED -> ACTIVE` succeeds.
  - `ACTIVE`, `PENDING_ACTIVATION`, and `ARCHIVED` reactivation attempts are rejected.
  - Soft-deleted/tombstoned organizations cannot be revived through reactivation.
  - Rejected transitions do not create successful-reactivation audit evidence.
  - Complete when PR #23 is merged and CI is green.

- [ ] **OL06-07 — Lifecycle audit evidence**
  - Successful reactivation emits `identity.organization.reactivated` audit evidence.
  - Audit persistence uses the same lifecycle request transaction pattern certified in OL-05.
  - Complete when PR #23 is merged and CI is green.

- [ ] **OL06-08 — FAIR CRM/product boundary audit**
  - Confirm current FAIR CRM does not expose an alternate organization-reactivation authority that widens the Core SYSTEM boundary.
  - Confirm OL-06 does not accidentally resume queued/running product jobs, provider credentials, outbound mail or other side effects; those remain OL-07.

- [ ] **OL06-09 — Cross-repository certification**
  - KYROX Core runtime implementation and tests merged/green.
  - FAIR CRM boundary audited without widening reactivation authority.
  - KYROX Platform evidence synchronized canonically.

- [ ] **OL06-10 — ADR / roadmap status synchronization**
  - ADR-0006 records OL-06 as accepted while implementation is in progress.
  - After certification, SaaS/FAIR CRM roadmap wording must mark OL-06 DONE and move the next decision gate to OL-07.

## Target certified matrix

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

## Current implementation evidence

KYROX Core PR #23 (`feat(identity): implement OL-06 organization reactivation`) is open. Its first CI run completed successfully with lint and the backend test suite green. Additional source-state certification tests were added afterward, so the latest PR head must complete CI successfully before merge/certification.

## Completion rule

OL-06 becomes **DONE** only after Core PR #23 is merged with green CI, the FAIR CRM/product boundary is audited, and ADR/roadmap status is synchronized. Until then, the accepted decision is implementation-active but not certified complete.
