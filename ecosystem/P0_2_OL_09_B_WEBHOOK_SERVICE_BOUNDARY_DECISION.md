# P0.2 OL-09B — Suspended Webhook Cutoff / Signing-Secret Decision

**Status:** ACCEPTED — ZERO-RETENTION WEBHOOK CUTOFF AT `SUSPENDED`  
**Accepted:** 2026-09-08  
**Parent readiness:** `ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`  
**Related credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`  
**Related grace decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`

## Purpose

Define the final FAIR CRM MailerSend webhook boundary when an organization enters authoritative Core `SUSPENDED`, including the lifecycle of the webhook signing secret.

This decision supersedes the earlier partial OL09-B1 shape that allowed a protected receive-only webhook set while suspended. Under the final accepted policy there is **no suspended receive-only retention window**.

## Decision

The successful authoritative Core transition into the current `SUSPENDED` episode is simultaneously:

1. the end of normal tenant-facing MailerSend webhook processing,
2. the end of protective MailerSend webhook processing,
3. the effective expiry boundary of the MailerSend webhook signing secret.

The accepted drain duration is therefore:

```text
webhook signing-secret retention after SUSPENDED = 0 days
```

There is no `SUSPENDED + N days` webhook-drain clock and no provider-terminal-event criterion.

The separate OL09-A 30-day reversible organization closure grace remains unchanged. That grace does **not** extend webhook verification or signing-secret retention.

## Exact lifecycle semantics

The boundary is the successful authoritative Core transition into `SUSPENDED` for the current suspension episode.

Not authoritative for this decision:

- FAIR CRM closure-execution creation time,
- first webhook received after suspension,
- first time FAIR CRM happens to observe `SUSPENDED`,
- worker start time,
- operator-entered time,
- OL09-A grace expiry.

No deadline arithmetic is required for OL09-B. The policy is immediate at the suspension boundary.

## Signing-secret semantics

From the authoritative `SUSPENDED` boundary onward:

- the webhook signing secret is no longer authorized for inbound verification,
- the signing secret must be irreversibly zeroized from FAIR CRM secret-bearing storage through the accepted credential-disposition path,
- no new `receive_only_pending` retention window is created for that suspension episode,
- physical purge must be idempotent and retry-safe,
- a purge failure must remain durably blocked/visible and must never re-authorize use of the secret.

Because Core and FAIR CRM are separate runtime boundaries, this policy does not claim impossible cross-service same-millisecond transactional deletion. It defines the **effective security/lifecycle boundary** at the successful Core `SUSPENDED` transition: even if physical zeroization is still retrying because of process or infrastructure failure, the retained bytes are not authorized for webhook processing.

This is what "simultaneous with suspension" means in the contract: **no additional retention period starts after suspension**. The security boundary is immediate; physical persistence cleanup must converge to that decision without creating a temporary service allowance.

## Webhook behavior while suspended

After the authoritative `SUSPENDED` transition, no MailerSend webhook event may mutate tenant state.

This includes all currently recognized events:

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

Therefore the earlier partial-B1 suspended protective exception for `activity.unsubscribed`, `activity.spam_complaint`, and `activity.hard_bounced` is superseded by this final decision.

While suspended, webhook ingress must not:

- update provider status,
- mutate communication consent/suppression state,
- create CRM activities,
- update engagement/dashboard metrics,
- enqueue replay/background work for the event,
- create a backlog for later reactivation,
- use a retained signing secret merely because physical purge has not yet completed.

The exact HTTP acknowledgement/rejection shape for post-suspension provider deliveries is an implementation detail. Whatever response policy is later implemented, post-suspension requests must be inert with respect to tenant state and must not regain authority from a secret whose effective lifetime has ended.

## Reactivation semantics

OL09-A continues to permit `SUSPENDED -> ACTIVE` during the accepted 30-day reversible closure grace under the existing lifecycle authority.

Reactivation does **not** resurrect the deleted webhook signing secret and does not backfill webhook events ignored during suspension.

Before MailerSend webhook processing can resume after reactivation, a valid webhook verification configuration/signing secret must exist again through an accepted credential/configuration path. Reactivation alone must not reconstruct, restore, or infer previously zeroized secret material.

## Performance / load contract

Zero-retention removes the need for a suspended receive-only drain worker, drain timer, provider-terminal scan, historical-message scan, replay backlog, per-message timer, or per-tenant polling loop.

Required properties remain:

- no scan of previously sent mail,
- no backfill of suspended-period analytics,
- no steady-state per-webhook Core network round-trip merely to preserve a receive-only mode,
- deterministic lifecycle signal/orchestration for the `SUSPENDED` boundary,
- idempotent retry of physical secret purge when infrastructure failure prevents immediate completion.

## Lifecycle authority / implementation gate

Core remains the authoritative lifecycle owner. FAIR CRM must not fabricate suspension from local timestamps or operator input.

A bounded runtime implementation must therefore obtain a deterministic, fail-closed signal/evidence of the authoritative `SUSPENDED` transition. That mechanism is an implementation requirement; it does not change the accepted zero-retention policy.

If authoritative suspension evidence is missing or ambiguous, the system must not fabricate a destructive timestamp. Existing/pre-policy suspended organizations without verifiable authoritative suspension evidence remain blocked until a deterministic Core-authoritative path exists.

## Relationship to OL08-C4

OL08-C4 allows a signing secret to remain temporarily recoverable **only while an explicitly accepted receive-only requirement exists**.

OL09-B now decides that no such requirement exists after authoritative Core `SUSPENDED`.

Therefore, for this policy:

```text
Core -> SUSPENDED
  -> webhook verification authority ends
  -> webhook signing secret purge required
  -> no receive_only_pending retention interval
```

Final signing-secret purge remains credential-disposition work only. It does not by itself prove provider-token invalidation, product-data cleanup, artifact cleanup, audit-retention completion, backup reconciliation, `cleanup_complete`, tombstone readiness, or Core deletion.

## Explicitly not authorized

This decision does not authorize:

- MailerSend token revoke success for an unidentifiable token,
- product-data anonymization or hard delete,
- generated-artifact deletion,
- closure-package expiry,
- audit/security evidence retention duration,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone,
- restoration of a purged signing secret during reactivation.

## Decision summary

**OL09-B is accepted with zero post-suspension signing-secret retention. The successful authoritative Core transition into `SUSPENDED` is the effective cutoff for all MailerSend webhook processing and for authorization to use the webhook signing secret. The secret must be zeroized through an idempotent fail-closed credential-disposition path; there is no 30-day webhook drain, no protective suspended-event exception, and no provider-terminal criterion. OL09-A's separate 30-day reversible organization grace remains unchanged.**
