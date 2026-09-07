# KYROX Ecosystem Status

Single source of truth for **cross-repository current state**. Detailed product/Core status lives in the project status files linked below. Do not duplicate sprint histories, test-count histories or roadmap queues here.

| Field | Value |
|-------|-------|
| Active milestone | **M4 — FAIR CRM v1** |
| Core policy | Frozen for speculative product work; bug/security/performance fixes and approved reusable product-driven platform needs are allowed |
| Documentation hub | `kyrox-platform` |
| Implementation repos | `kyrox-core`, `fair-crm` |
| Last ecosystem sync | **2026-09-08** |

## SaaS readiness

**P0.1 Tenant Isolation Certification is DONE.** FAIR CRM organization-owned paths are certified across direct/nested resource access, derived relationships, bulk mutations, background execution, mail/SMTP ownership, exports/downloads/artifacts and audit context. The canonical Platform Super Admin exception is separately certified in Core and production-shaped FAIR CRM integration evidence.

Closure evidence is recorded in [projects/fair-crm/backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md](../projects/fair-crm/backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md). FAIR CRM PRs #83 and #84 close TI-07 and TI-09; Core PR #11 closes TI-08. The final FAIR CRM TI-09 head passed Development Standard Gate #268 and Prod-Path E2E #140 before merge. P0.1 completion does not waive the SaaS-impact gates for future changes; new organization-owned behavior must continue to ship with applicable cross-organization evidence.

**The approved P0.2 identity / SaaS onboarding workstream is DONE as of 2026-08-29.** [ADR-0006](decisions/0006-organization-lifecycle-and-onboarding.md) remains Proposed overall. OL-01 through OL-07 are implemented/certified. OL08-A is accepted and OL08-01 is DONE. OL08-B partially accepts the technical closure-export contract; OL08-02 closure-quiescence certification and the bounded OL08-03A export manifest/completeness planner are now implemented/certified. `not_required` policy authority, persistent/downloadable package lifecycle and all irreversible closure phases remain gated. **OL08-C provider credential disposition is the next decision gate; no OL08-C runtime is authorized.** OL08-D through OL08-G, OL-09 retention/grace policy and OL-10 backup implications remain separately gated.

The completed workstream keeps `Organization` as the account boundary, keeps the direct single-organization user model, uses the existing protected `OrganizationAdmin` role for the first normal admin, preserves existing Platform Super Admin organization/user creation, and provides controlled public commercial signup plus Core-owned activation/set-password, password reset/change, one-time identity action tokens, shared password policy, session/credential invalidation and production identity-email capability. FAIR CRM remains a thin consumer of public Core identity APIs and owns no credential authority.

The canonical completion record is [P0.2 Identity / SaaS Onboarding Implementation Tracker](P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md). CORE-01 through CORE-09 were delivered through Core PRs #12–#20, ending at Core `main` `f6cbf417410d9148c225242790103d8cc9541f21` after CI #84 / run `33228476878` passed with 381 tests. The final Core certification includes privilege-injection resistance and cross-organization activation-token isolation.

FAIR CRM then delivered CRM-BE-01/02 through PRs #86/#87, public auth and login integration through PRs #88/#89, authenticated `/settings/security` password change through PR #90, and Super Admin manual user-management compatibility certification through PR #91. CRM-UI-03 keeps current-password verification, PasswordPolicy, hashing and credential mutation in Core; after a successful change the Core sessions are revoked, the FAIR CRM refresh cookie is cleared, local frontend session state is cleared and the user returns to login. CRM-UI-04 confirms the existing admin-supplied manual password path remains available and no unsupported setup-link or new Super Admin assignment path was introduced.

Final FAIR CRM PR #92 (`d498245c4c60bd36b9b3a8aeffed4912e198123b`) added a production-shaped cross-repository certification without changing application runtime. Development Standard Gate #306 and Prod-Path E2E #151 passed the final head before merge. The certified lifecycle covers signup → activation → login → forgot/reset → login → password change → login against real FAIR CRM + real KYROX Core, including one-time token replay rejection and prior-session invalidation.

**OL-07 suspension/reactivation runtime is DONE as of 2026-09-07.** OL07-03 established the Core-owned product lifecycle snapshot contract and FAIR CRM fail-closed lifecycle guard. OL07-04 made queued/pending organization-owned FAIR CRM work cancel before start when Core reports a non-active lifecycle state. OL07-05 completed cooperative cancellation of already-running covered work at safe checkpoints. OL07-06 blocked new SMTP/provider handoff at the final central lifecycle checkpoint. OL07-07 made claimed mail durably `SENDING` before provider handoff, safely recovered a real SQLAlchemy session when that checkpoint commit failed, and made ambiguous MailerSend/SMTP in-flight outcomes terminal non-auto-retry. FAIR CRM PR #254 then certified deterministic reactivation/resumption semantics. PR #254 final head `e17593e49ecb25a3aef736b0ceaa1fafa14c7e77` passed Development Standard Gate #700 and Prod-Path E2E #264 before merge as `18b0b638ba946c2910698e1df7c4ab5283c4958f`.

**OL08-A closure orchestration is ACCEPTED and OL08-01 is DONE as of 2026-09-07.** FAIR CRM PR #255 added the FAIR CRM-owned durable non-destructive closure execution state machine, SYSTEM-authorized start/status/retry, live Core `SUSPENDED` precondition, idempotent duplicate/race handling, explicit blocked/retry evidence, transactional append-only local audit evidence and canonical tenant-isolation registration. Final head `aa34cd3e5d00ec6f7d6b7adaad4afa950319830e` passed Development Standard Gate #707 / run `34155567277` and Prod-Path E2E #270 / run `34155567315`, then merged to FAIR CRM `main` as `e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`. Platform PR #36 passed Platform Standards CI #104 / run `34156643910` and merged as `f08f3a334c56c3c1be31694af56bf65330e44fe9`, completing cross-repository certification.

**OL08-B closure-export technical contract is PARTIALLY ACCEPTED as of 2026-09-07.** The accepted architecture uses explicit policy-conditioned `required` / `not_required` disposition, a versioned organization/execution-scoped manifest, explicit structured-data completeness classification, hard secret exclusion and SYSTEM/operator-only control. No accepted policy currently authorizes `not_required`, so that path must fail closed. Generated/binary artifacts and persistent/downloadable closure-package lifecycle remain deferred to OL08-E/applicable OL-09 policy. The detailed contract is [P0.2 OL-08B Closure Export Contract Decision](P0_2_OL_08_B_EXPORT_DECISION.md).

**OL08-02 and OL08-03A are DONE as of 2026-09-08.** FAIR CRM PR #256 final head `bae0e7f720e29b688765999fff12deda8624dad7` passed Development Standard Gate #711 / run `34160597160` and Prod-Path E2E #273 / run `34160597182`, then merged as `00f7219c45a5c761df0861e7b30a89ad2a67652d`. It certified closure quiescence against the existing OL-07 runtime and fixed the closure-execution parent/event FK flush ordering while preserving one transaction. FAIR CRM PR #257 then implemented the bounded non-destructive OL08-03A planner: durable organization/execution/schema-version export-plan identity, explicit v1 completeness registry, organization-scoped counts, record-ID-only fingerprints, hard secret-source exclusion, SYSTEM metadata endpoints, idempotency and tenant-isolation evidence. Final head `6927dabea1cf46e1ee70b726d3c8ccd1ae247dcd` passed Development Standard Gate #715 / run `34163087279` and Prod-Path E2E #276 / run `34163087299`, then merged as `eac3a0793a6ea0382e3b82169a1e3c18c0accfc9`. No package/download, `not_required` success, irreversible cleanup gate or Core tombstone was added.

## KYROX Core

Canonical detail: [projects/kyrox-core/PROJECT_STATUS.md](../projects/kyrox-core/PROJECT_STATUS.md)  
Active planning: [projects/kyrox-core/ROADMAP.md](../projects/kyrox-core/ROADMAP.md)

Core remains the reusable, product-agnostic SaaS backend. Identity, authentication, authorization, organization/user/role governance and shared platform services are implemented in Core. Products consume Core through public contracts; product domain logic does not belong in Core.

The approved P0.2 identity/onboarding primitives are complete. Core owns canonical organization/identity lifecycle and SYSTEM-scoped organization suspend/reactivate/delete authority. Product-specific closure progress/export/provider/data/artifact behavior remains outside Core and is consumed/orchestrated only through accepted public contracts.

## FAIR CRM

Canonical detail: [projects/fair-crm/PROJECT_STATUS.md](../projects/fair-crm/PROJECT_STATUS.md)  
Current work queue: [projects/fair-crm/ROADMAP.md](../projects/fair-crm/ROADMAP.md)

FAIR CRM remains the active M4 product. Its P0.1 tenant-isolation certification, P0.2 identity bridge, OL-07 suspension/reactivation runtime, OL08-01 closure execution, OL08-02 quiescence certification and OL08-03A export manifest/completeness planner are complete within their accepted boundaries.

A Platform SuperAdmin/SYSTEM-authorized caller may start, inspect or retry a closure execution only while live Core lifecycle authority reports `SUSPENDED`. The product persists execution/event evidence with database-enforced single-open/idempotency constraints and explicit blocked/retry semantics. For the same closure execution, OL08-03A may produce only non-destructive planning metadata: a versioned completeness manifest with organization-scoped counts/fingerprints and explicit included/excluded/deferred evidence. Reusable credential/secret tables are not planner sources.

The next lifecycle step is **OL08-C provider credential disposition decision-readiness/acceptance**, not runtime implementation. Persistent/downloadable closure packages, `not_required` policy authority, provider credential revoke/purge, product-data/artifact destruction, retention/grace, backup reconciliation, cleanup-complete/tombstone-ready state and Core tombstone remain gated.

The current documentation/quality focus is to keep Platform as the single human/AI knowledge source and to ensure permission-controlled UI surfaces consistently follow effective permissions and the shared CRUD/UI authorization standard.

## Milestones

| Milestone | Status | Canonical document |
|-----------|--------|--------------------|
| M1 Foundation | Completed / historical | [archive/milestones/M1_FOUNDATION.md](../archive/milestones/M1_FOUNDATION.md) |
| M2 Identity | Completed / historical | [archive/milestones/M2_IDENTITY.md](../archive/milestones/M2_IDENTITY.md) |
| M3 Platform Services | Completed / historical | [archive/milestones/M3_PLATFORM_SERVICES.md](../archive/milestones/M3_PLATFORM_SERVICES.md) |
| M4 FAIR CRM v1 | **Active** | [projects/fair-crm/MILESTONE_M4.md](../projects/fair-crm/MILESTONE_M4.md) |

## Repository boundaries

| Repository | Owner scope |
|------------|-------------|
| `kyrox-platform` | All human/AI documentation, shared standards, project docs, ADRs, status and roadmap |
| `kyrox-core` | Reusable SaaS platform implementation, tests, migrations and CI |
| `fair-crm` | FAIR CRM product implementation, tests, migrations, CI and machine-readable contracts |

See [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md) and [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md).
