# P0.2 OL08-E1 — Runtime Acceptance

**Status:** ACCEPTED — NON-DESTRUCTIVE PACKAGE / INVENTORY / INTEGRITY SLICE  
**Date:** 2026-09-09  
**Canonical source:** GitHub `main`  
**Policy decision:** `ecosystem/P0_2_OL_08_E_ARTIFACT_PACKAGE_LIFECYCLE_DECISION.md`

## 1. Acceptance scope

This record accepts only the first executable OL08-E runtime slice:

- persistent canonical closure-package identity and state,
- portable structured export materialization from the accepted OL08-B / OL08-03A registry,
- registered current-model managed-artifact inventory,
- deterministic immutable package bytes,
- exact package membership and SHA-256 integrity verification,
- restart-safe canonical package reconciliation,
- SYSTEM-only package metadata/inventory/retrieval,
- the accepted 30-day package availability clock from durable `ready_at`.

This slice is deliberately **non-destructive**.

It does **not** accept or execute:

- deletion of source managed-artifact bytes,
- strict post-delete non-existence certification,
- expiry/purge of the canonical package itself,
- OL08-D relational product-data hard delete,
- terminal cleanup readiness,
- Core tombstone.

Those remain later runtime gates.

## 2. Canonical runtime implementation

Merged FAIR CRM PR: `hinthorozu/fair-crm#267` — `feat(closure): implement OL08-E1 canonical closure package runtime`.

- exact PR head: `36a484eb9491f2f226454269bb1a5af2d7b3037f`
- merged FAIR CRM `main`: `025db874770ec8e9c50986f94a7c7f8cec3b27bd`
- `Development Standard Gate` run `34402079984` / run #749 — **SUCCESS**
- `Prod-Path E2E` run `34402080016` / run #296 — **SUCCESS**

The Development Standard Gate passed feature-contract applicability, backend baseline enforcement, FastAPI compile/import and the full backend zero-new-regression pytest gate. Prod-Path E2E also passed the primary production path, OL07-03 lifecycle authority contract, P0.2 identity lifecycle certification and todo authorization regressions on the exact same PR head.

## 3. Durable package and artifact state

Migration `0080_closure_packages` adds two closure-owned durable state surfaces:

1. `crm_organization_closure_packages`
2. `crm_organization_closure_artifact_inventory`

The package record is organization + closure-execution scoped and versioned. It tracks canonical package identity, export-plan identity, schema versions, lifecycle state, non-public storage locator, manifest and package digests, byte size, attempts, bounded failure evidence, durable ready/integrity timestamps and package expiry.

The accepted package-state vocabulary follows the policy lifecycle:

```text
planned
  -> generating
  -> ready
  -> integrity_verified
  -> expired
  -> purged
```

with unsafe/incomplete work able to enter `blocked`.

E1 implements through `integrity_verified` and enforces retrieval expiry by time. It does not yet implement the destructive `expired -> purged` execution.

The artifact inventory records versioned artifact identity/classification, authoritative owner type/id, storage kind, package inclusion disposition, future cleanup action, private locator metadata, package member path where applicable, byte size and content digest.

## 4. Required-export materialization

Package generation is permitted only when:

- SYSTEM / Platform SuperAdmin closure authority is present,
- live Kyrox Core lifecycle authority reports `SUSPENDED`,
- the closure execution is open and `in_progress`,
- the required OL08-03A export plan exists,
- the plan remains `required` + `planned`.

The runtime does not promote the OL08-03A planning digest into package-integrity evidence.

For every currently accepted `INCLUDED` structured source, package generation re-reads current tenant-scoped record identities and compares count + record-ID digest against the durable plan. Any identity drift blocks package generation as stale rather than silently materializing a different export.

Current records are then serialized into deterministic structured package members. Existing field exclusions remain enforced, including `ImportBatch.stored_file_content`, which is handled only through the registered artifact path.

Secret-bearing source tables remain structurally excluded. Raw binary bytes encountered in an ordinary portable structured source are treated as an unregistered artifact-class failure and block generation.

## 5. Current-model artifact inventory

E1 implements the artifact classes verified by the accepted OL08-E decision against current FAIR CRM storage behavior.

### 5.1 Managed quote-template logos

For tenant-managed local quote-template logo URLs:

- authoritative organization ownership must match,
- path traversal/symlink escape is rejected,
- a referenced managed file must exist and be readable,
- referenced bytes are included in the package,
- size and SHA-256 are recorded.

Valid tenant-root logo files that exist but are not referenced by any current quote-template version are still inventoried as managed orphan artifacts. They are not added to the required portable package merely because they exist; their future cleanup action remains separately recorded for the destructive artifact-purge slice.

Non-managed/external logo URLs remain `external_reference` entries only. FAIR does not remote-fetch, remote-delete or treat them as FAIR-owned artifact bytes.

### 5.2 Import upload bytes

Current tenant-owned `ImportBatch.stored_file_content` bytes are registered as managed embedded artifacts and included in the canonical package under a deterministic import-batch member path.

The bytes are not duplicated through the ordinary structured-record serializer.

### 5.3 Scraper handoff JSON/XLSX

Scraper handoff artifacts are considered managed only through an authoritative organization-owned scraper run plus the already accepted run-id/root safe-path rule.

The runtime:

- does not glob arbitrary files globally,
- rejects out-of-root recorded paths,
- rejects symlinks and non-regular files,
- rejects wrong recorded artifact types,
- blocks when an explicitly recorded handoff file is missing,
- includes attributable existing JSON/XLSX bytes in the package with digest/size evidence.

## 6. Canonical package determinism and restart safety

Package identity is deterministic for:

```text
organization
+ closure execution
+ package schema version
```

The archive itself is generated with stable member ordering and fixed ZIP entry metadata. The canonical manifest contains the exact member registry with SHA-256 and byte size for every included member.

The archive is immutable once canonical bytes exist:

- an identical deterministic regeneration may reconcile to the existing bytes,
- different generated bytes may not overwrite the existing canonical package,
- archive membership must exactly match the manifest registry,
- every member digest/size must verify,
- the canonical manifest encoding must verify,
- the final archive SHA-256 must verify.

A crash after archive creation but before package/inventory database state commits does not require creating a second package. On retry, the deterministic identity finds the existing canonical archive, self-verifies it, compares its manifest body against the currently accepted export/artifact membership and can reconstruct the durable package/inventory state only when the identity is exact.

## 7. Readiness and availability clock

`ready_at` is the durable canonical readiness boundary for OL09-E timing.

E1 records:

```text
expires_at = ready_at + 30 days
```

A repeated successful generation does not create a new canonical package or reset the readiness/expiry clock.

A download does not mutate `ready_at` or `expires_at`.

Initial retrieval remains SYSTEM-only. Retrieval additionally requires:

- live Core `SUSPENDED`,
- an open in-progress closure execution,
- package state `integrity_verified`,
- current time before `expires_at`,
- fresh verification of canonical archive + manifest digests.

No customer self-service package delivery surface is introduced by E1.

## 8. Evidence and locator boundary

Public SYSTEM package responses do not expose the physical package `storage_locator`.

Artifact inventory responses likewise do not expose private `locator_json`.

Audit success evidence records bounded state, schema/timing and cryptographic digest metadata. It does not persist package contents or secret-bearing credential material.

The package manifest may contain portable tenant product records because that is the purpose of the required closure export; this is distinct from audit/evidence retention and from reusable credential material, which remains excluded.

## 9. Acceptance result

The OL08-E1 non-destructive runtime conditions are satisfied on canonical `main`:

- **durable canonical package identity/state:** satisfied;
- **versioned managed-artifact inventory:** satisfied for current verified artifact classes;
- **required export-plan precondition:** satisfied;
- **stale-plan/current-identity fail-closed comparison:** satisfied;
- **portable structured materialization:** satisfied for accepted current included registry;
- **reusable-secret source exclusion:** satisfied;
- **managed quote-logo ownership/inclusion boundary:** satisfied;
- **external logo reference-only behavior:** satisfied;
- **import embedded-byte inclusion:** satisfied;
- **scraper run/root attribution boundary:** satisfied;
- **deterministic immutable archive:** satisfied;
- **exact manifest/member SHA-256 verification:** satisfied;
- **restart-safe existing-canonical reconciliation:** satisfied;
- **SYSTEM-only retrieval:** satisfied;
- **30-day clock from durable readiness:** satisfied;
- **download does not reset retention:** satisfied;
- **private storage locator exclusion from response schemas:** satisfied;
- **exact-head Development Standard Gate + Prod-Path E2E:** satisfied.

Therefore **P0.2 OL08-E1 canonical closure package / inventory / integrity runtime is accepted**.

## 10. Residual OL08-E runtime

OL08-E as a whole is **not yet runtime-complete**.

The next executable OL08-E slice must implement strict destructive cleanup without weakening the accepted gates. At minimum it must preserve:

- package `integrity_verified` as a mandatory prerequisite before managed source-artifact deletion,
- authoritative tenant/owner scoping for every delete target,
- no remote deletion for external references,
- explicit treatment of orphan managed artifacts,
- idempotent delete/retry behavior,
- post-delete non-existence verification before the artifact-cleanup phase may be considered satisfied,
- package availability through the accepted 30-day window,
- package purge only after expiry,
- fail-closed behavior for unknown/unregistered persistent artifact classes or ambiguous ownership.

Only after that destructive artifact/package runtime is implemented and certified should OL08-D product-data deletion be allowed to consume the artifact/package gate as satisfied.