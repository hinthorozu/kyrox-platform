# P0.2 OL-08-F — Retained Evidence Purge Runtime Acceptance

**Status:** RUNTIME ACCEPTED / CERTIFIED  
**Accepted:** 2026-09-11  
**Retention policy authority:** `ecosystem/P0_2_OL_09_D_AUDIT_SECURITY_RETENTION_DECISION.md`  
**Terminal clock authority:** `ecosystem/P0_2_OL_08_07_RUNTIME_ACCEPTANCE.md`  
**Parent tracker:** `ecosystem/P0_2_OL_08_IMPLEMENTATION.md`

## Purpose

Record cross-repository runtime acceptance for the post-terminal OL08-F retained-evidence purge implementation.

The accepted runtime consumes the already-certified terminal clock:

```text
T_terminal = Core organization.deleted_at = FAIR closure_execution.closed_at
retention_deadline = T_terminal + 12 calendar months
```

OL08-F is post-terminal retention maintenance. It does not move the terminal tombstone earlier, does not extend the package or product-data lifetimes, and does not create a second closure clock.

## Accepted ownership split

The runtime preserves repository ownership rather than treating retained evidence as one database concern.

Kyrox Core owns organization audit evidence. FAIR CRM owns its local closure-orchestration evidence graph. Each repository purges only the evidence it owns.

FAIR's coordinator is fail-closed across that boundary:

1. require Platform SuperAdmin / SYSTEM authority,
2. re-read authoritative Core lifecycle state,
3. require a durable Core tombstone with non-null `deleted_at`,
4. when local terminal closure evidence still exists, require exact `FAIR closed_at == Core deleted_at`,
5. compute the exact 12-calendar-month deadline from the authoritative terminal timestamp,
6. reject before that deadline,
7. purge Core-owned organization audit evidence first through the dedicated authenticated Core endpoint,
8. only after Core confirms the same terminal timestamp/deadline may FAIR purge its own local retained closure evidence.

A Core outage, invalid response, missing tombstone, premature deadline, terminal-clock mismatch or Core retention precondition failure leaves FAIR local retained evidence untouched.

## Accepted Kyrox Core runtime

Kyrox Core PR #31 adds the Core-owned audit-retention action.

Accepted behavior:

- the authoritative retention clock is the existing organization tombstone `deleted_at`,
- purge is forbidden until exactly 12 calendar months from that timestamp,
- organization audit rows are deleted by organization scope,
- later audit activity does not restart or extend the terminal retention clock,
- unknown or non-tombstoned organizations fail closed,
- the internal purge surface reuses the dedicated product-lifecycle credential,
- repeated purge after success is idempotent and converges with `purged_count = 0`,
- the purge operation does not append a new organization-scoped audit row that would manufacture a fresh retention tail,
- leap-day calendar semantics are deterministic.

Core runtime surface:

```text
POST /api/v1/organizations/{organization_id}/retained-audit-evidence/purge
```

The response carries the organization id, authoritative terminal tombstone timestamp, computed retention deadline and purged-row count so FAIR can verify cross-repository clock agreement before deleting local evidence.

## Accepted FAIR CRM runtime

FAIR CRM PR #271 adds the product-owned retained-evidence coordinator and explicit FK-safe local purge.

Accepted local evidence scope:

- closure credential events,
- closure credential dispositions,
- closure artifact inventory,
- closure packages,
- closure export plans,
- closure product-cleanup evidence,
- closure events,
- closure executions.

Accepted deletion order is explicit rather than delegated to cascade convenience:

```text
credential events
  -> credential dispositions
artifact inventory
  -> packages
  -> export plans
product-cleanup items
closure events
  -> closure executions
```

The implementation remains organization-scoped and preserves foreign-organization evidence.

## Evidence boundary preserved

OL08-F is intentionally limited to the accepted minimal closure/audit/security evidence boundary.

The runtime does **not** reinterpret unrelated retained data as OL08-F evidence. In particular:

- system-admin merge/reconstruction payload tables remain outside this purge,
- system data-operation reconstruction/output payloads remain outside this purge,
- full-database backups remain under OL10's independent 30-day ageing/pruning contract,
- already-deleted customer/product business payloads are not copied into retained evidence,
- reusable credentials/secrets are not retained by this policy,
- secret plaintext, secret hashes/fingerprints and secret-derived oracles are not introduced as retention evidence,
- closure-package bytes are governed by their separate OL09-E 30-day package lifecycle and are already terminally purged before OL08-07 tombstone completion.

This runtime does not create a new legal/security-hold mechanism or waive any separately accepted future hold policy. A separately accepted hold contract would need to gate destructive retention actions explicitly.

## Exact 12-calendar-month semantics

The retention deadline is calendar-based, not `365 days` and not a second relative timer from a later maintenance event.

Examples:

- `2026-09-11T10:00:00Z` -> `2027-09-11T10:00:00Z`,
- leap-day terminal timestamps clamp deterministically to the valid target calendar date.

The clock is never reset by:

- later Core audit writes,
- FAIR retry attempts,
- package download or purge time,
- OL08-F invocation time,
- the first successful Core purge,
- the first successful FAIR local purge.

## Restart and partial-failure semantics

The cross-repository operation is deliberately ordered for safe recovery.

If Core purge fails, FAIR local evidence is not deleted.

If Core purge succeeds but FAIR local deletion fails before commit, retry is safe because Core purge is idempotent. The next call revalidates the same authoritative terminal clock, Core returns zero or remaining owned audit rows as applicable, and FAIR may retry its local transaction.

After FAIR local evidence is fully gone, a repeated call can still derive the terminal timestamp from Core's durable organization tombstone and converges with zero local purge counts. Local evidence deletion therefore does not destroy the authority needed to prove that a repeat request is post-deadline.

## Authorization after terminal tombstone

The accepted runtime operates after the organization is already Core-tombstoned.

Core's Platform SuperAdmin path is DB-backed and independent from ordinary organization RBAC/lifecycle eligibility. FAIR therefore retains a SYSTEM-authorized maintenance path after tombstone without reactivating product work or treating the deleted organization as operationally active.

## Regression coverage

Core coverage includes:

- dedicated lifecycle credential enforcement,
- unknown/non-tombstoned rejection,
- pre-deadline rejection,
- exact-deadline success,
- deterministic leap-day calendar handling,
- organization isolation,
- later-audit non-extension,
- repeated idempotent purge.

FAIR coverage includes:

- pre-deadline fail-closed behavior,
- Core retention failure leaving local evidence untouched,
- Core/FAIR terminal-clock mismatch rejection,
- exact-deadline success,
- full retained FK graph purge in explicit dependency order,
- foreign-organization isolation,
- repeated idempotent convergence,
- leap-day calendar semantics,
- API registration.

## Exact runtime evidence

### Kyrox Core

Kyrox Core PR #31:

- final head: `041cfb0e9011012c0dd418ddf3b88cacbac09f0b`,
- CI #114 / run `34581214297`: **SUCCESS**,
- squash merge: `bcfe46f5d85fea01adc3758dc4f7745d160a5f40`.

The Core workflow is PR-triggered; no separate push run exists for the squash merge commit. The exact pre-merge head that became the squash content passed the repository CI gate before merge.

### FAIR CRM

FAIR CRM PR #271:

- final head: `9ba4886dda13713b0f0eb04e442aa1ca35f6d433`,
- Development Standard Gate #771 / run `34581693247`: **SUCCESS**,
- Prod-Path E2E #314 / run `34581693235`: **SUCCESS**,
- squash merge: `aa98ef0042217dfb11d3d49175bdb35fc33e76d1`,
- post-merge `main` Development Standard Gate #772 / run `34582662064`: **SUCCESS** on that exact merge commit.

Prod-Path #314 exercised FAIR against the newly merged Core runtime before FAIR merge and passed the real two-service gate.

## Explicitly not accepted by OL08-F

This acceptance does not authorize or certify:

- purge before the exact 12-calendar-month deadline,
- retention or re-creation of deleted customer/product payloads as evidence,
- retention of reusable secrets or secret-derived fingerprints/oracles,
- treating full backups as OL08-F evidence or changing OL10 backup ageing,
- purging global/shared platform evidence merely because an organization closed,
- remote provider deletion or any new credential lifecycle behavior,
- reopening, reactivating or otherwise making a tombstoned organization operational,
- `not_required` closure-export success without separate accepted policy authority.

## Result

OL08-F is runtime-covered across its actual ownership boundary:

> **Minimal retained Core audit evidence and FAIR closure evidence remain protected until exactly 12 calendar months from the authoritative Core terminal tombstone timestamp; after that deadline the SYSTEM-only, fail-closed, tenant-scoped and retry-safe purge converges without extending the clock or retaining deleted product/secret payloads.**

With OL08-F accepted, the retained-evidence purge obligation identified by OL09-D is no longer an open runtime gap.