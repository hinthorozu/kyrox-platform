# Fair Stand

Fair / exhibition stand configurator product in the KYROX ecosystem.

**Code repository:** `https://github.com/hinthorozu/fair-stand`  
**Human/AI ecosystem documentation:** this tree under `kyrox-platform`  
**Runtime contracts:** `fair-stand` repository (`ITEM_CONTRACT.md`, change-gate)  
**Ecosystem status:** [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md)  
**Ownership ADR:** [../../ecosystem/decisions/0007-fair-stand-product-ownership.md](../../ecosystem/decisions/0007-fair-stand-product-ownership.md)

## Ownership

| Concern | Owner |
|---------|--------|
| Item identity (`itemKey`) and Category identity (`catalogKey`) | Fair Stand product |
| Item/Category relational data (`fair_stand_*`) | Fair Stand domain |
| Configurator runtime, catalog projection, scene, BOM | Fair Stand repository |
| Physical PostgreSQL + FastAPI process | Fair CRM **host** (not domain owner) |
| Auth / org UUID / session | KYROX Core via existing Fair CRM session |
| CRM customers, fairs, todos, `crm_*` tables | Fair CRM |

Fair Stand being embedded at CRM `/fair-stand` does **not** make Item data a CRM domain.

Catalog is a projection of Items. `catalogKey` is never Item identity.

## Canonical Fair Stand-only docs (this tree)

| Doc | Role |
|-----|------|
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Live product status |
| [ROADMAP.md](ROADMAP.md) | Product work queue |

Runtime Item contract and change-gate remain in the `fair-stand` repository because CI verifies them there.

## Related

- [Document Governance](../../ecosystem/DOCUMENT_GOVERNANCE.md)
- [Repository strategy](../../ecosystem/REPOSITORY_STRATEGY.md)
- [Core integration guide](../kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)
