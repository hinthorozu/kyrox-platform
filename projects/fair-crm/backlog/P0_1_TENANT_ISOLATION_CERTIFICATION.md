# P0.1 Tenant Isolation Certification

Status: **IN PROGRESS**
Owner: FAIR CRM / SaaS readiness
Canonical roadmap: [`../../../ecosystem/SAAS_ROADMAP.md`](../../../ecosystem/SAAS_ROADMAP.md)

## Purpose

Certify that FAIR CRM organization-owned data and side effects remain isolated by the canonical `organization` account boundary across HTTP/API flows, repositories, relationships, exports/downloads and background execution.

This work does not introduce a new Tenant entity. `organization` remains the canonical account boundary. Permission scope answers **what** an actor may do; organization scope answers **whose data** the actor may access or mutate. Request body/query values are not trusted tenant authority.

P0.1 is complete only when all required cross-tenant negative paths fail closed and the required isolation evidence is green. Green CI alone is not sufficient.

## Required invariants

1. Organization-owned reads, mutations and side effects are scoped by trusted organization context.
2. A foreign resource identifier must not become authority by itself.
3. Parent/child, source/target and bulk relationships must not cross organization boundaries.
4. Background authorization bypass must never imply tenant-isolation bypass.
5. Jobs carrying `organization_id` plus entity/job/run identifiers must re-load or mutate through an organization-scoped boundary.
6. Export/download access must re-check organization ownership; possession of a file/export identifier is not sufficient authority.
7. Foreign-organization resource probing should use not-found semantics where appropriate and must not disclose resource existence.
8. Platform Super Admin bypass is explicit and separately tested; users cannot self-assert it through request data.

## Current certification state

The first P0.1 hardening wave is merged into `fair-crm/main` through PR **#82** (`fix: complete P0.1 tenant isolation certification`). The merge commit is `23a5087e9466afab542a9458c6f3654743067cbf`.

TI-07 export/download ownership certification is merged through FAIR CRM PR **#83** (`fix: certify P0.1 export and artifact tenant isolation`). The merge commit is `5fbd7ff703c1e3c8456213ccd5a7566e85025d24`. PR #83 passed Development Standard Gate **#263** and Prod-Path E2E **#136** after the tenant-isolation fixes and adversarial coverage below.

TI-08 Super Admin isolation certification is now in progress through Core PR **#11** (`test: certify P0.1 Super Admin isolation contract`). This is certification-only Core evidence; it does not change runtime authorization behavior.

These changes are implementation and gate evidence for the delivered work; they do **not** by themselves close TI-08 until its Core evidence is green, nor do they close the remaining TI-09 certification gate.

### Delivered hardening

| Item | Status | Evidence | Result |
| --- | --- | --- | --- |
| TI-01 Scraper background tenant scope | **DONE** | FAIR CRM #63, integrated through #73/#82 | Worker/run state, cancellation and transition paths preserve organization scope. |
| TI-02 Background-job tenant contract | **DONE** | FAIR CRM #64, integrated through #73/#82 | Import, data-operation and fair-email worker mismatch tests prove fail-closed outer job boundaries. |
| TI-03 Mail / SMTP ownership chain | **DONE** | FAIR CRM #65 and #66, integrated through #74/#75/#82 | Email-account/provider config and fair-email batch/outbox mutations are organization-scoped. |
| TI-04 Customer communication child repositories | **DONE** | FAIR CRM #67, integrated through #76/#82 | Child reads/replacements and shared query helpers carry organization scope. |
| TI-05 Quote render derived-ID hardening | **DONE** | FAIR CRM #68, integrated through #77/#82 | Render-time customer/fair/template/content/tag references fail closed on foreign derived IDs. |
| TI-06 Todo worklist join hardening | **DONE** | FAIR CRM #72, integrated through #81/#82 | Worklist/follow-up joins validate authoritative organization across derived references. |
| TI-07 Export / download ownership certification | **DONE** | FAIR CRM #83; merge `5fbd7ff703c1e3c8456213ccd5a7566e85025d24`; Development #263; Prod-Path #136 | Customer Excel derived joins are tenant-scoped, scraper artifacts fail closed on foreign/corrupt run pointers, and quote-template logos are no longer unauthenticated public static assets. |

### TI-07 adversarial evidence

FAIR CRM #83 certifies the covered downloadable/generated artifact boundaries with deterministic negative tests:

- Customer Excel export does not follow an own participation to a foreign fair.
- Customer Excel export does not follow a foreign participation cross-linked to an own customer.
- Scraper Excel download rejects a stored artifact pointer that resolves to another run and rejects direct foreign-run download.
- Managed quote-template logo delivery requires authenticated organization scope; a foreign organization receives not-found semantics.
- The legacy unauthenticated quote-logo static path is no longer mounted.
- Quote-template create/update reject managed logo pointers owned by another organization.
- Quote rendering inlines only the authoritative organization's managed local logo and rejects unsafe/traversal storage resolution.

### Additional P0.1 hardening delivered in the first wave

These findings were discovered during the audit and were merged without inventing new TI numbers:

- FAIR CRM #69 — template-management derived references.
- FAIR CRM #70 — participation derived-parent joins and shared participation existence correlation.
- FAIR CRM #71 — activity derived-customer search/sort join.
- FAIR CRM #72 — todo worklist/follow-up derived references.

The consolidated integration sequence was #73–#81, followed by final integration PR #82.

## Remaining certification gates

### TI-08 — Platform Super Admin isolation contract

Status: **IN PROGRESS**
Severity: **HIGH**

The canonical Platform Super Admin global bypass is accepted architecture. It must be distinguished from ordinary tenant membership and permission checks and must not be user-assertable.

Current evidence:

- Core derives Super Admin authority from the authenticated token subject plus the DB-backed `identity_users.is_super_admin` snapshot; request data does not define the flag.
- FAIR CRM Prod-Path E2E #136 passed the existing live checks where the canonical Super Admin authorizes a foreign organization and organization-header mismatch through Core.
- FAIR CRM role-matrix tests reject foreign organization scope for ordinary organization roles.
- Core PR #11 adds API-level certification that a normal authenticated user cannot self-assert global scope through body/query/header data, while the same already-issued access token gains global scope only after the authoritative Core DB user row becomes Super Admin.

Required:

- Verify the current Core Super Admin bypass integration used by FAIR CRM.
- Test normal tenant actor, foreign tenant actor and Platform Super Admin separately.
- Verify request body, query and header data cannot grant global scope.
- Verify authorization bypass does not accidentally turn lower repository/job boundaries into unscoped tenant access for ordinary actors.

Done when:

- Core PR #11 evidence is green and merged.
- Canonical bypass behavior is explicit and tested.
- Ordinary users cannot self-assert or inherit global tenant scope.

### TI-09 — Final P0.1 adversarial certification suite

Status: **TODO**
Severity: **RELEASE GATE**

The final matrix must cover, where applicable:

- Tenant A accessing its own resource.
- Tenant A using Tenant B direct UUID.
- Own parent + foreign child and foreign parent + own child.
- Cross-organization source/target relationship mutation.
- Mixed-organization bulk IDs.
- Request-body/query organization spoofing.
- Organization-header spoofing and missing organization context.
- Mismatched background `{organization_id, entity_id/job_id/run_id}`.
- Foreign retry/cancel/status/heartbeat.
- Foreign export/download.
- Foreign SMTP/email account/operation identifiers.
- Cross-linked database fixtures where relationship-derived IDs are trusted.
- Platform Super Admin canonical bypass.
- Audit/job/event records retaining the correct organization context where applicable.

Done when:

- The matrix is represented by deterministic automated evidence or an explicitly documented non-applicability decision.
- Repository-, API-, worker- and production-shaped gates required by the matrix are green.

## Work order from current state

1. **TI-08** Platform Super Admin isolation contract.
2. **TI-09** Final adversarial certification suite and closure.

Newly discovered tenant-isolation findings take priority if their severity is higher than the current item.

## P0.1 exit gate

P0.1 may be marked **DONE** only when:

- TI-01 through TI-09 are DONE or have an explicit approved non-applicability record,
- all confirmed isolation gaps are closed,
- all organization-owned background execution paths fail closed on mismatched scope,
- mail/SMTP and export/download ownership paths are certified,
- direct, nested, relational and bulk cross-tenant negative tests pass,
- Platform Super Admin behavior is separately verified,
- repository-, API- and worker-level tenant-isolation suites are green,
- relevant SaaS/security/permission-scope gates are satisfied,
- project status/changelog are updated with the delivered result.

## Change-record rule

Each implementation PR for this certification should state:

- which isolation boundary was changed or certified,
- why the previous evidence was insufficient for P0.1,
- which negative tests prove fail-closed behavior,
- whether the change affects Core ownership or remains FAIR CRM-owned.

Do not move FAIR CRM business semantics into `kyrox-core`; reuse the existing Core organization/auth/RBAC/audit/jobs primitives.
