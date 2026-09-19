# ADR-0007: Fair Stand product ownership and hosted Item catalog

- **Status:** Accepted
- **Date:** 2026-09-18
- **Deciders:** KYROX ecosystem maintainers

## Context

Fair Stand already exists as a runtime/configurator repository (`fair-stand`) and is hosted inside the Fair CRM UI. KYROX ADR-0001 described a three-repository model (`kyrox-platform`, `kyrox-core`, `fair-crm`) and did not record Fair Stand. That left a governance gap: Item/Category source-of-truth work had no canonical product owner.

Fair Stand Item and Category data must move from a static JavaScript master to relational PostgreSQL. ADR-0002 forbids putting product domain logic in Core. Hosting Fair Stand inside the CRM UI does not make CRM the Item domain owner.

## Decision

1. **Fair Stand is a KYROX product.** Canonical Item identity is `itemKey`. Canonical Category identity is the database-generated integer `id`. Catalog is a projection of Items, not a second Item master.
2. **Documentation** lives under `projects/fair-stand/` in `kyrox-platform`.
3. **Runtime/frontend code** lives in the existing `fair-stand` repository.
4. **Item/Category backend** is a Fair Stand bounded context **physically hosted** in the Fair CRM application and Fair CRM PostgreSQL database, using `fair_stand_*` tables only.
5. **Physical hosting is not domain ownership.** Fair CRM remains the shell/host and owns `crm_*` CRM domain tables. Fair Stand owns Item/Category semantics, seed, and catalog APIs under `/api/v1/fair-stand/...`.
6. **No Core Item domain.** Core remains auth, organization context, and RBAC. Products consume Core over HTTP. No new login, gateway, or service port is required.
7. **No CRM business foreign keys** to `fair_stand_*` tables and no `fair_stand_*` foreign keys to `crm_*` tables.
8. **Item catalog is global product data** for this migration. Tables do not carry `organization_id`. Authenticated CRM session access is reused; no new permission code is invented solely for this cutover.
9. **ADR-0001 is extended, not replaced.** Optional extra repos (`kyrox-ui`, `kyrox-sdk`, public docs sites) still require a future ADR. Fair Stand is recognized as an existing product repository, not as a newly created optional platform repo.

## Consequences

- Cross-repo delivery order for Item catalog: platform docs → Fair CRM hosted backend/API → Fair Stand frontend bootstrap/cutover.
- Fair CRM quality/feature-contract machinery applies to the hosted API because the code lives in `fair-crm`.
- Fair Stand change-gate/CI applies to the configurator runtime.
- Category/Item physical DELETE remains forbidden at product level because KYROX FK policy is CASCADE/CASCADE; deactivate with `is_active` instead.

## Related

- [ADR-0001: Repository strategy](0001-repository-strategy.md)
- [ADR-0002: Core and product separation](0002-core-product-separation.md)
- [REPOSITORY_STRATEGY.md](../REPOSITORY_STRATEGY.md)
- [projects/fair-stand/README.md](../../projects/fair-stand/README.md)
