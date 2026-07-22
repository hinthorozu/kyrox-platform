# KYROX Core — Project Status

Living status for the Core platform. Ecosystem summary: [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md). Do not duplicate this matrix into standards or ADRs.

| Field | Value |
|-------|-------|
| Current version | v0.4.0 |
| Alembic head | `20260701_0025` |
| Repository status | Frozen — bug/security/performance fixes + CRM-driven reusable needs only |
| Platform baseline | Completed |
| Active ecosystem milestone | M4 (product delivery; Core frozen) |

## Capability matrix

| Area | Status |
|------|--------|
| Foundation | Completed — v0.1.0 |
| Identity | Completed — v0.2.0 |
| Authentication | Completed |
| Authorization | Completed — v0.2.1 Authorization Hardening |
| Organization | Completed — v0.3.0 |
| Membership | Completed — v0.3.0 |
| Audit Query API | Completed |
| Audit Event Write API | Completed |
| Product Authorization Check API | Completed |
| Settings Platform | Completed — v0.4.0 |
| Background Jobs Platform | Completed — v0.4.0 |
| Notifications Platform | Completed — v0.4.0 |
| FAIR CRM permission seeds | Completed — migration `20260701_0025` |
| File Storage | Planned |
| Caching | Planned |
| Observability | Planned |
| DevOps | Planned |

## Integration contract

Products integrate via HTTP only: [integrations/PRODUCT_INTEGRATION_GUIDE.md](integrations/PRODUCT_INTEGRATION_GUIDE.md).

As-built auth facts:

- JWT access claims: `sub`, `email`, `sid`, `exp`, `iat`, `jti`
- Organization scope: `X-Organization-Id` header (not embedded in JWT)
- Security ADR: [../../ecosystem/decisions/0003-identity-security-strategy.md](../../ecosystem/decisions/0003-identity-security-strategy.md)

## Roadmap

Freeze policy and future Core work: [ROADMAP.md](ROADMAP.md).  
Deferred items: [../../ecosystem/KNOWN_DEFERRED.md](../../ecosystem/KNOWN_DEFERRED.md).

## Update protocol

When Core ships a release or meaningful capability change:

1. Update this file’s version, alembic head, and capability matrix.
2. Update [CHANGELOG.md](CHANGELOG.md).
3. Refresh the Core summary section in [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md).
4. Do not paste test counts or commit SHAs into permanent standards.
