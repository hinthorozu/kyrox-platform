# P0.2 OL-05 — Organization Destructive Lifecycle Authority Implementation Tracker

**Status:** IN PROGRESS  
**Decision:** OL-05 ACCEPTED  
**Accepted:** 2026-09-03  
**Current resume point:** `OL05-08 — add deterministic negative authorization matrix; OL05-07 audit gap is carried into OL05-09`  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**Working decision draft:** `ecosystem/P0_2_LIFECYCLE_DECISIONS_DRAFT.md`  
**Scope owners:** `kyrox-core` for canonical organization lifecycle authority, `fair-crm` for product bridge/UI enforcement, `kyrox-platform` for policy/tracking/certification.

## Accepted OL-05 policy

Organization suspension, closure and destructive deletion remain Platform SuperAdmin-controlled SYSTEM operations. OrganizationAdmin cannot directly execute these operations. An organization-facing closure-request workflow may be provided, but such a request does not grant destructive lifecycle authority. All executed lifecycle transitions must be auditable.

> Organizasyon suspend, kapatma ve destructive delete işlemleri yalnız Platform SuperAdmin tarafından yürütülür. OrganizationAdmin bu işlemleri doğrudan gerçekleştiremez. OrganizationAdmin için kapatma talebi oluşturma özelliği sağlanabilir ancak bu talep destructive lifecycle yetkisi vermez. Gerçekleştirilen lifecycle değişiklikleri audit edilmelidir.

## Scope boundary

This tracker certifies **who may execute destructive organization lifecycle operations** and whether that authority is enforced end-to-end. It does not decide OL-06 reactivation, OL-07 queued/running work, OL-08 offboarding ordering, OL-09 retention, OL-10 backup restore, OL-11 Admin/System IA, or the optional closure-request feature.

---

## OL05-01 — Core permission / scope authority audit — COMPLETE

- [x] `identity.organizations.suspend` is SYSTEM-scope.
- [x] `identity.organizations.delete` is SYSTEM-scope.
- [x] Both are non-assignable to organization roles.
- [x] Existing system-permission role grants are removed by migration.
- [x] PostgreSQL permission-lifecycle trigger rejects role assignment for non-organization-scope permissions.
- [x] Role-management API rejects `permission_scope != organization`.
- [x] Runtime permission checker grants normal users only organization-scope permissions.
- [x] SuperAdmin bypass is based on the canonical database `is_super_admin` identity flag, not a role-name bypass.

**Evidence:**
- Core `backend/alembic/versions/20260816_0055_permission_scope.py`
- Core `backend/app/modules/identity/api/role_management/routes.py`
- Core `backend/app/modules/identity/infrastructure/authorization/services/sqlalchemy_permission_checker.py`
- Core authorization guards/scope enforcement.

**Result:** **PASS — current authority model matches accepted OL-05 policy.** No runtime authorization defect found here. Dedicated OL-05 regression tests are still required under OL05-08.

---

## OL05-02 — Core suspend endpoint authority audit — COMPLETE

- [x] Canonical public entry point located: `POST /api/v1/organizations/{organization_id}/suspend`.
- [x] Endpoint requires `identity.organizations.suspend` and organization-scope assertion.
- [x] SuperAdmin reaches the operation through the canonical platform bypass.
- [x] OrganizationAdmin cannot resolve the SYSTEM-scope permission through normal role authorization.
- [x] Cross-organization path/header spoofing does not create lifecycle authority.
- [x] No alternate suspend entry point that weakens this authority was identified in the current organization API.

**Evidence:** Core `backend/app/modules/identity/api/organization/routes.py`, authorization guards/scope, permission-scope migration and runtime permission checker.

**Result:** **PASS by current-code authority inspection.** Explicit actor-by-actor API regression tests are missing and are required under OL05-08 before DONE.

---

## OL05-03 — Core delete / closure endpoint authority audit — COMPLETE

- [x] Canonical public delete entry point located: `DELETE /api/v1/organizations/{organization_id}`.
- [x] Current Core delete is soft-delete/tombstone behavior; broader product closure is outside OL-05 and remains OL-08.
- [x] Endpoint requires `identity.organizations.delete` and organization-scope assertion.
- [x] SuperAdmin reaches the operation through the canonical platform bypass.
- [x] OrganizationAdmin cannot resolve the SYSTEM-scope permission through normal role authorization.
- [x] Cross-organization path/header spoofing does not create lifecycle authority.
- [x] No alternate organization delete path that weakens this authority was identified in the current organization API.

**Evidence:** Core organization routes/use-case/repository plus permission-scope/authorization evidence from OL05-01.

**Result:** **PASS by current-code authority inspection.** Explicit actor-by-actor API regression tests are still required under OL05-08.

---

## OL05-04 — Role-assignment / permission-governance negative audit — COMPLETE

- [x] SYSTEM lifecycle permissions cannot be assigned through the normal role-management API.
- [x] Custom organization roles cannot receive SYSTEM-scope permissions.
- [x] Database trigger prevents direct role-permission insertion for SYSTEM-scope permissions in PostgreSQL.
- [x] Runtime permission resolution additionally requires `permission_scope = organization` for normal users.
- [x] No role-name shortcut grants destructive lifecycle authority.

**Evidence:** permission-scope migration, role-management routes and SQLAlchemy permission checker.

**Result:** **PASS — defense in depth exists at API, DB-governance and runtime resolution layers.** A dedicated regression test for lifecycle permission assignment remains part of OL05-08.

---

## OL05-05 — FAIR CRM backend boundary audit — COMPLETE

- [x] Current destructive organization UI client does not use a FAIR CRM backend lifecycle proxy; it calls KYROX Core directly.
- [x] FAIR CRM therefore does not mint or reinterpret destructive lifecycle authority on this path.
- [x] The caller-supplied organization ID is still re-authorized by Core; it is not itself authority.
- [x] No FAIR CRM backend organization-lifecycle module/route was identified in the current backend application tree.

**Evidence:** FAIR CRM `frontend/src/api/organizations.ts`; current FAIR CRM backend application tree.

**Result:** **PASS — no additional FAIR backend destructive-lifecycle authority surface found.**

---

## OL05-06 — FAIR CRM UI / route audit — COMPLETE

- [x] Organization page delete control is gated by `identity.organizations.delete`.
- [x] That permission is SYSTEM-scope/non-assignable in Core, so OrganizationAdmin/normal organization roles cannot legitimately receive it.
- [x] Direct navigation to the organizations page does not grant destructive authority; the actual DELETE call is re-authorized by Core.
- [x] Organization creation is separately gated by `session.isSuperAdmin === true`.
- [x] No organization suspend control is currently exposed by this FAIR CRM page.
- [x] Broader Admin/System navigation restructuring is intentionally left to OL-11.

**Evidence:** FAIR CRM `frontend/src/pages/OrganizationsPage.tsx`, `frontend/src/api/organizations.ts`, `frontend/src/permissions/navigationPermissions.ts`, `frontend/src/permissions/corePermissions.ts`, `frontend/src/auth/AuthContext.tsx`.

**Result:** **PASS for OL-05 authority.** Current admin information architecture may be confusing, but it does not replace Core backend authorization and is not an OL-05 blocker by itself.

---

## OL05-07 — Audit evidence verification — COMPLETE, REAL GAP FOUND

- [x] Verified Core audit architecture: audit recording is explicit application/service behavior; there is no generic middleware auto-audit that automatically covers organization suspend/delete.
- [x] Inspected current organization suspend/delete route, use-case and repository path.
- [x] No explicit lifecycle audit event is recorded by the current suspend/delete execution path.

Required accepted-policy evidence is therefore currently missing for successful suspend/delete transitions:

- actor identity,
- target organization,
- lifecycle action,
- timestamp/outcome as an organization lifecycle audit record.

The audit subsystem already supports structured actor/resource/action/context data; the lifecycle path simply does not invoke it today.

**Result:** **FAIL / VERIFIED IMPLEMENTATION GAP.** Add explicit audit recording for successful organization suspension and deletion/soft-deletion, with no secret/token/password material. This defect is carried to OL05-09.

---

## OL05-08 — Negative authorization certification matrix — NEXT

Final deterministic evidence must prove at minimum:

| Actor / attempt | Suspend | Delete / closure | Expected |
| --- | ---: | ---: | --- |
| Platform SuperAdmin | allowed | allowed | PASS |
| OrganizationAdmin — own org | denied | denied | 403 / authoritative denial |
| OrganizationAdmin — other org | denied | denied | 403 / authoritative denial |
| Normal organization user — own org | denied | denied | 403 / authoritative denial |
| Normal organization user — other org | denied | denied | 403 / authoritative denial |
| Spoofed organization identifier | denied | denied | no authority bypass |
| Organization role assignment attempt for SYSTEM lifecycle permission | denied | denied | permission remains non-assignable |

- [ ] Add/strengthen deterministic Core API regression tests for the matrix.
- [ ] Add/strengthen role-assignment negative regression coverage for lifecycle SYSTEM permissions.
- [ ] Prove SuperAdmin allowed cases still work.
- [ ] Treat any uncovered row as a certification gap.

**Evidence:** _pending implementation/tests_

---

## OL05-09 — Verified-gap implementation

Verified gaps from OL05-01 through OL05-07:

1. **REAL IMPLEMENTATION DEFECT:** successful Core organization suspend/delete transitions are not explicitly audit-recorded.
2. **MISSING PROOF/TEST:** actor-by-actor suspend/delete negative authorization matrix is not directly covered by the current organization API test suite.
3. **MISSING PROOF/TEST:** lifecycle SYSTEM-permission role-assignment invariant needs a focused regression test even though API/DB/runtime controls already exist.

Planned narrow implementation:

- [ ] Add explicit Core audit recording for successful suspend.
- [ ] Add explicit Core audit recording for successful delete/soft-delete.
- [ ] Add narrow authorization/audit regression tests.
- [ ] Do not add OL-06/07/08/09/10 behavior.
- [ ] Do not add optional closure-request workflow.

---

## OL05-10 — Cross-repository certification

- [ ] Core authoritative tests green.
- [ ] FAIR CRM relevant authorization/UI evidence remains green where applicable.
- [ ] Production-shaped/integration gate green where applicable.
- [ ] Direct API negative cases prove OrganizationAdmin cannot execute destructive lifecycle operations.
- [ ] SuperAdmin allowed cases prove canonical operations still work.
- [ ] Audit evidence verified for successful lifecycle execution.
- [ ] No tenant-isolation regression introduced.

---

## OL05-11 — Canonical status synchronization

Only after OL05-01 through OL05-10 are complete:

- [ ] Update this tracker to `Status: DONE`.
- [ ] Set `Current resume point: OL-05 complete; continue with OL-06`.
- [ ] Update ADR-0006 OL-05 implementation/certification status without changing the accepted policy.
- [ ] Update the lifecycle draft/status table and applicable roadmap/status records.
- [ ] Preserve all evidence.

---

## Completion rule

`ACCEPTED` means the policy is decided. `DONE` means the accepted policy has been verified in current code, real gaps fixed, negative authorization behavior proven, audit evidence confirmed, and relevant cross-repository gates green.

## Resume protocol

Whenever work stops, keep **Current resume point** set to the next action. On resume: read this tracker, verify current repo heads, continue from the pending item, and do not repeat already-certified work unless a repository change invalidates the evidence.
