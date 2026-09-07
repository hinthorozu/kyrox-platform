# P0.2 OL-08B — Closure Export Contract Decision

**Status:** PARTIALLY ACCEPTED 2026-09-07 — technical export contract accepted; package materialization/delivery and `not_required` policy source remain gated  
**Date:** 2026-09-07  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Decision summary

OL08-B accepts the **technical closure-export contract** without inventing a universal legal/business export obligation.

Accepted architecture:

- closure export is owned by one FAIR CRM closure execution and one organization,
- export disposition is modeled as `required` / `not_required`, with missing/unknown disposition failing closed,
- `not_required` is **not currently executable** because no accepted policy source exists yet,
- the first implementation must enumerate customer-portable structured data classes explicitly,
- generated/binary artifacts are deferred to OL08-E,
- reusable secrets/credentials are always excluded,
- Core identity remains outside FAIR CRM export ownership,
- initial export control remains Platform SuperAdmin / SYSTEM/operator only,
- no export phase may unblock irreversible cleanup or Core tombstone until the complete package, artifact-lifecycle and policy requirements are separately accepted and certified.

This acceptance authorizes only the narrow non-destructive implementation slice described below. It does **not** authorize a closure-complete downloadable package, provider revoke/secret purge, product-data/artifact deletion/anonymization, retention durations, backup reconciliation or Core tombstone.

## Verified baseline

The current product already has tenant-safe feature-level export/download primitives, but not an organization-wide closure export:

- customer Excel export is organization-scoped and exports the filtered Customers view plus selected communication/fair information,
- scraper artifacts are protected by authoritative organization/run ownership,
- managed quote-template logos are served through organization-scoped authenticated routing,
- quote rendering is organization-scoped and depends on owned customer/fair/template/content data,
- P0.1 TI-07 certified these export/download/artifact ownership boundaries,
- none of these paths provides one closure snapshot, a completeness manifest, an integrity proof, or a durable closure-execution export decision.

Existing UI/API exports therefore remain feature exports and must not be composed informally and called a closure-complete package.

## Accepted OL08-B architecture

### 1. Policy-conditioned disposition is the accepted model

The accepted contract shape is:

```text
required
not_required
```

A missing/unknown disposition fails closed.

`not_required` requires durable non-secret policy evidence from a separately accepted policy source. An arbitrary normal-user flag or ad-hoc operator toggle is not authority.

**Current runtime rule:** because no accepted `not_required` policy source exists yet, implementation must not expose or persist a successful `not_required` disposition. That path remains gated.

### 2. Export belongs to the closure execution

A closure export plan belongs to exactly one:

- organization,
- closure execution,
- stable export identity / schema version.

Evidence from one organization/execution cannot satisfy another.

### 3. Required export remains a prerequisite, but no completion gate is authorized yet

The future full required-export state model is expected to converge on:

```text
pending
  -> generating
  -> ready
  -> integrity_verified
```

However the currently authorized implementation slice must **not** expose `integrity_verified`, `export_complete`, `cleanup_complete` or `ready_for_tombstone` as a gate-opening state.

Until package materialization/delivery and artifact lifetime are separately accepted, export evidence may be prepared and validated but cannot authorize later irreversible phases.

### 4. Versioned manifest contract is accepted

The manifest schema must identify at minimum:

- export schema/version,
- organization id,
- closure execution id,
- export id,
- planning/generation timestamp where applicable,
- included portable data classes,
- excluded/deferred data classes with durable reason codes,
- record counts for structured classes,
- canonical content fingerprints/digests where produced,
- completion/planning state,
- secret-exclusion classification.

The manifest is authoritative evidence of what the exporter considers in scope; silent omission is forbidden.

### 5. First-version portable structured data classes

The accepted v1 structured-data completeness registry must classify the following FAIR CRM product data as customer-portable where present:

- customers and customer communications,
- contacts,
- fairs and participations,
- activities, todos and follow-up/task records,
- quotes plus portable quote-template/template-content source data,
- cost-catalog product data,
- import/data-integration metadata and structured results needed to explain/reproduce customer data,
- scraper/enrichment run metadata and normalized customer-owned structured result data,
- operation/automation definitions, run metadata and customer-portable structured results,
- mail templates plus normalized customer communication/mail-send history and status records.

The first implementation must classify every registry entry as included, excluded or deferred with a stable reason; it must not silently ignore a category.

### 6. Explicit first-version exclusions/deferred classes

The following are not part of the initial portable structured package contract:

- generated/binary files, uploads and artifacts — **deferred to OL08-E**,
- raw scraper/operation artifact files — **deferred to OL08-E**,
- managed quote/logo binary assets — **deferred to OL08-E**,
- reusable provider/SMTP credentials or encrypted secret payloads — **always excluded**,
- provider-side credential lifecycle/revocation evidence — **OL08-C**,
- raw provider webhook payloads/signatures and internal provider diagnostics — excluded unless a later accepted portability rule says otherwise,
- Core identity/password/session/token data — outside FAIR CRM ownership,
- system-admin database backups/restores — OL-10 / operations scope,
- derived dashboard views that can be reproduced from underlying exported data,
- internal closure orchestration event payloads beyond non-secret manifest/audit references.

Non-secret provider account descriptors may be classified later under OL08-C; they are not required for the first OL08-B completeness baseline.

### 7. Secrets and security credentials are excluded

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

Secret exclusion is a hard certification property, not a best-effort filter.

### 8. Core identity remains a separate ownership boundary

FAIR CRM closure export must not directly read Core databases or duplicate Core credential authority.

If future commercial policy requires identity/account metadata in a customer handover, that requires an explicit public Core export contract or separately accepted cross-repository contract.

### 9. Initial control/delivery authority is SYSTEM/operator-only

The first implementation remains under Platform SuperAdmin / SYSTEM authority and is bound to the existing OL08 closure execution.

No customer-facing self-service handover/download flow is authorized by this decision. A future customer-facing flow requires its own authorization/delivery contract.

### 10. Tenant isolation and audit remain mandatory

Planning, generation, status, retry and future download/materialization operations must remain bound to the target organization and closure execution.

Audit/closure evidence may record export id, execution id, organization id, state transition, schema version, digest/reference metadata and actor/timestamp, but must not copy business payloads or secrets into audit events.

## Resolved acceptance questions

1. **Disposition model:** Option C / policy-conditioned `required` / `not_required` is accepted.
2. **v1 portable classes:** the structured FAIR CRM business-data categories enumerated above are mandatory completeness-registry entries.
3. **Generated files/artifacts:** deferred to OL08-E; they must be explicitly marked deferred/excluded in the manifest rather than silently omitted.
4. **Delivery authority:** SYSTEM/operator-only initially; no customer-facing handover flow in this slice.
5. **`not_required` authority:** no accepted source exists yet. Therefore runtime must not allow `not_required` to satisfy export obligation. A later accepted policy must provide durable policy code/version/reason evidence before that path can exist.

## Authorized implementation boundary

Before any package-producing export runtime, complete **OL08-02 closure-quiescence certification** against the already-certified OL-07 lifecycle behavior.

After OL08-02 is green, OL08-B authorizes only the first non-destructive OL08-03 slice:

### OL08-03A — Export manifest / completeness planner

Authorized:

- durable export-plan identity tied to one closure execution and organization,
- versioned manifest schema,
- explicit structured-data completeness registry,
- organization-scoped record counting / planning,
- deterministic canonical fingerprints/digests where safe without retaining package payload,
- explicit included/excluded/deferred reason evidence,
- hard secret-exclusion validation,
- SYSTEM-only plan/status/retry semantics,
- idempotency and tenant-isolation tests,
- append-only non-secret audit/closure evidence.

Not authorized in OL08-03A:

- persistent/downloadable closure package materialization,
- package retention/expiry policy,
- `not_required` success state,
- `integrity_verified` as an irreversible-phase gate,
- customer-facing download/handover,
- provider credential revoke/purge,
- organization-wide data/artifact deletion/anonymization,
- `cleanup_complete` / `ready_for_tombstone`,
- Core tombstone.

## Why package materialization remains gated

A persistent/downloadable closure package creates a new sensitive artifact with storage, access, expiry and deletion obligations. OL08-E and applicable OL-09 policy have not yet defined that artifact lifecycle.

Therefore this decision accepts the export contract and completeness planner first, while keeping package materialization/delivery outside the authorized slice until artifact-lifecycle policy is explicit.

## Remaining gates

- **OL08-02:** certify closure quiescence against real OL-07 runtime before export planning is trusted.
- **OL08-03A:** implement/certify manifest + completeness planner after OL08-B acceptance.
- **OL08-C:** provider credential disposition remains OPEN.
- **OL08-D:** product-data disposition remains OPEN / depends on OL-09.
- **OL08-E:** generated artifact disposition remains OPEN and is required before persistent closure-package lifecycle is accepted.
- **OL08-F:** audit/security retention remains OPEN.
- **OL08-G / OL-10:** backup/restore reconciliation remains OPEN.
- **OL-09:** retention/grace durations remain OPEN CHOICE.

## Hard prohibition

OL08-B acceptance does not make the closure execution cleanup-complete or tombstone-ready. No later irreversible phase may treat an export plan/manifest as equivalent to a delivered, retained or integrity-verified closure package.
