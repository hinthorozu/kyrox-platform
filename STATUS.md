# KYROX PLATFORM STATUS

Single source of truth for ecosystem progress. Application code lives in **kyrox-core** and **fair-crm**; this repository records status only.

---

# KYROX Core

## Capability Matrix

| Area | Status |
|------|--------|
| Foundation | Completed - v0.1.0 |
| Identity | Completed - v0.2.0 |
| Authentication | Completed |
| Authorization | Completed - v0.2.1 Authorization Hardening |
| Organization | Completed - v0.3.0 Organization & Membership Platform |
| Membership | Completed - v0.3.0 Organization & Membership Platform |
| Audit Query API | Completed |
| Audit Event Write API | Completed - product integration API |
| Product Authorization Check API | Completed - product integration API |
| Settings Platform | Completed - v0.4.0 Platform Services |
| Background Jobs Platform | Completed - v0.4.0 Platform Services |
| Notifications Platform | Completed - v0.4.0 Platform Services |
| FAIR CRM permission seeds | Completed - migration `20260701_0025` |
| File Storage | Planned |
| Caching | Planned |
| Observability | Planned |
| DevOps | Planned |

## Core Snapshot

| Field | Value |
|-------|-------|
| Current Version | v0.4.0 |
| Latest Known Commit | c4544b6 |
| Alembic Head | `20260701_0025` |
| Current Test Count | 307 passed, 1 skipped |
| Repository Status | Frozen - bug fixes, security fixes, performance fixes, and CRM-driven reusable platform needs only |
| Platform Baseline | Completed |

---

# FAIR CRM

FAIR CRM is **active in product development**. It is no longer in a "not started" or pure integration-preparation state.

## Product Snapshot

| Area | Status |
|------|--------|
| Architecture | Active and documented in `fair-crm` |
| Backend | Active development |
| Frontend | Active development |
| Customer module | Completed foundation |
| Fair module | Completed foundation |
| Customer/Fair Participation | Completed foundation |
| Adapter Management | Completed |
| Linked Fairs | Completed |
| Fair -> Adapter relationship | Completed |
| Adapter CRUD | Completed |
| Run v2 + JSON Handoff | Completed |
| Current technical target | Canonical Import Schema |
| Next target | Import Batch / Preview / Duplicate / Merge pipeline |

## Current Milestone

M4 - FAIR CRM v1 (active)

## Current Phase

Active FAIR CRM product delivery and data-integration pipeline hardening.

## Primary Product Repo

`fair-crm`

---

# Repository Boundaries

| Repository | Owner Scope |
|------------|-------------|
| `kyrox-platform` | Ecosystem status, roadmap, ADRs, milestones, product planning |
| `kyrox-core` | Reusable SaaS platform capabilities only |
| `fair-crm` | CRM product domain, product UI, product database, data integration workflows |

Core remains reusable and product-agnostic. FAIR CRM-specific domain behavior stays in `fair-crm`.
