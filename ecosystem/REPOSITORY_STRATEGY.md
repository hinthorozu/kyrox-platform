# Repository Strategy

Fixed KYROX repository model. Changes require a new ADR. Decision records: [ADR-0001](decisions/0001-repository-strategy.md) and [ADR-0007](decisions/0007-fair-stand-product-ownership.md).

## The repositories

| Repository | Purpose | Contains application code? | Contains Markdown docs? |
|------------|---------|----------------------------|-------------------------|
| **kyrox-platform** | Management and documentation hub | No | **Yes — only docs hub** |
| **kyrox-core** | Reusable SaaS backend platform | Yes | **No** |
| **fair-crm** | First CRM product on KYROX Core; also the physical host process/database for Fair Stand backend bounded contexts | Yes | **No** |
| **fair-stand** | Fair Stand configurator runtime (frontend/3D/BOM/persistence client) | Yes | Machine-readable contracts plus Fair Stand runtime docs required by that repo's change-gate |

All **ecosystem** and **cross-product** human documentation is maintained under this repository. See [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md). Fair Stand keeps its own runtime contracts in `fair-stand` because that repository's change-gate is machine-verified there; product ownership and ecosystem rules remain here.

## Responsibilities

### kyrox-platform

- Ecosystem vision, roadmap, status, workflow
- Cross-repo ADRs and repository strategy
- Project documentation trees under `projects/`
- Shared standards under `standards/`
- Historical archive under `archive/`

Nothing in this repo is deployed. It does not contain application `backend/` or `frontend/` packages.

### kyrox-core

- Authentication and identity
- Organization / membership multi-tenancy primitives
- Shared platform services (audit, settings, jobs, notifications)
- Public HTTP APIs and contracts consumed by products

Core is the shared backend foundation for all KYROX products. Documentation: [projects/kyrox-core/](../projects/kyrox-core/). Core must not contain Fair Stand Item/Category domain logic.

### fair-crm

- CRM domain features
- Product UI and CRM product database (`crm_` tables)
- Data integration / import / scraper product workflows
- Product deployment and configuration
- **Physical host** for Fair Stand Item/Category backend (`fair_stand_*` tables, Fair Stand catalog API) without owning that domain

fair-crm is the reference CRM product that validates Core in real use. Documentation: [projects/fair-crm/](../projects/fair-crm/).

### fair-stand

- Configurator runtime, catalog UI, scene/renderer, module behavior, client project persistence
- Item/Category **consumer** of the canonical DB/API aggregate
- Does not own Core auth and does not own CRM customer/fair/todo data

Documentation: [projects/fair-stand/](../projects/fair-stand/).

## Boundaries

1. **Platform vs implementation** — Decide and document in kyrox-platform; implement in kyrox-core, fair-crm, or fair-stand according to ownership.
2. **Core vs product** — Core never depends on products; products depend on Core via HTTP only ([ADR-0002](decisions/0002-core-product-separation.md)).
3. **Fair Stand vs Fair CRM** — CRM hosts Fair Stand UI and the Fair Stand bounded-context process/DB. Hosting is not Item domain ownership ([ADR-0007](decisions/0007-fair-stand-product-ownership.md)).
4. **No extra optional repos yet** — Do not create kyrox-ui, kyrox-sdk, kyrox-docs, or similar without an ADR. Fair Stand is an existing product repository recognized by ADR-0007, not a new optional platform library.
5. **No Markdown ecosystem-rule trees in Core/CRM** — Keep ecosystem/shared docs here. Fair Stand may keep runtime change-gate contracts in-repo.

## Naming and ownership

- Platform and Core use the `kyrox-` prefix; products use their product name (`fair-crm`, `fair-stand`).
- Fair Stand tables/APIs use the `fair_stand` / `/fair-stand` prefix. CRM tables use `crm_`.
- Cross-repo references use repository names and milestone IDs (for example M4, ADR-0001).

## When to add a repository

Adding another repository (beyond the four recorded here) requires:

1. An ADR in `ecosystem/decisions/`
2. Updates to [ROADMAP.md](ROADMAP.md) and this file
3. Explicit approval before creating the remote repository

## Related

- [ADR-0001: Repository strategy](decisions/0001-repository-strategy.md)
- [ADR-0002: Core and product separation](decisions/0002-core-product-separation.md)
- [ADR-0007: Fair Stand product ownership](decisions/0007-fair-stand-product-ownership.md)
- [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md)
- [STATUS.md](STATUS.md)
