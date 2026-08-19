# KYROX Core

Reusable SaaS backend platform for KYROX products. Provides identity, organization/membership, authorization, and shared platform services.

**Code repository:** `https://github.com/hinthorozu/kyrox-core`  
**Human/AI documentation:** this tree under `kyrox-platform`  
**Ecosystem status:** [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md)

## Before Core-specific docs

Read [../../standards/README.md](../../standards/README.md) for shared KYROX standards applicable to the task. Core-specific documentation extends those shared rules; it must not create a second copy of reusable standards.

## Canonical Core docs

| Doc | Role |
|-----|------|
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Live Core status (SSoT) |
| [ROADMAP.md](ROADMAP.md) | Core future direction / freeze policy |
| [CHANGELOG.md](CHANGELOG.md) | Core delivered history |
| [integrations/PRODUCT_INTEGRATION_GUIDE.md](integrations/PRODUCT_INTEGRATION_GUIDE.md) | Product HTTP integration contract |
| [decisions/](decisions/) | Core-specific ADRs |
| [Backend Architecture Standards](../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md) | Shared layered backend standard |
| [Core vs product separation](../../ecosystem/decisions/0002-core-product-separation.md) | Cross-repository ownership boundary |
| [Identity security strategy](../../ecosystem/decisions/0003-identity-security-strategy.md) | Identity/security architecture |

## Current delivery

Do not duplicate current versions, migration heads or transient CI counts here. See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current implementation truth and [ROADMAP.md](ROADMAP.md) for future work.

## Boundaries

- Core must remain product-agnostic; product domain behavior belongs in product repositories.
- Products consume Core through public integration contracts and must not import Core runtime modules or share Core database sessions.
- Organization context for organization-scoped calls follows the canonical Core integration contract.

## Historical designs

Pre-implementation design drafts for platform services live under [../../archive/kyrox-core/designs/](../../archive/kyrox-core/designs/). They are historical, not normative.
