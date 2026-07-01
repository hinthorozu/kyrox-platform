# AI Workflow

## Purpose

This repository (**kyrox-platform**) is the Single Source of Truth for the KYROX ecosystem.

Every AI assistant must analyze the current repository state before making implementation decisions.

Never rely solely on previous conversations.

The repository is always the source of truth.

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

Reusable SaaS Platform.

Contains:

- Identity
- Authentication
- Authorization
- Audit
- Platform Services

Never contains product logic.

---

## fair-crm

Business product.

Consumes KYROX Core.

Contains CRM logic only.

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

Never:

- Put CRM logic into Core
- Skip review
- Skip quality gate

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