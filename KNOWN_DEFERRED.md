# Known Deferred Work

This document lists work that is **intentionally deferred** — not forgotten, not rejected, and not missing from planning. Items here are postponed until there is a concrete need, dependency, or milestone trigger. When an item is picked up, it should move into a milestone, ADR, or sprint plan and be removed or updated here.

## Authentication

- Email Verification
- Password Reset
- MFA
- Login Rate Limiting
- Account Lockout
- Refresh Token Reuse Detection
- Device Management
- Session Management UI

These extend the baseline defined in [ADR-0003](decisions/0003-identity-security-strategy.md). Core authentication and authorization are in place; the items above are hardening and UX layers deferred until products or security requirements demand them.

## Platform Services

- Cache
- Event Bus
- Metrics
- OpenTelemetry
- Distributed Tracing

Platform services beyond audit (settings, jobs, notifications, file storage) follow the M3 roadmap. Observability and messaging infrastructure are deferred to avoid building unused abstraction before fair-crm and other products define real load and integration patterns.

## Developer Experience

- Docker Compose
- GitHub Actions
- Coverage Reports
- Release Automation

Tooling and CI/CD improvements are deferred until the core platform surface stabilizes enough to justify standardized pipelines across kyrox-core and product repos.

## How to use this list

1. **Do not treat deferred items as bugs or gaps** — they are conscious scope boundaries.
2. **Before starting deferred work** — add or update an ADR or milestone scope in kyrox-platform, then implement in kyrox-core or the relevant product repo.
3. **When an item ships** — update [STATUS.md](STATUS.md), [ROADMAP.md](ROADMAP.md), and [CHANGELOG.md](CHANGELOG.md); remove or annotate the item here.

See [docs/WORKFLOW.md](docs/WORKFLOW.md) for decide → implement → review flow.
