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

# PART I — DESIGN CONTRACT

## Gate 0 — Delivery Contract

Every material delivery starts with a concise contract that answers all applicable questions:

```text
Feature/module and business purpose
Owning repository/project
Product-specific vs reusable platform capability
Feature profile / applicability
Tenant/organization scope
Permissions/actions and scope
Role/template/system-admin effects
Data model and migration need
API/integration boundaries
Audit/side effects
Frontend routes/navigation/actions
Forms/tables/responsive requirements
Tests and runtime acceptance
Deployment dependencies/order
```

A field may be N/A only with a valid architectural reason.

**PASS:** material requirements are unambiguous; owner, scope, destructive semantics, user flow and acceptance path are explicit.

## Gate 1 — Ownership and platform boundary

Decide where the capability belongs before code.

- Reusable platform infrastructure belongs in Core only after the ownership decision is explicit.
- Product/domain semantics stay in the product.
- Provider/site-specific execution stays behind the applicable adapter/handler boundary.
- Core must not depend on product code.
- Products consume Core through public contracts; no shared runtime modules, DB sessions or cross-repository foreign keys.

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

Quality semantics: [../quality/QUALITY_GATE_STANDARD.md](../quality/QUALITY_GATE_STANDARD.md).

## Gate 14 — Authorization acceptance

Protected user-facing work is not complete with mocks/dev bypass alone.

At minimum, prove applicable combinations of:

- privileged/system user behavior,
- organization-admin behavior,
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
- loading/empty/error/refresh behavior,
- dirty-form behavior,
- responsive/visual QA,
- keyboard/focus/accessibility behavior.

# PART V — RUNTIME, DEPLOYMENT AND COMPLETION

## Gate 16 — Runtime synchronization

Do not accept behavior against stale services/builds.

Apply required migrations, restart/rebuild affected runtimes, verify environment/version/route, and make at least one real request/workflow through the changed path when runtime-sensitive.

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
- data/migrations,
- backend truth and authorization,
- tenant isolation,
- API/integration contract,
- audit/side effects,
- frontend/UI and effective-permission visibility,
- tests/quality gates,
- real runtime authorization when applicable,
- deployment/runtime synchronization,
- canonical documentation/status/changelog updates.

If an applicable gate is unresolved, report the work as **implemented but incomplete/not accepted**, not DONE.

## Reviewer / AI hard-fail conditions

Stop/reject when material issues include:

- permission/scope/ownership guessed,
- system capability incorrectly assignable to organization roles,
- production-shaped traffic uses hard-coded tenant context,
- backend trusts unvalidated tenant identifiers,
- product data access lacks tenant scoping,
- protected route/action lacks backend authorization,
- UI exposes protected capability without effective permission,
- UI hiding is used as a substitute for backend security,
- direct route bypasses UI authorization,
- frontend authorization relies on role-name strings instead of effective permissions,
- shipped migration is rewritten rather than superseded by a new migration,
- Core/product runtime or DB coupling violates repository boundaries,
- ad-hoc UI duplicates an existing shared primitive,
- scalable list behavior is simulated with large client-side datasets,
- tests/build pass while the real accepted path still fails,
- visual UI accepted without real render evidence,
- stale runtime used for acceptance,
- a second documentation source of truth is created.

# Golden delivery rule

**Design the security and ownership contract first; implement backend truth second; render the same truth in the UI third; prove the real runtime path last.**

```text
Requirement
= ownership/scope contract
= permission/effective authorization
= tenant data scope
= backend guard
= frontend visibility (when applicable)
= real runtime behavior
```

Any disagreement between those layers is a defect.
