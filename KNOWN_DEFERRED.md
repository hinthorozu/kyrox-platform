# Known Deferred Work

These items are intentionally postponed.

They are NOT forgotten.

Platform baseline (kyrox-core v0.4.0) is complete. Deferred items below remain out of scope until a milestone, ADR, or product need triggers them.

---

# Authentication

- Email Verification
- Password Reset
- MFA
- Login Rate Limiting
- Account Lockout
- Refresh Token Reuse Detection
- Device Management
- Session Management UI

Baseline auth is delivered in kyrox-core v0.2.0–v0.2.1. Items above are hardening and UX layers deferred until products or security requirements demand them.

---

# Platform Services

- Cache
- Event Bus
- Metrics
- OpenTelemetry
- Distributed Tracing
- File Storage

Core platform services (audit, settings, background jobs, notifications) are delivered in v0.4.0. Observability, caching, messaging, and file storage remain deferred.

---

# Developer Experience

- Docker Compose
- GitHub Actions
- Coverage Reports
- Release Automation

Tooling and CI/CD improvements are deferred until the fair-crm integration surface stabilizes.

---

# FAIR CRM

M4 FAIR CRM v1 is **active**. FAIR CRM Integration Preparation is the current phase.

Product implementation begins in **fair-crm**. Deferred CRM modules (architecture, backend, frontend, import engine, CRM modules) are tracked in [STATUS.md](STATUS.md) and [M4_FAIR_CRM_V1.md](milestones/M4_FAIR_CRM_V1.md).
