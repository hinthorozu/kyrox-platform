# KYROX Ecosystem Status

Single source of truth for **cross-repo** progress. Detailed product and Core status live in project status files linked below. Do not duplicate sprint tables here.

| Field | Value |
|-------|-------|
| Active milestone | **M4 — FAIR CRM v1** |
| Core policy | Frozen (bug/security/performance fixes + reusable platform needs only) |
| Documentation hub | This repository (`kyrox-platform`) |
| Last ecosystem sync | 2026-07-22 |

---

## KYROX Core (summary)

Canonical detail: [projects/kyrox-core/PROJECT_STATUS.md](../projects/kyrox-core/PROJECT_STATUS.md)

| Area | Status |
|------|--------|
| Foundation | Completed — v0.1.0 |
| Identity / Authentication / Authorization | Completed — v0.2.x |
| Organization & Membership | Completed — v0.3.0 |
| Audit write + query APIs | Completed |
| Product authorization check API | Completed |
| Settings / Background Jobs / Notifications | Completed — v0.4.0 |
| FAIR CRM permission seeds | Completed — Alembic `20260701_0025` |
| File Storage / Caching / Observability / DevOps | Planned |

| Field | Value |
|-------|-------|
| Current version | v0.4.0 |
| Alembic head | `20260701_0025` |
| Repository status | Frozen |

---

## FAIR CRM (summary)

Canonical detail: [projects/fair-crm/PROJECT_STATUS.md](../projects/fair-crm/PROJECT_STATUS.md)

FAIR CRM is **active in product development** (M4). It is not in “integration preparation only.”

| Area | Status |
|------|--------|
| Customer / Fair / Participation foundation | Completed |
| Contacts / Activities / Central Activities | Completed |
| Adapter management, linked fairs, Run v2 + JSON handoff | Completed |
| Data Integration / Import Engine / Merge / Preview | Completed (09.0–09.1) |
| Universal Source Adapter Framework + Excel adapter | Completed (09.2) |
| Admin Database Backups (+ format options) | Completed (09.2.2 / 09.2.4) |
| Global responsive UI / UniversalDataTable standard | Completed (ADR-032) |
| Current planned sprint | **09.3 — CSV Source Adapter** |
| Product version (as of last status sync) | v0.9.4 |

---

## Milestone status

| Milestone | Status | Document |
|-----------|--------|----------|
| M1 Foundation | Completed (historical) | [archive/milestones/M1_FOUNDATION.md](../archive/milestones/M1_FOUNDATION.md) |
| M2 Identity | Completed (historical) | [archive/milestones/M2_IDENTITY.md](../archive/milestones/M2_IDENTITY.md) |
| M3 Platform Services | Completed (historical) | [archive/milestones/M3_PLATFORM_SERVICES.md](../archive/milestones/M3_PLATFORM_SERVICES.md) |
| M4 FAIR CRM v1 | **Active** | [projects/fair-crm/MILESTONE_M4.md](../projects/fair-crm/MILESTONE_M4.md) |

---

## Repository boundaries

| Repository | Owner scope |
|------------|-------------|
| `kyrox-platform` | Ecosystem status, roadmap, ADRs, all Markdown documentation |
| `kyrox-core` | Reusable SaaS platform capabilities (code only) |
| `fair-crm` | CRM product domain, UI, product DB, data integration (code only) |

See [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md) and [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md).
