# P0.2 OL-07 — Suspension Job / Provider Behavior Implementation Tracker

**Status:** DONE 2026-09-07 — lifecycle authority, suspension execution, provider handoff and deterministic reactivation/resumption certified  
**Canonical decision source:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Scope

OL-07 defines deterministic FAIR CRM behavior when the Core-owned organization lifecycle no longer allows product work and when a suspended organization is later reactivated. The lifecycle authority remains KYROX Core; FAIR CRM consumes the public lifecycle contract and owns product-job/provider behavior.

OL-07 is complete. This tracker records the implemented and verified suspension, provider-handoff and reactivation/resumption semantics. It does **not** authorize OL-08 closure/export/retention/delete behavior.

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

- [x] **OL07-07 — Define in-flight provider handoff semantics**
  - FAIR CRM PR #253 made the claimed mail operation's `SENDING` state durable before external provider handoff begins.
  - If the durable checkpoint commit fails, no provider call is attempted; the SQLAlchemy session is rolled back/recovered before worker failure bookkeeping and the pre-handoff failure remains retryable as `handoff_checkpoint_commit_failed`.
  - MailerSend and SMTP outcomes that become ambiguous after handoff starts are terminalized as non-auto-retry uncertain failures so an unknown provider acceptance cannot cause a duplicate send.
  - SMTP/provider acceptance remains successful even if only later connection close/QUIT cleanup fails.
  - Provider error policy cannot re-enable automatic retry for `provider_handoff_uncertain`, `smtp_handoff_uncertain`, `smtp_timeout`, or stale `sending_timeout` outcomes.
  - Regression coverage includes real SQLAlchemy commit-failure session recovery, provider-not-called on checkpoint failure, MailerSend/SMTP ambiguous handoff, acceptance-after-close failure, and no-auto-retry behavior.
  - PR #253 final head `c94be579f071deb7de8ed340690c4d88d5d71c93` passed Development Standard Gate #696 and Prod-Path E2E #261 before merge.
  - FAIR CRM merge commit: `4f52961341bc4d80c4a576fa85525aa511d68b82`.
  - **OL07-07 completed 2026-09-07.**

- [x] **Final reactivation/resumption certification**
  - FAIR CRM PR #254 certified that Core `SUSPENDED -> ACTIVE` restores eligibility for new work but does not resurrect previously terminalized product work.
  - Work explicitly cancelled because of suspension remains `CANCELLED`; old detached callbacks remain locally non-startable after reactivation.
  - Newly created/queued work after reactivation may start through the normal lifecycle gate.
  - Work deferred only because Core lifecycle authority was temporarily unavailable remains non-terminal and may start once authority returns and reports `ACTIVE`.
  - Provider accounts/configuration remain active and encrypted during suspension; new outbound work after reactivation can use the same configured account without a lifecycle credential re-enable mutation.
  - Mail cancelled before provider handoff remains terminal and is not selected by the mail worker after reactivation.
  - `provider_handoff_uncertain` remains terminal/non-auto-retry after reactivation; lifecycle restoration cannot make an ambiguous external side effect safe to resend.
  - No FAIR CRM application runtime change was required because the existing state machines and worker selectors already enforced these semantics; PR #254 added explicit cross-state regression certification.
  - PR #254 final head `e17593e49ecb25a3aef736b0ceaa1fafa14c7e77` passed Development Standard Gate #700 and Prod-Path E2E #264 before merge.
  - FAIR CRM squash-merge commit: `18b0b638ba946c2910698e1df7c4ab5283c4958f`.
  - **Deterministic reactivation/resumption certified 2026-09-07.**

## Final certified behavior

```text
Core lifecycle ACTIVE
  -> fresh/new queued work may start
  -> currently running allowed work may continue
  -> new outbound SMTP/provider handoff may proceed
  -> provider configuration preserved through suspension is usable without lifecycle re-enable
  -> work merely deferred by temporary lifecycle-authority outage may proceed once authority returns ACTIVE
  -> previously suspension-cancelled work is NOT resurrected
  -> cancelled/ambiguous mail is NOT automatically resent

Core lifecycle SUSPENDED / non-active
  -> queued work is cancelled before start
  -> running work stops at the next safe checkpoint
  -> open product transaction is rolled back where the runner owns that transaction
  -> running job/run is terminalized as cancelled
  -> new outbound SMTP/provider handoff is blocked at the central delivery boundary
  -> claimed/synchronous mail work blocked at that boundary is terminalized as cancelled
  -> provider account configuration and encrypted credentials are preserved
  -> an already-started provider handoff is never synthetically recalled
  -> ambiguous in-flight provider outcomes are terminal failed/non-auto-retry

Core lifecycle unavailable / invalid
  -> fail closed
  -> do not invent ACTIVE state
  -> do not call the outbound provider
  -> do not falsely record explicit suspension cancellation
  -> pre-start work left non-terminal may proceed later only after authority returns and reports ACTIVE
```

## OL-07 completion boundary

OL-07 is **DONE**. The suspension and reactivation lifecycle semantics are deterministic across queued work, running work, outbound provider handoff and ambiguous in-flight delivery outcomes.

OL-07 completion does not authorize or imply:

- closure/export/retention/anonymization/delete sequencing,
- provider credential revocation for organization closure,
- retention/grace durations,
- backup ageing or restore behavior.

Those remain OL-08 through OL-10 decision scope.
