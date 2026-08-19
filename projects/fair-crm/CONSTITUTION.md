# KYROX Fair CRM — Product Constitution

**Status:** Canonical Fair CRM product constitution  
**Scope:** FAIR CRM product/domain rules and implementation profile only

This document defines what is **specific and binding for FAIR CRM**. Reusable development, quality, backend and UI engineering rules are owned by KYROX shared standards and are not repeated here.

The pre-consolidation long-form constitution is preserved for history at [../../archive/fair-crm/CONSTITUTION_PRE_CONSOLIDATION.md](../../archive/fair-crm/CONSTITUTION_PRE_CONSOLIDATION.md).

## 1. Documentation hierarchy

Before material Fair CRM work:

1. Start from the KYROX Platform [README](../../README.md) / [AGENTS](../../AGENTS.md).
2. Read applicable [shared standards](../../standards/README.md).
3. Read this Fair CRM product constitution.
4. Read [PROJECT_STATUS.md](PROJECT_STATUS.md) for current delivered truth.
5. Read [ROADMAP.md](ROADMAP.md) for active/future product work.
6. Read relevant product ADRs and domain-specific documents.

Key execution documents:

- [DEVELOPMENT_STANDARD.md](DEVELOPMENT_STANDARD.md) — Fair CRM extension of shared feature delivery.
- [FEATURE_APPLICABILITY_STANDARD.md](FEATURE_APPLICABILITY_STANDARD.md) — Fair CRM feature-contract/runtime extension.
- [QUALITY_GATE_STANDARD.md](QUALITY_GATE_STANDARD.md) — Fair CRM repository quality extension.
- [PERMISSION_SCOPE_GOVERNANCE.md](PERMISSION_SCOPE_GOVERNANCE.md) — Fair CRM permission/catalog scope rules.
- [frontend/FRONTEND_UI_MASTER_STANDARD.md](frontend/FRONTEND_UI_MASTER_STANDARD.md) — Fair CRM UI implementation profile.
- [decisions/DECISIONS.md](decisions/DECISIONS.md) — Fair CRM ADR history.

No chat, sprint note or code-repo Markdown copy supersedes these canonical Platform documents.

## 2. Product mission

FAIR CRM is the first KYROX product. It manages fair/exhibition CRM relationships and the acquisition, review, enrichment and use of customer data.

Canonical long-term direction: [VISION.md](VISION.md).

### Product principles

1. **Business workflow first** — product priority follows approved business value/workflow, not technical convenience alone.
2. **Preview first** — external/imported data is reviewed before final CRM writes.
3. **Human approval for data decisions** — enrichment, verification, matching and AI/external suggestions do not silently overwrite CRM truth unless an explicit later product decision changes that rule.
4. **Conservative merge** — populated CRM data is not overwritten by empty/conflicting external values without approved merge semantics.
5. **Explicit workflows over hidden automation** — material state changes are visible and reviewable.
6. **Platform thinking** — reusable infrastructure is evaluated for Core; Fair CRM keeps CRM business semantics.

## 3. Product ownership boundary

### FAIR CRM owns

- customers and customer communication data,
- fairs and participations,
- contacts, activities, todos/follow-up work,
- CRM-specific import/data-integration and merge decisions,
- CRM-specific scraper/adapter orchestration,
- CRM-specific operations/automation handlers,
- quotations and cost-catalog product behavior,
- CRM-specific mail recipient/business orchestration,
- product UI and `crm_*` product database schema.

### KYROX Core owns

Reusable platform identity, authentication, organization/user/role governance, authorization/effective permissions and shared platform services explicitly owned by Core.

Canonical boundary: [ADR-0002](../../ecosystem/decisions/0002-core-product-separation.md).

### Hard repository rules

- Fair CRM is an independent service with its own database.
- No Core Python runtime imports in Fair CRM.
- No shared SQLAlchemy sessions/connection pools.
- No cross-repository database foreign keys.
- Product/Core integration uses public contracts.
- A reusable-looking capability is evaluated before being duplicated in Fair CRM.

## 4. Language and naming

- Backend code, DB schema, API paths/query params and permission codes: **English**.
- User-visible frontend labels/messages/confirmations/empty states: **Turkish**.
- Product database tables use the `crm_` prefix unless an accepted product architecture decision defines another owned system table family.
- Fair CRM permission codes use the `fair_crm.` namespace.

## 5. Tenant and authorization invariant

Organization-owned product data is always scoped using validated organization context.

```text
authenticated actor
  -> active organization context
  -> Core effective authorization
  -> organization-scoped Fair CRM access
  -> domain invariant
```

Rules:

- request-body organization IDs are not authorization context,
- cross-organization resource IDs cannot bypass tenant isolation,
- UI effective-permission visibility and backend authorization must agree,
- failure to resolve protected authorization fails closed,
- dev-bypass/fallback identity behavior is development-only and must not become production authority.

Permission-scope details: [PERMISSION_SCOPE_GOVERNANCE.md](PERMISSION_SCOPE_GOVERNANCE.md).  
Shared UI authorization semantics: [../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md](../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md).

## 6. Product architecture profile

FAIR CRM is an independent FastAPI product service with React/TypeScript frontend and its own PostgreSQL product database.

Backend product modules follow the shared layered backend standard using the established product shape:

```text
backend/app/modules/<module>/
  domain/
  application/
  infrastructure/
  api/
```

Fair CRM-specific conventions:

- API base path: `/api/v1`,
- health endpoint: `/health`,
- request/response JSON: `snake_case`,
- UUIDs serialize as strings,
- datetimes use timezone-aware ISO 8601,
- product routes use documented FastAPI response models/errors,
- scalable list APIs are server-side paginated/searched/sorted/filtered.

Shared backend rule: [../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md](../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md).

## 7. List / pagination product convention

Default list contract unless a module has an accepted exception:

```text
page       = 1 (1-based)
page_size  = 25 (1..100)
sort_order = asc|desc
search     = module-dependent free-text search
```

Sort fields are whitelist-mapped server-side; user input is never interpolated into SQL column expressions.

Frontend list screens use the Fair CRM shared table/list infrastructure rather than fetching a large unbounded dataset and performing page/sort/filter locally.

Exact Fair CRM component behavior is owned by [frontend/FRONTEND_UI_MASTER_STANDARD.md](frontend/FRONTEND_UI_MASTER_STANDARD.md).

## 8. Archive / restore convention

For aggregates explicitly designed as archivable, archive is distinct from hard delete.

Canonical Fair CRM behavior for such aggregates:

- archive records archived state and preserves prior status when required for restore,
- archived entities reject normal update mutations where the domain contract requires immutability,
- restore returns the aggregate to its approved prior/default state,
- frontend wording/permission must match the real action,
- hard delete is used only when the product explicitly defines physical deletion semantics.

Do not force archive/restore onto entities whose approved domain behavior is hard delete or another lifecycle.

## 9. External data / import invariant

FAIR CRM data-integration flows follow the product's preview/decision architecture:

```text
source
  -> analyze/normalize
  -> map
  -> match
  -> preview
  -> explicit decision
  -> apply
  -> report
```

External data does not bypass the approved decision/merge path into CRM truth.

Canonical import architecture and merge behavior:

- [import/IMPORT_ARCHITECTURE.md](import/IMPORT_ARCHITECTURE.md)
- [import/MERGE_RULES.md](import/MERGE_RULES.md)
- relevant import ADRs in [decisions/DECISIONS.md](decisions/DECISIONS.md)

## 10. Long-running product operations

FAIR CRM automation types/handlers remain product-owned when they contain CRM business meaning. Reuse the existing product operation/job infrastructure rather than inventing feature-local lifecycle engines.

A future extraction of genuinely generic Operation Engine infrastructure to Core requires an explicit ownership decision; it is not implied by this constitution.

Current planned pause-vs-cancel behavior is tracked in [ROADMAP.md](ROADMAP.md).

## 11. Mail product boundary

FAIR CRM owns CRM-specific recipient resolution, templates/business context, exclusions/communication rules and CRM activity/history effects.

Whether provider-neutral delivery infrastructure should be promoted to Core remains an explicit deferred ownership decision. Do not duplicate/move it silently.

Related product backlog: [ROADMAP.md](ROADMAP.md) and `backlog/` specifications.

## 12. Frontend product profile

Fair CRM frontend uses the single product design system defined in [frontend/FRONTEND_UI_MASTER_STANDARD.md](frontend/FRONTEND_UI_MASTER_STANDARD.md).

Product-specific facts include:

- visible UI copy is Turkish,
- shared primitives/tokens live in the Fair CRM frontend implementation,
- standard list entry uses the Fair CRM UniversalDataTable path,
- Fair CRM form/dirty-state implementation and canonical confirmation copy live in the UI master,
- supported breakpoints/component names remain product implementation details.

Reusable UI principles: [../../standards/ui/UI_FOUNDATION_STANDARD.md](../../standards/ui/UI_FOUNDATION_STANDARD.md).

## 13. Database / restore safety

Fair CRM development/operational data may be valuable. Destructive data/import experiments require the applicable verified backup safety process.

A restored database reflects the schema at backup time. Apply current Alembic migrations before accepting the restored runtime.

Operational details belong in [ops/](ops/) and shared database standards, not repeated throughout product docs.

## 14. Product Definition of Done

Fair CRM-specific completion requires the shared feature-delivery/quality gates plus applicable product evidence:

- product/tenant ownership correct,
- Fair CRM/Core boundary preserved,
- permissions and effective UI behavior agree,
- `crm_*` data/migrations correct where applicable,
- product API contract and real runtime verified,
- Turkish UI and Fair CRM UI master followed when frontend applies,
- external-data flows preserve preview/human-decision invariants where applicable,
- product status/changelog/roadmap updated in the correct document when truth or planning changed.

Canonical shared DoD: [../../standards/development/FEATURE_DELIVERY_STANDARD.md](../../standards/development/FEATURE_DELIVERY_STANDARD.md).

## 15. Change rule

Change this constitution only when a **Fair CRM-specific product invariant or product implementation profile** changes.

If a rule would apply unchanged to another KYROX product, update the appropriate shared standard instead of adding it here.
