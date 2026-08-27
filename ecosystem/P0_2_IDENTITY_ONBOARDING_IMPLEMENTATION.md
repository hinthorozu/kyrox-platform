# P0.2 Identity / SaaS Onboarding Implementation Tracker

**Status:** ACTIVE — implementation approved for the onboarding/credential workstream  
**Started:** 2026-08-27  
**Canonical owner:** `kyrox-platform` for architecture/tracking, `kyrox-core` for generic identity runtime, `fair-crm` for product bridge/UI  
**Parent:** [ADR-0006](decisions/0006-organization-lifecycle-and-onboarding.md) / [KYROX SaaS Readiness Roadmap](SAAS_ROADMAP.md)

This file is the canonical execution checklist for the first active P0.2 implementation workstream: public organization signup, first-user activation, password reset/change and the supporting Core security/session/notification primitives.

The purpose is to keep one durable answer to four questions:

1. What already exists?
2. What has been explicitly approved?
3. What still has to be built?
4. Where did implementation stop?

Do not delete completed checklist items. Mark them complete with evidence so the execution history survives later conversations and repository changes.

---

## 1. Approved contract

The following decisions are approved for implementation in this workstream.

- [x] `Organization` remains the canonical customer/account/tenant boundary; no parallel Tenant entity.
- [x] Core remains the single source of truth for identity/authentication/account credentials.
- [x] FAIR CRM must not implement its own password hashing, activation token store or independent identity database.
- [x] Public commercial signup is added **in addition to** existing Platform Super Admin organization creation; Super Admin creation is not removed.
- [x] The first normal user created through public signup receives the existing protected `OrganizationAdmin` role; no Owner role is introduced.
- [x] The current direct single-organization user model (`identity_users.organization_id`) remains the onboarding baseline; removed membership semantics are not restored.
- [x] Public signup uses secure account activation/set-password rather than an administrator-generated final password.
- [x] Existing Super Admin manual user creation remains available.
- [x] Super Admin user management may later offer a second "send setup link" mode without removing the current "admin sets password" mode.
- [x] Password reset and password change are Core-owned generic identity capabilities.
- [x] FAIR CRM continues to use a thin backend auth bridge to public Core APIs, matching the existing login/refresh/logout pattern.
- [x] Signup/bootstrap must be atomic: organization + first user + OrganizationAdmin assignment + activation token creation cannot leave a partially provisioned active account.
- [x] Raw activation/reset tokens, passwords and password hashes must never be logged or written to audit records.
- [x] Credential changes must invalidate prior authenticated sessions/credentials according to the final Core implementation contract.

### Out of scope for this tracker

The rest of ADR-0006 remains separately gated. This file does **not** accept or implement:

- organization suspension job/provider orchestration,
- closure/delete/export/retention policy,
- retention/grace durations,
- backup restoration policy,
- billing/entitlement behavior,
- multi-organization memberships,
- a new Owner role.

---

## 2. Verified existing baseline

### Core identity/authentication

- [x] Core has canonical user/organization/authentication persistence.
- [x] Normal users use direct `identity_users.organization_id` ownership.
- [x] Platform Super Admin uses `identity_users.is_super_admin = true` with no organization assignment.
- [x] Core exposes login, refresh and logout.
- [x] Core uses Argon2id password hashing.
- [x] `identity_users.password_hash` is nullable, which permits an inactive user with no password before activation.
- [x] User status already supports an inactive state.
- [x] Core has session and refresh-token persistence/revocation primitives.
- [x] Existing logout revokes the supplied refresh token and its single session.
- [ ] Core can revoke all active sessions/refresh credentials for a user.

### Organization / role baseline

- [x] Existing `POST /organizations` is Platform Super Admin-only.
- [x] Existing organization creation currently creates only the organization, not its first user.
- [x] Existing organization creation starts organizations as `ACTIVE`.
- [x] Existing organization status values are `ACTIVE`, `SUSPENDED`, `ARCHIVED`.
- [x] `OrganizationAdmin` exists as a protected, assignable organization-scoped role.
- [x] Legacy Owner role has been removed.
- [x] Existing manual user management can create a user and assign an organization role.
- [x] Existing manual user management allows an administrator-provided password.
- [x] Existing manual user password validation at the API boundary is currently only `min_length=1`; there is no shared production password policy.

### Activation / password recovery baseline

- [ ] Public organization signup exists.
- [ ] Account activation/set-password token capability exists.
- [ ] Forgot-password endpoint exists.
- [ ] Reset-password endpoint exists.
- [ ] Authenticated self-service change-password endpoint exists.
- [ ] One-time identity security token persistence exists.
- [ ] Central reusable password policy exists.

### Core notifications

- [x] Core has generic notifications, jobs and settings modules.
- [x] Notification model already supports recipient, subject/body, template key, idempotency and job linkage.
- [x] Core has an email notification channel abstraction.
- [x] Current Core email channel implementation is a log stub only.
- [ ] A real production Core identity email adapter/provider is configured.
- [ ] Notifications support platform-scoped recipients that have no `organization_id` (required for Super Admin credential flows).
- [ ] Identity templates exist for activation/reset/password-changed messages.

### FAIR CRM auth/product baseline

- [x] FAIR CRM frontend has `/login`.
- [x] FAIR CRM backend auth bridge proxies login/refresh/logout to Core rather than issuing credentials itself.
- [x] Refresh transport uses the existing FAIR CRM HttpOnly-cookie bridge pattern.
- [x] FAIR CRM has `/admin/system/users` and existing Super Admin/user-management UI surfaces.
- [ ] FAIR CRM has signup UI.
- [ ] FAIR CRM has activation UI.
- [ ] FAIR CRM has forgot-password UI.
- [ ] FAIR CRM has reset-password UI.
- [ ] FAIR CRM has authenticated security/change-password UI.

---

## 3. Target runtime flow

### 3.1 Public signup

```text
FAIR CRM /signup
  -> FAIR CRM auth bridge
  -> Core POST /api/v1/auth/signup
  -> one Core transaction:
       create PENDING_ACTIVATION organization
       create INACTIVE first user with password_hash = NULL
       assign OrganizationAdmin
       create one-time activation token
       enqueue activation notification
  -> generic success response
```

### 3.2 Activation

```text
activation email
  -> FAIR CRM /activate?token=...
  -> FAIR CRM auth bridge
  -> Core POST /api/v1/auth/activation/complete
  -> validate single-use token + expiry + purpose
  -> enforce PasswordPolicy
  -> set Argon2id password
  -> activate user
  -> activate organization
  -> consume token
  -> audit transition
  -> user returns to /login
```

### 3.3 Forgot/reset password

```text
FAIR CRM /forgot-password
  -> Core password/forgot through bridge
  -> same public response whether email exists or not
  -> rate limit / resend controls
  -> password-reset token + identity email
  -> FAIR CRM /reset-password?token=...
  -> Core password/reset
  -> PasswordPolicy
  -> update hash
  -> consume token
  -> revoke prior sessions/credentials
  -> audit
  -> login again
```

### 3.4 Authenticated password change

```text
FAIR CRM /settings/security
  -> current password + new password
  -> Core password/change through bridge
  -> verify current password
  -> PasswordPolicy
  -> reject no-op/same credential where applicable
  -> update hash
  -> revoke prior sessions/credentials
  -> audit
  -> clear FAIR CRM local/cookie session
  -> login again
```

### 3.5 Existing Super Admin manual create

```text
/admin/system/users
  -> existing manual create path remains supported
  -> Super Admin can still provide the user's password directly
```

A later extension in this same workstream may add:

```text
Create user mode:
  [manual password]
  [send setup link]
```

The setup-link mode is additive; it must not remove or silently change the current manual mode.

---

## 4. Required Core API contract

Final endpoint names may be adjusted only if Core's existing API conventions require it; semantics below are binding for this workstream.

| Capability | Core API | Auth | Status |
| --- | --- | --- | --- |
| Login | `POST /api/v1/auth/login` | Public | EXISTING |
| Refresh | `POST /api/v1/auth/refresh` | Refresh token | EXISTING |
| Logout | `POST /api/v1/auth/logout` | Refresh token | EXISTING |
| Public signup | `POST /api/v1/auth/signup` | Public | TODO |
| Complete activation | `POST /api/v1/auth/activation/complete` | One-time token | TODO |
| Forgot password | `POST /api/v1/auth/password/forgot` | Public | TODO |
| Reset password | `POST /api/v1/auth/password/reset` | One-time token | TODO |
| Change password | `POST /api/v1/auth/password/change` | Access token + current password | TODO |
| Existing manual user create | `/organizations/{organization_id}/users/manual` | RBAC | KEEP |

Public forgot-password responses must not reveal whether the email exists.

---

## 5. Core implementation checklist

### Phase CORE-01 — Password policy

- [ ] Add one reusable Core `PasswordPolicy` primitive.
- [ ] Apply it to public activation.
- [ ] Apply it to password reset.
- [ ] Apply it to authenticated password change.
- [ ] Apply it to existing manual user create/update so all password-setting paths have one policy.
- [ ] Decide and document production minimum length; initial design target is 12 characters with no forced composition gimmicks.
- [ ] Preserve maximum input limits and denial/error contract.
- [ ] Unit tests cover valid, too-short, too-long and Unicode/edge input.

**DONE when:** no password-setting path bypasses the shared policy and Core CI is green.

### Phase CORE-02 — One-time identity action tokens

- [ ] Add identity action-token domain model.
- [ ] Add migration/table for hashed one-time tokens.
- [ ] Support purposes at minimum `account_activation` and `password_reset`.
- [ ] Generate cryptographically random raw tokens.
- [ ] Persist only token hashes.
- [ ] Add expiry.
- [ ] Add `consumed_at` / one-use semantics.
- [ ] Invalidate or supersede older live token for the same user/purpose when reissued.
- [ ] Never expose raw token in logs/audit.
- [ ] Add deterministic repository/use-case tests for expiry, replay and purpose mismatch.

**DONE when:** raw token compromise cannot occur from Core persistence/logging and replay is rejected.

### Phase CORE-03 — Session / credential invalidation

- [ ] Extend session/refresh repositories with user-scoped active-session lookup/revocation.
- [ ] Add a reusable `revoke_all_for_user` application primitive.
- [ ] Ensure password reset revokes prior refresh sessions.
- [ ] Ensure password change revokes prior refresh sessions.
- [ ] Define and implement access-token invalidation/fail-closed semantics after a credential change; do not leave a long-lived pre-change access token effectively valid until natural expiry without an explicit accepted security reason.
- [ ] Tests prove all prior device/session credentials fail after reset/change.

**DONE when:** credential rotation has deterministic server-side session invalidation and stale credential tests pass.

### Phase CORE-04 — Core identity notifications / production email

- [ ] Extend notification ownership/scope so platform identity recipients without an organization can be notified safely.
- [ ] Preserve organization-scoped notification behavior.
- [ ] Add a real email adapter/provider implementation for Core notifications.
- [ ] Add identity activation template.
- [ ] Add password-reset template.
- [ ] Add password-changed/security-notice template if sent.
- [ ] Keep secret/provider configuration in Core/platform infrastructure, not FAIR CRM tenant SMTP configuration.
- [ ] Add idempotency tests.
- [ ] Add redaction/logging tests.

**DONE when:** Core can deliver production identity email independently of FAIR CRM product email accounts.

### Phase CORE-05 — Public signup + atomic bootstrap

- [ ] Add `PENDING_ACTIVATION` organization status or an equivalent explicit non-operational pre-activation state.
- [ ] Ensure normal authorization does not treat pre-activation organizations as active.
- [ ] Add public signup request/response contract.
- [ ] Validate/normalize organization name and generated/selected slug with existing Core policies.
- [ ] Reject/handle duplicate email and duplicate organization/slug safely.
- [ ] Create organization + first user + OrganizationAdmin assignment + activation token in one transaction/UoW.
- [ ] First user starts inactive with no password hash.
- [ ] First user is not a Super Admin.
- [ ] Existing Super Admin `POST /organizations` remains unchanged/available.
- [ ] Existing manual user create remains unchanged/available except shared password-policy hardening.
- [ ] Tests prove rollback leaves no orphan active organization/user/role assignment when any bootstrap step fails.

**DONE when:** a new commercial account can be provisioned without direct SQL and no partial account survives a failed signup transaction.

### Phase CORE-06 — Activation

- [ ] Add activation completion use case/API.
- [ ] Validate token hash, expiry, purpose, consumed state and target user.
- [ ] Enforce PasswordPolicy.
- [ ] Set Argon2id password hash.
- [ ] Activate user.
- [ ] Activate organization in the same transaction where required.
- [ ] Consume token atomically.
- [ ] Emit audit evidence without secrets.
- [ ] Reject expired/replayed/wrong-purpose tokens.

**DONE when:** activation is single-use, atomic and a newly activated OrganizationAdmin can authenticate normally.

### Phase CORE-07 — Forgot/reset password

- [ ] Add forgot-password API/use case.
- [ ] Return indistinguishable public response for existing/non-existing email.
- [ ] Add rate limiting / throttling strategy at the appropriate Core/edge layer.
- [ ] Add resend cooldown / token supersession behavior.
- [ ] Add reset-password API/use case.
- [ ] Enforce PasswordPolicy.
- [ ] Consume reset token atomically.
- [ ] Revoke old sessions/credentials.
- [ ] Add audit evidence.
- [ ] Tests cover enumeration resistance, expiry, replay, invalid token, inactive/deleted user policy and successful login with new password only.

**DONE when:** password recovery is production-safe and user enumeration/replay tests pass.

### Phase CORE-08 — Authenticated password change

- [ ] Add authenticated change-password API/use case.
- [ ] Require current password verification.
- [ ] Enforce PasswordPolicy on new password.
- [ ] Define/reject same-password change.
- [ ] Update hash atomically.
- [ ] Revoke prior sessions/credentials.
- [ ] Add audit evidence.
- [ ] Tests cover wrong current password and session invalidation.

**DONE when:** authenticated users can securely change their own password through Core without admin intervention.

### Phase CORE-09 — Core security/adversarial certification

- [ ] Activation replay test.
- [ ] Reset replay test.
- [ ] Expired token tests.
- [ ] Wrong-purpose token tests.
- [ ] Raw-token-not-persisted test.
- [ ] Secret/token log redaction test.
- [ ] User enumeration test.
- [ ] Rate-limit/cooldown tests where deterministic.
- [ ] Bootstrap rollback/atomicity tests.
- [ ] OrganizationAdmin bootstrap role test.
- [ ] Normal user cannot self-assert Super Admin during signup.
- [ ] Cross-organization isolation tests for any new organization/user identifier path.
- [ ] Existing Super Admin manual create regression test.
- [ ] Existing login/refresh/logout regression tests.
- [ ] Core final-head CI green.

**DONE when:** final implementation head passes the Core gate with no unresolved security or tenant-isolation regression.

---

## 6. FAIR CRM backend bridge checklist

### Phase CRM-BE-01 — Core client extensions

- [ ] Extend `CoreAuthClient` with signup.
- [ ] Extend with activation complete.
- [ ] Extend with forgot password.
- [ ] Extend with reset password.
- [ ] Extend with authenticated change password.
- [ ] Preserve thin-client behavior; no Core token validation/business logic is copied into FAIR CRM.
- [ ] Preserve safe error mapping and avoid leaking Core/provider internals.

### Phase CRM-BE-02 — Bridge routes

- [ ] Add `POST /api/v1/auth/signup` bridge route.
- [ ] Add activation-complete bridge route.
- [ ] Add forgot-password bridge route.
- [ ] Add reset-password bridge route.
- [ ] Add change-password bridge route.
- [ ] Keep existing login/refresh/logout routes unchanged unless the shared transport contract requires a compatible extension.
- [ ] Keep CSRF/cookie rules correct for cookie-authenticated mutating paths.
- [ ] Clear refresh cookie after successful password change/reset when required by the final session contract.

**DONE when:** FAIR CRM remains a transport bridge and all credential authority remains in Core.

---

## 7. FAIR CRM frontend/UI checklist

### Phase CRM-UI-01 — Public auth routes

- [ ] Add `/signup` route/page.
- [ ] Add `/activate` route/page.
- [ ] Add `/forgot-password` route/page.
- [ ] Add `/reset-password` route/page.
- [ ] Ensure public auth routes do not require an authenticated product session.
- [ ] Add labels, validation and accessible loading/error/success states.

### Phase CRM-UI-02 — Login integration

- [ ] Add "Şifremi unuttum" link to login.
- [ ] Add "Hesap oluştur" link to login.
- [ ] Preserve current login behavior.
- [ ] Activation success returns user to login rather than silently issuing an implicit product session unless implementation evidence justifies a different accepted choice.

### Phase CRM-UI-03 — Security settings

- [ ] Add authenticated `/settings/security` or the canonical account/security route.
- [ ] Current-password field.
- [ ] New-password field.
- [ ] Confirmation UX if UI standard requires it.
- [ ] Successful change clears local/session state and returns to login.

### Phase CRM-UI-04 — Super Admin user-management compatibility

- [ ] Existing manual create flow remains visible and functional.
- [ ] Existing manual password entry remains supported.
- [ ] Add optional "send setup link" mode only after Core setup-token capability is available.
- [ ] Protected role assignment rules remain backend-authoritative.
- [ ] No UI change creates a new Super Admin assignment path.

**DONE when:** both commercial self-service and existing operator-driven account provisioning work through the same Core identity authority.

---

## 8. Cross-repository acceptance / E2E checklist

- [ ] New organization signup creates exactly one organization and first OrganizationAdmin.
- [ ] Pre-activation user cannot log in.
- [ ] Pre-activation organization cannot use normal FAIR CRM APIs.
- [ ] Activation link permits password set once.
- [ ] Reusing activation link fails safely.
- [ ] Activated user can log in through FAIR CRM bridge.
- [ ] Forgot-password response is indistinguishable for unknown email.
- [ ] Reset link works once and expires.
- [ ] Old password fails after reset.
- [ ] Prior refresh/session credentials fail after reset/change.
- [ ] New password succeeds after reset/change.
- [ ] Existing Super Admin manual organization creation still works.
- [ ] Existing Super Admin manual user creation still works.
- [ ] Organization A activation/user identifiers cannot mutate/read Organization B state.
- [ ] Permanent ABC ↔ XYZ tenant-isolation system gate remains green.
- [ ] FAIR CRM unit/integration tests green.
- [ ] Development Standard Gate green on final head.
- [ ] Prod-Path E2E green on final head where applicable.
- [ ] Core CI green on final Core head.

---

## 9. Documentation / governance checklist

- [x] Implementation direction explicitly approved on 2026-08-27.
- [x] Canonical cross-repository tracker created in `kyrox-platform`.
- [ ] ADR-0006 records OL-01/02/03/04 onboarding sub-decisions as approved for implementation while remaining lifecycle decisions stay open.
- [ ] `ecosystem/SAAS_ROADMAP.md` marks this onboarding/credential workstream active and removes stale wording that password reset/email verification are merely deferred candidates.
- [ ] `ecosystem/STATUS.md` points to this tracker and records current phase.
- [ ] `projects/kyrox-core/ROADMAP.md` promotes the approved generic identity work as active product-driven Core work.
- [ ] `projects/fair-crm/ROADMAP.md` promotes the bridge/UI portion as active FAIR CRM work.
- [ ] Project status/changelog documents are updated as each implementation PR actually merges; planning checkboxes must not claim runtime delivery before code exists.
- [ ] Final completion synchronizes Core/FAIR CRM/Platform status, roadmaps and changelogs.

---

## 10. Execution order / current position

The implementation order is intentionally dependency-first:

1. **Platform planning/governance record** — this tracker + ADR/roadmap/status synchronization.
2. **CORE-01** PasswordPolicy.
3. **CORE-02** one-time identity action tokens.
4. **CORE-03** user-wide session/credential invalidation.
5. **CORE-04** Core production identity notifications/email.
6. **CORE-05** atomic public signup/bootstrap.
7. **CORE-06** activation.
8. **CORE-07** forgot/reset password.
9. **CORE-08** authenticated password change.
10. **CORE-09** adversarial/security certification and final Core CI.
11. **CRM-BE-01/02** FAIR CRM Core client + auth bridge.
12. **CRM-UI-01/02/03/04** public auth/security/Super Admin compatibility UI.
13. **Cross-repository E2E / tenant-isolation / production-shaped gates.**
14. **Platform final documentation closure.**

### Current position

- [x] Architecture/runtime audit completed.
- [x] User approved the identity/onboarding implementation direction.
- [x] Implementation tracker drafted.
- [ ] Platform documentation PR merged.
- [ ] **NEXT RUNTIME PHASE: CORE-01 — PasswordPolicy.**

When work resumes, start from the first unchecked item in this section unless a failed CI/security finding requires returning to an earlier phase.

---

## 11. Definition of DONE for this workstream

This tracker may be marked DONE only when all of the following are true:

- public signup is production-safe and atomic,
- first user is the existing OrganizationAdmin role and no Owner role was introduced,
- account activation is single-use, expiring and does not persist raw tokens,
- forgot/reset password resists user enumeration and replay,
- authenticated password change verifies the current credential,
- all password-setting paths use one Core password policy,
- credential changes invalidate prior sessions/credentials deterministically,
- Core can send identity/security email independently of FAIR CRM tenant email configuration,
- FAIR CRM remains a thin Core consumer for identity,
- FAIR CRM has signup/activation/forgot/reset/change-password UX,
- existing Super Admin manual organization/user creation remains functional,
- tenant isolation and permission invariants remain intact,
- required Core, FAIR CRM Development Standard and production-shaped gates are green on the final implementation heads,
- canonical Platform/Core/FAIR CRM status/roadmap/changelog documents are synchronized.

Until then, this file remains **ACTIVE** and the first unchecked execution item is the canonical resume point.
