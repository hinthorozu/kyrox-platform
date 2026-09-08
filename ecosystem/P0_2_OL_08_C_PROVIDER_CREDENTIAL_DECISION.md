# P0.2 OL-08C — Provider Credential Disposition Decision

**Status:** ACCEPTED — BOUNDED RUNTIME AUTHORIZATION  
**Accepted:** 2026-09-08  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`  
**Canonical lifecycle ADR:** `ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md`

## Purpose

Define the accepted provider/SMTP credential-disposition contract for organization closure without widening OL08 into product-data deletion, artifact deletion, retention/grace choice, backup policy or Core tombstone.

This decision accepts credential-only lifecycle semantics and authorizes a bounded first runtime slice. It does **not** authorize closure completion or any non-credential destructive phase.

## Verified FAIR CRM implementation facts

### 1. Email account identity and secret-bearing config are separate persisted records

`backend/app/modules/email_accounts/infrastructure/persistence/models.py` defines:

- `email_accounts` with organization ownership, `is_active` and `deleted_at`,
- `email_account_smtp_configs` with SMTP username/password,
- `email_account_provider_configs` with provider `config_json`.

The config rows use FK `ondelete="CASCADE"`, but current email-account deletion is a soft delete of the parent record. Normal deletion therefore does not physically remove config-row secret material.

### 2. Normal email-account delete is not a closure credential-disposition primitive

`DeleteEmailAccountUseCase` snapshots the response, calls `account.soft_delete()`, updates the account and records audit evidence. `soft_delete()` sets `deleted_at`, clears default and sets `is_active=False`; it does not delete SMTP/provider config rows or call an external provider.

Closure must not claim that current `DELETE /email-accounts/{id}` provides provider invalidation or local secret zeroization.

### 3. Stored secrets are encrypted, but still persist

SMTP password values and provider fields marked `secret=True` are encrypted at rest. Encryption is not closure-time zeroization: reusable credential material remains recoverable by the application until it is physically removed/blanked from secret-bearing storage.

### 4. MailerSend has distinct send and webhook secrets

The current MailerSend provider definition contains:

- `api_token` — required reusable secret used for outbound API authentication,
- `webhook_signing_secret` — optional secret used to verify inbound provider webhooks.

These have different lifecycle purposes and must not be treated as one undifferentiated purge step.

### 5. Inactive accounts intentionally remain webhook-readable

The repository webhook lookup does not require `is_active`; its explicit purpose is to allow delayed provider webhooks for previously sent messages. It does require `deleted_at IS NULL`.

MailerSend webhook processing loads the account and provider config, reads `webhook_signing_secret` and verifies the incoming signature before provider-status/consent processing.

Therefore:

- setting `is_active=False` can disable outbound account use while preserving receive-only webhook verification,
- setting `deleted_at` or removing the signing secret too early prevents delayed signed webhook processing,
- normal soft-delete is not the first closure credential step.

### 6. Current MailerSend adapter has no credential-management lifecycle API

`backend/app/modules/email_delivery/infrastructure/mailersend_adapter.py` implements outbound email send against `/v1/email`; it does not expose token-management operations.

MailerSend's current public API supports token status update/pause and token deletion through a provider `token_id`. FAIR CRM currently stores the token secret but not that provider token identifier. Existing credentials therefore cannot be declared deterministically revocable until targeting support exists.

Reference: `https://developers.mailersend.com/api/v1/account/tokens`.

### 7. Generic SMTP has no universal remote-revoke API

FAIR CRM SMTP configuration is host/port/username/password based and may target arbitrary SMTP infrastructure. Remote invalidation may mean password reset, application-password revocation, credential deletion, account disable or another provider-specific action.

Local secret disposition and provider-side invalidation are therefore separate obligations.

## Accepted OL08-C contract

OL08-C is decomposed into four concerns:

1. **outbound disablement**,
2. **external/provider-side invalidation**,
3. **local reusable-secret zeroization**,
4. **receive-only webhook drain and final signing-secret zeroization**.

No one concern may be used as evidence that another concern succeeded.

### OL08-C1 — outbound credential disablement — ACCEPTED

Once credential disposition begins for a closure execution:

- no new outbound use of organization-owned email credentials is permitted,
- outbound disablement occurs before credential destruction,
- receive-only webhook verification may remain available for provider events already in flight,
- normal email-account soft delete is not required for this step.

`outbound_disabled` is a durable credential-disposition state, not closure completion.

### OL08-C2 — provider-side invalidation — ACCEPTED

Provider-side invalidation is required whenever a deterministic supported capability exists for the exact reusable external credential.

Capability/evidence classes are:

- **supported_identifiable** — exact credential can be targeted through an accepted provider adapter/capability; invalidation is mandatory,
- **supported_unidentifiable** — provider supports invalidation but FAIR CRM cannot safely target the exact credential; execution must remain blocked until targeting support exists,
- **operator_required** — generic/provider-specific infrastructure requires an explicit external/operator action whose evidence can be recorded, but FAIR CRM has no deterministic management adapter,
- **not_applicable** — only when there is demonstrably no reusable external credential or no external invalidation obligation for that credential class.

Rules:

- local zeroization never counts as provider-side invalidation,
- `supported_unidentifiable` cannot be downgraded to `not_applicable`,
- no generic operator override may fabricate success for a supported-but-unidentifiable managed-provider credential,
- provider/operator evidence must be non-secret, durable and tied to organization + closure execution + credential/account identity,
- MailerSend token invalidation requires a deterministic provider `token_id` targeting strategy before automated success can be claimed.

For generic SMTP, remote invalidation is not assumed merely because the local password was removed. If external invalidation is required but cannot be automated, the disposition remains `operator_required` until explicit non-secret evidence is recorded.

### OL08-C3 — local reusable-secret zeroization — ACCEPTED

Before the relevant send-credential disposition can be complete, reusable local send secrets must become unrecoverable from FAIR CRM secret-bearing config storage.

Required classes include, where present:

- SMTP passwords,
- MailerSend/API provider tokens,
- other provider reusable authentication secrets.

Rules:

- inactive/soft-deleted account state is insufficient,
- encrypted-at-rest secret text is insufficient,
- evidence records credential class, account/credential identifier, outcome, timestamps and reason codes only,
- audit/evidence must never contain plaintext/decrypted secrets,
- secret hashes/fingerprints must not be persisted as a credential oracle.

Webhook verification secrets are handled separately under OL08-C4.

### OL08-C4 — receive-only webhook drain — ACCEPTED ORDERING / FINAL PURGE GATED BY DRAIN CRITERION

After outbound disablement, a provider webhook signing secret may remain temporarily recoverable only for receive-only verification of delayed events that belong to previously handed-off work.

During `receive_only_pending`:

- no new outbound provider handoff is permitted,
- the account must remain non-deleted if current webhook lookup requires it,
- the signing secret may be used only for inbound signature verification,
- this state is not credential-disposition completion.

The final signing-secret zeroization is mandatory before OL08-C can be fully complete.

If the drain criterion requires elapsed time, **the duration is not chosen by OL08-C** and remains gated by OL-09. OL08-C authorizes the ordering/state model but does not invent hours/days.

## Accepted state model

Credential disposition evidence is separate from the existing email-account lifecycle:

```text
pending
  -> outbound_disabled
  -> external_invalidation_pending
       -> external_invalidated
       -> operator_required
       -> blocked_supported_unidentifiable
  -> local_send_secrets_purged
  -> receive_only_pending        (only if a signing secret must remain)
  -> webhook_secret_purged
  -> disposition_complete

any unresolved required step -> blocked with durable non-secret evidence
```

A credential with no receive-only requirement may move from `local_send_secrets_purged` directly to `disposition_complete` only after all required external-invalidation obligations are satisfied.

Important invariants:

- `outbound_disabled` is not credential destruction,
- `external_invalidated` requires provider/operator evidence appropriate to the capability class,
- `local_send_secrets_purged` does not imply webhook signing-secret purge,
- `receive_only_pending` cannot authorize outbound use,
- `disposition_complete` applies only to credential disposition and does not imply export delivery, product-data cleanup, artifact cleanup, retention completion, backup reconciliation or tombstone readiness.

## Retry / uncertain-result semantics — ACCEPTED

Provider-side invalidation is an external side effect and must be fail-closed.

- pre-handoff/connect failures may be retried according to provider-specific safe policy,
- once an invalidation request may have reached the provider, an ambiguous result becomes durable `external_invalidation_unknown`/blocked evidence,
- ambiguous invalidation must not be blindly auto-retried if duplicate/repeated calls could have unsafe or misleading semantics,
- provider-specific reconciliation may resolve the ambiguity only through deterministic evidence,
- for an identifier previously validated as the exact credential, a provider lookup proving the credential is absent/inactive may satisfy reconciliation,
- otherwise operator/system intervention is required; success must not be fabricated from timeout/error alone.

## Authorized engineering slice after this acceptance

After this decision is merged, **OL08-04A — credential disposition state/evidence foundation** is authorized.

OL08-04A may implement:

- durable organization + closure-execution + email-account/credential disposition identity,
- credential capability classification,
- SYSTEM-only status/start/retry/reconcile surfaces,
- live Core `SUSPENDED` fail-closed precondition where mutation starts/retries,
- outbound-disabled evidence/state integration without deleting the email account,
- provider capability interface and deterministic MailerSend token-target metadata/support,
- local **send-secret** zeroization only after required external invalidation evidence is satisfied,
- receive-only signing-secret state without final time-based purge,
- append-only non-secret audit evidence,
- tenant-isolation, idempotency, failure/restart and uncertain-result tests.

The first runtime slice must **not** declare full OL08-C completion while a signing secret remains in `receive_only_pending`.

## Still gated

This acceptance does **not** authorize:

- arbitrary MailerSend token deletion without deterministic exact-token targeting,
- blind provider invalidation retries after ambiguous handoff,
- treating local secret purge as remote revoke success,
- final webhook signing-secret purge before its accepted drain criterion,
- inventing a webhook drain duration; time-based policy remains OL-09,
- normal email-account soft delete as credential-disposition completion,
- persistent/downloadable closure package materialization,
- `not_required` export success without an accepted policy source,
- product-data anonymization/hard delete — OL08-D,
- generated artifact purge — OL08-E,
- audit/security evidence retention duration — OL08-F / OL-09,
- backup ageing/restore reconciliation — OL08-G / OL-10,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

## Decision summary

The accepted policy is **disable outbound first, invalidate externally where required, zeroize local reusable send secrets, preserve signing-secret receive-only capability only while explicitly required, and fail closed on unsupported/ambiguous evidence**.

OL08-C is accepted as a credential-disposition contract. Full credential-disposition completion remains dependent on a valid receive-only drain criterion when a webhook signing secret exists; if that criterion is time-based, OL-09 must decide the duration before final signing-secret purge can be certified.
