# P0.2 Organization Lifecycle Decisions — Temporary Draft

**Status:** TEMPORARY WORKING NOTE — NOT ACCEPTED POLICY  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**Purpose:** Keep the current real OL-05 → OL-10 Platform state visible while another topic is reviewed. This file must not be treated as an implementation authorization or as a replacement for ADR-0006.

## Current canonical state

| ID | Decision area | Current Platform state |
| --- | --- | --- |
| OL-05 | Self-service suspend/delete authority | **PENDING ACCEPTANCE** |
| OL-06 | Reactivation | **PENDING ACCEPTANCE** |
| OL-07 | Suspension job/provider behavior | **OPEN DETAIL** |
| OL-08 | Closure/export/retention/delete sequence | **PENDING ACCEPTANCE** |
| OL-09 | Retention/grace durations | **OPEN CHOICE** |
| OL-10 | Backup restore implications | **OPEN CHOICE** |
| OL-11 | Platform SuperAdmin vs organization management context | **PROPOSED — NOT ACCEPTED** |

## OL-05 — Self-service suspend/delete authority

### Verified baseline

- `identity.organizations.delete` and `identity.organizations.suspend` are SYSTEM-scope operations.
- Organization roles cannot receive those permissions.
- Current destructive lifecycle authority therefore remains platform/system controlled.

### Proposed direction already recorded in ADR-0006

- Keep actual suspend/delete execution as Platform Super Admin operations.
- An OrganizationAdmin-facing product may later expose a **request closure** workflow, but a request must not gain SYSTEM-scope destructive authority.

### Status

**PENDING ACCEPTANCE** — this direction is documented but not yet accepted as final lifecycle policy.

---

## OL-06 — Reactivation

### Verified baseline

- The Core organization domain already has a reactivation transition.
- The current public organization API does not expose a reactivation endpoint.

### Proposed direction already recorded in ADR-0006

- Add an explicit Platform Super Admin reactivation action before commercial suspension is considered operationally complete.
- The action must be auditable and lifecycle-tested.

### Status

**PENDING ACCEPTANCE** — the need and proposed direction are documented, but implementation is not yet authorized.

---

## OL-07 — Suspension job/provider behavior

### Verified runtime finding

Core suspension blocks new normal permission-protected work when authorization is checked, but already queued/running FAIR CRM work generally continues from previously established organization-scoped job context without re-checking Core organization lifecycle state.

Verified affected areas include:

- scraper background runs,
- enrichment runs,
- import analyze/apply/bulk jobs,
- scheduled/bulk email delivery,
- provider-backed outbound mail,
- product-owned credentials that remain active unless separately disabled.

Tenant isolation remains intact; this is a lifecycle-policy gap rather than a cross-tenant leak.

### Decisions still required

ADR-0006 / the runtime audit require explicit choices for at least:

1. session/refresh-token behavior on suspension,
2. queued jobs: cancel, pause or retain,
3. running scraper/enrichment: cooperative cancel or bounded drain,
4. import mutation behavior at suspension,
5. queued outbound mail disposition,
6. in-flight provider-call best-effort behavior,
7. provider credential usability during suspension,
8. audit evidence for transition and affected work.

### Status

**OPEN DETAIL** — the runtime gap is verified, but the exact per-capability policy is intentionally unresolved.

---

## OL-08 — Closure/export/retention/delete sequence

### Verified baseline

Core organization delete is currently a Core soft-delete/tombstone operation. It does not delete or orchestrate FAIR CRM product data, jobs, provider state, generated files or backups.

### Proposed staged offboarding direction already recorded in ADR-0006

```text
closure approved
  -> block new work
  -> settle/cancel active product work
  -> export if policy/user right requires it
  -> revoke/disable provider credentials
  -> apply product retention/anonymization/deletion policy
  -> handle generated files/artifacts
  -> define audit retention
  -> define backup ageing/restoration implications
  -> Core organization tombstone/soft-delete
```

Core must not directly manipulate FAIR CRM tables; product cleanup must use public product/Core contracts and explicit orchestration.

### Status

**PENDING ACCEPTANCE** — staged offboarding is documented as the proposed direction but is not yet accepted as final policy.

---

## OL-09 — Retention/grace durations

### Current state

No canonical numeric durations are accepted yet.

Before destructive closure implementation, Platform requires explicit decisions for:

- business-data retention after cancellation/closure,
- anonymization versus hard delete by data class,
- audit/security-log retention,
- generated-file retention,
- provider credential deletion/revocation timing,
- backup ageing,
- whether a closure grace/reactivation window exists and its duration.

These values are business/legal policy inputs and must not be invented from technical convenience.

### Status

**OPEN CHOICE** — no accepted `30 days`, `365 days`, or other numeric retention/grace rule currently exists in Platform.

---

## OL-10 — Backup restore implications

### Current state

Backup ageing and restoration behavior for suspended/closed/deleted organizations has not yet been accepted as a lifecycle contract.

ADR-0006 requires this to be explicit before destructive closure is implemented. The policy must define what happens if a backup contains data for an organization that has since been suspended, closed, anonymized or deleted.

No current canonical rule states that restore automatically reactivates, resurrects, re-tombstones or re-purges an organization; that behavior remains to be decided.

### Status

**OPEN CHOICE** — backup restore implications remain unresolved.

---

## OL-11 — Platform SuperAdmin and Organization Management Context Separation

### Problem / design question

The current FAIR CRM UI contains several areas under a broad `Admin` concept, but platform-level administration and tenant/organization-level administration are different security and operational contexts.

A Platform SuperAdmin should **not** be modeled as belonging to a special or synthetic organization merely so the UI can reuse organization-scoped behavior. Doing that would blur tenant isolation and create recurring exceptions around `organization_id`.

### Proposed identity model

- **SuperAdmin = platform-level identity**
- **OrganizationAdmin = tenant/organization-level identity**
- SuperAdmin remains outside normal organization membership.
- OrganizationAdmin operates only within its own organization scope.

### Proposed management-context split

#### Organization Management

Organization-scoped administration should contain tenant-owned capabilities such as:

- users,
- roles and permissions,
- SMTP / e-mail accounts,
- mail templates,
- organization-owned cost catalog,
- organization settings,
- organization-owned business data only.

Organization Management must never expose platform-wide data or destructive platform operations merely because the user has an organization admin role.

#### System Administration

Platform-level administration should contain capabilities such as:

- create / suspend / reactivate / close organizations,
- list and inspect all organizations,
- system backup / restore,
- health monitoring,
- background jobs,
- audit,
- maintenance mode,
- storage management,
- system-wide configuration.

These capabilities are Platform SuperAdmin scope.

### Backup boundary

**OrganizationAdmin must never see or control platform backup/restore.**

A FAIR CRM database backup may contain data belonging to multiple tenants, while a KYROX Core backup contains platform identity data such as users, organizations, roles, permissions and sessions. Backup/restore is therefore a platform/system operation, not an organization-management capability.

### Proposed UI architecture

A separate application is not required.

The preferred direction is to keep one frontend but expose distinct administration shells/contexts, for example:

```text
/organization/...
/system-admin/...
```

Normal Platform SuperAdmin operation should not require selecting an organization first.

Example platform flow:

```text
System Administration
  -> Organizations
  -> System Users / Identity
  -> Backups
  -> Health
  -> Audit
```

### SuperAdmin organization context / support access

When a Platform SuperAdmin needs to inspect or support a specific tenant, the system may provide an explicit action such as:

**View as Organization / Switch to Organization Context**

Example:

```text
ABC Fuarcılık
  -> View as Organization
  -> active organization context = ABC Fuarcılık
```

The critical rule is:

> The SuperAdmin does not become a member of ABC Fuarcılık. The system only opens an explicit, temporary organization context.

That context may allow the SuperAdmin to inspect the product under the selected tenant boundary, but it must not change the SuperAdmin's canonical platform identity or create synthetic organization membership.

### Target model

```text
SUPERADMIN
Platform scope
│
├── System Administration
│   ├── Organizations
│   ├── Backups
│   ├── Health
│   ├── Audit
│   └── Maintenance
│
└── View as Organization
      ↓
    ORGANIZATION CONTEXT
      ├── Customers
      ├── Fairs
      ├── Todos
      ├── Email Accounts
      └── Organization Settings
```

### Audit requirement

Any SuperAdmin entry into an organization context should be explicit and auditable.

Example audit evidence:

```text
Platform SuperAdmin
  -> entered organization context: ABC Fuarcılık
  -> viewed Customer X
```

This makes privileged tenant access observable instead of silently treating the SuperAdmin as an ordinary tenant member.

### UI naming direction

After lifecycle/security work is stabilized, the current broad `Admin` information architecture should be split into two explicit concepts:

- **Organization Management / Organizasyon Yönetimi**
- **System Administration / Sistem Yönetimi**

This UI/navigation rename and shell separation does **not** need to block the current P0.2 lifecycle work. The security boundary, however, must remain correct even before the UI is reorganized.

### Status

**PROPOSED — NOT ACCEPTED**

This section records a design proposal only. It must not be treated as implemented architecture or accepted Platform policy until it is reviewed and promoted into the canonical ADR/roadmap.

---

## Important boundary

This draft records **what Platform currently says plus explicit working proposals**, not a new accepted policy.

- OL-01 → OL-04 are already approved and their implementation workstream is complete.
- OL-05 → OL-10 remain gated exactly as shown above.
- OL-11 is a new working proposal and is **not accepted or implemented**.
- Do not mark OL-05 → OL-11 `ACCEPTED` here.
- Do not implement runtime lifecycle changes from this draft alone.
- Final decisions must be written back to ADR-0006 and then promoted into an implementation checklist before code changes begin.
