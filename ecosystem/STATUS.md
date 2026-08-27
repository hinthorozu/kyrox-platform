# KYROX Ecosystem Status

Single source of truth for **cross-repository current state**. Detailed product/Core status lives in the project status files linked below. Do not duplicate sprint histories, test-count histories or roadmap queues here.

| Field | Value |
|-------|-------|
| Active milestone | **M4 — FAIR CRM v1** |
| Core policy | Frozen for speculative product work; bug/security/performance fixes and approved reusable product-driven platform needs are allowed |
| Documentation hub | `kyrox-platform` |
| Implementation repos | `kyrox-core`, `fair-crm` |
| Last ecosystem sync | **2026-08-27** |

## SaaS readiness

**P0.1 Tenant Isolation Certification is DONE.** FAIR CRM organization-owned paths are certified across direct/nested resource access, derived relationships, bulk mutations, background execution, mail/SMTP ownership, exports/downloads/artifacts and audit context. The canonical Platform Super Admin exception is separately certified in Core and production-shaped FAIR CRM integration evidence.

Closure evidence is recorded in [projects/fair-crm/backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md](../projects/fair-crm/backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md). FAIR CRM PRs #83 and #84 close TI-07 and TI-09; Core PR #11 closes TI-08. The final FAIR CRM TI-09 head passed Development Standard Gate #268 and Prod-Path E2E #140 before merge. P0.1 completion does not waive the SaaS-impact gates for future changes; new organization-owned behavior must continue to ship with applicable cross-organization evidence.

The active cross-repository SaaS-readiness phase is **P0.2 — Organization lifecycle contract and SaaS onboarding**. [ADR-0006](decisions/0006-organization-lifecycle-and-onboarding.md) remains Proposed overall because suspension/closure/retention/backup decisions are still open, but the identity/onboarding subset OL-01 through OL-04 was explicitly approved for implementation on **2026-08-27**.

The approved workstream keeps `Organization` as the account boundary, keeps the direct single-organization user model, uses the existing `OrganizationAdmin` role for the first normal admin, preserves existing Platform Super Admin organization/user creation, and adds controlled public commercial signup plus Core-owned activation/set-password, password reset/change, one-time identity action tokens, shared password policy, session/credential invalidation and production identity-email capability. FAIR CRM remains a thin consumer of public Core identity APIs and will own the bridge/UI only.

The canonical implementation/resume checklist is [P0.2 Identity / SaaS Onboarding Implementation Tracker](P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md). **CORE-01 — PasswordPolicy is delivered** through Core PR #12. **CORE-02 — one-time identity action tokens is delivered** through Core PR #13. **CORE-03 — user-wide session/credential invalidation is delivered** through Core PR #14; Core CI #63 / run `33102833407` succeeded on final head `1b2dff1c5613405273ebe673210d522977e8d0c5` with 352 tests passing, and the PR merged to Core `main` as `63889c6c29a73b3224cdda0da21ed2bcc9ac9cb4`. Protected access tokens now fail closed when JWT `sid` is missing, revoked or belongs to a different subject. Password reset/change endpoints do not exist yet and retain explicit CORE-07/08 integration work. The next runtime phase is **CORE-04 — Core identity notifications / production email**.

The P0.2 lifecycle audit also confirmed that Core now uses direct `identity_users.organization_id` ownership for normal users; legacy memberships and membership invitations were removed by migration `20260817_0057_remove_memberships`. Organization suspend/delete remain SYSTEM-scope, Core delete remains a Core soft-delete, and the domain reactivation transition currently lacks a public organization API endpoint.

The [P0.2 lifecycle runtime audit](P0_2_LIFECYCLE_RUNTIME_AUDIT.md) confirms the still-open OL-07 execution gap: normal permission-protected starts are blocked after suspension, but already queued/running FAIR CRM scraper, enrichment, import and mail work generally continues from previously established organization-scoped job context without re-checking authoritative Core organization status. Import background execution explicitly trusts queue-time authorization, and outbound delivery checks product email-account activity rather than Core organization lifecycle state. This remains a **lifecycle-policy gap, not a P0.1 tenant-isolation regression**; onboarding approval does not authorize suspension/closure runtime changes.

## KYROX Core

Canonical detail: [projects/kyrox-core/PROJECT_STATUS.md](../projects/kyrox-core/PROJECT_STATUS.md)  
Active planning: [projects/kyrox-core/ROADMAP.md](../projects/kyrox-core/ROADMAP.md)

Core remains the reusable, product-agnostic SaaS backend. Identity, authentication, authorization, organization/user/role governance and shared platform services are implemented in Core. Products consume Core through public HTTP contracts; product domain logic does not belong in Core.

The P0.2 identity/onboarding primitives are an approved, product-driven Core workstream. CORE-01 established the shared 12–255 character password policy. CORE-02 added generic hash-only, expiring, single-use identity action tokens. CORE-03 added user-wide session/refresh invalidation plus server-side access-token session enforcement. **CORE-04 production identity notifications/email is next.**

The Core migration head remains `20260827_0063_identity_action_tokens`; CORE-03 required no schema migration. Current-state details belong in the Core project status, not in permanent standards or roadmap documents.

## FAIR CRM

Canonical detail: [projects/fair-crm/PROJECT_STATUS.md](../projects/fair-crm/PROJECT_STATUS.md)  
Current work queue: [projects/fair-crm/ROADMAP.md](../projects/fair-crm/ROADMAP.md)

FAIR CRM remains the active M4 product. Existing implementation includes the CRM foundations, data integration/import flows, operations/automation flows, mail delivery flows, quotation-related capabilities and a cost-catalog implementation. Its P0.1 tenant-isolation certification is complete; ongoing product work remains subject to the same SaaS-impact, authorization-scope and tenant-isolation delivery rules.

The FAIR CRM portion of the approved P0.2 workstream is the thin Core auth bridge plus signup/activation/forgot/reset/change-password UI and preservation of the existing Super Admin manual user-management flow. It starts after the dependent Core contracts are implemented and certified.

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