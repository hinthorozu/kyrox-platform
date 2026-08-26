# P0.1 Tenant Isolation Certification

Status: **DONE**
Owner: FAIR CRM / SaaS readiness
Completed: **2026-08-26**
Canonical roadmap: [`../../../ecosystem/SAAS_ROADMAP.md`](../../../ecosystem/SAAS_ROADMAP.md)

## Purpose

Certify that FAIR CRM organization-owned data and side effects remain isolated by the canonical `organization` account boundary across HTTP/API flows, repositories, relationships, exports/downloads and background execution.

This work does not introduce a new Tenant entity. `organization` remains the canonical account boundary. Permission scope answers **what** an actor may do; organization scope answers **whose data** the actor may access or mutate. Request body/query values are not trusted tenant authority.

## Required invariants

1. Organization-owned reads, mutations and side effects are scoped by trusted organization context.
2. A foreign resource identifier does not become authority by itself.
3. Parent/child, source/target and bulk relationships cannot cross organization boundaries.
4. Background authorization bypass does not imply tenant-isolation bypass.
5. Jobs carrying `organization_id` plus entity/job/run identifiers re-load or mutate through an organization-scoped boundary.
6. Export/download access re-checks organization ownership; possession of a file/export identifier is not sufficient authority.
7. Foreign-organization resource probing uses fail-closed/not-found semantics where appropriate and does not disclose foreign resource content.
8. Platform Super Admin bypass is explicit and separately tested; users cannot self-assert it through request data.

## Final certification state

P0.1 is complete. The hardening and certification sequence is merged across FAIR CRM and Core:

- FAIR CRM first hardening wave: PRs **#63–#72**, integrated through **#73–#82**; #82 merge `23a5087e9466afab542a9458c6f3654743067cbf`.
- TI-07 export/download ownership certification: FAIR CRM **#83**, merge `5fbd7ff703c1e3c8456213ccd5a7566e85025d24`; Development Standard Gate **#263** and Prod-Path E2E **#136** passed.
- TI-08 Platform Super Admin isolation contract: Core **#11**, merge `c0392f8c351593e28d0e18755e93768ff603f4f4`; Core CI **#54** passed. FAIR CRM production-shaped Super Admin integration is also covered by Prod-Path E2E.
- TI-09 final adversarial certification: FAIR CRM **#84**, merge `d167bbd88ac8561c39c70b870728b63e3ffc7956`; Development Standard Gate **#268** and Prod-Path E2E **#140** passed on final head `11e7146971c3b1fb30e0cfccd06cc5878b7004e5`.

### Delivered hardening

| Item | Status | Evidence | Result |
| --- | --- | --- | --- |
| TI-01 Scraper background tenant scope | **DONE** | FAIR CRM #63, integrated through #73/#82 | Worker/run state, cancellation and transition paths preserve organization scope. |
| TI-02 Background-job tenant contract | **DONE** | FAIR CRM #64, integrated through #73/#82 | Import, data-operation and fair-email worker mismatch tests prove fail-closed outer job boundaries. |
| TI-03 Mail / SMTP ownership chain | **DONE** | FAIR CRM #65 and #66, integrated through #74/#75/#82 | Email-account/provider config and fair-email batch/outbox mutations are organization-scoped. |
| TI-04 Customer communication child repositories | **DONE** | FAIR CRM #67, integrated through #76/#82 | Child reads/replacements and shared query helpers carry organization scope. |
| TI-05 Quote render derived-ID hardening | **DONE** | FAIR CRM #68, integrated through #77/#82 | Render-time customer/fair/template/content/tag references fail closed on foreign derived IDs. |
| TI-06 Todo worklist join hardening | **DONE** | FAIR CRM #72, integrated through #81/#82 | Worklist/follow-up joins validate authoritative organization across derived references. |
| TI-07 Export / download ownership certification | **DONE** | FAIR CRM #83; merge `5fbd7ff703c1e3c8456213ccd5a7566e85025d24`; Development #263; Prod-Path #136 | Customer Excel derived joins are tenant-scoped, scraper artifacts fail closed on foreign/corrupt run pointers, and quote-template logos require managed tenant-scoped delivery. |
| TI-08 Platform Super Admin isolation contract | **DONE** | Core #11; merge `c0392f8c351593e28d0e18755e93768ff603f4f4`; Core CI #54; FAIR CRM Prod-Path | Global scope is derived from authenticated identity plus Core DB `is_super_admin`; ordinary users cannot self-assert it through request body/query/header data. |
| TI-09 Final adversarial certification suite | **DONE** | FAIR CRM #84; merge `d167bbd88ac8561c39c70b870728b63e3ffc7956`; Development #268; Prod-Path #140 | Remaining bulk, source/target, spoofing, missing-context, contacts, activities, cost-catalog and audit-context gaps have deterministic negative evidence. |

### Additional P0.1 hardening delivered in the first wave

These findings were discovered during the audit and were merged without inventing new TI numbers:

- FAIR CRM #69 — template-management derived references.
- FAIR CRM #70 — participation derived-parent joins and shared participation existence correlation.
- FAIR CRM #71 — activity derived-customer search/sort join.
- FAIR CRM #72 — todo worklist/follow-up derived references.

## TI-09 final adversarial matrix

| Adversarial case | Final evidence |
| --- | --- |
| Tenant A accesses its own resource | Existing CRUD/API suites across customers, fairs, contacts, activities, todos, operations, templates, quotations and cost catalog. |
| Tenant A uses Tenant B direct UUID | Existing customer/fair/todo/operation/template suites plus FAIR CRM #84 contact, activity and cost-catalog direct-ID tests. |
| Own parent + foreign child / foreign parent + own child | FAIR CRM #67–#72 derived-reference suites; #84 foreign contact parent and cost-product/category cross-link tests. |
| Cross-organization source/target mutation | FAIR CRM #84 proves participation bulk move cannot target a foreign fair. |
| Mixed-organization bulk IDs | FAIR CRM #84 proves import-row bulk decisions and activity bulk deletion ignore/reject foreign IDs without mutating foreign rows. |
| Request body/query organization spoofing | FAIR CRM #84 proves body/query `organization_id` cannot override authenticated organization context. |
| Organization-header spoofing and missing organization context | Ordinary-role foreign-header denial is covered by FAIR CRM role-matrix tests; Core #11 proves header/request data cannot assert global scope; #84 proves missing organization context fails closed. |
| Mismatched background `{organization_id, entity_id/job_id/run_id}` | TI-01/TI-02 suites cover scraper, import, data-operation and fair-email workers. |
| Foreign retry/cancel/status/heartbeat | TI-01 scraper lifecycle tests prove foreign scope cannot mutate run state or heartbeat. |
| Foreign export/download | TI-07 / FAIR CRM #83 covers customer export, scraper artifacts and managed quote logos. |
| Foreign SMTP/email account/operation identifiers | TI-03 / FAIR CRM #65–#66 covers account/config and fair-email child ownership. |
| Cross-linked database fixtures / corrupt derived IDs | FAIR CRM #68–#72 and #83 cover quote, template, participation, activity, todo/worklist, export and artifact derived references. |
| Platform Super Admin canonical bypass | Core #11 + Core CI #54 and FAIR CRM production-shaped Prod-Path evidence prove DB-backed global scope and ordinary-user denial. |
| Audit/job/event organization context | TI-02 organization-owned job entities plus FAIR CRM #84 explicit duplicate-merge audit `organization_id` assertion. |

## P0.1 exit gate — satisfied

P0.1 was marked **DONE** on 2026-08-26 because:

- TI-01 through TI-09 are DONE,
- all confirmed isolation gaps found during the certification audit are closed,
- organization-owned background execution paths fail closed on mismatched scope,
- mail/SMTP and export/download ownership paths are certified,
- direct, nested, relational and bulk cross-tenant negative tests pass,
- Platform Super Admin behavior is separately verified,
- repository-, API-, worker- and production-shaped gates required by the matrix are green,
- Core/product ownership boundaries remain intact,
- project and ecosystem status/change records are updated as part of the closure PR.

## Work order after P0.1

P0.1 no longer owns active implementation work. The next canonical priority is **P0.2 — Entitlement enforcement path**, but roadmap order does not itself start implementation; P0.2 must be explicitly promoted/started under the normal project workflow.

Newly discovered tenant-isolation regressions remain release-blocking security defects and must be handled ahead of lower-severity work.

## Change-record rule

Future tenant-isolation changes should state:

- which isolation boundary changed or was re-certified,
- which negative tests prove fail-closed behavior,
- whether the change affects Core ownership or remains FAIR CRM-owned.

Do not move FAIR CRM business semantics into `kyrox-core`; reuse the existing Core organization/auth/RBAC/audit/jobs primitives.
