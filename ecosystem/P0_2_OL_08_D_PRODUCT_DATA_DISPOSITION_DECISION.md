# P0.2 OL-08D — Product-Data Disposition Matrix Decision

**Status:** ACCEPTED — PRODUCT-DATA MATRIX ACCEPTED; DESTRUCTIVE RUNTIME STILL GATED  
**Accepted:** 2026-09-09  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Decision readiness:** `ecosystem/P0_2_OL_08_DECISION_READINESS.md`  
**Related export contract:** `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`  
**Related credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`  
**Related retention policy:** `ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`

## Purpose

Define the organization-offboarding disposition for FAIR CRM relational product data after the accepted OL09-A reversible grace, without silently widening this decision into provider-secret handling, generated-file deletion, backup ageing, closure-package lifecycle or Core tombstone.

OL08-D answers **what happens to relational product data**. It does not by itself authorize the destructive worker.

## Accepted policy

For the currently verified FAIR CRM model, the default organization-offboarding disposition is:

> **Tenant-owned relational product data is hard-deleted after the valid 30-day SUSPENDED grace and after every applicable phase-specific dependency is satisfied.**

No currently verified tenant-owned product-data class is accepted for long-lived anonymized retention.

The matrix therefore uses four boundaries:

1. **HARD_DELETE** — tenant-owned relational product data,
2. **RETAIN_SYSTEM** — shared/global system catalogs that are not owned by the closing organization,
3. **SEPARATE_POLICY** — closure/security evidence, credentials, generated/binary artifacts and backups governed by another accepted/offboarding policy,
4. **OUTSIDE_FAIR_CRM_OWNERSHIP** — Core-owned identity/session/token state.

Anonymization is **not** a fallback. A future data class may use anonymization only through an explicit revision that states why hard deletion is inappropriate and defines the irreversible transformation.

## Timing boundary

OL09-C is authoritative for product-data timing:

```text
organization becomes SUSPENDED
  -> 30-day reversible grace
  -> grace validly satisfied
  -> accepted OL08-D HARD_DELETE classes become time-eligible
```

There is no additional generic `+30`, `+60`, `+90` or other product-data retention interval after the 30-day grace.

Time eligibility is not execution authorization. A class remains blocked while any required export, credential, artifact, lifecycle, referential-integrity or other accepted obligation is unresolved.

## Verified current FAIR CRM ownership facts

The current FAIR CRM model uses explicit organization ownership on the primary product-data rows, including customers, contacts, fairs, participations, activities, todos/worklists, quotes/templates/content, cost-catalog records, imports/data-integration jobs, scraper/enrichment state, operations/runs, mail templates, mail-send history/batches and email-account metadata.

Several child rows inherit ownership from an organization-owned parent rather than carrying a directly usable organization key. Cleanup must resolve those children through the verified parent relationship; it must not perform an unscoped table-wide delete.

The current schema also contains meaningful `RESTRICT`, `SET NULL` and `CASCADE` edges. Database cascade convenience is not the policy. The destructive implementation must use an explicit dependency order and certify every covered edge.

## Accepted disposition matrix

| Data class | Current examples | Disposition | Required boundary |
| --- | --- | --- | --- |
| Customers | `crm_customers` | **HARD_DELETE** | Grace satisfied; export dependency satisfied. |
| Customer communications | customer email/phone/website child rows | **HARD_DELETE** | Delete with verified customer ownership/cascade. |
| Contacts | `crm_contacts` | **HARD_DELETE** | Grace/export gates. |
| Fairs | `crm_fairs` | **HARD_DELETE** | Delete only after quote/todo/participation `RESTRICT` dependents are removed. |
| Customer fair participations | `crm_customer_fair_participations` | **HARD_DELETE** | Remove before referenced fair. |
| Activities | `crm_activities` | **HARD_DELETE** | Grace/export gates; do not retain CRM narrative as audit evidence. |
| Todos and workflow state | `crm_todos`, steps, outcome definitions, worklist states | **HARD_DELETE** | Remove fair-restricting todos before fairs; child workflow rows first/cascade as certified. |
| Quotes | `crm_quotes` | **HARD_DELETE** | Remove before customer/fair/template rows because those references are restrictive. |
| Quote templates and versions | `crm_quote_templates`, `crm_quote_template_versions` | **HARD_DELETE** | Break current-version/version cycle deterministically; logo bytes remain OL08-E. |
| Portable template-content data | `crm_template_contents`, `crm_template_content_tags` | **HARD_DELETE** | Contents before tag rows where required by `RESTRICT`. |
| Cost catalog | `crm_cost_products`, `crm_cost_categories` | **HARD_DELETE** | Products before categories because product→category is `RESTRICT`. |
| Import metadata and structured rows | `crm_import_batches`, `crm_import_rows`, import jobs/templates | **HARD_DELETE** | Import child rows/jobs before batches as required. Embedded/raw upload bytes remain artifact-gated as described below. |
| Scraper/enrichment relational state | run history/logs, tenant adapters/hides, customer enrichment state | **HARD_DELETE** | External/generated output files remain OL08-E; remove relational rows only after required artifact/export dependency is resolved. |
| Operations/automation relational state | `crm_operations`, runs, run items/payload/result metadata | **HARD_DELETE** | Run items → runs → operation; external result artifacts remain OL08-E. |
| Mail templates | `crm_mail_templates` | **HARD_DELETE** | Grace/export gates. |
| Mail-send/customer communication history | `mail_send_operations` | **HARD_DELETE** | Includes recipient, rendered message body and provider/status metadata; must not be copied into long-lived audit evidence. |
| Fair-email batch metadata | `crm_fair_email_batches` | **HARD_DELETE** | Delete with mail-send communication state. |
| Email-account non-secret product configuration | `email_accounts` metadata | **HARD_DELETE**, **credential-gated** | Only after OL08-C obligations for the account are complete and retained closure evidence no longer requires the live parent row. |
| SMTP/provider secret-bearing config | SMTP/provider config rows | **SEPARATE_POLICY — OL08-C**, then parent cleanup | Hard deletion must never be used as fabricated evidence of provider revoke/secret-disposition success. |
| Closure execution/event evidence | closure executions/events | **SEPARATE_POLICY — OL09-D** | Minimal non-secret evidence retained 12 months from accepted durable terminal closure milestone. |
| Closure export-plan evidence | closure export plans/manifests/digests | **SEPARATE_POLICY — OL09-D** | Retain only accepted minimal non-secret control evidence. |
| Credential-disposition evidence | credential dispositions/events | **SEPARATE_POLICY — OL09-D / OL08-C** | Retained evidence must not retain reusable secrets. |
| Generated/binary product artifacts | uploads, logos, scraper/operation output files, generated exports | **SEPARATE_POLICY — OL08-E** | No relational delete may strand or prematurely destroy a required artifact obligation. |
| Future persistent closure package | package bytes/object | **SEPARATE_POLICY — OL08-B / OL08-E / OL09-E** | 30-day package window only if separately authorized/materialized. |
| Global/shared system catalogs | e.g. `operation_types` | **RETAIN_SYSTEM** | No organization-owned row to delete. |
| Derived dashboard views | derived/non-source views | **NO INDEPENDENT RETENTION** | Disappear with source product data; do not materialize for closure evidence. |
| Core identity/session/token state | Core-owned auth/lifecycle data | **OUTSIDE_FAIR_CRM_OWNERSHIP** | Core remains authority; FAIR CRM must not delete it as OL08-D work. |
| Database backups / restore images | system DB backup payloads and restore state | **SEPARATE_POLICY — OL-10** | Product-row hard delete does not imply backup erasure. |

## Why HARD_DELETE rather than anonymization

The verified tenant-owned product model contains customer/business identity, contacts, communication content, operational payloads, imported raw/normalized rows, scraper/enrichment outputs, quote/template content and workflow history whose continuing product purpose ends with final organization offboarding.

The separately accepted OL09-D policy already provides the narrow mechanism for retaining the minimum non-secret closure/security evidence needed after product cleanup.

Keeping anonymized copies of ordinary CRM/product rows would therefore create a second retention system without a demonstrated product, security or closure requirement.

Accordingly:

- **hard delete is the accepted product-data disposition**, and
- **minimal control evidence is retained separately**, not derived by leaving anonymized product rows behind.

If a future legal/business requirement needs class-specific anonymized retention, that requirement must be explicitly accepted before implementation.

## Critical credential/evidence boundary

Current credential-disposition evidence references `email_accounts` with a restrictive FK. That implementation detail must **not** silently extend retention of the full email-account product row for the 12-month OL09-D evidence period.

Before email-account metadata becomes destructively eligible, the implementation must provide an accepted evidence-safe relationship that preserves only the minimum required non-secret account/credential identity while allowing the product account row to be deleted.

Acceptable implementation shapes may include a durable non-secret scalar identifier and an FK that is safely nullable/detached, provided referential/evidence integrity remains deterministic.

The policy does not prescribe one migration shape here, but it requires all of the following:

- no reusable secret copied into evidence,
- no secret hash/fingerprint retained as a credential oracle,
- no full email-account product record retained merely to satisfy an audit FK,
- no account/config deletion before OL08-C required provider invalidation/local-secret obligations are complete,
- no declaration of credential success from product-row deletion alone.

This is a **mandatory implementation gate**, not an optional optimization.

## Artifact-bearing relational rows

Some relational rows contain or point to artifact material, including examples such as:

- import `stored_file_content`,
- quote-template `logo_url`,
- scraper output JSON/Excel paths,
- operation/scraper handoff/result references.

OL08-D accepts the relational row as HARD_DELETE product data, but it does **not** use relational deletion to bypass OL08-E.

Rules:

- if deleting the row would itself destroy embedded binary/upload content governed by OL08-E, the row remains blocked until OL08-E authorizes that artifact disposition,
- if the row only points to external/object-storage bytes, the implementation must first preserve whatever locator/evidence OL08-E needs and satisfy the accepted artifact action before the source locator is destroyed,
- artifact cleanup success must be independently evidenced; a missing relational pointer is not proof that external bytes were deleted,
- source artifacts required for an accepted export/package flow must remain until that dependency is complete.

## Dependency-aware deletion contract

The implementation must not issue a generic `DELETE ... WHERE organization_id = ?` across tables in arbitrary order.

Known current ordering constraints include:

- quotes restrict deletion of referenced customers, fairs and quote templates,
- customer-fair participations restrict deletion of referenced fairs,
- todos restrict deletion of referenced fairs,
- cost products restrict deletion of categories,
- template contents restrict deletion of content tags,
- quote templates/versions form a current-version/version restrictive cycle,
- closure credential-disposition evidence restricts deletion of referenced email accounts.

A safe implementation must therefore maintain an explicit, versioned dependency plan.

### Minimum accepted ordering shape

The exact runtime can split this into transactions/chunks, but its semantic ordering must satisfy at least:

1. **Preconditions / blockers**
   - authoritative same suspension episode still `SUSPENDED`,
   - OL09-A 30-day grace validly satisfied,
   - required export/package obligations satisfied,
   - no unresolved phase-specific legal/policy hold,
   - class-specific OL08-E dependencies satisfied,
   - credential-dependent account rows blocked until OL08-C permits them.

2. **Leaf operational/history rows**
   - mail-send history / fair-email batch rows,
   - operation run items → runs → operations,
   - scraper logs and run/enrichment/tenant-adapter state,
   - import jobs/rows and then batch/template metadata,
   - quotes before their referenced customer/fair/template parents.

3. **Workflow/relationship rows**
   - todo worklist/step rows and todos,
   - activities,
   - participations.

4. **Primary CRM entities**
   - contacts,
   - customers,
   - fairs.

5. **Tenant configuration/content catalogs**
   - quote-template cycle broken deterministically, then versions/templates,
   - template contents before tags,
   - cost products before categories,
   - mail templates.

6. **Email-account product metadata**
   - only after OL08-C completion and evidence-parent decoupling requirements are satisfied,
   - secret-bearing config handling remains independently certified under OL08-C.

This list is a minimum policy ordering. Runtime implementation must re-derive and test the complete FK graph against the exact code/migration head before destructive authorization.

## Ownership/scoping rules

Every destructive handler must be tenant-safe by construction.

Required:

- organization-owned root rows are selected by the authoritative target organization,
- child rows without direct organization ownership are selected only through verified organization-owned parent identities,
- a foreign-organization ID supplied through an API/request must never widen the delete set,
- no table-wide cleanup based solely on user-supplied IDs,
- no cross-organization cascading relation may be assumed safe without invariant/test evidence,
- unexpected ownership mismatch fails closed before mutation.

A DB cascade may implement a verified child deletion, but the closure engine must still know that the child class exists and must certify its ownership and expected deletion semantics.

## Export-before-delete boundary

OL08-B remains the export authority.

No HARD_DELETE class may be destroyed while an accepted required closure export/package obligation still needs that class or its artifact.

Current `not_required` export success remains gated until separately accepted policy authority exists. OL08-D does not create such authority.

Deletion evidence must not be used as a substitute for export completeness evidence.

## Evidence for destructive product cleanup

The future destructive engine must record **minimal non-secret control evidence**, not copies of deleted product content.

Per class/phase, evidence may include:

- organization + closure execution identity,
- policy/matrix version,
- class key,
- action (`hard_delete`),
- started/completed/blocked timestamps,
- deterministic row counts before/after,
- bounded reason/error codes,
- dependency status,
- implementation/schema version.

It must not retain:

- customer names/contact details,
- message subjects/bodies,
- imported raw rows,
- scraper result payloads/log bodies,
- operation payload/result bodies,
- reusable credentials,
- raw provider signatures/webhook payloads,
- secret hashes/fingerprints.

Such cleanup evidence is itself governed by OL09-D.

## Failure, retry and restart semantics

Destructive cleanup must be fail-closed, idempotent and restart-safe.

Required behavior:

- completed class handlers are not reinterpreted as permission to skip later required classes,
- retry re-evaluates current lifecycle/dependency authority before new irreversible mutation,
- an FK/restrict failure becomes explicit blocked evidence rather than a force-delete workaround,
- unexpected residual rows prevent class completion,
- process downtime does not reset grace or create a new delete deadline,
- partial deletion must resume from durable class/phase evidence rather than restart from an unsafe global delete,
- no retry may reconstruct deleted customer/product payload merely to prove what was deleted.

## Reactivation boundary

Before the accepted 30-day grace is satisfied, reactivation invalidates destructive eligibility for that suspension episode under OL09-A.

No OL08-D hard delete may run during the reversible grace.

Once irreversible product cleanup has lawfully begun after grace and all accepted gates, reactivation semantics must remain governed by the final closure orchestration contract; the product engine must never silently recreate deleted product data.

## Explicitly not authorized by this decision

OL08-D acceptance does **not** itself authorize:

- a production hard-delete/anonymization worker,
- an unreviewed generic SQL organization purge,
- artifact/file deletion — OL08-E,
- persistent closure-package creation/delivery — OL08-B / OL08-E,
- `not_required` export success,
- provider/API-token revoke success — OL08-C,
- secret deletion as a substitute for external invalidation evidence,
- evidence cleanup before OL09-D expiry,
- backup ageing/restore reconciliation — OL-10,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

The destructive OL08-05 runtime remains gated until the remaining artifact/package action contract and backup/restore boundary allow a bounded implementation to be safely authorized.

## Acceptance checklist

- [x] Current verified tenant-owned relational product data defaults to HARD_DELETE.
- [x] No current product-data class is accepted for anonymized long-lived retention.
- [x] Global/shared system catalogs are retained and are not treated as tenant rows.
- [x] Closure/audit/security evidence remains separate under OL09-D.
- [x] Credential/secret disposition remains separate under OL08-C.
- [x] Generated/binary artifacts remain separate under OL08-E.
- [x] Core-owned identity/session/token state remains outside FAIR CRM ownership.
- [x] Backups remain OL-10.
- [x] Email-account cleanup cannot be blocked for 12 months merely by the current evidence FK design; evidence/product ownership must be decoupled safely.
- [x] Artifact-bearing relational rows cannot bypass OL08-E.
- [x] Explicit dependency-aware deletion is required; cascade convenience is not policy.
- [x] Destructive evidence is minimal/non-secret and does not copy customer payloads.
- [x] Destructive runtime remains separately gated.

## Decision summary

**OL08-D is accepted. After the authoritative organization has remained in the same `SUSPENDED` episode through the valid OL09-A 30-day reversible grace, currently verified tenant-owned FAIR CRM relational product data is designated for HARD_DELETE with no additional generic product-data retention interval. No current product-data class is accepted for anonymized long-lived retention. Global/system catalogs remain, closure/security evidence follows OL09-D, credentials follow OL08-C, generated/binary artifacts follow OL08-E, Core identity remains outside FAIR CRM ownership and backups remain OL-10. Hard deletion is dependency-aware, export-gated, credential/artifact-gated, tenant-scoped, idempotent and fail-closed. This decision accepts the matrix but does not yet authorize the production destructive worker.**
