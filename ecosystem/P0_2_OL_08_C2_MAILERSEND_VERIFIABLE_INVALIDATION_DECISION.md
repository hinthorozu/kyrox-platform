# P0.2 OL-08C2 — MailerSend Legacy Token Verifiable Invalidation Decision

**Status:** ACCEPTED — OPERATOR ACTION + EXACT-SECRET INVALIDITY VERIFICATION  
**Accepted:** 2026-09-09  
**Parent credential decision:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`

## Purpose

Resolve the current-model MailerSend API-token closure blocker without guessing a provider `token_id`, deleting an arbitrary provider token, or accepting operator attestation as sufficient proof.

The existing OL08-C contract correctly classified current MailerSend credentials as blocked because FAIR CRM stores the reusable token secret but does not have a deterministic provider token identifier.

This decision adds a safe reconciliation path based on **proof that the exact stored secret is no longer accepted by MailerSend**.

## Verified provider facts

MailerSend's current public API provides:

- token listing through `GET /v1/token`,
- token lookup/update/delete through a provider `token_id`,
- token list/lookup responses containing token metadata and ids but not the original access-token secret,
- standard authentication semantics where HTTP `401 Unauthorized` means the provided API token is invalid,
- HTTP `403 Forbidden` means the request/action is denied for the account or token, including insufficient token permissions.

Therefore listing provider tokens cannot safely map a legacy FAIR CRM secret to one provider token id. Name, creation time, scopes or list position are insufficient exact-binding evidence.

At the same time, MailerSend can directly prove the liveness/non-liveness of the **exact secret FAIR CRM already stores** by authenticating a non-mutating API request with that secret.

## Accepted legacy invalidation path

For a legacy/current-model MailerSend credential whose exact provider token id is not deterministically bound:

```text
outbound disabled
  -> operator_required_provider_delete
  -> operator deletes intended token in MailerSend dashboard/provider control plane
  -> FAIR CRM verifies the exact stored secret against a non-mutating MailerSend endpoint
       -> definitive HTTP 401: exact stored secret invalid -> external invalidation confirmed
       -> HTTP 200 or 403: secret still authenticates / is not proven invalid -> remain blocked
       -> timeout/429/5xx/ambiguous response: unknown -> remain blocked and reconcile later
  -> local reusable token secret may then be zeroized under OL08-C3
```

The operator action is necessary for legacy credentials because FAIR CRM lacks a safe exact provider target.

The **operator assertion is not the success evidence**. Success comes from the subsequent provider response proving the exact stored secret is invalid.

## Verification request

The first implementation may use a non-mutating MailerSend token-list request such as:

```text
GET https://api.mailersend.com/v1/token?limit=10
Authorization: Bearer <stored exact MailerSend API token>
```

The purpose is authentication verification, not token discovery.

The response classification is:

| Result | Meaning | Closure result |
| --- | --- | --- |
| `401 Unauthorized` | MailerSend states the provided exact API token is invalid | **external invalidation confirmed** |
| `200 OK` | stored secret remains valid and request is allowed | **blocked — token still usable** |
| `403 Forbidden` | authentication was not proven invalid; account/token may lack permission or be restricted | **blocked — invalidation not confirmed** |
| `429` | rate/quota condition | **unknown/blocked; retry safely later** |
| `5xx`, timeout, connection/TLS failure | provider result unavailable/ambiguous | **unknown/blocked; reconcile later** |
| any unexpected status/body | no accepted proof of invalidity | **unknown/blocked** |

No request with side effects may be used merely to test token invalidity.

## Why `403` is not success

A `403` can mean the token is valid but lacks the required scope, or that account/provider policy denies the requested action.

Therefore `403` is deliberately treated as evidence that invalidity has **not** been established.

The system must not reinterpret suspension/account restrictions as token revocation.

## No guessed automated delete

This decision does not authorize FAIR CRM to:

- list tokens and choose one by name/date/scope similarity,
- delete the only returned token,
- trust an unverified user-entered provider token id,
- infer token identity from a domain id,
- delete a provider token merely because the local secret can authenticate the same MailerSend account.

A wrong automated `DELETE /v1/token/{token_id}` could revoke another credential and is therefore prohibited without deterministic target binding.

## Future deterministically identified tokens

Future MailerSend credential enrollment may support automated provider invalidation when FAIR CRM has durable proof binding the stored reusable secret to the provider token id.

Strong binding may be established when a trusted provider creation response produces the `token_id` and access token as one atomic enrollment result and FAIR CRM persists the non-secret provider id with provenance tied to that credential record.

Merely asking an operator/user to type a token id next to an independently copied secret is not equivalent proof.

For an accepted deterministically bound credential:

- automated provider delete/pause may use the exact id according to the accepted adapter contract,
- post-action exact-secret invalidity verification should still be used before declaring external invalidation complete where provider semantics permit it,
- local secret zeroization follows only after accepted provider invalidation evidence.

## Capability-state amendment

For current legacy MailerSend credentials, the prior `supported_unidentifiable` state remains accurate until an operator invalidation attempt occurs.

This decision supersedes only the prior rule that such a credential must remain permanently blocked because no automated exact `token_id` exists.

A bounded implementation may add a verified operator-reconciliation state such as:

```text
supported_unidentifiable
  -> operator_invalidation_required
  -> invalidation_verification_pending
  -> external_invalidated        only on definitive exact-secret 401 proof
```

Existing database enum/check/state names may be revised in the implementation slice as required. Policy meaning is authoritative over legacy naming.

No generic operator override is introduced. An operator can initiate/record the provider action, but cannot manually force `external_invalidated` without the accepted provider invalidity proof.

## Evidence contract

Durable non-secret evidence may record:

- organization id,
- closure execution id,
- email-account/credential identity,
- provider = MailerSend,
- capability/reconciliation state,
- verification endpoint class,
- HTTP classification (`401`, `403`, `429`, `5xx`, transport failure),
- attempt timestamps/count,
- final invalidation-confirmed timestamp,
- bounded reason/error code.

Evidence must not record:

- API token plaintext,
- Authorization header,
- secret hash/fingerprint,
- response headers/body containing sensitive account data beyond the bounded classification needed for proof.

Long-lived evidence remains subject to OL09-D.

## Local secret zeroization

The stored MailerSend API token remains a reusable local secret until OL08-C3 zeroization succeeds.

For the legacy operator-verification path:

- definitive provider `401` proof satisfies the external invalidation obligation for the exact stored secret,
- after that proof, local token zeroization is mandatory,
- local deletion before provider invalidity proof must not be used because it would destroy the exact credential needed for reconciliation,
- once local zeroization succeeds, later closure phases do not retain or reconstruct the token.

Webhook signing-secret handling remains separate and follows accepted OL09-B zero-post-suspension retention.

## Retry / ambiguity semantics

The verification request is non-mutating and may be retried safely after transport/5xx/429 uncertainty.

Rules:

- `401` is terminal success evidence for provider invalidity,
- `200`/`403` is terminal for that attempt but leaves the credential unresolved/alive,
- network/5xx/429 never fabricates success,
- retry uses the same stored secret until invalidity is proven or operator/system intervention changes the state,
- after external invalidation is confirmed and local secret zeroized, no further provider authentication verification is possible or required for that credential.

## Security properties

This path proves the property closure actually needs:

> the exact reusable MailerSend API secret stored by FAIR CRM can no longer authenticate to MailerSend.

It avoids the weaker and riskier question:

> which provider token-list row probably corresponds to this secret?

The policy therefore preserves fail-closed exactness without permanently blocking legacy credentials solely because historical provider ids were not stored.

## Explicitly not authorized

This decision does not authorize:

- guessed/heuristic provider token deletion,
- operator-only attestation as success,
- local secret purge before provider invalidity proof for this path,
- MailerSend account/domain deletion as a substitute,
- customer-facing credential-management authority,
- provider credential reconstruction,
- cleanup/tombstone while another required credential obligation remains blocked.

## Acceptance checklist

- [x] Legacy token id is not guessed from provider token listings.
- [x] Operator action alone cannot mark invalidation successful.
- [x] Exact stored secret is used only for a non-mutating liveness/invalidity verification request.
- [x] Definitive MailerSend HTTP 401 is accepted as proof that the exact token is invalid.
- [x] HTTP 200/403 does not satisfy invalidation.
- [x] 429/5xx/network ambiguity fails closed and is retryable.
- [x] Local secret is retained only until provider invalidity can be proven, then zeroized.
- [x] No plaintext/hash/fingerprint of the secret is retained as evidence.
- [x] Future automated deletion still requires deterministic provider-id binding provenance.
- [x] Webhook signing-secret lifecycle remains separate.

## Decision summary

**OL08-C2 resolves the legacy MailerSend exact-token targeting blocker without guessing a token id. For an unidentifiable legacy credential, an authorized operator performs the provider-side delete, then FAIR CRM authenticates a non-mutating MailerSend request with the exact stored secret. Only a definitive provider `401 Unauthorized` — documented by MailerSend as meaning the provided API token is invalid — confirms external invalidation. `200`/`403` means invalidity is not proven; rate-limit, server and transport failures remain blocked/unknown. After exact-secret invalidity is confirmed, the local reusable token is zeroized. Automated provider deletion remains prohibited until future credentials have deterministic token-id binding provenance.**
