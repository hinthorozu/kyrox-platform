# P0.2 OL-08 — Organization Offboarding Decision Readiness

**Status:** DECISION READINESS ONLY — OL-08 remains PENDING ACCEPTANCE  
**Date:** 2026-09-07  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Purpose

This document records the verified implementation baseline and unresolved decisions for OL-08 before any destructive organization-offboarding runtime is authorized.

It does **not** accept OL-08, choose retention durations, authorize organization-wide purge/anonymization, authorize credential destruction, or define backup ageing/restoration policy.

OL-07 is already complete and provides deterministic suspension/reactivation behavior. OL-08 starts from that quiesced-work foundation and addresses what must happen before Core's final organization tombstone/soft-delete.

## Binding boundaries already established

- Core remains the canonical organization lifecycle authority.
- Suspension, closure and destructive organization lifecycle execution remain Platform SuperAdmin / SYSTEM authority under OL-05.
- FAIR CRM owns product-data, product-artifact and product-provider cleanup semantics; Core must not directly manipulate FAIR CRM tables.
- Core organization delete is a Core soft-delete/tombstone, not complete product-data deletion.
- Core tombstone must be the **final** lifecycle step after applicable product offboarding work succeeds.
- OL-07 already blocks new work, terminalizes suspension-cancelled work, stops covered running work at safe checkpoints and prevents new provider handoff while non-active.
- OL-09 owns retention/grace-duration choices and remains OPEN CHOICE.
- OL-10 owns backup ageing/restoration implications and remains OPEN CHOICE.

## Verified FAIR CRM baseline

### 1. Quiesce / settle active work — AVAILABLE

OL-07 provides the execution safety primitives needed at the start of offboarding:

- covered queued/pending work is cancelled before start when lifecycle is explicitly non-active,
- covered already-running work cooperatively stops at safe checkpoints,
- new SMTP/provider handoff is blocked at the final delivery boundary,
- ambiguous already-started provider handoff is not automatically resent,
- reactivation does not resurrect suspension-cancelled work.

This means OL-08 does not need to invent a second generic job-cancellation framework.

### 2. Export / download ownership — PARTIAL CAPABILITY, NOT A CLOSURE EXPORT

P0.1 TI-07 already certifies tenant-safe export/download ownership for existing FAIR CRM paths, including customer Excel export, scraper artifacts and managed quote-template logos.

This proves organization-scoped export/download security primitives exist. It does **not** provide one organization-wide closure export package, completeness manifest, integrity evidence, or a policy deciding whether export is required before closure.

### 3. System backup / restore — AVAILABLE AT DATABASE LEVEL, NOT TENANT RESTORE

FAIR CRM exposes system-admin database backup/restore workflows. The API creates backup jobs for selected platform database keys and restore jobs target a database URL/database key.

Backup/restore records carry organization context for authorization/audit, but the backup payload/restore target is the selected database, not a single organization's product dataset.

Therefore current backup/restore cannot be treated as an OL-08 organization export or as a safe organization-only rollback mechanism after purge. Backup ageing and restoration of data belonging to a closed organization remain OL-10 blockers.

### 4. Provider/email account disable — AVAILABLE

Email accounts support `is_active`, and inactive accounts cannot be used for delivery. Existing lifecycle behavior also blocks outbound provider handoff while the organization is non-active.

This is sufficient to stop new provider side effects during offboarding.

### 5. Provider/email account delete — SOFT DELETE ONLY

The existing email-account delete flow snapshots the response, marks the account soft-deleted/inactive and records audit evidence.

SMTP/provider configuration and encrypted secret rows are stored separately. The normal account delete path does not constitute organization-closure secret purge or provider-side credential revocation.

Therefore OL-08 must explicitly distinguish:

1. **disable side effects** — already possible and required before destructive cleanup,
2. **provider-side revoke** — adapter/provider-specific behavior requiring an approved contract where applicable,
3. **local encrypted-secret purge** — product-owned destructive storage behavior requiring approved sequencing and audit semantics.

### 6. Organization-wide product purge/anonymization — NOT IMPLEMENTED

Current FAIR CRM has no dedicated organization-offboarding purge/anonymization module or organization-wide destructive cleanup operation.

The current registered System Admin data operations are analysis-oriented customer cleanup tools, not an organization closure engine.

A future OL-08 implementation must enumerate organization-owned data classes and relationships explicitly rather than issue an unreviewed generic delete.

## Data classes that require an explicit offboarding disposition

The implementation plan must classify, at minimum:

- customers and contacts,
- fairs and participations,
- activities, todos, follow-ups and related workflow records,
- quotations, quote templates/content/assets and cost catalog data,
- imports, import rows/results/uploads,
- scraper/enrichment runs and generated artifacts,
- operations/automation runs, logs and result artifacts,
- mail-send operations, batches/outbox/results and webhook/provider identifiers,
- SMTP/provider account records and encrypted credentials,
- generated/exported files,
- FAIR CRM audit/event references where product-owned,
- system backup/restore metadata and database dumps where they can contain organization data.

Each class must eventually be assigned one approved action such as retain, anonymize, hard-delete, revoke, export-then-delete, or retain-until-policy-expiry. Those choices must not be inferred from database cascade convenience.

## Proposed OL-08 orchestration shape — NOT YET ACCEPTED

The current architecture supports the following decision shape, subject to explicit acceptance:

```text
closure approved by SYSTEM authority
  -> organization becomes non-active / no new product work
  -> verify covered queued/running work is settled
  -> freeze closure snapshot / idempotency key
  -> generate closure export if approved policy or user right requires it
  -> verify export completeness/integrity if an export is required
  -> disable all product provider accounts / new external side effects
  -> revoke provider-side credentials where an approved provider contract exists
  -> apply approved per-data-class retention/anonymization/delete policy
  -> purge local provider secrets at the approved irreversible stage
  -> remove/expire generated product files according to approved policy
  -> preserve required audit/security evidence according to approved policy
  -> verify no active product work or usable provider credential remains
  -> Core organization tombstone/soft-delete LAST
```

The orchestration must be restartable/idempotent. A partial failure must not silently advance to Core tombstone while required product cleanup remains incomplete.

## Required acceptance decisions before destructive implementation

### OL08-A — Closure state/orchestration authority

Decide how a closure approved by Platform SuperAdmin is represented while product cleanup is in progress. A Core tombstone cannot be used as the starting signal because it is defined as the final step.

Required outcome:

- one authoritative closure execution identifier/state,
- SYSTEM-only execution,
- idempotent retry/restart semantics,
- explicit failure state,
- auditable actor, target organization, phase and timestamps.

### OL08-B — Export obligation and contract

Decide whether closure export is:

- always required,
- operator/user requested,
- legally/policy conditionally required,
- or N/A for particular data classes.

If required, define format, included data classes, artifact ownership, expiry and completeness/integrity evidence.

Existing feature-level exports cannot silently be treated as a complete closure export.

### OL08-C — Provider credential disposition

Decide, per provider type:

- whether provider-side revocation is technically supported/required,
- whether local secret deletion occurs before or after retained delivery/audit metadata is finalized,
- what evidence proves the credential is no longer usable,
- how external provider identifiers needed for historical audit are retained without retaining reusable secrets.

### OL08-D — Product-data disposition matrix

Blocked on OL-09 policy choices where duration or grace affects the action.

For every data class, approve one of:

- retain for approved duration,
- anonymize,
- hard-delete,
- export then delete,
- retain indefinitely only where an explicit legal/audit requirement says so.

No duration is chosen in this readiness document.

### OL08-E — Generated artifact disposition

Define treatment of uploads, exports, scraper artifacts, quote/logo assets, operation results and other product files independently from relational rows.

### OL08-F — Audit/security evidence

Define which lifecycle/offboarding audit evidence survives product-data cleanup and for how long. Raw credentials, tokens and unnecessary personal/business payloads must not be retained merely for debugging convenience.

### OL08-G — Backup/restore interaction

Blocked on OL-10.

Define:

- when closed organization data ages out of backups,
- whether a full database restore may reintroduce logically deleted organization data,
- mandatory post-restore reconciliation/tombstone replay if applicable,
- whether restore into production requires a closure-state reconciliation gate.

## Technical implementation order after acceptance

A safe implementation can be split into independently reviewable phases:

1. **OL08-01 — Closure execution contract/state machine**
   - no destructive cleanup yet,
   - SYSTEM-authorized start/status/retry,
   - idempotency and audit evidence,
   - Core tombstone prohibited until product phases complete.

2. **OL08-02 — Quiescence certification**
   - reuse OL-07 lifecycle behavior,
   - prove no covered queued/running/new provider work survives the closure precondition.

3. **OL08-03 — Closure export contract**
   - only after OL08-B acceptance,
   - organization-scoped manifest and completeness evidence.

4. **OL08-04 — Provider disable/revoke/secret cleanup**
   - only after OL08-C acceptance,
   - separate disable, external revoke and local secret purge states.

5. **OL08-05 — Product data/artifact disposition engine**
   - only after OL08-D/E and applicable OL-09 decisions,
   - explicit per-data-class handlers with idempotent evidence.

6. **OL08-06 — Backup/restore reconciliation**
   - only after OL-10 acceptance.

7. **OL08-07 — Final Core tombstone orchestration**
   - allowed only when every required prior phase is verified complete,
   - tombstone remains the final cross-repository lifecycle mutation.

8. **Final cross-repository certification**
   - partial-failure restart,
   - duplicate execution/idempotency,
   - cross-organization denial,
   - provider-secret non-usability,
   - export ownership/completeness where applicable,
   - no product resurrection after final tombstone,
   - backup/restore behavior per accepted OL-10 policy.

The numbering above is a readiness proposal only. It becomes an implementation sequence only after OL-08 is explicitly accepted.

## Current blockers

| Blocker | Owner | Status | Why it blocks destructive runtime |
| --- | --- | --- | --- |
| OL-08 acceptance | Platform/maintainers | **PENDING ACCEPTANCE** | Closure orchestration itself is not yet an accepted lifecycle decision. |
| Export obligation/format | Product/policy | **OPEN** | Existing exports do not define a closure-complete package. |
| Provider revocation + local secret purge sequencing | Product/provider policy | **OPEN** | Soft-delete is not credential revocation/destruction. |
| OL-09 retention/grace choices | Business/legal/maintainers | **OPEN CHOICE** | Cannot safely choose retain/anonymize/hard-delete timing. |
| OL-10 backup ageing/restoration | Operations/policy/maintainers | **OPEN CHOICE** | Full database restore can conflict with destructive closure semantics. |

## Readiness conclusion

OL-08 is **not implementation-ready for destructive cleanup**.

The repository already has strong prerequisites: OL-07 quiescence semantics, tenant-safe existing exports/downloads, system backup/restore infrastructure, organization-scoped provider accounts and account disable/soft-delete behavior. The missing work is not a generic framework gap; it is the explicit offboarding policy and orchestration contract that determines what may be destroyed, when, with what evidence, and how backup restoration must behave afterward.

Until the acceptance decisions above are resolved:

- do not hard-delete organization product data,
- do not purge provider secrets as a lifecycle side effect,
- do not treat existing database backup as an organization export,
- do not call Core organization delete/tombstone as the beginning of closure,
- do not invent retention/grace durations,
- do not claim OL-08 implemented or accepted.
