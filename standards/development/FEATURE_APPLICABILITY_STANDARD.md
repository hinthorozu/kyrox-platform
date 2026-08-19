# KYROX Feature Applicability Standard

**Status:** Canonical shared KYROX standard  
**Scope:** Material feature delivery in KYROX products and reusable platform capabilities  
**Audience:** Human developers, AI agents, reviewers and quality tooling

This standard answers one question:

> **Which delivery gates actually apply to this feature?**

Not every feature is CRUD and not every feature has a frontend. Required work must never be skipped, and non-applicable work must never be invented merely to satisfy a generic checklist.

## 1. Decide applicability before implementation

Every material feature begins with an explicit Feature Profile as part of its delivery/design contract.

Canonical feature types:

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

Use `other` only with an explicit description. Do not select a misleading profile to avoid a product decision.

## 2. Gate states are REQUIRED or N/A

Every governed delivery area is one of:

```text
REQUIRED
N/A
```

`OPTIONAL` is not a gate state. Product scope decides whether a capability is in the delivery; after that decision it is REQUIRED or N/A.

Every `N/A` requires an architectural reason. `N/A` is not a bypass for inconvenient or failing work.

Valid example:

```text
Frontend: N/A
Reason: Scheduled service has no user-facing route, page, menu or action.
```

## 3. Canonical applicability areas

Products may add product-specific areas, but these concepts must retain their meaning:

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

## 4. Default applicability matrix

Defaults guide the delivery contract; explicit requirements may override them with a reason.

| Feature type | DB / migration | Permissions | Backend / API | Tenant isolation | Frontend / UI | UI guards | Audit | Tests | Runtime auth |
|---|---|---|---|---|---|---|---|---|---|
| `crud_module` | REQUIRED as needed by model | REQUIRED for protected actions | REQUIRED | REQUIRED when scoped | REQUIRED | REQUIRED | REQUIRED for meaningful mutations | REQUIRED | REQUIRED when protected |
| `read_only_module` | As needed | `read` when protected | REQUIRED | REQUIRED when scoped | REQUIRED when user-facing | REQUIRED when protected | Usually N/A | REQUIRED | REQUIRED when protected |
| `backend_service` | As needed | N/A unless user/API-triggered | REQUIRED | REQUIRED when scoped | N/A | N/A | REQUIRED for meaningful side effects | REQUIRED | N/A unless user/API-triggered |
| `background_job` | As needed | Permission on user trigger if present | REQUIRED | REQUIRED when scoped | N/A unless status/control UI exists | As applicable | REQUIRED | REQUIRED | As applicable |
| `scheduled_job` | As needed | N/A for scheduler trigger | REQUIRED | REQUIRED when scoped | N/A unless admin/status UI exists | As applicable | REQUIRED | REQUIRED | N/A for scheduler path |
| `user_triggered_operation` | As needed | REQUIRED; normally semantic action such as `execute` | REQUIRED | REQUIRED when scoped | REQUIRED when trigger is UI | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| `integration_adapter` | As needed | Semantic permissions only for exposed management/execution | REQUIRED | REQUIRED when scoped | N/A unless configurable by users | As applicable | REQUIRED for state/external actions | REQUIRED | As applicable |
| `system_admin` | As needed | SYSTEM/platform permission or explicit system guard | REQUIRED | Explicit | REQUIRED if user-facing | REQUIRED if UI exists | REQUIRED | REQUIRED | REQUIRED |
| `core_platform_capability` | As needed | As designed | REQUIRED in Core | According to platform contract | N/A unless consumed through product UI | As applicable | REQUIRED where security/side effects matter | REQUIRED | REQUIRED when authorization-sensitive |
| `ui_only` | N/A | Existing effective-permission model | N/A unless API changes | N/A | REQUIRED | REQUIRED when protected | N/A | REQUIRED | Existing backend authorization must remain valid |
| `maintenance` | As needed | Usually N/A | As needed | As needed | As needed | As needed | As needed | REQUIRED for changed behavior | As applicable |
| `other` | Explicit | Explicit | Explicit | Explicit | Explicit | Explicit | Explicit | REQUIRED | Explicit |

## 5. CRUD permissions are conditional, not universal

Do not create fake CRUD permissions for a service that does not expose CRUD behavior.

A user-triggered operation may need only a semantic action such as `.execute`. A scheduler-only internal service may have end-user permissions N/A while still requiring tenant isolation, trusted triggering, idempotency, audit/logging and tests.

## 6. Trigger authorization and internal execution are different

### User-triggered work

```text
User
  -> authenticated entry point
  -> semantic permission check
  -> enqueue/execute approved work
  -> worker/service operates on validated scoped context
```

### Scheduled work

```text
Trusted scheduler
  -> worker/service
  -> scoped processing
```

### Internal/event work

```text
Approved internal trigger
  -> validated scoped payload
  -> service/job
```

Do not invent an end-user role for internal execution. Protect the trusted trigger according to its architecture.

## 7. Tenant isolation is independent from user permissions

`permissions = N/A` does not imply `tenant_isolation = N/A`.

Any service processing organization/tenant-owned data requires an explicit scope strategy. Cross-tenant processing is a deliberate platform/system design, never an accidental consequence of running in a worker.

## 8. Frontend applicability

Frontend is REQUIRED only when the approved feature has a user-facing surface. When frontend is N/A, menu, route guards, forms, visual QA and frontend tests are normally N/A for the same reason.

If a backend capability later gains UI, that is a material change and applicability must be reclassified.

## 9. Permission-aware UI applicability

For a protected user-facing feature:

- read/module access controls relevant navigation and route entry,
- actions map to their exact effective permissions,
- direct URLs cannot bypass authorization-aware rendering,
- backend authorization remains mandatory.

Canonical UI semantics: [../ui/CRUD_UI_AUTHORIZATION_STANDARD.md](../ui/CRUD_UI_AUTHORIZATION_STANDARD.md).

## 10. System capabilities

A system-only capability may have a UI while remaining unavailable to organization roles. Its scope and assignability must follow the platform authorization model. CRUD-shaped UI does not turn a system capability into an organization capability.

## 11. Machine-readable feature contracts

A product may keep a machine-readable feature contract in its implementation repository. That contract is governance/CI metadata, not a second human-readable source of truth.

Product-specific documentation defines exact paths/schema fields while preserving this standard's semantics.

At minimum, contract tooling should reject contradictions such as:

1. permissions not required but permission items present,
2. permissions required but no explicit permission declared,
3. system-only permission declared assignable contrary to platform policy,
4. frontend not required but routes/menu declared,
5. organization-scoped backend data with tenant isolation marked N/A,
6. user-triggered protected operation with runtime authorization marked N/A,
7. frontend-required feature with visual QA silently omitted,
8. N/A gate without a reason,
9. executable behavior changed while all relevant tests are marked N/A without an approved exception.

## 12. CI enforcement maturity

Automation may be introduced in layers:

1. **Contract correctness** — schema, allowed profiles, REQUIRED/N/A and invariants.
2. **Change-to-contract matching** — material feature changes require an applicable contract where the product uses this mechanism.
3. **Code conformance** — static/tests verify properties that can be proven reliably.
4. **Real runtime acceptance** — authorization/runtime-sensitive behavior is verified through the production-shaped integration path.

Static checks must not claim to prove security properties they cannot reliably establish.

## 13. Review rule

Reject both failure modes:

- **missing required work** — for example, a scoped background job queries data without tenant isolation;
- **invented non-required work** — for example, a scheduler-only service receives fake CRUD permissions and an empty admin page only to satisfy a checklist.

## Golden applicability rule

**The standard is conditional, not optional.**

```text
Requirement
  -> Feature Profile
  -> Applicability Matrix
  -> REQUIRED / N/A gates with reasons
  -> implementation
  -> automated evidence
  -> runtime acceptance where applicable
```

Product extensions may define exact feature-contract paths, product permission names and runtime topology; they must not redefine these shared semantics.
