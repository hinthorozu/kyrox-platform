# ADR-0002: Core and product separation

- **Status:** Accepted
- **Date:** 2026-07-01
- **Deciders:** KYROX ecosystem maintainers

## Context

KYROX Core is intended to be a **reusable backend foundation** for multiple SaaS products. If Core depends on a specific product (e.g. fair-crm), the platform becomes harder to reuse, test in isolation, and evolve without product-specific leakage.

Products, conversely, naturally depend on shared platform capabilities: identity, tenancy, billing hooks, and shared services.

## Decision

**Core and products are separate.**

1. **Core does not depend on products.** kyrox-core must not import, reference, or require code from fair-crm or any future product repository.
2. **Products depend on Core.** fair-crm (and future products) consume kyrox-core via stable APIs, packages, or contracts defined by Core.
3. **Product-specific logic stays in product repos.** Domain rules, product UI, and CRM-specific integrations belong in fair-crm, not in Core—unless generalized and promoted via ADR into Core.

## Consequences

### Positive

- Core can be developed, tested, and released independently
- Additional products can adopt Core without inheriting fair-crm assumptions
- Clear boundary for code review: platform vs product

### Negative

- Some logic may be duplicated briefly before promotion to Core is justified
- Requires discipline to avoid "just this once" product imports in Core

### Neutral

- Shared UI or client SDKs, if added later, should follow the same dependency direction: they may depend on Core contracts but Core must not depend on them for runtime behavior

## Verification

- Dependency graphs in kyrox-core must not list fair-crm or other product packages
- PRs to kyrox-core that introduce product-specific domain concepts should be rejected or refactored into fair-crm

## Related

- [ADR-0001: Repository strategy](0001-repository-strategy.md)
- [ECOSYSTEM.md](../REPOSITORY_STRATEGY.md)
- [REPOSITORY_STRATEGY.md](../REPOSITORY_STRATEGY.md)
