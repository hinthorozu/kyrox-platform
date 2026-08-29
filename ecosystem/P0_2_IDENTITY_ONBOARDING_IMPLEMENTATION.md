# P0.2 Identity / SaaS Onboarding Implementation Tracker

**Status:** DONE — approved onboarding/credential workstream completed 2026-08-29  
**Started:** 2026-08-27  
**Completed:** 2026-08-29  
**Current resume point:** `P0.2 identity/onboarding slice complete; remaining ADR-0006 lifecycle decisions remain separately gated`  
**Canonical owner:** `kyrox-platform` for architecture/tracking, `kyrox-core` for generic identity runtime, `fair-crm` for product bridge/UI  
**Parent:** [ADR-0006](decisions/0006-organization-lifecycle-and-onboarding.md) / [KYROX SaaS Readiness Roadmap](SAAS_ROADMAP.md)

This file is the canonical execution checklist for the completed P0.2 identity/onboarding implementation workstream: public organization signup, first-user activation, password reset/change and the supporting Core security/session/notification primitives.

The purpose is to keep one durable answer to four questions:

1. What already exists?
2. What has been explicitly approved?
3. What was built and certified?
4. What remains outside this workstream?

Do not delete completed checklist items. Keep evidence so the execution history survives later conversations and repository changes.

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
- [x] Core can revoke all active sessions/refresh credentials for a user through the reusable CORE-03 primitive.

### Organization / role baseline

- [x] Existing `POST /organizations` is Platform Super Admin-only.
- [x] Existing organization creation currently creates only the organization, not its first user.
- [x] Existing organization creation starts organizations as `ACTIVE`.
- [x] Core organization status now includes `PENDING_ACTIVATION` alongside `ACTIVE`, `SUSPENDED`, `ARCHIVED` — delivered by Core PR #16.
- [x] `OrganizationAdmin` exists as a protected, assignable organization-scoped role.
- [x] Legacy Owner role has been removed.
- [x] Existing manual user management can create a user and assign an organization role.
- [x] Existing manual user management allows an administrator-provided password.
- [x] Before CORE-01, manual user password validation at the API boundary was only `min_length=1`; CORE-01 replaced that with the shared Core PasswordPolicy.

### Activation / password recovery baseline

- [x] Public organization signup exists — delivered by Core PR #16; FAIR CRM backend bridge is delivered through PRs #86/#87 and public UI through PR #88.
- [x] Account activation/set-password API exists — delivered by Core PR #17 as `POST /api/v1/auth/activation/complete` using the generic one-time token primitive from CORE-02.
- [x] Forgot-password endpoint exists — delivered by Core PR #18 as `POST /api/v1/auth/password/forgot` with enumeration-safe public behavior and resend throttling/cooldown.
- [x] Reset-password endpoint exists — delivered by Core PR #18 as `POST /api/v1/auth/password/reset` with one-time token consumption, shared PasswordPolicy and credential invalidation.
- [x] Authenticated self-service change-password endpoint exists — delivered by Core PR #19 as `POST /api/v1/auth/password/change` with current-password verification and credential invalidation.
- [x] One-time identity security token persistence exists — delivered by Core PR #13 on 2026-08-27.
- [x] Central reusable password policy exists — delivered by Core PR #12 on 2026-08-27.

### Core notifications

- [x] Core has generic notifications, jobs and settings modules.
- [x] Notification model supports recipient, subject/body, template key, idempotency and job linkage.
- [x] Core has an email notification channel abstraction.
- [x] Core preserves the redacted log email adapter for development/test and has a configurable Core-owned SMTP production adapter delivered by Core PR #15.
- [x] Notifications and their internal dispatch jobs support platform-scoped recipients with no `organization_id` while preserving organization-scoped behavior.
- [x] Generic identity templates exist for activation, password reset and password-changed/security messages.

### FAIR CRM auth/product baseline

- [x] FAIR CRM frontend has `/login`.
- [x] FAIR CRM backend auth bridge proxies login/refresh/logout to Core rather than issuing credentials itself.
- [x] FAIR CRM backend auth bridge also proxies signup/activation/forgot/reset/change-password to Core through CRM-BE-01/02.
- [x] Refresh transport uses the existing FAIR CRM HttpOnly-cookie bridge pattern.
- [x] FAIR CRM has `/admin/system/users` and existing Super Admin/user-management UI surfaces.
- [x] FAIR CRM has signup UI — delivered through PR #88.
- [x] FAIR CRM has activation UI — delivered through PR #88.
- [x] FAIR CRM has forgot-password UI — delivered through PR #88.
- [x] FAIR CRM has reset-password UI — delivered through PR #88.
- [x] FAIR CRM has authenticated security/change-password UI — delivered through PR #90.

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

A later extension may add:

```text
Create user mode:
  [manual password]
  [send setup link]
```

The setup-link mode is additive and remains deferred until Core has an approved setup-token contract; the completed workstream does not invent that contract.

---

## 4. Required Core API contract

Final endpoint names may be adjusted only if Core's existing API conventions require it; semantics below are binding for this workstream.

| Capability | Core API | Auth | Status |
| --- | --- | --- | --- |
| Login | `POST /api/v1/auth/login` | Public | EXISTING |
| Refresh | `POST /api/v1/auth/refresh` | Refresh token | EXISTING |
| Logout | `POST /api/v1/auth/logout` | Refresh token | EXISTING |
| Public signup | `POST /api/v1/auth/signup` | Public | DELIVERED CORE-05 |
| Complete activation | `POST /api/v1/auth/activation/complete` | One-time token | DELIVERED CORE-06 |
| Forgot password | `POST /api/v1/auth/password/forgot` | Public | DELIVERED CORE-07 |
| Reset password | `POST /api/v1/auth/password/reset` | One-time token | DELIVERED CORE-07 |
| Change password | `POST /api/v1/auth/password/change` | Access token + current password | DELIVERED CORE-08 |
| Existing manual user create | `/organizations/{organization_id}/users/manual` | RBAC | KEEP |

Public forgot-password responses must not reveal whether the email exists.

---

## 5. Core implementation checklist

### Phase CORE-01 — Password policy — DONE 2026-08-27

- [x] Add one reusable Core `PasswordPolicy` primitive.
- [x] Apply it to existing manual user create/update so current password-setting paths use one policy.
- [x] Set the production minimum to 12 characters with no forced composition gimmicks.
- [x] Set and enforce the production maximum at 255 characters.
- [x] Keep Argon2id focused on hashing/verification rather than embedding password rules in infrastructure.
- [x] Return a safe 422 denial/error contract without echoing the submitted password.
- [x] Unit tests cover valid, too-short, too-long, Unicode and non-echoed-error cases.
- [x] Future activation, reset and authenticated change-password phases retain explicit `Enforce PasswordPolicy` checklist items below; no nonexistent endpoint is falsely marked delivered by CORE-01.

**Evidence:** Core PR #12 final head `15db64cba636b340ee0841e25137d2bbea2dbd93`; CI #57 / run `33093204127` SUCCESS; merged to Core `main` as `323cfa750a0c731bd15de11dfbd19e83858dc1f7`.

**DONE:** shared policy exists, current manual password-setting paths use it, tests are green, and later password-setting endpoints are required to reuse it.

### Phase CORE-02 — One-time identity action tokens — DONE 2026-08-27

- [x] Add identity action-token domain model.
- [x] Add migration/table for hashed one-time tokens.
- [x] Support purposes at minimum `account_activation` and `password_reset`.
- [x] Generate cryptographically random raw tokens.
- [x] Persist only token hashes.
- [x] Add expiry.
- [x] Add `consumed_at` / one-use semantics.
- [x] Invalidate or supersede older live token for the same user/purpose when reissued.
- [x] Never expose raw token in logs/audit.
- [x] Add deterministic repository/use-case tests for expiry, replay and purpose mismatch.

**Evidence:** Core PR #13 final head `fe3408a52667f0d8f3c6bb3de8bdedc3b9745809`; Core CI #60 / run `33097948707` SUCCESS with `348 passed`; merged to Core `main` as `f1f88e7f12a7d38d3f917d05840c8562f6f0287a`. Migration `20260827_0063` has direct upgrade/downgrade schema tests proving the action-token table contains only hashed token material and no raw-token column. The workflow's `Run lint` step reported success but explicitly skipped Ruff because Ruff is not installed, so lint execution is not claimed as separate evidence.

**DONE:** raw token compromise from Core action-token persistence/logging is prevented by the implemented contract, reissue supersedes older live same-purpose tokens, and replay/purpose/expiry checks are deterministic.

### Phase CORE-03 — Session / credential invalidation primitive — DONE 2026-08-27

- [x] Extend session/refresh repositories with user-scoped active-session and active-refresh-token lookup.
- [x] Add reusable `RevokeAllUserSessionsUseCase` / revoke-all-for-user application primitive.
- [x] Revoke target-user live refresh credentials with `SESSION_REVOKED` and revoke active sessions while leaving other users untouched.
- [x] Make protected access-token validation fail closed unless JWT `sid` resolves to an active server-side session owned by JWT `sub`.
- [x] Tests cover target-user scoping, idempotent revoke-all, inconsistent active-token/revoked-session cleanup, revoked/deleted session rejection and `sid`/`sub` ownership mismatch.
- [x] CORE-07 password reset invokes the reusable primitive and proves prior credentials fail after reset — delivered by Core PR #18.
- [x] CORE-08 password change invokes the reusable primitive and proves prior access/refresh credentials fail after change — delivered by Core PR #19.

**Evidence:** Core PR #14 final head `1b2dff1c5613405273ebe673210d522977e8d0c5`; Core CI #63 / run `33102833407` SUCCESS with `352 passed`; merged to Core `main` as `63889c6c29a73b3224cdda0da21ed2bcc9ac9cb4`. No schema migration was required. CORE-07 integrated this primitive into password reset through Core PR #18; CORE-08 integrated it into authenticated password change through Core PR #19 and proves both the submitting access-token session and prior refresh token fail after successful change. The workflow's `Run lint` step again explicitly skipped Ruff because Ruff is not installed, so no separate Ruff lint execution is claimed.

**DONE:** Core has deterministic server-side user-wide session/refresh invalidation, stale access tokens fail immediately when their server-side session is revoked/deleted/mismatched, and both password-reset and authenticated password-change paths invoke the same reusable primitive.

### Phase CORE-04 — Core identity notifications / production email — DONE 2026-08-27

- [x] Extend notification ownership/scope so platform identity recipients without an organization can be notified safely.
- [x] Preserve organization-scoped notification behavior.
- [x] Add a real email adapter/provider implementation for Core notifications.
- [x] Add identity activation template.
- [x] Add password-reset template.
- [x] Add password-changed/security-notice template if sent.
- [x] Keep secret/provider configuration in Core/platform infrastructure, not FAIR CRM tenant SMTP configuration.
- [x] Add idempotency tests.
- [x] Add redaction/logging tests.

**Evidence:** Core PR #15 final head `271124290858e0447af5ac90adc58436ccadf5a4`; Core CI #64 / run `33109701064` SUCCESS; merged to Core `main` as `09617df8a17aa2ac744b5b1a9692d6418bbf0899`. Migration `20260827_0064_platform_identity_notifications` makes notification/job `organization_id` nullable for explicit platform scope and adds dedicated partial unique idempotency constraints for platform-scoped notifications and jobs. Core now has configurable SMTP delivery with separate `CORE_EMAIL_*` / `CORE_SMTP_*` environment configuration, while the existing log adapter remains the default development/test provider. Tests cover platform-scoped enqueue/idempotent replay, identity template contracts, SMTP dispatch, generic provider-failure mapping, recipient/credential/action-token log redaction and direct migration upgrade/downgrade behavior. The workflow's `Run lint` step reported success; separate Ruff execution is not claimed because the workflow only executes Ruff when available.

**DONE:** Core can deliver identity/security email independently of FAIR CRM tenant/product email accounts and can represent/queue platform identity recipients without inventing an organization. Token-bearing activation/reset integrations delivered later preserve the workstream-wide rule that raw activation/reset token material is not persisted or logged.

### Phase CORE-05 — Public signup + atomic bootstrap — DONE 2026-08-28

- [x] Add `PENDING_ACTIVATION` organization status or an equivalent explicit non-operational pre-activation state.
- [x] Ensure normal authorization does not treat pre-activation organizations as active.
- [x] Add public signup request/response contract.
- [x] Validate/normalize organization name and generated/selected slug with existing Core policies.
- [x] Reject/handle duplicate email and duplicate organization/slug safely.
- [x] Create organization + first user + OrganizationAdmin assignment + activation token in one transaction/UoW.
- [x] First user starts inactive with no password hash.
- [x] First user is not a Super Admin.
- [x] Existing Super Admin `POST /organizations` remains unchanged/available.
- [x] Existing manual user create remains unchanged/available except shared password-policy hardening.
- [x] Tests prove rollback leaves no orphan active organization/user/role assignment when any bootstrap step fails.

**Evidence:** Core PR #16 final head `052a2ac16c906bf854ea79917550fae04b44a2d1`; Core CI #70 / run `33119509255` SUCCESS with `363 passed`; merged to Core `main` as `8e406c9e286f494026edfe460ab7ca4156c2fe4d`. No schema migration was required; migration head remains `20260827_0064_platform_identity_notifications`. The public `POST /api/v1/auth/signup` path creates the pending organization, inactive/passwordless/non-Super-Admin first user, protected `OrganizationAdmin` assignment, activation action token, platform notification and dispatch job on the same request database session. A forced late notification failure plus request rollback leaves no orphan organization/user/role/token. Activation notification/job persistence contains only the safe action-token UUID reference; the raw activation token and token-bearing action URL are derived/materialized only in memory during dispatch and are absent from persisted notification/job payloads, API response and captured logs. Existing Platform Super Admin organization create and manual user/password provisioning remain separate compatible paths. The workflow's `Run lint` step reported success but explicitly skipped Ruff because Ruff is not installed, so separate Ruff execution is not claimed.

**DONE:** a new commercial account can be provisioned through Core without direct SQL, remains non-operational until activation, receives exactly the existing protected first-admin role at bootstrap, and no partial signup state survives a failed bootstrap transaction.

### Phase CORE-06 — Activation — DONE 2026-08-28

- [x] Add activation completion use case/API.
- [x] Validate token hash, expiry, purpose, consumed state and target user.
- [x] Enforce PasswordPolicy.
- [x] Set Argon2id password hash.
- [x] Activate user.
- [x] Activate organization in the same transaction where required.
- [x] Consume token atomically.
- [x] Emit audit evidence without secrets.
- [x] Reject expired/replayed/wrong-purpose tokens.

**Evidence:** Core PR #17 final head `f4649d86863eccbfaf531d29353cfa2048041cdc`; Core CI #71 / run `33198567633` SUCCESS with `368 passed`; merged to Core `main` as `66dfdc373724509450e9ee2aed45f876b2935d1a`. No schema migration was required; migration head remains `20260827_0064_platform_identity_notifications`. `POST /api/v1/auth/activation/complete` applies the shared `PasswordPolicy` before token consumption, atomically consumes an `account_activation` token, requires the expected inactive/passwordless/non-Super-Admin user and `pending_activation` organization state, sets the Argon2id password hash, activates user and organization in the same request `DbSession`, and writes secret-safe `identity.activation.complete` audit evidence. Tests cover success, weak-password non-consumption, replay, expiry, wrong-purpose tokens, audit-failure rollback, absence of raw token/password from persisted audit/response/captured logs, and successful login with the newly set password. Activation returns the user to login and does not issue an implicit session. The workflow's `Run lint` step reported success but explicitly printed `ruff not installed, skipping`, so separate Ruff lint execution is not claimed.

**DONE:** activation is single-use and atomic, weak-password attempts do not consume a valid activation token, and a newly activated OrganizationAdmin can authenticate normally with the password set through Core.

### Phase CORE-07 — Forgot/reset password — DONE 2026-08-29

- [x] Add forgot-password API/use case.
- [x] Return indistinguishable public response for existing/non-existing email.
- [x] Add rate limiting / throttling strategy at the appropriate Core/edge layer through deterministic database-backed account resend cooldown.
- [x] Add resend cooldown / token supersession behavior.
- [x] Add reset-password API/use case.
- [x] Enforce PasswordPolicy.
- [x] Consume reset token atomically.
- [x] Revoke old sessions/credentials using the CORE-03 primitive.
- [x] Add audit evidence.
- [x] Tests cover enumeration resistance, expiry, replay, invalid token, inactive/deleted user policy, prior credential invalidation and successful login with new password only.

**Evidence:** Core PR #18 final head `7529f82689b970991314e9621feaa0341fe3f0a2`; Core CI #78 / run `33227509093` SUCCESS with `375 passed, 120 warnings in 19.07s`; merged to Core `main` as `db5695d2c77a8e2dbe29dd19f4a3cb22d770e7d8`. No schema migration was required; migration head remains `20260827_0064_platform_identity_notifications`. Public `POST /api/v1/auth/password/forgot` normalizes the email, returns the same 202 response for known/unknown/non-eligible accounts, limits recoverable accounts to active credential-bearing users in active organizations (or the supported Super Admin account shape), applies a 60-second database-backed resend cooldown, and reuses CORE-02 supersession when a new reset token is issued after cooldown. Reset notification persistence contains only the action-token UUID reference; raw reset token/action URL material is reconstructed in memory at dispatch. Public `POST /api/v1/auth/password/reset` validates the shared `PasswordPolicy` before token consumption, atomically consumes a `password_reset` token, replaces the Argon2id credential, invokes CORE-03 user-wide session/refresh invalidation and records secret-safe `identity.password.reset` audit evidence. Tests cover enumeration-safe responses, cooldown/supersession, raw-token non-persistence/log redaction, weak-password non-consumption, expiry/replay/invalid-token handling, inactive/deleted account policy, prior refresh/session invalidation, old-password rejection and successful login with the new password. The workflow's `Run lint` step reported success but explicitly printed `ruff not installed, skipping`, so separate Ruff lint execution is not claimed.

**DONE:** password recovery is production-safe at the Core contract level, user enumeration is suppressed, reset tokens are expiring/single-use/superseded, secrets remain out of persistence/logging/audit, and successful reset invalidates prior credentials before the user logs in again.

### Phase CORE-08 — Authenticated password change — DONE 2026-08-29

- [x] Add authenticated change-password API/use case.
- [x] Require current password verification.
- [x] Enforce PasswordPolicy on new password.
- [x] Define/reject same-password change.
- [x] Update hash atomically.
- [x] Revoke prior sessions/credentials using the CORE-03 primitive.
- [x] Add audit evidence.
- [x] Tests cover wrong current password and session/credential invalidation.

**Evidence:** Core PR #19 final head `ecb77f8918e9a156b686eb902c50692e92de3339`; Core CI #82 / run `33228044257` SUCCESS with `379 passed, 120 warnings in 20.96s`; merged to Core `main` as `75905f02bdf621419f9b6560fff5809e56150ad5`. No schema migration was required; migration head remains `20260827_0064_platform_identity_notifications`. Authenticated `POST /api/v1/auth/password/change` requires a valid Bearer access token whose `sid` resolves to an active server-side session owned by `sub`, verifies the current password before mutation, applies the shared `PasswordPolicy`, rejects same-password/no-op changes, replaces the Argon2id credential, invokes CORE-03 to revoke all live sessions/refresh credentials including the submitting session, writes secret-safe `identity.password.change` audit evidence and issues no replacement session. Tests prove missing authentication fails, wrong-current/weak/same-password attempts do not revoke the existing session, successful change makes the old access and refresh credentials fail, rejects the old password, permits fresh login with the new password, keeps plaintext current/new passwords out of response/log/audit evidence, and rolls back the password hash plus session/refresh revocations if a later audit write fails. The workflow's `Run lint` step reported success but explicitly printed `ruff not installed, skipping`, so separate Ruff lint execution is not claimed.

**DONE:** authenticated users can securely change their own password through Core, failed validation attempts do not disturb the existing authenticated session, and a successful change deterministically invalidates all prior credentials before a new login.

### Phase CORE-09 — Core security/adversarial certification — DONE 2026-08-29

- [x] Activation replay test.
- [x] Reset replay test.
- [x] Expired token tests.
- [x] Wrong-purpose token tests.
- [x] Raw-token-not-persisted test.
- [x] Secret/token log redaction test.
- [x] User enumeration test.
- [x] Rate-limit/cooldown tests where deterministic.
- [x] Bootstrap rollback/atomicity tests.
- [x] OrganizationAdmin bootstrap role test.
- [x] Normal user cannot self-assert Super Admin during signup.
- [x] Cross-organization isolation tests for any new organization/user identifier path.
- [x] Existing Super Admin manual create regression test.
- [x] Existing login/refresh/logout regression tests.
- [x] Core final-head CI green.

**Evidence:** Core PR #20 final head `5c5113320ea910e80555e6cc526ed0c708580cd4`; Core CI #84 / run `33228476878` SUCCESS with `381 passed, 120 warnings in 20.99s`; merged to Core `main` as `f6cbf417410d9148c225242790103d8cc9541f21`. No runtime code or schema migration changed in CORE-09; the migration head remains `20260827_0064_platform_identity_notifications`. The final-head suite re-ran activation/reset replay, expiry and wrong-purpose coverage, raw-token non-persistence and secret/log redaction, forgot-password enumeration resistance and deterministic cooldown/supersession, signup bootstrap rollback/atomicity and protected `OrganizationAdmin` assignment, reset/change credential invalidation, existing Platform Super Admin/manual provisioning regressions and login/refresh/logout regressions. CORE-09 also added explicit adversarial API tests proving signup payloads cannot self-assert `is_super_admin` or inject a privileged role and that an Organization A activation token activates only its bound user/organization while leaving Organization B pending/passwordless with its token untouched. The workflow's `Run lint` step again explicitly printed `ruff not installed, skipping`, so separate Ruff lint execution is not claimed.

**DONE:** the completed Core onboarding/credential implementation passes the final Core gate with no unresolved security or tenant-isolation regression in the certified surface. Core implementation is handed off to the FAIR CRM thin bridge/UI phases.

---

## 6. FAIR CRM backend bridge checklist

### Phase CRM-BE-01 — Core client extensions — DONE 2026-08-29

- [x] Extend `CoreAuthClient` with signup.
- [x] Extend with activation complete.
- [x] Extend with forgot password.
- [x] Extend with reset password.
- [x] Extend with authenticated change password.
- [x] Preserve thin-client behavior; no Core token validation/business logic is copied into FAIR CRM.
- [x] Preserve safe error mapping and avoid leaking Core/provider internals.

**Evidence:** FAIR CRM PR #86 final head `934a7d1843bf5f036f06225393af2af4aa3810ce`; Development Standard Gate #278 SUCCESS with `1767 passed`; Prod-Path E2E #148 SUCCESS; merged to FAIR CRM `main` as `a83fa9a11dd603962cbb29510a0b11748f886d9f`. The existing `CoreAuthClient` was extended with signup, activation-complete, forgot/reset and authenticated change-password transport only. Public Core 4xx details remain available for product UX, provider/Core 5xx internals are sanitized, malformed success responses fail closed, and no password policy, action-token validation/persistence or credential mutation was copied into FAIR CRM. No FAIR CRM schema migration was required.

### Phase CRM-BE-02 — Bridge routes — DONE 2026-08-29

- [x] Add `POST /api/v1/auth/signup` bridge route.
- [x] Add activation-complete bridge route.
- [x] Add forgot-password bridge route.
- [x] Add reset-password bridge route.
- [x] Add change-password bridge route.
- [x] Keep existing login/refresh/logout routes unchanged unless the shared transport contract requires a compatible extension.
- [x] Keep CSRF/cookie rules correct for cookie-authenticated mutating paths.
- [x] Clear refresh cookie after successful password change/reset when required by the final session contract.

**Evidence:** FAIR CRM PR #87 final head `1068a5a94d26799e6b63565e18cf6a61e5699a72`; Development Standard Gate #280 / run `33230174837` SUCCESS with `1781 passed, 2 warnings`; Prod-Path E2E #149 / run `33230174828` SUCCESS; merged to FAIR CRM `main` as `0c8a0004f5067dbd8041898a1fe590026c22d736`. Public signup/activation/forgot/reset bridge routes do not require an authenticated cookie/CSRF header; authenticated password change requires a single Bearer access token and forwards it to Core without local JWT credential authority. Successful reset/change clears the FAIR CRM refresh cookie because Core invalidates prior sessions, while failed change validation does not clear a still-valid cookie. Existing login/refresh/logout behavior remains unchanged. No FAIR CRM schema migration was required.

**DONE:** FAIR CRM remains a transport bridge and all credential authority remains in Core.

---

## 7. FAIR CRM frontend/UI checklist

### Phase CRM-UI-01 — Public auth routes — DONE 2026-08-29

- [x] Add `/signup` route/page.
- [x] Add `/activate` route/page.
- [x] Add `/forgot-password` route/page.
- [x] Add `/reset-password` route/page.
- [x] Ensure public auth routes do not require an authenticated product session.
- [x] Add labels, validation and accessible loading/error/success states.

**Evidence:** FAIR CRM PR #88 final head `3111660795f001d37e899e40abda9d880a3aa1d5`; Development Standard Gate #291 / run `33233202519` SUCCESS with `56 passed` frontend test files / `307 passed` tests, production Vite build success and zero-new UI-governance violations; merged to FAIR CRM `main` as `9265dbb24b13e404c8a18cdd21918948a3997b06`. Public auth screens render outside the authenticated `AuthProvider`/product app, use the existing shared `PageShell`/Card/Banner/FormField UI system, consume only the thin FAIR CRM auth bridge, and do not introduce product-local credential authority. Activation/reset tokens are captured from the link, removed from the browser address bar after initial render, never displayed/logged and passed only to the bridge/Core. No FAIR CRM schema migration was required. This frontend-only change did not produce a separate Prod-Path E2E run, so no Prod-Path result is claimed for CRM-UI-01.

### Phase CRM-UI-02 — Login integration — DONE 2026-08-29

- [x] Add "Şifremi unuttum" link to login.
- [x] Add "Hesap oluştur" link to login.
- [x] Preserve current login behavior.
- [x] Activation success returns user to login rather than silently issuing an implicit product session unless implementation evidence justifies a different accepted choice.

**Evidence:** FAIR CRM PR #89 final head `298dcadbd88df5580db97d7c5f0305570e2c3e26`; Development Standard Gate #293 / run `33233998091` SUCCESS with `57` frontend test files / `308` tests passed, production Vite build success and zero-new UI-governance regression PASS; merged to FAIR CRM `main` as `874c24b1c4c56ea7087e3acd6ea0708117e3a1a3`. The existing login authentication/session flow is unchanged; the login screen now exposes the already-delivered public `/forgot-password` and `/signup` routes. Focused rendering coverage locks the link labels/targets. CRM-UI-01 already established that activation success returns explicitly to login with no implicit product session, and CRM-UI-02 preserves that behavior. No backend or FAIR CRM schema migration changed. This frontend-only phase did not produce a separate Prod-Path E2E run, so no Prod-Path result is claimed for CRM-UI-02.

### Phase CRM-UI-03 — Security settings — DONE 2026-08-29

- [x] Add authenticated `/settings/security` route.
- [x] Current-password field.
- [x] New-password field.
- [x] Confirmation UX.
- [x] Successful change clears local/session state and returns to login.

**Evidence:** FAIR CRM PR #90 final head `d99dcec064a9fecb9452729aca490a1f9f76a849`; Development Standard Gate #300 / run `33234676182` SUCCESS; merged to FAIR CRM `main` as `c40bd8518eca2561640c00de0537d8e0e0e85fbb`. The authenticated security screen uses the existing FAIR CRM/Core bridge, forwards one Bearer access token, and keeps current-password verification, PasswordPolicy, hashing and mutation in Core. On successful Core change, prior Core sessions are revoked, the FAIR CRM bridge clears the refresh cookie, frontend local auth state is cleared and the user returns to `/login`. Failed validation/current-password/policy responses leave the existing local session intact. No backend, schema, product RBAC or credential-authority change was introduced.

### Phase CRM-UI-04 — Super Admin user-management compatibility — DONE 2026-08-29

- [x] Existing manual create flow remains visible and functional.
- [x] Existing manual password entry remains supported.
- [x] Confirm optional "send setup link" mode remains deferred until an approved Core setup-token capability exists; no unsupported UI path is added.
- [x] Protected role assignment rules remain backend-authoritative.
- [x] No UI change creates a new Super Admin assignment path.

**Evidence:** FAIR CRM PR #91 final head `a5730c767ff1274484bfe9ddaa55c948cf4d73f9`; Development Standard Gate #303 / run `33235256876` SUCCESS; merged to FAIR CRM `main` as `b6cd8b8c9baebee54d83334f4c5669ea1564106e`. The test-only compatibility certification locks `/admin/system/users` to the existing administrator-supplied password flow and Core `POST /api/v1/organizations/{organization_id}/users/manual` transport. FAIR CRM passes the password through unchanged, role selection remains required for normal users, and Super Admin controls remain conditional on Core's `can_manage_super_admin` response. No production runtime, backend, schema, permission-catalog or UI behavior changed.

**DONE:** both commercial self-service and existing operator-driven account provisioning use the same Core identity authority without adding product-local credential ownership.

---

## 8. Cross-repository acceptance / E2E checklist

- [x] New organization signup creates exactly one organization and first OrganizationAdmin — CORE-05 atomic bootstrap/role evidence plus the final product lifecycle signup path.
- [x] Pre-activation user cannot log in — CORE-05/06 inactive/passwordless activation contract.
- [x] Pre-activation organization cannot use normal FAIR CRM APIs — pending organizations are non-operational and cannot produce an authenticated normal-user product session before activation.
- [x] Activation link permits password set once — CORE-06 plus final PR #92 lifecycle certification.
- [x] Reusing activation link fails safely — final PR #92 requires replay rejection.
- [x] Activated user can log in through FAIR CRM bridge — final PR #92 lifecycle certification.
- [x] Forgot-password response is indistinguishable for unknown email — CORE-07 enumeration-resistance tests and unchanged thin FAIR CRM transport.
- [x] Reset link works once and expires — CORE-07 expiry/single-use tests; final PR #92 also requires replay rejection through the product path.
- [x] Old password fails after reset — final PR #92 lifecycle certification.
- [x] Prior refresh/session credentials fail after reset/change — final PR #92 rejects both prior access and refresh credentials after each credential mutation.
- [x] New password succeeds after reset/change — final PR #92 logs in successfully after both reset and password change.
- [x] Existing Super Admin manual organization creation still works — CORE-05/09 regression coverage preserves the existing Platform Super Admin organization path.
- [x] Existing Super Admin manual user creation still works — CORE-09 plus CRM-UI-04 compatibility certification.
- [x] Organization A activation/user identifiers cannot mutate/read Organization B state — CORE-09 explicit cross-organization activation-token certification.
- [x] Permanent ABC ↔ XYZ tenant-isolation system baseline remains intact — P0.1 remains certified; subsequent P0.2 changes do not weaken tenant ownership, and final Prod-Path #151 passed the existing production-shaped regression suite with 35 passed / 0 failed.
- [x] FAIR CRM unit/integration coverage green across the delivered backend/UI phases; the final certification PR is CI-only and adds no runtime code.
- [x] Development Standard Gate green on final FAIR CRM certification head — #306 / run `33246959509` on `d498245c4c60bd36b9b3a8aeffed4912e198123b`.
- [x] Prod-Path E2E green on final FAIR CRM certification head — #151 / run `33246959442` on the same head; existing gate 35 passed / 0 failed plus P0.2 lifecycle PASS.
- [x] Core CI green on final Core head — Core CI #84 / run `33228476878` on `5c5113320ea910e80555e6cc526ed0c708580cd4` with 381 tests passed.

### Final cross-repository certification evidence

FAIR CRM PR #92 final head `d498245c4c60bd36b9b3a8aeffed4912e198123b` passed Development Standard Gate #306 / run `33246959509` and Prod-Path E2E #151 / run `33246959442`, then merged to `main` as `2f9f159a303ffd055121547de51dcaefc15fc6a9`. The lifecycle gate runs FAIR CRM against real KYROX Core `main` at `f6cbf417410d9148c225242790103d8cc9541f21` and exercises Core's real SMTP adapter with an in-process memory-only SMTP sink. It certifies signup → activation → login → forgot/reset → login → password change → login; activation/reset replay is rejected and pre-credential-change access/refresh credentials are rejected after reset/change. The script keeps raw action tokens, generated passwords and session material process-local and does not persist or upload them. PR #92 changes CI/test/governance only; no FAIR CRM/Core application runtime or schema behavior changed.

---

## 9. Documentation / governance checklist

- [x] Implementation direction explicitly approved on 2026-08-27.
- [x] Canonical cross-repository tracker created in `kyrox-platform`.
- [x] ADR-0006 records OL-01/02/03/04 onboarding sub-decisions as approved for implementation while remaining lifecycle decisions stay open.
- [x] `ecosystem/SAAS_ROADMAP.md` promotes the onboarding/credential workstream without treating still-gated suspension/closure decisions as approved.
- [x] `ecosystem/STATUS.md` points to this tracker and records completion of the approved onboarding slice.
- [x] `projects/kyrox-core/ROADMAP.md` records the approved generic identity work as delivered product-driven Core work.
- [x] `projects/fair-crm/ROADMAP.md` records the bridge/UI/certification portion as DONE.
- [x] Platform planning/governance PR #12 merged as `c0b9d543437a95343032929364c331a1504fc9b0` after Platform Standards CI #35 / run `33091623466` succeeded on final head `20ac02c263071f06753298c657c165c2bdabb73f`.
- [x] CORE-01 implementation evidence synchronized after Core PR #12.
- [x] CORE-02 implementation evidence synchronized after Core PR #13.
- [x] CORE-03 implementation evidence synchronized after Core PR #14.
- [x] CORE-04 implementation evidence synchronized after Core PR #15.
- [x] CORE-05 implementation evidence synchronized after Core PR #16.
- [x] CORE-06 implementation evidence synchronized after Core PR #17.
- [x] CORE-07 implementation evidence synchronized after Core PR #18.
- [x] CORE-08 implementation evidence synchronized after Core PR #19.
- [x] CORE-09 final Core security/adversarial certification evidence synchronized after Core PR #20.
- [x] CRM-BE-01 and CRM-BE-02 FAIR CRM backend bridge evidence synchronized after PRs #86/#87.
- [x] CRM-UI-01 public auth UI evidence synchronized after PR #88.
- [x] CRM-UI-02 login-integration evidence synchronized after PR #89.
- [x] CRM-UI-03 security-settings evidence synchronized after PR #90.
- [x] CRM-UI-04 Super Admin compatibility evidence synchronized after PR #91.
- [x] Final cross-repository lifecycle certification evidence synchronized after FAIR CRM PR #92.
- [x] FAIR CRM project status, roadmap, changelog and ecosystem status are synchronized by the final Platform closure change.
- [x] Final completion preserves the explicit boundary that ADR-0006 suspension/closure/retention/billing lifecycle decisions remain open.

---

## 10. Execution order / final position

The implementation order was intentionally dependency-first:

1. **Platform planning/governance record** — tracker + ADR/roadmap/status synchronization. ✅
2. **CORE-01** PasswordPolicy. ✅
3. **CORE-02** one-time identity action tokens. ✅
4. **CORE-03** user-wide session/credential invalidation. ✅
5. **CORE-04** Core production identity notifications/email. ✅
6. **CORE-05** atomic public signup/bootstrap. ✅
7. **CORE-06** activation. ✅
8. **CORE-07** forgot/reset password. ✅
9. **CORE-08** authenticated password change. ✅
10. **CORE-09** adversarial/security certification and final Core CI. ✅
11. **CRM-BE-01** FAIR CRM Core client extensions. ✅
12. **CRM-BE-02** FAIR CRM auth bridge routes. ✅
13. **CRM-UI-01** public auth routes. ✅
14. **CRM-UI-02** login integration. ✅
15. **CRM-UI-03** security settings. ✅
16. **CRM-UI-04** Super Admin compatibility certification. ✅
17. **Cross-repository identity lifecycle / production-shaped gates.** ✅
18. **Platform final documentation closure.** ✅

### Final position

- [x] Architecture/runtime audit completed and implementation direction approved.
- [x] CORE-01 through CORE-09 delivered and Core final-head CI green.
- [x] CRM-BE-01/02 delivered through FAIR CRM PRs #86/#87 with applicable Development Standard and Prod-Path evidence.
- [x] CRM-UI-01/02 delivered through FAIR CRM PRs #88/#89 with frontend test/build/UI-governance evidence.
- [x] CRM-UI-03 delivered through FAIR CRM PR #90; final head `d99dcec064a9fecb9452729aca490a1f9f76a849`; Development Standard Gate #300 / run `33234676182` SUCCESS; merge `c40bd8518eca2561640c00de0537d8e0e0e85fbb`.
- [x] CRM-UI-04 compatibility certification delivered through FAIR CRM PR #91; final head `a5730c767ff1274484bfe9ddaa55c948cf4d73f9`; Development Standard Gate #303 / run `33235256876` SUCCESS; merge `b6cd8b8c9baebee54d83334f4c5669ea1564106e`.
- [x] Final cross-repository lifecycle certification delivered through FAIR CRM PR #92; final head `d498245c4c60bd36b9b3a8aeffed4912e198123b`; Development Standard Gate #306 / run `33246959509` SUCCESS; Prod-Path E2E #151 / run `33246959442` SUCCESS; merge `2f9f159a303ffd055121547de51dcaefc15fc6a9`.
- [x] The approved identity/onboarding workstream is complete. There is no next runtime phase in this tracker.
- [x] Remaining ADR-0006 suspension/closure/retention/export/billing decisions remain separately gated and are not silently promoted by this completion.

Future work must start from the canonical roadmap/ADR decision appropriate to its own scope rather than reopening this completed tracker by implication.

---

## 11. Definition of DONE for this workstream

This tracker is DONE because all of the following are true:

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

**Workstream boundary:** this DONE status is limited to the approved P0.2 identity/onboarding slice. It does not close the still-gated suspension, closure, retention/export, billing/entitlement or other lifecycle-policy decisions in ADR-0006.
