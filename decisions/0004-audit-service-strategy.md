# ADR-0004: Audit service strategy

- **Status:** Accepted
- **Date:** 2026-07-01
- **Deciders:** KYROX ecosystem maintainers

## Context

M3 Platform Services extends **kyrox-core** with shared capabilities that multiple products consume. **Audit logging** is the first platform service because security, compliance, and operational visibility depend on a consistent, trustworthy activity trail across products.

Today, kyrox-core delivers identity foundations (users, organizations, memberships, authentication, authorization) without a centralized audit store. Products such as fair-crm will need to record who did what, when, and in which organization context—without each product inventing its own audit schema or coupling Core to product domains.

Requirements for the Audit Service:

- **Product-independent** — Core owns the audit module; no FAIR CRM imports or domain types in Core audit code.
- **Organization-aware** — Events may be scoped to an organization when applicable; system-level events may omit organization context.
- **User-aware** — Events may reference the acting user and session when known.
- **Identity integration** — Correlates with kyrox-core identity (`user_id`, `organization_id`, session id from JWT `sid` where available).
- **Reusable** — fair-crm and future products emit audit events through Core contracts; audit does not depend on product modules.

This ADR defines the strategy and data model **before** Sprint 0.4.2+ implementation in kyrox-core.

## Decision

Adopt a **central Audit Service** in kyrox-core with the following strategy:

| # | Area | Decision |
|---|------|----------|
| 1 | Storage | Single **`audit_logs`** table in kyrox-core (PostgreSQL), append-only |
| 2 | Structured payloads | **`JSONB`** columns for `old_values`, `new_values`, and `metadata` |
| 3 | Write semantics | **Best-effort** for general events; **must not silently swallow failures** for classified security-critical events (see below) |
| 4 | Application API | **`AuditService`** (application layer) backed by an **`AuditLogRepository`** port (domain) |
| 5 | Dependency direction | Products and Core modules **call** audit; audit **never imports** product modules |
| 6 | Event categories | Supports **user-initiated** and **system** events (nullable actor fields where N/A) |
| 7 | Domain purity | Domain layer has **no hard dependency** on HTTP request context; callers pass explicit fields |
| 8 | Capture mechanism | **Explicit audit calls** from use cases/services first; **HTTP middleware** auto-audit deferred |

### AuditLog data model (draft)

Table: **`audit_logs`**

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `organization_id` | UUID | Yes | Organization context when applicable; null for platform/system events |
| `user_id` | UUID | Yes | Acting user; null for system/automated events |
| `session_id` | UUID | Yes | Identity session reference (JWT `sid` when available) |
| `action` | VARCHAR | No | Namespaced action code (see Event naming) |
| `resource_type` | VARCHAR | No | Logical resource type (e.g. `user`, `role`, `setting`) |
| `resource_id` | VARCHAR | Yes | Resource identifier (UUID or opaque string) |
| `old_values` | JSONB | Yes | Prior state snapshot or diff input |
| `new_values` | JSONB | Yes | New state snapshot or diff input |
| `metadata` | JSONB | Yes | Extra context (request id, source module, correlation ids) |
| `ip_address` | VARCHAR(45) | Yes | Client IP when known |
| `user_agent` | VARCHAR(512) | Yes | Client user agent when known |
| `created_at` | TIMESTAMPTZ | No | Event timestamp (server default `now()`) |

**Indexes (implementation draft):**

- `(organization_id, created_at DESC)` — org activity timelines
- `(user_id, created_at DESC)` — user activity
- `(action, created_at DESC)` — security and ops filtering
- `(resource_type, resource_id)` — resource history lookup

**Constraints:**

- No updates or deletes in normal operation (append-only; retention/archival is a future ops concern).
- Foreign keys to `identity_users`, `identity_organizations`, and `identity_sessions` are **optional** (nullable FKs or logical references only) to avoid blocking audit writes when referenced rows are soft-deleted or when system events have no actor.

### Event naming convention

Actions use dot-separated namespaces:

```text
<module>.<resource>.<verb>
```

| Segment | Meaning | Examples |
|---------|---------|----------|
| `module` | Core platform area or product prefix | `identity`, `core`, `fair_crm` |
| `resource` | Entity or concern | `user`, `permission`, `settings`, `company` |
| `verb` | Past-tense or canonical verb | `login`, `logout`, `granted`, `updated`, `created` |

**Core examples (in scope for kyrox-core):**

- `identity.user.login`
- `identity.user.logout`
- `identity.user.created`
- `identity.permission.granted`
- `identity.permission.revoked`
- `identity.role.assigned`
- `core.settings.updated`

**Product example (documentation only — not implemented in Core):**

- `fair_crm.company.created` — emitted by fair-crm via Core audit API; illustrates that product modules use their own `module` prefix without Core knowing CRM domain logic.

Rules:

- Use lowercase segments; separate with `.` (no spaces).
- Prefer stable verbs; avoid UI-specific labels in action names.
- `resource_type` aligns with the middle segment where practical (e.g. action `identity.user.login` → `resource_type`: `user`).
- Product-prefixed actions are allowed in the **same table**; Core stores them opaquely without validating product semantics.

### Write semantics and error handling

**General events (best-effort):**

- Audit write failures are logged at error level; the primary business operation may still succeed if audit is non-blocking by design.
- Callers use `AuditService.record(...)` (or equivalent) after the main transaction commits where possible to avoid orphan audit rows.

**Security-critical events (must not fail silently):**

Classify at minimum:

- `identity.user.login` (success and failure variants via metadata)
- `identity.user.logout`
- `identity.permission.granted` / `identity.permission.revoked`
- `identity.role.assigned` / `identity.role.unassigned`
- Super-admin or privilege-elevation actions

For these, if persistence fails after the business operation succeeded, the service **must** propagate an error or escalate (log + metric + optional re-raise policy defined in application layer). Implementation must not use bare `except: pass` for security event writes.

### Application-level port and service

**Domain:**

- Entity: `AuditLog`
- Port: `AuditLogRepository` with `append(audit_log: AuditLog) -> AuditLog`
- No FastAPI, SQLAlchemy, or request objects in domain

**Application:**

- `AuditService.record(...)` — accepts explicit fields (organization_id, user_id, session_id, action, resource_type, resource_id, old/new/metadata, ip, user_agent)
- Optional helpers: `record_user_event(...)`, `record_system_event(...)` for clarity
- Security-critical flag or internal routing for stricter error policy

**Infrastructure:**

- SQLAlchemy model `AuditLogModel` → table `audit_logs`
- `SqlAlchemyAuditLogRepository` implements port
- JSONB mapping for PostgreSQL; JSON/text fallback acceptable in SQLite tests only

**API (deferred in first implementation sprint):**

- Read/query APIs and admin UI are out of scope for Sprint 0.4.1
- HTTP middleware that auto-audits all routes is **deferred**; identity use cases call audit explicitly first (login, logout, permission changes)

### Integration with kyrox-core identity

| Identity concept | Audit field | Notes |
|------------------|-------------|-------|
| User | `user_id` | From authenticated user or explicit system null |
| Organization | `organization_id` | From `X-Organization-Id` or use-case context; not from JWT (Core does not put `org_id` in access tokens) |
| Session | `session_id` | JWT claim `sid` when available |
| Client | `ip_address`, `user_agent` | Passed by API/application from request; not read inside domain |

Products depend on Core identity for authentication; they pass the same explicit context into audit calls when recording product events.

## Consequences

### Positive

- One audit schema and query model for all KYROX products
- Clear separation: products emit events; Core persists them
- JSONB allows evolving payloads without schema churn for every new field
- Explicit calls keep domain testable and avoid magic middleware in early sprints
- Aligns with layered architecture in kyrox-core ([ADR-0002](0002-core-product-separation.md))

### Negative

- Explicit calls require discipline; missed call sites mean gaps until middleware or conventions are added
- JSONB payloads need size limits and redaction policies to avoid storing secrets or PII unnecessarily
- Best-effort vs security-critical dual policy adds application complexity
- Append-only table grows unbounded; retention/archival ADR needed later

### Neutral

- Product-prefixed actions (`fair_crm.*`) live in the same table; reporting may filter by action prefix
- Read APIs and export for compliance are follow-on sprints

## Security and privacy considerations

1. **Sensitive data** — Do not store passwords, tokens, refresh tokens, or full secrets in `old_values` / `new_values` / `metadata`. Redact or omit at the caller; AuditService may document forbidden keys.
2. **PII minimization** — Store user id references, not duplicate email/name, unless required for immutable forensic snapshots (prefer ids + lookup).
3. **Tamper resistance** — Append-only application policy; no update/delete endpoints in v1. Database-level immutability optional later.
4. **Tenant isolation** — Queries by organization must enforce organization scope at the application/API layer when read paths are added.
5. **Failed login** — Record with null or system user and metadata `{ "outcome": "failure", "reason": "invalid_credentials" }` without user enumeration leakage in external APIs (audit row is internal).
6. **Access control** — Reading audit logs requires dedicated permissions (e.g. `core.audit.read`); design only in this ADR; implementation with authorization core in a later sprint.
7. **Correlation** — Encourage `metadata.request_id` / `metadata.trace_id` for cross-service tracing without coupling audit domain to HTTP.

## Implementation impact for kyrox-core

Sprint sequence (indicative):

| Sprint | Focus |
|--------|--------|
| **0.4.1** | This ADR + design (kyrox-platform) — **no code** |
| **0.4.2** | Domain entity, port, `AuditService`, repository, migration, unit tests |
| **0.4.3** | Wire explicit audit calls in identity (login, logout, permission grant/revoke) |
| **0.4.4+** | Query API, retention, middleware evaluation (optional) |

kyrox-core must:

1. Add `modules/audit/` (or `modules/platform/audit/`) following domain → application → infrastructure → api layout.
2. Create Alembic migration for `audit_logs` with JSONB columns on PostgreSQL.
3. Implement `AuditService` injectable via FastAPI dependencies where API layer records events.
4. Keep audit module free of fair-crm imports.
5. Extend quality gate tests; no PostgreSQL required for unit tests (SQLite JSON columns acceptable for mapper/repo tests).

Products (fair-crm):

- Call Core `AuditService` through documented contract (HTTP internal API or shared package TBD in implementation sprint).
- Use `fair_crm.*` action prefix for product domain events.

## Out of scope

- **FAIR CRM domain logic** in Core audit module
- **Automatic HTTP middleware** audit for all routes (deferred)
- **Audit read/admin UI** and export (later sprint)
- **Log shipping / SIEM integration** (ops follow-up)
- **Retention, archival, and legal hold** policies (future ADR)
- **Settings, Notifications, Background Jobs** (separate M3 sprints)
- **Replacing application logging** — audit complements structured logs; does not replace them
- **Blockchain or WORM storage** — not required for v1

## Related

- [ADR-0002: Core and product separation](0002-core-product-separation.md)
- [ADR-0003: Identity security strategy](0003-identity-security-strategy.md)
- [M3 Platform Services](../milestones/M3_PLATFORM_SERVICES.md)
- [ROADMAP.md](../ROADMAP.md)
