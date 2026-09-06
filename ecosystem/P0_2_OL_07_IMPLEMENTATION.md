# P0.2 OL-07 — Suspension Job / Provider Behavior Implementation Tracker

**Status:** IN PROGRESS — OL07-03, OL07-04 and OL07-05 complete  
**Current resume point:** OL07-06  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Scope

OL-07 defines deterministic FAIR CRM behavior when the Core-owned organization lifecycle no longer allows product work. The lifecycle authority remains KYROX Core; FAIR CRM consumes the public lifecycle contract and owns product-job/provider behavior.

OL-07 is not complete yet. This tracker records only implemented and verified substeps and must not be read as approval of still-open provider/in-flight semantics.

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

## Current certified behavior

```text
Core lifecycle ACTIVE
  -> queued work may start
  -> running work may continue

Core lifecycle SUSPENDED / non-active
  -> queued work is cancelled before start
  -> running work stops at the next safe checkpoint
  -> open product transaction is rolled back where the runner owns that transaction
  -> running job/run is terminalized as cancelled

Core lifecycle unavailable / invalid
  -> fail closed
  -> do not invent ACTIVE state
  -> do not falsely record explicit suspension cancellation
```

## Still open in OL-07

OL07-05 does **not** complete OL-07. The following provider/outbound side-effect behavior remains separately gated:

- OL07-06+ outbound provider dispatch / credential-side behavior after suspension,
- in-flight provider-call semantics where an already handed-off SMTP/provider action cannot necessarily be recalled,
- deterministic provider-side resumption behavior after organization reactivation,
- final OL-07 cross-repository certification and canonical ADR/roadmap closure.

No OL-08 closure/export/retention/delete behavior is authorized by this tracker.

## Resume point

**Next: OL07-06.** Do not broaden OL07-05 further; its running-work checkpoint scope is complete and merged.
