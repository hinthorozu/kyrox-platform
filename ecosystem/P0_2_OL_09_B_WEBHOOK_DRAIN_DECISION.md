# P0.2 OL-09B — Suspended Webhook Service Boundary / Receive-Only Drain Decision

**Status:** PARTIALLY ACCEPTED — SERVICE BOUNDARY ACCEPTED; EXPIRY / FINAL PURGE DURATION OPEN  
**Accepted:** 2026-09-08  
**Parent lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`  
**OL-09 readiness:** `ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`  
**OL09-A decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**Related credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Define what FAIR CRM may continue to do with MailerSend webhook traffic after an organization enters the suspended closure path, without turning receive-only webhook handling into continued customer-facing mail service and without creating avoidable load.

This decision intentionally separates:

1. **OL09-B1 — suspended webhook service boundary / minimum protective handling — ACCEPTED**, and
2. **OL09-B2 — receive-only expiry criterion, exact duration and final signing-secret purge — OPEN**.

The 30-day organization closure grace accepted by OL09-A does **not** automatically become the webhook receive-only duration.

## Verified FAIR CRM runtime facts

### 1. Current MailerSend webhook ingress is synchronous work

`backend/app/modules/email_webhooks/api/routes.py` accepts public MailerSend webhook POSTs, parses the payload, enters a bounded semaphore and runs `MailerSendWebhookService.handle()` in a threadpool.

The current route therefore already protects the asyncio loop from webhook bursts, but every accepted provider event that reaches the service may still perform synchronous database work.

### 2. Current supported provider event taxonomy

`backend/app/modules/email_delivery/application/provider_status_policy.py` currently maps these MailerSend events:

- `activity.sent`,
- `activity.delivered`,
- `activity.soft_bounced`,
- `activity.hard_bounced`,
- `activity.deferred`,
- `activity.opened`,
- `activity.opened_unique`,
- `activity.clicked`,
- `activity.clicked_unique`,
- `activity.unsubscribed`,
- `activity.spam_complaint`.

The normal webhook service resolves the mail-send operation and may update its provider status for this taxonomy.

### 3. Only two current events have explicit consent-protection semantics

`MailerSendWebhookService` currently treats only:

- `activity.unsubscribed`, and
- `activity.spam_complaint`

as `CONSENT_EVENTS`.

For those events, the current implementation can turn the linked customer/contact `email_allowed` flag off. It also creates a CRM Activity record describing the consent change.

The accepted suspended-mode boundary must preserve the **protective consent mutation** but must not preserve the customer-facing Activity creation merely to keep serving a suspended tenant.

### 4. Delivery/engagement status tracking is normal product service

For suspended-mode policy purposes, `sent`, `delivered`, `deferred`, soft/hard bounce provider-status progression, `opened` and `clicked` tracking are not required to continue the customer's normal mail analytics/service after suspension.

This does not claim that those provider events are globally useless. It means their normal tenant-facing status/analytics processing is not an obligation during suspended receive-only drain.

### 5. OL08-C already separates send credentials from webhook verification secrets

A MailerSend webhook signing secret may remain temporarily available only in explicit receive-only use after outbound disablement. It must not authorize new outbound provider use.

Final signing-secret zeroization remains mandatory, but its expiry criterion/duration is not decided by OL09-B1.

## OL09-B1 — Accepted suspended webhook service boundary

### B1.1 Normal customer-facing mail webhook service stops

Once FAIR CRM has durable, trustworthy evidence that the organization is in the suspended closure path, normal customer-facing MailerSend webhook processing stops.

In suspended receive-only mode FAIR CRM must not continue, merely for the tenant's benefit:

- open/click analytics,
- ordinary sent/delivered/deferred/bounce provider-status progression,
- dashboard/engagement updates,
- customer activity generation,
- historical mail rescans,
- queue/job creation for dropped analytics events.

Suspension is not a 30-day extension of normal mail analytics service.

### B1.2 Minimum protective event set

The currently accepted minimum protective set is limited to the event classes that already have explicit consent-protection semantics in current FAIR CRM:

- `activity.unsubscribed`,
- `activity.spam_complaint`.

For these events suspended-mode handling may perform only the minimum tenant-scoped mutation necessary to preserve future communication safety:

- resolve the already-known mail-send operation/recipient relationship as needed,
- set the linked customer/contact `email_allowed = false` idempotently,
- retain only the minimum non-secret evidence needed to prove that the protective consent action occurred.

Suspended-mode handling must **not** create the normal CRM Activity record or other engagement/service output solely because that protective webhook arrived.

No other event is added to the protective set by inference. In particular, current hard-bounce handling only advances provider status; it does not currently implement a separate durable suppression rule, so OL09-B1 does not invent one.

A future additional suppression event requires an explicit accepted safety rule and corresponding tenant-isolation/idempotency evidence.

### B1.3 Fast-drop behavior for non-protective events

After signature/account validation and after a cheap local suspended-mode decision, non-protective events should be acknowledged successfully and dropped before normal operation lookup/status/analytics/CRM side effects wherever the accepted implementation can safely do so.

The drop path must be designed to avoid provider retries caused solely by FAIR CRM intentionally declining customer-facing processing.

The accepted target is:

```text
provider webhook
  -> parse + account/signature validation
  -> cheap local suspended receive-only gate
       -> non-protective event: 2xx / drop, no normal service work
       -> unsubscribe/spam complaint: minimum protective consent mutation only
```

Invalid signatures, unknown/deleted accounts and missing required signing-secret configuration continue to follow their security/error semantics; suspended mode is not a signature bypass.

### B1.4 Load / execution constraints

The suspended receive-only path must be low-cost by construction:

- no polling for webhook events,
- no scan of historical messages,
- no per-message timer,
- no per-tenant scheduled worker merely to decide whether an event should be dropped,
- no queue/job creation for dropped normal analytics events,
- no Core network round-trip on every webhook request,
- no customer-facing Activity creation for the two protective consent events,
- no provider-status write for intentionally dropped normal-service events.

The implementation should use one cheap organization/account-scoped local durable decision path suitable for indexing/caching while preserving fail-closed lifecycle semantics. The exact storage/contract shape is an engineering detail to be certified; local evidence must not be fabricated from an untrusted client flag.

### B1.5 Lifecycle correctness

Core remains canonical organization lifecycle authority. A local fast-path marker may only represent a Core-authoritative suspended episode through an accepted synchronization/orchestration path.

Current code has no webhook-specific suspension gate, and the existing Core product lifecycle snapshot does not itself provide an event push. OL09-B1 therefore does **not** authorize guessing suspension from arbitrary timestamps or client state.

Reactivation must make stale suspended-mode state incapable of permanently suppressing legitimate new active-organization webhook behavior. Any runtime slice must prove current-episode identity / stale-state handling and tenant isolation.

## OL09-B2 — Receive-only expiry / final signing-secret purge — OPEN

OL09-B1 does not select:

- an exact number of hours/days,
- the timestamp that starts the receive-only expiry clock,
- whether expiry is fixed-time, provider-evidence-based or hybrid,
- the final signing-secret purge scheduler/batch cadence,
- how unverifiable late provider events are evidenced after final purge.

The OL09-A 30-day closure grace must not be copied into OL09-B2 without a separate decision.

Until OL09-B2 is accepted, a required webhook signing secret may remain `receive_only_pending` under OL08-C but may not be declared finally purged merely because OL09-A grace elapsed.

## Authorized engineering boundary after OL09-B1 acceptance

After this decision is canonical, a bounded non-destructive runtime slice may implement/certify only:

- a trustworthy local suspended receive-only webhook gate tied to the current organization lifecycle/closure episode,
- fast successful drop of non-protective MailerSend events before normal tenant-facing provider-status/analytics work,
- minimum idempotent `email_allowed = false` handling for `activity.unsubscribed` and `activity.spam_complaint`,
- suppression of normal CRM Activity creation in that suspended protective path,
- non-secret minimal audit/evidence where needed,
- no per-webhook Core network request,
- tenant isolation, stale/reactivated-state, duplicate-event and load-oriented regression coverage.

This authorization does **not** include final webhook signing-secret purge or any time-based cleanup worker.

## Still gated

OL09-B1 does not authorize or complete:

- OL09-B2 expiry duration/final webhook-signing-secret purge,
- arbitrary MailerSend token deletion or supported-unidentifiable token success,
- product-data anonymization/hard delete,
- generated-artifact purge,
- closure-package materialization/expiry,
- audit/security evidence retention duration,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Decision summary

**A suspended organization no longer receives normal mail analytics/service from delayed MailerSend webhooks. FAIR CRM keeps only the smallest receive-only safety path needed for explicit unsubscribe/spam-consent protection, and intentionally dropped normal-service events must take a cheap successful fast path. The expiry duration and final signing-secret purge remain a separate OL09-B2 decision.**
