# CRUD & UI Authorization Standard

**Status:** Canonical shared KYROX standard  
**Scope:** All KYROX products that expose permission-controlled CRUD or user actions  
**Audience:** Human developers, AI agents, reviewers and test authors

This document defines reusable CRUD permission semantics and how effective permissions control UI visibility and backend access. Product-specific documents may add domain-specific actions or explicit exceptions, but must not redefine these base semantics.

## 1. Core principle

The UI must represent what the authenticated user is actually allowed to do, and the backend must independently enforce the same authorization.

**UI hiding is usability, not security. Backend authorization is mandatory.**

## 2. Canonical CRUD semantics

Unless an explicit product/domain contract defines a different non-CRUD action, use these semantics:

| Capability | Permission meaning | UI expectation |
|---|---|---|
| `read` | View/list/detail access | Page, navigation entry, list/detail data and read-only entry points are available only when the relevant read capability is effective |
| `create` | Create a new entity | New/Add/Create buttons and create routes/forms are available only with effective create permission |
| `update` | Modify an existing entity | Edit buttons, editable controls and update routes/forms are available only with effective update permission |
| `delete` | Delete/remove an entity | Delete/remove actions and confirmation flows are available only with effective delete permission |

A product may define additional actions such as `merge`, `approve`, `export`, `send`, `execute` or `restore`. Each such action must map to an explicit permission/capability and follow the same visibility + backend-enforcement model.

## 3. Effective permission is the source for UI decisions

Frontend visibility and route/action availability must use the **effective permission result for the current authenticated user and active scope/context**. Do not infer permission from:

- role names such as `admin` or `owner`,
- menu grouping,
- route names,
- UI labels,
- hard-coded organization IDs,
- assumptions that a user who can read can also update/delete,
- assumptions that Super Admin and organization-scoped users share identical UI rules.

The authorization source must be the platform-approved effective permission mechanism for that product.

## 4. Surfaces that must obey permission visibility

Permission enforcement is not limited to buttons. Every applicable UI entry point must be covered:

- sidebar / top navigation,
- module cards / dashboard shortcuts,
- list-page toolbar actions,
- row actions,
- detail-page actions,
- create/edit/delete buttons,
- bulk actions,
- context menus / dropdown items,
- direct routes,
- tabs or sections whose content itself requires a permission,
- keyboard/shortcut actions where applicable.

A hidden toolbar button with an unguarded direct route is a failure. A guarded route with an incorrectly visible action is also a failure.

## 5. Hide, disable or deny

Default behavior for an action the user does not possess is **do not present it as an available action**.

Use a disabled control only when the user is authorized for the capability but a temporary domain/state constraint prevents execution (for example, an entity cannot be deleted while processing). The disabled state should explain the state constraint when useful.

Do not use disabled controls as a substitute for missing permission unless a product-specific UX standard explicitly requires discoverability.

Direct navigation to an unauthorized route must not expose the protected operation. The frontend should use the product-standard unauthorized/not-found handling, while the backend independently returns the correct authorization failure.

## 6. Backend remains authoritative

Every protected backend operation must verify authorization even when the UI hides the action.

Required properties:

- tenant/organization scope is validated where applicable,
- permission is checked server-side,
- object identifiers cannot bypass scope,
- bulk endpoints enforce the same authorization semantics,
- background/service entry points do not assume frontend checks occurred.

Never weaken backend authorization merely to make a frontend flow work.

## 7. Permission naming and scope

This standard defines CRUD/action semantics, not product-specific permission slugs.

Each product must define its permission catalog and scope using the applicable platform/project governance. New permissions must have an explicit ownership/scope decision before implementation. Do not invent a permission solely to satisfy a generic CRUD checklist when the feature is not user-facing or the operation does not exist.

## 8. Reusable implementation expectation

Products should implement permission-aware UI using shared permission utilities/components/hooks rather than repeated inline role checks.

Avoid:

- `if (role === "admin")` for action visibility,
- page-local permission parsers,
- duplicated `canCreate/canEdit/canDelete` logic with inconsistent semantics,
- manually hiding one button while leaving equivalent actions elsewhere.

If a common helper is insufficient, improve the shared product/platform mechanism rather than creating another parallel permission system.

## 9. Acceptance matrix

For every permission-controlled CRUD/action surface changed or added, verify at minimum:

1. **Permission granted:** relevant navigation/action/route is available and backend operation succeeds when domain state is valid.
2. **Permission absent:** relevant navigation/action is not presented; direct route cannot expose the operation; backend denies direct API execution.
3. **Mixed permissions:** independent CRUD permissions behave independently (for example read + update without delete must not show delete).
4. **Scope mismatch:** permission in one organization/scope does not authorize another scope.
5. **Super Admin/system behavior:** follows the canonical platform/product authorization model rather than frontend role-name assumptions.

Automated tests should cover both UI gating and backend denial for material authorization paths.

## 10. Product-specific extension

A product-specific document should contain only what is unique to that product, for example:

- Fair CRM `customer.merge` requires `fair_crm.customers.merge` and has domain-specific eligibility rules.
- A future inventory product might define `stock.adjust` with its own state constraints.

Those documents must link to this standard and describe only the additional semantics.

## 11. Conflict rule

If a project document repeats CRUD/UI permission rules from this file, consolidate the reusable rule here and reduce the project document to product-specific details plus a link.

If an explicit product exception is required, document the exception, its reason and its scope. Silent divergence is not allowed.
