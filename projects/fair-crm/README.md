# Fair CRM

First KYROX product: multi-tenant fair / exhibition CRM built on KYROX Core identity and platform services.

**Code repository:** `https://github.com/hinthorozu/fair-crm`  
**Documentation:** this tree under `kyrox-platform`  
**Ecosystem status:** [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md)  
**Active milestone:** [MILESTONE_M4.md](MILESTONE_M4.md)

## Canonical product docs

| Doc | Role |
|-----|------|
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Live product status (SSoT) |
| [ROADMAP.md](ROADMAP.md) | Product ops / sprint backlog |
| [CHANGELOG.md](CHANGELOG.md) | Product release history |
| [CONSTITUTION.md](CONSTITUTION.md) | Binding development constitution / DoD |
| [VISION.md](VISION.md) | Long-term product vision |
| [architecture/ARCHITECTURE.md](architecture/ARCHITECTURE.md) | Service layout and modules |
| [decisions/DECISIONS.md](decisions/DECISIONS.md) | Product ADRs |
| [frontend/FRONTEND_UI_MASTER_STANDARD.md](frontend/FRONTEND_UI_MASTER_STANDARD.md) | UI master standard |
| [import/IMPORT_ARCHITECTURE.md](import/IMPORT_ARCHITECTURE.md) | Import / data integration architecture |
| [integrations/INTEGRATION_WITH_CORE.md](integrations/INTEGRATION_WITH_CORE.md) | Core HTTP integration notes |
| [ops/DEV_RUNTIME.md](ops/DEV_RUNTIME.md) | Local development runtime |

## Current delivery (summary)

Do not treat this paragraph as status SSoT — see [PROJECT_STATUS.md](PROJECT_STATUS.md).

- Foundations: Customers, Fairs, Participations, Contacts, Activities
- Scraper adapter management and Run v2 handoff completed
- Import / Data Integration engine, merge, preview, Excel adapter completed
- Admin database backups MVP completed
- Responsive UniversalDataTable standard completed
- Next planned sprint: **CSV Source Adapter (09.3)**

## Boundaries

- Product code and `crm_` schema live in the `fair-crm` code repo.
- Platform-generic capabilities must be evaluated under ecosystem ADR-0002 / product ADR-009 before building inside Fair CRM.
- Integrate with Core only through public HTTP APIs.

## Related ecosystem docs

- [DOCUMENT_GOVERNANCE.md](../../ecosystem/DOCUMENT_GOVERNANCE.md)
- [WORKFLOW.md](../../ecosystem/WORKFLOW.md)
- [Core integration guide](../kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)
