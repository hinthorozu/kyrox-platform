# P0.2 OL09-B — Runtime Acceptance

Status: **ACCEPTED**  
Date: **2026-09-09**  
Canonical source: GitHub `main`

## 1. Acceptance scope

This record closes the runtime implementation gate for the accepted OL09-B MailerSend webhook/signing-secret boundary.

The accepted policy remains:

- authoritative Kyrox Core `SUSPENDED` is the effective webhook security boundary;
- signing-secret post-suspension retention is **0 days**;
- there is no suspended receive-only/protective drain interval;
- signing-secret use becomes unauthorized at the suspension boundary even if physical zeroization requires retry;
- reactivation does not resurrect a zeroized signing secret;
- the separate OL09-A 30-day organization grace does not extend signing-secret retention.

## 2. Rollout-safe lifecycle episode contract

Merged Core PR: `hinthorozu/kyrox-core#28` — `feat(identity): expose lifecycle episode timestamp`.

- exact PR head: `8c7cbc9330662a079f11fd9ef42abcd68cee0fba`
- merged Core `main`: `816a27a6ce313878e0c3d53c4bbe6b513826b646`
- CI: `CI` run `34377917992` / run #109 — **SUCCESS**

Accepted behavior:

1. Core product lifecycle snapshots expose additive `updated_at` without changing existing lifecycle semantics.
2. `updated_at` identifies the current lifecycle episode used to distinguish a current suspension from a delayed/stale signal.
3. Active, suspended, deleted and unknown lifecycle behavior remains covered by the Core contract tests.

## 3. FAIR CRM consumer / zeroization boundary

Merged FAIR CRM PR: `hinthorozu/fair-crm#264` — `fix(closure): enforce OL09-B suspension secret zeroization`.

- exact PR head: `ed69e8b5e0460e76e0bfc37423f8bc93fcb89fa3`
- merged FAIR CRM `main`: `a8e3fc072ec64c12c44d304ca44cad1e07ac25cd`
- `Development Standard Gate` run `34379392721` / run #743 — **SUCCESS**
- `Prod-Path E2E` run `34379392719` / run #293 — **SUCCESS**

Accepted behavior:

1. FAIR exposes a purpose-separated authenticated internal suspension-security endpoint.
2. The signal credential fails closed when unset or invalid.
3. FAIR re-reads live Core lifecycle authority before mutating credentials.
4. A signal is mutation-authoritative only when Core is still `suspended` and Core `updated_at` matches the signaled lifecycle episode.
5. Delayed signals from an older suspension episode are acknowledged without touching current credentials.
6. Current MailerSend `webhook_signing_secret` values are zeroized idempotently.
7. The old `receive_only_pending` / `webhook_signing_secret_retained_for_drain` path is removed.
8. MailerSend `api_token` is not fabricated as revoked or deleted; the separate OL08-C2 `supported_unidentifiable` blocker remains intact.
9. Reactivation does not restore a previously zeroized signing secret.

## 4. Core suspension signal producer / delivery

Merged Core PR: `hinthorozu/kyrox-core#29` — `feat(identity): deliver OL09-B suspension security signal`.

- exact PR head: `1dd2335160c021729cbc28a89bb10caf28223def`
- merged Core `main`: `944b9896eb143c15fff0a119451576c2a7fb2d10`
- CI: `CI` run `34379699904` / run #111 — **SUCCESS**
- Backend CI lint: **SUCCESS**
- Backend CI tests: **SUCCESS**

Accepted behavior:

1. A successful Core suspension transaction durably enqueues `core.identity.organization_suspended` with the exact organization id and lifecycle `updated_at` episode.
2. Suspension state, lifecycle audit evidence and signal-job creation share the request database transaction; failure to persist the signal prevents a falsely successful committed suspension edge.
3. The signal uses an episode-scoped idempotency key.
4. Core uses a purpose-separated `FAIR_CRM_CORE_LIFECYCLE_SIGNAL_TOKEN`; no insecure production signal-secret default is accepted.
5. Delivery uses the FAIR internal lifecycle-security endpoint rather than per-webhook Core polling.
6. FAIR unavailability/non-200 delivery remains retryable through the durable jobs mechanism.
7. This security-critical job does not become permanently terminal merely because an ordinary attempt bound is exhausted.
8. Core's pending-job processing is wired to a continuous in-process dispatcher, so persisted delivery does not depend on a process restart.

## 5. Distributed-boundary semantics

OL09-B does not require an impossible cross-database atomic delete between Core and FAIR.

At the authoritative Core `SUSPENDED` transition:

- Core work eligibility becomes non-active immediately;
- the suspension transaction durably records the security-signal obligation;
- FAIR accepts only the matching live suspension episode;
- physical signing-secret zeroization is idempotent and retry-safe;
- a delayed signal cannot zeroize credentials created in a later reactivated/new lifecycle episode.

Therefore a transient FAIR outage can delay physical byte removal, but it does not create an accepted post-suspension authorization/drain interval. The zero-retention policy remains the security contract, and delivery continues until the current episode is safely reconciled or becomes stale because lifecycle authority moved on.

## 6. Acceptance result

The OL09-B implementation conditions are satisfied on canonical `main`:

- **additive lifecycle episode identity:** satisfied;
- **purpose-separated authenticated Core → FAIR signal:** satisfied;
- **durable/retry-safe suspension delivery:** satisfied;
- **stale-signal protection:** satisfied;
- **MailerSend signing-secret zeroization:** satisfied;
- **receive-only retention path removed:** satisfied;
- **MailerSend API-token blocker preserved:** satisfied;
- **exact-head CI evidence:** satisfied.

Therefore **P0.2 OL09-B webhook/signing-secret zero-retention is runtime-accepted**.

## 7. Operational prerequisite

This record accepts the merged runtime contract; it does not claim production deployment/configuration has already occurred.

Before enabling the producer in an environment, FAIR must run the accepted consumer version and Core/FAIR must be configured with the same purpose-separated `FAIR_CRM_CORE_LIFECYCLE_SIGNAL_TOKEN`. Missing/invalid configuration must remain fail-closed.
