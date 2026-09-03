# ADR-0006: Organization lifecycle and SaaS onboarding contract

- **Status:** Proposed — OL-01 through OL-05 accepted; remaining lifecycle decisions still gated
- **Date:** 2026-08-26
- **Deciders:** KYROX ecosystem maintainers
- **Roadmap gate:** P0.2 — Organization lifecycle contract and SaaS onboarding decisions

## Context

P0.1 tenant-isolation certification is complete. The next SaaS-readiness gate is to define how a commercial KYROX account is created, administered, suspended, reactivated and eventually closed without duplicating Core capabilities or leaking lifecycle semantics across repositories.

The current implementation has evolved beyond older membership-oriented documentation. This ADR records the verified current architecture first, then defines or proposes lifecycle decisions. The identity/onboarding subset was explicitly approved for implementation on 2026-08-27. OL-05 destructive lifecycle authority was accepted on 2026-09-03. Reactivation, suspension runtime behavior, closure sequencing, retention and backup decisions remain open, so the ADR as a whole remains Proposed.

The canonical implementation checklist for the completed onboarding subset is [P0.2 Identity / SaaS Onboarding Implementation Tracker](../P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md).

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
- Existing manual user creation requires an administrator-supplied password and currently applies only a minimal API boundary length check rather than one shared production password policy.
- Core user persistence allows `password_hash = NULL`, and inactive users already exist as a supported user state.
- Core authentication currently exposes login, refresh and logout, but no public signup, account activation/set-password, forgot/reset-password or authenticated self-service change-password flow.
- Core no longer has membership invitation/acceptance after migration 0057.
- Core notifications/jobs/settings infrastructure exists, but the current email channel is a log stub rather than a production identity-email sender.
- Existing logout revokes one supplied refresh token/session; user-wide credential/session invalidation is not yet exposed as a generic primitive.

### Cross-repository lifecycle reality

Core and FAIR CRM use separate persistence. Suspending or soft-deleting an organization in Core does not automatically:

- cancel or drain FAIR CRM background jobs,
- revoke or disable FAIR CRM provider credentials,
- export, retain, anonymize or delete FAIR CRM business data,
- expire product-generated files/artifacts,
- define backup ageing behavior for deleted organization data.

Those effects require an explicit lifecycle contract and product orchestration; they cannot be inferred from Core database cascades.

The [P0.2 lifecycle runtime audit](../P0_2_LIFECYCLE_RUNTIME_AUDIT.md) verifies the current suspension execution split in detail: Core blocks new normal permission-protected work after suspension, while already queued/running FAIR CRM scraper, enrichment, import and outbound-mail work generally proceeds from previously established organization-scoped job context without re-checking Core organization lifecycle state. Import background execution explicitly trusts queue-time authorization, and email delivery checks product email-account activity rather than Core organization status. This is an OL-07 lifecycle-policy gap, not a P0.1 tenant-isolation regression.

## Decision state

OL-01 through OL-05 are accepted. OL-01 through OL-04 onboarding/credential implementation is complete. OL-05 acceptance locks destructive lifecycle authority but is not `DONE` until implementation verification and certification are completed. Other lifecycle sections remain proposals/open choices until separately accepted.

### 1. Keep Organization as the only account boundary — APPROVED

Retain the current ADR-0003 model:

```text
Organization = customer/account boundary
organization_id = product/Core isolation key
Tenant = infrastructure terminology only
```

No new Tenant table/entity is created.

### 2. Keep the direct single-organization user model for current M4 — APPROVED

Use the current `identity_users.organization_id` model as the baseline for M4 rather than reintroducing memberships.

A future requirement for one normal user to participate in multiple organizations requires a separate accepted architecture change. It must not be smuggled into P0.2 as an implementation detail.

This decision supersedes membership-specific wording in ADR-0005 and older roadmap text where it describes implementation rather than a generic concept.

### 3. Do not create an Owner role — APPROVED

The first normal administrative user of an organization uses the existing `OrganizationAdmin` role. Platform-wide authority remains `is_super_admin` only.

No `Owner` role, role-name bypass or hidden ownership permission model is introduced.

### 4. Add public commercial signup without removing Platform Super Admin organization creation — APPROVED

The existing Platform Super Admin `POST /organizations` flow remains supported. Public commercial signup is an **additional** controlled onboarding path owned by Core identity/account lifecycle primitives and consumed by FAIR CRM through a thin public API bridge.

Public signup must define and implement:

- a non-operational pre-activation organization state such as `PENDING_ACTIVATION`, or an equivalent explicit state contract,
- first inactive normal user creation with no administrator-generated final password,
- `OrganizationAdmin` assignment,
- secure one-time account activation/set-password,
- duplicate/abuse controls,
- atomic rollback so failed bootstrap cannot leave a partially provisioned active organization,
- audit evidence without raw tokens/passwords,
- product bridge/UI integration without duplicating Core identity behavior.

This approval changes the earlier proposal that organization creation remain Super Admin-only for all M4 flows. Super Admin organization creation remains available; self-service public signup is added alongside it.

### 5. Define the first-user bootstrap explicitly — APPROVED

Public signup must provide one production-safe Core orchestration that results in:

```text
organization created in pre-activation state
  -> first normal user created inactive with password_hash = NULL
  -> OrganizationAdmin assigned
  -> one-time activation credential issued
  -> user sets own password
  -> user + organization activate
  -> user can authenticate
  -> user can reach FAIR CRM first-run flow
```

The bootstrap must be transactional/atomic and must not assign OrganizationAdmin to Platform Super Admin or rely on direct SQL.

### 6. Use generic Core account activation, not restored membership invitations — APPROVED

Core will implement a generic identity account activation/set-password mechanism that fits the current direct single-organization user model. It is not a restored membership invitation model.

The same generic identity/security foundation will support:

- public signup first-user activation,
- optional future Super Admin "send setup link" user creation alongside the existing manual-password create mode,
- forgot/reset password,
- authenticated password change,
- user-wide session/credential invalidation after credential changes.

Existing Super Admin manual user creation remains supported. The setup-link mode is additive and must not remove the current admin-supplied password path.

### 7. Keep destructive organization authority SYSTEM-scoped — ACCEPTED 2026-09-03

Organization suspension, closure and destructive deletion remain Platform SuperAdmin-controlled SYSTEM operations. OrganizationAdmin cannot directly execute these operations.

An organization-facing product may provide a **request closure** workflow, but the request itself does not gain authority to execute system-scope suspension, closure or destructive deletion.

OrganizationAdmin may continue to update safe organization profile fields where separately permitted; this does not imply destructive account authority.

All executed lifecycle transitions must be auditable. Audit evidence must identify the actor, target organization, transition and timestamp; a reason/context should be recorded where the operation contract supports it.

Acceptance of this decision locks the authority policy but does not by itself prove implementation completion. OL-05 becomes `DONE` only after Core and FAIR CRM behavior is verified against this contract, negative authorization cases are tested, SuperAdmin execution is tested, UI/direct-route behavior is consistent where applicable, and lifecycle audit evidence is proven. Any verified gap must be implemented before closure.

### 8. Add an explicit reactivation system action before relying on suspension operationally — PROPOSED

Suspension is incomplete as an operational lifecycle if there is no supported reactivation path.

Before commercial suspension is considered complete, Core should expose a Platform Super Admin reactivation action using the existing domain transition, with audit and lifecycle tests.

### 9. Suspension must have cross-repository product semantics — OPEN DETAIL

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

### 10. Organization deletion is the final step of an offboarding workflow, not the first step — PROPOSED

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

### 11. Retention and legal-data policy remain decision blockers — OPEN

P0.2 does not invent retention durations. Before destructive closure implementation, the maintainers must approve at least:

- business-data retention after cancellation/closure,
- anonymization versus hard delete by data class,
- audit/security log retention,
- generated-file retention,
- provider credential deletion/revocation timing,
- backup ageing and restore behavior,
- whether a closure grace/reactivation window exists.

These policy values feed P1.5 Data Lifecycle / KVKK-GDPR readiness and cannot be guessed from technical convenience.

## Required P0.2 decisions

| ID | Decision | Current baseline | Approved / proposed direction | Status |
| --- | --- | --- | --- | --- |
| OL-01 | Who creates organizations? | Existing endpoint Super Admin only | Keep Super Admin flow and add controlled public commercial signup | **APPROVED 2026-08-27** |
| OL-02 | First normal admin role | OrganizationAdmin exists; Owner removed | Use OrganizationAdmin; no Owner | **APPROVED 2026-08-27** |
| OL-03 | User ↔ organization model | Direct single `organization_id`; memberships removed | Keep single-org model for M4 | **APPROVED 2026-08-27** |
| OL-04 | Team/user onboarding | Direct manual user create exists; activation/reset absent | Generic Core activation/set-password + reset/change; keep manual Super Admin create | **APPROVED 2026-08-27** |
| OL-05 | Self-service suspend/delete | SYSTEM scope | Platform SuperAdmin-only execution; optional closure-request flow without destructive authority; lifecycle transitions auditable | **ACCEPTED 2026-09-03** |
| OL-06 | Reactivation | Domain transition exists; API missing | Add Super Admin reactivation API before operational use | **PENDING ACCEPTANCE** |
| OL-07 | Suspension job/provider behavior | New protected starts are denied, but queued/running scraper, enrichment, import and mail work generally does not re-check Core lifecycle state; outbound delivery relies on product account activity | Block new work; explicitly cancel/pause/drain existing work; disable side effects | **OPEN DETAIL** |
| OL-08 | Closure/export/retention/delete sequence | Not defined cross-repo | Staged offboarding before Core tombstone | **PENDING ACCEPTANCE** |
| OL-09 | Retention/grace durations | Not defined | Business/legal decision required | **OPEN CHOICE** |
| OL-10 | Backup restore implications | Not defined | Must be explicit before destructive closure | **OPEN CHOICE** |

## Implementation gate

The approved OL-01 through OL-04 onboarding/credential subset is implemented and tracked in [P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md](../P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md).

OL-05 is now accepted and authorized for implementation verification and any narrowly required remediation needed to satisfy the accepted authority/audit contract. Acceptance is not completion: OL-05 remains open until verification, tests and certification establish that the runtime matches the decision.

Runtime work for OL-06 through OL-10 remains gated until the relevant decisions are accepted. OL-05 acceptance must not be misread as acceptance of reactivation, suspension job/provider semantics, closure sequencing, retention durations or backup behavior.

Implementation ownership remains:

### Core-owned

- canonical password policy,
- hashed one-time identity action tokens,
- public organization signup/bootstrap primitive,
- first-user `OrganizationAdmin` bootstrap,
- account activation/set-password,
- forgot/reset/change password,
- user-wide session/credential invalidation,
- generic identity notification/email capability,
- identity/security audit records,
- existing Super Admin manual user/organization flows preserved,
- destructive organization lifecycle authority enforcement and Core lifecycle audit behavior for accepted OL-05.

### FAIR CRM-owned

- thin auth bridge endpoints/client extensions to public Core APIs,
- signup/activation/forgot/reset/change-password UX,
- existing Super Admin user-management UX compatibility plus optional setup-link mode,
- product first-value onboarding after authentication,
- UI/direct-route consistency with accepted OL-05 authority where FAIR CRM exposes organization lifecycle controls,
- product lifecycle behavior for still-open suspension/closure decisions.

### Platform-owned

- lifecycle/onboarding policy and ADR,
- cross-repository sequencing/checklists,
- retention/security governance,
- acceptance evidence and status synchronization.

## P0.2 exit criteria

P0.2 as a whole is complete only when:

- every OL decision required for the chosen commercial lifecycle is Accepted or explicitly N/A,
- implementation matches the direct/current identity model or a separately accepted replacement,
- public signup and first OrganizationAdmin provisioning are production-safe and atomic,
- supported activation/password recovery/change flows are production-safe,
- existing Super Admin manual organization/user creation remains functional,
- suspension blocks normal access and has deterministic product job/provider semantics,
- reactivation is supported if suspension is reversible,
- closure/export/retention/delete behavior is explicit,
- Core and FAIR CRM boundaries are preserved,
- lifecycle and identity-security transitions are auditable without leaking secrets,
- applicable Core/FAIR CRM/production-shaped gates are green,
- canonical roadmap/status/changelog are synchronized.

## Relationship to existing ADRs

This ADR's accepted decisions:

- extend ADR-0003 Organization-as-account semantics,
- keep ADR-0003 Platform Super Admin invariant intact,
- keep ADR-0005 `OrganizationAdmin` role governance intact,
- supersede membership-specific implementation wording in ADR-0005 because Core migration 0057 removed memberships,
- do not authorize a new Owner role or self-service destructive organization action,
- keep organization suspension, closure and destructive deletion as Platform SuperAdmin-controlled SYSTEM operations under OL-05.

The ADR remains Proposed overall until the remaining lifecycle decisions are resolved.

## Related

- [P0.2 Identity / SaaS Onboarding Implementation Tracker](../P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md)
- [P0.2 Organization Lifecycle Runtime Audit](../P0_2_LIFECYCLE_RUNTIME_AUDIT.md)
- [KYROX SaaS Readiness Roadmap](../SAAS_ROADMAP.md)
- [ADR-0002: Core and product separation](0002-core-product-separation.md)
- [ADR-0003: Identity security strategy](0003-identity-security-strategy.md)
- [ADR-0005: Role template and permission governance](0005-role-template-and-permission-governance.md)
- [Core Organization as Tenant Concept](../../projects/kyrox-core/decisions/0003-organization-as-tenant-concept.md)
- [Core Product Integration Guide](../../projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)
