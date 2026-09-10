# P0.2 OL-08D — Product-Data Hard-Delete Runtime Acceptance

**Status:** RUNTIME ACCEPTED / CERTIFIED  
**Accepted:** 2026-09-10  
**Canonical policy:** `ecosystem/P0_2_OL_08_D_PRODUCT_DATA_DISPOSITION_DECISION.md`  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Export/package dependency:** `ecosystem/P0_2_OL_08_E1_RUNTIME_ACCEPTANCE.md`  
**Artifact dependency:** `ecosystem/P0_2_OL_08_E2_RUNTIME_ACCEPTANCE.md`  
**Credential dependency:** `ecosystem/P0_2_OL_08_C2_RUNTIME_ACCEPTANCE.md`

## Purpose

Record runtime acceptance for the OL08-D dependency-aware relational product-data hard-delete implementation in FAIR CRM.

This acceptance certifies the current-model product-data deletion engine only after the accepted lifecycle, export/package, credential and artifact gates are actually satisfied. It does **not** accept terminal closure readiness, OL08-F retained-evidence purge or Core organization tombstone.

## Accepted FAIR CRM runtime

FAIR CRM PR #269 implements:

- migration `0082_closure_product_cleanup`,
- a versioned explicit 19-class product-cleanup dependency plan,
- durable per-class cleanup evidence with bounded counts, status, attempts, timestamps and failure codes,
- SYSTEM-only reconcile/status API surfaces,
- one destructive class per reconcile call/transaction so progress is restart-safe and later irreversible work re-evaluates current authority,
- live Core lifecycle verification before every destructive mutation,
- exact current `SUSPENDED` episode continuity and the accepted 30-day OL09-A grace,
- canonical OL08-E package/integrity and artifact-cleanup prerequisites,
- OL08-C credential-completion prerequisite before product-data mutation,
- explicit child/parent delete ordering instead of treating database cascade behavior as the policy,
- organization-scoped deletion and cross-organization isolation,
- explicit current-email-account credential-evidence gating,
- detachment of credential-disposition evidence from the live `email_accounts` foreign key while retaining the minimum non-secret scalar account UUID,
- import `stored_file_content` destruction through the authorized import relational hard-delete path and reconciliation of the corresponding E2 artifact inventory to positive non-existence evidence,
- fail-closed handling for unknown persistent `system_data_operation` output-file references,
- bounded non-secret control evidence only; deleted business payloads and reusable secrets are not copied into cleanup evidence.

## Export/package identity gate

The runtime does not treat the existence of a package row as sufficient destructive authorization.

Before the **first irreversible product-data delete**, it revalidates the current tenant-scoped identities against the accepted OL08-03A export plan that is bound to the canonical package:

- package `export_plan_id` must match the accepted current export plan,
- every accepted data-class classification/source must still match the registry,
- current scoped record counts must match the plan,
- current record-ID-only identity digests must match the plan,
- any post-package identity drift blocks destructive cleanup before the first delete.

This preserves the accepted package-before-delete boundary: deletion cannot silently destroy product rows that were not represented by the accepted export/package identity set.

## Lifecycle / timing contract

The runtime preserves the accepted OL09-A timing semantics:

```text
current authoritative Core suspension episode updated_at
  + 30 days
  -> product-data classes may become time-eligible
     only while the same current suspension episode is still SUSPENDED
     and every class/phase dependency is satisfied
```

There is no extra generic retention interval after that grace.

If Core authority is unavailable, the organization is no longer `SUSPENDED`, or a different suspension episode is observed after cleanup began, the next irreversible class is blocked. A previously completed class is not reinterpreted as permission to continue under a new episode.

## Dependency-aware deletion contract

The accepted runtime uses a deterministic 19-class sequence covering the current verified product model, including communication history, operations, scraper state, system-data-operation state, duplicate-merge history, imports/data integration, quotes, todo/workflow state, activities, participations, contacts, customer communications, customers, fairs, quote templates, template contents, cost catalog, mail templates and email accounts.

Each reconcile attempt processes at most the next incomplete class. Completed classes remain durable evidence; blocked classes remain explicit and retryable. Unexpected residual organization-owned rows, referential-integrity failures or database failures do not trigger force-delete fallbacks.

Global/shared system data, closure/security evidence, backup/restore state and Core identity/session/token state remain outside OL08-D product deletion.

## Credential/evidence boundary

Email-account product rows are not deleted merely because they are product data.

The runtime requires matching terminal OL08-C credential-disposition evidence before the email-account class can complete. The evidence relationship is then detached from the live product-row foreign key while preserving the non-secret scalar account UUID required for retained control evidence.

This means:

- provider invalidation/local-secret obligations cannot be fabricated by deleting the product row,
- reusable secrets are not copied into retained evidence,
- the full email-account product row is not retained for the OL09-D evidence period solely to satisfy an audit FK.

## Import embedded-byte boundary

OL08-E2 deliberately leaves an import upload inventory item as `relational_delete_required` while `crm_import_batches.stored_file_content` still exists.

OL08-D now closes that dependency through the authorized relational deletion path:

```text
package contains accepted import upload bytes
  -> E2 marks relational_delete_required while source bytes remain
  -> OL08-D deletes the owning import relational data at the authorized class
  -> embedded bytes disappear with that relational deletion
  -> artifact inventory is reconciled to already_absent with positive non-existence evidence
```

The runtime does not claim artifact success merely because a pointer or metadata row disappeared.

## Fail-closed / retry contract

Accepted behavior includes:

- no cleanup plan is seeded before lifecycle/grace/package/artifact/credential prerequisites pass,
- no first irreversible delete occurs if current export identity differs from the accepted package-bound plan,
- every later reconcile rechecks current lifecycle authority and same suspension episode,
- at most one class is destructively processed per reconcile transaction,
- current organization scope is enforced for root and child deletion,
- unknown persistent system-operation output artifacts block the affected class,
- referential-integrity/database errors become bounded blocked evidence rather than force-delete workarounds,
- completed classes are idempotently skipped while later classes remain independently gated,
- product cleanup completion means only that the explicit current OL08-D class plan is complete; it does not mean terminal closure is complete.

## Exact runtime evidence

FAIR CRM PR #269:

- final head: `aec1b5d44206fa38b19f4289d3975da94c20a833`,
- Development Standard Gate #760 / run `34418454313`: **SUCCESS**,
- Prod-Path E2E #305 / run `34418454097`: **SUCCESS**,
- FAIR CRM squash merge: `210313886e2d9d6c0443367e22b9728baa041329`,
- FAIR CRM `main` was verified at that exact merge commit after merge.

The final test foundation uses the real OL08-03A export planner and real OL08-E1 package builder rather than a synthetic empty manifest. A dedicated regression also proves that product identity added after package creation blocks the first irreversible delete.

## Explicitly not accepted by OL08-D

OL08-D does not authorize or certify:

- generic `cleanup_complete` across the entire offboarding workflow,
- `ready_for_tombstone`,
- final Core organization deletion/tombstone,
- OL08-F purge/de-identification of the retained 12-month closure/audit/security evidence,
- early purge of retained evidence before its accepted 12-month clock,
- `not_required` export success,
- bypass of a still-blocked credential, artifact, package or lifecycle dependency,
- deletion of shared/global catalogs, backup images or Core-owned identity state.

## Result

The current-model FAIR CRM relational product-data deletion boundary is runtime-covered under its accepted prerequisites.

After OL08-D acceptance, the next remaining explicit OL08 runtime gap is **OL08-F retained minimal closure/audit/security evidence purge/de-identification after the accepted 12-month terminal-closure retention clock**. Terminal cleanup/tombstone readiness remains prohibited until every remaining closure obligation is implemented, satisfied and certified.
