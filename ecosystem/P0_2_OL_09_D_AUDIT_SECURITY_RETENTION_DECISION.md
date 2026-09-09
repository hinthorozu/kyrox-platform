# P0.2 OL-09D — Audit / Security Evidence Retention Decision

**Status:** ACCEPTED — 12-MONTH MINIMAL NON-SECRET EVIDENCE RETENTION  
**Accepted:** 2026-09-09  
**Parent readiness:** `ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md`  
**Related grace decision:** `ecosystem/P0_2_OL_09_A_CLOSURE_GRACE_DECISION.md`  
**Related credential contract:** `ecosystem/P0_2_OL_08_C_PROVIDER_CREDENTIAL_DECISION.md`

## Purpose

Define how long FAIR CRM retains the minimum non-secret control/security evidence needed to prove organization closure actions after the closure has reached a separately accepted durable terminal milestone.

This decision is intentionally separate from customer/product-data retention. It does not authorize keeping customer records, message contents, uploaded/generated files, reusable credentials or raw provider payloads merely because they may be useful for audit.

## Decision

FAIR CRM retains eligible closure/audit/security evidence for **12 months** after the closure reaches a separately accepted durable terminal closure milestone.

There is no additional indefinite retention by default.

The retention rule is:

```text
organization closure in progress
  -> required minimal non-secret control/security evidence retained

separately accepted durable terminal closure milestone reached
  -> audit_retention_started_at = terminal closure evidence timestamp
  -> retain eligible evidence for 12 months

12 months elapsed
  -> evidence becomes eligible for purge or irreversible de-identification
     according to the accepted evidence-disposition implementation
```

The 12-month clock does **not** start from:

- the Core `SUSPENDED` transition,
- the beginning or end of the 30-day OL09-A grace,
- closure-execution creation,
- worker start time,
- first observation of lifecycle state,
- UI/operator-entered time.

If no separately accepted durable terminal closure milestone/timestamp exists yet, the 12-month retention clock has not started and the evidence remains retained.

## Evidence covered

The policy applies only to minimum non-secret closure/control/security evidence that is necessary to prove what the system did and whether required closure obligations succeeded, failed or remained blocked.

Eligible evidence may include, where applicable:

- closure execution identity/state/event evidence,
- authoritative lifecycle/suspension episode references used by closure policy,
- export completeness/disposition evidence,
- credential-disposition outcome evidence,
- provider/operator external invalidation outcome evidence,
- local secret-zeroization outcome evidence,
- irreversible product-data disposition outcome evidence once OL08-D is accepted and implemented,
- generated-artifact/package disposition outcome evidence once those phases are accepted,
- cleanup/tombstone evidence only if those later phases are separately accepted.

Evidence should be bounded to fields such as identifiers, reason/status codes, policy/schema versions, timestamps, actor/authority class and non-secret outcome metadata.

## Explicitly excluded from audit retention

This policy does not authorize retention of:

- API tokens,
- webhook signing secrets,
- SMTP passwords,
- decrypted or reusable credential material,
- credential hashes/fingerprints that could become a verification oracle,
- customer/contact product records merely for audit convenience,
- email/message bodies,
- raw provider webhook payloads or signatures,
- uploaded/generated binary artifacts,
- closure export-package content,
- system backups.

Those remain governed by their own product-data, credential, artifact/package or backup policies.

## Relationship to OL09-A and OL09-C

OL09-A and OL09-C remain independent:

```text
Core -> SUSPENDED
  -> 30-day reversible grace
  -> OL08-D classes later accepted as anonymize/hard_delete may become time-eligible
  -> closure continues until every separately accepted required obligation is satisfied
  -> terminal closure milestone
  -> 12-month OL09-D evidence retention starts
```

Therefore OL09-D is **not** `SUSPENDED + 12 months` and is **not** `30-day grace + 12 months` by arithmetic alone.

A closure that remains blocked for months does not consume its post-closure evidence-retention period while still unresolved.

## Retention expiry semantics

At or after 12 months from the authoritative terminal closure evidence timestamp, eligible evidence may be purged or irreversibly de-identified only through a separately implemented deterministic retention action.

Requirements:

- exact UTC timestamp comparison,
- explicit retention-policy version,
- deterministic organization + closure-execution identity,
- idempotent/restart-safe execution,
- no secret or customer payload copied into retention evidence before deletion,
- legal/security hold or other separately accepted exception must fail closed and be explicit; runtime must not invent ad-hoc extensions,
- process downtime does not reset or extend the deadline,
- expiry does not authorize backup mutation; backup ageing/restore remains OL-10.

## Pre-existing closures

A historical closure must not receive a fabricated retention deadline from suspension time, record creation time or first observation time if a trustworthy terminal closure timestamp cannot be established.

Such evidence remains retained until a deterministic accepted terminal timestamp/evidence path exists.

## Runtime boundary

This decision accepts the retention policy only. It does not by itself authorize:

- a purge scheduler/worker,
- deletion/anonymization of product data,
- deletion of generated artifacts or closure packages,
- backup deletion,
- `cleanup_complete` / `ready_for_tombstone`,
- Core organization delete/tombstone.

A later bounded implementation must prove the exact evidence classes, terminal clock source, expiry calculation, purge/de-identification behavior, tenant isolation, restart behavior and audit-without-secrets invariant before destructive evidence cleanup is certified.

## Decision summary

**OL09-D is accepted: retain only minimal non-secret closure/audit/security evidence, start its post-closure retention clock at a separately accepted durable terminal closure milestone, retain it for 12 months, then make that evidence eligible for deterministic purge or irreversible de-identification. Customer/product data, credentials, message content, artifacts and backups are outside this 12-month policy.**
