# P0.2 OL-05 — Organization Destructive Lifecycle Authority Implementation Tracker

**Status:** IN PROGRESS  
**Decision:** OL-05 ACCEPTED  
**Accepted:** 2026-09-03  
**Current resume point:** `OL05-01 — Core permission / scope authority audit`  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**Working decision draft:** `ecosystem/P0_2_LIFECYCLE_DECISIONS_DRAFT.md`  
**Scope owners:** `kyrox-core` for canonical organization lifecycle authority, `fair-crm` for product bridge/UI enforcement, `kyrox-platform` for policy/tracking/certification.

## Accepted OL-05 policy

Organization suspension, closure and destructive deletion remain Platform SuperAdmin-controlled SYSTEM operations. OrganizationAdmin cannot directly execute these operations. An organization-facing closure-request workflow may be provided, but such a request does not grant destructive lifecycle authority. All executed lifecycle transitions must be auditable.

Turkish working statement:

> Organizasyon suspend, kapatma ve destructive delete işlemleri yalnız Platform SuperAdmin tarafından yürütülür. OrganizationAdmin bu işlemleri doğrudan gerçekleştiremez. OrganizationAdmin için kapatma talebi oluşturma özelliği sağlanabilir ancak bu talep destructive lifecycle yetkisi vermez. Gerçekleştirilen lifecycle değişiklikleri audit edilmelidir.

## Scope boundary

This tracker certifies **who may execute destructive organization lifecycle operations** and whether that authority is enforced end-to-end.

It does **not** decide:

- OL-06 reactivation semantics,
- OL-07 queued/running job and provider behavior after suspension,
- OL-08 closure/export/retention/delete sequencing,
- OL-09 retention/grace durations,
- OL-10 backup restore semantics,
- OL-11 final Admin/System UI information architecture,
- an OrganizationAdmin self-service closure-request feature.

The optional closure-request feature is non-blocking for OL-05 unless separately approved.

---

## Execution checklist

### OL05-01 — Core permission / scope authority audit

- [ ] Verify `identity.organizations.suspend` is SYSTEM-scope.
- [ ] Verify `identity.organizations.delete` is SYSTEM-scope.
- [ ] Verify these permissions are non-assignable to organization roles.
- [ ] Verify no alternate permission, role-name bypass or legacy path grants equivalent destructive authority.
- [ ] Record exact code/migration/test evidence.

**Evidence:** _pending_

**Result:** _pending_

---

### OL05-02 — Core suspend endpoint authority audit

- [ ] Locate every public/internal organization suspend entry point.
- [ ] Verify backend authorization is Platform SuperAdmin/SYSTEM authoritative.
- [ ] Verify OrganizationAdmin cannot suspend its own organization by direct API call.
- [ ] Verify OrganizationAdmin cannot suspend another organization.
- [ ] Verify normal users cannot suspend any organization.
- [ ] Verify spoofed organization identifiers cannot bypass authority.
- [ ] Record exact endpoint, guard, tests and runtime evidence.

**Evidence:** _pending_

**Result:** _pending_

---

### OL05-03 — Core delete / closure endpoint authority audit

- [ ] Locate every public/internal organization delete/soft-delete/closure entry point.
- [ ] Verify backend authorization is Platform SuperAdmin/SYSTEM authoritative.
- [ ] Verify OrganizationAdmin cannot delete/close its own organization by direct API call.
- [ ] Verify OrganizationAdmin cannot delete/close another organization.
- [ ] Verify normal users cannot delete/close any organization.
- [ ] Verify spoofed organization identifiers cannot bypass authority.
- [ ] Record exact endpoint, guard, tests and runtime evidence.

**Evidence:** _pending_

**Result:** _pending_

---

### OL05-04 — Role-assignment and permission-governance negative checks

- [ ] Verify SYSTEM lifecycle permissions cannot be assigned to `OrganizationAdmin`.
- [ ] Verify custom organization roles cannot receive those permissions.
- [ ] Verify role-template/update APIs reject or filter SYSTEM lifecycle permissions as intended.
- [ ] Verify no database-backed organization role currently contains destructive organization lifecycle authority.
- [ ] Add or strengthen negative tests if the current suite does not prove this invariant.

**Evidence:** _pending_

**Result:** _pending_

---

### OL05-05 — FAIR CRM backend boundary audit

- [ ] Locate FAIR CRM organization lifecycle bridge/proxy/client paths, if any.
- [ ] Verify FAIR CRM does not weaken Core lifecycle authority.
- [ ] Verify tenant/user-controlled `organization_id` input cannot be used to execute a SYSTEM lifecycle operation.
- [ ] Verify FAIR CRM never treats frontend visibility as the security boundary.
- [ ] If FAIR CRM has no destructive lifecycle bridge, record that explicitly as evidence rather than inventing one.

**Evidence:** _pending_

**Result:** _pending_

---

### OL05-06 — FAIR CRM UI / route audit

- [ ] Verify OrganizationAdmin does not see destructive organization suspend/delete controls.
- [ ] Verify normal users do not see such controls.
- [ ] Verify direct navigation to any lifecycle-management route does not grant authority.
- [ ] Verify Platform SuperAdmin-only lifecycle UI, if present, matches backend authority.
- [ ] Treat UI hiding as UX only; backend denial remains mandatory.
- [ ] Do not perform the broader OL-11 Admin/System information-architecture refactor here.

**Evidence:** _pending_

**Result:** _pending_

---

### OL05-07 — Audit evidence verification

For every executed destructive lifecycle transition covered by OL-05:

- [ ] actor identity is recorded,
- [ ] target organization is recorded,
- [ ] action/transition is recorded,
- [ ] timestamp is recorded,
- [ ] outcome/status is determinable,
- [ ] secrets/tokens/passwords are not logged,
- [ ] audit evidence cannot be forged by organization-scoped caller input.

Reason/description may be recorded where supported; absence of an optional free-text reason does not by itself fail OL-05 unless policy is expanded later.

**Evidence:** _pending_

**Result:** _pending_

---

### OL05-08 — Negative authorization certification matrix

The final evidence must prove at minimum:

| Actor / attempt | Suspend | Delete / closure | Expected |
| --- | ---: | ---: | --- |
| Platform SuperAdmin | allowed | allowed | PASS |
| OrganizationAdmin — own org | denied | denied | 403 / authoritative denial |
| OrganizationAdmin — other org | denied | denied | 403 / authoritative denial |
| Normal organization user — own org | denied | denied | 403 / authoritative denial |
| Normal organization user — other org | denied | denied | 403 / authoritative denial |
| Spoofed organization identifier | denied | denied | no authority bypass |
| Organization role assignment attempt for SYSTEM lifecycle permission | denied | denied | permission remains non-assignable |

- [ ] Matrix covered by deterministic automated tests and/or production-shaped certification evidence.
- [ ] Any uncovered row is treated as a test/certification gap until resolved.

**Evidence:** _pending_

**Result:** _pending_

---

### OL05-09 — Verified-gap implementation

Do not patch speculatively.

- [ ] Consolidate findings from OL05-01 through OL05-08.
- [ ] Classify each finding as:
  - already correct,
  - missing proof/test only,
  - real implementation defect.
- [ ] Implement only verified defects required by the accepted OL-05 policy.
- [ ] Add the narrowest sufficient regression tests.
- [ ] Do not add OL-06/07/08/09/10 behavior under OL-05.
- [ ] Do not add the optional closure-request product feature unless separately authorized.

**Verified gaps:** _pending_

**Implementation evidence:** _pending_

---

### OL05-10 — Cross-repository certification

- [ ] Core authoritative tests green.
- [ ] FAIR CRM relevant authorization/UI tests green.
- [ ] Production-shaped / integration gate green where applicable.
- [ ] Direct API negative cases prove OrganizationAdmin cannot execute destructive lifecycle operations.
- [ ] SuperAdmin allowed cases prove the canonical operation still works.
- [ ] Audit evidence verified for successful lifecycle execution.
- [ ] No tenant-isolation regression introduced.

**Evidence:** _pending_

**Result:** _pending_

---

### OL05-11 — Canonical status synchronization

Only after OL05-01 through OL05-10 are complete:

- [ ] Update this tracker to `Status: DONE`.
- [ ] Set `Current resume point: OL-05 complete; continue with OL-06`.
- [ ] Update ADR-0006 OL-05 status from `ACCEPTED` to implementation/certification-complete wording without changing the accepted policy.
- [ ] Update the P0.2 lifecycle decision draft/status table.
- [ ] Update applicable Platform/Fair CRM roadmap or status records if required.
- [ ] Preserve evidence; do not delete completed checklist history.

**Evidence:** _pending_

---

## Completion rule

`ACCEPTED` means the policy is decided. `DONE` means the accepted policy has been verified in current code, any real gaps have been fixed, negative authorization behavior is proven, audit evidence is confirmed, and the relevant cross-repository gates are green.

OL-05 must not be marked DONE merely because the current design appears to match the policy.

## Resume protocol

Whenever work stops, update **Current resume point** at the top of this file to the first incomplete checklist item and preserve all completed evidence below it.

On resume:

1. read this tracker,
2. read ADR-0006 only if policy context is needed,
3. verify current repository heads before relying on old evidence,
4. continue from the first unchecked item,
5. do not restart already-certified work unless repository changes invalidate its evidence.
