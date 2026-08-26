# P0.1 Tenant Isolation Certification

Status: **IN PROGRESS**
Owner: FAIR CRM / SaaS readiness
Canonical roadmap: [`../../ecosystem/SAAS_ROADMAP.md`](../../ecosystem/SAAS_ROADMAP.md)

## Purpose

Certify that FAIR CRM organization-owned data and side effects remain isolated by the canonical `organization` account boundary across HTTP/API flows, repositories, relationships, exports/downloads and background execution.

This work does not introduce a new Tenant entity. `organization` remains the canonical account boundary. Permission scope answers **what** an actor may do; organization scope answers **whose data** the actor may access or mutate. Request body/query values are not trusted tenant authority.

P0.1 is complete only when relevant cross-tenant negative paths fail closed and the required isolation tests are green. Green CI alone is not sufficient.

## Audit scope

The certification covers organization-owned paths in:

- customers and customer child records,
- contacts,
- fairs,
- quotations and cost catalog,
- todos and worklists,
- imports,
- scraper,
- operations,
- mail / SMTP,
- exports and downloads,
- background jobs, retries, cancellation and status transitions,
- Platform Super Admin global-bypass behavior.

## Required invariants

1. Organization-owned reads, mutations and side effects are scoped by trusted organization context.
2. A foreign resource identifier must not become authority by itself.
3. Parent/child, source/target and bulk relationships must not cross organization boundaries.
4. Background authorization bypass must never imply tenant-isolation bypass.
5. Jobs carrying `organization_id` plus entity/job/run identifiers must re-load or mutate through an organization-scoped boundary.
6. Export/download access must re-check organization ownership; possession of a file/export identifier is not sufficient authority.
7. Foreign-organization resource probing should use not-found semantics where appropriate and must not disclose resource existence.
8. Platform Super Admin bypass is explicit and separately tested; users cannot self-assert it through request data.

## Current audit summary

### Strong certification candidates

These areas currently show consistent organization scoping in their main repository paths, subject to the negative tests listed below:

- Cost catalog CRUD and category/product relationships.
- Participation/activity main repository paths and bulk participation movement.
- Import batch/row/job repository boundaries and organization-carrying job commands.
- Operations aggregate/run/item repository chain.
- Customer main aggregate CRUD.
- Todo main aggregate/step/state repositories.
- Quote main CRUD.
- Scraper user-facing run detail/log/export paths that validate the parent run first.

### Gaps / hardening work

#### TI-01 — Scraper background tenant scope

Status: **IN REVIEW**
Severity: **HIGH / P0.1 blocker**
Implementation: `fair-crm` PR **#63** (`fix(scraper): enforce tenant scope in background run state`)

Problem:

Some scraper run-history/state-transition paths can fall back to `run_id`-only repository access. The background command carries organization context, but complete/fail/cancel/heartbeat-style transitions must preserve that scope through the repository mutation boundary.

Required:

- Require organization scope for background run loads and mutations.
- Ensure run-log access always derives from an organization-scoped parent run.
- Add mismatched `{organization_id, run_id}` negative tests for worker execution and state transitions.

Implemented in PR #63:

- Organization-scoped run-history reads and updates.
- Organization propagation through complete/fail/cancel/heartbeat transitions.
- Organization-aware cooperative cancellation checks.
- Worker-entry validation before scraper run-log or execution side effects.
- Cross-tenant negative tests for repository/service mutation, heartbeat and fair/enrichment/adapter-test workers.

Done when:

- Foreign run IDs cannot be read or mutated by a worker for another organization.
- Repository and worker tests prove fail-closed behavior.
- Existing scraper API/runtime tests remain green.

#### TI-02 — Background-job tenant contract

Status: **TODO**
Severity: **HIGH**

Problem:

A job payload carrying `organization_id` is not sufficient if downstream services or repositories later mutate by entity/job/run ID alone.

Required:

- Audit imports, scraper, operations and mail background consumers.
- Re-load/mutate organization-owned resources using organization-scoped repository boundaries.
- Add mismatched organization/entity/job tests for retry, cancel, status and execution paths.

Done when:

- Internal/AllowAll authorization adapters cannot cross tenant boundaries.
- Every organization-owned job fails closed on mismatched scope.

#### TI-03 — Mail / SMTP ownership chain

Status: **TODO**
Severity: **HIGH**

Problem:

Mail send/test/retry flows and SMTP/provider credentials combine sensitive configuration with side effects. Permission checks alone do not establish tenant ownership.

Required:

- Audit email/SMTP account list/detail/create/update/delete boundaries.
- Audit credential/provider lookups.
- Audit test-mail, send, retry and background-send paths.
- Prove foreign SMTP/email-account/mail-operation IDs cannot be used across organizations.

Done when:

- Account, credential, operation and background-send paths are organization-scoped.
- Cross-tenant negative tests are green.

#### TI-04 — Customer communication child repositories

Status: **TODO**
Severity: **MEDIUM/HIGH**

Problem:

Some customer communication child reads/replacements rely on an already validated `customer_id` and do not independently carry explicit organization scope at the child repository boundary.

Required:

- Scope child reads/replacements by organization plus parent customer identity, or enforce equivalent fail-closed ownership at the repository boundary.
- Add own-parent/foreign-child and foreign-parent/own-child tests where applicable.

Done when:

- Child access cannot cross organization boundaries even if the repository is invoked from another use case.

#### TI-05 — Quote render derived-ID hardening

Status: **TODO**
Severity: **MEDIUM**

Problem:

Quote CRUD is scoped, but render-time related records can be loaded through previously derived primary keys without repeating organization ownership checks.

Required:

- Harden organization-owned related lookups used during rendering.
- Add cross-linked/corrupt fixture tests such as Org A quote referencing an Org B customer/fair/template resource.

Done when:

- Render output cannot consume foreign organization data even under inconsistent relationship data.

#### TI-06 — Todo worklist join hardening

Status: **TODO**
Severity: **MEDIUM**

Problem:

The worklist begins from organization-scoped data, while some joined organization-owned tables rely on ID relationships without explicit organization predicates on every joined resource.

Required:

- Review worklist joins and add organization predicates where appropriate.
- Add cross-linked fixture tests.

Done when:

- Corrupt/mismatched relationships cannot expose another organization's Todo/Customer/outcome data.

#### TI-07 — Export / download ownership certification

Status: **TODO**
Severity: **HIGH**

Problem:

Every downloadable artifact must preserve organization ownership through creation, job completion and download. File/export IDs, paths or tokens must not become tenant authority by themselves.

Required:

- Inventory export/download endpoints across FAIR CRM.
- Verify parent/resource ownership on download.
- Verify generated-file/job ownership and storage-key derivation.
- Add foreign export/file/job negative tests.

Done when:

- Foreign exports/downloads fail closed across all covered modules.

#### TI-08 — Platform Super Admin isolation contract

Status: **TODO**
Severity: **HIGH**

Problem:

Canonical global bypass must be distinguished from ordinary tenant membership/permission checks and must not be user-assertable.

Required:

- Verify the current Core Super Admin bypass integration used by FAIR CRM.
- Test normal tenant actor, foreign tenant actor and Platform Super Admin separately.
- Verify request body/query/header data cannot grant global scope.

Done when:

- Canonical bypass behavior is explicit, tested and does not weaken normal tenant isolation.

#### TI-09 — Final P0.1 adversarial certification suite

Status: **TODO**
Severity: **RELEASE GATE**

Required matrix includes:

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
- Verification that audit/job/event records retain the correct organization context where applicable.

## Work order

Execute P0.1 in this order unless a newly discovered higher-severity gap changes priority:

1. **TI-01** Scraper background tenant scope.
2. **TI-02** Generic background-job tenant contract.
3. **TI-03** Mail / SMTP ownership chain.
4. **TI-04** Customer communication child repositories.
5. **TI-05** Quote render derived-ID hardening.
6. **TI-06** Todo worklist join hardening.
7. **TI-07** Export / download certification.
8. **TI-08** Platform Super Admin isolation contract.
9. **TI-09** Full adversarial certification suite and closure.

## P0.1 exit gate

P0.1 may be marked DONE only when:

- all confirmed isolation gaps are closed,
- all organization-owned background execution paths fail closed on mismatched scope,
- mail/SMTP and export/download ownership paths are certified,
- direct, nested, relational and bulk cross-tenant negative tests pass,
- Platform Super Admin behavior is separately verified,
- repository-, API- and worker-level tenant-isolation suites are green,
- relevant SaaS/security/permission-scope gates are satisfied,
- project status/changelog are updated with the delivered result.

## Change-record rule

Each implementation PR for this certification should reference the relevant `TI-xx` item and state:

- which isolation boundary was changed,
- why the old behavior was insufficient for P0.1,
- which negative tests prove the new fail-closed behavior,
- whether the change affects Core ownership or remains FAIR CRM-owned.

Do not move FAIR CRM business semantics into `kyrox-core`; reuse the existing Core organization/auth/RBAC/audit/jobs primitives.
