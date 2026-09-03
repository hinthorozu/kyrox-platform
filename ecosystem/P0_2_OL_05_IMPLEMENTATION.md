# P0.2 OL-05 — Destructive Organization Authority Implementation Tracker

**Status:** DONE — OL-05 certified 2026-09-03  
**Decision:** OL-05 ACCEPTED 2026-09-03  
**Started:** 2026-09-03  
**Completed:** 2026-09-03  
**Current resume point:** COMPLETE — OL-05 certified; next decision gate is OL-06  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Accepted policy

> **Organization suspension, closure and destructive deletion remain Platform SuperAdmin-controlled SYSTEM operations. OrganizationAdmin cannot directly execute these operations. An organization-facing closure-request workflow may be provided, but such a request does not grant destructive lifecycle authority. All executed lifecycle transitions must be auditable.**

Operationally:

- organization suspension is Platform SuperAdmin / SYSTEM authority only,
- organization closure/destructive lifecycle execution is Platform SuperAdmin / SYSTEM authority only,
- OrganizationAdmin cannot receive the required SYSTEM permissions through an organization role,
- a future organization-facing closure request is only a request and does not confer lifecycle execution authority,
- successful lifecycle transitions must create audit evidence,
- Core organization delete remains a soft-delete/tombstone; FAIR CRM product-data offboarding/retention/deletion semantics remain OL-08 scope.

## Certification checklist

- [x] **OL05-01 — Core permission/scope authority audit**
  - `identity.organizations.suspend` and `identity.organizations.delete` are SYSTEM-scope lifecycle permissions.
  - Normal organization authorization does not resolve SYSTEM permissions as organization-role authority.

- [x] **OL05-02 — Core suspend endpoint authority audit**
  - The Core suspend endpoint remains protected by backend authorization; UI visibility is not treated as the security boundary.

- [x] **OL05-03 — Core delete endpoint authority audit**
  - The Core delete endpoint remains protected by backend authorization.
  - Core delete is a soft-delete/tombstone and is not treated as FAIR CRM product-data deletion.

- [x] **OL05-04 — Organization-role assignment negative regression**
  - KYROX Core PR #22 adds regression coverage proving a SYSTEM-scope lifecycle permission cannot be assigned to an organization-role template, even by Platform SuperAdmin.
  - The test requires HTTP 403 and proves no role-permission association is persisted.
  - PR #22 merged to Core `main`; CI was green.

- [x] **OL05-05 — FAIR CRM backend/product boundary audit**
  - Current FAIR CRM `main` exposes no alternate product-owned suspend/delete authority that widens the Core SYSTEM boundary.
  - Organization lifecycle authority therefore remains Core-owned rather than being duplicated in FAIR CRM.

- [x] **OL05-06 — FAIR CRM UI/direct-call consistency audit**
  - The current organization-management UI consumes KYROX Core organization APIs.
  - UI permission gating is treated only as UX; Core backend authorization remains authoritative for lifecycle mutations.
  - No FAIR CRM suspend UI action was found in the current organization page during certification.

- [x] **OL05-07 — Lifecycle audit evidence**
  - KYROX Core PR #21 adds audit events for successful organization suspend/delete transitions.
  - Audit persistence occurs in the same request transaction as the lifecycle mutation so a successful mutation is not intentionally committed without its audit evidence.

- [x] **OL05-08 — Negative authorization matrix**
  - KYROX Core PR #21 certifies anonymous denial, normal organization-user denial, cross-organization spoof denial, and Platform SuperAdmin success for the covered lifecycle endpoints.
  - Rejected requests are asserted not to mutate organization state.
  - PR #21 merged to Core `main`; lint and the Core test suite were green.

- [x] **OL05-09 — Verified gap implementation**
  - Real gap: successful lifecycle transitions lacked explicit audit evidence -> fixed by Core PR #21.
  - Evidence gap: SYSTEM lifecycle permission assignment invariant lacked a direct regression -> fixed by Core PR #22.
  - No speculative OL-06/OL-07/OL-08 runtime behavior was added.

- [x] **OL05-10 — Cross-repository certification**
  - KYROX Core: authority, mutation denial, role-assignment boundary and lifecycle audit certified.
  - FAIR CRM: current product/UI integration does not widen or duplicate Core lifecycle authority.
  - KYROX Platform: accepted policy and certification evidence synchronized canonically.

- [x] **OL05-11 — ADR / roadmap status synchronization**
  - ADR-0006 records OL-05 as accepted and certified/DONE.
  - SaaS and FAIR CRM roadmap wording records OL-05 completion while keeping OL-06 through OL-10 gated.

## Certified matrix

```text
Platform SuperAdmin -> suspend                         ALLOW
Platform SuperAdmin -> Core delete/tombstone           ALLOW
OrganizationAdmin -> suspend                           DENY
OrganizationAdmin -> delete                            DENY
Normal organization user -> suspend/delete             DENY
Cross-organization spoof -> lifecycle authority        DENY
SYSTEM lifecycle permission -> organization role       DENY
Successful suspend/delete -> audit evidence             REQUIRED / CERTIFIED
```

## Scope boundary / non-goals

OL-05 certifies **who may execute destructive organization lifecycle authority**. It does not decide or implement:

- OL-06 reactivation API/policy,
- OL-07 queued/running job and provider behavior after suspension,
- OL-08 closure/export/retention/anonymization/delete sequencing,
- OL-09 retention/grace durations,
- OL-10 backup restore implications,
- a future organization-facing closure-request product flow.

Those remain separately gated and must not be inferred from OL-05 completion.

## Completion statement

**OL-05 is DONE as of 2026-09-03.** The accepted authority model is implemented and regression-certified across the relevant Core and FAIR CRM boundaries, executed Core lifecycle transitions are auditable, and canonical Platform status is synchronized. Full P0.2 remains open because OL-06 through OL-10 are unresolved.