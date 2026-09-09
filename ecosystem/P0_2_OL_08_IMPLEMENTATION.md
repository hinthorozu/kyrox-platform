# P0.2 OL-08 — Organization Offboarding Implementation Tracker

**Status:** IN PROGRESS — OL08-01, OL08-02, OL08-03A, OL08-04A and OL08-C2 DONE / CERTIFIED; current-model credential runtime is covered, while closure package/artifact and destructive product-data runtime remain open  
**Started:** 2026-09-07  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**Readiness source:** `ecosystem/P0_2_OL_08_DECISION_READINESS.md`  
**OL08-B decision:** `ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md`  
**OL08-C decision:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`  
**OL08-C2 decision:** `ecosystem/P0_2_OL_08_C2_MAILERSEND_VERIFIABLE_INVALIDATION_DECISION.md`  
**OL08-C2 runtime acceptance:** `ecosystem/P0_2_OL_08_C2_RUNTIME_ACCEPTANCE.md`  
**Current resume point:** OL08-E closure-package / managed-artifact runtime first, then OL08-D destructive product-data runtime after every accepted grace/export/credential/artifact gate is actually satisfied

## Current canonical policy/runtime truth

The older OL-09 decision-readiness resume point is superseded.

Canonical merged policy/runtime now establishes:

- OL09-A: 30-day reversible organization grace from the authoritative current Core suspension episode,
- OL09-B: zero-day post-suspension MailerSend webhook-signing-secret retention plus an immediate fail-closed webhook ingress cutoff,
- OL09-C: no additional generic product-data retention interval after the valid 30-day grace,
- OL09-D: 12-month minimal non-secret closure/audit/security evidence retention from the separately accepted terminal closure milestone,
- OL09-E: closure-package retention is 30 days from durable package readiness; download does not reset the clock,
- OL08-D: current verified tenant-owned relational product data is accepted for dependency-aware hard delete after all applicable gates,
- OL08-E: managed-artifact inventory, canonical closure package, integrity verification and strict managed-artifact purge policy are accepted,
- OL08-C2: legacy MailerSend tokens may be reconciled by exact-secret invalidity proof without guessing provider token ids,
- OL10: backup ageing/restore reconciliation policy and runtime are accepted, including FAIR CRM 30-day full-DB backup ageing and fail-closed Core lifecycle reconciliation.

Timing/policy acceptance does not itself execute destructive closure work. Product-data and artifact/package runtime still requires implementation and certification.

## Accepted OL08-A policy

Organization closure execution is a Platform SuperAdmin / SYSTEM-controlled, FAIR CRM-owned durable orchestration. Core remains canonical organization lifecycle authority. Closure execution may begin only after Core reports the organization as non-deleted and `SUSPENDED`; Core tombstone remains the final cross-repository lifecycle mutation.

Operational invariants:

- closure execution authority remains Platform SuperAdmin / SYSTEM only,
- Core remains authoritative for organization lifecycle state,
- closure progress is FAIR CRM-owned durable state rather than a new Core `OrganizationStatus`,
- at most one open closure execution may exist per organization,
- start/retry behavior is idempotent and restartable,
- failure/block state and audit evidence are explicit,
- Core tombstone remains prohibited until every required later phase is implemented, satisfied and certified.

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

OL08-E subsequently accepted the package/artifact lifecycle needed to continue a required export, but package materialization/integrity runtime is still open.

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

## Current decision/runtime matrix

| Decision | Current canonical status | Runtime boundary |
| --- | --- | --- |
| OL08-B — closure export technical contract | **PARTIALLY ACCEPTED / OL08-03A DONE** | Planner is implemented. OL08-E package policy is accepted, but package materialization/integrity runtime remains open. `not_required` still has no accepted success authority. |
| OL08-C — provider credential disposition | **ACCEPTED / CURRENT-MODEL RUNTIME COVERED** | OL08-04A foundation, OL08-C2 MailerSend exact-secret reconciliation and OL09-B signing-secret zeroization are implemented. Individual credentials may remain blocked pending required external/operator evidence. |
| OL08-D — product-data disposition | **POLICY ACCEPTED / RUNTIME OPEN** | Verified tenant-owned relational product data is hard-delete eligible only after valid grace and all phase gates. Destructive runtime is not yet implemented/certified. |
| OL08-E — generated artifacts / closure package | **POLICY ACCEPTED / RUNTIME OPEN** | Managed-artifact inventory, canonical package, integrity verification and strict purge semantics are accepted; production runtime is still open. |
| OL08-F — audit/security evidence | **TIMING POLICY ACCEPTED / PURGE RUNTIME OPEN** | Minimal non-secret evidence retention is 12 months from the accepted terminal closure milestone; later purge/de-identification runtime remains separate. |
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
- execute product-data hard delete merely because 30 days elapsed; all export/credential/artifact and other phase gates still apply,
- delete managed artifact bytes without registered ownership, tenant scoping and non-existence verification,
- let package download reset its accepted 30-day expiry clock,
- purge/de-identify retained minimal closure/security evidence before its accepted 12-month policy permits it,
- add `cleanup_complete` / `ready_for_tombstone` before every required closure obligation is actually satisfied,
- invoke final Core organization tombstone while any required FAIR closure phase remains incomplete or blocked.

## Current resume point

Proceed with the next executable closure runtime in dependency order:

1. **OL08-E runtime** — persistent canonical closure-package materialization, registered managed-artifact inventory, deterministic integrity verification, availability/expiry state and strict tenant-scoped artifact/package purge semantics under the already accepted policy.
2. **OL08-D runtime** — dependency-aware tenant product-data hard delete only after the valid OL09-A grace and required export/package, credential and artifact gates are satisfied.
3. Continue toward terminal cleanup/tombstone readiness only after all remaining runtime obligations are implemented and certified.

No accepted timing decision by itself authorizes destructive execution.
