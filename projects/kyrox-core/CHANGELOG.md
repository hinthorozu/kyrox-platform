# Changelog

All notable changes to KYROX Core are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- P0.2 CORE-08 authenticated self-service password change; delivered through Core PR #19
- Authenticated `POST /api/v1/auth/password/change` requiring a valid access token backed by an active server-side session, current-password verification, shared Core `PasswordPolicy`, same-password/no-op rejection and Argon2id credential replacement
- Secret-safe `identity.password.change` audit evidence plus CORE-03 user-wide session/refresh invalidation, including the session used to perform the change; no replacement session is issued implicitly
- CORE-08 tests covering missing authentication, wrong-current/weak/same-password denial, non-revocation on failed changes, stale access/refresh invalidation after success, old-password rejection, new-password login, audit redaction and audit-failure rollback
- P0.2 CORE-07 Core-owned forgot/reset password flow; delivered through Core PR #18
- Public `POST /api/v1/auth/password/forgot` with enumeration-safe responses, active-account eligibility, 60-second database-backed resend cooldown, reset-token supersession and configurable reset-token TTL
- Public `POST /api/v1/auth/password/reset` using the shared Core `PasswordPolicy`, atomic single-use reset-token consumption, Argon2id credential replacement, CORE-03 user-wide session/refresh invalidation and secret-safe `identity.password.reset` audit evidence
- CORE-07 tests covering enumeration resistance, cooldown/supersession, raw-token non-persistence/log redaction, weak-password non-consumption, expiry/replay/invalid-token handling, inactive/deleted-account policy, prior credential invalidation, old-password rejection and successful login with the new password only
- P0.2 CORE-06 single-use account activation/set-password flow; delivered through Core PR #17
- Public `POST /api/v1/auth/activation/complete` contract using the existing account-activation token primitive, shared Core `PasswordPolicy` and Argon2id hashing
- Secret-safe `identity.activation.complete` organization audit evidence and activation tests covering replay, expiry, wrong-purpose tokens, rollback, non-consumption on weak password and post-activation login
- P0.2 CORE-05 public commercial signup and atomic first-account bootstrap; delivered through Core PR #16
- Public `POST /api/v1/auth/signup` contract creating a `PENDING_ACTIVATION` organization and inactive first user with no password hash
- Atomic first-user `OrganizationAdmin` assignment, activation-token issuance and activation-notification enqueue on one request database transaction
- Reconstructable hash-only activation-token delivery mode that persists only token hashes/token UUID references while materializing raw token/action URL only in memory during dispatch
- CORE-05 tests covering pending bootstrap invariants, protected OrganizationAdmin assignment, duplicate conflicts, SQLAlchemy rollback, hash-only token materialization, raw-token non-persistence/log redaction and pre-activation login rejection
- P0.2 CORE-04 Core-owned production identity-email capability; delivered through Core PR #15
- Platform-scoped identity notifications and corresponding internal dispatch jobs without requiring a fabricated organization
- Core-owned configurable SMTP adapter plus stable activation, password-reset and password-changed identity templates
- Alembic `20260827_0064` for explicit platform notification/job scope and dedicated platform idempotency constraints
- CORE-04 tests covering platform scope, idempotent replay, migration upgrade/downgrade, SMTP dispatch and secret/recipient/log redaction
- P0.2 CORE-03 reusable user-wide session/refresh credential invalidation primitive; delivered through Core PR #14
- User-scoped active-session and active-refresh-token repository queries plus idempotent `RevokeAllUserSessionsUseCase`
- Access-token session enforcement tests covering revoked/deleted sessions and JWT `sid`/`sub` ownership mismatch
- P0.2 CORE-02 generic one-time identity action-token primitive for `account_activation` and `password_reset`; delivered through Core PR #13
- Hash-only `identity_action_tokens` persistence with expiry, consumed/invalidation timestamps, same-user/purpose supersession and migration `20260827_0063`
- Atomic conditional token consumption plus deterministic expiry, replay, wrong-purpose, unknown-token, redaction, persistence and migration tests
- P0.2 CORE-01 shared Core `PasswordPolicy` with 12–255 character bounds and no forced composition requirement; delivered through Core PR #12
- Password-policy and manual user-management regression tests covering boundary, Unicode and safe non-echoed error behavior
- Alembic `20260701_0025` — seed FAIR CRM customer permissions (`fair_crm.customers.create`, `.read`, `.update`, `.archive`) in Core RBAC tables
- Migration tests for FAIR CRM permission seed

### Changed

- Successful authenticated password change now verifies the current credential, requires a distinct policy-compliant new password, replaces the Core-owned Argon2id credential atomically and invokes CORE-03 so the current and all other prior sessions/refresh credentials fail immediately; the endpoint requires login again rather than issuing a new session
- Successful password reset now replaces the Core-owned Argon2id credential, consumes the one-time reset token and invokes CORE-03 user-wide session/refresh invalidation so previously issued credentials fail immediately; reset does not issue an implicit session
- Forgot-password behavior now suppresses account existence/eligibility differences behind one public response and applies deterministic resend cooldown/token supersession without persisting raw reset tokens or token-bearing URLs
- Successful account activation now consumes the one-time token and transitions the inactive/passwordless first user plus its `PENDING_ACTIVATION` organization to `ACTIVE` in the same request transaction; activation does not issue an implicit session
- Activation password-policy validation occurs before token consumption, and invalid/expired/replayed/wrong-purpose token conditions use one generic public error contract without exposing token details
- Identity action-token consumption fallback normalizes persisted SQLite naive UTC expiry values before diagnostic expiry/replay checks
- Normal public account provisioning now starts organizations in explicit non-operational `PENDING_ACTIVATION` state; existing normal authorization continues to require `ACTIVE`
- Existing Platform Super Admin organization creation and manual user/password provisioning remain available and are not repurposed by public signup
- The protected historical `organization_admin` role slug is accepted by the RoleSlug compatibility boundary while other invalid underscore slugs remain rejected
- Identity action-token materialization normalizes persisted SQLite naive UTC datetimes before expiry comparison, preserving deterministic behavior across SQLite tests and timezone-aware runtime clocks
- Core identity/security email delivery can now use separate Core SMTP credentials and does not depend on FAIR CRM tenant/product mail-provider configuration; the log adapter remains the development/test default
- Notification and job persistence now support explicit platform scope where required by Core identity delivery while preserving existing organization-scoped behavior
- SMTP dispatch maps provider failures to generic errors and delivery logs omit message bodies/action URLs/tokens, SMTP credentials and full recipient addresses
- Protected access-token validation now requires JWT `sid` to resolve to an active server-side session owned by JWT `sub`; revoked/deleted/mismatched sessions fail closed with 401 instead of leaving stale access tokens valid until natural expiry
- User-wide credential invalidation revokes live refresh tokens with `SESSION_REVOKED` and active sessions while preserving other users; both CORE-07 password reset and CORE-08 authenticated password change now invoke this primitive
- Existing manual organization-user create/update password-setting paths now use the shared Core password policy while preserving Platform Super Admin manual user creation
- Argon2id remains responsible for hashing/verification only; password policy is an application-level Core primitive reusable by activation/reset/change-password flows
- Identity action-token issuance returns raw opaque token material only to the immediate caller while Core persistence stores only SHA-256 hashes; reissue supersedes older live same-purpose tokens

## [0.4.0] — 2026-07-01

Sprint **0.4.0** — Platform Services (Audit Query, Settings, Background Jobs, Notifications).

### Added

**Audit Query API (Sprint 0.4.1)**

- `ListOrganizationAuditLogsUseCase` with cursor pagination and filter policy
- Query repository port and SQLAlchemy implementation
- `GET /api/v1/organizations/{id}/audit-logs` — permission `audit.logs.read`
- Alembic `20260701_0017` (query indexes), `20260701_0018` (permission seed)

**Settings Platform (Sprint 0.4.2)**

- Domain: `Setting`, scope enum (system / organization), key/value validation policy
- Application: get, list, upsert, delete use cases
- Infrastructure: `platform_settings` table, repository, mapper
- Org-scoped API: `/organizations/{id}/settings` — permissions `settings.platform.read`, `settings.platform.update`
- System-scoped API: `/system/settings` — super-admin guard
- Alembic `20260701_0019`, `20260701_0020`

**Background Jobs Platform (Sprint 0.4.3)**

- Domain: `Job`, status lifecycle, `JobHandler` / `JobHandlerRegistry` ports
- Application: enqueue, get status, process pending jobs; in-process worker
- Infrastructure: `platform_jobs` table; PostgreSQL `FOR UPDATE SKIP LOCKED` claim path
- API: `POST /organizations/{id}/jobs`, `GET /jobs/{id}` — permissions `jobs.platform.enqueue`, `jobs.platform.read`
- Stub handler: `core.platform.echo`
- Alembic `20260701_0021`, `20260701_0022`

**Notifications Platform (Sprint 0.4.4)**

- Domain: `Notification`, channel/status lifecycle, channel and settings reader ports
- Application: send, get status, dispatch (job handler use case); settings-aware suppression
- Infrastructure: `platform_notifications` table; `EmailLogStubAdapter` (PII-safe logs)
- Jobs integration: `core.platform.notification.dispatch` via `JobEnqueuePort`
- Settings integration: org keys `kyrox.notifications.email_enabled`, `kyrox.notifications.email_from` via reader port
- API: `POST /organizations/{id}/notifications/send`, `GET /notifications/{id}` — permissions `notifications.platform.send`, `notifications.platform.read`
- Alembic `20260701_0023`, `20260701_0024`

**Tests**

- Architecture, import-boundary, integration, and API route tests for all platform modules
- **307 tests passing**, 1 skipped (`python scripts/quality_check.py`)

### Changed

- `app/api/v1/router.py` includes audit, settings, jobs, and notifications routers
- `app/main.py` registers job handler registry and notification platform bootstrap
- Identity `PermissionModule` enum extended: `jobs`, `notifications`

### Notes

- Notifications dispatch is idempotent for terminal states (`sent`, `failed`, `suppressed`)
- Email stub adapter logs redacted recipient only — no full body/subject at INFO level
- Accept-invite API integration test still skipped on SQLite (naive datetime roundtrip)

---

## [0.3.0] — 2026-07-01

Sprint **0.3.5** — Organization & Membership Platform (full vertical slice).

### Added

**Domain (`domain/organization/`, `domain/membership/`)**

- Canonical `Organization` aggregate with lifecycle (active, suspended, archived)
- Canonical `Membership` and `MembershipInvite` aggregates with invite/accept/suspend/remove transitions
- Value objects, enums, exceptions, and repository ports for organization and membership bounded contexts

**Application (`application/organization/`, `application/membership/`)**

- Organization use cases: create, get, update, suspend
- Membership use cases: list, invite, accept invite, suspend, remove
- `MembershipRoleAssigner` for owner/member role assignment on org create and invite accept
- `InviteTokenIssuer` for secure invite token generation

**Infrastructure (`infrastructure/organization/`, `infrastructure/membership/`)**

- SQLAlchemy ORM models, mappers, and repositories for organizations, memberships, and membership invites
- `SecureInviteTokenService` for invite token hashing
- Legacy `persistence/models.py` re-exports canonical models

**Migrations (Alembic `20260701_0014`–`20260701_0016`)**

- `identity_memberships`: `invited_at`, `joined_at` lifecycle columns with backfill
- `identity_membership_invites` table for pending invite persistence
- Schema cleanup: fail-fast guard for orphaned `role_id`, drop legacy `role_id` column, indexes

**API & DI (`api/organization/`, `api/membership/`)**

- `POST /api/v1/organizations` — create organization (JWT; owner from token `sub`)
- `GET|PATCH /api/v1/organizations/{id}` — read/update (Bearer + `X-Organization-Id` + permission)
- `POST /api/v1/organizations/{id}/suspend` — suspend organization
- `GET /api/v1/organizations/{id}/memberships` — list memberships
- `POST /api/v1/organizations/{id}/memberships/invite` — invite member
- `POST /api/v1/memberships/invites/accept` — accept invite (JWT only)
- `POST /api/v1/memberships/{id}/suspend` — suspend membership
- `DELETE /api/v1/memberships/{id}` — remove membership
- Composition root: canonical repositories wired in `membership/dependencies.py`; `get_membership_role_assigner` defined in a single location

**Tests**

- Domain, application, infrastructure, migration, and API architecture/import-boundary/route tests
- **228 tests passing**, 1 skipped (`python scripts/quality_check.py`)

### Changed

- `app/api/v1/router.py` includes organization and membership routers
- Identity permission codes expected for org-scoped routes: `identity.organizations.*`, `identity.memberships.*`

### Notes

- Permission seed migration for `identity.organizations.*` / `identity.memberships.*` is tracked for Sprint 0.4.0
- Accept-invite API integration test skipped on SQLite due to naive datetime roundtrip (PostgreSQL production path unaffected)

---

## [0.2.0] — 2026-07-01

Sprint **0.3.2–0.3.4** (+ identity hardening) — Authentication, Authorization, and legacy identity persistence.

### Added

- Identity persistence: users, organizations, memberships (legacy monolithic layer)
- Authentication: Argon2id, JWT access tokens, refresh rotation, sessions
- Authorization: RBAC with `AuthorizationService`, `require_permission` guard, `X-Organization-Id` header
- API: `POST /api/v1/auth/login`, `/refresh`, `/logout`
- Alembic migrations through authorization schema hardening
- Audit module foundation (domain, application service, repository — no public API yet)

### Tests

- 62+ tests at hardening milestone; expanded through subsequent sprints

---

## [0.1.0] — 2026-07-01

Sprint **0.1–0.2.5** — Architecture, backend foundation, and layered architecture standards.

### Added

- Project documentation, ADRs, backend scaffold
- FastAPI app, health endpoint, SQLAlchemy + Alembic tooling
- [Backend Architecture Standards](../../standards/backend/../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md)

[0.4.0]: https://github.com/kyrox/kyrox-core/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/kyrox/kyrox-core/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/kyrox/kyrox-core/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kyrox/kyrox-core/releases/tag/v0.1.0