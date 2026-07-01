# Changelog

All notable changes to KYROX ecosystem planning and documentation in **kyrox-platform** are recorded here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This changelog tracks **platform decisions and milestones**, not application releases (those belong in kyrox-core and fair-crm).

## [Unreleased]

### Added

- [STATUS.md](STATUS.md) — live ecosystem capability and sprint snapshot.
- [KNOWN_DEFERRED.md](KNOWN_DEFERRED.md) — intentionally deferred work backlog.
- README updated: kyrox-platform as management repository and single source of truth.

## [0.2.0] - 2026-07-01

### Completed (kyrox-core / M2–M3)

- **Identity** — user and organization model; org-scoped authorization boundary.
- **Authentication** — JWT access tokens, refresh token flow, Core auth APIs.
- **Authorization** — roles and permissions scoped to organization.
- **Audit** — audit service baseline (M3; Sprint 0.4.2).

### Changed

- M2 Identity Platform marked **completed**; active milestone moved to **M3 Platform Services**.
- ROADMAP and STATUS reflect kyrox-core **v0.2.0** with **74 passing tests**.

## [0.1.0] - 2026-07-01

### Added

- kyrox-platform initialized as documentation-only management center for the KYROX ecosystem.
- Initial repository structure: vision, roadmap, workflow, ADRs, product and milestone docs.
- ADR-0001: Three-repository strategy (kyrox-platform, kyrox-core, fair-crm).
- ADR-0002: Core and product separation (Core independent; products depend on Core).
- Milestone definitions M1–M4; M1 Foundation completed.

[Unreleased]: https://github.com/kyrox/kyrox-platform/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/kyrox/kyrox-platform/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kyrox/kyrox-platform/releases/tag/v0.1.0
