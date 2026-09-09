# P0.2 OL08-C2 — Runtime Acceptance

**Status:** ACCEPTED  
**Date:** 2026-09-09  
**Canonical source:** GitHub `main`  
**Policy decision:** `ecosystem/P0_2_OL_08_C2_MAILERSEND_VERIFIABLE_INVALIDATION_DECISION.md`

## 1. Acceptance scope

This record closes the runtime implementation gate for the accepted OL08-C2 legacy/current-model MailerSend API-token reconciliation path.

The accepted security property is narrow and exact:

> FAIR CRM may declare a stored legacy MailerSend API token externally invalid only after MailerSend itself proves that the exact stored secret can no longer authenticate.

No heuristic provider-token targeting, guessed delete, operator-only override, local-delete-as-proof, or ambiguous provider result is accepted as success.

## 2. Canonical runtime implementation

Merged FAIR CRM PR: `hinthorozu/fair-crm#266` — `feat(closure): implement OL08-C2 MailerSend invalidation verification`.

- exact PR head: `9cdaed2a5df57a78446758d6db3f3afb38ee4d86`
- merged FAIR CRM `main`: `ca41d369727874dff5c5e70cda43828086ffa9a4`
- `Development Standard Gate` run `34392895839` / run #747 — **SUCCESS**
- `Prod-Path E2E` run `34392895803` / run #295 — **SUCCESS**

No schema migration or new persistent credential-state vocabulary was required. The implementation reuses the existing OL08-04A credential disposition state machine and adds a bounded verification/reconciliation path.

## 3. Exact-secret verification contract

The accepted runtime uses the exact locally stored MailerSend API token only to authenticate a non-mutating provider request.

Current implementation request class:

```text
GET https://api.mailersend.com/v1/token?limit=10
Authorization: Bearer <exact stored MailerSend API token>
```

The request is used for authentication verification, not token discovery.

Runtime classification is fail-closed:

| Provider result | Runtime meaning | Credential disposition |
| --- | --- | --- |
| HTTP `401` | exact stored secret is invalid | external invalidation confirmed |
| HTTP `200` | exact stored secret still authenticates | blocked |
| HTTP `403` | invalidity not proven | blocked |
| HTTP `429` | rate/quota ambiguity | unknown/blocked; retry later |
| HTTP `5xx` | provider result unavailable | unknown/blocked; retry later |
| transport/TLS/request failure | provider result unavailable | unknown/blocked; retry later |
| unexpected status | no accepted invalidity proof | unknown/blocked |

Only the definitive `401` branch advances to confirmed external invalidation.

## 4. Reconciliation and local zeroization

The runtime requires all of the following before verification can run:

- SYSTEM / Platform SuperAdmin closure authority,
- the target closure execution is open,
- live Kyrox Core lifecycle authority reports the organization as `SUSPENDED`,
- the disposition is the legacy MailerSend `supported_unidentifiable` credential class awaiting reconciliation,
- the exact local reusable API token is still available for verification.

If the exact token is already unavailable before accepted proof exists, the implementation fails closed rather than fabricating external invalidation.

For a non-`401` result:

- the disposition remains blocked,
- the exact local token remains stored because it is still required for later reconciliation,
- a bounded non-secret evidence code is recorded,
- a later reconciliation attempt may safely retry the non-mutating request.

For a definitive `401` result:

1. external invalidation is marked confirmed for that exact credential,
2. only then is the local MailerSend API token zeroized,
3. the existing disposition progresses through local send-secret purge to completion,
4. a repeated call after successful completion is idempotent and does not require another provider verification.

## 5. Evidence boundary

Durable evidence is deliberately bounded.

It may record identifiers, disposition state, attempt count/timestamps and provider-result classifications such as `mailersend_exact_secret_http_401`.

It does not persist:

- API-token plaintext,
- Authorization headers,
- secret hashes/fingerprints,
- MailerSend response bodies,
- sensitive provider response headers.

Operator assertion is not accepted success evidence. An operator may perform the required provider-side action for an unidentifiable legacy credential, but FAIR CRM advances only on the subsequent accepted exact-secret provider proof.

## 6. Relationship to OL09-B

MailerSend API-token reconciliation and webhook signing-secret handling remain separate credential obligations.

OL09-B has already removed post-suspension webhook-signing-secret authorization and established zero-day post-suspension signing-secret retention. OL08-C2 does not restore a receive-only drain period and does not alter the OL09-B ingress cutoff or stale-safe Core-to-FAIR zeroization signal.

The C2 verifier operates only on the MailerSend reusable API token needed for provider-side send credential reconciliation.

## 7. Acceptance result

The accepted OL08-C2 implementation requirements are satisfied on canonical `main`:

- **no guessed provider token id:** satisfied;
- **no automated heuristic delete:** satisfied;
- **operator assertion alone cannot complete invalidation:** satisfied;
- **non-mutating exact-secret verification:** satisfied;
- **only provider HTTP 401 confirms invalidity:** satisfied;
- **200/403 remain blocked:** satisfied;
- **429/5xx/transport/unexpected results fail closed:** satisfied;
- **retry/reconciliation preserves the exact secret until proof:** satisfied;
- **local reusable token zeroizes only after accepted proof:** satisfied;
- **secret/header/body/fingerprint exclusion from durable evidence:** satisfied;
- **SYSTEM + live Core SUSPENDED guards:** satisfied;
- **successful repeat is idempotent:** satisfied;
- **exact-head Development Standard Gate and Prod-Path E2E:** satisfied.

Therefore **P0.2 OL08-C2 legacy MailerSend verifiable invalidation is runtime-accepted**.

## 8. Residual operational boundary

Runtime acceptance does not claim that every deployed tenant credential has already been invalidated at MailerSend.

For a legacy `supported_unidentifiable` credential, the provider-side operator action remains an operational prerequisite. Until the exact stored secret produces accepted `401` proof, that credential remains blocked and closure cannot falsely treat the obligation as complete.

Future automated MailerSend token deletion remains separately constrained: it requires deterministic provider-token-id binding provenance and must not be inferred from token listings, names, dates, scopes or operator-entered unverified ids.
