# AI Workflow

## Purpose

This repository (**kyrox-platform**) is the Single Source of Truth for the KYROX ecosystem.

Every AI assistant must analyze the current repository state before making implementation decisions.

Never rely solely on previous conversations.

The repository is always the source of truth.

Application code lives in **kyrox-core** and **fair-crm** — not here.

---

# Roles

| Role | Responsibility |
|------|----------------|
| Product Owner | Business decisions, priorities, acceptance |
| CTO / Software Architect (AI) | Architecture, sprint planning, reviews |
| Cursor | Implementation |

---

# Repositories

## kyrox-platform

Project Management

- Vision
- ADRs
- Roadmap
- Status
- Milestones
- Deferred backlog

No application code.

---

## kyrox-core

Reusable SaaS Platform — **v0.4.0** (commit `c4544b6`).

**Status:** Platform baseline complete. **Frozen** except bug fixes, security fixes, performance fixes, and CRM-driven platform needs.

Contains:

- Authentication
- Authorization
- Organization
- Membership
- Audit Query API
- Settings Platform
- Background Jobs Platform
- Notifications Platform

Never contains product logic.

**Tests:** 307 passed, 1 skipped. **Alembic head:** `20260701_0024`.

---

## fair-crm

Business product — **next active implementation repo**.

Consumes KYROX Core v0.4.0.

Contains CRM logic only.

**Current milestone:** M4 FAIR CRM v1 — FAIR CRM Integration Preparation.

---

# Standard Workflow

Always follow this order.

1. Analyze repository
2. Review documentation
3. Determine milestone
4. Determine sprint
5. Review architecture
6. Prepare implementation
7. Cursor implementation
8. Code review
9. Quality Gate
10. Commit
11. Push
12. Tag (Milestone)

---

# Mandatory Documents

Always review:

- README.md
- ROADMAP.md
- STATUS.md
- KNOWN_DEFERRED.md
- CHANGELOG.md
- decisions/
- milestones/

---

# Architecture Rules

Always:

- Core before Product
- Design before Code
- Review before Commit
- Product never depends backwards
- No duplicated logic
- kyrox-core changes during M4 only for fixes or CRM-driven reusable platform needs

Never:

- Put CRM logic into Core
- Skip review
- Skip quality gate
- Add application code to kyrox-platform

---

# Repository Priority

If there is any conflict:

Repository

↓

Git History

↓

ADR

↓

Roadmap

↓

Previous Conversations

Repository is always correct.
