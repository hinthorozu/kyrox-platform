# P0.2 OL-10 — Backup Ageing / Restore Reconciliation Decision

Status: **ACCEPTED**  
Date: **2026-09-09**  
Canonical source: GitHub `main`

## 1. Scope

OL-10 closes the policy gap left explicitly open by OL08-G and OL09: an older FAIR CRM full-database backup can contain organization-scoped data that has since passed through suspension/closure and destructive product-data disposition.

This decision defines:

1. the maximum age of a restorable FAIR CRM database backup,
2. the authoritative lifecycle source required after restore,
3. fail-closed behavior when restored tenant data disagrees with or cannot be reconciled against current authority,
4. the implementation gates required before a restore may be certified complete.

This decision does **not** weaken or replace OL08-D/E/C2 or OL09-A/B/C/D/E.

## 2. Verified current runtime

### FAIR CRM backup / restore

Current `fair-crm/main` uses PostgreSQL custom-format full database dumps (`pg_dump -Fc`). Restore uses `pg_restore` with `--clean --if-exists --single-transaction --no-owner --no-acl --exit-on-error`.

The current restore maintenance runner executes, in order:

1. dump verification,
2. database connection disposal,
3. destructive full-database restore,
4. Alembic upgrade to head,
5. generic post-restore health checks,
6. restore-job completion.

The generic health check verifies connectivity, expected critical tables and row counts. It does **not** reconcile organization lifecycle against Kyrox Core.

Restore is configurable and currently defaults enabled. There is no backup maximum-age/retention configuration and no automatic backup-pruning runtime. Backup deletion is manual.

`SystemBackup` already records `completed_at`, which is the appropriate timestamp for ageing a successfully created recovery artifact. Downloading or restoring a backup does not create a new backup and therefore must not reset its age.

### Core organization lifecycle / deletion

Current `kyrox-core/main` is the canonical organization lifecycle authority. Product runtimes can query the token-protected lifecycle snapshot endpoint.

Current Core deletion is a soft delete: the organization row receives `deleted_at`; the ordinary repository lookup filters deleted rows. Consequently, the current lifecycle snapshot returns `404` both when an organization is soft-deleted and when no visible organization row can be resolved through that lookup path.

There is currently no separate durable organization tombstone contract that lets a product distinguish, from that `404` alone, a terminally deleted organization from an unknown/nonexistent organization.

Therefore **Core `404` is not proof of closure or terminal deletion** and must never be converted into an automatic destructive purge decision.

## 3. Decision OL10-A — backup maximum age

A successfully completed FAIR CRM full-database backup has a **maximum retention/restorable age of 30 calendar days** from its successful `completed_at` timestamp in UTC.

Rules:

- age origin: successful `SystemBackup.completed_at` in UTC;
- maximum age: `30 days`;
- download does not reset age;
- restore attempt does not reset age;
- copying/renaming a dump does not reset the source backup's authoritative age;
- there is no "keep last backup forever" exception;
- operational recovery continuity must be maintained by creating a fresh successful backup, not by extending stale backup lifetime;
- OL09-D's 12-month minimal audit/security evidence retention does **not** justify retaining full database backup contents for 12 months;
- closure-package retention under OL09-E does not extend full-database backup retention.

### Rationale

The existing system has no evidence-backed longer backup retention requirement. A full database dump is a high-blast-radius recovery artifact containing data for multiple organizations, so retaining it indefinitely would defeat accepted offboarding deletion policy. Thirty days preserves a meaningful recovery window while bounding the period during which already-closed organization data can remain recoverable from an older full dump. It is also consistent with the accepted 30-day closure/grace horizon without redefining that horizon as backup-specific authority.

This is a **whole-backup** policy. A full database dump cannot be safely aged per organization.

## 4. Decision OL10-B — restored FAIR CRM state is not lifecycle authority

Rows restored from FAIR CRM — including organization-closure execution rows, local observations, export metadata, credential-disposition evidence or other closure-related records — are historical data from the backup timestamp.

They are **not authoritative current organization lifecycle truth** after restore.

A restore must reconcile every organization represented by restored tenant-bearing FAIR CRM product data against **live external authoritative lifecycle truth**, with Kyrox Core as the current organization lifecycle authority.

The candidate set must be derived from the full tenant-bearing product-data surface, not only from restored organization-closure records. FAIR CRM's canonical tenant-isolation registry is the starting inventory for that coverage and must remain complete under CI governance.

## 5. Decision OL10-C — fail-closed post-restore reconciliation

A restore must not be certified `COMPLETED`, and production service must not be made available from the restored database, until reconciliation succeeds.

Required sequence:

1. restore dump,
2. migrate schema to current head,
3. run existing generic post-restore health checks,
4. enumerate organization IDs represented by restored tenant-bearing product data,
5. fetch current external authoritative lifecycle/deletion truth for each organization,
6. produce and persist a non-secret reconciliation result,
7. apply only destructive disposition actions already authorized by accepted offboarding contracts and backed by sufficient current authority,
8. re-check authority where the destructive path requires a live gate,
9. certify reconciliation,
10. only then mark the restore completed / permit normal production availability.

### Reconciliation matrix

| Authoritative result | Restore treatment |
| --- | --- |
| Explicit current `ACTIVE`, not deleted, internally consistent | Organization data may remain eligible for normal product access, subject to ordinary runtime authorization. |
| Explicit current non-active lifecycle such as `SUSPENDED`, `ARCHIVED` or another non-work-allowed state | Must remain non-operable. Do not treat the restored FAIR CRM closure phase as authority for irreversible purge. Apply only disposition steps whose external authoritative gates are satisfied. |
| Explicit authoritative terminal deletion/tombstone | Restored organization product data must not become usable and must be reconciled through the accepted destructive disposition contract. |
| Core/external timeout, network failure, auth failure, malformed payload, inconsistent payload, stale/unverifiable authority | **BLOCK / UNKNOWN.** Fail closed. Restore cannot be certified complete. |
| `404` from the current Core lifecycle lookup | **BLOCK / UNKNOWN.** A `404` is not sufficient proof of deletion under the current contract. Do not auto-purge and do not certify the restore. |

No FAIR CRM row restored from the dump may downgrade an external `SUSPENDED`, terminal-deleted or unknown result back to active.

## 6. Decision OL10-D — durable deletion truth prerequisite

The current Core soft-delete implementation is sufficient to deny ordinary organization access, but the current lifecycle snapshot contract does not expose enough deletion evidence for OL-10 to classify a soft-deleted organization separately from an unresolved/missing organization.

Therefore runtime completion of terminal restore reconciliation requires an external authoritative contract that can positively represent deletion state.

Minimum acceptable contract behavior:

- current visible organization: explicit lifecycle state plus work-allowed semantics;
- current soft-deleted organization: explicit deleted state (`deleted_at`, `is_deleted` or equivalent), not an ambiguous success path;
- truly unknown organization: remains distinguishable from deleted;
- any future hard-delete implementation must preserve durable terminal tombstone truth for at least as long as a still-valid backup can be restored and reconciled.

The implementation must not infer a tombstone that Core does not currently store.

## 7. Decision OL10-E — maintenance boundary

Fail-closed reconciliation must be protected by a maintenance boundary **outside the database being restored**.

The restored FAIR CRM database itself cannot be trusted to say that maintenance mode is active, because the restore overwrites that database.

The current manual restore script requires an explicit restore enablement but does not itself establish a complete externally durable production-unavailable boundary. Runtime implementation must therefore ensure that normal FAIR CRM serving cannot resume before post-restore reconciliation is certified.

A failed or blocked reconciliation leaves the restore job failed/blocked and the restored database unavailable for normal production traffic. An operator may remediate the authoritative dependency and rerun reconciliation; the safe response is never to bypass the gate.

## 8. Runtime implementation gates

OL-10 is accepted only with the following implementation sequence; this platform decision does not pretend those runtime changes already exist.

### Core

1. Extend the product lifecycle/deletion authority so soft-deleted organizations are positively distinguishable from unknown/missing organizations without changing ordinary user-facing lookup semantics.
2. Keep `work_allowed=false` for any deleted or non-active organization.
3. Add tests proving deleted vs unknown behavior and fail-closed token/auth behavior.
4. Preserve a durable terminal tombstone if a future change physically removes the organization row while a valid backup can still reference it.

### FAIR CRM

1. Add explicit backup max-age configuration with a 30-day policy default and tests.
2. Reject/restict restoration of tracked backups older than 30 days using authoritative successful `completed_at`.
3. Add automatic/operational pruning so expired full backup artifacts do not remain indefinitely merely because restore rejects them.
4. Build restore candidate enumeration from the tenant-bearing product-data inventory, not the restored closure table alone.
5. Insert authoritative lifecycle reconciliation after migration + generic health and before restore completion.
6. Treat unavailable/ambiguous Core truth, including current ambiguous `404`, as blocked/failed reconciliation.
7. Enforce an external maintenance boundary so backend availability cannot race ahead of reconciliation.
8. Persist non-secret reconciliation evidence adequate for operator/audit diagnosis without copying product data into the audit record.
9. Add regression tests covering an old backup that resurrects data for an organization whose lifecycle advanced after the backup.

### Platform / CI

1. Keep OL-10 policy and implementation evidence linked from the P0.2 trackers.
2. Require each runtime PR to pass its repository CI on the exact PR head before merge.
3. Treat repository `main` after merge as canonical evidence.

## 9. Required regression scenarios

At minimum, runtime certification must cover:

1. backup at T1 contains org A as active; Core says A active at restore -> reconciliation can pass for A;
2. backup at T1 contains org A active; Core now says A suspended -> restored A data cannot become operable;
3. backup at T1 contains org A; Core positively says A deleted/tombstoned -> restored product data is reconciled through accepted destructive disposition and cannot become operable;
4. backup at T1 contains org A; Core returns current ambiguous `404` -> restore is blocked, not purged and not certified;
5. Core unavailable/auth invalid/malformed response -> restore is blocked;
6. restored closure row claims active/open while Core says non-active/deleted -> Core wins;
7. restored closure row claims closed while Core says active -> restored closure row cannot itself trigger destructive purge;
8. valid tracked backup age <= 30 days -> eligible to enter restore pipeline, still subject to reconciliation;
9. tracked backup age > 30 days -> restore rejected;
10. download/restore attempts do not reset backup age;
11. backend/production availability cannot resume between `pg_restore` and reconciliation certification.

## 10. Closure condition for OL-10

Policy decision OL-10 is **accepted by this document**.

Implementation closure requires all of the following on canonical `main` branches:

- Core exposes sufficient authoritative deletion truth for reconciliation;
- FAIR CRM enforces 30-day backup ageing/retention;
- FAIR CRM performs fail-closed post-restore reconciliation before completion/availability;
- the maintenance boundary is externally durable;
- required regressions pass CI;
- platform implementation tracking points to the merged runtime PR evidence.

Until those runtime gates are merged, old-backup resurrection remains an explicitly known implementation risk and destructive organization offboarding is not restore-safe certified.