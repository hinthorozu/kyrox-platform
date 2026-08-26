# KYROX Ecosystem Status

Single source of truth for **cross-repository current state**. Detailed product/Core status lives in the project status files linked below. Do not duplicate sprint histories, test-count histories or roadmap queues here.

| Field | Value |
|-------|-------|
| Active milestone | **M4 — FAIR CRM v1** |
| Core policy | Frozen for speculative product work; bug/security/performance fixes and reusable product-driven platform needs are allowed |
| Documentation hub | `kyrox-platform` |
| Implementation repos | `kyrox-core`, `fair-crm` |
| Last ecosystem sync | **2026-08-26** |

## SaaS readiness

**P0.1 Tenant Isolation Certification is DONE.** FAIR CRM organization-owned paths are certified across direct/nested resource access, derived relationships, bulk mutations, background execution, mail/SMTP ownership, exports/downloads/artifacts and audit context. The canonical Platform Super Admin exception is separately certified in Core and production-shaped FAIR CRM integration evidence.

Closure evidence is recorded in [projects/fair-crm/backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md](../projects/fair-crm/backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md). FAIR CRM PRs #83 and #84 close TI-07 and TI-09; Core PR #11 closes TI-08. The final FAIR CRM TI-09 head passed Development Standard Gate #268 and Prod-Path E2E #140 before merge. P0.1 completion does not waive the SaaS-impact gates for future changes; new organization-owned behavior must continue to ship with applicable cross-organization evidence.

The next cross-repository SaaS-readiness phase is **P0.2 — Organization lifecycle contract and SaaS onboarding decisions**. P0.2 is currently a **decision/architecture gate, not runtime implementation**. [ADR-0006](decisions/0006-organization-lifecycle-and-onboarding.md) is Proposed and records the verified current Core model plus unresolved lifecycle/onboarding choices. No new Tenant entity, Owner role, self-service destructive organization authority, membership model or invitation flow is approved by that proposal.

The P0.2 audit confirmed that Core now uses direct `identity_users.organization_id` ownership for normal users; legacy memberships and membership invitations were removed by migration `20260817_0057_remove_memberships`. Organization creation is currently Platform Super Admin only, organization suspend/delete are SYSTEM-scope, Core delete is a Core soft-delete, and the domain reactivation transition currently lacks a public organization API endpoint. Cross-repository FAIR CRM job/provider/data-retention behavior therefore requires an explicit lifecycle contract before implementation.

## KYROX Core

Canonical detail: [projects/kyrox-core/PROJECT_STATUS.md](../projects/kyrox-core/PROJECT_STATUS.md)

Core remains the reusable, product-agnostic SaaS backend. Identity, authentication, authorization, organization/user/role governance and shared platform services are implemented in Core. Products consume Core through public HTTP contracts; product domain logic does not belong in Core.

The migration history has advanced substantially beyond the old `20260701_0025` documentation baseline and currently reaches `20260821_0062_fair_crm_mail_send_operations_permissions`. Current-state details belong in the Core project status, not in permanent standards or roadmap documents.

## FAIR CRM

Canonical detail: [projects/fair-crm/PROJECT_STATUS.md](../projects/fair-crm/PROJECT_STATUS.md)  
Current work queue: [projects/fair-crm/ROADMAP.md](../projects/fair-crm/ROADMAP.md)

FAIR CRM remains the active M4 product. Existing implementation includes the CRM foundations, data integration/import flows, operations/automation flows, mail delivery flows, quotation-related capabilities and a cost-catalog implementation. Its P0.1 tenant-isolation certification is complete; ongoing product work remains subject to the same SaaS-impact, authorization-scope and tenant-isolation delivery rules.

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
