# P0.2 Identity / SaaS Onboarding Implementation Tracker

**Status:** ACTIVE — implementation approved for the onboarding/credential workstream  
**Started:** 2026-08-27  
**Current resume point:** `CRM-UI-01 — Public auth routes`  
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

- [x] Public organization signup exists — delivered by Core PR #16; FAIR CRM backend bridge is delivered through PRs #86/#87 and public UI remains later work.
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
- [x] ADR-0006 records OL-01/02/03/04 onboarding sub-decisions as approved for implementation while remaining lifecycle decisions stay open.
- [x] `ecosystem/SAAS_ROADMAP.md` marks this onboarding/credential workstream active and removes stale wording that password reset/email verification are merely deferred candidates.
- [x] `ecosystem/STATUS.md` points to this tracker and records current phase.
- [x] `projects/kyrox-core/ROADMAP.md` promotes the approved generic identity work as active product-driven Core work.
- [x] `projects/fair-crm/ROADMAP.md` promotes the bridge/UI portion as active FAIR CRM work.
- [x] Platform planning/governance PR #12 merged as `c0b9d543437a95343032929364c331a1504fc9b0` after Platform Standards CI #35 / run `33091623466` succeeded on final head `20ac02c263071f06753298c657c165c2bdabb73f`.
- [x] CORE-01 implementation evidence is synchronized into the tracker, Core project status/changelog and ecosystem status after Core PR #12 merge.
- [x] CORE-02 implementation evidence is synchronized into the tracker, Core project status/changelog and ecosystem status after Core PR #13 merge.
- [x] CORE-03 implementation evidence is synchronized into this tracker after Core PR #14 merge; reset/change endpoint integration was later completed by CORE-07/08.
- [x] CORE-04 implementation evidence is synchronized into the tracker, Core project status/changelog/roadmap and ecosystem status after Core PR #15 merge; token-bearing activation/reset integration remained deferred to the owning later phases.
- [x] CORE-05 implementation evidence is synchronized into the tracker, Core project status/changelog/roadmap and ecosystem status after Core PR #16 merge; activation completion remained explicitly owned by CORE-06 until delivery.
- [x] CORE-06 implementation evidence is synchronized into the tracker, Core project status/changelog/roadmap and ecosystem status after Core PR #17 merge; forgot/reset remained explicitly owned by CORE-07 until delivery.
- [x] CORE-07 implementation evidence is synchronized into the tracker, Core project status/changelog/roadmap and ecosystem status after Core PR #18 merge; authenticated password change remained explicitly owned by CORE-08 until delivery.
- [x] CORE-08 implementation evidence is synchronized into the tracker, Core project status/changelog/roadmap and ecosystem status after Core PR #19 merge; CORE-09 remained explicitly owned by the final Core certification phase until delivery.
- [x] CORE-09 final Core security/adversarial certification evidence is synchronized into the tracker, Core project status/changelog/roadmap and ecosystem status after Core PR #20 merge; the canonical resume point moved to FAIR CRM backend integration.
- [x] CRM-BE-01 and CRM-BE-02 FAIR CRM backend bridge evidence is synchronized after PRs #86 and #87; the canonical resume point moves to CRM-UI-01.
- [ ] Project status/changelog documents continue to be updated as each later implementation PR actually merges; planning checkboxes must not claim runtime delivery before code exists.
- [ ] Final completion synchronizes Core/FAIR CRM/Platform status, roadmaps and changelogs.

---

## 10. Execution order / current position

The implementation order is intentionally dependency-first:

1. **Platform planning/governance record** — this tracker + ADR/roadmap/status synchronization.
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
13. **CRM-UI-01** public auth routes. ← NEXT
14. **CRM-UI-02/03/04** login integration, security settings and Super Admin compatibility UI.
15. **Cross-repository E2E / tenant-isolation / production-shaped gates.**
16. **Platform final documentation closure.**

### Current position

- [x] Architecture/runtime audit completed.
- [x] User approved the identity/onboarding implementation direction.
- [x] Implementation tracker and synchronized roadmap/ADR/status documentation merged through Platform PR #12.
- [x] Platform Standards CI #35 / run `33091623466` succeeded on PR #12 final head.
- [x] CORE-01 PasswordPolicy delivered through Core PR #12; CI #57 / run `33093204127` SUCCESS; merge `323cfa750a0c731bd15de11dfbd19e83858dc1f7`.
- [x] CORE-02 one-time identity action tokens delivered through Core PR #13; final head `fe3408a52667f0d8f3c6bb3de8bdedc3b9745809`; CI #60 / run `33097948707` SUCCESS with 348 tests passed; merge `f1f88e7f12a7d38d3f917d05840c8562f6f0287a`.
- [x] CORE-03 user-wide session/credential invalidation delivered through Core PR #14; final head `1b2dff1c5613405273ebe673210d522977e8d0c5`; CI #63 / run `33102833407` SUCCESS with 352 tests passed; merge `63889c6c29a73b3224cdda0da21ed2bcc9ac9cb4`.
- [x] CORE-04 Core identity notifications / production email delivered through Core PR #15; final head `271124290858e0447af5ac90adc58436ccadf5a4`; CI #64 / run `33109701064` SUCCESS; merge `09617df8a17aa2ac744b5b1a9692d6418bbf0899`; migration head `20260827_0064_platform_identity_notifications`.
- [x] CORE-05 public signup + atomic bootstrap delivered through Core PR #16; final head `052a2ac16c906bf854ea79917550fae04b44a2d1`; CI #70 / run `33119509255` SUCCESS with 363 tests passed; merge `8e406c9e286f494026edfe460ab7ca4156c2fe4d`; migration head remains `20260827_0064_platform_identity_notifications`.
- [x] CORE-06 activation delivered through Core PR #17; final head `f4649d86863eccbfaf531d29353cfa2048041cdc`; CI #71 / run `33198567633` SUCCESS with 368 tests passed; merge `66dfdc373724509450e9ee2aed45f876b2935d1a`; migration head remains `20260827_0064_platform_identity_notifications`.
- [x] CORE-07 forgot/reset password delivered through Core PR #18; final head `7529f82689b970991314e9621feaa0341fe3f0a2`; CI #78 / run `33227509093` SUCCESS with 375 tests passed; merge `db5695d2c77a8e2dbe29dd19f4a3cb22d770e7d8`; migration head remains `20260827_0064_platform_identity_notifications`.
- [x] CORE-08 authenticated password change delivered through Core PR #19; final head `ecb77f8918e9a156b686eb902c50692e92de3339`; CI #82 / run `33228044257` SUCCESS with 379 tests passed; merge `75905f02bdf621419f9b6560fff5809e56150ad5`; migration head remains `20260827_0064_platform_identity_notifications`.
- [x] CORE-09 Core security/adversarial certification delivered through Core PR #20; final head `5c5113320ea910e80555e6cc526ed0c708580cd4`; CI #84 / run `33228476878` SUCCESS with 381 tests passed; merge `f6cbf417410d9148c225242790103d8cc9541f21`; no runtime/schema change and migration head remains `20260827_0064_platform_identity_notifications`.
- [x] CRM-BE-01 Core client extensions delivered through FAIR CRM PR #86; final head `934a7d1843bf5f036f06225393af2af4aa3810ce`; Development Standard Gate #278 SUCCESS with 1767 tests passed; Prod-Path E2E #148 SUCCESS; merge `a83fa9a11dd603962cbb29510a0b11748f886d9f`.
- [x] CRM-BE-02 auth bridge routes delivered through FAIR CRM PR #87; final head `1068a5a94d26799e6b63565e18cf6a61e5699a72`; Development Standard Gate #280 / run `33230174837` SUCCESS with 1781 tests passed; Prod-Path E2E #149 / run `33230174828` SUCCESS; merge `0c8a0004f5067dbd8041898a1fe590026c22d736`.
- [ ] **NEXT RUNTIME PHASE: CRM-UI-01 — FAIR CRM public auth routes.**

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