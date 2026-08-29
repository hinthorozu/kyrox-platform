# KYROX Core Roadmap

KYROX Core is the reusable SaaS backend platform for KYROX products. This document contains **future direction and accepted planning only**. Current version, migration state, CI state and capability truth belong in [PROJECT_STATUS.md](PROJECT_STATUS.md).

## Guiding rule

Core remains product-agnostic. Product domain behavior stays in product repositories. Products integrate with Core through documented public HTTP APIs and contracts.

The cross-repository [KYROX SaaS Readiness Roadmap](../../ecosystem/SAAS_ROADMAP.md) defines SaaS sequencing and ownership guardrails. It does not automatically activate Core candidates: billing/subscription, generic metering, observability or other reusable SaaS infrastructure still requires a proven product need and the applicable ownership/planning/ADR decision.

During FAIR CRM M4, Core is frozen against speculative platform development. Allowed work is limited to:

- bug fixes,
- security fixes,
- performance/reliability fixes,
- reusable platform needs proven by a real product requirement.

A reusable-looking capability must have an explicit ownership decision before migration or implementation. Do not move FAIR CRM business semantics into Core merely to make code reusable.

## Existing platform baseline

The existing Core baseline covers identity/authentication, organization/user/role governance, authorization, audit, settings, background jobs, notifications and product authorization integration. See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current implementation truth.

## Active product-driven platform work

### P0.2 Identity / SaaS onboarding foundation — ACTIVE 2026-08-27

The ecosystem approved the reusable identity/onboarding subset of ADR-0006 as a real FAIR CRM commercial requirement. This work is therefore allowed under the M4 Core freeze and is not speculative platform expansion.

Canonical tracker: [../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md](../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md)

Core owns the generic runtime primitives:

- shared production password policy across every password-setting path,
- hashed, expiring, single-use identity action tokens,
- user-wide session/credential invalidation after password reset/change,
- production Core identity email/notification capability,
- controlled public organization signup,
- atomic first-user bootstrap using the existing `OrganizationAdmin` role,
- account activation/set-password,
- forgot/reset password,
- authenticated self-service password change,
- security/audit evidence without raw credentials/tokens.

Binding compatibility constraints:

- keep existing Platform Super Admin `POST /organizations`,
- keep existing Super Admin/manual user creation and admin-supplied password mode,
- do not add an Owner role,
- do not restore removed membership/invitation semantics,
- do not place FAIR CRM product business semantics in Core,
- do not claim runtime delivery until implementation/test/CI evidence actually merges.

Execution status:

- **CORE-01 — PasswordPolicy: DONE 2026-08-27.** Shared 12–255 character password policy is used by current password-setting paths while existing Super Admin/manual provisioning remains available.
- **CORE-02 — One-time identity action tokens: DONE 2026-08-27.** Hash-only, expiring, single-use activation/reset token primitives with supersession and replay protection are delivered.
- **CORE-03 — Session / credential invalidation: DONE 2026-08-27.** Reusable user-wide session/refresh revocation and server-side access-token session enforcement are delivered; both password-reset and authenticated password-change integrations now invoke the primitive.
- **CORE-04 — Core identity notifications / production email: DONE 2026-08-27.** Platform-scoped identity notifications, Core-owned SMTP delivery, identity templates, platform idempotency and redacted delivery logging are delivered independently of FAIR CRM tenant mail configuration.
- **CORE-05 — Public signup + atomic bootstrap: DONE 2026-08-28.** Controlled public signup now creates a non-operational pending organization, inactive first user with no password hash, existing protected `OrganizationAdmin` assignment, hash-only activation token and platform identity notification atomically while preserving existing operator provisioning.
- **CORE-06 — Activation: DONE 2026-08-28.** Single-use activation/set-password now consumes the account-activation token atomically, applies the shared password policy and Argon2id hashing, activates the pending user and organization together, records secret-safe audit evidence and returns the user to login without issuing an implicit session.
- **CORE-07 — Forgot/reset password: DONE 2026-08-29.** Enumeration-resistant recovery, reset-token delivery/consumption, resend cooldown/supersession, shared password policy, user-wide session/credential invalidation and secret-safe audit evidence are delivered.
- **CORE-08 — Authenticated password change: DONE 2026-08-29.** Authenticated users can verify the current credential, apply the shared password policy to a distinct new password, atomically replace the hash, revoke all prior sessions/refresh credentials and emit secret-safe audit evidence without an implicit replacement session.
- **CORE-09 — Core security/adversarial certification: DONE 2026-08-29.** The completed onboarding/credential surface passed final-head adversarial and regression certification, including signup privilege-injection resistance and cross-organization activation isolation.
- Core runtime work for this approved onboarding slice is complete; the next execution phase is the FAIR CRM thin auth bridge in the canonical tracker.

## Future platform candidates

These are candidates, not automatically scheduled work:

- file storage service,
- webhooks / event-bus capabilities,
- billing and subscription hooks,
- advanced platform administration and impersonation policies,
- caching where justified by measured need,
- observability and operational hardening,
- performance and scaling hardening.

A candidate becomes active work only through the KYROX planning/ADR flow or a documented reusable product need.

## Product-driven platform extraction

When FAIR CRM or a future product develops infrastructure that appears reusable:

1. Separate generic lifecycle/infrastructure from product business meaning.
2. Decide ownership: Core / product / provider-handler.
3. Document the public contract and migration impact.
4. Move only the generic capability; keep domain orchestration in the product.
5. Verify the real product path through public Core APIs.

## Related

- [PROJECT_STATUS.md](PROJECT_STATUS.md)
- [integrations/PRODUCT_INTEGRATION_GUIDE.md](integrations/PRODUCT_INTEGRATION_GUIDE.md)
- [../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md](../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md)
- [../../ecosystem/SAAS_ROADMAP.md](../../ecosystem/SAAS_ROADMAP.md)
- [../../ecosystem/ROADMAP.md](../../ecosystem/ROADMAP.md)
- [../../ecosystem/WORKFLOW.md](../../ecosystem/WORKFLOW.md)
- [../../ecosystem/decisions/0002-core-product-separation.md](../../ecosystem/decisions/0002-core-product-separation.md)
- [../../ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md](../../ecosystem/decisions/0006-organization-lifecycle-and-onboarding.md)
