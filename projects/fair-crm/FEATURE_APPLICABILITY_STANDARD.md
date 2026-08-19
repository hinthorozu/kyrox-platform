# FAIR CRM — Feature Applicability Extension

**Status:** Binding Fair CRM extension  
**Canonical shared rule:** [../../standards/development/FEATURE_APPLICABILITY_STANDARD.md](../../standards/development/FEATURE_APPLICABILITY_STANDARD.md)

Fair CRM **inherits the shared KYROX Feature Applicability Standard unchanged**. This file contains only Fair CRM-specific contract paths, runtime topology and naming details. It must not redefine REQUIRED/N/A semantics, feature classification, tenant-isolation independence or the shared review rules.

## 1. Fair CRM feature contract location

For material Fair CRM features, the implementation repository may carry machine-readable governance metadata at:

```text
.kyrox/features/<feature-id>.json
```

Schema:

```text
.kyrox/feature-contract.schema.json
```

These JSON files are CI/governance metadata, **not human-readable sources of truth**. Human/AI rules remain in `kyrox-platform`.

## 2. Fair CRM contract ownership fields

A Fair CRM product feature normally declares:

```text
owner: fair-crm
```

Platform reusability must be classified before implementation. If the capability is truly reusable platform infrastructure, follow the ecosystem ownership/ADR flow rather than implementing a second shared capability in Fair CRM.

## 3. Fair CRM permission examples

Permission semantics follow the shared CRUD/UI standard and Fair CRM permission-scope governance.

Examples:

```text
fair_crm.<module>.read
fair_crm.<module>.create
fair_crm.<module>.update
fair_crm.<module>.archive
fair_crm.<module>.delete
fair_crm.<module>.execute
```

Only actions that actually exist in the approved product behavior are declared. Background/scheduled work does not receive fake CRUD permissions.

Canonical permission scope rules: [PERMISSION_SCOPE_GOVERNANCE.md](PERMISSION_SCOPE_GOVERNANCE.md).  
Canonical UI visibility rules: [../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md](../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md).

## 4. Fair CRM tenant scope

Organization-owned Fair CRM data requires tenant isolation even when end-user permissions are N/A for an internal/scheduled path. Trusted jobs/workers carry validated organization/resource context; they do not become cross-tenant merely because no browser user triggered them.

## 5. Fair CRM frontend applicability

When a feature has Fair CRM UI, applicable menu/route/action visibility follows **effective permissions**, never role-name assumptions. Frontend-specific implementation and visual rules come from [frontend/FRONTEND_UI_MASTER_STANDARD.md](frontend/FRONTEND_UI_MASTER_STANDARD.md).

When the approved feature has no user-facing surface, frontend/menu/route/forms/visual QA may be N/A with a concrete reason as defined by the shared applicability standard.

## 6. Real authorization acceptance path

For authorization-sensitive Fair CRM user flows, metadata/static checks do not replace the production-shaped path:

```text
real login/JWT
  -> active organization context
  -> Core authorization
  -> Fair CRM API
  -> real product result / UI
```

The exact integration contract is [integrations/INTEGRATION_WITH_CORE.md](integrations/INTEGRATION_WITH_CORE.md) plus the Core [Product Integration Guide](../kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md).

## 7. Fair CRM CI contract invariants

Fair CRM tooling may enforce additional schema/path details, but it must preserve the shared invariants. In particular:

- N/A requires a reason,
- user-triggered protected work requires runtime authorization evidence,
- organization-scoped backend/data work cannot mark tenant isolation N/A,
- frontend-required work cannot silently omit applicable UI/visual checks,
- permissions marked not required cannot carry hidden permission items,
- system-scoped permissions follow Fair CRM/Core scope governance.

## 8. Execution order

The delivery sequence for Fair CRM remains [DEVELOPMENT_STANDARD.md](DEVELOPMENT_STANDARD.md). Applicability decides which gates in that sequence are REQUIRED or N/A; it never weakens the shared execution or quality rules.
