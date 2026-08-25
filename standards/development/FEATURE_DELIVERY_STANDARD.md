# KYROX Feature Delivery Standard

**Status:** Canonical shared KYROX standard  
**Scope:** Material features, modules, integrations, jobs, permission-controlled actions, UI work and platform capabilities  
**Audience:** Human developers, AI agents and reviewers

This standard defines the reusable execution order for KYROX feature delivery. Product extensions define product-specific permission slugs, API conventions, UI implementation details, runtime topology and deployment steps; they must not redefine the shared gates.

The purpose is deterministic delivery: design the ownership/security contract first, implement backend truth, render the same truth in the UI when applicable, then prove the real runtime path.

## Precedence

Before implementation:

1. read ecosystem documentation governance and workflow,
2. read applicable shared standards,
3. read the owning project documentation/ADRs,
4. resolve explicit task requirements,
5. stop on material ambiguity rather than inventing product behavior.

Applicability of each gate is governed by [FEATURE_APPLICABILITY_STANDARD.md](FEATURE_APPLICABILITY_STANDARD.md). A gate is REQUIRED or N/A with a reason; non-applicable work is not invented.

Cross-repository SaaS sequencing and current platform/product ownership constraints are defined in [../../ecosystem/SAAS_ROADMAP.md](../../ecosystem/SAAS_ROADMAP.md). The roadmap does not replace this delivery standard; it determines strategic priority while this file defines binding delivery/acceptance semantics.

# PART I — DESIGN CONTRACT

## Gate 0 — Delivery Contract

Every material delivery starts with a concise contract that answers all applicable questions:

```text
Feature/module and business purpose
Owning repository/project
Product-specific vs reusable platform capability
Feature profile / applicability
SaaS-impact classification
Tenant/organization scope
Permissions/actions and scope
Role/template/system-admin effects
Plan/entitlement/usage/account-lifecycle impact when applicable
Data model and migration need
API/integration boundaries
Audit/side effects
Frontend routes/navigation/actions
Forms/tables/responsive requirements
Tests and runtime acceptance
Deployment dependencies/order
```

A field may be N/A only with a valid architectural reason.

The SaaS-impact classification considers, at minimum, organization-owned data, organization/system permission scope, Core/product/provider ownership, entitlement/plan behavior, usage/quota behavior, organization lifecycle, secrets/security, background jobs/audit, data export/retention/delete and scale/infrastructure dependency.

**PASS:** material requirements are unambiguous; owner, scope, destructive semantics, user flow, SaaS-impact dimensions and acceptance path are explicit.

## Gate 1 — Ownership and platform boundary

Decide where the capability belongs before code.

- Reusable platform infrastructure belongs in Core only after the ownership decision is explicit.
- Product/domain semantics stay in the product.
- Provider/site-specific execution stays behind the applicable adapter/handler boundary.
- Core must not depend on product code.
- Products consume Core through public contracts; no shared runtime modules, DB sessions or cross-repository foreign keys.
- Existing Core capabilities such as identity, organization/membership, authorization, audit and generic jobs are reused rather than duplicated in a product.
- During a Core freeze, future-looking platform candidates require a proven product need and the applicable planning/ADR decision before implementation.

If ownership is unclear, stop and decide before implementation.

## Gate 2 — Authorization contract

Authorization is designed before protected backend routes and UI.

For every user-controlled action:

- identify the semantic action (`read`, `create`, `update`, `archive`, `delete`, `execute`, `approve`, `export`, etc.),
- map it to an explicit permission/capability when the platform model requires one,
- decide organization/system scope,
- define assignability and role/template effects,
- define system/Super-Admin behavior using the platform model rather than fake role grants.

Do not invent CRUD permissions for behavior that is not CRUD. Do not use vague umbrella permissions to avoid action design.

UI semantics: [../ui/CRUD_UI_AUTHORIZATION_STANDARD.md](../ui/CRUD_UI_AUTHORIZATION_STANDARD.md).

## SaaS safety overlay — mandatory for every material delivery

The SaaS overlay is a review of affected architecture/security dimensions, not a demand to build all SaaS capabilities for every feature.

Rules:

1. **Organization is the account boundary.** `tenant isolation` is the security term; do not introduce a parallel Tenant account model without an accepted architecture change.
2. **Tenant isolation is separate from permission.** Organization-owned data requires validated organization context and scoped access even when a user has the action permission.
3. **Platform Super Admin follows the canonical bypass model.** Do not make organization-isolation tests fail merely because a real Super Admin is intentionally platform-wide; normal organization users and OrganizationAdmins must still fail cross-organization access.
4. **Plan/entitlement is separate from RBAC.** A role permission says what a user may do; an entitlement says whether the organization/product package includes the capability. Do not substitute plan-name checks for backend authorization or entitlement enforcement.
5. **Usage/quota enforcement is server authoritative when applicable.** Client-only counters/limits are not acceptance evidence; concurrency/retry semantics must be explicit.
6. **Organization lifecycle changes are security changes.** Do not invent Owner roles, self-service suspend/delete or destructive account behavior contrary to current governance without an explicit decision/ADR.
7. **Async/background execution preserves organization context.** A worker is not exempt from tenant isolation merely because user permissions are N/A at execution time.
8. **Production security configuration is part of acceptance.** Development bypasses/fallback identities, secret exposure or unsafe credential handling cannot be hidden behind green tests.
9. **No speculative scale/platform work.** Introduce caches, queues, event buses, extra services or generic platform capabilities only when the current requirement and ownership decision justify them.

Every affected SaaS dimension needs test/runtime evidence appropriate to the property. An unaffected dimension is N/A with a concise architectural reason.

# PART II — DATA, INTEGRATION AND BACKEND TRUTH

## Gate 3 — Data and migration contract

Before schema work:

- ownership and tenant key strategy are explicit,
- cross-service identifiers are logical identifiers, not cross-database FKs,
- repository/data-access paths enforce scope,
- migrations are additive/forward-moving; already-applied migrations are not rewritten to change shipped behavior,
- seed/catalog migrations follow existing idempotency/repeat-safety rules,
- restore/migration acceptance follows the canonical database standards.

After permission/schema migrations, verify resulting runtime/DB state rather than assuming migration code produced the intended state.

## Gate 4 — Cross-service integration contract

Use public ports/adapters/contracts. Do not duplicate platform authorization or shared service behavior inside a product merely to avoid integration.

Authenticated/scoped context comes from the real session/request context, not hard-coded test/default identifiers in production-shaped flows.

Protected behavior fails closed when authorization state cannot be resolved.

## Gate 5 — Backend architecture

Backend implementation follows the canonical [Backend Architecture Standards](../backend/BACKEND_ARCHITECTURE_STANDARDS.md).

At minimum:

- domain owns pure business rules/invariants,
- application owns use-case orchestration,
- infrastructure owns persistence/external technology,
- API/transport remains thin,
- modules communicate through stable contracts rather than importing another module's infrastructure implementation,
- tenant filters and safe sort/filter whitelists are enforced where applicable.

## Gate 6 — Backend authorization mapping

Every protected endpoint/use case maps to the capability representing the exact action.

Authorization and tenant isolation are separate layers:

```text
Authenticated/trusted actor
  -> validated tenant/context
  -> authorization decision
  -> tenant-scoped query/mutation
  -> domain invariants
```

Permission answers **what** may be done; tenant scope answers **to whose data**. Neither replaces the other.

Cross-tenant identifiers must not leak resource existence contrary to the owning product's API/security contract.

## Gate 7 — API contract

Before UI consumes an API, the backend contract is stable enough to test and integrate.

Shared expectations:

- documented request/response schemas,
- stable status/error semantics,
- identifiers/date-time serialization defined,
- API documentation/OpenAPI verified when applicable,
- list APIs use server-side pagination/search/sort/filter for scalable datasets,
- unbounded client-side fetch/sort/filter/pagination is not used to simulate server behavior.

Product extensions define exact base paths, casing, response conventions and status codes.

## Gate 8 — Audit and side effects

Mutations/sensitive operations define audit/side-effect behavior before completion.

Use existing shared audit/job/operation infrastructure when applicable; do not create feature-local duplicate lifecycle/status engines.

Failure policy for auxiliary effects (audit, notification, telemetry) must be explicit: best-effort vs transactional behavior is a product/platform decision, not an accident.

# PART III — FRONTEND / USER SURFACE

## Gate 9 — Frontend data layer

When frontend is REQUIRED, follow the owning product's shared client/type/label/component structure. Do not duplicate auth/header/error handling page-by-page when shared infrastructure exists.

Permission codes/capabilities used by UI flow through the canonical permission mechanism.

## Gate 10 — Permission-aware UI

The UI represents the authenticated user's **effective permissions**, not role-name guesses.

Applicable navigation, direct routes, toolbar actions, row/detail actions and create/update/delete/execute controls must agree with effective permissions and backend authorization.

Missing permission normally means the action is not presented. Disabled state is for authorized actions blocked by temporary domain state unless an explicit UX exception exists.

A visible/allowed UI action that the same real user cannot execute because authorization is mismatched is **not accepted**.

Where product plans/entitlements exist, permission denial and entitlement/plan denial remain distinct states; the UI must not present a package limitation as a role-permission failure or vice versa.

Canonical rule: [../ui/CRUD_UI_AUTHORIZATION_STANDARD.md](../ui/CRUD_UI_AUTHORIZATION_STANDARD.md).

## Gate 11 — UI/design-system contract

When UI is REQUIRED:

- use the owning product's canonical shared primitives/design system,
- do not create parallel/ad-hoc control families,
- use design tokens and shared layout patterns,
- implement responsive behavior for supported sizes,
- separate loading/empty/error states correctly,
- preserve successful visible data during silent refresh where the product standard requires it,
- verify accessibility/focus behavior,
- perform real rendered/visual QA; build success alone is insufficient.

Product UI standards define exact components, tokens, breakpoints and page structure.

## Gate 12 — Forms, dialogs and destructive behavior

Create/edit/update flows preserve unsaved user data according to the owning product's dirty-form standard.

Destructive semantics are explicit:

- archive is not silently relabeled delete,
- hard delete is not silently implemented as archive,
- restore behavior matches the domain/permission contract,
- organization/account suspension/deletion follows explicit platform permission/lifecycle policy,
- confirmation uses shared product primitives,
- critical actions remain usable at supported viewport sizes.

# PART IV — TESTING AND ACCEPTANCE

## Gate 13 — Test matrix

Test every applicable executable layer:

- domain invariants/state transitions,
- application success/failure/orchestration,
- infrastructure persistence/scoping/mapping,
- API request/response/auth/isolation/validation/not-found behavior,
- frontend behavior when applicable,
- integration/runtime-sensitive behavior where static tests are insufficient.

For every change touching organization-owned data or scoped execution, include cross-organization denial tests at the lowest reliable layer and at the API/runtime boundary where the risk cannot be proven statically. Direct resource IDs, bulk operations, exports/downloads and background-job/run identifiers must not bypass scope.

For plan/entitlement/quota work, test backend enforcement, mixed permission/entitlement states, concurrent limit behavior and retry/idempotency where applicable.

Quality semantics: [../quality/QUALITY_GATE_STANDARD.md](../quality/QUALITY_GATE_STANDARD.md).

## Gate 14 — Authorization acceptance

Protected user-facing work is not complete with mocks/dev bypass alone.

At minimum, prove applicable combinations of:

- privileged/system user behavior,
- Platform Super Admin behavior according to the canonical bypass invariant,
- organization-admin behavior in its own organization,
- organization-admin or normal-user access to another organization is denied,
- restricted/default/custom role behavior,
- granted action succeeds,
- ungranted action is denied,
- tenant/scope mismatch is denied,
- missing read capability hides/guards UI entry and backend remains protected,
- independent mutation permissions behave independently.

Production-shaped acceptance uses a real authentication/session path through the actual authorization service and product API.

## Gate 15 — Frontend verification

When frontend is REQUIRED, verify applicable evidence:

- build/tests/governance checks,
- real route render,
- real API data,
- permission-controlled navigation/routes/actions,
- plan/entitlement visibility and denial semantics when applicable,
- loading/empty/error/refresh behavior,
- dirty-form behavior,
- responsive/visual QA,
- keyboard/focus/accessibility behavior.

# PART V — RUNTIME, DEPLOYMENT AND COMPLETION

## Gate 16 — Runtime synchronization

Do not accept behavior against stale services/builds.

Apply required migrations, restart/rebuild affected runtimes, verify environment/version/route, and make at least one real request/workflow through the changed path when runtime-sensitive.

Security/runtime acceptance includes verifying that development-only bypass/fallback behavior is not acting as production authority in the accepted environment.

## Gate 17 — Deployment order

Deploy dependencies before consumers. When a product depends on a new/changed Core contract or permission:

1. Core change/migration is ready,
2. Core is deployed/migrated and verified,
3. product backend is deployed/migrated,
4. product frontend is built/deployed,
5. authorization/session refresh is performed when required,
6. real-role/runtime smoke and UI acceptance are run.

Skip non-applicable steps explicitly; do not silently assume a dependency already exists.

## Gate 18 — Definition of Done

A material feature is DONE only when every applicable gate is complete:

- design/ownership/security decisions,
- SaaS-impact classification with REQUIRED/N/A reasons,
- data/migrations,
- backend truth and authorization,
- tenant isolation and cross-organization denial evidence when scoped,
- API/integration contract,
- audit/side effects,
- entitlement/usage/account-lifecycle behavior when applicable,
- frontend/UI and effective-permission visibility,
- tests/quality gates,
- real runtime authorization/security behavior when applicable,
- deployment/runtime synchronization,
- canonical documentation/status/changelog updates.

**Green CI is necessary but not sufficient.** If an applicable SaaS property remains unproven or the production-shaped protected path still fails, report the work as **implemented but incomplete/not accepted**, not DONE.

## Reviewer / AI hard-fail conditions

Stop/reject when material issues include:

- permission/scope/ownership guessed,
- system capability incorrectly assignable to organization roles,
- production-shaped traffic uses hard-coded tenant context,
- backend trusts unvalidated tenant identifiers,
- product data access lacks tenant scoping,
- cross-organization denial evidence is missing for changed organization-owned access,
- protected route/action lacks backend authorization,
- UI exposes protected capability without effective permission,
- UI hiding is used as a substitute for backend security,
- direct route bypasses UI authorization,
- frontend authorization relies on role-name strings instead of effective permissions,
- a plan name is used as the effective authorization mechanism instead of the approved entitlement/permission contracts,
- quota enforcement exists only in the client or is concurrency-unsafe when the limit must be hard,
- organization lifecycle behavior invents Owner/self-service destructive authority contrary to canonical governance,
- product-specific business semantics are moved into Core without an explicit ownership decision,
- a product duplicates Core-owned authorization/organization/audit/generic-job infrastructure,
- organization-scoped background work executes without validated organization context or deliberate system scope,
- a development bypass/fallback identity can become production authority,
- secrets/tokens/credentials are exposed in logs, audit payloads or committed configuration,
- shipped migration is rewritten rather than superseded by a new migration,
- Core/product runtime or DB coupling violates repository boundaries,
- ad-hoc UI duplicates an existing shared primitive,
- scalable list behavior is simulated with large client-side datasets,
- tests/build pass while the real accepted path still fails,
- visual UI accepted without real render evidence,
- stale runtime used for acceptance,
- a second documentation source of truth is created.

# Golden delivery rule

**Design the security, ownership and SaaS-impact contract first; implement backend truth second; render the same truth in the UI third; prove the real runtime path last.**

```text
Requirement
= ownership/scope contract
= SaaS-impact classification
= permission/effective authorization
= tenant data scope
= backend guard
= entitlement/usage constraint when applicable
= frontend visibility (when applicable)
= real runtime behavior
```

Any disagreement between those layers is a defect.
