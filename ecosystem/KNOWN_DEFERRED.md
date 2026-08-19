# Known Deferred Work

Intentionally postponed ecosystem work. These items are **not active roadmap priority unless promoted through an explicit product/planning/ADR decision**.

Current state: [STATUS.md](STATUS.md).  
Ecosystem direction: [ROADMAP.md](ROADMAP.md).  
Fair CRM active/future queue: [../projects/fair-crm/ROADMAP.md](../projects/fair-crm/ROADMAP.md).

## Authentication / identity candidates

Potential future Core work, activated only by an explicit requirement:

- email verification,
- password reset,
- MFA,
- login rate limiting / account lockout,
- refresh-token reuse detection,
- device/session-management UX and policy hardening.

The canonical identity/security architecture remains [ADR-0003](decisions/0003-identity-security-strategy.md).

## Shared platform capability candidates

Demand-driven candidates include:

- file storage,
- caching where measured need exists,
- event bus / webhooks as a reusable platform capability,
- metrics / OpenTelemetry / distributed tracing,
- broader platform-level billing/subscription hooks,
- additional operational/release automation.

Candidate does not mean scheduled. See [../projects/kyrox-core/ROADMAP.md](../projects/kyrox-core/ROADMAP.md).

## Open ownership decisions — do not infer silently

Two infrastructure areas were previously captured in a July “Platform Ownership Review”. The general ownership rule is already canonical in [ADR-0002](decisions/0002-core-product-separation.md) and the ecosystem/project workflow, so the old review document is historical. **The following extraction decisions themselves remain open until explicitly decided:**

### Generic email delivery infrastructure

Evaluate whether provider-account abstraction, generic delivery execution, retry/rate-limit mechanics and provider-neutral delivery status should be promoted to Core. FAIR CRM recipient selection, CRM templates/context, exclusions and CRM activity/history remain product semantics.

Do not move or duplicate code until an explicit ownership decision is made from the actual current implementation.

### Generic Operation Engine infrastructure

Evaluate whether lifecycle/capability primitives such as start/cancel/pause/resume/retry/schedule and generic run/job state are sufficiently product-independent to promote to Core. FAIR CRM automation types, handlers, source selection and domain results remain product-owned.

Do not move or duplicate code until an explicit ownership decision is made from the actual current implementation.

Historical proposal: [../archive/ecosystem/PLATFORM_OWNERSHIP_REVIEW_2026-07-23.md](../archive/ecosystem/PLATFORM_OWNERSHIP_REVIEW_2026-07-23.md).

## FAIR CRM deferred specifications

FAIR CRM detailed deferred specifications live under its project tree and are surfaced through the canonical product roadmap. Do not duplicate individual product backlog items here.

See [../projects/fair-crm/ROADMAP.md](../projects/fair-crm/ROADMAP.md).

## Promotion rule

When a deferred item becomes real work:

1. establish owner and scope,
2. record any required ADR/decision,
3. add it to the appropriate roadmap,
4. implement in the owning code repository,
5. update status/changelog after delivery.
