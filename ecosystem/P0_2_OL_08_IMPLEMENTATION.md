# P0.2 OL-08 — Organization Offboarding Implementation Tracker

**Status:** IN PROGRESS — OL08-01, OL08-02, OL08-03A, OL08-04A, OL08-C2, OL08-D, OL08-E1, OL08-E2 and OL08-07 DONE / CERTIFIED; current-model credential, canonical package/inventory/integrity, managed-artifact/package purge, product-data hard-delete and terminal Core-tombstone runtimes are covered, while OL08-F retained-evidence purge/de-identification remains open  
**Started:** 2026-09-07  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**Readiness source:** `ecosystem/P0_2_OL_08_DECISION_READINESS.md`  
**OL08-B decision:** `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`  
**OL08-C decision:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`  
**OL08-C2 decision:** `ecosystem/P0_2_OL_08_C2_MAILERSEND_VERIFIABLE_INVALIDATION_DECISION.md`  
**OL08-C2 runtime acceptance:** `ecosystem/P0_2_OL_08_C2_RUNTIME_ACCEPTANCE.md`  
**OL08-D decision:** `ecosystem/P0_2_OL_08_D_PRODUCT_DATA_DISPOSITION_DECISION.md`  
**OL08-D runtime acceptance:** `ecosystem/P0_2_OL_08_D_RUNTIME_ACCEPTANCE.md`  
**OL08-E decision:** `ecosystem/P0_2_OL_08_E_ARTIFACT_PACKAGE_LIFECYCLE_DECISION.md`  
**OL08-E1 runtime acceptance:** `ecosystem/P0_2_OL_08_E1_RUNTIME_ACCEPTANCE.md`  
**OL08-E2 runtime acceptance:** `ecosystem/P0_2_OL_08_E2_RUNTIME_ACCEPTANCE.md`  
**OL08-07 terminal decision:** `ecosystem/P0_2_OL_08_07_TERMINAL_CLOSURE_MILESTONE_DECISION.md`  
**OL08-07 runtime acceptance:** `ecosystem/P0_2_OL_08_07_RUNTIME_ACCEPTANCE.md`  
**Current resume point:** OL08-F retained minimal closure/audit/security evidence purge/de-identification after 12 calendar months from the certified authoritative terminal Core `deleted_at` / FAIR `closed_at` timestamp

## Current canonical policy/runtime truth

The older OL-09 decision-readiness resume point is superseded.

Canonical merged policy/runtime now establishes:

- OL09-A: 30-day reversible organization grace from the authoritative current Core suspension episode,
- OL09-B: zero-day post-suspension MailerSend webhook-signing-secret retention plus an immediate fail-closed webhook ingress cutoff,
- OL09-C: no additional generic product-data retention interval after the valid 30-day grace,
- OL09-D: 12-month minimal non-secret closure/audit/security evidence retention from the authoritative terminal Core tombstone timestamp,
- OL09-E: closure-package retention is 30 days from durable package readiness; download does not reset the clock,
- OL08-D policy: current verified tenant-owned relational product data is accepted for dependency-aware hard delete after all applicable gates,
- OL08-D runtime: the current-model 19-class product-data hard-delete engine is implemented/certified with exact current-suspension episode/grace, export-plan/package identity, credential and artifact prerequisites; import embedded bytes are physically resolved through the authorized relational-delete path,
- OL08-E: managed-artifact inventory, canonical closure package, integrity verification and strict managed-artifact purge policy are accepted,
- OL08-E1 runtime: canonical package materialization, current-model artifact inventory, deterministic integrity verification, restart reconciliation and SYSTEM-only retrieval are implemented/certified,
- OL08-E2 runtime: exact post-grace managed-file deletion, post-delete non-existence evidence, external-reference non-action and independent canonical package expiry/purge are implemented/certified,
- OL08-C2: legacy MailerSend tokens may be reconciled by exact-secret invalidity proof without guessing provider token ids,
- OL08-07 runtime: final Core tombstone orchestration is implemented/certified; FAIR `closed_at` mirrors authoritative Core `deleted_at`, same-suspension-episode CAS is enforced, terminal prerequisites are revalidated, and Core-success/FAIR-write partial failure is restart-reconciled without a second delete,
- OL10: backup ageing/restore reconciliation policy and runtime are accepted, including FAIR CRM 30-day full-DB backup ageing and fail-closed Core lifecycle reconciliation.

Timing/policy acceptance does not itself authorize destructive work. OL08-D product-data hard delete and OL08-07 terminal tombstone are runtime-covered, but each execution remains fail-closed on its live prerequisites. OL08-F is now a **post-terminal retention-maintenance runtime**: it may act only after the accepted 12-month deadline measured from the certified terminal timestamp.

## Accepted OL08-A policy

Organization closure execution is a Platform SuperAdmin / SYSTEM-controlled, FAIR CRM-owned durable orchestration. Core remains canonical organization lifecycle authority. Closure execution may begin only after Core reports the organization as non-deleted and `SUSPENDED`; Core tombstone remains the final cross-repository lifecycle mutation.

Operational invariants:

- closure execution authority remains Platform SuperAdmin / SYSTEM only,
- Core remains authoritative for organization lifecycle state,
- closure progress is FAIR CRM-owned durable state rather than a new Core `OrganizationStatus`,
- at most one open closure execution may exist per organization,
- start/retry behavior is idempotent and restartable,
- failure/block state and audit evidence are explicit,
- Core tombstone may execute only through the certified OL08-07 terminal gate set after every required pre-terminal obligation is satisfied.

## OL08-01 — Non-destructive closure execution — DONE 2026-09-07

FAIR CRM PR #255 delivered:

- durable `organization_closure_executions` state,
- append-only closure evidence,
- SYSTEM-authorized start/status/retry,
- live Core `SUSPENDED` fail-closed precondition,
- one-open-execution and idempotency constraints,
- tenant isolation and foreign-organization denial,
- transactional audit evidence,
- no destructive cleanup/tombstone behavior.

Exact evidence:

- FAIR CRM PR #255 final head `aa34cd3e5d00ec6f7d6b7adaad4afa950319830e`,
- Development Standard Gate #707 / run `34155567277`: SUCCESS,
- Prod-Path E2E #270 / run `34155567315`: SUCCESS,
- FAIR CRM merge `e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`,
- Platform PR #36 / Platform Standards CI #104: SUCCESS.

## OL08-02 — Closure quiescence certification — DONE 2026-09-08

FAIR CRM PR #256 certified that an open closure execution does not bypass OL-07 lifecycle guards. Queued work cannot start, running work stops at accepted checkpoints, new provider handoff is blocked, ambiguous already-started handoff remains terminal/non-auto-retry, suspension-cancelled work is not resurrected and lifecycle-authority outage fails closed.

It also fixed the closure-start FK ordering while retaining one transaction.

Exact evidence:

- FAIR CRM PR #256 final head `bae0e7f720e29b688765999fff12deda8624dad7`,
- Development Standard Gate #711 / run `34160597160`: SUCCESS,
- Prod-Path E2E #273 / run `34160597182`: SUCCESS,
- FAIR CRM merge `00f7219c45a5c761df0861e7b30a89ad2a67652d`.

## OL08-B / OL08-03A — Export manifest and completeness planning

OL08-B remains a policy-conditioned export contract:

```text
required
not_required
```

Missing/unknown disposition fails closed. No accepted policy source currently authorizes `not_required`, so runtime must not use it as satisfied evidence.

OL08-03A is DONE. FAIR CRM PR #257 delivered a versioned organization + closure-execution scoped manifest/completeness planner, explicit structured-data registry, tenant-scoped counts and record-ID-only fingerprints, secret-source exclusion, idempotent planning and non-secret evidence.

Exact evidence:

- FAIR CRM PR #257 final head `6927dabea1cf46e1ee70b726d3c8ccd1ae247dcd`,
- Development Standard Gate #715 / run `34163087279`: SUCCESS,
- Prod-Path E2E #276 / run `34163087299`: SUCCESS,
- FAIR CRM merge `eac3a0793a6ea0382e3b82169a1e3c18c0accfc9`.

OL08-E1 materializes a required plan into a persistent canonical package and verifies real package membership/integrity. OL08-E2 provides the accepted managed-file cleanup and package-purge mechanics. OL08-D revalidates package-bound export identities before the first irreversible product-data delete. `not_required` still has no accepted success authority.

## OL08-C — Provider credential disposition

The accepted credential contract separates:

1. outbound disablement,
2. external/provider invalidation evidence,
3. local reusable send-secret zeroization,
4. webhook signing-secret lifecycle.

A successful closure may never substitute local secret deletion for required external invalidation evidence.

### OL08-04A — Credential state/evidence foundation — DONE / CERTIFIED 2026-09-08

FAIR CRM PR #258 delivered:

- migration `0079_closure_credential_dispositions`,
- durable credential disposition rows and append-only evidence,
- SYSTEM-only start/list/get/retry/reconcile,
- live Core `SUSPENDED` fail-closed mutation precondition,
- outbound disablement without email-account deletion,
- generic SMTP `operator_required` behavior and evidence-before-local-zeroization ordering,
- MailerSend `supported_unidentifiable` fail-closed classification,
- no unverified provider-id override,
- tenant isolation and non-secret evidence boundaries.

Exact evidence:

- FAIR CRM PR #258 final head `ea12e43f0ba0066842630208217d27962fdde53c`,
- Development Standard Gate #719 / run `34194802163`: SUCCESS,
- Prod-Path E2E #279 / run `34194802141`, final attempt 2: SUCCESS,
- FAIR CRM merge `f5fb4ad18165848ae632b71496a5e5d1cb7a403b`,
- Platform PR #42 / Platform Standards CI #116: SUCCESS.

### OL08-C2 — Legacy MailerSend verifiable invalidation — DONE / RUNTIME ACCEPTED 2026-09-09

Canonical policy: `ecosystem/P0_2_OL_08_C2_MAILERSEND_VERIFIABLE_INVALIDATION_DECISION.md`.

Canonical runtime acceptance: `ecosystem/P0_2_OL_08_C2_RUNTIME_ACCEPTANCE.md`.

FAIR CRM PR #266 implements the accepted legacy/current-model reconciliation path without guessing a MailerSend provider token id.

Accepted runtime behavior:

- exact stored MailerSend API token is used only for a non-mutating provider authentication request,
- definitive HTTP `401` is the only provider result that confirms exact-secret invalidity,
- HTTP `200` and `403` remain blocked because invalidity is not proven,
- `429`, `5xx`, transport/TLS/request and unexpected results remain unknown/blocked and safely reconcilable,
- operator assertion alone cannot mark invalidation successful,
- the exact local token is retained until accepted invalidity proof because it is required for reconciliation,
- after definitive `401`, external invalidation is confirmed and the local API token is zeroized,
- success is idempotent; a completed credential is not re-authenticated,
- durable evidence stores bounded classifications only, never token plaintext, Authorization headers, secret hash/fingerprint or sensitive provider bodies/headers,
- live Core `SUSPENDED`, SYSTEM authority and open-execution guards remain mandatory.

Exact evidence:

- FAIR CRM PR #266 exact head `9cdaed2a5df57a78446758d6db3f3afb38ee4d86`,
- Development Standard Gate #747 / run `34392895839`: SUCCESS,
- Prod-Path E2E #295 / run `34392895803`: SUCCESS,
- FAIR CRM merge `ca41d369727874dff5c5e70cda43828086ffa9a4`.

OL09-B separately covers MailerSend webhook-signing-secret zeroization and the immediate post-suspension ingress authorization cutoff. Therefore the current-model MailerSend send token and webhook verification secret are no longer blocked by the older unresolved runtime assumptions.

A particular legacy credential can still remain operationally blocked until the required provider-side operator action is followed by definitive exact-secret `401` proof. That is correct fail-closed execution state, not an unimplemented contract.

## OL08-E1 — Canonical package / managed-artifact inventory / integrity — DONE / RUNTIME ACCEPTED 2026-09-09

Canonical policy: `ecosystem/P0_2_OL_08_E_ARTIFACT_PACKAGE_LIFECYCLE_DECISION.md`.

Canonical E1 runtime acceptance: `ecosystem/P0_2_OL_08_E1_RUNTIME_ACCEPTANCE.md`.

FAIR CRM PR #267 implements the non-destructive package/inventory/integrity slice:

- migration `0080_closure_packages`,
- durable canonical package and versioned artifact inventory state,
- deterministic package identity per organization + closure execution + schema,
- real portable structured export materialization from the accepted OL08-03A registry,
- stale plan/current record-identity fail-closed checks,
- hard reusable-secret source exclusion,
- managed quote-template logo inventory and referenced-file inclusion,
- external logo URLs as reference-only/non-owned pointers,
- import `stored_file_content` artifact inclusion,
- org-owned/safe-path scraper JSON/XLSX handoff inclusion,
- deterministic immutable archive bytes with exact member registry,
- SHA-256 manifest/member/final-package verification,
- restart-safe reconciliation of existing canonical bytes after incomplete durable state commit,
- SYSTEM-only metadata/inventory/download surface,
- live Core `SUSPENDED` retrieval gate,
- 30-day package clock from durable `ready_at`, with downloads not resetting it,
- no source artifact delete, package purge, product-data delete or tombstone behavior in E1.

Exact evidence:

- FAIR CRM PR #267 exact head `36a484eb9491f2f226454269bb1a5af2d7b3037f`,
- Development Standard Gate #749 / run `34402079984`: SUCCESS,
- Prod-Path E2E #296 / run `34402080016`: SUCCESS,
- FAIR CRM merge `025db874770ec8e9c50986f94a7c7f8cec3b27bd`.

## OL08-E2 — Strict managed-artifact / canonical package purge — DONE / RUNTIME ACCEPTED 2026-09-09

Canonical E2 runtime acceptance: `ecosystem/P0_2_OL_08_E2_RUNTIME_ACCEPTANCE.md`.

FAIR CRM PR #268 implements the bounded destructive artifact/package slice:

- migration `0081_closure_artifact_purge`,
- durable cleanup status/attempt/failure/non-existence evidence per artifact,
- exact current-Core-suspension `updated_at + 30 days` source-cleanup gate,
- canonical package integrity prerequisite before source cleanup,
- tenant-scoped quote-template logo deletion,
- run-scoped scraper handoff deletion,
- fail-closed digest mismatch protection for package-copied managed artifacts,
- traversal and symlink rejection for managed logo and scraper handoff paths,
- positive post-delete non-existence verification,
- external-reference non-action with no remote fetch/delete,
- import embedded bytes retained as `relational_delete_required` while the owning relational row still carries those bytes,
- reconciliation to `already_absent` only after OL08-D or equivalent accepted relational cleanup removes the embedded bytes,
- package purge independently governed by `ready_at + 30 days`,
- immediate package purge eligibility on live Core reactivation/cancellation semantics,
- exact package digest/manifest verification before delete,
- durable blocked/retry-safe behavior for ownership, integrity, I/O and verification failures,
- SYSTEM-only separate source-purge and package-purge operations.

Exact evidence:

- FAIR CRM PR #268 final head `3f1c26ad5f7d629eed158ed06a3db51e291cc50c`,
- Development Standard Gate #754 / run `34405415996`: SUCCESS,
- Prod-Path E2E #300 / run `34405415956`: SUCCESS,
- FAIR CRM merge `791f11e1a19c4d316e340a2bf06413013c693505`.

OL08-E current-model package/file-artifact mechanics are therefore runtime-covered through E1 + E2. The remaining import embedded-byte dependency is now completed by the accepted OL08-D relational hard-delete runtime, which reconciles the corresponding artifact inventory to positive non-existence evidence.

## OL08-D — Dependency-aware relational product-data hard delete — DONE / RUNTIME ACCEPTED 2026-09-10

Canonical policy: `ecosystem/P0_2_OL_08_D_PRODUCT_DATA_DISPOSITION_DECISION.md`.

Canonical runtime acceptance: `ecosystem/P0_2_OL_08_D_RUNTIME_ACCEPTANCE.md`.

FAIR CRM PR #269 implements the accepted current-model product-data hard-delete boundary:

- migration `0082_closure_product_cleanup`,
- versioned explicit 19-class dependency plan with durable per-class evidence,
- one destructive class per reconcile transaction for restart-safe progress,
- live Core current `SUSPENDED` episode and exact 30-day grace re-evaluation before every destructive mutation,
- canonical package integrity + E2 artifact-cleanup gate,
- OL08-C credential-completion gate,
- package-bound OL08-03A export identity/count revalidation before the first irreversible delete,
- explicit child/parent ordering rather than relying on DB cascade as policy,
- cross-organization isolation and organization-scoped deletes,
- current email-account product-row deletion only after terminal credential evidence,
- evidence-parent decoupling that retains only the non-secret account UUID rather than the live product row,
- import `stored_file_content` destruction through the authorized relational delete and E2 inventory non-existence reconciliation,
- fail-closed unknown persistent system-data-operation artifact handling,
- bounded non-secret counts/status/failure evidence without copying deleted business content or reusable secrets,
- no generic terminal cleanup declaration and no Core tombstone.

Exact evidence:

- FAIR CRM PR #269 final head `aec1b5d44206fa38b19f4289d3975da94c20a833`,
- Development Standard Gate #760 / run `34418454313`: SUCCESS,
- Prod-Path E2E #305 / run `34418454097`: SUCCESS,
- FAIR CRM squash merge `210313886e2d9d6c0443367e22b9728baa041329`,
- FAIR CRM `main` verified at `210313886e2d9d6c0443367e22b9728baa041329` after merge.

OL08-D current-model product deletion is therefore runtime-covered. Operational execution can still remain blocked for a particular organization until every live grace/export/package/credential/artifact prerequisite actually passes.

## OL08-07 — Terminal closure / final Core tombstone — DONE / RUNTIME ACCEPTED 2026-09-11

Canonical policy: `ecosystem/P0_2_OL_08_07_TERMINAL_CLOSURE_MILESTONE_DECISION.md`.

Canonical runtime acceptance: `ecosystem/P0_2_OL_08_07_RUNTIME_ACCEPTANCE.md`.

FAIR CRM PR #270 implements the accepted terminal milestone:

- migration `0083` adds durable terminal `completed` closure state,
- final Core tombstone is guarded by the complete accepted FAIR closure prerequisite set,
- same-suspension-episode CAS is enforced through Core's conditional tombstone contract,
- terminal success is derived only after Core reports `is_deleted = true` with non-null authoritative `deleted_at`,
- FAIR `closed_at` mirrors that exact Core timestamp,
- Core-success / FAIR-write partial failure is restart-reconciled from Core state without a second delete,
- repeated finalization is idempotent,
- start/retry cannot reopen a tombstoned organization,
- lifecycle/tombstone authority outage, episode drift or incomplete terminal evidence fails closed.

Exact evidence:

- FAIR CRM PR #270 final head `628c098ff2ddbfebaa5330aee94836089c54a304`,
- Development Standard Gate #769 / run `34574144876`: SUCCESS,
- Prod-Path E2E #313 / run `34574144891`: SUCCESS,
- FAIR CRM squash merge `0c2f00649dccd217bd0affdb8fb95fc7de1ba462`,
- FAIR CRM `main` verified at `0c2f00649dccd217bd0affdb8fb95fc7de1ba462` after merge.

OL08-07 therefore supplies the certified runtime clock source required by OL09-D and OL08-F: `T_terminal = Core deleted_at = FAIR closed_at`.

## Current decision/runtime matrix

| Decision | Current canonical status | Runtime boundary |
| --- | --- | --- |
| OL08-B — closure export technical contract | **PARTIALLY ACCEPTED / OL08-03A + E1 PACKAGE RUNTIME DONE** | Planner and required canonical package materialization/integrity are implemented. `not_required` still has no accepted success authority. |
| OL08-C — provider credential disposition | **ACCEPTED / CURRENT-MODEL RUNTIME COVERED** | OL08-04A foundation, OL08-C2 MailerSend exact-secret reconciliation and OL09-B signing-secret zeroization are implemented. Individual credentials may remain blocked pending required external/operator evidence. |
| OL08-D — product-data disposition | **POLICY + CURRENT-MODEL RUNTIME ACCEPTED** | Dependency-aware 19-class tenant product-data hard delete is implemented behind live grace/export/package/credential/artifact gates. Import embedded-byte destruction is coupled and certified through this phase. |
| OL08-E — generated artifacts / closure package | **POLICY ACCEPTED / E1 + E2 CURRENT-MODEL RUNTIME ACCEPTED** | Canonical package/inventory/integrity, strict managed-file cleanup, external-reference non-action and package expiry/purge are implemented. Import embedded-byte non-existence is reconciled through OL08-D. |
| OL08-07 — terminal closure / Core tombstone | **POLICY + RUNTIME ACCEPTED** | Final same-episode Core tombstone, authoritative `deleted_at` -> FAIR `closed_at` reconciliation, restart safety and completed terminal state are implemented behind the complete pre-tombstone gate set. |
| OL08-F — audit/security evidence | **TIMING POLICY ACCEPTED / PURGE RUNTIME OPEN** | Minimal non-secret evidence retention is 12 calendar months from certified terminal Core `deleted_at` / FAIR `closed_at`; purge/de-identification runtime remains to be implemented. |
| OL08-G — backup/restore interaction | **POLICY + RESTORE RUNTIME ACCEPTED VIA OL10** | FAIR full-DB 30-day ageing/pruning and fail-closed restore reconciliation are runtime-accepted; residual total-loss Core authority boundary remains fail-closed. |
| OL09-A through OL09-E | **TIMING POLICY COMPLETE** | 30-day reversible grace, zero-day webhook-secret retention, product-data timing, 12-month evidence retention and 30-day package retention are accepted. OL09-B runtime is separately accepted. |
| OL10 | **POLICY + RUNTIME ACCEPTED** | Canonical restore reconciliation and backup-ageing contract recorded by Platform PRs #53/#54. |

## Hard prohibitions that remain

Until the applicable runtime is implemented and its gate conditions are satisfied, OL-08 work must not:

- claim a required export complete without the accepted canonical package/integrity evidence,
- use `not_required` as export success without a separately accepted policy authority,
- treat local secret zeroization as provider-side invalidation proof,
- treat operator assertion as MailerSend C2 success without exact-secret `401` proof,
- guess or heuristically select a MailerSend provider token id for deletion,
- execute an OL08-D product-data class merely because 30 days elapsed; all live export/credential/artifact/lifecycle and other applicable phase gates still apply,
- delete managed artifact bytes without registered ownership, tenant scoping, package-integrity prerequisite and post-delete non-existence verification,
- treat managed-file E2 success as proof that import `stored_file_content` is gone while its relational row still carries bytes,
- remote-delete or remote-fetch external-reference logo URLs as though they were FAIR-owned bytes,
- purge the canonical closure package before its accepted `ready_at + 30 days` expiry unless the accepted closure-cancellation/reactivation path makes that package immediately purge-pending,
- let package download reset its accepted 30-day expiry clock,
- purge/de-identify retained minimal closure/security evidence before its accepted 12-month policy permits it,
- invoke final Core organization tombstone while any required FAIR closure phase remains incomplete or blocked,
- substitute FAIR wall-clock time for authoritative Core `deleted_at` when persisting terminal `closed_at`.

## Current resume point

Proceed with the next executable closure runtime in dependency order:

1. **OL08-F runtime** — implement purge/de-identification of the retained minimal non-secret closure/audit/security evidence only after **12 calendar months from the certified terminal Core `deleted_at` / FAIR `closed_at` timestamp**. It must preserve the accepted evidence boundary, avoid retaining deleted product payloads or secret-derived oracles, and remain fail-closed before the retention deadline.
2. OL08-F is **post-terminal retention maintenance**. It is not a prerequisite for the already-certified OL08-07 tombstone path; rather, OL08-07 supplies the authoritative clock that OL08-F must consume.

No accepted timing decision by itself authorizes destructive execution.