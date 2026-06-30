# M2 — Identity

- **Status:** Active
- **Primary repository:** kyrox-core

## Goal

Deliver identity and access foundations in KYROX Core so products can authenticate users, manage organizations, and enforce authorization in a multi-tenant SaaS model. **Organization** is the account boundary in the domain model; *tenant* is infrastructure terminology only.

## Scope (implementation in kyrox-core)

- User model and registration/authentication flows
- Organization model, membership, and active org context (`org_id` in tokens)
- Security strategy per [ADR-0003](../decisions/0003-identity-security-strategy.md):
  - Argon2id password hashing
  - JWT access tokens (15-minute lifetime; claims: `sub`, `email`, `org_id`, `is_super_admin`, `exp`, `iat`, `jti`)
  - Refresh tokens (30-day lifetime, hashed in database, rotation enabled)
  - Token revocation and logout (revoke refresh token)
  - Multi-device sessions (one refresh token record per session/device)
  - Email verification required before full activation
  - Token-based, short-lived password reset
  - Secrets via environment variables initially
- Authorization model (roles/permissions scoped to organization)
- APIs or modules exposed for product consumption

## Out of scope (this milestone)

- MFA (planned for future ADR — not first implementation)
- Secret manager integration (planned migration from env-based secrets)
- FAIR CRM-specific security or authorization rules
- Full CRM features (fair-crm — M4)
- Complete platform services catalog (M3)
- Public docs site or client SDK repos

## Dependencies

- M1 Foundation completed (repo strategy and separation agreed)

## Success criteria

- A product (or integration test harness) can authenticate a user and operate within a tenant context using Core only
- Core remains free of fair-crm imports ([ADR-0002](../decisions/0002-core-product-separation.md))
- Milestone-worthy release tagged in kyrox-core when complete

## Planning references

- [ADR-0003: Identity security strategy](../decisions/0003-identity-security-strategy.md)
- [ADR-0002: Core and product separation](../decisions/0002-core-product-separation.md)
- [VISION.md](../VISION.md) — Core-first, product-independent foundation
- [WORKFLOW.md](../docs/WORKFLOW.md) — Decide in platform, implement in Core
- [ROADMAP.md](../ROADMAP.md)

## Next (after completion)

→ [M3 Platform Services](M3_PLATFORM_SERVICES.md)
