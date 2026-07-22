# KYROX Core

Reusable SaaS backend platform for KYROX products. Provides identity, organization/membership, authorization, and platform services (audit, settings, jobs, notifications).

**Code repository:** `https://github.com/hinthorozu/kyrox-core`  
**Documentation:** this tree under `kyrox-platform`  
**Ecosystem status:** [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md)

## Canonical Core docs

| Doc | Role |
|-----|------|
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Live Core status (SSoT) |
| [ROADMAP.md](ROADMAP.md) | Core roadmap and freeze policy |
| [CHANGELOG.md](CHANGELOG.md) | Core release history |
| [integrations/PRODUCT_INTEGRATION_GUIDE.md](integrations/PRODUCT_INTEGRATION_GUIDE.md) | Product HTTP integration contract |
| [decisions/](decisions/) | Core-specific ADRs |
| [../../standards/backend/../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md](../../standards/backend/../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md) | Layered backend standard |
| [../../ecosystem/decisions/0002-core-product-separation.md](../../ecosystem/decisions/0002-core-product-separation.md) | Core vs product separation |
| [../../ecosystem/decisions/0003-identity-security-strategy.md](../../ecosystem/decisions/0003-identity-security-strategy.md) | Identity security (as-built) |

## Current delivery (summary)

See [PROJECT_STATUS.md](PROJECT_STATUS.md) for live values.

- Platform baseline complete at **v0.4.0**
- Frozen during M4 except bug/security/performance fixes and reusable needs driven by products
- File Storage and several platform capabilities remain planned

## Boundaries

- Core must not contain product domain logic (CRM entities, fair-specific workflows).
- Products must not import Core Python modules or share Core database sessions.
- Organization context for org-scoped calls is supplied via `X-Organization-Id` (not JWT `org_id`).

## Historical designs

Pre-implementation design drafts for platform services live under [../../archive/kyrox-core/designs/](../../archive/kyrox-core/designs/). They are not normative.
