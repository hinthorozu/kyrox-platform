# Changelog

All notable changes to KYROX ecosystem planning and documentation in **kyrox-platform** are recorded here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This changelog tracks **platform decisions and milestones**, not application releases (those belong in kyrox-core and fair-crm).

## [Unreleased]

## [0.4.0] - 2026-07-01

### Completed (kyrox-core / M3)

- **Platform Services** — kyrox-core **v0.4.0** released (commit `c4544b6`, Alembic head `20260701_0024`).
- **Audit Query API** — query surface for audit logs.
- **Settings Platform** — tenant-scoped and system-scoped configuration.
- **Background Jobs Platform** — job registration, scheduling, status.
- **Notifications Platform** — outbound notification dispatch abstraction.
- **Organization & Membership** — delivered in v0.3.0; included in platform baseline.
- **Authorization Hardening** — delivered in v0.2.1.

### Changed

- M3 Platform Services marked **completed**; platform baseline complete.
- kyrox-core **frozen** — changes limited to bug fixes, security fixes, performance fixes, and CRM-driven platform needs.
- Active milestone moved to **M4 FAIR CRM v1**; current phase **FAIR CRM Integration Preparation**.
- STATUS and ROADMAP reflect **307 passed, 1 skipped** tests.

## [0.2.0] - 2026-07-01

### Completed (kyrox-core / M2–M3 partial)

- **Identity** — user and organization model; org-scoped authorization boundary.
- **Authentication** — JWT access tokens, refresh token flow, Core auth APIs.
- **Authorization** — roles and permissions scoped to organization.
- **Audit** — audit service baseline.

### Changed

- M2 Identity Platform marked **completed**; active milestone moved to **M3 Platform Services**.

## [0.1.0] - 2026-07-01

### Added

- kyrox-platform initialized as documentation-only management center for the KYROX ecosystem.
- Initial repository structure: vision, roadmap, workflow, ADRs, product and milestone docs.
- ADR-0001: Three-repository strategy (kyrox-platform, kyrox-core, fair-crm).
- ADR-0002: Core and product separation (Core independent; products depend on Core).
- Milestone definitions M1–M4; M1 Foundation completed.

[Unreleased]: https://github.com/kyrox/kyrox-platform/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/kyrox/kyrox-platform/compare/v0.2.0...v0.4.0
[0.2.0]: https://github.com/kyrox/kyrox-platform/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kyrox/kyrox-platform/releases/tag/v0.1.0
