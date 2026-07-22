# Repository Strategy

This document describes the **fixed three-repository model** for KYROX. The structure is final for now; changes require a new ADR.

## The three repositories

| Repository        | Purpose | Contains code? |
|-------------------|---------|----------------|
| **kyrox-platform** | Management and decision center | No — documentation only |
| **kyrox-core**     | Reusable SaaS backend platform   | Yes — shared backend |
| **fair-crm**       | First product on KYROX Core      | Yes — product application |

## Responsibilities

### kyrox-platform

- Roadmap and milestone definitions
- Vision and ecosystem documentation
- ADRs and product plans
- Workflow and process definitions

Nothing in this repo is deployed. It does not contain `backend/`, `frontend/`, or application packages.

### kyrox-core

- Authentication and identity
- Multi-tenancy primitives
- Shared platform services (as milestones progress)
- APIs and contracts consumed by products

Core is the **single shared backend foundation** for all KYROX products.

### fair-crm

- CRM domain features
- Product-specific UI and integrations
- Product deployment and configuration

fair-crm is the **reference product** that validates Core in real use.

## Boundaries

1. **Platform vs implementation** — Decide in kyrox-platform; implement in kyrox-core or fair-crm.
2. **Core vs product** — Core never depends on products; products depend on Core ([ADR-0002](../decisions/0002-core-product-separation.md)).
3. **No extra repos yet** — Do not create kyrox-ui, kyrox-sdk, kyrox-docs, or similar without an ADR.

## Naming and ownership

- Repository names use the `kyrox-` prefix for platform and core; the first product uses its product name (`fair-crm`).
- Cross-repo references in docs use repository names and milestone IDs (e.g. M2, ADR-0001).

## When to add a repository

Adding a fourth repository (e.g. shared UI, SDK, docs site) requires:

1. A proposal documented as an ADR in kyrox-platform
2. Updates to [ECOSYSTEM.md](ECOSYSTEM.md) and [ROADMAP.md](../ROADMAP.md)
3. Explicit approval before creating the remote repository

## Related ADRs

- [ADR-0001: Repository strategy](../decisions/0001-repository-strategy.md)
- [ADR-0002: Core and product separation](../decisions/0002-core-product-separation.md)
