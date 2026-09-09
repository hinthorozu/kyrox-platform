# P0.2 OL-08E2 — Strict Artifact / Closure Package Purge Runtime Acceptance

**Status:** RUNTIME ACCEPTED / CERTIFIED  
**Accepted:** 2026-09-09  
**Canonical policy:** `ecosystem/P0_2_OL_08_E_ARTIFACT_PACKAGE_LIFECYCLE_DECISION.md`  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**E1 runtime acceptance:** `ecosystem/P0_2_OL_08_E1_RUNTIME_ACCEPTANCE.md`

## Purpose

Record runtime acceptance for the destructive OL08-E2 slice implemented in FAIR CRM after the OL08-E1 canonical package/inventory/integrity runtime.

This acceptance covers current-model managed source-file cleanup and canonical closure-package purge. It does **not** accept OL08-D relational product-data hard delete, final cleanup readiness or Core tombstone.

## Accepted FAIR CRM runtime

FAIR CRM PR #268 implements:

- migration `0081_closure_artifact_purge`,
- durable per-artifact cleanup status, retry/failure evidence and post-delete non-existence timestamp,
- durable canonical package `purged_at`,
- SYSTEM-only source-artifact purge and package-purge surfaces,
- live Core lifecycle checks before destructive source cleanup,
- exact OL09-A 30-day source-cleanup grace from the authoritative current Core suspension episode `updated_at`,
- canonical package integrity evidence as a prerequisite to source cleanup,
- re-verification of canonical package bytes while those bytes remain available,
- continued use of already-certified integrity + strict package-purge evidence after the canonical package has itself been purged,
- strict tenant-owned managed quote-template logo deletion,
- strict run-owned scraper JSON/XLSX handoff deletion,
- content-digest fail-closed protection where E1 captured source artifact bytes,
- path traversal and symlink fail-closed behavior; destructive closure paths never follow managed-logo or scraper-handoff symlinks,
- post-delete non-existence verification before file cleanup can be considered successful,
- idempotent retry/reconciliation of already-purged or already-absent managed artifacts,
- external-reference logo URLs as `not_applicable`; no remote fetch or delete,
- import `stored_file_content` explicitly left as `relational_delete_required` while bytes remain,
- import inventory reconciliation to `already_absent` only after the underlying row/bytes are no longer present,
- canonical package retention independent of source cleanup,
- strict canonical package purge at the accepted `ready_at + 30 days` deadline,
- immediate package purge eligibility after live Core reactivation/cancellation semantics,
- exact package digest/manifest verification before package deletion,
- durable blocked state rather than fabricated success for ownership, integrity, I/O or non-existence-verification failures.

## Boundary with OL08-D

E2 intentionally does not erase `ImportBatchModel.stored_file_content` while the owning relational row still contains those bytes.

The accepted OL08-E policy permits those embedded bytes to disappear with the OL08-D import-batch hard-delete action or through an explicit byte-clear immediately before that row deletion. Therefore:

```text
E2 sees stored_file_content still present
  -> relational_delete_required
  -> not artifact-cleanup success for that embedded byte class

OL08-D later destroys the owning row/bytes
  -> E2 inventory can reconcile already_absent
```

This is a dependency boundary, not an E2 implementation gap. OL08-D remains the next executable closure runtime.

## Package versus source timing

The runtime preserves the accepted independent clocks:

```text
Core current SUSPENDED episode updated_at + 30 days
  -> managed source-file cleanup may become eligible
     only if package-integrity prerequisites are satisfied

canonical package ready_at + 30 days
  -> package retrieval authorization ends
  -> canonical package may be strictly purged
```

Package downloads do not extend either clock. Package purge does not prove source cleanup, and source cleanup does not prove package purge.

## Fail-closed / retry contract

Accepted behavior:

- source cleanup before the exact Core 30-day grace is rejected without deleting bytes,
- non-SUSPENDED/deleted or unavailable lifecycle authority cannot authorize source deletion,
- a changed digest-protected source artifact is blocked rather than deleting replacement bytes,
- unsafe/traversing/symlink locators are blocked,
- scraper cleanup never broad-globs or recursively deletes the shared handoff directory,
- external pointers are never treated as FAIR CRM-owned remote bytes,
- file delete success requires post-delete non-existence verification,
- package delete success requires post-delete non-existence verification,
- a package integrity mismatch blocks package purge and preserves bytes,
- retries are idempotent and resume from durable evidence,
- an already strictly purged package can continue to satisfy the historical package-before-delete prerequisite only when durable integrity and purge evidence are both valid.

## Exact runtime evidence

FAIR CRM PR #268:

- final head: `3f1c26ad5f7d629eed158ed06a3db51e291cc50c`,
- Development Standard Gate #754 / run `34405415996`: **SUCCESS**,
- Prod-Path E2E #300 / run `34405415956`: **SUCCESS**,
- FAIR CRM merge: `791f11e1a19c4d316e340a2bf06413013c693505`.

An earlier Prod-Path #297 attempt on the pre-hardening head encountered a transient bootstrap SuperAdmin `/customers` authorization check while migration/startup succeeded. The same head passed a retry, no unrelated authorization patch was made, and the final symlink-hardened exact head subsequently passed Prod-Path #300 in full. The accepted evidence is the final exact-head run above.

## Explicitly not accepted by E2

E2 does not authorize or certify:

- OL08-D tenant relational product-data hard delete,
- early deletion of import embedded bytes independently of their accepted OL08-D dependency,
- generic cleanup completion,
- `ready_for_tombstone`,
- Core organization deletion/tombstone,
- early purge/de-identification of OL09-D 12-month retained minimal evidence,
- customer-facing closure-package delivery,
- `not_required` export success.

## Result

The current FAIR CRM managed-artifact / canonical closure-package runtime is covered through E1 + E2:

- inventory and package materialization,
- package integrity,
- managed-file source purge,
- external-reference non-action,
- package retention/strict purge,
- durable failure/retry evidence.

The remaining embedded import-byte obligation is deliberately coupled to OL08-D relational deletion. The next runtime implementation point is therefore **OL08-D dependency-aware product-data hard delete** under all accepted grace/export/credential/artifact gates.
