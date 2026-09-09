# P0.2 OL-10 — Runtime Acceptance

Status: **ACCEPTED**  
Date: **2026-09-09**  
Canonical source: GitHub `main`

## 1. Acceptance scope

This record closes the runtime implementation gates defined by `P0_2_OL_10_BACKUP_AGEING_RESTORE_RECONCILIATION_DECISION.md` for planned FAIR CRM and Kyrox Core database restore flows.

The accepted runtime evidence is the merged code on the canonical `main` branches of Kyrox Core and FAIR CRM. Restored product-local closure records are not promoted to lifecycle authority.

## 2. Kyrox Core evidence

Merged runtime PR: `hinthorozu/kyrox-core#27` — `feat(identity): add OL10 self-restore lifecycle guard`.

Merged Core `main` commit: `5e832328479e846b1e4c0d33e0123a4f62a9aa7a`.

Exact PR head before merge: `b8ab65a198561cde094c633fd40a065b69a2202a`.

CI evidence:

- workflow: `CI`
- run: `34365926320` / run #107
- result: **SUCCESS**
- test result: **409 passed**

Accepted Core behavior:

1. Product lifecycle authority positively distinguishes soft-deleted organizations from unknown organizations through `is_deleted` / `deleted_at` while preserving ordinary lookup semantics.
2. A planned destructive Core restore captures current organization lifecycle truth before `pg_restore` into restore-process memory outside the database being replaced.
3. The snapshot includes every organization, including soft-deleted rows, with current `status` and `deleted_at`.
4. After restore/migration, Core-owned reconciliation re-applies pre-restore lifecycle truth before restore certification.
5. An organization present only in an old backup is fail-closed soft-tombstoned instead of becoming usable.
6. If the restored backup is missing an organization present in the pre-restore authoritative snapshot, certification blocks rather than inventing unrecoverable current state.
7. No hard-delete is inferred without a durable hard-delete tombstone contract.

## 3. FAIR CRM evidence

Merged runtime PR: `hinthorozu/fair-crm#263` — `feat(backup): enforce OL10 restore reconciliation`.

Merged FAIR CRM `main` commit: `698cd886417d50ab38faddc840663ac6aa47529c`.

Exact PR head before merge: `066c41575c1e4a6815dd2f798a4f1439cdf6fe04`.

Exact-head CI evidence:

- `Development Standard Gate`, run `34366237019` / run #738: **SUCCESS**
- `Prod-Path E2E`, run `34366236958` / run #289: **SUCCESS**
- Prod-Path E2E was explicitly rerun after Core PR #27 was merged so the final certification used canonical merged Core `main`.
- rerun job `102518130961`: all prod-path, OL07-03 lifecycle authority, P0.2 identity lifecycle certification and todo authorization regression steps passed.

Accepted FAIR CRM behavior:

1. FAIR CRM full-database backup maximum age is **30 calendar days** from successful `SystemBackup.completed_at` UTC.
2. Exact 30-day boundary remains eligible; older backups are rejected.
3. Restore requires tracked successful backup provenance, same-database source/target identity, expected file identity and matching checksum.
4. Arbitrary uploaded dumps are blocked because authoritative backup-age provenance cannot be established safely.
5. Expired FAIR CRM full-database backup artifacts and metadata are physically pruned; no keep-last-forever exception is introduced.
6. Universal data packages are outside the OL-10 full-database retention rule.
7. Post-restore organization candidate enumeration scans restored tenant-bearing tables containing `organization_id`; restored closure rows are not the candidate authority.
8. FAIR CRM restore reconciles every discovered organization against live current Kyrox Core lifecycle truth before completion.
9. Core timeout, auth failure, malformed/inconsistent response, unknown organization or otherwise unverifiable authority blocks certification.
10. Explicit Core deletion prevents restored organization data from becoming usable; FAIR does not invent irreversible purge authority from restored local state.
11. Suspended/archived non-deleted organizations remain governed by the ordinary Core work gate.

## 4. Core restore integration through FAIR maintenance tooling

FAIR CRM's maintenance runner may orchestrate a tracked Kyrox Core database restore, but lifecycle authority remains Core-owned:

1. tracked completed Core backup provenance and checksum are required;
2. FAIR's 30-day retention policy is not incorrectly projected onto Core backups because no Core retention duration was accepted by OL-10;
3. after dump verification and immediately before destructive restore, the runner invokes the Core-owned lifecycle guard from the configured Core repository and Core virtual environment;
4. the captured authority remains in process memory across database replacement;
5. after Core migration, the Core-owned guard reconciles the restored Core database;
6. the restore job cannot become `COMPLETED` until reconciliation succeeds.

## 5. External maintenance boundary

The accepted production boundary is outside both databases:

- `data/restore_maintenance.lock` is created before the destructive maintenance execution;
- FAIR CRM backend and mail worker must be stopped for every restore;
- FAIR CRM restore requires live Core service so current external lifecycle authority remains queryable;
- Core restore requires Core service stopped while the Core-owned CLI reads/reconciles the database directly;
- FAIR CRM backend, mail worker and Kyrox Core systemd units refuse startup while the external restore lock exists;
- failed or blocked reconciliation retains the lock;
- the lock is cleared only after certified restore success.

This prevents normal production availability from racing ahead of reconciliation after `pg_restore`.

## 6. OL-10 acceptance result

The implementation closure conditions in the OL-10 decision are satisfied on canonical `main` for the supported planned restore paths:

- **Core authoritative deletion truth:** satisfied.
- **FAIR CRM 30-day backup ageing/retention:** satisfied.
- **Physical full-backup pruning:** satisfied.
- **Fail-closed FAIR post-restore reconciliation:** satisfied.
- **Core planned self-restore lifecycle reconciliation:** satisfied.
- **External maintenance boundary:** satisfied.
- **Regression/CI evidence on exact heads:** satisfied.

Therefore **P0.2 OL-10 backup ageing / restore reconciliation is runtime-accepted**.

## 7. Explicit residual boundary — not silently closed

This acceptance does **not** claim that current lifecycle truth can be recovered after total loss of the current Kyrox Core database when no pre-restore snapshot can be captured.

That disaster-recovery scenario requires a separately durable external lifecycle ledger/tombstone authority. Until such an authority exists, a restore performed without current Core lifecycle truth must remain fail-closed.

Likewise, if a future Core implementation physically hard-deletes organization rows while a still-valid backup can reference those organizations, Core must preserve durable terminal tombstone truth for the required reconciliation horizon. OL-10 does not authorize inferring such a tombstone from absence alone.
