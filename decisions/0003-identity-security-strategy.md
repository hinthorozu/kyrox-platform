# ADR-0003: Identity security strategy

- **Status:** Accepted
- **Date:** 2026-07-01
- **Deciders:** KYROX ecosystem maintainers

## Context

M2 Identity requires concrete security choices for authentication and session management in **kyrox-core**. Without an agreed strategy, implementation may diverge across services or embed product-specific assumptions.

KYROX Core must provide a **product-independent** identity layer. **Organization** is the account and authorization boundary in the domain model. The term *tenant* may be used only in infrastructure or deployment documentation (e.g. database isolation, row-level scoping), not as a first-class domain entity alongside organization.

Products such as fair-crm consume Core identity APIs and JWT contracts; they must not define Core security behavior. This ADR locks decisions for the first M2 implementation so kyrox-core can proceed with a consistent, reviewable baseline.

## Decision

Adopt the following **Identity Security Strategy** for KYROX Core:

| # | Area | Decision |
|---|------|----------|
| 1 | Password hashing | **Argon2id** |
| 2 | Access token format | **JWT** |
| 3 | Access token lifetime | **15 minutes** |
| 4 | Refresh token lifetime | **30 days** |
| 5 | Refresh token storage | **Hashed in database** (never store plaintext) |
| 6 | Refresh token rotation | **Enabled** — issue new refresh token on each refresh; invalidate previous |
| 7 | Token revocation | **Supported** — refresh tokens and sessions can be revoked server-side |
| 8 | Logout | **Revoke refresh token** for the session being terminated |
| 9 | Multi-device sessions | **Supported** — each device/session has its own refresh token record |
| 10 | Email verification | **Required** before full account activation |
| 11 | Password reset | **Token-based**, short-lived single-use reset tokens |
| 12 | MFA | **Planned for future** — not in first M2 implementation |
| 13 | Secrets management | **Environment-based** initially; migrate to a **secret manager** later |
| 14 | JWT claims (access token) | `sub`, `email`, `org_id`, `is_super_admin`, `exp`, `iat`, `jti` |

### JWT claims

Access tokens issued by Core include:

| Claim | Purpose |
|-------|---------|
| `sub` | Subject — stable user identifier |
| `email` | Authenticated user's email (for display and audit; authorization still uses `org_id` and roles) |
| `org_id` | Active organization context — account boundary for authorization |
| `is_super_admin` | Platform-level super-admin flag (strictly scoped; false for normal users) |
| `exp` | Expiration time |
| `iat` | Issued-at time |
| `jti` | Unique token ID — supports revocation lists and audit correlation |

Products must treat `org_id` as the scope for tenant-scoped data. Core does not embed product-specific claims in the baseline JWT; products may map `org_id` to their own resources via Core APIs.

### Organization as account boundary

- Users belong to one or more **organizations**.
- Authorization and data scoping use **organization** as the domain boundary.
- Infrastructure docs may refer to multi-tenant deployment patterns; the Core domain model uses **organization**, not a parallel *tenant* entity.

## Consequences

### Positive

- Single, documented security baseline for all KYROX products
- Short-lived access tokens limit exposure; refresh rotation reduces replay risk
- Hashed refresh tokens protect against database compromise
- Email verification and token-based password reset align with common SaaS expectations
- Multi-device sessions supported without sharing one long-lived token across devices
- JWT claim set is minimal and product-agnostic

### Negative

- Refresh token rotation requires careful handling of race conditions (parallel refresh requests)
- 15-minute access tokens increase refresh traffic; clients must implement refresh reliably
- Email verification adds friction before activation; requires outbound email infrastructure or stub in early dev
- Environment-based secrets are weaker than a dedicated secret manager until migration

### Neutral

- MFA deferred — acceptable for M2 v1 but should be ADR-updated before high-assurance deployments
- `is_super_admin` in JWT requires strict issuance rules and short access token lifetime to limit blast radius

## Security rationale

**Argon2id** — Memory-hard password hashing resistant to GPU/ASIC attacks; recommended by OWASP for new systems.

**JWT access tokens (15 min)** — Stateless verification for APIs with bounded lifetime; stolen access tokens expire quickly.

**Refresh tokens (30 days, hashed, rotated)** — Longer convenience for users without storing long-lived secrets in clients as plaintext bearer tokens. Hashing at rest prevents mass token theft from DB leaks. Rotation detects reuse and limits impact of a stolen refresh token.

**Revocation and logout** — Server-side refresh token records allow immediate session termination; access tokens remain valid until expiry unless a blocklist/denylist is added later (optional enhancement).

**Multi-device sessions** — Separate refresh token per device/session enables selective logout without invalidating all devices.

**Email verification** — Reduces account takeover via mistyped or unowned email addresses; gates full activation until ownership is proven.

**Password reset tokens** — Short-lived, single-use tokens avoid sending passwords by email and limit window for interception.

**Secrets** — Environment variables suffice for initial development and small deployments; secret manager migration is planned before production hardening at scale.

**Claim minimalism** — Standard claims plus `org_id` and `is_super_admin` support multi-org SaaS without product-specific JWT pollution per [ADR-0002](0002-core-product-separation.md).

## Implementation impact for kyrox-core

kyrox-core must implement:

1. **User credentials** — Argon2id hash storage; no plaintext passwords.
2. **Token service** — Issue JWT access tokens with the defined claims; sign with a secret from environment (key rotation strategy documented in Core).
3. **Refresh token store** — Persist hashed refresh tokens with metadata (user id, org context, device/session id, expiry, revocation flag).
4. **Refresh endpoint** — Validate refresh token, rotate (invalidate old, issue new), return new access + refresh pair.
5. **Revocation API** — Revoke by refresh token id or session id; logout calls revocation for current session.
6. **Email verification flow** — Registration creates unverified user; verification token/link activates account; unverified users have restricted capabilities defined in Core.
7. **Password reset flow** — Generate short-lived reset token; validate once; update password with new Argon2id hash; invalidate outstanding reset tokens.
8. **Organization context** — Access token `org_id` reflects active organization; switching org re-issues tokens (product or Core endpoint TBD in Core design docs).
9. **Super admin** — Separate issuance path for `is_super_admin`; audit all use.

Products (e.g. fair-crm) **consume** tokens and Core auth middleware; they do **not** implement hashing, refresh storage, or JWT signing.

## Out of scope

- **MFA / TOTP / WebAuthn** — Planned; requires future ADR when scheduled.
- **FAIR CRM-specific rules** — e.g. CRM role names, deal-level permissions, field-level security.
- **OAuth2 social login / SSO** — Not part of M2 baseline unless added via separate ADR.
- **Public key JWT (JWKS) rotation automation** — May follow in Core ops docs; signing secret in env is sufficient for M2 start.
- **Access token denylist** — Optional later; 15-minute lifetime is primary mitigation for M2.
- **Secret manager integration** — Planned migration; not required for initial M2 development environment.

## Related

- [ADR-0002: Core and product separation](0002-core-product-separation.md)
- [M2 Identity](../milestones/M2_IDENTITY.md)
- [ROADMAP.md](../ROADMAP.md)
