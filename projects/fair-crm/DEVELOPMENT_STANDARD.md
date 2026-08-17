# FAIR CRM / KYROX — Feature Delivery Development Standard

**Status:** Canonical / binding execution standard  
**Scope:** New Fair CRM modules, features, CRUD flows, permissions, Core integration, backend, frontend, UI, migrations, tests and deployment  
**Audience:** Human developers, AI coding agents and reviewers

This document defines the **mandatory execution order** for delivering a Fair CRM feature safely and consistently. It does not replace the detailed canonical rules owned by the Constitution, UI Master Standard, Permission Scope Governance, backend architecture standards, ADRs or Core integration contract. Instead, it defines **when each rule must be applied, what artifact must exist, and which gate must pass before work may continue**.

The objective is deterministic delivery: the same kind of feature must be designed, implemented, authorized, rendered, tested and deployed through the same sequence every time.

---

## 0. Precedence and canonical sources

Before implementation, apply these sources in this order:

1. `ecosystem/DOCUMENT_GOVERNANCE.md` — documentation ownership / SSoT.
2. `ecosystem/WORKFLOW.md` — ambiguity gate, human/AI execution, runtime acceptance.
3. `projects/fair-crm/CONSTITUTION.md` — Fair CRM architecture, module, API, testing and DoD rules.
4. `projects/fair-crm/PERMISSION_SCOPE_GOVERNANCE.md` — ORGANIZATION vs SYSTEM security boundary.
5. `projects/fair-crm/frontend/FRONTEND_UI_MASTER_STANDARD.md` — binding frontend/UI rules.
6. `standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md` — layered backend architecture.
7. Relevant Fair CRM / Core ADRs and integration contracts.
8. Explicit user-approved task requirements, provided they do not silently contradict an unchanged canonical rule.

### Hard stop

**No code is written until Gate 0 is complete.**

If a required product decision is missing or conflicting, stop and ask the product owner. Do not infer business behavior, permission scope, destructive semantics, role behavior or UI workflow from common practice.

---

# PART I — DESIGN CONTRACT

## Gate 0 — Create the Delivery Contract

Every new module or material feature starts with a short Delivery Contract. It may live in the task/PR/chat while work is active; permanent decisions belong in the canonical platform documentation according to Document Governance.

The Delivery Contract must answer all applicable fields:

```text
Feature / module:
Business purpose:
Owning repository:
Tier:
Product-specific or platform-generic:
Organization-scoped data?:
Permission scope per action: ORGANIZATION / SYSTEM
Permission codes:
Default-role/template impact:
Super Admin behavior:
OrganizationAdmin behavior:
Database tables / columns:
Migration required?:
API endpoints:
Audit events:
Frontend route(s):
Menu / navigation entry:
Read/create/update/archive/delete/execute UI actions:
List/search/sort/filter/pagination requirements:
Responsive / modal / form / table requirements:
Tests required:
Runtime acceptance users/roles:
Deployment order:
```

A field may be `N/A`, but it may not be silently omitted when it is applicable.

### Gate 0 PASS criteria

- [ ] Requirement is unambiguous.
- [ ] Owning repository is explicit.
- [ ] ADR-009 platform-reusability decision is explicit.
- [ ] Tier is classified where required by the Constitution.
- [ ] Permission scope is decided for every new permission.
- [ ] Data ownership / tenant scope is explicit.
- [ ] Destructive behavior is explicit: archive/restore vs hard delete.
- [ ] UI surface and user flow are explicit.
- [ ] Acceptance roles/users are defined.

If any checkbox cannot be answered, **do not start implementation**.

---

## Gate 1 — Repository ownership and platform boundary

Apply ADR-009 before choosing where code lives.

### Fair CRM owns

CRM-specific domain behavior and product data, for example customers, fairs, participations, activities, product operations and product UI.

### KYROX Core owns

Reusable platform capabilities such as authentication, RBAC, organization identity, permission catalog, audit platform behavior, platform settings, generic jobs and other cross-product primitives.

### Hard rules

- Fair CRM never imports Core Python packages.
- Fair CRM and Core never share SQLAlchemy sessions.
- No cross-repository database foreign keys.
- Fair CRM communicates with Core only through public HTTP contracts.
- If the requested capability is platform-generic, stop Fair CRM implementation until ownership is approved.

---

## Gate 2 — Permission and role contract

Permission design happens **before backend routes and before UI**.

### 2.1 Permission naming

Use semantic action identifiers:

```text
fair_crm.<module>.read
fair_crm.<module>.create
fair_crm.<module>.update
```

For destructive behavior, match the real domain action:

```text
fair_crm.<module>.archive   # archivable aggregates
fair_crm.<module>.delete    # only when real hard-delete semantics are approved
```

Special operations use the actual action:

```text
fair_crm.<module>.execute
fair_crm.<module>.approve
fair_crm.<module>.export
```

Do not use vague umbrella permissions such as `full_access` to avoid defining actual actions.

### 2.2 Permission scope

Every permission must explicitly be one of:

```text
organization
system
```

Never infer scope from the slug, route, module name, `admin` wording or UI location.

#### ORGANIZATION

- Action is limited to the active `organization_id`.
- May be assigned to organization roles when assignable.
- OrganizationAdmin may receive it according to Core governance.
- Custom organization roles may receive it when assignable.
- Non-Super-Admins exercise it only through an active role assignment in the same organization.

#### SYSTEM

- Effective access is Super Admin only under the current platform model.
- `is_assignable = false`.
- Never granted to OrganizationAdmin.
- Never granted to organization default-role derivatives or custom organization roles.
- Must not appear in organization role-management permission lists.

### 2.3 Super Admin

Super Admin authority comes from:

```text
identity_users.is_super_admin = true
```

It is not implemented as an organization role and does not require `identity_role_permissions` rows. The central Super Admin bypass remains the first authorization rule.

### 2.4 OrganizationAdmin

OrganizationAdmin is a protected global organization role. Its role definition is global; organization scope comes from the active `identity_user_roles.organization_id` assignment.

Rules:

- Receives organization-scoped permissions according to Core governance.
- Never receives system-scoped permissions.
- Acts only inside its assigned organization.
- Never creates or grants Super Admin access.

### 2.5 Default templates and custom roles

For each new ORGANIZATION permission, explicitly evaluate its behavior for the canonical default templates and organization custom roles. Do not invent template semantics; follow the current Core role-template governance. If the expected template inclusion is unclear, stop and ask.

### Gate 2 PASS criteria

- [ ] Every action has an explicit permission code or documented reason why no permission is required.
- [ ] Every new permission has explicit `permission_scope`.
- [ ] SYSTEM permissions are non-assignable.
- [ ] OrganizationAdmin behavior is defined.
- [ ] Default template impact is evaluated.
- [ ] Super Admin relies on central bypass, not a fake role grant.

---

# PART II — DATA AND CORE AUTHORIZATION

## Gate 3 — Database and migration contract

### Fair CRM product tables

- Product tables use the `crm_` prefix.
- Organization-owned records carry `organization_id` as the tenant key where applicable.
- Core IDs stored by Fair CRM are logical identifiers, not cross-database foreign keys.
- Repository queries must enforce organization scope; request-body organization IDs are never trusted as authorization context.

### Migration rules

- Use Alembic.
- Never edit an already-applied migration to change production behavior; create a new migration.
- Permission scope changes require a new Core migration.
- Permission/catalog seeds must be repeat-safe/idempotent where the existing pattern requires it.
- New permission migrations set `permission_scope` explicitly; do not rely on a database default as the design decision.
- After a database restore, apply `alembic upgrade head` before runtime acceptance.
- Before destructive migration/import experiments on valuable dev data, follow the canonical backup safety rule.

### Permission migration acceptance

After Core migration, verify the resulting state rather than assuming seed logic worked:

- permission exists,
- lifecycle is active,
- scope is correct,
- assignability is correct,
- OrganizationAdmin has the expected ORGANIZATION permission,
- no organization role has an unintended SYSTEM permission.

---

## Gate 4 — Core integration contract

When Fair CRM requires authorization or another Core capability:

- use the existing port/adapter boundary under `integrations/kyrox_core/`,
- call Core through HTTP,
- do not duplicate Core authorization logic in Fair CRM,
- do not authorize by role-name checks inside product business code when a permission check exists,
- forward the real authenticated access token and current organization context.

### Organization context hard rule

For an authenticated non-dev session, `X-Organization-Id` must come from the authenticated session's resolved organization context. A compile-time/test fallback organization ID must **never** become the effective production organization for a logged-in user.

`VITE_ORGANIZATION_ID` or equivalent fallback values are allowed only for their explicitly approved development/bypass purpose.

When the effective organization changes, permission state must be resolved/refreshed for that organization.

### Fail-closed rule

If authorization state cannot be resolved, protected actions fail closed. Connectivity or permission-loading failure must never grant access.

---

# PART III — BACKEND IMPLEMENTATION

## Gate 5 — Backend module structure

New Fair CRM modules follow the canonical layered module structure:

```text
backend/app/modules/<module>/
  domain/
  application/
  infrastructure/
  api/
```

### Domain

- Pure business rules and invariants.
- No FastAPI, SQLAlchemy, HTTP request/response or infrastructure imports.
- Domain exceptions and value objects live here when appropriate.

### Application

- One cohesive use case per business operation.
- Orchestrates domain and ports.
- Receives validated application inputs; does not construct HTTP responses.
- Authorization/audit dependencies enter through ports/adapters, not hidden globals.

### Infrastructure

- SQLAlchemy models/repositories and external technology implementations.
- Tenant filters are mandatory for organization-owned data.
- Sort fields map to a fixed whitelist; never interpolate arbitrary user input into SQL.

### API

- Thin FastAPI transport only.
- Request/response schemas, dependency wiring and error mapping.
- No business rules and no direct ad-hoc SQLAlchemy queries in route handlers.

### Cross-module rule

Modules communicate through application/domain contracts. Do not import another module's infrastructure implementation to save time.

---

## Gate 6 — Backend authorization mapping

Every protected API operation maps to the permission that represents that exact action.

Typical mapping:

```text
GET    /resources                -> <module>.read
GET    /resources/{id}           -> <module>.read
POST   /resources                -> <module>.create
PATCH  /resources/{id}           -> <module>.update
DELETE /resources/{id}           -> <module>.archive or <module>.delete according to approved semantics
POST   /resources/{id}/restore   -> canonical archive/restore permission for that module
POST   /resources/{id}/execute   -> <module>.execute
```

### Security layering

A request is allowed only when all applicable layers succeed:

```text
Authenticated user
  -> current organization context
  -> Core authorization decision
  -> Fair CRM organization-scoped query/mutation
  -> domain invariants
```

Permission answers **what** the user may do. Organization scoping answers **which tenant's data** they may do it to. Neither replaces the other.

### Wrong organization behavior

Product resource lookup must not leak cross-tenant existence. Follow the canonical API behavior for wrong-org resources (normally not-found semantics for product data) while authorization itself remains 401/403 as defined by the platform contract.

---

## Gate 7 — API contract

Before frontend implementation, the backend contract must be stable enough to consume.

### Standard requirements

- Base path: `/api/v1`.
- Request/response JSON: `snake_case`.
- UUIDs serialized as strings.
- Datetimes: timezone-aware ISO 8601.
- Create: `201` with resource body.
- Update/archive/restore: canonical response body/status from the Constitution.
- Errors use the shared `{ "detail": "..." }` convention where applicable.
- `response_model`, tags and documented error responses are present.
- Swagger/OpenAPI is verified on the running backend after changes.

### List endpoints

New list screens use server-side behavior:

- pagination,
- search where applicable,
- sorting,
- filtering or documented exception,
- total count / page metadata,
- organization scoping.

Do not fetch an unbounded dataset and then `sort()`, `filter()` or `slice()` it in the browser to simulate server behavior.

---

## Gate 8 — Audit and side effects

For mutations and sensitive operations, define audit behavior before completion.

Use the existing audit port/adapter. Do not create feature-local audit transport.

Fair CRM audit writes remain best-effort where the Constitution defines them as best-effort: a successful product mutation must not be turned into a business failure solely because Core audit transport is temporarily unavailable.

Background jobs, import, export, execution and other long-running behavior must use the existing canonical job/operation standards rather than inventing a second status engine.

---

# PART IV — FRONTEND AND UI

## Gate 9 — Frontend data layer

Implement frontend in this order unless an existing module pattern requires a small equivalent variation:

```text
types
  -> api client
  -> labels
  -> permission helpers/catalog
  -> reusable/domain components
  -> page/route
```

Rules:

- All visible UI copy is Turkish.
- API calls use the shared API client/header construction.
- Errors use `ApiError` and centralized/module label strings.
- Do not embed raw fetch/header/auth logic independently in pages when shared API infrastructure exists.
- Permission codes used by the UI are registered in the canonical frontend permission catalog/check path.

---

## Gate 10 — Permission-aware UI contract

Frontend permission behavior is mandatory and separate from backend security.

### 10.1 Navigation

A module/menu entry is rendered only when the current effective permission set allows the capability needed to open it, normally the module's `read` permission.

Example:

```text
fair_crm.xyz.read present   -> XYZ menu may render
fair_crm.xyz.read absent    -> XYZ menu does not render
```

### 10.2 Routes / deep links

Hiding a menu is not sufficient. Direct navigation to a protected route must be permission-guarded before rendering the protected screen.

If the permission is absent, the protected page must not render its data/actions. Use the project's shared unauthorized/redirect behavior when available; do not create page-local authorization logic for each route.

### 10.3 Actions

Page actions map to their exact permissions:

```text
read       -> list/detail visibility
create     -> new/create action
update     -> edit/save mutation action
archive    -> archive/restore action when that is the canonical module permission
delete     -> hard-delete action only when approved
execute    -> execute/start/retry/cancel actions according to the operation contract
```

Unauthorized actions are not rendered by default. A deliberately visible-but-disabled restricted action requires an explicit product/UI decision.

### 10.4 Do not authorize by role name in normal product UI

The UI should consume effective permission decisions, not infer capability from strings such as `OrganizationAdmin` or `ReadUser`. Role identity checks are reserved for role-governance screens where the role itself is the subject.

### 10.5 System capabilities

System-scope capabilities naturally disappear for organization users because Core denies those permissions; Super Admin receives them through the central bypass. Do not grant or fake system access in the frontend.

### 10.6 Permission load failure

Fail closed: missing/failed permission state does not reveal protected menus or actions.

### 10.7 Acceptance invariant

If UI state says an action is available but the same real user/JWT receives a Core/product `403` for that action, the feature is **not accepted**. Fix the permission catalog/session/role/backend mismatch; do not treat repeated 403 as normal UX.

---

## Gate 11 — UI Design System contract

Before any production UI change, read `frontend/FRONTEND_UI_MASTER_STANDARD.md`.

The following are mandatory outcomes; detailed implementation remains owned by the UI Master Standard:

- one design system only,
- existing shared primitives reused,
- no second/ad-hoc button, modal, table, form-control, alert, loading or navigation family,
- no raw controls when a shared primitive exists,
- design tokens instead of page-local magic values,
- `PageShell -> PageHeader -> Toolbar/Filters -> Content` page structure,
- `UniversalDataTable` / responsive table path for standard lists,
- server-side table state and URL synchronization,
- shared form primitives,
- dirty-form protection on create/edit/update flows,
- loading vs empty vs error states correctly separated,
- silent background refresh when existing successful data is already visible,
- accessibility semantics and focus behavior,
- responsive behavior from minimum supported width through ultrawide,
- real Visual QA, not build-only acceptance.

### Required viewport evidence

At minimum, UI work is smoke-checked at:

```text
390
768
1024
1440
ultrawide
```

Breakpoint boundaries and table-container resize behavior are checked where relevant.

### Visual PASS rule

Build success, no overflow, inventory gate success or shared-component usage alone does not prove UI quality. Alignment, spacing, hierarchy, density, readability and action placement must pass real rendered review.

---

## Gate 12 — Forms, modals and destructive actions

### Forms

- Use canonical shared form controls and layout primitives.
- Create/edit/update flows report dirty state.
- Clean exit requires no confirmation.
- Dirty exit uses the canonical shared dirty-form confirmation.
- Failed save does not clear dirty state.
- Successful save resets baseline/dirty state.

### Modals / dialogs

- Use shared `Modal`, `FormModal`, `ConfirmDialog` or `Drawer` according to the UI Master Standard.
- No page-local backdrop/focus/footer implementation.
- Critical actions remain reachable on mobile.

### Destructive operations

- Archive/delete/restore behavior must match the approved domain contract and permission.
- Confirmation UI uses shared confirmation patterns.
- The frontend must not relabel hard delete as archive or vice versa.

---

# PART V — TESTING AND ACCEPTANCE

## Gate 13 — Backend test matrix

All applicable layers are tested:

### Domain

- invariants,
- state transitions,
- invalid transitions,
- archive/restore rules where applicable.

### Application

- use-case success,
- expected failures,
- fake repository/port behavior,
- authorization/audit orchestration where owned by the use case.

### Infrastructure

- persistence,
- organization filters,
- sort/filter mapping,
- migration-dependent behavior.

### API

- request/response contract,
- 401 unauthenticated,
- 403 unauthorized,
- correct permission success,
- wrong-organization isolation,
- validation and not-found cases.

---

## Gate 14 — Authorization acceptance matrix

A feature with permissions is not complete until the **real runtime** path is proven with real JWT authorization, not only mocks or dev bypass.

Minimum applicable matrix:

```text
Super Admin
  ORGANIZATION action -> allowed
  SYSTEM action       -> allowed

OrganizationAdmin
  allowed ORGANIZATION action in own org -> allowed
  SYSTEM action                         -> denied
  other organization                    -> denied

Restricted/default/custom role
  granted action     -> allowed
  ungranted action   -> denied

No module read permission
  menu               -> hidden
  direct route       -> denied/not rendered
  API                -> 403
```

For create/update/archive/delete/execute, test at least one role that has `read` but does **not** have the mutation permission.

### Production-shaped acceptance path

```text
real login/JWT
  -> resolved organization context
  -> Core authorization check
  -> Fair CRM API
  -> UI/workflow
  -> real result/data
```

Mocks, `AllowAllAuthorization`, dev bypass and frontend build are implementation aids, not final authorization evidence.

---

## Gate 15 — Frontend verification

Applicable checks:

- [ ] `npm run build` passes.
- [ ] Relevant frontend tests pass.
- [ ] UI inventory/governance gates pass where applicable.
- [ ] Real route renders.
- [ ] Real API data loads.
- [ ] Permission-controlled menu is correct.
- [ ] Direct URL guard is correct.
- [ ] Create/update/archive/delete/execute controls match permissions.
- [ ] Initial loading state is visible while data is pending.
- [ ] Empty state appears only after successful empty response.
- [ ] Error state does not become infinite loading.
- [ ] Background refresh does not blank successful data.
- [ ] Dirty-form flow passes.
- [ ] Responsive / Visual QA passes.
- [ ] Keyboard/focus/accessibility behavior has no regression.

---

# PART VI — RUNTIME, DEPLOYMENT AND COMPLETION

## Gate 16 — Runtime synchronization

Never mark a change complete against stale services.

### Backend/Core changes

- apply pending migrations,
- restart affected service,
- verify correct environment,
- verify OpenAPI/Swagger when API changed,
- make at least one real request through the changed path.

### Frontend changes

- restart/rebuild the active frontend runtime,
- verify the active port/build,
- verify the affected route,
- inspect browser Network behavior for the expected endpoint and organization context.

---

## Gate 17 — Deployment order

When a Fair CRM feature introduces or changes Core permissions, the default deployment order is:

```text
1. Core code / permission migration ready
2. Deploy Core
3. Run Core alembic upgrade head
4. Verify permission catalog, scope, assignability and role effects
5. Deploy Fair CRM backend
6. Run Fair CRM alembic upgrade head when required
7. Verify backend health / Swagger / live API
8. Deploy/build Fair CRM frontend
9. Refresh/re-login authorization session when required
10. Run real-role smoke tests
11. Run final UI workflow acceptance
```

Do not deploy frontend assumptions about a permission that has not yet been created and verified in Core.

For changes without Core work, skip the Core steps explicitly rather than silently.

---

## Gate 18 — Completion / Definition of Done

A feature is DONE only when every applicable item is true:

### Design

- [ ] Delivery Contract completed.
- [ ] Ownership / ADR-009 decision completed.
- [ ] Permission scope decisions completed.

### Core / authorization

- [ ] Permission catalog/migration complete where required.
- [ ] Scope and assignability verified in DB/runtime.
- [ ] OrganizationAdmin behavior verified.
- [ ] SYSTEM permissions unavailable to organization roles.
- [ ] Super Admin bypass verified where relevant.

### Backend

- [ ] Layered module architecture followed.
- [ ] Organization isolation implemented.
- [ ] Exact endpoint-permission mapping implemented.
- [ ] API contract / Swagger complete.
- [ ] Audit/side-effect behavior implemented where applicable.
- [ ] Backend tests pass.

### Frontend

- [ ] Types/API/labels follow existing structure.
- [ ] Permission catalog/check path updated.
- [ ] Menu visibility follows permission.
- [ ] Direct route is guarded.
- [ ] Action buttons follow exact mutation permissions.
- [ ] Shared UI primitives used.
- [ ] UI Master Standard passes.
- [ ] Responsive and Visual QA passes.
- [ ] Frontend build/tests pass.

### Runtime

- [ ] Migrations applied.
- [ ] Services restarted/rebuilt.
- [ ] Real API verified.
- [ ] Real JWT authorization matrix verified.
- [ ] Real UI workflow verified.
- [ ] No unintended 401/403/500 in the accepted path.

### Documentation

- [ ] Permanent rule/architecture changes updated in their canonical owner.
- [ ] PROJECT_STATUS updated only when status changed.
- [ ] CHANGELOG updated only when delivery/release history changed.
- [ ] No duplicate Markdown source of truth created in application repositories.

If any applicable box is false, report the work as **implemented but incomplete/not accepted**, not DONE.

---

# PART VII — STANDARD IMPLEMENTATION ORDER

For a normal new organization-scoped CRUD module, the expected sequence is:

```text
01 Requirement freeze / ambiguity check
02 ADR-009 ownership decision
03 Tier classification
04 Permission action list
05 ORGANIZATION/SYSTEM scope decision per permission
06 Default-role / OrganizationAdmin / Super Admin behavior decision
07 Data model + organization_id contract
08 Product migration design
09 Core permission migration/catalog update
10 Core permission runtime verification
11 Backend domain
12 Backend application use cases
13 Backend infrastructure repository/model
14 Backend API schemas/dependencies/routes
15 Endpoint permission guards
16 Organization isolation tests
17 Audit integration
18 Swagger/live API verification
19 Frontend types
20 Frontend API module
21 Turkish labels
22 Frontend permission catalog/helper
23 Menu permission guard
24 Route/deep-link permission guard
25 Page + shared UI components
26 Per-action create/update/archive/delete/execute guards
27 Loading/empty/error behavior
28 Dirty-form behavior where applicable
29 Responsive implementation
30 Backend full/targeted quality checks
31 Frontend build/tests/UI governance gates
32 Real JWT authorization matrix
33 Visual QA
34 Deployment in dependency order
35 Post-deploy smoke
36 Status/changelog sync when applicable
37 Completion report
```

Do not jump directly from “feature requested” to “page/API coding”. The gates exist to prevent permission, tenant, migration, UI and deployment mismatches.

---

# PART VIII — REVIEWER / AI FAIL CONDITIONS

The change must be stopped or rejected when any of these are found:

- permission scope was guessed,
- a system permission is assignable to an organization role,
- Super Admin was implemented as a normal organization role grant,
- OrganizationAdmin role definition was incorrectly made tenant-specific instead of using assignment scope,
- authenticated production traffic uses a hard-coded/test organization ID,
- backend trusts organization ID from request data without validated context,
- product data query lacks tenant scoping,
- route/action exists without matching backend permission guard,
- UI shows a protected menu/action without the required effective permission,
- UI hides a control but backend does not enforce authorization,
- direct URL bypasses UI authorization,
- frontend authorization is based on role-name strings instead of effective permissions,
- an old migration is rewritten instead of adding a new migration,
- Core Python code is imported into Fair CRM,
- cross-repo DB FK/session coupling is introduced,
- raw/ad-hoc UI duplicates an existing shared component,
- list screen performs client-side large-dataset sort/filter/pagination,
- build/tests pass but real runtime/JWT path still returns unintended 401/403/500,
- UI was accepted without real render/Visual QA,
- stale services were used for acceptance,
- documentation was duplicated instead of updating the canonical owner.

---

# Golden delivery rule

**Design the security and ownership contract first; implement backend truth second; render the same truth in the UI third; prove the real runtime path last.**

A feature is correct only when the following agree:

```text
Requirement
= Permission catalog
= Role/effective authorization
= Tenant data scope
= Backend guard
= Frontend visibility
= Real runtime behavior
```

Any disagreement between those layers is a defect, even if individual unit tests or builds pass.
