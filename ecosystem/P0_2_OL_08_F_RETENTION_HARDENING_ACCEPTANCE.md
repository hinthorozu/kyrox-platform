# P0.2 OL-08-F — Retention Contract Hardening Acceptance

**Status:** HARDENING RUNTIME ACCEPTED / CERTIFIED  
**Accepted:** 2026-09-12  
**Base runtime acceptance:** `ecosystem/P0_2_OL_08_F_RUNTIME_ACCEPTANCE.md`  
**Retention policy authority:** `ecosystem/P0_2_OL_09_D_AUDIT_SECURITY_RETENTION_DECISION.md`

## Purpose

Record the final Kyrox Core hardening that aligns the already-accepted OL08-F retained-evidence runtime with the full OL09-D retention contract.

This document supplements, and does not replace, the OL08-F runtime acceptance for Core PR #31 and FAIR CRM PR #271. The authoritative retention clock remains unchanged:

```text
T_terminal = Core organization.deleted_at = FAIR closure_execution.closed_at
retention_deadline = T_terminal + 12 calendar months
```

## Accepted hardening boundary

Kyrox Core PR #32 adds the policy and minimization semantics required by OL09-D beyond the basic 12-month purge clock.

Accepted behavior:

- explicit retention policy version `ol09-d.v1`,
- terminal tombstone transaction minimizes retained Core audit history to bounded organization/closure control evidence,
- customer/business audit rows are removed from post-terminal retention scope,
- free-form JSON, IP-address and user-agent fields are stripped from retained pre-terminal control rows,
- the terminal minimization outcome is recorded as bounded retention-safe evidence,
- a deleted organization cannot accept new customer/business audit payloads,
- only retention-safe lifecycle/closure control audit actions remain writable after tombstone and their payload fields are stripped,
- the 12-month retained-audit purge endpoint requires the expected policy-version handshake,
- retry after prior purge supports verification-only `already purged` semantics so missing FAIR closure evidence cannot accidentally authorize a first destructive Core purge,
- the authoritative `deleted_at + 12 calendar months` clock, tenant isolation, idempotency and fail-closed preconditions remain unchanged,
- minimization and tombstone mutations share the same request-scoped database transaction,
- no migration is required.

## Security and evidence invariant

After terminal closure, Core retention is intentionally narrow. OL09-D does not authorize twelve months of arbitrary historical business payload simply because that payload once appeared in an audit row.

The accepted retained boundary is therefore:

- minimal,
- non-secret,
- organization-scoped,
- versioned,
- deterministic,
- sufficient for bounded lifecycle/closure audit and security proof,
- retry-safe without manufacturing a new destructive authorization path.

Reusable secrets, secret-derived fingerprints/oracles, customer/business payload bodies, free-form request metadata and unrelated product evidence are not promoted into the post-terminal retention set by this hardening.

## Relationship to FAIR CRM

FAIR CRM remains the owner of FAIR closure-orchestration evidence and continues to coordinate OL08-F through the accepted Core purge surface before deleting FAIR-owned retained evidence.

This Core hardening does not change FAIR's ownership boundary or its exact terminal clock. It strengthens the Core side of the cross-repository contract so that:

1. terminal minimization occurs atomically with the Core tombstone,
2. the retained Core evidence set is policy-versioned and bounded,
3. a later purge proves the expected policy version,
4. retries distinguish verification of an already-purged state from authorization of a first destructive purge.

## Exact runtime evidence

Kyrox Core PR #32:

- title: `fix(audit): align OL08-F runtime with OL09-D retention contract`,
- final head: `a154681ba454dad350b14b1418f31ab6146df55a`,
- Core CI #116 / run `34584149326`: **SUCCESS** on that exact head,
- squash merge: `0cc705ade76e565b1ea2d7672b2364abc432e047`,
- Core `main` verified at exactly `0cc705ade76e565b1ea2d7672b2364abc432e047` after merge.

The PR was based directly on the previously accepted Core PR #31 merge `bcfe46f5d85fea01adc3758dc4f7745d160a5f40`, so the hardening is an additive follow-up to the certified OL08-F runtime rather than a replacement implementation.

## Result

The OL08-F / OL09-D Core retention boundary is now fully hardened:

> **At terminal tombstone, Core atomically reduces retained organization audit history to a bounded, non-secret, versioned lifecycle/closure evidence set; after the exact 12-calendar-month deadline, purge remains tenant-scoped, fail-closed, deterministic and retry-safe, including verification-only handling of already-purged state.**

This closes the verified OL09-D retention-contract gaps discovered after the initial OL08-F runtime acceptance. It does not reopen OL08, change the terminal clock, or authorize any additional lifecycle runtime work.
