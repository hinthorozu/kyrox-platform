# P0.2 OL-08 — Organization Offboarding Implementation Tracker

**Status:** IN PROGRESS — OL08-01, OL08-02, OL08-03A and OL08-04A DONE; OL08-B technical export contract remains partially accepted; OL08-C credential-disposition contract ACCEPTED but full credential disposition remains incomplete  
**Decision:** OL08-A ACCEPTED 2026-09-07; OL08-B technical contract PARTIALLY ACCEPTED 2026-09-07; OL08-C ACCEPTED 2026-09-08  
**Started:** 2026-09-07  
**Current resume point:** OL-09 retention/grace decision-readiness — begin with OL09-A closure grace/reversibility and OL09-B webhook drain criterion; no new purge/delete runtime is authorized  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**Readiness source:** `ecosystem/P0_2_OL_08_DECISION_READINESS.md`  
**OL08-B decision:** `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`  
**OL08-C decision:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`  
**OL-09 readiness:** `ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`

## Accepted OL08-A policy

Organization closure execution is a Platform SuperAdmin / SYSTEM-controlled, FAIR CRM-owned durable orchestration. Core remains canonical organization lifecycle authority. Closure execution may begin only after Core reports the organization as non-deleted and `SUSPENDED`; Core tombstone remains the final cross-repository lifecycle mutation.

Operational invariants:

- closure execution authority remains Platform SuperAdmin / SYSTEM only,
- Core remains authoritative for organization lifecycle state,
- closure progress is FAIR CRM-owned durable state rather than a new Core `OrganizationStatus`,
- at most one open closure execution may exist per organization,
- start/retry behavior is idempotent and restartable,
- failure/block state and audit evidence are explicit,
- Core tombstone remains prohibited until every required later phase is separately accepted, implemented and certified.

## OL08-01 — Non-destructive closure execution — DONE 2026-09-07

FAIR CRM PR #255 implements the accepted OL08-A / OL08-01 closure execution contract.

Delivered runtime:

- durable `organization_closure_executions` state,
- append-only closure event evidence,
- migration `0077_organization_closure_executions`,
- SYSTEM-authorized start/status/retry API,
- live Core lifecycle re-check on start/retry,
- canonical `SUSPENDED` precondition and fail-closed lifecycle-authority handling,
- unique organization + idempotency identity,
- database-enforced one-open-execution constraint,
- same-key duplicate convergence,
- explicit `blocked` evidence and same-execution retry,
- canonical tenant-isolation registry coverage,
- foreign organization denial before mutation,
- transactional local audit evidence,
- no `cleanup_complete`, `ready_for_tombstone`, DELETE or Core tombstone call.

State boundary:

```text
no execution
  -> in_progress              only if Core == SUSPENDED and SYSTEM-authorized
  -> blocked                  explicit recoverable evidence
  -> in_progress              idempotent retry of same execution
```

Exact implementation evidence:

- FAIR CRM PR #255 final head `aa34cd3e5d00ec6f7d6b7adaad4afa950319830e`,
- Development Standard Gate #707 / run `34155567277`: SUCCESS,
- Prod-Path E2E #270 / run `34155567315`: SUCCESS,
- FAIR CRM merge `e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`,
- Platform PR #36 exact head `ea77abf48ee606ace0756303075aec518eb2c4aa`,
- Platform Standards CI #104 / run `34156643910`: SUCCESS,
- Platform merge `f08f3a334c56c3c1be31694af56bf65330e44fe9`.

Therefore OL08-01A through OL08-01I are complete.

## OL08-B — Closure export technical contract — PARTIALLY ACCEPTED 2026-09-07

The accepted technical architecture is policy-conditioned export disposition:

```text
required
not_required
```

A missing/unknown disposition fails closed. `not_required` requires durable evidence from a separately accepted policy source.

**Current rule:** no accepted `not_required` policy source exists, therefore no runtime may use `not_required` to satisfy export obligation.

Accepted export-contract invariants:

- export evidence belongs to one organization + one closure execution,
- the manifest is versioned and explicitly classifies included/excluded/deferred data classes,
- first-version customer-portable structured categories are enumerated rather than inferred from a database dump,
- generated/binary artifacts remain deferred to OL08-E,
- reusable provider/security credentials are always excluded,
- Core identity remains outside FAIR CRM export ownership,
- initial control remains Platform SuperAdmin / SYSTEM/operator-only,
- no export evidence may open an irreversible closure gate until package lifecycle and remaining policy are separately accepted.

Canonical detailed decision: `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`.

### Accepted v1 structured completeness registry

The first export completeness planner must classify at minimum:

- customers and customer communications,
- contacts,
- fairs and participations,
- activities, todos and follow-up/task records,
- quotes plus portable quote-template/template-content source data,
- cost-catalog product data,
- import/data-integration metadata and structured results,
- scraper/enrichment run metadata and normalized customer-owned structured results,
- operation/automation definitions, run metadata and customer-portable structured results,
- mail templates plus normalized customer communication/mail-send history/status records.

Explicitly deferred/excluded in the first version:

- generated/binary files and uploads — OL08-E,
- scraper/operation artifact files — OL08-E,
- quote/logo binary assets — OL08-E,
- provider/SMTP reusable secrets — always excluded,
- provider-side credential disposition behavior — OL08-C,
- Core credential/session/token data — outside FAIR CRM ownership,
- system database backups/restores — OL-10,
- derived dashboard views,
- raw provider webhook/signature/security payloads unless separately accepted later.

## OL08-02 — Closure quiescence certification — DONE 2026-09-08

FAIR CRM PR #256 certified that an open OL08 closure execution does not bypass the already-certified OL-07 suspension/runtime guards.

Certified behavior:

- covered queued/pending organization work cannot start once Core reports non-active lifecycle,
- covered running work stops at the existing safe checkpoints,
- new outbound provider handoff is blocked at the final lifecycle checkpoint,
- ambiguous already-started provider handoff remains terminal/non-auto-retry,
- suspension-cancelled work is not resurrected,
- lifecycle-authority outage fails closed,
- closure execution does not introduce a parallel cancellation framework or bypass OL-07 guards.

The certification also exposed and fixed one real OL08-01 transactional integrity defect: the parent closure execution is now flushed before its append-only start event so the existing FK cannot be violated, while both writes remain in one transaction with no intermediate commit.

Exact implementation evidence:

- FAIR CRM PR #256 final head `bae0e7f720e29b688765999fff12deda8624dad7`,
- Development Standard Gate #711 / run `34160597160`: SUCCESS,
- Prod-Path E2E #273 / run `34160597182`: SUCCESS,
- FAIR CRM merge `00f7219c45a5c761df0861e7b30a89ad2a67652d`.

Therefore OL08-02 is complete and OL08-03A became executable within the already accepted OL08-B boundary.

## OL08-03A — Export manifest / completeness planner — DONE 2026-09-08

FAIR CRM PR #257 implements the bounded, non-destructive export manifest/completeness planner authorized by OL08-B after OL08-02 certification.

Delivered runtime:

- durable export-plan identity tied to one organization + closure execution + schema version,
- migration `0078_closure_export_plans`,
- successful durable state limited by DB constraints to `required` + `planned`,
- SYSTEM-only POST planning and GET metadata/status endpoints,
- live Core `SUSPENDED` precondition for planning,
- explicit v1 structured-data completeness registry,
- organization-scoped record counts,
- deterministic record-ID-only fingerprints,
- explicit included/excluded/deferred reason evidence,
- hard secret-source exclusion for reusable SMTP/provider credential tables,
- idempotent repeat planning through organization/execution/schema-version uniqueness,
- append-only non-secret closure/audit evidence,
- tenant-isolation and foreign-organization denial coverage,
- no package/download endpoint and no customer-facing handover route.

The planner does **not** persist or expose a closure-complete package, `not_required` success, `integrity_verified`, credential revoke/purge, product-data/artifact destruction, `cleanup_complete`, `ready_for_tombstone` or Core tombstone.

Exact implementation evidence:

- FAIR CRM PR #257 final head `6927dabea1cf46e1ee70b726d3c8ccd1ae247dcd`,
- Development Standard Gate #715 / run `34163087279`: SUCCESS,
- Prod-Path E2E #276 / run `34163087299`: SUCCESS,
- FAIR CRM merge `eac3a0793a6ea0382e3b82169a1e3c18c0accfc9`.

Therefore the currently authorized OL08-B engineering slice is complete. OL08-B itself remains only partially accepted because package lifecycle and `not_required` policy authority are still unresolved.

## OL08-C — Provider credential disposition — ACCEPTED 2026-09-08

Canonical detailed decision: `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`.

Accepted contract:

- outbound credential use is disabled before credential destruction,
- provider-side invalidation, local reusable-secret zeroization and webhook-signing-secret drain are separate obligations,
- deterministic provider invalidation is mandatory for `supported_identifiable` credentials,
- `supported_unidentifiable` credentials fail closed and cannot be downgraded to not-applicable/operator-success,
- generic/provider-specific SMTP invalidation may require explicit operator evidence and cannot be inferred from local password removal,
- local reusable send secrets must become unrecoverable from FAIR CRM storage before the send-credential disposition can complete,
- MailerSend/API send tokens and webhook verification secrets have different lifecycles,
- a webhook signing secret may remain only in an explicit receive-only state for delayed signed events,
- final signing-secret zeroization is mandatory, but any elapsed-time drain duration remains an OL-09 choice,
- provider invalidation with an ambiguous external result fails closed and is reconciled rather than blindly auto-retried,
- normal email-account soft delete is not credential-disposition completion evidence.

### Authorized OL08-04A engineering boundary

The first runtime slice may implement only:

- durable organization + closure-execution + credential/account disposition state/evidence,
- credential capability classification,
- SYSTEM-only start/status/retry/reconcile surfaces,
- live Core `SUSPENDED` fail-closed mutation precondition,
- outbound-disabled evidence without deleting the email account,
- provider capability interface and deterministic MailerSend token-target metadata/support,
- external invalidation evidence/reconciliation semantics,
- local **send-secret** zeroization after required external invalidation evidence,
- receive-only webhook signing-secret state without inventing a final time-based purge duration,
- append-only non-secret audit evidence,
- tenant-isolation, idempotency, failure/restart and uncertain-result coverage.

OL08-04A must not declare full OL08-C completion while any required webhook signing secret remains `receive_only_pending`.

## OL08-04A — Credential disposition state/evidence foundation — DONE / CERTIFIED 2026-09-08

FAIR CRM PR #258 implements the bounded credential-only foundation authorized by OL08-C.

Delivered runtime:

- migration `0079_closure_credential_dispositions`,
- durable organization + closure-execution + email-account credential disposition rows,
- append-only credential evidence events,
- SYSTEM-only start/list/get/retry/reconcile surfaces under the existing closure router,
- live Core `SUSPENDED` fail-closed precondition on start/retry/reconcile,
- closure start disables outbound email-account eligibility without soft-deleting the account,
- generic SMTP reusable password is classified `operator_required`,
- local SMTP password zeroization occurs only after explicit non-secret external invalidation evidence,
- current-model MailerSend API tokens are classified `supported_unidentifiable` and remain blocked,
- operator evidence cannot override a supported-but-unidentifiable MailerSend credential,
- MailerSend target IDs may be retained only as unverified metadata and do not enable provider invalidation or local token purge,
- webhook signing secrets may remain explicitly `receive_only_pending`,
- tenant-scoped repository identity and foreign-organization denial are covered,
- disposition/audit evidence excludes secret plaintext and secret fingerprints.

Exact implementation/certification evidence:

- FAIR CRM PR #258 final head `ea12e43f0ba0066842630208217d27962fdde53c`,
- Development Standard Gate #719 / run `34194802163`: SUCCESS,
- Prod-Path E2E #279 / run `34194802141`, final attempt 2: SUCCESS,
- FAIR CRM merge `f5fb4ad18165848ae632b71496a5e5d1cb7a403b`,
- Platform PR #42 final head `7d3de63c8072b908d8d3c2c38a3a386af22e3921`,
- Platform Standards CI #116 / run `34196046348`: SUCCESS,
- Platform merge `144ee611c1f061d10ec36c4713b08262a1465bf1`.

This implementation does **not** call a MailerSend token-delete/pause API, does not claim deterministic MailerSend token invalidation from unverified metadata, does not final-purge a webhook signing secret, does not choose a webhook drain duration and does not open any product-data/artifact/retention/backup/tombstone phase.

OL08-04A is therefore cross-repository certified. **OL08-C itself remains incomplete** wherever a required credential is still blocked/unidentifiable or a webhook signing secret remains `receive_only_pending`.

## Still-gated OL-08 decisions

| Decision | Status | Runtime boundary |
| --- | --- | --- |
| OL08-B — closure export technical contract | **PARTIALLY ACCEPTED / OL08-03A DONE** | Manifest/completeness planner is implemented; persistent/downloadable package lifecycle and `not_required` policy remain gated. |
| OL08-C — provider credential disposition | **ACCEPTED / OL08-04A DONE; FULL CREDENTIAL DISPOSITION INCOMPLETE** | Credential state/evidence foundation and guarded SMTP zeroization are certified. Current-model MailerSend credentials fail closed as supported-but-unidentifiable; final webhook signing-secret purge remains dependent on an accepted drain criterion and any time-based duration remains OL-09. |
| OL08-D — product-data disposition matrix | **OPEN / depends on OL-09** | No organization-wide anonymize/hard-delete authorized. |
| OL08-E — generated artifact disposition | **OPEN** | No closure-driven artifact purge or persistent closure-package lifecycle authorized. |
| OL08-F — audit/security evidence retention | **OPEN / policy required** | No retention duration chosen. |
| OL08-G — backup/restore interaction | **OPEN / depends on OL-10** | No backup ageing or restore reconciliation semantics authorized. |
| OL-09 — retention/grace durations | **OPEN CHOICE / DECISION READINESS ACTIVE** | No duration or grace window is accepted. Readiness is documented in `P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`. |
| OL-10 — backup restore implications | **OPEN CHOICE** | Destructive closure cannot be certified until restore behavior is explicit. |

## Hard prohibitions

Until separately accepted, OL-08 work must not:

- claim a closure-complete delivered export package,
- permit `not_required` without an accepted policy source,
- treat local secret zeroization as provider-side invalidation evidence,
- auto-mark supported-but-unidentifiable provider credentials complete,
- blindly retry ambiguous provider invalidation side effects,
- purge a required webhook signing secret before its accepted drain criterion,
- invent a webhook drain/retention duration,
- anonymize or hard-delete organization product data,
- delete closure-driven generated files/artifacts,
- choose retention/grace durations,
- define backup ageing/restore reconciliation,
- add `cleanup_complete` / `ready_for_tombstone`,
- invoke Core organization delete/tombstone.

## Current resume point

Proceed with **OL-09 retention/grace decision-readiness**, beginning with:

1. **OL09-A — closure grace/reversibility and clock origin**, and
2. **OL09-B — webhook receive-only drain criterion**.

The readiness document does not select any duration and does not authorize runtime. OL08-D/E/F/G, persistent closure-package materialization, `not_required` export success, product-data/artifact destruction, final webhook signing-secret purge, backup reconciliation, cleanup/tombstone-ready state and Core tombstone remain gated until their applicable policy is separately accepted.
