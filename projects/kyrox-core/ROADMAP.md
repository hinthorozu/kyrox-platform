# KYROX Core Roadmap

KYROX Core is the reusable SaaS backend platform for KYROX products. This document contains **future direction and accepted planning only**. Current version, migration state, CI state and capability truth belong in [PROJECT_STATUS.md](PROJECT_STATUS.md).

## Guiding rule

Core remains product-agnostic. Product domain behavior stays in product repositories. Products integrate with Core through documented public HTTP APIs and contracts.

During FAIR CRM M4, Core is frozen against speculative platform development. Allowed work is limited to:

- bug fixes,
- security fixes,
- performance/reliability fixes,
- reusable platform needs proven by a real product requirement.

A reusable-looking capability must have an explicit ownership decision before migration or implementation. Do not move FAIR CRM business semantics into Core merely to make code reusable.

## Existing platform baseline

The existing Core baseline covers identity/authentication, organization/user/role governance, authorization, audit, settings, background jobs, notifications and product authorization integration. See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current implementation truth.

## Future platform candidates

These are candidates, not automatically scheduled work:

- file storage service,
- webhooks / event-bus capabilities,
- billing and subscription hooks,
- advanced platform administration and impersonation policies,
- caching where justified by measured need,
- observability and operational hardening,
- performance and scaling hardening.

A candidate becomes active work only through the KYROX planning/ADR flow or a documented reusable product need.

## Product-driven platform extraction

When FAIR CRM or a future product develops infrastructure that appears reusable:

1. Separate generic lifecycle/infrastructure from product business meaning.
2. Decide ownership: Core / product / provider-handler.
3. Document the public contract and migration impact.
4. Move only the generic capability; keep domain orchestration in the product.
5. Verify the real product path through public Core APIs.

## Related

- [PROJECT_STATUS.md](PROJECT_STATUS.md)
- [integrations/PRODUCT_INTEGRATION_GUIDE.md](integrations/PRODUCT_INTEGRATION_GUIDE.md)
- [../../ecosystem/ROADMAP.md](../../ecosystem/ROADMAP.md)
- [../../ecosystem/WORKFLOW.md](../../ecosystem/WORKFLOW.md)
- [../../ecosystem/decisions/0002-core-product-separation.md](../../ecosystem/decisions/0002-core-product-separation.md)
