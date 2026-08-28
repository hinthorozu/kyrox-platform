# KYROX Core — Project Status

Living status for KYROX Core. Ecosystem summary: [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md). Future work: [ROADMAP.md](ROADMAP.md).

| Field | Value |
|-------|-------|
| Last verified | **2026-08-28** |
| Repository mode | Stable platform baseline; fixes and reusable product-driven changes continue |
| Active ecosystem milestone | M4 — FAIR CRM v1 |
| Migration head in `main` | `20260827_0064_platform_identity_notifications` |
| Main CI | Core CI #71 green on P0.2 CORE-06 final head before merge |

## Current capability state

| Area | Status |
|------|--------|
| Identity and authentication | Implemented baseline plus shared 12–255 character `PasswordPolicy`, one-time identity action tokens, user-wide session/refresh invalidation, server-side access-token session enforcement, controlled public signup/atomic first-user bootstrap and single-use activation/set-password |
| Authorization | Implemented; normal organization permission checks require an `active` organization, so `pending_activation` organizations are non-operational until successful activation |
| Organization and user management | Implemented; normal users use direct single-organization ownership via `identity_users.organization_id`; public signup creates a `pending_activation` organization and inactive first `OrganizationAdmin`, and CORE-06 activates both after a valid one-time token/password-set flow while existing Platform Super Admin organization/user creation remains available |
| Membership / invitation model | Removed by migration `20260817_0057_remove_memberships`; not a current Core capability |
| Roles and permissions | Implemented and evolved through later migrations |
| Audit | Implemented; activation completion records secret-safe `identity.activation.complete` organization audit evidence |
| Settings | Implemented |
| Background jobs | Implemented; internal jobs support platform scope where required by Core identity notifications while existing organization-scoped behavior remains available |
| Notifications | Implemented baseline plus Core-owned production SMTP identity-email capability, platform-scoped recipients/jobs, identity templates, deterministic platform idempotency and redacted delivery logging |
| Product authorization integration | Implemented |
| FAIR CRM permission catalog support | Implemented, including quotation, cost-catalog and mail-send-operation permissions |
| File storage | Planned |
| Caching | Demand-driven candidate |
| Observability | Demand-driven candidate |

## P0.2 identity / SaaS onboarding progress

The approved identity/onboarding implementation workstream is tracked in [P0.2 Identity / SaaS Onboarding Implementation Tracker](../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md).

**CORE-01 — PasswordPolicy is delivered.** Core PR #12 merged to `main` as `323cfa750a0c731bd15de11dfbd19e83858dc1f7` after CI #57 / run `33093204127` succeeded on final head `15db64cba636b340ee0841e25137d2bbea2dbd93`.

CORE-01 delivered one reusable 12–255 character password policy, kept Argon2id focused on hashing/verification, wired existing manual user create/update to the shared policy, returned safe non-secret validation failures, and preserved existing login plus Platform Super Admin manual user creation.

**CORE-02 — One-time identity action tokens is delivered.** Core PR #13 merged to `main` as `f1f88e7f12a7d38d3f917d05840c8562f6f0287a` after CI #60 / run `33097948707` succeeded on final head `fe3408a52667f0d8f3c6bb3de8bdedc3b9745809` with 348 tests passing.

CORE-02 delivered hash-only, expiring, single-use `account_activation` / `password_reset` action tokens, same-user/purpose supersession, atomic conditional consumption and migration `20260827_0063_identity_action_tokens` with direct schema evidence.

**CORE-03 — Session / credential invalidation is delivered.** Core PR #14 merged to `main` as `63889c6c29a73b3224cdda0da21ed2bcc9ac9cb4` after CI #63 / run `33102833407` succeeded on final head `1b2dff1c5613405273ebe673210d522977e8d0c5` with 352 tests passing.

CORE-03 delivered:

- user-scoped active-session and active-refresh-token repository queries,
- reusable `RevokeAllUserSessionsUseCase` with target-user scoping and idempotent behavior,
- `SESSION_REVOKED` refresh-token invalidation and active-session revocation without affecting other users,
- cleanup of inconsistent state where a live refresh token remains attached to an already-revoked session,
- protected access-token fail-closed validation requiring JWT `sid` to resolve to an active server-side session owned by JWT `sub`,
- tests proving revoked/deleted sessions and `sid`/`sub` ownership mismatch return 401.

Password reset and authenticated password change do not exist yet and must invoke the CORE-03 primitive in CORE-07/CORE-08 with endpoint-level stale-credential tests.

**CORE-04 — Core identity notifications / production email is delivered.** Core PR #15 merged to `main` as `09617df8a17aa2ac744b5b1a9692d6418bbf0899` after CI #64 / run `33109701064` succeeded on final head `271124290858e0447af5ac90adc58436ccadf5a4`.

CORE-04 delivered:

- platform-scoped notifications for identity recipients without requiring a fabricated organization,
- corresponding platform-scoped internal dispatch jobs while preserving organization-scoped notification/job behavior,
- separate Core-owned SMTP provider configuration rather than FAIR CRM tenant/product mail credentials,
- stable generic activation, password-reset and password-changed identity templates,
- migration `20260827_0064_platform_identity_notifications`, which makes platform notification/job scope explicit and adds dedicated platform idempotency constraints,
- tests for platform scope, idempotent replay, migration upgrade/downgrade and SMTP delivery/redaction,
- provider-error and logging behavior that does not expose message bodies, action URLs/tokens, SMTP credentials or full recipient addresses.

The workflow's lint step reported success; separate Ruff execution is not claimed because the workflow only runs Ruff when it is installed. Production SMTP delivery requires deployment environment configuration for the Core-owned provider credentials; no FAIR CRM tenant mail account is required.

**CORE-05 — Public signup + atomic bootstrap is delivered.** Core PR #16 merged to `main` as `8e406c9e286f494026edfe460ab7ca4156c2fe4d` after CI #70 / run `33119509255` succeeded on final head `052a2ac16c906bf854ea79917550fae04b44a2d1` with 363 tests passing.

CORE-05 delivered:

- public `POST /api/v1/auth/signup` with normalized organization name/slug handling and safe duplicate email/slug conflicts,
- explicit `pending_activation` organization state, which existing normal authorization does not treat as operational,
- one-request transaction/bootstrap creating a pending organization, inactive first user with `password_hash = NULL`, existing protected `OrganizationAdmin` assignment, activation action token, platform identity notification and dispatch job,
- first-user invariants preserving direct organization ownership and `is_super_admin = false` with no Owner role or restored membership model,
- hash-only activation-token persistence with a safe token UUID reference in notification/job persistence; the raw token/action URL is reconstructed only in memory at delivery time from a dedicated Core secret,
- rollback tests proving a late bootstrap failure leaves no organization, user, role assignment or action token behind,
- API evidence proving raw activation token material is absent from persisted notification/job payloads, response and captured logs,
- compatibility preservation for existing Platform Super Admin organization creation, manual user creation and existing login behavior.

CORE-05 required no schema migration because organization status is string-backed; the migration head therefore remains `20260827_0064_platform_identity_notifications`. The workflow's `Run lint` step reported success but explicitly skipped Ruff because Ruff is not installed, so no separate Ruff lint execution is claimed.

**CORE-06 — Activation is delivered.** Core PR #17 merged to `main` as `66dfdc373724509450e9ee2aed45f876b2935d1a` after CI #71 / run `33198567633` succeeded on final head `f4649d86863eccbfaf531d29353cfa2048041cdc` with 368 tests passing.

CORE-06 delivered:

- public `POST /api/v1/auth/activation/complete` for one-time account activation/set-password,
- shared Core `PasswordPolicy` validation before token consumption so a weak password does not burn a valid activation token,
- atomic `account_activation` token consumption with generic invalid/expired/replayed/wrong-purpose external errors,
- strict target-state validation requiring an inactive, passwordless, non-Super-Admin user directly assigned to a `pending_activation` organization,
- Argon2id password hashing plus user and organization transition to `ACTIVE` in the same request `DbSession`,
- secret-safe `identity.activation.complete` audit evidence containing state transition metadata but no raw token, password, password hash or email,
- rollback evidence proving a later audit failure restores the unconsumed token, inactive/passwordless user and pending organization,
- API evidence proving activation replay fails safely and a successfully activated user can authenticate normally with the newly set password,
- no implicit login/session issuance from the activation endpoint; successful activation returns the user to the normal login flow.

CORE-06 required no schema migration; the migration head remains `20260827_0064_platform_identity_notifications`. CI #71 reported `368 passed, 120 warnings in 18.32s`. The workflow's `Run lint` step reported success but explicitly printed `ruff not installed, skipping`, so separate Ruff lint execution is not claimed.

The next runtime phase is **CORE-07 — Forgot/reset password**. It must add enumeration-resistant recovery, password-reset token delivery/consumption, shared PasswordPolicy enforcement, CORE-03 session/credential invalidation and secret-safe audit evidence. Authenticated change-password remains CORE-08.

## Organization lifecycle baseline

Current Core organization lifecycle behavior relevant to SaaS P0.2:

- existing operator-driven organization creation remains Platform Super Admin only and creates an `ACTIVE` organization,
- public signup creates a separate explicit `PENDING_ACTIVATION` organization and inactive first user; CORE-06 activation moves both to `ACTIVE` only after successful one-time token validation and password set,
- normal users are assigned directly to one organization and receive database-backed roles,
- the first public-signup user receives the existing protected `OrganizationAdmin` role and is not a Super Admin,
- the legacy `Owner` role is removed; `OrganizationAdmin` remains the protected organization administrative role,
- organization suspend/delete are SYSTEM-scope and are not assignable to organization roles,
- normal authorization requires an active organization; `PENDING_ACTIVATION`, `SUSPENDED` and `ARCHIVED` organizations are non-operational for normal permission-protected paths,
- Core organization delete is a soft-delete (`deleted_at`), not cross-product data deletion,
- the domain supports reactivation, but a public organization reactivation endpoint is not currently exposed,
- cross-repository product job/provider/data-retention effects are not implied by Core organization state changes.

The proposed cross-repository lifecycle contract is [ADR-0006](../../ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md). It remains **Proposed overall**; only the explicitly approved onboarding subset is authorized for implementation.

## Migration status

The former documentation baseline at `20260701_0025` is obsolete. The current Core migration tree reaches `20260827_0064_platform_identity_notifications`. Relevant identity evolution includes permission-scope enforcement, removal of the legacy Owner role, protected OrganizationAdmin governance, replacement of memberships with direct user organization ownership, direct user-role validation, later FAIR CRM permission additions, hashed one-time identity action-token persistence and explicit platform scope for Core identity notification/jobs. CORE-03 changed runtime session/credential behavior without schema changes; CORE-04 advanced the migration head from `0063` to `0064`; CORE-05 added string-backed `pending_activation` runtime semantics and public bootstrap without a schema migration; CORE-06 added activation/set-password runtime and audit behavior without a schema migration.

The code repository is the implementation source for complete migration history. This document records the verified current head and capability-level state only.

## Integration contract

Products integrate with Core through public HTTP APIs. Product domain implementation stays in the product repository.

Canonical contract: [integrations/PRODUCT_INTEGRATION_GUIDE.md](integrations/PRODUCT_INTEGRATION_GUIDE.md).

## Update protocol

When Core changes materially:

1. Update this file with current capability truth and migration head when useful.
2. Update [CHANGELOG.md](CHANGELOG.md) for delivered history.
3. Refresh the summary in [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md).
4. Keep exact test counts and commit SHAs out of permanent standards and roadmap documents; implementation evidence may be recorded in project status/tracker history.