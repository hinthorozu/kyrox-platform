# KYROX Ecosystem

Overview of how KYROX repositories and responsibilities fit together.

## Ecosystem map

```
                    ┌─────────────────────┐
                    │   kyrox-platform    │
                    │  (decide & plan)    │
                    └──────────┬──────────┘
                               │ informs
                               ▼
                    ┌─────────────────────┐
                    │     kyrox-core      │
                    │  (shared backend)   │
                    └──────────┬──────────┘
                               │ consumed by
                               ▼
                    ┌─────────────────────┐
                    │      fair-crm       │
                    │   (first product)   │
                    └─────────────────────┘
```

## Repositories

### kyrox-platform (this repo)

- Vision, roadmap, milestones
- Architecture Decision Records (ADRs)
- Product plans and ecosystem documentation
- **No application code**

### kyrox-core

- Reusable SaaS backend platform
- Identity, tenancy, shared services
- Stable APIs and contracts for products
- **Does not depend on any product repository**

### fair-crm

- First KYROX product: CRM built on Core
- Product-specific domain logic, UI, and deployments
- **Depends on kyrox-core**

## Dependency rules

| From          | To            | Allowed |
|---------------|---------------|---------|
| kyrox-platform | kyrox-core    | No code dependency (documentation only) |
| kyrox-core     | fair-crm      | **No** — Core must not import or require product code |
| fair-crm       | kyrox-core    | **Yes** — Products consume Core APIs and libraries |

See [decisions/0002-core-product-separation.md](../decisions/0002-core-product-separation.md).

## What we are not adding (for now)

The following are **out of scope** until explicitly decided via ADR:

- kyrox-ui (shared UI library)
- kyrox-sdk (client SDK)
- kyrox-docs (public documentation site)

Additional repositories require a new ADR and roadmap update.

## Current focus

| Layer        | Repository     | Focus                          |
|--------------|----------------|--------------------------------|
| Planning     | kyrox-platform | M2 Identity scope & decisions  |
| Platform     | kyrox-core     | Identity implementation        |
| Product      | fair-crm       | Aligned with Core milestones   |

## Related documents

- [VISION.md](../VISION.md)
- [ROADMAP.md](../ROADMAP.md)
- [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md)
- [WORKFLOW.md](WORKFLOW.md)
