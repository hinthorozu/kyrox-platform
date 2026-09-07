# P0.2 OL-08B — Closure Export Decision Proposal

**Status:** PROPOSED — NOT ACCEPTED / NO RUNTIME AUTHORIZED  
**Date:** 2026-09-07  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Decision source if accepted:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Purpose

Define the decision boundary for a complete FAIR CRM organization-closure export without treating existing feature exports as a closure-complete package and without authorizing destructive cleanup.

This proposal does **not** authorize OL08-03 runtime, does not choose a retention/expiry duration, does not define provider credential disposition, does not delete/anonymize any product data or artifacts, and does not permit the Core organization tombstone.

## Verified baseline

The current product already has tenant-safe feature-level export/download primitives, but not an organization-wide closure export:

- customer Excel export is organization-scoped and exports the filtered Customers view plus selected communication/fair information,
- scraper artifacts are protected by authoritative organization/run ownership,
- managed quote-template logos are served through organization-scoped authenticated routing,
- quote rendering is organization-scoped and depends on owned customer/fair/template/content data,
- P0.1 TI-07 certified these export/download/artifact ownership boundaries,
- none of these paths provides one closure snapshot, a completeness manifest, an integrity proof, or a decision that an export is required before irreversible cleanup.

Therefore existing UI/API exports must not be composed informally and called a closure export.

## Decision options

### Option A — Always generate a closure export

Every closure execution must produce and verify a complete export package before later irreversible phases may proceed.

Advantages:
- simplest sequencing invariant,
- strongest operator recovery/data-handover posture,
- no per-closure ambiguity about whether export was required.

Costs/risks:
- creates a new sensitive copy for every closure even when nobody needs it,
- introduces storage/delivery/expiry obligations,
- expiry duration still depends on OL-09 / artifact policy,
- large organizations may make closure slower and more operationally expensive.

### Option B — Explicitly requested export only

Closure export is generated only when requested by an authorized operator/customer workflow.

Advantages:
- avoids unnecessary sensitive copies,
- lower storage and processing burden.

Costs/risks:
- an operator-only toggle cannot safely stand in for future legal/policy requirements,
- later destructive phases need durable evidence explaining why export was not required.

### Option C — Policy-conditioned export

Each closure execution carries an authoritative export disposition:

- `required`, or
- `not_required` with durable policy/reason evidence.

If `required`, later irreversible phases cannot advance until the package is complete and integrity-verified. If `not_required`, the execution records the decision without fabricating an export.

This is the **recommended contract shape** because it does not hard-code an unverified universal legal/business rule and still makes sequencing deterministic. It requires the source of the disposition to be an accepted policy/authorized SYSTEM workflow; an arbitrary normal-user flag is not authority.

## Proposed OL08-B contract

If accepted, OL08-B should establish the following invariants.

### 1. Export is a closure-execution phase, not a normal feature export

The export belongs to one durable OL08 closure execution and one organization. It has a stable export id and cannot be reused as evidence for another organization/execution.

### 2. Export disposition is explicit

Each closure execution that reaches the export phase must record one of:

```text
required
not_required
```

`not_required` must retain non-secret policy/reason evidence. A missing/unknown disposition fails closed and cannot be interpreted as export complete.

### 3. Required export is a prerequisite for later irreversible phases

When disposition is `required`:

```text
pending
  -> generating
  -> ready
  -> integrity_verified
```

A required export that is failed/incomplete/unverified blocks advancement to later destructive cleanup or Core tombstone readiness.

Retries must converge on the same logical export for the same closure execution or create a clearly versioned replacement while invalidating the superseded candidate as completion evidence.

### 4. Package is organization-scoped and versioned

Recommended package form:

```text
closure-export-<organization>-<execution>.zip
  manifest.json
  data/*.jsonl or *.csv
  artifacts/...              only accepted portable customer-owned artifacts
```

The exact serialization may evolve by schema version, but the manifest must identify:

- export schema/version,
- organization id,
- closure execution id,
- export id,
- generation timestamp,
- included data classes,
- excluded/non-portable data classes with reason,
- per-file record count where applicable,
- per-file byte size,
- per-file cryptographic digest,
- package-level digest or equivalent integrity evidence,
- completion state.

### 5. Export must be complete against an explicit data-class contract

The first implementation must enumerate product-owned classes rather than run an unreviewed database dump. At minimum the completeness contract must classify:

- customers and customer communications,
- contacts,
- fairs and participations,
- activities/todos/follow-ups,
- quotes and portable quote/template/content data,
- cost-catalog product data,
- import metadata/results that are customer-portable,
- scraper/enrichment result data that is customer-portable,
- operation/automation definitions and customer-portable result data,
- mail history/customer communication records that are customer-portable,
- customer-owned uploads/generated artifacts when OL08-E says they are part of export.

The manifest must also explicitly classify excluded categories rather than silently omit them.

### 6. Secrets and security credentials are excluded

Closure export must never contain reusable authentication/provider secrets, including:

- password hashes,
- session/refresh/access tokens,
- activation/reset tokens,
- SMTP passwords,
- provider API keys/tokens,
- encryption keys,
- webhook signing secrets,
- raw bearer credentials,
- internal database connection secrets.

Historical non-secret identifiers may be exported only when part of the accepted portable-data contract.

### 7. Core identity remains a separate ownership boundary

FAIR CRM closure export must not directly read Core databases or duplicate Core credential authority. If future commercial policy requires identity/account metadata in a customer export, that requires an explicit public Core export contract or a separately accepted cross-repository contract.

OL08-B must not authorize direct cross-database reads.

### 8. Tenant isolation remains mandatory

Generation, status, download and retry must all be bound to the target organization and closure execution. Foreign organization ids/artifact ids cannot be used to read or replace another organization's closure package.

Platform SuperAdmin/SYSTEM execution authority remains the OL-05/OL08-A exception; it does not weaken repository-level organization predicates.

### 9. Audit evidence must not store payloads/secrets

Audit/closure events should record export id, execution id, organization id, state transition, schema version, digest/reference metadata and actor/timestamp. They must not copy the exported business payload or credentials into audit records.

### 10. Artifact lifetime is intentionally not chosen here

OL08-B may define ownership and integrity of the closure export artifact, but it must **not invent an expiry duration**. Artifact retention/expiry must be aligned with OL08-E and applicable OL-09 policy before production cleanup can rely on it.

Until that policy is accepted, OL08-03 implementation may generate/verify export evidence only if its storage lifecycle is explicitly non-destructive and cannot be mistaken for a final retention decision.

## Proposed implementation slice after acceptance

If OL08-B is accepted, authorize **OL08-03 — closure export contract/runtime** as a non-destructive phase attached to the existing OL08-01 execution.

Suggested independently reviewable work:

1. durable closure-export record/state + manifest schema,
2. SYSTEM-only export start/status/download bound to closure execution,
3. organization-scoped data-class exporters,
4. deterministic manifest/count/digest generation,
5. failure/retry/idempotency behavior,
6. tenant-isolation and secret-exclusion adversarial tests,
7. integration into closure execution phase evidence,
8. Platform certification.

Still prohibited after OL08-B/OL08-03 alone:

- provider credential revoke/purge,
- organization-wide data anonymization/delete,
- artifact destruction,
- retention/grace duration choice,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core tombstone invocation.

## Acceptance questions

Before changing this proposal to ACCEPTED, maintainers must explicitly resolve:

1. Is the disposition model `policy-conditioned required/not_required` accepted, or must every closure always export?
2. Which first-version product data classes are customer-portable and mandatory for completeness?
3. Are generated files/artifacts included now or deferred until OL08-E?
4. Is export delivery SYSTEM/operator-only initially, or must a customer-facing handover flow be part of OL08-B?
5. What accepted policy supplies `not_required` evidence so that an operator cannot silently bypass a mandatory export obligation?

## Current recommendation

Adopt **Option C — policy-conditioned export** as the architecture, but do not implement OL08-03 until the five acceptance questions above are explicitly resolved and ADR-0006 / the OL-08 tracker record OL08-B as accepted.
