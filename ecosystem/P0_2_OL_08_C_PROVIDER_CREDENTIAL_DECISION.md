# P0.2 OL-08C — Provider Credential Disposition Decision Readiness

**Status:** PROPOSED / READINESS ONLY — NOT ACCEPTED  
**Date:** 2026-09-08  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Canonical lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Purpose

Define the decision boundary for provider/SMTP credential handling during organization closure without authorizing any provider revoke, credential rotation, local secret purge, data deletion, artifact deletion or Core tombstone.

This document records current implementation facts, the security/sequencing constraints those facts create, and the policy questions that must be accepted before OL08-C runtime work may begin.

## Current FAIR CRM implementation facts

### 1. Email account identity and secret-bearing config are separate persisted records

`backend/app/modules/email_accounts/infrastructure/persistence/models.py` defines:

- `email_accounts` with organization ownership, `is_active` and `deleted_at`,
- `email_account_smtp_configs` with SMTP username/password,
- `email_account_provider_configs` with provider `config_json`.

The config rows use FK `ondelete="CASCADE"`, but current email-account deletion is a soft delete of the parent record, not a physical parent delete. Therefore normal deletion does not imply physical removal of config-row secret material.

### 2. Current normal email-account delete is not a closure credential-disposition primitive

`DeleteEmailAccountUseCase` snapshots the response, calls `account.soft_delete()`, updates the account and records audit evidence. `soft_delete()` sets `deleted_at`, clears default and sets `is_active=False`; it does not delete SMTP/provider config rows or call an external provider.

Closure must therefore not claim that current `DELETE /email-accounts/{id}` provides provider revoke or local secret purge.

### 3. Stored secrets are encrypted, but still persist

SMTP password values and provider fields marked `secret=True` are stored using FAIR CRM secret encryption. Encryption-at-rest is not equivalent to closure-time zeroization: encrypted credential material remains reusable while the application can decrypt it.

### 4. Current MailerSend provider credentials contain two different security functions

The current MailerSend provider definition contains:

- `api_token` — required secret used for outbound API authentication,
- `webhook_signing_secret` — optional secret used to verify inbound provider webhooks.

These cannot safely be treated as one undifferentiated purge operation.

### 5. Inactive accounts may intentionally remain webhook-readable

The repository webhook lookup does not require `is_active`; its explicit purpose is to allow delayed provider webhooks for previously sent messages. It does require `deleted_at IS NULL`.

MailerSend webhook processing loads the account, loads the provider config, reads `webhook_signing_secret` and verifies the incoming signature before provider-status/consent processing.

Therefore:

- setting `is_active=False` can stop normal sending eligibility while preserving receive-only webhook verification,
- setting `deleted_at` or purging the signing secret too early makes delayed webhook processing impossible,
- the normal soft-delete path is not suitable as the first closure credential step.

### 6. Current MailerSend adapter has no credential-management lifecycle API

`backend/app/modules/email_delivery/infrastructure/mailersend_adapter.py` implements the outbound email send boundary against `/v1/email`. It does not expose token pause/delete/revoke operations.

MailerSend's current public API supports token pause/update and token deletion by `token_id`, but FAIR CRM's current provider config stores the token secret and not the provider token identifier. Automated external invalidation therefore cannot be assumed from the current model.

### 7. Generic SMTP cannot have one universal provider-side revoke contract

FAIR CRM SMTP configuration is host/port/username/password based and may target arbitrary SMTP infrastructure. Provider-side invalidation semantics vary by provider: password reset, credential deletion, account disable, application-password revocation or no remotely manageable credential lifecycle at all.

OL08-C must distinguish local secret disposition from external/provider-side invalidation capability.

## Required decision decomposition

OL08-C should be decided as four separate concerns.

### OL08-C1 — outbound credential disablement

Question: what must happen immediately once closure credential disposition begins?

Proposed invariant:

- no new outbound use of any organization-owned email credential may be allowed,
- this must not rely on physical secret deletion as the first step,
- receive-only webhook processing may remain possible where required by accepted policy.

This proposal does not choose a new lifecycle duration or grace window.

### OL08-C2 — provider-side credential invalidation

Question: when is remote revoke/pause/delete required, and what is the success evidence?

Decision must distinguish:

- **supported + identifiable** — FAIR CRM has an explicit provider capability and sufficient provider-side identifier/auth to invalidate the credential,
- **supported but not currently identifiable** — provider supports invalidation but current FAIR CRM data is insufficient to target the exact credential,
- **unsupported / provider-agnostic** — no reliable remote invalidation contract exists,
- **not applicable** — credential is local-only or there is no reusable external credential.

A local delete/zeroization must never be recorded as evidence that external invalidation succeeded.

For MailerSend specifically, current API capabilities make provider-side token invalidation technically possible, but the existing FAIR CRM credential record does not persist `token_id`; an implementation needs an explicit targeting strategy before it can claim deterministic automatic revocation.

### OL08-C3 — local secret zeroization

Question: which locally persisted secrets must become unrecoverable, and at what point?

Candidate mandatory classes:

- SMTP passwords,
- MailerSend/API provider tokens,
- provider reusable authentication secrets,
- webhook verification secrets after their receive-only purpose is complete.

Local zeroization evidence must be secret-free. Audit/events must record identifiers, credential class, outcome, timestamps and reason codes — never plaintext/decrypted secrets or secret hashes that could become a credential oracle.

### OL08-C4 — webhook receive-only drain

Question: when may webhook verification secrets be removed?

Current code requires a live non-deleted account and signing secret to verify delayed MailerSend events. A safe contract therefore needs an explicit receive-only phase or an equivalent accepted rule.

The exact time-based drain/retention duration is **not** decided here and remains coupled to OL-09 if a duration is required. OL08-C may define ordering and state semantics without inventing a number of hours/days.

## Candidate disposition state model

Readiness recommendation only — not accepted runtime:

```text
pending
  -> outbound_disabled
  -> external_invalidation_pending | external_invalidation_not_applicable
  -> receive_only_pending           (only where delayed signed provider events matter)
  -> local_secrets_purged
  -> disposition_complete

failure at any required step -> blocked with durable non-secret evidence
```

Important constraints:

- `outbound_disabled` is not credential destruction,
- `external_invalidation_not_applicable` must not be used to hide a supported-but-unimplemented provider capability,
- `receive_only_pending` cannot authorize new outbound provider handoff,
- `local_secrets_purged` cannot be declared while any required reusable local secret remains recoverable,
- `disposition_complete` must not imply product-data cleanup, artifact cleanup, export delivery, retention completion or tombstone readiness.

## Recommended acceptance direction

The safest bounded direction for OL08-C is:

1. **Separate outbound disable, external invalidation and local zeroization.**
2. **Treat webhook signing secrets separately from send credentials** so delayed signed events can be processed in a receive-only state until an accepted drain criterion is satisfied.
3. **Require provider-capability evidence.** Automatic remote invalidation is mandatory only when an accepted adapter capability can target the exact credential deterministically; otherwise the execution must remain explicitly unresolved/blocked or require separately accepted operator evidence rather than fabricating success.
4. **Require local secret zeroization before OL08-C completion**, except for a signing secret that is still in an accepted receive-only phase.
5. **Do not reuse normal email-account soft delete as closure completion evidence.** Closure needs separate durable disposition evidence tied to organization + closure execution + credential/account.
6. **Keep OL08-C non-destructive outside credential material.** No customer/product data, generated artifact, export package, audit history or Core organization record is deleted by this slice.

## Decisions still required before runtime authorization

The acceptance PR must explicitly answer:

1. Is provider-side invalidation required whenever a deterministic provider capability exists?
2. For provider capabilities that exist but current FAIR CRM lacks a stable provider credential identifier, must closure block until identifier/management support is added, or may operator evidence satisfy the requirement?
3. What evidence is accepted for generic SMTP providers where remote invalidation cannot be standardized?
4. Is receive-only webhook verification required after outbound disablement, and what event/drain condition ends it?
5. If the drain condition requires elapsed time, is that choice deferred to OL-09 rather than invented in OL08-C?
6. Must local reusable secrets be physically removed/zeroized from config storage rather than merely making the account inactive/soft-deleted?
7. What retry/idempotency semantics apply when provider-side invalidation has an uncertain result?

## Explicit non-goals / prohibitions

This readiness document does **not** authorize:

- MailerSend token pause/delete,
- SMTP password reset/rotation,
- any provider-management API call,
- deletion or blanking of stored SMTP/provider secrets,
- email-account closure soft delete as an OL08-C phase,
- persistent/downloadable closure package materialization,
- `not_required` export success,
- product-data anonymization/hard delete,
- generated artifact purge,
- retention/grace duration selection,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Engineering gate after acceptance

Only after a separate OL08-C acceptance change may implementation begin. Any authorized runtime should start with a bounded, credential-only disposition state/evidence layer and provider capability interface; destructive product-data/artifact phases remain separately gated under OL08-D/E and OL-09/10.
