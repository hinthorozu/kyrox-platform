# P0.2 OL-07 — Suspension Job / Provider Behavior Implementation Tracker

**Status:** IN PROGRESS — OL07-03, OL07-04, OL07-05 and OL07-06 complete  
**Current resume point:** OL07-07  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Scope

OL-07 defines deterministic FAIR CRM behavior when the Core-owned organization lifecycle no longer allows product work. The lifecycle authority remains KYROX Core; FAIR CRM consumes the public lifecycle contract and owns product-job/provider behavior.

OL-07 is not complete yet. This tracker records only implemented and verified substeps and must not be read as approval of still-open in-flight/provider-resumption semantics.

## Completed implementation sequence

- [x] **OL07-03 — Cross-repository lifecycle authority contract**
  - KYROX Core PR #25 added the product lifecycle snapshot contract and dedicated product lifecycle credential.
  - Core merge commit: `5ad6da0459da640893e4339a87f5528e93271161`.
  - FAIR CRM PR #249 added the read-only lifecycle client and reusable fail-closed `OrganizationLifecycleGuard`.
  - FAIR CRM merge commit: `52ecbbae2bf295f6b79eb4e89a4ac0100c0e145e`.
  - This step established lifecycle authority only; it did not alter queued/running execution behavior.

- [x] **OL07-04 — Cancel queued product work before start**
  - FAIR CRM PR #250 added deterministic pre-start lifecycle gating for organization-owned queued/pending work.
  - Covered import analyze/bulk-decision/apply, detached scraper/enrichment/data-operation jobs, and the central mail-send worker before queue claim/provider dispatch.
  - `ACTIVE` allows start; suspended/non-active lifecycle cancels before start; unavailable/invalid Core lifecycle state fails closed without guessing cancellation.
  - Cross-organization decisions remain isolated by authoritative organization context.
  - FAIR CRM merge commit: `a01b9de53090e42ddfa5f9c88a19655cc830c4b2`.

- [x] **OL07-05 — Cancel already-running product work at safe checkpoints**
  - FAIR CRM PR #251 added cooperative lifecycle checkpoints for already-running organization-owned FAIR CRM work.
  - Covered import analyze, import apply/bulk decision, scraper/adapter-test/enrichment, and data-operation execution boundaries.
  - `ACTIVE` allows the current work unit to proceed.
  - Suspended/non-active lifecycle stops before the next safe unit, rolls back the open transaction where applicable, and terminalizes the running job/run as cancelled.
  - Core lifecycle unavailable/invalid remains fail-closed and is not falsely recorded as an explicit suspension cancellation.
  - No next row/chunk/destructive boundary starts after suspension is observed at a checkpoint.
  - PR #251 final head `523f2274a37b3876b092c34b6f761573bd13eedd` passed Backend Quality Check, Feature Contract / Applicability, Frontend Tests / Build / UI Governance, and Prod-Path E2E before merge.
  - FAIR CRM squash-merge commit: `3b7b1552fc42e596dd5890eeef627d0e4159a968`.
  - **OL07-05 completed 2026-09-06.**

- [x] **OL07-06 — Block outbound provider handoff after suspension**
  - FAIR CRM PR #252 added the final lifecycle checkpoint in the central `EmailDeliveryService` immediately before real SMTP/provider dispatch.
  - `ACTIVE` allows the outbound handoff to proceed.
  - Suspended/non-active lifecycle prevents the provider from being called and terminalizes claimed/synchronous mail work as cancelled.
  - Core lifecycle unavailable/invalid fails closed before provider handoff and is not falsely recorded as explicit suspension cancellation.
  - The queue-claim → provider-handoff race is closed: lifecycle is re-checked after claim at the central side-effect boundary.
  - Worker lifecycle-authority outage after claim is recorded as failed/deferred with retry eligibility rather than sent.
  - Suspension does not delete, decrypt-persist, deactivate, or otherwise mutate provider account credentials; persisted provider secrets remain encrypted and configured.
  - PR #252 final head `d8b79e0883b2ac24f52e6c89d1a33654f211d580` passed Backend Quality Check, Feature Contract / Applicability, Frontend Tests / Build / UI Governance, and Prod-Path E2E before merge.
  - FAIR CRM squash-merge commit: `1215d3817acedd17392a036e7227d94fe330e680`.
  - **OL07-06 completed 2026-09-07.**

## Current certified behavior

```text
Core lifecycle ACTIVE
  -> queued work may start
  -> running work may continue
  -> outbound SMTP/provider handoff may proceed

Core lifecycle SUSPENDED / non-active
  -> queued work is cancelled before start
  -> running work stops at the next safe checkpoint
  -> open product transaction is rolled back where the runner owns that transaction
  -> running job/run is terminalized as cancelled
  -> new outbound SMTP/provider handoff is blocked at the central delivery boundary
  -> claimed/synchronous mail work blocked at that boundary is terminalized as cancelled
  -> provider account configuration and encrypted credentials are preserved

Core lifecycle unavailable / invalid
  -> fail closed
  -> do not invent ACTIVE state
  -> do not call the outbound provider
  -> do not falsely record explicit suspension cancellation
```

## Still open in OL-07

OL07-06 does **not** complete OL-07. The following provider lifecycle behavior remains separately gated:

- OL07-07+ in-flight provider-call semantics where an already handed-off SMTP/provider action cannot necessarily be recalled,
- deterministic provider-side resumption behavior after organization reactivation,
- final OL-07 cross-repository certification and canonical ADR/roadmap closure.

No OL-08 closure/export/retention/delete behavior is authorized by this tracker.

## Resume point

**Next: OL07-07.** OL07-06 provider-handoff prevention is complete and merged; do not broaden it into already-handed-off provider recall or reactivation-resumption semantics.
