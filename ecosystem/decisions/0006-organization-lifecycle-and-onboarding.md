# ADR-0006: Organization lifecycle and SaaS onboarding contract

- **Status:** Proposed
- **Date:** 2026-08-26
- **Deciders:** KYROX ecosystem maintainers
- **Roadmap gate:** P0.2 — Organization lifecycle contract and SaaS onboarding decisions

## Context

P0.1 tenant-isolation certification is complete. The next SaaS-readiness gate is to define how a commercial KYROX account is created, administered, suspended, reactivated and eventually closed without duplicating Core capabilities or leaking lifecycle semantics across repositories.

The current implementation has evolved beyond older membership-oriented documentation. This ADR records the verified current architecture first, then proposes the lifecycle contract that must be accepted before implementation work begins.

## Verified current implementation

### Organization and user model

- `Organization` is the canonical account/data boundary. No parallel `Tenant` entity is introduced.
- Migration `20260817_0057_remove_memberships` replaced `identity_memberships` with direct `identity_users.organization_id` ownership for normal users.
- The same migration removed `identity_membership_invites` and membership permissions.
- A normal user belongs to exactly one organization in the current Core model.
- Platform Super Admin has `identity_users.is_super_admin = true` and `organization_id = NULL`.
- Migration `20260814_0043_remove_owner_role` removed the legacy `owner` role. No new Owner role is part of the current architecture.
- `OrganizationAdmin` is the protected full-access organization role defined by ADR-0005 and remains normal database-backed RBAC, not an authorization bypass.

### Current organization API authority

- `POST /organizations` is Platform Super Admin only.
- `GET /organizations/{id}` and `PATCH /organizations/{id}` use organization-scoped permissions and organization-scope enforcement.
- `identity.organizations.delete` and `identity.organizations.suspend` are SYSTEM-scope, non-assignable permissions; organization roles cannot receive them.
- Normal authorization requires the organization to be active, so suspended organizations fail normal RBAC checks.
- Current Core organization delete is a soft delete (`deleted_at`); it does not hard-delete product data in another repository/database.
- The domain has a `reactivate` transition, but the current organization API does not expose a reactivation endpoint.

### Current onboarding capability

- Core user management can create a user directly inside an organization and assign an available role.
- There is currently no membership invitation/acceptance workflow after migration 0057.
- Therefore older documentation must not claim that invitation APIs already exist.

### Cross-repository lifecycle reality

Core and FAIR CRM use separate persistence. Suspending or soft-deleting an organization in Core does not automatically:

- cancel or drain FAIR CRM background jobs,
- revoke or disable FAIR CRM provider credentials,
- export, retain, anonymize or delete FAIR CRM business data,
- expire product-generated files/artifacts,
- define backup ageing behavior for deleted organization data.

Those effects require an explicit lifecycle contract and product orchestration; they cannot be inferred from Core database cascades.

## Proposed decision

The following is the proposed P0.2 baseline. It is **not binding until this ADR becomes Accepted**.

### 1. Keep Organization as the only account boundary

Retain the current ADR-0003 model:

```text
Organization = customer/account boundary
organization_id = product/Core isolation key
Tenant = infrastructure terminology only
```

No new Tenant table/entity is created.

### 2. Keep the direct single-organization user model for current M4

Use the current `identity_users.organization_id` model as the baseline for M4 rather than reintroducing memberships speculatively.

A future requirement for one normal user to participate in multiple organizations would require a separate accepted architecture change. It must not be smuggled into P0.2 as an implementation detail.

This decision, if accepted, supersedes membership-specific wording in ADR-0005 and older roadmap text where it describes implementation rather than a generic concept.

### 3. Do not create an Owner role

The first normal administrative user of an organization should use the existing `OrganizationAdmin` role. Platform-wide authority remains `is_super_admin` only.

No `Owner` role, role-name bypass or hidden ownership permission model is introduced.

### 4. Keep organization creation controlled by Platform Super Admin for M4

For the current M4 baseline, organization creation remains a Platform Super Admin operation.

Self-service public organization creation may be added only after an explicit commercial signup requirement defines:

- identity verification / account activation,
- abuse and duplicate-account controls,
- initial OrganizationAdmin creation,
- entitlement/billing interaction if applicable,
- rollback when onboarding is abandoned.

### 5. Define the first-user bootstrap explicitly

Creating an organization and creating its first normal user are separate operations today. P0.2 implementation should provide one production-safe orchestration that results in:

```text
organization created
  -> first normal user created/activated
  -> OrganizationAdmin assigned
  -> user can authenticate
  -> user can reach FAIR CRM first-run flow
```

The implementation must not assign OrganizationAdmin to Platform Super Admin and must not rely on direct SQL.

### 6. Invitation/account-activation mechanism is an explicit product decision

Core no longer has membership invitations. P0.2 must therefore choose one supported onboarding mechanism instead of assuming invitations exist.

Candidate choices:

1. **Direct administrative user creation** — simplest existing capability, but requires a secure initial-password/activation process suitable for commercial use.
2. **Reintroduce a generic Core invitation/activation capability** — only if FAIR CRM has a real product requirement; it must fit the current direct single-organization user model rather than restoring obsolete membership semantics by default.

No invitation implementation begins until this choice is accepted.

### 7. Keep destructive organization authority SYSTEM-scoped

Actual organization suspension and deletion remain Platform Super Admin operations.

An organization-facing product may later provide a **request closure** workflow, but the request itself does not gain authority to execute system-scope suspend/delete.

OrganizationAdmin may continue to update safe organization profile fields where permitted; this does not imply destructive account authority.

### 8. Add an explicit reactivation system action before relying on suspension operationally

Suspension is incomplete as an operational lifecycle if there is no supported reactivation path.

Before commercial suspension is considered complete, Core should expose a Platform Super Admin reactivation action using the existing domain transition, with audit and lifecycle tests.

### 9. Suspension must have cross-repository product semantics

Core suspension already causes normal permission checks to fail because authorization requires an active organization. P0.2 must additionally define product-side behavior.

Proposed semantics:

- deny new normal user product requests immediately,
- block creation/start of new organization-owned background work,
- deterministically cancel, pause or drain already-running product jobs according to each job type,
- prevent new outbound mail/provider side effects,
- keep provider secrets encrypted but unusable while suspended,
- preserve data for reactivation until the retention/closure policy says otherwise,
- preserve Platform Super Admin diagnostic/support access according to the canonical bypass model,
- record the transition and resulting orchestration in audit evidence.

Exact job drain/cancel semantics must be specified per product capability; no generic Core job assumption may silently overwrite FAIR CRM behavior.

### 10. Organization deletion is the final step of an offboarding workflow, not the first step

Core's current delete is only a Core soft-delete. It must not be treated as complete customer data deletion.

A commercial closure sequence should be explicitly ordered:

```text
closure approved
  -> block new work
  -> settle/cancel active product work
  -> export if policy/user right requires it
  -> revoke/disable provider credentials
  -> apply product retention/anonymization/deletion policy
  -> handle generated files/artifacts
  -> define audit retention
  -> define backup ageing/restoration implications
  -> Core organization tombstone/soft-delete
```

Cross-repository product cleanup is orchestrated through public product/Core contracts. Core must not directly manipulate FAIR CRM tables.

### 11. Retention and legal-data policy remain decision blockers

P0.2 does not invent retention durations. Before destructive closure implementation, the maintainers must approve at least:

- business-data retention after cancellation/closure,
- anonymization versus hard delete by data class,
- audit/security log retention,
- generated-file retention,
- provider credential deletion/revocation timing,
- backup ageing and restore behavior,
- whether a closure grace/reactivation window exists.

These policy values feed P1.5 Data Lifecycle / KVKK-GDPR readiness and cannot be guessed from technical convenience.

## Required P0.2 decisions before implementation

| ID | Decision | Current baseline | Proposed direction | Status |
| --- | --- | --- | --- | --- |
| OL-01 | Who creates organizations? | Super Admin only | Keep Super Admin only for M4 | **PENDING ACCEPTANCE** |
| OL-02 | First normal admin role | OrganizationAdmin exists; Owner removed | Use OrganizationAdmin; no Owner | **PENDING ACCEPTANCE** |
| OL-03 | User ↔ organization model | Direct single `organization_id`; memberships removed | Keep single-org model for M4 | **PENDING ACCEPTANCE** |
| OL-04 | Team/user onboarding | Direct user creation exists; invites removed | Choose secure direct activation or new generic invitation capability | **OPEN CHOICE** |
| OL-05 | Self-service suspend/delete | SYSTEM scope | Keep execution Super Admin only; optional closure-request flow later | **PENDING ACCEPTANCE** |
| OL-06 | Reactivation | Domain transition exists; API missing | Add Super Admin reactivation API before operational use | **PENDING ACCEPTANCE** |
| OL-07 | Suspension job/provider behavior | No cross-repo lifecycle orchestration | Block new work; explicitly cancel/pause/drain existing work; disable side effects | **OPEN DETAIL** |
| OL-08 | Closure/export/retention/delete sequence | Not defined cross-repo | Staged offboarding before Core tombstone | **PENDING ACCEPTANCE** |
| OL-09 | Retention/grace durations | Not defined | Business/legal decision required | **OPEN CHOICE** |
| OL-10 | Backup restore implications | Not defined | Must be explicit before destructive closure | **OPEN CHOICE** |

## Acceptance / implementation gate

No P0.2 runtime implementation should begin from this ADR until the relevant decisions above are accepted.

Once accepted, implementation must be split by canonical ownership:

### Core-owned

- organization lifecycle API primitives,
- user/OrganizationAdmin bootstrap primitives where generic,
- generic account activation/invitation capability only if explicitly chosen,
- system-scope authorization enforcement,
- lifecycle audit records,
- reactivation primitive.

### FAIR CRM-owned

- product onboarding UX/orchestration,
- product job suspension/drain behavior,
- provider credential/product side-effect behavior,
- FAIR CRM export and product data lifecycle actions,
- first-value onboarding steps.

### Platform-owned

- lifecycle policy/ADR,
- cross-repository sequencing,
- retention/security governance,
- acceptance evidence and status synchronization.

## P0.2 exit criteria

P0.2 is complete only when:

- every OL decision required for the chosen commercial flow is Accepted or explicitly N/A,
- implementation matches the direct/current identity model or a separately accepted replacement,
- first organization + first OrganizationAdmin can be provisioned without direct SQL,
- the supported activation/invitation flow is production-safe,
- suspension blocks normal access and has deterministic product job/provider semantics,
- reactivation is supported if suspension is reversible,
- closure/export/retention/delete behavior is explicit,
- Core and FAIR CRM boundaries are preserved,
- lifecycle transitions and destructive actions are auditable,
- applicable Core/FAIR CRM/production-shaped gates are green,
- canonical roadmap/status/changelog are synchronized.

## Relationship to existing ADRs

If accepted, this ADR:

- extends ADR-0003 Organization-as-account semantics,
- keeps ADR-0003 Platform Super Admin invariant intact,
- keeps ADR-0005 `OrganizationAdmin` role governance intact,
- supersedes membership-specific implementation wording in ADR-0005 because Core migration 0057 removed memberships,
- does not authorize a new Owner role or self-service destructive organization action.

## Related

- [KYROX SaaS Readiness Roadmap](../SAAS_ROADMAP.md)
- [ADR-0002: Core and product separation](0002-core-product-separation.md)
- [ADR-0003: Identity security strategy](0003-identity-security-strategy.md)
- [ADR-0005: Role template and permission governance](0005-role-template-and-permission-governance.md)
- [Core Organization as Tenant Concept](../../projects/kyrox-core/decisions/0003-organization-as-tenant-concept.md)
- [Core Product Integration Guide](../../projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)
