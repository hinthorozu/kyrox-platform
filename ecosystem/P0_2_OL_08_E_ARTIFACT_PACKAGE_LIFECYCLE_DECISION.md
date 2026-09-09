# P0.2 OL-08E — Generated Artifact / Closure Package Lifecycle Decision

**Status:** ACCEPTED — ARTIFACT ACTION/LIFECYCLE CONTRACT ACCEPTED; RUNTIME STILL GATED  
**Accepted:** 2026-09-09  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Related export contract:** `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`  
**Related product-data matrix:** `ecosystem/P0_2_OL_08_D_PRODUCT_DATA_DISPOSITION_DECISION.md`  
**Related timing policy:** `ecosystem/P0_2_OL_09_E_ARTIFACT_EXPIRY_DECISION.md`

## Purpose

Define ownership, package inclusion, destructive disposition and failure semantics for FAIR CRM generated/binary artifacts during organization closure.

OL08-E answers **what happens to product artifacts and how a required closure package behaves**. OL09-E remains authoritative for timing: ordinary product artifacts receive no generic post-grace extension, while a persistent closure package has a 30-day availability window from durable readiness.

This decision does not authorize Core tombstone or backup ageing.

## Verified current artifact baseline

### 1. Managed quote-template logos

Quote-template logos are stored under a tenant-rooted managed filesystem location:

```text
data/images/quote-template-logos/<organization_id>/<filename>
```

The current helper validates managed URLs against the authoritative organization and rejects cross-organization/traversal resolution. Upload writes a generated filename into the organization directory.

Non-managed/external logo URLs remain supported but are not FAIR CRM-owned bytes.

### 2. Scraper handoff artifacts

Scraper JSON/XLSX handoff files are persisted under a managed handoff directory using the run id in the filename.

The current helper validates that candidate paths remain under the configured handoff root and contain the expected run id. It also provides best-effort deletion for normal run-history cleanup.

That existing best-effort behavior is **not sufficient evidence for closure completion** because an `OSError` may leave an orphaned file while normal deletion continues.

### 3. Import upload bytes

Import batches may persist original upload bytes directly in relational storage (`stored_file_content`) together with raw preview/structured import state.

Those bytes are artifact material even though they are embedded in a database row rather than stored as an external file.

### 4. Existing customer Excel export is not persistent storage

The feature-level customer export builds a buffer and returns a streaming response. There is no separately persisted customer-export artifact to expire merely because the endpoint was used.

### 5. Current operation results are primarily relational

The currently verified operation/run/run-item model stores configuration, payload/result and status metadata relationally. No general persistent operation-artifact store has been verified in the current baseline.

Future operation handlers that introduce persistent files must register those artifact classes before closure certification.

## Accepted artifact ownership classes

OL08-E uses the following ownership/action classes.

### A. `managed_product_artifact` — FAIR CRM-owned bytes

Current examples:

- managed quote-template logo files,
- scraper handoff JSON/XLSX files,
- original import upload bytes persisted in `stored_file_content`,
- any later explicitly registered FAIR CRM tenant-owned generated/uploaded file.

Disposition: **PACKAGE-THEN-HARD-DELETE when the artifact is required in the closure package; otherwise HARD-DELETE after all accepted dependencies are satisfied.**

### B. `external_reference` — pointer only, bytes not owned by FAIR CRM

Example:

- quote-template logo URL that is not a FAIR CRM managed-logo URL.

Disposition:

- the relational pointer disappears with its OL08-D product row,
- FAIR CRM must **not** issue a remote delete merely because it stored the URL,
- no claim is made that external bytes were destroyed.

### C. `ephemeral_response` — generated for one response, not durably stored

Example:

- current customer Excel streaming export.

Disposition:

- no closure artifact purge action exists because FAIR CRM does not persist a reusable server-side artifact for that response,
- normal transport/runtime temporary-resource cleanup remains ordinary application behavior, not closure evidence.

### D. `closure_package` — closure-execution-owned sensitive artifact

A persistent closure package may be created only for a closure export whose disposition is `required`.

Current `not_required` success remains unavailable until a separately accepted policy source exists.

Disposition:

- package is retained/available according to OL09-E,
- then made unavailable and strictly purged,
- package lifecycle evidence survives only as minimal non-secret OL09-D evidence.

## Required closure package contract

OL08-B already requires an explicit structured-data completeness registry and excludes secrets. OL08-E now accepts the package-materialization layer for the `required` path.

### Canonical package contents

The package must contain:

1. **versioned manifest**
   - organization id,
   - closure execution id,
   - package/export schema version,
   - included/excluded artifact/data classes with reason codes,
   - record/artifact counts,
   - package creation/readiness timestamps,
   - integrity metadata.

2. **portable structured export**
   - the structured customer-portable classes accepted under OL08-B,
   - encoded in deterministic, documented package entries rather than as a raw database dump.

3. **registered tenant-owned portable artifacts where present**
   - managed quote-template logo bytes,
   - original import upload bytes when present,
   - scraper handoff JSON/XLSX artifacts when they are safely attributable to the closing organization/run,
   - future artifact classes only after explicit registry acceptance.

### Hard exclusions

The package must never contain:

- reusable SMTP/provider credentials,
- API tokens,
- webhook signing secrets,
- passwords or password hashes,
- secret hashes/fingerprints used as credential oracles,
- bearer/session/refresh/reset tokens,
- encryption/database credentials,
- raw provider webhook signatures/security payloads unless a later explicit portability policy says otherwise,
- Core-owned credential/session/token state,
- system database backups/restore images,
- internal environment/configuration secrets.

External URLs may remain as ordinary exported structured metadata when they are part of a portable product row, but FAIR CRM must not fetch arbitrary remote bytes at closure merely to embed them in the package.

## Package format / integrity contract

The first persistent closure package is a **single deterministic archive artifact** with a versioned internal layout.

The implementation may choose the concrete archive library, but the externally meaningful contract is:

- one canonical package identity per organization + closure execution + package schema version,
- one immutable canonical package once it reaches `ready`,
- a cryptographic digest of the final package bytes for integrity verification,
- no secret material in package or integrity evidence,
- deterministic manifest-to-package membership checks,
- package state and digest tied to the same exact package bytes.

A ZIP-compatible archive is the expected first implementation format unless an implementation review demonstrates a safer equivalent. The policy requirement is the deterministic single-package contract, not a specific compression library.

## Accepted package state model

```text
planned
  -> generating
  -> ready
  -> integrity_verified
  -> expired
  -> purged

any unsafe/unresolved condition -> blocked
```

Rules:

- `ready` means canonical package bytes have been durably written and are immutable,
- `integrity_verified` means the manifest/package membership and final package digest have been deterministically verified,
- no product-data/artifact destructive phase may use package generation as a prerequisite until the required package is `integrity_verified`,
- `expired` means retrieval authorization is removed at the exact OL09-E deadline,
- `purged` requires positive deletion/non-existence evidence from the managed package store,
- a failed delete is `blocked`/purge-pending, never successful merely because the deadline passed.

## Access / delivery authority

The initial persistent closure-package lifecycle remains **Platform SuperAdmin / SYSTEM/operator-only**, consistent with OL08-B.

This decision authorizes a bounded SYSTEM/operator package retrieval capability needed to verify/retrieve the required package, but it does **not** create customer-facing self-service handover.

Any future customer-facing delivery/download flow requires a separate authorization contract.

Package storage must not be exposed through a public static directory. Retrieval must pass authoritative closure/package ownership and authorization checks.

## Timing and expiry

OL09-E is authoritative:

```text
canonical package first becomes durably ready/available
  -> 30-day availability window starts

30 days later
  -> retrieval authorization ends
  -> package becomes purge-eligible
```

Downloads do not reset or extend the clock.

Generation retries before `ready` do not start the clock.

Rewriting identical bytes after `ready` must not silently reset the clock.

A separately accepted replacement of a corrupt/invalid canonical package must carry explicit supersession evidence before a new readiness timestamp may exist.

## Reactivation / closure cancellation

If the organization is reactivated during the reversible grace and the closure execution is cancelled/terminalized:

- any generated closure package for that cancelled execution immediately loses retrieval authorization,
- its ordinary 30-day availability window no longer justifies retention,
- the package becomes **cancellation-purge-pending** and must be strictly purged as soon as the accepted cleanup path runs,
- a cancelled package must never later unblock destructive work,
- a later new suspension/closure creates a new package identity and never reuses the cancelled package.

No product artifact is deleted as closure work during the reversible grace merely because it was copied into a cancelled package.

## Artifact inventory before relational deletion

Artifact ownership evidence must be captured **before** OL08-D removes relational rows that are needed to locate/attribute artifact bytes.

The closure execution must build a versioned artifact inventory containing at minimum:

- artifact class,
- organization identity,
- owning product/run/template/import identity,
- managed/external/embedded classification,
- package inclusion disposition,
- cleanup action,
- bounded non-secret locator metadata sufficient for the purge handler while the execution is active.

Long-lived OL09-D evidence must not retain unnecessary storage paths or business payloads. After cleanup, durable evidence should reduce to class/count/outcome/reason/timestamp/version information and stable non-secret identifiers required for proof.

The artifact inventory is not authorization to scan/delete unrelated filesystem content.

## Current artifact-class decisions

### Managed quote-template logos

**Package:** include when present and referenced by the closing organization's quote-template data.

**Purge:** after required package integrity is verified and OL09-A grace is satisfied, delete all FAIR CRM-managed logo files owned by the closing organization that are in the accepted closure artifact inventory.

The closure implementation should also safely reconcile the organization's managed logo directory for unreferenced/orphan files that are provably inside the authoritative organization-owned directory. It must not follow symlinks or escape the configured logo root.

Non-managed external logo URLs are not remote-deleted.

### Scraper handoff JSON/XLSX

**Package:** include safely attributable handoff files when present in the artifact inventory.

**Purge:** enumerate artifact ownership from organization-owned scraper runs before deleting run history, validate every candidate through the accepted managed handoff-root/run-id rule, and then strictly delete it.

The existing normal-path `delete_handoff_artifacts_for_run()` helper may inform the implementation but its best-effort error swallowing cannot be used to certify closure purge success. Closure requires a strict variant/result contract that reports deletion failure and verifies non-existence.

Because the scraper handoff directory is not organized by tenant directory, closure must **not** recursively delete or glob arbitrary files merely from a path prefix. Ownership comes from the closure inventory + verified run identity.

### Import `stored_file_content`

**Package:** include the original upload bytes when present, tied to the import batch identity and package manifest.

**Purge:** once package integrity/export dependencies and OL09-A grace are satisfied, embedded bytes are destroyed with the accepted import-batch OL08-D hard-delete action or by an equivalent explicit byte-clear step immediately before row deletion.

A relational row disappearing is acceptable physical-byte evidence only because the bytes live in that exact database row; the cleanup engine must still record the class action/count without copying bytes into audit evidence.

### Existing streamed feature exports

Current customer Excel streaming exports are not persistent server-side closure artifacts and require no retained artifact cleanup entry.

### Future operation/generated artifacts

No generic persistent operation-file store is accepted merely because operation payload/result rows exist.

Any future handler that writes files/object-store blobs must register:

- storage root/provider,
- tenant ownership resolution,
- safe locator validation,
- package inclusion rule,
- strict purge capability,
- residual/non-existence verification,

before OL08 closure can certify that artifact class.

Unknown persistent artifact classes fail closed; they are not silently ignored.

## Strict purge semantics

Closure artifact deletion is not best-effort.

For every managed artifact class:

- delete must be tenant/owner scoped,
- missing-at-delete may count as already-purged only when ownership and expected locator were deterministically established,
- permission/I/O/provider errors become durable blocked evidence,
- retries are idempotent,
- successful completion requires post-delete non-existence verification appropriate to the store,
- one artifact-class failure prevents that class and downstream cleanup from being marked complete,
- no broad recursive delete may cross an authoritative tenant root,
- symlink/path-traversal escape must fail closed,
- deleting a relational locator is not evidence that external bytes are gone.

Object-store implementations, if added later, must provide equivalent exact-key/tenant-prefix ownership and deletion verification semantics.

## Package-before-delete gate

When export disposition is `required` — the only currently executable successful disposition — irreversible OL08-D/E source cleanup is blocked until:

- the package was generated for the same organization + closure execution,
- required structured registry classes are represented,
- required registered artifacts are included or explicitly excluded by an accepted stable reason,
- secret-exclusion checks pass,
- package byte digest verifies,
- manifest/package membership verifies,
- package reaches `integrity_verified`.

A manifest plan alone remains insufficient.

`not_required` continues to fail closed until a separate accepted policy source exists.

## Package expiry versus source cleanup

The 30-day package availability window does **not** force original source artifacts to remain for an extra 30 days.

After the valid 30-day closure grace and package integrity verification, source product data/artifacts may proceed through OL08-D/E cleanup even while the closure package remains available for its independent 30-day package window.

Conversely, package expiry does not prove source cleanup happened.

These are separately evidenced obligations.

## Cleanup evidence

Minimal non-secret evidence may record:

- organization + closure execution id,
- artifact/package policy version,
- class key,
- package id/schema version,
- state transitions,
- artifact counts,
- package byte size,
- package digest,
- generated/ready/integrity-verified/expired/purged timestamps,
- purge outcome and bounded reason code.

It must not retain:

- original artifact bytes,
- customer/upload contents,
- message content,
- arbitrary scraper payloads,
- credentials/secrets,
- raw authorization material.

Long-lived evidence follows OL09-D.

## Failure / restart semantics

Generation and purge must be idempotent and restart-safe.

- generation interrupted before canonical `ready` may resume/restart without fabricating readiness,
- if canonical package bytes may have been written but final commit/result is ambiguous, reconciliation must verify exact store state and digest before proceeding,
- package identity/version prevents duplicate successful canonical packages for one closure execution,
- purge ambiguity is reconciled by non-existence verification rather than blindly recording success,
- a partial artifact-class purge resumes from durable class inventory/evidence,
- retry re-checks closure validity and dependencies before new destructive action,
- expired/cancelled packages are never silently regenerated because a retrieval request arrives.

## Interaction with OL08-D

OL08-D relational cleanup and OL08-E artifact cleanup form one coordinated destructive phase but retain separate action evidence.

Relational cleanup must not destroy artifact ownership/locator information before OL08-E has built its inventory and completed any required package copy.

Artifact cleanup must not use file deletion as evidence that relational product rows are gone.

Both must succeed before the corresponding product-data/artifact cleanup phase can be considered complete.

## Explicitly not authorized by this decision

This acceptance does not yet authorize:

- production package generation/download endpoints without the bounded implementation slice and tests,
- customer-facing package delivery,
- `not_required` export success,
- arbitrary external-URL deletion,
- broad filesystem deletion outside proven tenant/run ownership,
- treating best-effort artifact cleanup as closure success,
- provider credential revoke/purge — OL08-C,
- database backup deletion/restore reconciliation — OL-10,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

The first runtime slice must remain bounded to package/inventory/artifact-disposition machinery and cannot advance final tombstone while unresolved credential or backup obligations remain.

## Acceptance checklist

- [x] Current persistent artifact classes are explicitly separated from relational data.
- [x] Managed quote logos are FAIR CRM-owned; external logo URLs are pointer-only and not remote-deleted.
- [x] Scraper handoff files use run-scoped safe ownership and require strict closure deletion rather than existing best-effort cleanup.
- [x] Import `stored_file_content` is treated as embedded artifact bytes.
- [x] Current customer Excel streaming export is not treated as persistent artifact storage.
- [x] Unknown/future persistent artifact classes fail closed until registered.
- [x] Required closure export may now materialize one canonical persistent package.
- [x] Package includes manifest + structured export + registered portable tenant artifacts.
- [x] Secrets/Core credentials/backups are hard-excluded.
- [x] Package must reach `integrity_verified` before required-export cleanup gate can open.
- [x] Initial package access remains SYSTEM/operator-only.
- [x] Package timing follows OL09-E: 30 days from durable readiness; download does not reset it.
- [x] Reactivation/cancellation immediately revokes package availability and makes it purge-pending.
- [x] Artifact inventory precedes relational locator deletion.
- [x] Managed artifact purge is strict, tenant-scoped, idempotent and non-existence verified.
- [x] Package lifetime does not extend original source artifact retention.
- [x] Long-lived evidence remains minimal/non-secret under OL09-D.
- [x] Runtime and tombstone remain separately gated.

## Decision summary

**OL08-E is accepted. FAIR CRM-managed tenant artifacts are explicitly inventoried, included in a required closure package when portable, and strictly hard-deleted after the valid OL09-A grace, required package integrity and class-specific dependencies. Managed quote logos, scraper handoff files and embedded import upload bytes are the verified current persistent artifact classes; external URLs are not FAIR CRM-owned bytes and current customer Excel streaming exports are not persistent artifacts. The required export path may materialize one canonical integrity-verified closure package under SYSTEM/operator authority; its 30-day lifecycle follows OL09-E, and cancellation/reactivation revokes it immediately and triggers strict purge. Best-effort deletion cannot certify closure success. This accepts the action/lifecycle contract but does not yet authorize final cleanup/tombstone or OL-10 backup behavior.**
