# FAIR CRM — Feature Delivery Extension

**Status:** Binding Fair CRM product extension  
**Canonical shared execution rule:** [../../standards/development/FEATURE_DELIVERY_STANDARD.md](../../standards/development/FEATURE_DELIVERY_STANDARD.md)

Fair CRM inherits the shared KYROX Feature Delivery Standard unchanged. This document contains only Fair CRM-specific ownership, permission, API, UI, Core-integration and deployment details. It must not redefine the shared delivery gates.

## Required reading order for Fair CRM work

1. [../../ecosystem/DOCUMENT_GOVERNANCE.md](../../ecosystem/DOCUMENT_GOVERNANCE.md)
2. [../../ecosystem/WORKFLOW.md](../../ecosystem/WORKFLOW.md)
3. [../../standards/README.md](../../standards/README.md) and all applicable shared standards
4. [CONSTITUTION.md](CONSTITUTION.md)
5. [PERMISSION_SCOPE_GOVERNANCE.md](PERMISSION_SCOPE_GOVERNANCE.md) when authorization changes
6. [frontend/FRONTEND_UI_MASTER_STANDARD.md](frontend/FRONTEND_UI_MASTER_STANDARD.md) when UI changes
7. Relevant Fair CRM/Core ADRs and integration contracts

If a material product decision is unclear or conflicting, stop before code and ask. Do not infer business behavior, permission scope, destructive semantics or workflow.

## Gate 0 — Fair CRM Delivery Contract additions

In addition to the shared Delivery Contract, Fair CRM work records when applicable:

```text
Tier / product priority classification
Fair CRM module/domain owner
Platform reusability decision (ADR-009)
Fair CRM permission codes and organization/system scope
OrganizationAdmin / Super Admin / default-role effects
crm_ tables / organization_id ownership
Core permission migration required?
Fair CRM API endpoints under /api/v1
Turkish UI route/menu/action surface
Core -> Fair CRM deployment dependency
Real users/roles used for acceptance
```

Applicability is governed by [FEATURE_APPLICABILITY_STANDARD.md](FEATURE_APPLICABILITY_STANDARD.md).

## Ownership / Core boundary

Fair CRM owns CRM domain behavior: customers, fairs, participations, activities, product operations, product UI, recipient/business selection and other CRM semantics.

KYROX Core owns reusable identity/auth/organization/permission platform behavior and other capabilities explicitly promoted to Core.

Hard Fair CRM boundary:

- no Core Python runtime imports,
- no shared SQLAlchemy sessions/databases,
- no cross-repository database foreign keys,
- Core consumed through public HTTP contracts,
- reusable-looking infrastructure is evaluated before duplicating it in Fair CRM.

Canonical cross-repo decision: [ADR-0002](../../ecosystem/decisions/0002-core-product-separation.md).  
Fair CRM product decision: [ADR-009](decisions/DECISIONS.md).

## Permission / role details

Fair CRM semantic permission family uses explicit actions such as:

```text
fair_crm.<module>.read
fair_crm.<module>.create
fair_crm.<module>.update
fair_crm.<module>.archive
fair_crm.<module>.delete
fair_crm.<module>.execute
fair_crm.<module>.approve
fair_crm.<module>.export
```

Only actions that exist are declared. Scope/assignability/default-role/Super Admin/OrganizationAdmin behavior is owned by [PERMISSION_SCOPE_GOVERNANCE.md](PERMISSION_SCOPE_GOVERNANCE.md) and Core governance, not repeated here.

UI visibility follows [CRUD & UI Authorization Standard](../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md).

## Fair CRM data / migration details

- Product tables use the `crm_` prefix.
- Organization-owned product records use `organization_id` where applicable.
- Core identifiers stored in Fair CRM are logical IDs, never cross-database FKs.
- Repository queries enforce organization scope; request-body organization IDs are not trusted as authorization context.
- Fair CRM migrations use Alembic and advance with new migrations rather than rewriting already-applied behavior.
- Core permission/scope/catalog changes are delivered through Core migrations and verified after migration.
- Restore acceptance applies `alembic upgrade head` before runtime acceptance.

Shared database rules under [../../standards/database/](../../standards/database/) remain authoritative where applicable.

## Core integration details

Fair CRM uses the existing Core integration boundary and public HTTP APIs. The real authenticated token and active organization context are forwarded according to the integration contract.

For authenticated production-shaped sessions:

- organization context comes from the authenticated/resolved organization,
- compile-time/test fallback organization IDs do not become the effective organization,
- `VITE_ORGANIZATION_ID` or equivalent fallbacks are development-only when explicitly approved,
- changing organization context requires permission state to be resolved/refreshed,
- authorization loading/connectivity failure fails closed.

Canonical Fair CRM integration notes: [integrations/INTEGRATION_WITH_CORE.md](integrations/INTEGRATION_WITH_CORE.md).  
Core contract: [../kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md](../kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md).

## Backend / API details

Fair CRM modules follow the shared layered backend standard and existing product module convention under `backend/app/modules/<module>/`.

Fair CRM API conventions include:

- base path `/api/v1`,
- JSON fields use `snake_case`,
- UUIDs serialize as strings,
- datetimes are timezone-aware ISO 8601,
- documented request/response models and errors,
- OpenAPI/Swagger verified after API changes,
- scalable list screens use server-side pagination/search/sort/filter rather than unbounded browser processing.

Protected operations map to the exact action permission and execute only after authentication, validated organization context, Core authorization, tenant-scoped product access and domain invariants all succeed.

## Audit / long-running operations

Use the existing Fair CRM audit adapter and canonical operations/job infrastructure. Do not create feature-local duplicate audit transport or a second operation/status engine.

Where the Constitution defines Core audit delivery as best-effort, temporary audit transport failure does not retroactively turn an otherwise successful product mutation into a business failure.

## Frontend details

For Fair CRM UI work:

- visible product copy is Turkish,
- use shared API/auth/header/error infrastructure,
- register/check permissions through the canonical effective-permission path,
- use [frontend/FRONTEND_UI_MASTER_STANDARD.md](frontend/FRONTEND_UI_MASTER_STANDARD.md),
- standard CRUD/action visibility follows the shared CRUD/UI authorization rule,
- role-name checks are not a substitute for effective permissions,
- direct routes are guarded as well as menu/action entry points,
- protected UI fails closed when permission state is unavailable.

Real rendered UI/Visual QA is required when UI is applicable. Product-specific breakpoints/component details live only in the UI master standard rather than being duplicated here.

## Fair CRM authorization acceptance

For protected user-facing work, prove applicable combinations with real authentication/runtime:

```text
Super Admin
OrganizationAdmin in own organization
restricted/default/custom organization role
user lacking mutation permission but possessing read
wrong organization / scope mismatch
user lacking module read permission
```

The production-shaped path is:

```text
real login/JWT
  -> active organization context
  -> Core authorization
  -> Fair CRM API
  -> Fair CRM UI/workflow/result
```

Mocks, bypasses and build success are implementation evidence, not final authorization acceptance.

## Fair CRM deployment dependency order

When Fair CRM depends on a new/changed Core permission or contract:

```text
1. Core change/migration ready
2. Deploy Core
3. Apply Core migrations
4. Verify permission/catalog/scope/role effects
5. Deploy Fair CRM backend
6. Apply Fair CRM migrations when required
7. Verify backend health/API/OpenAPI
8. Build/deploy Fair CRM frontend
9. Refresh/re-login authorization session when required
10. Run real-role smoke tests
11. Run final UI/workflow acceptance
```

When a step is N/A, record it explicitly rather than assuming it happened.

## Fair CRM Definition of Done additions

A Fair CRM delivery cannot be marked DONE while an applicable mismatch remains between:

```text
approved product requirement
= permission catalog/scope
= Core effective authorization
= organization data scope
= Fair CRM backend guard
= Fair CRM UI visibility
= real runtime behavior
```

Update canonical Platform documentation/status/changelog when the delivered truth changes. Do not recreate human-readable standards inside the `fair-crm` code repository.

## Related shared standards

- [Feature Delivery Standard](../../standards/development/FEATURE_DELIVERY_STANDARD.md)
- [Feature Applicability Standard](../../standards/development/FEATURE_APPLICABILITY_STANDARD.md)
- [Quality Gate Standard](../../standards/quality/QUALITY_GATE_STANDARD.md)
- [CRUD & UI Authorization Standard](../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md)
- [Backend Architecture Standards](../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md)
