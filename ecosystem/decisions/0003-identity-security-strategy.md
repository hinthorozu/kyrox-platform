# ADR-0003: Identity security strategy

- **Status:** Accepted (as-built amendment 2026-07-22)
- **Date:** 2026-07-01
- **Deciders:** KYROX ecosystem maintainers

## Context

M2 Identity required concrete security choices for authentication and session management in **kyrox-core**. Products consume Core identity APIs; they must not define Core security behavior.

**As-built note (2026-07-22):** The original decision draft included `org_id` and `is_super_admin` inside the JWT. Shipped Core does **not** embed organization in the access token. Organization scope is supplied per request via `X-Organization-Id`. This ADR records the **shipped** contract. See [PRODUCT_INTEGRATION_GUIDE.md](../../projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md).

## Decision

Adopt the following **Identity Security Strategy** for KYROX Core:

| # | Area | Decision |
|---|------|----------|
| 1 | Password hashing | **Argon2id** |
| 2 | Access token format | **JWT** |
| 3 | Access token lifetime | **15 minutes** |
| 4 | Refresh token lifetime | **30 days** |
| 5 | Refresh token storage | **Hashed in database** (never store plaintext) |
| 6 | Refresh token rotation | **Enabled** |
| 7 | Token revocation | **Supported** |
| 8 | Logout | **Revoke refresh token** for the session |
| 9 | Multi-device sessions | **Supported** |
| 10 | Email verification | **Required** before full activation — *implementation deferred; see KNOWN_DEFERRED* |
| 11 | Password reset | **Token-based** — *implementation deferred; see KNOWN_DEFERRED* |
| 12 | MFA | **Planned for future** |
| 13 | Secrets management | **Environment-based** initially; secret manager later |
| 14 | JWT claims (access token, as-built) | `sub`, `email`, `sid`, `exp`, `iat`, `jti` |
| 15 | Organization context | **`X-Organization-Id` header** (not a JWT claim) |

### JWT claims (as-built)

| Claim | Purpose |
|-------|---------|
| `sub` | User id |
| `email` | Authenticated email |
| `sid` | Session id |
| `exp` / `iat` | Expiry / issued-at |
| `jti` | Unique token id |

### Organization as account boundary

- Users belong to one or more **organizations**.
- Org-scoped Core and product routes require `Authorization: Bearer …` and `X-Organization-Id`.
- Domain language uses **organization**, not a parallel *tenant* entity (see Core ADR on organization naming).

## Consequences

### Positive

- Single documented security baseline for KYROX products
- Short-lived access tokens; refresh rotation reduces replay risk
- Header-based org context supports multi-org sessions without re-issuing JWTs on every org switch

### Negative / deferred

- Email verification and password reset remain required by strategy but are deferred in implementation ([KNOWN_DEFERRED.md](../KNOWN_DEFERRED.md))
- Access tokens remain valid until expiry unless a denylist is added later

## Related

- [PRODUCT_INTEGRATION_GUIDE.md](../../projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)
- [ADR-0002](0002-core-product-separation.md)
- [ADR-0004](0004-audit-service-strategy.md)
- Historical design draft: [IDENTITY_PLATFORM_DESIGN.md](../../archive/kyrox-core/designs/IDENTITY_PLATFORM_DESIGN.md)
