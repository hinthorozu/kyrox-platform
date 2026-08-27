# KYROX Core — Project Status

Living status for KYROX Core. Ecosystem summary: [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md). Future work: [ROADMAP.md](ROADMAP.md).

| Field | Value |
|-------|-------|
| Last verified | **2026-08-27** |
| Repository mode | Stable platform baseline; fixes and reusable product-driven changes continue |
| Active ecosystem milestone | M4 — FAIR CRM v1 |
| Migration head in `main` | `20260821_0062_fair_crm_mail_send_operations_permissions` |
| Main CI | Core CI #57 green on P0.2 CORE-01 final head before merge |

## Current capability state

| Area | Status |
|------|--------|
| Identity and authentication | Implemented; shared 12–255 character `PasswordPolicy` now governs existing password-setting paths |
| Authorization | Implemented |
| Organization and user management | Implemented; normal users currently have direct single-organization ownership via `identity_users.organization_id` |
| Membership / invitation model | Removed by migration `20260817_0057_remove_memberships`; not a current Core capability |
| Roles and permissions | Implemented and evolved through later migrations |
| Audit | Implemented |
| Settings | Implemented |
| Background jobs | Implemented |
| Notifications | Implemented |
| Product authorization integration | Implemented |
| FAIR CRM permission catalog support | Implemented, including quotation, cost-catalog and mail-send-operation permissions |
| File storage | Planned |
| Caching | Demand-driven candidate |
| Observability | Demand-driven candidate |

## P0.2 identity / SaaS onboarding progress

The approved identity/onboarding implementation workstream is tracked in [P0.2 Identity / SaaS Onboarding Implementation Tracker](../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md).

**CORE-01 — PasswordPolicy is delivered.** Core PR #12 merged to `main` as `323cfa750a0c731bd15de11dfbd19e83858dc1f7` after CI #57 / run `33093204127` succeeded on final head `15db64cba636b340ee0841e25137d2bbea2dbd93`.

Delivered behavior:

- one reusable Core `PasswordPolicy` owns password length validation,
- production bounds are 12–255 characters,
- no forced upper/lower/digit/symbol composition rule was introduced,
- Argon2id remains the hashing/verification primitive rather than owning password policy,
- existing manual user create/update now use the shared policy,
- policy failures return a safe 422 contract without echoing the submitted password,
- existing login and existing Platform Super Admin manual user creation remain supported.

The next runtime phase is **CORE-02 — one-time identity action tokens**. Activation/reset/change-password endpoints do not exist yet; their later phases explicitly require reuse of the same PasswordPolicy.

## Organization lifecycle baseline

Current Core organization lifecycle behavior relevant to SaaS P0.2:

- organization creation is Platform Super Admin only,
- normal users are assigned directly to one organization and receive database-backed roles,
- the legacy `Owner` role is removed; `OrganizationAdmin` is the protected organization administrative role,
- organization suspend/delete are SYSTEM-scope and are not assignable to organization roles,
- normal authorization requires an active organization,
- Core organization delete is a soft-delete (`deleted_at`), not cross-product data deletion,
- the domain supports reactivation, but a public organization reactivation endpoint is not currently exposed,
- cross-repository product job/provider/data-retention effects are not implied by Core organization state changes.

The proposed cross-repository lifecycle contract is [ADR-0006](../../ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md). It remains **Proposed overall**; only the explicitly approved onboarding subset is authorized for implementation.

## Migration status

The former documentation baseline at `20260701_0025` is obsolete. The current Core migration tree reaches `20260821_0062_fair_crm_mail_send_operations_permissions`. Relevant identity evolution includes permission-scope enforcement, removal of the legacy Owner role, protected OrganizationAdmin governance, replacement of memberships with direct user organization ownership, direct user-role validation and later FAIR CRM permission additions.

The code repository is the implementation source for complete migration history. This document records the verified current head and capability-level state only.

## Integration contract

Products integrate with Core through public HTTP APIs. Product domain implementation stays in the product repository.

Canonical contract: [integrations/PRODUCT_INTEGRATION_GUIDE.md](integrations/PRODUCT_INTEGRATION_GUIDE.md).

## Update protocol

When Core changes materially:

1. Update this file with current capability truth and migration head when useful.
2. Update [CHANGELOG.md](CHANGELOG.md) for delivered history.
3. Refresh the summary in [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md).
4. Keep exact test counts and commit SHAs out of permanent standards and roadmap documents; implementation evidence may be recorded in project status/tracker history.
