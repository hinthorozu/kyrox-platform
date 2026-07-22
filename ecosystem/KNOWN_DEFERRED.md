# Known Deferred Work

Intentionally postponed items. They are not forgotten.

Platform baseline (kyrox-core v0.4.0) is complete. Deferred items remain out of scope until a milestone, ADR, or product need triggers them.

Live status: [STATUS.md](STATUS.md). Product backlog detail: [../projects/fair-crm/PROJECT_STATUS.md](../projects/fair-crm/PROJECT_STATUS.md).

---

## Authentication (Core)

- Email verification
- Password reset
- MFA
- Login rate limiting
- Account lockout
- Refresh token reuse detection
- Device management
- Session management UI

Baseline auth is delivered in kyrox-core v0.2.0–v0.2.1. Strategy still requires email verification and password reset ([ADR-0003](decisions/0003-identity-security-strategy.md)); implementation is deferred.

---

## Platform services (Core)

- Cache
- Event bus
- Metrics / OpenTelemetry / distributed tracing
- File storage

Core platform services (audit, settings, background jobs, notifications) are delivered in v0.4.0.

---

## Developer experience

- Broader Docker Compose surface
- Expanded GitHub Actions
- Coverage reporting automation
- Release automation

---

## FAIR CRM

M4 is **active**. Do **not** treat FAIR CRM architecture, backend, frontend, or import engine as deferred — those exist and are tracked in product status.

Product deferred / planned examples (see product status for the live list):

- CSV Source Adapter (planned sprint 09.3)
- Customer emails
- Backup policy / history / scheduler tracks
- Reporting and later admin platform modules

Do not duplicate the product sprint table here.
