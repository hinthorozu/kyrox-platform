# Repository Strategy

Fixed three-repository model for KYROX. Changes require a new ADR. Decision record: [ADR-0001](decisions/0001-repository-strategy.md).

## The three repositories

| Repository | Purpose | Contains application code? | Contains Markdown docs? |
|------------|---------|----------------------------|-------------------------|
| **kyrox-platform** | Management and documentation hub | No | **Yes — only docs hub** |
| **kyrox-core** | Reusable SaaS backend platform | Yes | **No** |
| **fair-crm** | First product on KYROX Core | Yes | **No** |

All product and platform documentation is maintained under this repository. See [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md).

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

Core is the shared backend foundation for all KYROX products. Documentation: [projects/kyrox-core/](../projects/kyrox-core/).

### fair-crm

- CRM domain features
- Product UI and product database (`crm_` tables)
- Data integration / import / scraper product workflows
- Product deployment and configuration

fair-crm is the reference product that validates Core in real use. Documentation: [projects/fair-crm/](../projects/fair-crm/).

## Boundaries

1. **Platform vs implementation** — Decide and document in kyrox-platform; implement in kyrox-core or fair-crm.
2. **Core vs product** — Core never depends on products; products depend on Core via HTTP only ([ADR-0002](decisions/0002-core-product-separation.md)).
3. **No extra repos yet** — Do not create kyrox-ui, kyrox-sdk, kyrox-docs, or similar without an ADR.
4. **No Markdown in application repos** — Keep docs here; do not reintroduce `.md` trees into fair-crm or kyrox-core.

## Naming and ownership

- Platform and Core use the `kyrox-` prefix; the first product uses its product name (`fair-crm`).
- Cross-repo references use repository names and milestone IDs (for example M4, ADR-0001).

## When to add a repository

Adding a fourth repository requires:

1. An ADR in `ecosystem/decisions/`
2. Updates to [ROADMAP.md](ROADMAP.md) and this file
3. Explicit approval before creating the remote repository

## Related

- [ADR-0001: Repository strategy](decisions/0001-repository-strategy.md)
- [ADR-0002: Core and product separation](decisions/0002-core-product-separation.md)
- [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md)
- [STATUS.md](STATUS.md)
