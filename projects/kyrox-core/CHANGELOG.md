# Changelog

All notable changes to KYROX Core are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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

- Core identity/security email delivery can now use separate Core SMTP credentials and does not depend on FAIR CRM tenant/product mail-provider configuration; the log adapter remains the development/test default
- Notification and job persistence now support explicit platform scope where required by Core identity delivery while preserving existing organization-scoped behavior
- SMTP dispatch maps provider failures to generic errors and delivery logs omit message bodies/action URLs/tokens, SMTP credentials and full recipient addresses
- Protected access-token validation now requires JWT `sid` to resolve to an active server-side session owned by JWT `sub`; revoked/deleted/mismatched sessions fail closed with 401 instead of leaving stale access tokens valid until natural expiry
- User-wide credential invalidation revokes live refresh tokens with `SESSION_REVOKED` and active sessions while preserving other users; CORE-07/CORE-08 remain responsible for invoking the primitive from reset/change endpoints
- Existing manual organization-user create/update password-setting paths now use the shared Core password policy while preserving Platform Super Admin manual user creation
- Argon2id remains responsible for hashing/verification only; password policy is an application-level Core primitive reusable by later activation/reset/change-password flows
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