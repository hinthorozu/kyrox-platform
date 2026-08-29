# KYROX Ecosystem Status

Single source of truth for **cross-repository current state**. Detailed product/Core status lives in the project status files linked below. Do not duplicate sprint histories, test-count histories or roadmap queues here.

| Field | Value |
|-------|-------|
| Active milestone | **M4 — FAIR CRM v1** |
| Core policy | Frozen for speculative product work; bug/security/performance fixes and approved reusable product-driven platform needs are allowed |
| Documentation hub | `kyrox-platform` |
| Implementation repos | `kyrox-core`, `fair-crm` |
| Last ecosystem sync | **2026-08-29** |

## SaaS readiness

**P0.1 Tenant Isolation Certification is DONE.** FAIR CRM organization-owned paths are certified across direct/nested resource access, derived relationships, bulk mutations, background execution, mail/SMTP ownership, exports/downloads/artifacts and audit context. The canonical Platform Super Admin exception is separately certified in Core and production-shaped FAIR CRM integration evidence.

Closure evidence is recorded in [projects/fair-crm/backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md](../projects/fair-crm/backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md). FAIR CRM PRs #83 and #84 close TI-07 and TI-09; Core PR #11 closes TI-08. The final FAIR CRM TI-09 head passed Development Standard Gate #268 and Prod-Path E2E #140 before merge. P0.1 completion does not waive the SaaS-impact gates for future changes; new organization-owned behavior must continue to ship with applicable cross-organization evidence.

**The approved P0.2 identity / SaaS onboarding workstream is DONE as of 2026-08-29.** [ADR-0006](decisions/0006-organization-lifecycle-and-onboarding.md) remains Proposed overall because suspension/closure/retention/backup and related lifecycle decisions are still open, but its explicitly approved identity/onboarding subset OL-01 through OL-04 has now been implemented and production-path certified across Core and FAIR CRM.

The completed workstream keeps `Organization` as the account boundary, keeps the direct single-organization user model, uses the existing protected `OrganizationAdmin` role for the first normal admin, preserves existing Platform Super Admin organization/user creation, and provides controlled public commercial signup plus Core-owned activation/set-password, password reset/change, one-time identity action tokens, shared password policy, session/credential invalidation and production identity-email capability. FAIR CRM remains a thin consumer of public Core identity APIs and owns no credential authority.

The canonical completion record is [P0.2 Identity / SaaS Onboarding Implementation Tracker](P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md). CORE-01 through CORE-09 were delivered through Core PRs #12–#20, ending at Core `main` `f6cbf417410d9148c225242790103d8cc9541f21` after CI #84 / run `33228476878` passed with 381 tests. The final Core certification includes privilege-injection resistance and cross-organization activation-token isolation.

FAIR CRM then delivered CRM-BE-01/02 through PRs #86/#87, public auth and login integration through PRs #88/#89, authenticated `/settings/security` password change through PR #90, and Super Admin manual user-management compatibility certification through PR #91. CRM-UI-03 keeps current-password verification, password policy, hashing and credential mutation in Core; after a successful change the Core sessions are revoked, the FAIR CRM refresh cookie is cleared, local frontend session state is cleared and the user returns to login. CRM-UI-04 confirms the existing admin-supplied manual password path remains available and no unsupported setup-link or new Super Admin assignment path was introduced.

Final FAIR CRM PR #92 (`d498245c4c60bd36b9b3a8aeffed4912e198123b`) added CI-only cross-repository lifecycle certification and merged as `2f9f159a303ffd055121547de51dcaefc15fc6a9`. Development Standard Gate #306 / run `33246959509` and Prod-Path E2E #151 / run `33246959442` passed the same final head. The Prod-Path run first passed the existing production-shaped gate with **35 passed, 0 failed**, then certified signup → activation → login → forgot/reset → login → password change → login through real FAIR CRM + real KYROX Core. Core's real SMTP adapter delivered activation/reset email into an in-process memory-only SMTP sink; activation/reset replay was rejected and pre-credential-change access/refresh sessions were rejected after reset/change. The certification PR changed no FAIR CRM/Core application runtime or schema behavior.

The P0.2 lifecycle audit still records the separate OL-07 execution-policy gap: normal permission-protected starts are blocked after suspension, but already queued/running FAIR CRM work generally continues from previously established organization-scoped job context without re-checking authoritative Core organization status. This remains a **lifecycle-policy gap, not a P0.1 tenant-isolation regression**, and the completed onboarding workstream does not authorize suspension/closure runtime changes.

## KYROX Core

Canonical detail: [projects/kyrox-core/PROJECT_STATUS.md](../projects/kyrox-core/PROJECT_STATUS.md)  
Active planning: [projects/kyrox-core/ROADMAP.md](../projects/kyrox-core/ROADMAP.md)

Core remains the reusable, product-agnostic SaaS backend. Identity, authentication, authorization, organization/user/role governance and shared platform services are implemented in Core. Products consume Core through public HTTP contracts; product domain logic does not belong in Core.

The approved P0.2 identity/onboarding primitives are complete. CORE-01 established the shared 12–255 character password policy. CORE-02 added generic hash-only, expiring, single-use identity action tokens. CORE-03 added user-wide session/refresh invalidation plus server-side access-token session enforcement. CORE-04 added platform-scoped Core identity notifications, production SMTP delivery capability and generic identity templates. CORE-05 added controlled public signup with atomic pending-organization/first-admin bootstrap and secure token handoff. CORE-06 added single-use activation/set-password with atomic user/organization activation and secret-safe audit evidence. CORE-07 added enumeration-safe forgot/reset password, reset-token cooldown/supersession, shared password policy enforcement, credential replacement, user-wide session/refresh invalidation and secret-safe reset audit evidence. CORE-08 added authenticated self-service password change with current-password verification, same-password rejection, shared password policy, credential replacement, user-wide session/refresh invalidation and secret-safe change audit evidence. CORE-09 completed the Core security/adversarial certification.

The Core migration head remains `20260827_0064_platform_identity_notifications`; CORE-05 through CORE-09 required no schema migration. Current-state details belong in the Core project status, not in permanent standards or roadmap documents.

## FAIR CRM

Canonical detail: [projects/fair-crm/PROJECT_STATUS.md](../projects/fair-crm/PROJECT_STATUS.md)  
Current work queue: [projects/fair-crm/ROADMAP.md](../projects/fair-crm/ROADMAP.md)

FAIR CRM remains the active M4 product. Existing implementation includes the CRM foundations, data integration/import flows, operations/automation flows, mail delivery flows, quotation-related capabilities and a cost-catalog implementation. Its P0.1 tenant-isolation certification is complete; ongoing product work remains subject to the same SaaS-impact, authorization-scope and tenant-isolation delivery rules.

The approved P0.2 product integration is complete: thin Core auth bridge, public signup/activation/password-recovery, login entry links, authenticated security/password change, preserved Super Admin manual user provisioning and final cross-repository lifecycle certification. Credential authority and password/token logic remain entirely in Core. No unsupported setup-link mode was added.

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
