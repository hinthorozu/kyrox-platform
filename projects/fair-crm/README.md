# Fair CRM

First KYROX product: multi-tenant fair / exhibition CRM built on KYROX Core identity and platform services.

**Code repository:** `https://github.com/hinthorozu/fair-crm`  
**Human/AI documentation:** this tree under `kyrox-platform`  
**Ecosystem status:** [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md)

## Before Fair CRM-specific docs

Fair CRM inherits applicable shared KYROX standards. Read [../../standards/README.md](../../standards/README.md) first for the task area.

For CRUD, permission-driven UI visibility, navigation, routes and action gating, the canonical reusable rule is [../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md](../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md). Fair CRM documents may add product-specific permission slugs, domain constraints, design-system implementation and explicit exceptions; they must not duplicate or silently redefine the shared semantics.

## Canonical Fair CRM-only docs

| Doc | Role |
|-----|------|
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Live product status (SSoT) |
| [ROADMAP.md](ROADMAP.md) | Product ops / sprint backlog |
| [CHANGELOG.md](CHANGELOG.md) | Product release history |
| [CONSTITUTION.md](CONSTITUTION.md) | Fair CRM binding product constitution / DoD |
| [DEVELOPMENT_STANDARD.md](DEVELOPMENT_STANDARD.md) | Fair CRM feature-delivery execution order and acceptance gates |
| [FEATURE_APPLICABILITY_STANDARD.md](FEATURE_APPLICABILITY_STANDARD.md) | Fair CRM feature profiles and REQUIRED / N/A gate rules |
| [QUALITY_GATE_STANDARD.md](QUALITY_GATE_STANDARD.md) | Fair CRM CI, zero-new-regression and legacy quality-debt rules |
| [VISION.md](VISION.md) | Long-term Fair CRM product vision |
| [architecture/ARCHITECTURE.md](architecture/ARCHITECTURE.md) | Fair CRM service layout and modules |
| [decisions/DECISIONS.md](decisions/DECISIONS.md) | Fair CRM product ADRs |
| [frontend/FRONTEND_UI_MASTER_STANDARD.md](frontend/FRONTEND_UI_MASTER_STANDARD.md) | Fair CRM-specific UI/design-system implementation standard |
| [PERMISSION_SCOPE_GOVERNANCE.md](PERMISSION_SCOPE_GOVERNANCE.md) | Fair CRM-specific permission catalog/scope governance |
| [import/IMPORT_ARCHITECTURE.md](import/IMPORT_ARCHITECTURE.md) | Fair CRM import / data integration architecture |
| [integrations/INTEGRATION_WITH_CORE.md](integrations/INTEGRATION_WITH_CORE.md) | Fair CRM ↔ Core integration notes |
| [ops/DEV_RUNTIME.md](ops/DEV_RUNTIME.md) | Fair CRM development runtime |

## Ownership boundary

- Reusable rule that another product could use unchanged → move/maintain under `../../standards/`.
- Fair CRM-only domain/product behavior → maintain under this project tree.
- Cross-repo coordination → maintain under `../../ecosystem/`.
- Fair CRM code, tests, migrations, CI and machine-readable feature contracts → `fair-crm` code repository.
- Do not recreate human-readable standards inside the Fair CRM code repository.

## Related ecosystem docs

- [Document Governance](../../ecosystem/DOCUMENT_GOVERNANCE.md)
- [Workflow](../../ecosystem/WORKFLOW.md)
- [Shared Standards](../../standards/README.md)
- [Core integration guide](../kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)
