# P0.2 OL-09B — Suspended Webhook Service Boundary Decision

**Status:** PARTIALLY ACCEPTED — SUSPEND-TIME SERVICE BOUNDARY ACCEPTED; FINAL DRAIN EXPIRY OPEN  
**Accepted:** 2026-09-08  
**Parent readiness:** `ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`  
**Related credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`  
**Related grace decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`

## Purpose

Define what FAIR CRM may continue to do with delayed MailerSend webhooks after the organization enters Core `SUSPENDED`, without turning the receive-only drain into continued customer-facing mail service or unnecessary system load.

This decision deliberately separates two concerns:

1. **what may still be processed while suspended** — accepted here,
2. **how long the signing secret is retained before final purge** — still open.

## Verified current FAIR CRM facts

The current MailerSend webhook ingress is synchronous and public (signature protected). It uses a global semaphore to bound DB concurrency and delegates processing to `MailerSendWebhookService`.

The current provider-status policy recognizes these MailerSend event types:

- `activity.sent`
- `activity.delivered`
- `activity.soft_bounced`
- `activity.hard_bounced`
- `activity.deferred`
- `activity.opened`
- `activity.opened_unique`
- `activity.clicked`
- `activity.clicked_unique`
- `activity.unsubscribed`
- `activity.spam_complaint`

Current webhook processing normally resolves the email account, verifies the signing secret, resolves the mail-send operation by external message id and may update provider status.

`activity.unsubscribed` and `activity.spam_complaint` additionally enforce CRM communication consent by setting the resolved contact/customer `email_allowed=False` and recording the consent activity.

OL08-04A already provides durable credential-disposition evidence including `outbound_disabled_at`, `signing_secret_retained` and `receive_only_pending`, but that state is created when credential disposition starts; it is not itself proof that the exact Core suspension transition has just occurred.

The existing Core lifecycle guard deliberately performs live, uncached reads and does not persist Core lifecycle state.

## Accepted OL09-B1 — service boundary at suspension

The semantic service boundary is the authoritative Core transition into `SUSPENDED`.

From that boundary onward:

- no new outbound mail/provider handoff is permitted under the existing OL-07/OL08-C rules,
- delayed webhook traffic must **not** continue normal tenant-facing mail analytics or delivery-status service,
- receive-only processing is limited to the minimum safety/compliance set below,
- the 30-day OL09-A closure grace does not mean 30 more days of normal mail service.

### Allowed minimum protective event set while suspended

The accepted protective set is:

- `activity.unsubscribed`
- `activity.spam_complaint`
- `activity.hard_bounced`

Semantics:

- `unsubscribed` and `spam_complaint` may perform the minimum consent/suppression mutation required to prevent future unwanted mail if the organization later reactivates,
- `hard_bounced` may retain only minimum sender-safety/suppression evidence/status needed to avoid unsafe future delivery behavior,
- these events must not be expanded into customer-facing analytics, engagement scoring, dashboard work or unrelated activity generation beyond the minimum accepted compliance/safety evidence.

### Events that must be acknowledged and dropped while suspended

The following currently supported events are treated as non-essential tenant mail service while suspended:

- `activity.sent`
- `activity.delivered`
- `activity.soft_bounced`
- `activity.deferred`
- `activity.opened`
- `activity.opened_unique`
- `activity.clicked`
- `activity.clicked_unique`

For this dropped set, the suspended path must not:

- perform mail-send-operation lookup solely to update provider analytics/status,
- write provider-status progression,
- create CRM activities,
- enqueue background jobs,
- update dashboards/engagement metrics,
- create one durable audit row per dropped webhook,
- scan historical messages or precompute a backlog.

The endpoint may acknowledge the event successfully so the provider does not repeatedly retry an intentionally ignored tenant-service event.

Unknown/unsupported provider events remain ignored under the existing provider contract.

## Performance / load contract

The accepted design goal is **O(incoming webhook)** with an early, bounded fail-fast path and no tenant-wide work.

Required properties:

- no scan of previously sent mail,
- no per-tenant polling loop,
- no per-message scheduler,
- no replay queue for dropped analytics,
- no per-event Core network round-trip on the steady-state suspended fast path,
- no backfill of suspended-period analytics after later reactivation,
- any later expiry cleanup must be batch/index driven rather than one timer/process per tenant or message.

A 40,000-message pre-suspension send therefore does not cause FAIR CRM to iterate those 40,000 records after suspension. Only provider requests that actually arrive reach ingress, and non-protective events are expected to terminate on the cheapest safe path.

## Lifecycle authority / implementation constraint

Core remains the authoritative lifecycle owner. FAIR CRM must not invent suspension from local timestamps or operator input.

At the same time, the existing lifecycle guard is a synchronous uncached Core read. Calling it once for every delayed webhook would directly conflict with the accepted low-load objective.

Therefore this decision **does not yet authorize an implementation that guesses or locally fabricates Core lifecycle authority**. A bounded runtime slice must first define a deterministic, fail-closed way to make the authoritative `SUSPENDED` boundary cheaply available to webhook ingress without widening organization authority or introducing an unbounded per-webhook Core dependency.

Possible implementation mechanisms must be evaluated against existing lifecycle ownership and reactivation semantics before runtime authorization. This decision accepts the service behavior, not a speculative synchronization mechanism.

## Reactivation semantics

If Core transitions the organization back to `ACTIVE` within the OL09-A grace period:

- normal mail service may resume only through accepted reactivation/credential rules,
- webhook analytics intentionally dropped during the suspended interval are **not backfilled**,
- protective consent/safety effects recorded during suspension remain effective unless separately and lawfully changed by later user/operator action,
- reactivation must not reinterpret the suspended interval as a period of paid/active service.

## OL09-B2 — final receive-only drain expiry — STILL OPEN

This decision does **not** choose:

- the final signing-secret retention duration,
- the clock origin for that final purge,
- a provider-terminal criterion,
- a hybrid terminal/maximum-duration rule,
- the exact post-expiry handling of late signed webhooks after the secret is gone.

Until OL09-B2 is accepted, final webhook signing-secret zeroization remains gated by OL08-C4 / OL-09.

No cleanup timer, purge worker or expiry scheduler is authorized by this decision.

## Explicitly not authorized

This decision does not authorize:

- final webhook signing-secret purge,
- a 7-day, 30-day or other drain duration,
- customer-facing mail analytics while suspended,
- replay/backfill of ignored analytics,
- new outbound mail/provider handoff while suspended,
- MailerSend token revoke success for an unidentifiable token,
- product-data or generated-artifact deletion,
- closure-package expiry,
- audit/security evidence retention duration,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Decision summary

**Accepted:** suspension ends normal mail-service webhook processing immediately. During receive-only drain, only `unsubscribed`, `spam_complaint` and `hard_bounced` may receive minimum compliance/sender-safety handling; normal delivery/engagement events are acknowledged and dropped on an early low-cost path. Suspended-period analytics are never backfilled.

**Still open:** the deterministic low-cost lifecycle signal used by runtime ingress and the final signing-secret drain expiry/clock. Those must be accepted before the corresponding runtime/final purge can be certified.
