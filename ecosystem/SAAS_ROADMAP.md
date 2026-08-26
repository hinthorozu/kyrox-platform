# KYROX SaaS Readiness Roadmap

**Status:** Canonical cross-repository SaaS readiness strategy and sequencing  
**Scope:** KYROX Platform, KYROX Core, FAIR CRM, and future KYROX products  
**Execution rule:** Binding delivery/quality semantics remain in the shared standards; this roadmap defines SaaS priorities, ownership boundaries, decision gates and launch sequencing.

This document exists to make one rule explicit:

> **Every material change must preserve or improve KYROX SaaS safety. A green build or test suite is necessary, but it is not sufficient when tenant isolation, authorization scope, platform ownership, security, lifecycle, usage or production runtime behavior is affected.**

This file is not a competing product backlog. When an item becomes active implementation work, promote the concrete task into the owning project roadmap and implement it in the owning code repository. Cross-repository architecture or ownership changes require the applicable ecosystem decision/ADR first.

Canonical delivery gate: [../standards/development/FEATURE_DELIVERY_STANDARD.md](../standards/development/FEATURE_DELIVERY_STANDARD.md).  
Canonical applicability rule: [../standards/development/FEATURE_APPLICABILITY_STANDARD.md](../standards/development/FEATURE_APPLICABILITY_STANDARD.md).  
Canonical quality rule: [../standards/quality/QUALITY_GATE_STANDARD.md](../standards/quality/QUALITY_GATE_STANDARD.md).

---

## 1. Non-negotiable SaaS invariants

These invariants apply to all future product/platform work unless an explicit accepted ADR changes the architecture.

### 1.1 Organization is the account boundary

KYROX domain language uses **organization** as the account/data boundary. `tenant isolation` remains the technical security term, but no parallel `Tenant` entity/model is introduced merely to make the system “more SaaS”.

Organization-scoped behavior follows:

```text
authenticated actor
  -> active organization context
  -> Core effective authorization
  -> organization-scoped product/platform access
  -> domain invariant
```

### 1.2 Tenant isolation and permission checks are separate controls

A permission answers **what** the actor may do. Organization scope answers **to whose data** the action may apply. Neither substitutes for the other.

For non-Super-Admin users, a resource identifier from Organization B must never allow a user operating in Organization A to read, mutate, execute against, export, download or infer protected Organization B data.

### 1.3 Platform Super Admin is an explicit exception

Platform Super Admin behavior follows ADR-0003. `identity_users.is_super_admin = true` is a platform-wide authorization bypass after successful authentication. Cross-organization acceptance tests must therefore distinguish normal organization users from Platform Super Admin rather than reporting the designed Super Admin bypass as a tenant leak.

### 1.4 Core and products stay separate

KYROX Core remains product-agnostic. FAIR CRM and future products depend on Core through public contracts.

Forbidden:

- Core importing product code,
- product services importing Core runtime modules,
- shared Core/product SQLAlchemy sessions or connection pools,
- cross-repository database foreign keys,
- moving CRM business semantics into Core merely because code appears reusable.

### 1.5 Existing platform services are reused, not duplicated

Core already owns reusable identity, organization/membership, authorization, audit, settings, jobs and notifications capabilities. Product work must consume those public contracts where applicable instead of creating a second authorization, organization, audit or generic job platform inside a product.

Product-specific job handlers, workflow semantics and CRM actions remain product-owned.

### 1.6 Product semantics never leak into generic billing/entitlement infrastructure

If generic subscription, entitlement or usage infrastructure is promoted to Core later, Core stores/executes generic contracts only. Product semantics such as:

```text
scraper.enabled
quotes.enabled
bulk_email.enabled
max_customers
max_scraper_runs
```

remain owned by the product unless an explicit cross-product platform contract is accepted.

### 1.7 Current organization administration rules remain binding until explicitly changed

Do not invent an `Owner` role or self-service destructive organization authority from common SaaS conventions.

Current authorization governance classifies organization suspend/delete capabilities as SYSTEM scope. Self-service organization suspension/deletion, first-user role assignment, ownership transfer or similar lifecycle changes require an explicit product/platform decision and the corresponding permission/role/ADR changes before implementation.

### 1.8 No speculative platform build-out

During FAIR CRM M4, Core remains frozen against speculative platform development. Core changes are limited to bug/security/reliability work and reusable platform needs proven by a real product requirement. A future-looking capability does not become active merely because it appears in this roadmap.

---

# 2. Priority order

The sequence below is intentionally ordered from safety foundation to commercial capability to scale. Later phases must not be used to bypass unresolved P0 work.

## P0.0 — SaaS delivery governance enforcement — IMMEDIATE

### Goal

Make SaaS safety part of the normal KYROX delivery contract for every material change.

### Required actions

- Add SaaS-impact classification to the shared feature delivery/applicability flow.
- Treat tenant isolation, permission scope, Core/product ownership and production security regressions as hard failures.
- Require cross-organization tests whenever organization-owned data or organization-scoped execution changes.
- Require production-shaped runtime authorization evidence when static/unit tests cannot prove the security property.
- Keep “CI green” distinct from “SaaS-safe and accepted”.
- Require an explicit ownership decision before new reusable capabilities are added to Core.
- Require plan/entitlement/usage/billing effects to be classified before product code introduces package logic.

### Exit criteria

Every material delivery can answer:

```text
Does this change touch organization-owned data?
Does it change permission/system scope?
Does it change a Core/product boundary?
Does it affect entitlement/plan behavior?
Does it affect usage/quota behavior?
Does it affect organization/account lifecycle?
Does it introduce or expose secrets/security-sensitive behavior?
Does it add a background job, audit side effect or asynchronous execution path?
Does it affect export/delete/retention/data lifecycle?
Does it create a scaling dependency that is actually required now?
```

Affected dimensions are REQUIRED; unaffected dimensions are N/A with an architectural reason. No fake feature work is created merely to satisfy the checklist.

---

## P0.1 — Tenant isolation certification and regression gate — DONE 2026-08-26

### Goal

Prove that organization boundaries hold across every current and future organization-owned FAIR CRM path.

### Completion record

FAIR CRM completed TI-01 through TI-09 on 2026-08-26. The final adversarial certification is FAIR CRM PR #84 with Development Standard Gate #268 and Prod-Path E2E #140 green; the canonical Platform Super Admin exception is separately certified by Core PR #11 / Core CI #54. Detailed evidence is retained in `projects/fair-crm/backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md`.

### Coverage

At minimum:

- customers and contacts,
- fairs and participations,
- quotations and cost catalog,
- todos/activities,
- imports and import results,
- scraper/enrichment runs,
- operations/automation and run results,
- mail operations, SMTP/provider configuration and templates,
- exports/downloads/files/attachments,
- background jobs and scheduled/internal execution,
- admin/system endpoints that reference product data.

### Required test matrix

```text
Normal Organization A user -> Organization B resource: DENY / not exposed
OrganizationAdmin A        -> Organization B resource: DENY / not exposed
Platform Super Admin       -> platform model applies; cross-org bypass is allowed by design
```

Test list/detail/create/update/delete/archive/restore/execute/export/download paths where applicable. Direct resource IDs, bulk payloads and job/run IDs must not bypass scope.

### Exit criteria

- Cross-tenant regression tests are automated for every organization-scoped module.
- Organization scope is enforced at repository/use-case boundaries, not only UI routes.
- Request-body organization IDs are never treated as authorization context.
- Background/internal jobs carry validated organization context or have an explicit system-wide design.
- No unresolved cross-organization leak exists.

**Exit status:** **SATISFIED**. P0.1 is completed history; P0.2 is the next canonical priority but becomes active only through explicit promotion into the owning project roadmap.

---

## P0.2 — Organization lifecycle contract and SaaS onboarding decisions

### Goal

Define the commercial account lifecycle without duplicating Core organization/membership capabilities inside FAIR CRM.

### Existing baseline to reuse

Core owns organization and membership APIs, including organization creation, membership listing, invitations and invitation acceptance.

### Decisions required before implementation

- Who may create a new organization in the commercial flow?
- What role/capability does the first non-Super-Admin user receive?
- Is a separate business “owner” concept needed, or is OrganizationAdmin sufficient?
- Is ownership transfer required?
- May an organization request its own suspension/closure?
- Does actual suspend/delete remain Super-Admin-only, or is the current SYSTEM scope intentionally changed?
- What is the export/retention/delete sequence when a customer leaves?
- What happens to active sessions, jobs and provider credentials when an organization is suspended?

### Hard rule

Until these decisions are approved, do not invent self-service delete/suspend behavior, a new Owner role, or a second organization lifecycle inside FAIR CRM.

### Exit criteria

The full organization lifecycle is explicit, permission-scoped, auditable and backed by public Core contracts plus product orchestration where necessary.

---

## P0.3 — Production security hardening

### Goal

Raise the production runtime from single-product operational safety to commercial multi-organization SaaS safety.

### Immediate hardening review

- production dev bypass/fallback identity cannot become authority,
- JWT/auth secrets and provider/credential encryption secrets are separated by purpose,
- production requires explicit encryption secrets where credential-at-rest encryption depends on them,
- refresh cookie security settings are production-safe,
- CSRF protection remains enforced for cookie-auth mutating paths,
- sensitive logs/audit metadata redact secrets/tokens,
- provider/webhook signatures are verified where external callbacks exist,
- privileged/system endpoints fail closed,
- secret rotation/recovery procedures are documented when introduced.

### Deferred identity/security candidates

Email verification, password reset, MFA, login rate limiting/account lockout, refresh-token reuse detection and richer device/session controls are currently deferred platform candidates. They become active only through an explicit requirement/planning decision; do not implement them speculatively merely because they are common SaaS features.

### Exit criteria

No known production configuration permits a development bypass, cross-scope privilege escalation or avoidable credential exposure.

---

## P1.1 — Plan and entitlement architecture

### Goal

Allow commercial product packaging without hard-coding package names throughout FAIR CRM.

### Required ownership decision

Before implementation, decide which pieces are:

```text
Core generic capability
Product-owned entitlement semantics
Provider/billing adapter behavior
```

### Design constraints

- Avoid page/backend logic such as `if plan == "pro"` as the authorization model.
- Product feature entitlements are stable semantic capabilities, separate from role permissions.
- Permission answers whether a user may perform an action inside the organization.
- Entitlement answers whether the organization/product subscription includes the capability.
- The backend remains authoritative for entitlement enforcement; UI visibility/messages mirror backend truth.
- “No permission” and “not included in plan” are distinct outcomes.

### Exit criteria

The system has one approved entitlement contract and no parallel package-check systems.

---

## P1.2 — Usage metering and quota enforcement

### Goal

Measure organization usage and enforce package limits safely.

### Example dimensions

- active users,
- customer count,
- email sends,
- scraper/enrichment runs,
- imports,
- file/storage usage,
- API/automation execution where commercially relevant.

### Ownership examples

Generic counters/period semantics may be platform candidates only after an explicit ownership decision. Product metrics such as `max_customers` or `max_scraper_runs` remain FAIR CRM semantics unless generalized by accepted ADR.

### Hard requirements

- organization + metric + billing period scope,
- atomic quota checks for concurrent requests,
- idempotent accounting for retries,
- clear treatment of failed/cancelled executions,
- audit/diagnostic evidence for quota denials,
- no client-only quota enforcement.

### Exit criteria

Commercial limits are deterministic, concurrency-safe and observable.

---

## P1.3 — Billing and subscription integration

### Goal

Connect organization commercial state to plan/entitlement state without coupling product domain code to one payment provider.

### Current platform status

Billing/subscription hooks are a future Core candidate, not automatically active Core work. Activation requires a real product requirement plus the planning/ADR flow required by the M4 Core freeze.

### Design constraints

- provider adapters are replaceable,
- webhook/event processing is signed/verified and idempotent,
- subscription state is not inferred from UI success pages,
- grace period/cancel-at-period-end/suspension semantics are explicit,
- provider identifiers are not product authorization primitives,
- billing failure does not silently corrupt organization RBAC.

### Exit criteria

Subscription events deterministically produce the approved organization commercial state and entitlement state.

---

## P1.4 — SaaS onboarding UX

### Goal

Provide a clear first-run flow using existing Core capabilities instead of duplicating platform identity/organization logic.

Indicative flow after lifecycle decisions are approved:

```text
organization/account entry
  -> organization profile
  -> role/membership setup
  -> invite team
  -> connect mail/provider configuration
  -> add/import first customer
  -> run first approved workflow/automation
```

### Rules

- FAIR CRM orchestrates product UX; Core remains the source for identity/organization/membership/authorization.
- Do not preload later-stage data merely because a later onboarding step may need it.
- Permission errors, entitlement limits and temporary domain-state restrictions use distinct UI semantics.

### Exit criteria

A legitimate new organization can reach first product value through the approved production-shaped path without manual database edits.

---

## P1.5 — Data lifecycle / KVKK-GDPR readiness

### Goal

Define organization data ownership from creation to export, retention, anonymization/deletion and backup expiry.

### Required decisions

- export scope and format,
- retention period after cancellation/closure,
- anonymization vs hard delete by data class,
- audit-log retention/legal requirements,
- provider credential deletion/revocation,
- active job cancellation/drain policy,
- backup retention and when deleted organization data ages out of backups,
- restoration implications for previously deleted/anonymized data.

### Exit criteria

Organization exit is deterministic, auditable and does not leave uncontrolled product data or active credentials behind.

---

## P1.6 — SaaS administration and support surfaces

### Goal

Allow platform/product operators to manage organizations without direct SQL intervention.

### Scope rule

Every admin action must explicitly declare `organization` or `system` permission scope before implementation. System-wide organization lifecycle operations must not be made assignable to organization roles by UI convenience.

Potential views/actions include:

- organization status,
- commercial plan/subscription summary,
- user count and usage summary,
- quota state,
- entitlement override when explicitly designed,
- suspend/reactivate where policy allows,
- support/diagnostic context,
- audit/history links.

### Exit criteria

Operational support does not require uncontrolled database mutation and respects the canonical Super Admin/OrganizationAdmin boundary.

---

## P2.1 — Audit, observability and background-job hardening

### Goal

Improve operational evidence and asynchronous safety by extending existing Core/product infrastructure rather than replacing it.

### Existing baseline

Core Audit and Core Jobs already exist. FAIR CRM already has product-specific operation/job handlers and audit integration paths.

### Work areas

- audit coverage gap review,
- request/correlation/job identifiers,
- idempotency for retryable external/async operations,
- timeout and retry policies,
- duplicate execution prevention,
- organization context propagation,
- structured error/result metadata,
- metrics/tracing only when promoted from deferred status by measured need.

### Exit criteria

A material production operation can be traced from authenticated request through authorization, product execution, async work and final result without inventing a second platform service.

---

## P2.2 — Scale and infrastructure readiness

### Goal

Scale only from measured need, preserving the simple-first platform rule.

Candidates when justified:

- PostgreSQL connection-pool tuning,
- indexes/query-plan improvements,
- dedicated queue/worker scaling,
- Redis/cache where measured,
- object storage/file service,
- CDN for appropriate assets,
- horizontal API/worker scaling,
- tenant-aware storage/usage reporting,
- backup/restore performance hardening.

### Hard rule

Do not introduce Redis, event buses, microservices, extra databases, CDNs or distributed tracing solely because a mature SaaS product commonly has them. The need must be demonstrated and ownership must be explicit.

### Exit criteria

Scaling changes are backed by measured bottlenecks and production-shaped verification.

---

## P2.3 — Commercial SaaS launch gate

Commercial launch requires all applicable conditions below to be green or explicitly approved as N/A:

```text
[ ] Tenant isolation certification complete
[ ] Cross-organization regression suite green
[ ] Organization lifecycle decisions implemented and verified
[ ] Super Admin / OrganizationAdmin boundaries verified
[ ] Production dev bypass impossible
[ ] Purpose-separated secrets configured
[ ] Backup and restore acceptance verified
[ ] Entitlement enforcement verified if plans are live
[ ] Usage/quota concurrency and retry behavior verified if quotas are live
[ ] Billing webhook/event idempotency verified if billing is live
[ ] Organization export/retention/delete policy verified
[ ] Audit/security-event coverage accepted
[ ] Background-job organization scope and idempotency accepted
[ ] Runtime monitoring/health evidence available
[ ] Applicable load/performance acceptance complete
[ ] Canonical documentation/status/changelog synchronized
```

A missing applicable launch condition is not hidden by green CI.

---

# 3. Ownership matrix

| Capability | Canonical owner / decision rule |
|---|---|
| Identity/authentication | KYROX Core |
| Organizations/memberships | KYROX Core |
| RBAC/effective authorization | KYROX Core |
| Permission scope/catalog lifecycle | Core governance; product permission semantics registered through Core |
| Central audit platform | KYROX Core |
| Generic jobs platform | KYROX Core |
| FAIR CRM customer/fair/quote/todo/import/scraper semantics | FAIR CRM |
| FAIR CRM automation handlers and CRM results | FAIR CRM |
| CRM recipient/template/business mail orchestration | FAIR CRM |
| Generic billing/subscription hooks | Core candidate only after explicit product-driven ownership decision |
| Product package/feature semantics | FAIR CRM unless generalized by accepted ADR |
| Generic usage/metering primitives | Ownership decision required before Core implementation |
| Product quota meanings | FAIR CRM unless generalized by accepted ADR |
| Cross-repo SaaS strategy/standards | kyrox-platform |

---

# 4. SaaS-safe delivery rule for all future changes

The existing KYROX sequence becomes:

```text
Requirement
  -> ownership + organization/system scope decision
  -> SaaS-impact classification
  -> implementation
  -> targeted tests
  -> full applicable CI / strict-green quality checks
  -> tenant/security/entitlement/usage evidence where applicable
  -> production-shaped runtime authorization/workflow verification
  -> deployment synchronization
  -> canonical documentation/status/changelog update
  -> DONE
```

## Green is necessary, not sufficient

A change is **not DONE** merely because tests/build/CI are green when an applicable SaaS property remains unproven.

Examples:

- organization-scoped feature without cross-organization denial evidence,
- system permission accidentally assignable to an organization role,
- UI plan gate without backend entitlement enforcement,
- quota counter vulnerable to concurrent overrun,
- worker losing organization context,
- Core containing product-specific CRM semantics,
- product duplicating Core audit/authorization/organization infrastructure,
- development bypass usable in production,
- secret exposure in logs/audit/config,
- commercial lifecycle behavior invented without an approved decision.

These are acceptance failures even when ordinary unit tests pass.

---

# 5. Hard-fail / stop conditions

Stop implementation or reject acceptance when any of the following is discovered:

- organization/system scope is ambiguous,
- ownership between Core/product/provider is ambiguous,
- an organization-scoped data path has no scope strategy,
- cross-organization test coverage is missing for changed protected data access,
- request-body/path identifiers are trusted as organization authority without validated context,
- a SYSTEM permission can be granted to an organization role,
- a role name is used as an authorization bypass,
- a parallel Tenant account model is introduced without an accepted architecture change,
- a new Owner role or self-service destructive organization action is invented without explicit approval,
- product-specific entitlement/quota semantics are moved into Core without an ownership decision,
- plan names are hard-coded as the effective authorization mechanism,
- a product creates a second Core-owned audit/organization/authorization/jobs platform,
- a background job can process organization data without validated organization context or deliberate system scope,
- a security/tenant-isolation regression is proposed for baseline admission,
- CI is green but the real production-shaped protected path fails.

---

# 6. Activation and documentation rule

This roadmap is the canonical **cross-repository SaaS readiness strategy**.

When work becomes active:

1. decide owner and scope,
2. resolve required product/architecture decisions,
3. create/update the applicable ADR when the ownership/security model changes,
4. promote the concrete task into `projects/<owner>/ROADMAP.md`,
5. implement in the owning code repository,
6. verify through the shared delivery/quality gates,
7. update project status/changelog after delivery,
8. keep this file focused on cross-repository SaaS sequencing rather than sprint-level implementation history.

Do not copy this roadmap into `fair-crm` or `kyrox-core` code repositories.

---

## Related canonical documents

- [KYROX Workflow](WORKFLOW.md)
- [Ecosystem Roadmap](ROADMAP.md)
- [Known Deferred Work](KNOWN_DEFERRED.md)
- [Core/Product Separation — ADR-0002](decisions/0002-core-product-separation.md)
- [Identity Security Strategy — ADR-0003](decisions/0003-identity-security-strategy.md)
- [Audit Service Strategy — ADR-0004](decisions/0004-audit-service-strategy.md)
- [Role/Permission Governance — ADR-0005](decisions/0005-role-template-and-permission-governance.md)
- [FAIR CRM Constitution](../projects/fair-crm/CONSTITUTION.md)
- [FAIR CRM Permission Scope Governance](../projects/fair-crm/PERMISSION_SCOPE_GOVERNANCE.md)
- [KYROX Core Product Integration Guide](../projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)