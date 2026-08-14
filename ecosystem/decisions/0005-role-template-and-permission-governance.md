# ADR-0005: Role template and permission governance

- **Status:** Accepted
- **Date:** 2026-08-14
- **Deciders:** KYROX ecosystem maintainers

## Context

KYROX needs platform-managed default role standards without turning any role into a second Super Admin mechanism. Organizations also need freedom to customize their own working roles, while the platform must retain an emergency control that can revoke a dangerous capability from every non-Super-Admin user.

Directly editing one global role for an organization would leak changes into other organizations. Conversely, copying a template without recording its origin would make later platform-wide corrections unreliable. The role model therefore needs explicit template provenance, controlled synchronization, and permission-level lifecycle controls.

The Platform Super Admin invariant remains defined by [ADR-0003](0003-identity-security-strategy.md#platform-super-admin-invariant). Nothing in this decision creates another authorization bypass.

## Decision

### 1. Authorization remains database-backed

- `OrganizationAdmin`, `ReadUser`, `CreateUpdateUser`, and `FullUser` are roles or role templates, never authorization bypasses.
- Their access is determined only by registered permissions and database role-permission mappings.
- A role name, slug, template type, or `is_system` flag must never grant implicit access in an authorization guard.
- `is_super_admin = false` always follows normal RBAC, CRUD permission, membership, organization-scope, and ownership enforcement.

### 2. System default definitions

Core owns four protected system definitions:

| Definition | Assignment model | Permission management |
|------------|------------------|-----------------------|
| `OrganizationAdmin` | The protected system role is assignable in every organization | Only Platform Super Admin may change its global permission package |
| `ReadUser` | Template only; derive an organization-specific role before assignment | Platform template is managed by Super Admin; derived role is editable inside its organization |
| `CreateUpdateUser` | Template only; derive an organization-specific role before assignment | Platform template is managed by Super Admin; derived role is editable inside its organization |
| `FullUser` | Template only; derive an organization-specific role before assignment | Platform template is managed by Super Admin; derived role is editable inside its organization |

System definitions cannot be deleted, renamed, have their stable slug changed, or be converted into organization-owned custom roles. Their permission packages are deliberately editable by Platform Super Admin so the platform standard can evolve. Names describe starting policy, not permanent hardcoded capability promises; for example, `FullUser` may exclude role administration and `OrganizationAdmin` may exclude database backup operations.

New assignable organization-scoped permissions are included in `OrganizationAdmin` by default unless a stored platform policy explicitly excludes or locks them. Other templates receive permissions according to their database-managed template policy and exclusions. This allocation behavior must be data-driven and must not become a runtime role-name bypass.

### 3. Assignment authority

- Platform Super Admin may assign `OrganizationAdmin` in any organization.
- An `OrganizationAdmin` may assign another user as `OrganizationAdmin` only inside their own organization.
- Platform Super Admin derives organization-specific roles from `ReadUser`, `CreateUpdateUser`, or `FullUser` and assigns the derived role to a specific organization.
- A new non-Super-Admin user must have an organization membership and be assigned an available role belonging to that organization.
- An `OrganizationAdmin` may create, edit, delete, and assign derived or custom roles only inside their own organization, subject to protected-role and permission-lock rules.

### 4. Template derivation and provenance

A role derived from a system template is a distinct organization-owned role. It must record at least:

- its organization;
- its source system template;
- the source template version used for its last synchronization;
- whether organization-specific permission changes have been made;
- creation, update, and synchronization audit metadata.

Editing a derived role never changes its source template or another organization's role. Global template edits affect future derivations by default and do not silently overwrite existing organization customizations.

### 5. Template synchronization

Platform Super Admin may run **Update from template** with one of these scopes:

- one selected derived role;
- selected organizations or derived roles;
- every role derived from the selected template.

A forced synchronization replaces the target role's permission set with the current template permission set; it is not an additive merge. Therefore it may overwrite organization-specific changes.

Before execution, the system must show a preview containing the affected organizations, roles, users, permissions to add, and permissions to remove. The operation must be atomic for its selected scope and must produce an audit record identifying the actor, template version, targets, and resulting changes.

`OrganizationAdmin` is a shared protected system role rather than an organization-specific derivative. Changes to its global permission package therefore apply to every organization assignment immediately after the database change commits.

### 6. Platform-wide permission control

Template synchronization is insufficient when a capability must be removed from every non-Super-Admin role, including fully custom roles. Core therefore owns a permission-level lifecycle and assignment policy:

| State | Normal role behavior | Assignment behavior |
|-------|----------------------|---------------------|
| **Active and assignable** | Authorization follows role-permission mappings | Eligible roles may receive the permission |
| **Active and platform-locked** | No non-Super-Admin role may authorize the permission | Permission is hidden/disabled in role editors and cannot be assigned |
| **Inactive** | No non-Super-Admin role may authorize the permission | Permission cannot be assigned |

Only Platform Super Admin may lock, unlock, activate, or deactivate a permission platform-wide.

Locking or deactivating a permission must atomically:

1. mark it unavailable for role assignment;
2. remove it from `OrganizationAdmin` and every other system template;
3. remove it from every derived organization role;
4. remove it from every fully custom role;
5. prevent organization administrators from adding it back;
6. record the actor, reason, affected roles, and affected organizations in the audit trail.

Unlocking or reactivating a permission makes it assignable again but does not silently restore previous grants. Restoration requires an explicit template synchronization or deliberate role edit.

Platform Super Admin remains authorized regardless of permission lifecycle state because their access comes only from `identity_users.is_super_admin`, as defined by ADR-0003.

### 7. Product and frontend behavior

- Products consume Core authorization decisions and must not infer access from role names or template types.
- Role editors obtain assignable permissions from Core and must not display platform-locked or inactive permissions as editable choices.
- Frontends may hide or disable controls using Core-derived permission decisions, but backend enforcement remains mandatory.
- A new product permission and its template allocation or exclusion policy are one delivery unit; an endpoint is not authorization-complete while that policy is undefined.

## Consequences

### Positive

- Platform defaults can evolve without giving any role a hardcoded bypass.
- Organization-specific customization remains isolated.
- Super Admin can deliberately propagate a corrected standard to existing derived roles.
- Dangerous capabilities can be revoked from every non-Super-Admin role, including custom roles.
- Provenance, preview, atomic execution, and audit records make broad changes reviewable.

### Costs and constraints

- Derived roles require template provenance and version metadata.
- Template synchronization needs preview, diff, audit, and bulk-update support.
- Permission lifecycle changes require transactional cleanup of all role-permission mappings.
- Existing role records must be classified or migrated before forced synchronization can be trusted.

## Related

- [ADR-0003: Identity security strategy](0003-identity-security-strategy.md)
- [Core product integration guide](../../projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)
- [KYROX workflow authorization acceptance gate](../WORKFLOW.md#authorization-and-real-runtime-acceptance-gate)
