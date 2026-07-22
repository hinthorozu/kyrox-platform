# AI Workflow

## Purpose

This repository (**kyrox-platform**) is the single source of truth for the KYROX ecosystem.

Every AI assistant must analyze the current repository state before making implementation decisions. Never rely solely on previous conversations.

Application code lives in **kyrox-core** and **fair-crm** - not here.

## Roles

| Role | Responsibility |
|------|----------------|
| Product Owner | Business decisions, priorities, acceptance |
| CTO / Software Architect (AI) | Architecture, sprint planning, reviews |
| Coding agents | Implementation in the correct application repository |

## Repositories

### kyrox-platform

Project management:

- Vision
- ADRs
- Roadmap
- Status
- Milestones
- Deferred backlog

No application code.

### kyrox-core

Reusable SaaS platform - **v0.4.0** (latest known commit `c4544b6`).

**Status:** Platform baseline complete. **Frozen** except bug fixes, security fixes, performance fixes, and CRM-driven reusable platform needs.

Contains:

- Authentication
- Authorization
- Organization
- Membership
- Audit Query API
- Audit Event Write API
- Product Authorization Check API
- Settings Platform
- Background Jobs Platform
- Notifications Platform

Never contains product domain logic.

**Tests:** 307 passed, 1 skipped. **Alembic head:** `20260701_0025`.

### fair-crm

Business product - **active implementation repo**.

Consumes KYROX Core v0.4.0.

Contains CRM logic only.

**Current milestone:** M4 FAIR CRM v1 - active product delivery and data-integration pipeline hardening.

Current delivery snapshot:

- Customer/Fair/Participation foundation modules exist.
- Adapter Management completed.
- Linked Fairs completed.
- Fair -> Adapter relationship completed.
- Adapter CRUD completed.
- Run v2 + JSON Handoff completed.
- Next technical target: Canonical Import Schema.
- Following target: Import Batch / Preview / Duplicate / Merge pipeline.

## Standard Workflow

Always follow this order.

1. Analyze repository
2. Review documentation
3. Determine milestone
4. Determine sprint or current target
5. Review architecture
6. Prepare implementation plan
7. Implement in the correct repository
8. Code review
9. Quality gate
10. Commit only after explicit approval
11. Push only after explicit approval
12. Tag only when milestone rules are satisfied

## Mandatory Documents

Always review:

- `README.md`
- `ROADMAP.md`
- `STATUS.md`
- `KNOWN_DEFERRED.md`
- `CHANGELOG.md`
- `AGENTS.md`
- `decisions/`
- `milestones/`

## Architecture Rules

Always:

- Keep Core before Product for reusable platform capabilities.
- Design before code.
- Review before commit.
- Prevent product-to-Core reverse dependency.
- Avoid duplicated platform logic.
- Change kyrox-core during M4 only for fixes or CRM-driven reusable platform needs.

Never:

- Put CRM logic into Core.
- Skip review.
- Skip quality gates.
- Add application code to kyrox-platform.

## Repository Priority

If there is any conflict:

1. Current repository files
2. Git history
3. ADRs
4. Roadmap
5. Previous conversations

Repository files are the operational source of truth, but stale repository files must be corrected when they conflict with newer canonical status documents.
