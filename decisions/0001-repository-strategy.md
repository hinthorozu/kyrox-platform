# ADR-0001: Repository strategy

- **Status:** Accepted
- **Date:** 2026-07-01
- **Deciders:** KYROX ecosystem maintainers

## Context

KYROX is a multi-product SaaS ecosystem. We need a clear split between **where decisions are recorded** and **where code lives**, without premature fragmentation into many repositories or a monolithic codebase that mixes strategy with application logic.

We also need a stable model that teams can follow before adding optional repos (UI libraries, SDKs, public docs sites).

## Decision

Use **three repositories** for now:

| Repository | Role |
|------------|------|
| **kyrox-platform** | Ecosystem strategy, roadmap, ADRs, product planning — documentation only |
| **kyrox-core** | Reusable SaaS backend platform |
| **fair-crm** | First product built on KYROX Core |

This three-repo structure is **final for now**. Additional repositories (e.g. kyrox-ui, kyrox-sdk, kyrox-docs) are not created until explicitly decided via a new ADR.

## Consequences

### Positive

- Clear home for planning vs platform vs product code
- kyrox-platform stays lightweight and reviewable
- Core and first product can evolve on independent release cycles
- Easy to explain to contributors: decide here, implement there

### Negative

- Cross-repo changes require coordination (mitigated by workflow in [WORKFLOW.md](../docs/WORKFLOW.md))
- No shared monorepo tooling for atomic cross-repo commits

### Neutral

- Public documentation site or SDK may warrant a fourth repo later; that is out of scope until ADR-approved

## Related

- [REPOSITORY_STRATEGY.md](../docs/REPOSITORY_STRATEGY.md)
- [ECOSYSTEM.md](../docs/ECOSYSTEM.md)
- [ADR-0002: Core and product separation](0002-core-product-separation.md)
