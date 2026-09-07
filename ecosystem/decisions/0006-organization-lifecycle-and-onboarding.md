# ADR-0006: Organization lifecycle and SaaS onboarding contract

- **Status:** Proposed — OL-01 through OL-07 accepted and implementation/certification complete; OL-08 through OL-10 unresolved
- **Date:** 2026-08-26
- **Deciders:** KYROX ecosystem maintainers
- **Roadmap gate:** P0.2 — Organization lifecycle contract and SaaS onboarding decisions

## Context

P0.1 tenant-isolation certification is complete. The next SaaS-readiness gate is to define how a commercial KYROX account is created, administered, suspended, reactivated and eventually closed without duplicating Core capabilities or leaking lifecycle semantics across repositories.

The current implementation has evolved beyond older membership-oriented documentation. This ADR records the verified current architecture first, then defines or proposes lifecycle decisions. The identity/onboarding subset was explicitly approved for implementation on 2026-08-27 and completed on 2026-08-29. OL-05 destructive organization authority was accepted and implementation-certified on 2026-09-03. OL-06 reactivation was accepted on 2026-09-03 and implementation-certified on 2026-09-04 through KYROX Core PR #23. OL-07 suspension/job/provider/reactivation product semantics were implementation-certified on 2026-09-07 through FAIR CRM PRs #249–#254. Closure/offboarding sequencing, retention and backup implications remain open, so the ADR as a whole remains Proposed.

The canonical implementation checklist for the approved onboarding subset is [P0.2 Identity / SaaS Onboarding Implementation Tracker](../P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md). OL-05 completion evidence is retained in [P0.2 OL-05 Destructive Organization Authority Implementation Tracker](../P0_2_OL_05_IMPLEMENTATION.md). OL-06 completion evidence is retained in [P0.2 OL-06 Organization Reactivation Implementation Tracker](../P0_2_OL_06_IMPLEMENTATION.md). OL-07 completion evidence is retained in [P0.2 OL-07 Suspension Job / Provider Behavior Implementation Tracker](../P0_2_OL_07_IMPLEMENTATION.md).

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
- `identity.organizations.delete`, `identity.organizations.suspend`, and `identity.organizations.reactivate` are SYSTEM-scope, non-assignable permissions; organization roles cannot receive them.
- Normal authorization requires the organization to be active, so suspended organizations fail normal RBAC checks.
- Current Core organization delete is a soft delete (`deleted_at`); it does not hard-delete product data in another repository/database.
- The domain `reactivate` transition permits only `SUSPENDED -> ACTIVE`.
- KYROX Core PR #23 added the explicit reactivation API, permission and audit contract and was squash-merged to Core `main` as `f24089cbb29f38b42270d0d9edb2235aa7815719` after CI #88 passed.

### Current onboarding capability

- Core user management can create a user directly inside an organization and assign an available role.
- Existing manual user creation requires an administrator-supplied password and currently applies only a minimal API boundary length check rather than one shared production password policy.
- Core user persistence allows `password_hash = NULL`, and inactive users already exist as a supported user state.
- Core authentication currently exposes login, refresh and logout, but no public signup, account activation/set-password, forgot/reset-password or authenticated self-service change-password flow.
- Core no longer has membership invitation/acceptance after migration 0057.
- Core notifications/jobs/settings infrastructure exists, but the current email channel is a log stub rather than a production identity-email sender.
- Existing logout revokes one supplied refresh token/session; user-wide credential/session invalidation is not yet exposed as a generic primitive.

### Cross-repository lifecycle reality

Core and FAIR CRM use separate persistence. Suspending or soft-deleting an organization in Core does not automatically manipulate FAIR CRM tables or provider state. Cross-repository effects therefore require explicit public lifecycle contracts and product-owned orchestration.

OL-07 now defines the certified suspension/reactivation runtime split: Core remains lifecycle authority; FAIR CRM checks that authority at queued-work start, running-work safe checkpoints and immediately before outbound provider handoff. Explicit suspension terminalizes covered queued/running work according to the certified state machines, blocks new provider handoff, preserves provider configuration/credentials, and never fabricates provider recall after handoff starts. Reactivation restores eligibility for fresh/new work and safely deferred non-terminal work but does not resurrect suspension-cancelled work or auto-resend ambiguous provider outcomes.

## Decision state

OL-01 through OL-07 are accepted and their implementation/certification workstreams are complete. OL-08 through OL-10 remain proposals/open choices until separately accepted.

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

### 7. Keep destructive organization authority SYSTEM-scoped — ACCEPTED / DONE 2026-09-03

**Organization suspension, closure and destructive deletion remain Platform SuperAdmin-controlled SYSTEM operations. OrganizationAdmin cannot directly execute these operations. An organization-facing closure-request workflow may be provided, but such a request does not grant destructive lifecycle authority. All executed lifecycle transitions must be auditable.**

Operational meaning:

- actual organization suspension is executable only by Platform SuperAdmin/system authority,
- actual organization closure/destructive lifecycle execution is executable only by Platform SuperAdmin/system authority,
- OrganizationAdmin cannot obtain destructive lifecycle authority through an organization-scoped role,
- a future organization-facing **request closure** workflow is allowed, but the request is only a request and never grants SYSTEM-scope suspend/delete authority,
- safe organization-profile updates may remain organization-scoped where separately permitted,
- executed lifecycle transitions must create auditable evidence identifying the actor, target organization, transition and timestamp.

Implementation/certification evidence:

- KYROX Core PR #21 added explicit audit evidence for successful suspend/delete transitions and certified anonymous denial, organization-user denial, cross-organization spoof denial, Platform SuperAdmin success and no mutation on rejected requests.
- KYROX Core PR #22 added the direct regression proving a SYSTEM-scope lifecycle permission cannot be assigned to an organization-role template, even by Platform SuperAdmin, and that no role-permission association is persisted after the rejected request.
- Current FAIR CRM integration does not expose an alternate product-owned lifecycle authority that widens the Core SYSTEM boundary; organization lifecycle mutations remain Core-authoritative.
- The canonical completion record is [P0.2 OL-05 Destructive Organization Authority Implementation Tracker](../P0_2_OL_05_IMPLEMENTATION.md).

**Scope boundary:** Core organization delete remains a Core soft-delete/tombstone. This OL-05 completion certifies **authority**, not FAIR CRM product-data cleanup, export, retention, anonymization or hard-delete sequencing. Those remain OL-08 scope.

### 8. Keep organization reactivation SYSTEM-scoped and limited to SUSPENDED -> ACTIVE — ACCEPTED / DONE 2026-09-04

**Organization reactivation is a Platform SuperAdmin-controlled SYSTEM lifecycle operation. Core exposes an explicit reactivation action using the existing domain transition. Reactivation is valid only for a non-deleted organization in `SUSPENDED` state and transitions it to `ACTIVE`. Successful reactivation must be auditable.**

Operational meaning:

- actual reactivation is executable only by Platform SuperAdmin/system authority,
- `OrganizationAdmin` and normal organization users cannot obtain or execute reactivation authority through organization RBAC,
- `SUSPENDED -> ACTIVE` is the only valid reactivation transition,
- `ACTIVE`, `PENDING_ACTIVATION`, and `ARCHIVED` organizations are not reactivated through this action,
- soft-deleted/tombstoned organizations are not revived through this action,
- rejected reactivation attempts do not mutate organization lifecycle state or create successful-reactivation audit evidence,
- successful reactivation creates audit evidence identifying actor, target organization, transition and timestamp,
- Core reactivation restores canonical organization lifecycle state; product-side resumption then follows the separately certified OL-07 rules rather than an implicit restart contract.

Implementation/certification evidence:

- KYROX Core PR #23 added `identity.organizations.reactivate` as a SYSTEM-scoped, non-assignable permission, `POST /organizations/{organization_id}/reactivate`, existing-domain-transition reuse, `identity.organization.reactivated` audit evidence, authorization/source-state/soft-delete coverage and migration install/repair/downgrade coverage.
- Core PR #23 final head `655b61155e0ad799d7381d21858c9fd1d5b3a0f7` passed CI #88 and was squash-merged to Core `main` as `f24089cbb29f38b42270d0d9edb2235aa7815719`.
- The canonical completion record is [P0.2 OL-06 Organization Reactivation Implementation Tracker](../P0_2_OL_06_IMPLEMENTATION.md).

**Scope boundary:** OL-06 restores only the canonical Core organization state. Deterministic FAIR CRM suspension/reactivation job/provider behavior is defined and certified by OL-07; closure/export/retention/delete behavior remains OL-08+ scope.

### 9. Suspension must have cross-repository product semantics — ACCEPTED / DONE 2026-09-07

**Suspension and reactivation have deterministic FAIR CRM execution semantics. Core remains lifecycle authority; FAIR CRM owns product-job/provider behavior and fails closed when lifecycle authority cannot be trusted.**

Operational meaning:

- new normal user product requests remain blocked by active-organization authorization semantics,
- queued/pending organization-owned FAIR CRM work is lifecycle-gated before start and explicit suspension terminalizes covered queued work as cancelled,
- already-running covered work observes lifecycle at safe checkpoints and suspension stops before the next safe unit with owned transaction rollback where applicable,
- a final lifecycle checkpoint immediately before real SMTP/provider dispatch prevents new outbound side effects after suspension,
- provider account configuration and encrypted credentials are preserved through suspension rather than lifecycle-deactivated or deleted,
- once provider handoff starts, FAIR CRM does not synthesize recall; ambiguous MailerSend/SMTP handoff outcomes are terminal non-auto-retry to prevent duplicate sends,
- the claimed mail operation is durably `SENDING` before external handoff; checkpoint commit failure touches no provider and recovers the SQLAlchemy session before safe retry bookkeeping,
- Core `SUSPENDED -> ACTIVE` restores eligibility for fresh/new work and non-terminal work deferred only by temporary lifecycle-authority outage,
- reactivation does **not** resurrect suspension-cancelled queued/running work,
- reactivation does **not** auto-resend cancelled mail or ambiguous provider-handoff outcomes,
- newly created outbound work after reactivation may use the same preserved configured provider account without a lifecycle credential re-enable mutation.

Implementation/certification evidence:

- KYROX Core PR #25 and FAIR CRM PR #249 established the dedicated product lifecycle snapshot contract and fail-closed consumer guard.
- FAIR CRM PR #250 certified pre-start cancellation of queued work.
- FAIR CRM PR #251 certified cooperative cancellation of already-running work at safe checkpoints.
- FAIR CRM PR #252 certified the final pre-provider lifecycle checkpoint and provider credential preservation.
- FAIR CRM PR #253 certified durable `SENDING`, real-session checkpoint commit recovery and ambiguous in-flight provider no-auto-retry semantics; final head `c94be579f071deb7de8ed340690c4d88d5d71c93` passed Development Standard Gate #696 and Prod-Path E2E #261 and merged as `4f52961341bc4d80c4a576fa85525aa511d68b82`.
- FAIR CRM PR #254 certified deterministic reactivation/resumption across terminalized queued work, lifecycle-authority outage deferral, mail worker selection and preserved provider credentials; final head `e17593e49ecb25a3aef736b0ceaa1fafa14c7e77` passed Development Standard Gate #700 and Prod-Path E2E #264 and squash-merged as `18b0b638ba946c2910698e1df7c4ab5283c4958f`.
- The canonical completion record is [P0.2 OL-07 Suspension Job / Provider Behavior Implementation Tracker](../P0_2_OL_07_IMPLEMENTATION.md).

**Scope boundary:** OL-07 certifies suspension and reactivation runtime behavior only. Organization closure/export/retention/anonymization/delete sequencing, retention/grace periods and backup ageing/restoration remain OL-08 through OL-10.

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
| OL-01 | Who creates organizations? | Existing endpoint Super Admin only | Keep Super Admin flow and add controlled public commercial signup | **APPROVED 2026-08-27 / DONE** |
| OL-02 | First normal admin role | OrganizationAdmin exists; Owner removed | Use OrganizationAdmin; no Owner | **APPROVED 2026-08-27 / DONE** |
| OL-03 | User ↔ organization model | Direct single `organization_id`; memberships removed | Keep single-org model for M4 | **APPROVED 2026-08-27 / DONE** |
| OL-04 | Team/user onboarding | Direct manual user create exists; activation/reset absent | Generic Core activation/set-password + reset/change; keep manual Super Admin create | **APPROVED 2026-08-27 / DONE** |
| OL-05 | Self-service suspend/delete authority | SYSTEM scope | Execution Platform SuperAdmin only; optional closure-request flow later; transitions auditable | **ACCEPTED 2026-09-03 / DONE** |
| OL-06 | Reactivation | Domain transition exists; API missing on certified baseline | Platform SuperAdmin-only SYSTEM action; only `SUSPENDED -> ACTIVE`; explicit Core API + audit | **ACCEPTED 2026-09-03 / DONE 2026-09-04** |
| OL-07 | Suspension job/provider behavior | Previously queued/running product work and outbound mail could outlive Core suspension without deterministic product re-checks | Lifecycle-gate queued/running/provider boundaries; preserve credentials; no implicit restart/resend on reactivation | **ACCEPTED / DONE 2026-09-07** |
| OL-08 | Closure/export/retention/delete sequence | Not defined cross-repo | Staged offboarding before Core tombstone | **PENDING ACCEPTANCE** |
| OL-09 | Retention/grace durations | Not defined | Business/legal decision required | **OPEN CHOICE** |
| OL-10 | Backup restore implications | Not defined | Must be explicit before destructive closure | **OPEN CHOICE** |

## Implementation gate

The OL-01 through OL-04 onboarding/credential subset is complete and tracked in [P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md](../P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md).

OL-05 is accepted and its destructive-authority implementation/certification is complete, tracked in [P0_2_OL_05_IMPLEMENTATION.md](../P0_2_OL_05_IMPLEMENTATION.md).

OL-06 is accepted and its implementation/certification is complete, tracked in [P0_2_OL_06_IMPLEMENTATION.md](../P0_2_OL_06_IMPLEMENTATION.md). Core PR #23 / CI #88 is the certified runtime implementation evidence.

OL-07 is accepted and its cross-repository suspension/provider/reactivation implementation/certification is complete, tracked in [P0_2_OL_07_IMPLEMENTATION.md](../P0_2_OL_07_IMPLEMENTATION.md). FAIR CRM PRs #249–#254 are the certified product runtime evidence, ending with PR #254 merge `18b0b638ba946c2910698e1df7c4ab5283c4958f` after Development Standard Gate #700 and Prod-Path E2E #264 passed the final head.

Runtime work for OL-08 through OL-10 remains gated until the relevant decisions are accepted. Completion of OL-07 must not be misread as acceptance of closure/offboarding sequencing, retention or backup behavior.

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
- SYSTEM-scoped destructive organization authority and its audit evidence,
- SYSTEM-scoped organization reactivation authority, canonical `SUSPENDED -> ACTIVE` transition and its audit evidence.

### FAIR CRM-owned

- thin auth bridge endpoints/client extensions to public Core APIs,
- signup/activation/forgot/reset/change-password UX,
- existing Super Admin user-management UX compatibility plus optional setup-link mode,
- product first-value onboarding after authentication,
- certified OL-07 product lifecycle behavior for suspension, provider handoff and reactivation/resumption,
- product lifecycle behavior for still-open closure/offboarding decisions only after OL-08+ acceptance.

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
- preserve SYSTEM-only destructive organization authority and do not authorize self-service destructive organization action,
- preserve SYSTEM-only organization reactivation authority and limit the Core action to `SUSPENDED -> ACTIVE`,
- define deterministic FAIR CRM suspension/provider/reactivation runtime semantics through accepted OL-07 without granting implicit restart/resend behavior.

The ADR remains Proposed overall until OL-08 through OL-10 are resolved.

## Related

- [P0.2 Identity / SaaS Onboarding Implementation Tracker](../P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md)
- [P0.2 OL-05 Destructive Organization Authority Implementation Tracker](../P0_2_OL_05_IMPLEMENTATION.md)
- [P0.2 OL-06 Organization Reactivation Implementation Tracker](../P0_2_OL_06_IMPLEMENTATION.md)
- [P0.2 OL-07 Suspension Job / Provider Behavior Implementation Tracker](../P0_2_OL_07_IMPLEMENTATION.md)
- [P0.2 Organization Lifecycle Runtime Audit](../P0_2_LIFECYCLE_RUNTIME_AUDIT.md)
- [KYROX SaaS Readiness Roadmap](../SAAS_ROADMAP.md)
- [ADR-0002: Core and product separation](0002-core-product-separation.md)
- [ADR-0003: Identity security strategy](0003-identity-security-strategy.md)
- [ADR-0005: Role template and permission governance](0005-role-template-and-permission-governance.md)
- [Core Organization as Tenant Concept](../../projects/kyrox-core/decisions/0003-organization-as-tenant-concept.md)
- [Core Product Integration Guide](../../projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)