# FAIR CRM / KYROX — Feature Applicability Standard

**Status:** Canonical / binding applicability standard  
**Scope:** Fair CRM feature delivery, Core changes driven by Fair CRM, CI quality gates, Delivery Contracts  
**Audience:** Human developers, AI coding agents, reviewers and CI tooling

This document answers one question that the general delivery standard cannot answer by itself:

> **Which development gates actually apply to this feature?**

Not every feature is a CRUD module and not every feature has a frontend. A scheduled service, internal worker, integration adapter, read-only module, user-triggered operation or system capability must not be forced to invent CRUD permissions, pages, menus or UI that do not belong to the requirement.

The rule is therefore:

> **Required work must never be skipped; non-applicable work must never be invented.**

`projects/fair-crm/DEVELOPMENT_STANDARD.md` remains the canonical execution order. This document determines whether each gate in that order is **REQUIRED** or **N/A** for a particular feature.

---

## 1. Applicability is decided before implementation

Applicability is part of Gate 0 / Delivery Contract and must be decided before code is written.

Every material feature must have an explicit **Feature Profile**.

Allowed feature types:

```text
crud_module
read_only_module
backend_service
background_job
scheduled_job
user_triggered_operation
integration_adapter
system_admin
core_platform_capability
ui_only
maintenance
other
```

If none of these accurately describes the work, use `other` and describe the behavior explicitly. Do not select the closest profile merely to avoid a product decision.

---

## 2. REQUIRED vs N/A

Every applicable delivery area has exactly one state:

```text
REQUIRED
N/A
```

`OPTIONAL` is not a valid gate state. If a capability is genuinely optional from the product perspective, the product owner must decide whether it is in scope for the current delivery. After that decision it becomes either REQUIRED or N/A for the delivery.

### REQUIRED

The gate applies and must pass before the feature is accepted.

### N/A

The gate does not apply to the feature by design.

Every `N/A` must include a concrete reason.

Valid example:

```text
Frontend: N/A
Reason: Scheduled background service has no user-facing route, page, menu or action.
```

Invalid examples:

```text
Frontend: N/A
Reason: Not needed.
```

```text
Permissions: N/A
Reason: Easier this way.
```

`N/A` is not a bypass mechanism. It is an explicit architectural statement that the capability does not exist in the approved feature contract.

---

## 3. Canonical applicability areas

The machine-readable Feature Contract and CI gate use the following areas:

```text
database
migration
permissions
backend
api
tenant_isolation
audit
frontend
ui_permissions
menu
route_guard
forms
visual_qa
backend_tests
frontend_tests
runtime_authorization
runtime_verification
deployment
```

Additional feature-specific areas may be added when required, but the canonical areas above must not be renamed locally.

---

## 4. Default applicability matrix

This table defines defaults, not substitutes for the Delivery Contract. A feature may differ when the requirement genuinely differs, but every override must be explicit and justified.

| Feature type | DB / migration | Permissions | Backend / API | Tenant isolation | Frontend / UI | UI permission guards | Audit | Tests | Real JWT auth |
|---|---|---|---|---|---|---|---|---|---|
| `crud_module` | REQUIRED | REQUIRED | REQUIRED | REQUIRED when org-owned | REQUIRED | REQUIRED | REQUIRED for mutations | REQUIRED | REQUIRED |
| `read_only_module` | As needed | `read` when protected | REQUIRED | REQUIRED when org-owned | REQUIRED | REQUIRED when protected | Usually N/A | REQUIRED | REQUIRED when protected |
| `backend_service` | As needed | N/A unless user/API-triggered | REQUIRED | REQUIRED when org-owned | N/A | N/A | REQUIRED for meaningful side effects | REQUIRED | N/A unless user/API-triggered |
| `background_job` | As needed | N/A for internal execution; permission on user trigger if present | REQUIRED | REQUIRED when org-owned | N/A unless status/control UI exists | N/A unless UI exists | REQUIRED | REQUIRED | N/A unless user-triggered |
| `scheduled_job` | As needed | N/A for scheduler trigger | REQUIRED | REQUIRED when org-owned | N/A unless admin/status UI exists | N/A unless UI exists | REQUIRED | REQUIRED | N/A for scheduler path |
| `user_triggered_operation` | As needed | REQUIRED; normally semantic action such as `execute` | REQUIRED | REQUIRED when org-owned | REQUIRED when trigger is UI | REQUIRED when UI exists | REQUIRED | REQUIRED | REQUIRED |
| `integration_adapter` | As needed | N/A for internal adapter; semantic permissions for user management/execution if exposed | REQUIRED | REQUIRED when org-owned | N/A unless configurable by users | As applicable | REQUIRED for state-changing/external actions | REQUIRED | As applicable |
| `system_admin` | As needed | SYSTEM permission or explicit Super Admin guard | REQUIRED | Usually N/A or explicitly mixed | REQUIRED if user-facing | REQUIRED if UI exists | REQUIRED | REQUIRED | REQUIRED |
| `core_platform_capability` | As needed | As designed | REQUIRED in Core | According to platform contract | N/A unless a product consumes UI | N/A in Core-only delivery | REQUIRED where security/side effects matter | REQUIRED | REQUIRED when authorization-sensitive |
| `ui_only` | N/A | Existing effective permission model | N/A unless API changes too | N/A | REQUIRED | REQUIRED when protected | N/A | REQUIRED | Existing backend authorization must still be verified |
| `maintenance` | As needed | Usually N/A | As needed | As needed | As needed | As needed | As needed | REQUIRED for changed behavior | As applicable |
| `other` | Explicit | Explicit | Explicit | Explicit | Explicit | Explicit | Explicit | REQUIRED | Explicit |

---

## 5. CRUD permissions are not universal

CRUD permissions exist only when the product exposes those actions as meaningful user authorization boundaries.

A background service must not receive fake permissions such as:

```text
fair_crm.xyz_service.create
fair_crm.xyz_service.read
fair_crm.xyz_service.update
fair_crm.xyz_service.delete
```

merely because CRUD is the common module pattern.

If users can only start an operation, the correct permission may be only:

```text
fair_crm.xyz_sync.execute
```

If the service is triggered only by the scheduler or an internal trusted workflow, user RBAC may be:

```text
Permissions: N/A
Reason: No user, route or API authorization boundary triggers the service.
```

This does **not** mean the service has no security requirements. Tenant isolation, service authentication, trigger ownership, idempotency, logging/audit and tests still apply according to the feature contract.

---

## 6. Background execution model

Always distinguish the **trigger authorization** from the **internal execution**.

### User-triggered job

```text
User
  -> authenticated route
  -> semantic permission check (for example `.execute`)
  -> enqueue job
  -> worker executes approved job
```

The worker does not need to pretend to be a CRUD role. Authorization occurs at the trusted entry point; the queued job must carry enough validated organization/resource context to execute safely.

### Scheduled job

```text
Scheduler
  -> trusted internal trigger
  -> worker/service
  -> organization-safe processing
```

User CRUD permission is normally N/A for the scheduler path.

### Event/internal job

```text
Approved internal event
  -> service/job
  -> validated scoped payload
```

The internal trigger must be authenticated/trusted according to its architecture. Do not replace service trust with a fake end-user role.

---

## 7. Tenant isolation is independent from permissions

`permissions = N/A` never means `tenant_isolation = N/A` automatically.

If a backend service processes organization-owned records, tenant isolation is REQUIRED even when no user invokes it.

Example:

```text
Feature type: scheduled_job
Permissions: N/A
Frontend: N/A
Tenant isolation: REQUIRED
```

The service must have an explicit organization-processing strategy, for example processing one organization at a time or scoping every query by the organization carried by the trusted job context.

Cross-tenant queries require a specific platform/system design; they must not arise accidentally because a worker has no user permission check.

---

## 8. Frontend applicability

Frontend is REQUIRED only when the approved feature includes a user-facing surface.

When frontend is N/A, the following normally become N/A as well:

```text
ui_permissions
menu
route_guard
forms
visual_qa
frontend_tests
```

Each N/A still requires a reason in the Feature Contract, but one reason may support a coherent group when the same architectural fact applies to all of them.

If a backend service later receives a monitoring/control UI, that is a new material delivery and the applicability contract must be updated. Do not silently add a page without moving frontend/UI gates to REQUIRED.

---

## 9. Permission-aware UI applicability

When a user-facing protected feature exists:

- module/read access controls navigation and route visibility where applicable,
- mutation/action controls map to their exact effective permissions,
- direct URLs must not bypass authorization-aware rendering,
- backend authorization remains mandatory.

When no user-facing surface exists, these UI authorization gates are N/A rather than artificially satisfied with hidden placeholder pages.

---

## 10. System capabilities

A system-only capability may be user-facing to Super Admin while remaining unavailable to organization roles.

Example:

```text
Feature type: system_admin
Frontend: REQUIRED
Permissions: REQUIRED
Permission scope: system
OrganizationAdmin: denied
Super Admin: allowed via central bypass / system guard
```

A system capability does not become an organization capability merely because it has a CRUD-shaped UI.

---

## 11. Feature Contract — machine-readable form

For new material Fair CRM features, the code repository may carry a machine-readable contract at:

```text
.kyrox/features/<feature-id>.json
```

This file is **governance metadata**, not a second Markdown source of truth. The canonical meaning of its fields is defined by this document and `DEVELOPMENT_STANDARD.md`.

The repository schema lives at:

```text
.kyrox/feature-contract.schema.json
```

Minimum conceptual shape:

```json
{
  "version": 1,
  "id": "xyz-sync",
  "title": "XYZ Sync",
  "feature_type": "scheduled_job",
  "owner": "fair-crm",
  "platform_reusability": "product_specific",
  "trigger": "scheduled",
  "tenant_scope": "organization",
  "user_facing": false,
  "permissions": {
    "required": false,
    "reason": "Scheduler-only internal trigger; no user authorization boundary.",
    "items": []
  },
  "frontend": {
    "required": false,
    "reason": "No user-facing route, page, menu or action.",
    "routes": [],
    "menu": false
  },
  "applicability": {
    "backend": { "status": "required" },
    "tenant_isolation": { "status": "required" },
    "frontend": { "status": "na", "reason": "No user-facing surface." },
    "runtime_authorization": { "status": "na", "reason": "No user/JWT trigger." }
  }
}
```

The actual repository schema may contain additional validation fields, but it must preserve the semantics in this document.

---

## 12. Contract consistency rules

CI should reject internally contradictory contracts.

Mandatory invariants include:

1. `permissions.required = false` -> permission item list is empty and a reason exists.
2. `permissions.required = true` -> at least one explicit permission exists.
3. SYSTEM permission -> `assignable = false`.
4. `frontend.required = false` -> no frontend routes/menu are declared and a reason exists.
5. `user_facing = true` -> frontend cannot be N/A unless the approved interface is explicitly non-browser and documented.
6. `tenant_scope = organization` with backend/data access -> tenant isolation cannot be N/A.
7. User-triggered protected operation -> runtime authorization cannot be N/A.
8. Frontend REQUIRED -> Visual QA cannot be N/A.
9. Any `N/A` applicability entry -> non-empty reason.
10. Tests cannot be N/A for changed executable behavior without a specifically approved canonical exception.

---

## 13. CI enforcement phases

Automation is introduced in layers so existing code is not falsely treated as compliant merely because a new checker exists.

### Phase A — contract correctness

CI validates:

- JSON syntax/schema,
- allowed feature types,
- REQUIRED/N/A validity,
- mandatory N/A reasons,
- permission scope/assignability consistency,
- tenant/frontend/user-trigger invariants.

### Phase B — change-to-contract matching

CI requires a Feature Contract for detectable material additions such as:

- a new backend module,
- a new permission family/code,
- other explicitly configured material feature paths.

The contract must declare the affected paths/permission codes.

### Phase C — code conformance

Static/test gates progressively verify what can be proven reliably, for example:

- permission registration,
- backend permission guards,
- tenant-scoped repository paths,
- frontend permission catalog,
- menu/route/action guards,
- UI governance,
- backend tests and frontend build.

No static regex may claim to prove a security property it cannot reliably prove. Properties requiring real runtime evidence remain runtime acceptance gates.

### Phase D — real runtime acceptance

Authorization-sensitive features still require the production-shaped path defined by `DEVELOPMENT_STANDARD.md`:

```text
real login/JWT
  -> resolved organization
  -> Core authorization
  -> Fair CRM API
  -> real feature result/UI
```

CI metadata does not replace this acceptance rule.

---

## 14. Direct pushes vs protected merges

A GitHub Actions workflow can fail after a direct push to `main`, but it cannot retroactively prevent that push by itself.

To make CI a true merge gate, the repository must use branch protection/rulesets that require the development-standard check before merging.

Until branch protection is configured, the rule is still binding and failed checks must be treated as a broken main state that requires immediate correction.

---

## 15. Example profiles

### Normal organization CRUD module

```text
Type: crud_module
DB: REQUIRED
Permissions: REQUIRED — read/create/update/archive
Backend/API: REQUIRED
Tenant isolation: REQUIRED
Frontend: REQUIRED
Menu/route/action guards: REQUIRED
Visual QA: REQUIRED
Runtime authorization: REQUIRED
```

### Backend-only organization service

```text
Type: backend_service
DB: As required by data model
Permissions: N/A — no user/API trigger
Backend: REQUIRED
Tenant isolation: REQUIRED
Frontend: N/A — no user surface
Audit: REQUIRED when side effects occur
Tests: REQUIRED
Runtime authorization: N/A — no user/JWT boundary
```

### Scheduled organization job

```text
Type: scheduled_job
Permissions: N/A — scheduler is trusted trigger
Backend: REQUIRED
Tenant isolation: REQUIRED
Frontend: N/A
Audit/logging: REQUIRED
Idempotency/retry behavior: REQUIRED by job design
Tests: REQUIRED
```

### User-triggered background operation

```text
Type: user_triggered_operation
Permission: fair_crm.xyz.execute
Permission scope: organization
Backend/API: REQUIRED
Tenant isolation: REQUIRED
Worker: REQUIRED
Frontend: REQUIRED when user starts it from UI
Button guard: REQUIRED (.execute)
Audit: REQUIRED
Runtime authorization: REQUIRED
```

### Super Admin system tool

```text
Type: system_admin
Permission scope: system
Assignable: false
OrganizationAdmin: denied
Super Admin: allowed
Backend/API: REQUIRED
Frontend: REQUIRED if tool has UI
Menu/route guard: REQUIRED
Runtime authorization: REQUIRED
```

---

## 16. Review rule

A reviewer or AI must reject both kinds of error:

### Missing required work

Example: organization background job queries all rows without tenant isolation.

### Invented non-required work

Example: scheduler-only service receives four fake CRUD permissions and an empty admin page only to satisfy a generic checklist.

Both are architecture defects.

---

# Golden applicability rule

**The standard is conditional, not optional.**

Feature classification determines which gates are REQUIRED. Every remaining gate is either completed or explicitly N/A with a valid architectural reason.

```text
Feature requirement
  -> Feature Profile
  -> Applicability Matrix
  -> REQUIRED / N/A gates
  -> implementation
  -> automated checks
  -> real runtime acceptance where applicable
```

The goal is not to make every feature look the same. The goal is to make every feature follow the same decision discipline.
