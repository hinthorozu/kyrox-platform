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

The active cross-repository SaaS-readiness phase is **P0.2 — Organization lifecycle contract and SaaS onboarding**. [ADR-0006](decisions/0006-organization-lifecycle-and-onboarding.md) remains Proposed overall because suspension/closure/retention/backup decisions are still open, but the identity/onboarding subset OL-01 through OL-04 was explicitly approved for implementation on **2026-08-27**.

The approved workstream keeps `Organization` as the account boundary, keeps the direct single-organization user model, uses the existing `OrganizationAdmin` role for the first normal admin, preserves existing Platform Super Admin organization/user creation, and adds controlled public commercial signup plus Core-owned activation/set-password, password reset/change, one-time identity action tokens, shared password policy, session/credential invalidation and production identity-email capability. FAIR CRM remains a thin consumer of public Core identity APIs and will own the bridge/UI only.

The canonical implementation/resume checklist is [P0.2 Identity / SaaS Onboarding Implementation Tracker](P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md). CORE-01 through CORE-04 are delivered through Core PRs #12–#15. CORE-05 public signup + atomic bootstrap is delivered through Core PR #16. CORE-06 activation/set-password is delivered through Core PR #17. CORE-07 forgot/reset password is delivered through Core PR #18. CORE-08 authenticated password change is delivered through Core PR #19. **CORE-09 — Core security/adversarial certification is delivered through Core PR #20**, merged to Core `main` as `f6cbf417410d9148c225242790103d8cc9541f21` after CI #84 / run `33228476878` passed the final head `5c5113320ea910e80555e6cc526ed0c708580cd4` with 381 tests. The final certification re-ran the complete onboarding/credential security and regression surface and added explicit coverage proving signup cannot self-assert Super Admin/privileged role state and an Organization A activation token cannot mutate Organization B state.

**FAIR CRM backend handoff is complete through CRM-BE-02 and public auth UI is complete through CRM-UI-01.** CRM-BE-01 extended the thin Core auth client through FAIR CRM PR #86. CRM-BE-02 added the product `/api/v1/auth/*` bridge routes through PR #87. CRM-UI-01 added public `/signup`, `/activate`, `/forgot-password` and `/reset-password` screens through FAIR CRM PR #88; Development Standard Gate #291 passed 307 frontend tests, production build and the zero-new UI-governance gate before merge. FAIR CRM still owns no password policy, password hashing, action-token persistence or credential mutation. **The next execution phase is CRM-UI-02 — login integration.**

The P0.2 lifecycle audit also confirmed that Core now uses direct `identity_users.organization_id` ownership for normal users; legacy memberships and membership invitations were removed by migration `20260817_0057_remove_memberships`. Organization suspend/delete remain SYSTEM-scope, Core delete remains a Core soft-delete, and the domain reactivation transition currently lacks a public organization API endpoint.

The [P0.2 lifecycle runtime audit](P0_2_LIFECYCLE_RUNTIME_AUDIT.md) confirms the still-open OL-07 execution gap: normal permission-protected starts are blocked after suspension, but already queued/running FAIR CRM scraper, enrichment, import and mail work generally continues from previously established organization-scoped job context without re-checking authoritative Core organization status. Import background execution explicitly trusts queue-time authorization, and outbound delivery checks product email-account activity rather than Core organization lifecycle state. This remains a **lifecycle-policy gap, not a P0.1 tenant-isolation regression**; onboarding approval does not authorize suspension/closure runtime changes.

## KYROX Core

Canonical detail: [projects/kyrox-core/PROJECT_STATUS.md](../projects/kyrox-core/PROJECT_STATUS.md)  
Active planning: [projects/kyrox-core/ROADMAP.md](../projects/kyrox-core/ROADMAP.md)

Core remains the reusable, product-agnostic SaaS backend. Identity, authentication, authorization, organization/user/role governance and shared platform services are implemented in Core. Products consume Core through public HTTP contracts; product domain logic does not belong in Core.

The P0.2 identity/onboarding primitives are an approved, product-driven Core workstream. CORE-01 established the shared 12–255 character password policy. CORE-02 added generic hash-only, expiring, single-use identity action tokens. CORE-03 added user-wide session/refresh invalidation plus server-side access-token session enforcement. CORE-04 added platform-scoped Core identity notifications, production SMTP delivery capability and generic identity templates. CORE-05 added controlled public signup with atomic pending-organization/first-admin bootstrap and secure token handoff. CORE-06 added single-use activation/set-password with atomic user/organization activation and secret-safe audit evidence. CORE-07 added enumeration-safe forgot/reset password, reset-token cooldown/supersession, shared password policy enforcement, credential replacement, user-wide session/refresh invalidation and secret-safe reset audit evidence. CORE-08 added authenticated self-service password change with current-password verification, same-password rejection, shared password policy, credential replacement, user-wide session/refresh invalidation and secret-safe change audit evidence. **CORE-09 final Core security/adversarial certification is complete; the approved Core onboarding slice is now consumed by the FAIR CRM backend bridge and public auth UI.**

The Core migration head remains `20260827_0064_platform_identity_notifications`; CORE-05, CORE-06, CORE-07, CORE-08 and CORE-09 required no schema migration. Current-state details belong in the Core project status, not in permanent standards or roadmap documents.

## FAIR CRM

Canonical detail: [projects/fair-crm/PROJECT_STATUS.md](../projects/fair-crm/PROJECT_STATUS.md)  
Current work queue: [projects/fair-crm/ROADMAP.md](../projects/fair-crm/ROADMAP.md)

FAIR CRM remains the active M4 product. Existing implementation includes the CRM foundations, data integration/import flows, operations/automation flows, mail delivery flows, quotation-related capabilities and a cost-catalog implementation. Its P0.1 tenant-isolation certification is complete; ongoing product work remains subject to the same SaaS-impact, authorization-scope and tenant-isolation delivery rules.

The approved P0.2 backend integration and public auth UI are delivered. `CoreAuthClient` supports signup/activation/forgot/reset/change-password; FAIR CRM exposes the thin bridge routes and public signup/activation/password-recovery screens. The active product step is now login integration for account creation and password recovery, followed by authenticated account/security password change. The existing Super Admin manual user-management flow remains preserved. Credential authority and password/token logic remain entirely in Core.

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
