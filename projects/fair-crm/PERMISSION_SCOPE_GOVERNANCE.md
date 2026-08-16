# FAIR CRM / KYROX — Permission Scope Governance

**Status:** Mandatory canonical rule  
**Applies to:** FAIR CRM modules, KYROX Core permission catalog, RBAC role templates, role management UI, seeds and migrations

## Purpose

Every permission must be classified as exactly one of two scopes before implementation:

```text
organization
system
```

This classification is a security boundary. It is not a UI label and it must not be inferred from the permission slug, module name, URL path, or words such as `admin` or `platform`.

## Mandatory question before a new module or permission

Before creating permissions for a new module, the developer/AI must explicitly confirm the scope.

If the approved design has not already stated the answer, ask the product owner:

> **Bu modül/permission ORGANIZATION mı, SYSTEM mı?**

Example: a new `costs` / Maliyet module must not receive permissions until this question is answered.

If one module contains actions with different security boundaries, classify those permissions separately. A module may therefore contain both organization and system permissions, but each permission has one explicit scope.

Do not silently choose a scope when the requirement is ambiguous.

## ORGANIZATION scope

Use `permission_scope = 'organization'` when the permission belongs to a tenant/organization and can be delegated inside that organization.

Rules:

- The action is limited to the current `organization_id`.
- OrganizationAdmin may receive it.
- OrganizationAdmin may assign it to organization roles when `is_assignable = true`.
- ReadUser / CreateUpdateUser / FullUser templates may contain it according to their template rules.
- Custom organization roles may contain it.
- It may appear in the organization role-management permission list.
- A non-Super-Admin can only exercise it through an active role assignment in the same organization.
- New organization permissions may be auto-included in roles that have `auto_include_new_permissions = true`.

Typical examples:

```text
fair_crm.customers.read
fair_crm.customers.create
fair_crm.fairs.update
audit.logs.read
identity.roles.assign_protected
```

`identity.roles.assign_protected` is organization-scoped because an OrganizationAdmin is allowed to assign another OrganizationAdmin inside the same organization. This never grants Super Admin status.

## SYSTEM scope

Use `permission_scope = 'system'` when the action belongs to platform/Super Admin administration rather than management of one tenant.

Rules:

- Only Super Admin may effectively access the action.
- System permissions are never assignable to OrganizationAdmin.
- System permissions are never assignable to ReadUser / CreateUpdateUser / FullUser.
- System permissions are never assignable to custom organization roles.
- They must not appear in the organization role-management permission list.
- `is_assignable` must be `false` for current system permissions.
- Auto-include logic must never add them to organization roles.
- A stale/manual `identity_role_permissions` row must not make a system permission usable by a non-Super-Admin.
- Super Admin access comes from `identity_users.is_super_admin` / the central Super Admin bypass, not from a role grant.

Current SYSTEM permissions:

```text
fair_crm.admin.backups.read
fair_crm.admin.backups.create
fair_crm.admin.backups.execute
identity.permissions.lifecycle
identity.role_templates.read
identity.role_templates.manage
identity.organizations.delete
identity.organizations.suspend
```

## Super Admin and OrganizationAdmin are different concepts

### Super Admin

```text
identity_users.is_super_admin = true
```

- Platform-wide authority.
- Does not need a role assignment to obtain access.
- Bypasses normal organization RBAC.
- Can access both organization and system capabilities.

### OrganizationAdmin

- Protected organization RBAC role.
- May exist for more than one user in the same organization.
- Permission set is system-managed; organization users cannot edit the OrganizationAdmin role itself.
- Receives only organization-scoped permissions.
- May manage its own organization's users, organization roles and approved default-role derivatives.
- May assign another OrganizationAdmin inside the same organization when permitted.
- Can never grant or create Super Admin access.

## Default role templates

The global default templates are:

```text
ReadUser
CreateUpdateUser
FullUser
```

Rules:

- Their global/master definitions are managed only by Super Admin.
- Only Super Admin derives/assigns a default template into an organization.
- The derived organization role belongs only to that organization and may be customized by its OrganizationAdmin.
- Global template changes do not authorize system-scoped permissions to organization roles.
- System permissions must never be synchronized into organization template derivatives.

## Database contract

`identity_permissions.permission_scope` is the source of truth.

Allowed values:

```text
organization
system
```

For every new permission migration, set the scope explicitly. Do not rely on naming conventions and do not rely on the database default as the design decision.

Examples:

```text
fair_crm.costs.read
permission_scope = organization
is_assignable = true
```

```text
some.platform.destructive_operation
permission_scope = system
is_assignable = false
```

Changing the scope of an existing permission is a security change and requires a new migration. Do not rewrite old migrations.

## Enforcement contract

All implementation paths must preserve the boundary:

1. Organization permission-list APIs return only active, assignable `organization` permissions.
2. Organization role create/update rejects every `system` permission, including requests made by Super Admin on behalf of an organization role.
3. Authorization checks for non-Super-Admins require `permission_scope = 'organization'`.
4. Auto-include/new-permission triggers operate only on active `organization` permissions.
5. When a permission becomes `system`, remove existing organization role grants and template exclusions for that permission.
6. System actions remain accessible to Super Admin through the central Super Admin bypass / platform guard.
7. Frontend organization-role screens must never manually reconstruct a broader permission list than the Core organization permission API returns.

## New module checklist

Before coding a new module such as `costs` / Maliyet:

1. Decide whether the capability is product-specific or platform-generic under ADR-009.
2. List the permissions required by the module.
3. Ask/confirm: **ORGANIZATION or SYSTEM?**
4. Record `permission_scope` explicitly for every new permission.
5. For ORGANIZATION permissions, verify every data query and mutation is tenant-scoped by `organization_id`.
6. For SYSTEM permissions, verify no organization role/template can receive them and only Super Admin can effectively execute them.
7. Update Core catalog/migration, role matrix/seed references, API guards and frontend permission constants only where applicable.
8. Add tests for the scope boundary: organization users must fail SYSTEM actions; Super Admin must continue to succeed.

## Naming rule

Permission codes remain semantic action identifiers, for example:

```text
fair_crm.costs.read
fair_crm.costs.create
```

Do not rename an existing permission slug merely to express its scope. Scope belongs in `permission_scope`, not in the slug.

## Decision rule

When uncertain, do not guess.

Ask one question before implementation:

> **Bu yetki organizasyonun kendi içinde dağıtabileceği bir yetki mi, yoksa yalnız Super Admin'in platform seviyesinde yapacağı bir iş mi?**

The answer determines `organization` versus `system`.
