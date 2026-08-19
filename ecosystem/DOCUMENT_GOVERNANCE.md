# Document Governance

Single source of truth rules for all KYROX human- and AI-readable knowledge.

## Platform doctrine

> **Humans and AI agents learn the KYROX system from `kyrox-platform`. Application repositories are implementation and verification layers.**

All human-readable standards, architecture, decisions, product rules, status, roadmap and operating instructions live in this repository. Application repositories (`kyrox-core`, `fair-crm`, future products) contain code, tests, migrations, CI and machine-readable contracts required by implementation or verification; they must not become parallel documentation systems.

## Classification rule

| Information type | Location | Rule |
|---|---|---|
| Reusable rule/behavior | `standards/` | Write once; products consume it |
| Cross-repo strategy/workflow/ownership | `ecosystem/` | Ecosystem-wide |
| Fair CRM-only behavior | `projects/fair-crm/` | Extend shared standards; do not copy them |
| Core-only behavior | `projects/kyrox-core/` | Extend shared standards; do not copy them |
| Live ecosystem status | `ecosystem/STATUS.md` | Summary only |
| Live project status | `projects/<name>/PROJECT_STATUS.md` | Current truth |
| Future work | `ecosystem/ROADMAP.md` or `projects/<name>/ROADMAP.md` | Plans only |
| Historical/superseded material | `archive/` | Never normative |
| Machine-readable CI/runtime contracts | Application repo when technically required | Not human documentation |

Decision test: **Would another KYROX product reasonably use this same rule?** Yes → `standards/`; no → owning project; cross-repo → `ecosystem/`.

## Canonical routing

| Topic | Canonical source |
|---|---|
| Platform knowledge entry | `README.md` + `AGENTS.md` |
| Document ownership / anti-duplication | `ecosystem/DOCUMENT_GOVERNANCE.md` |
| Shared standards index | `standards/README.md` |
| Feature delivery / acceptance gates | `standards/development/FEATURE_DELIVERY_STANDARD.md` |
| Feature applicability / REQUIRED-N/A | `standards/development/FEATURE_APPLICABILITY_STANDARD.md` |
| Quality / strict-green / regression policy | `standards/quality/QUALITY_GATE_STANDARD.md` |
| UI foundation / responsive / visual QA / a11y | `standards/ui/UI_FOUNDATION_STANDARD.md` |
| CRUD / permission-driven UI behavior | `standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md` |
| Backend layered architecture | `standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md` |
| Ecosystem status | `ecosystem/STATUS.md` |
| Ecosystem roadmap | `ecosystem/ROADMAP.md` |
| Workflow | `ecosystem/WORKFLOW.md` |
| Repository strategy | `ecosystem/REPOSITORY_STRATEGY.md` + ADR-0001 |
| Core vs product boundary | ecosystem ADR-0002 |
| Fair CRM current state | `projects/fair-crm/PROJECT_STATUS.md` |
| Fair CRM future work | `projects/fair-crm/ROADMAP.md` |
| Fair CRM product invariants | `projects/fair-crm/CONSTITUTION.md` |
| Fair CRM delivery extension | `projects/fair-crm/DEVELOPMENT_STANDARD.md` |
| Fair CRM applicability extension | `projects/fair-crm/FEATURE_APPLICABILITY_STANDARD.md` |
| Fair CRM quality extension | `projects/fair-crm/QUALITY_GATE_STANDARD.md` |
| Fair CRM UI implementation | `projects/fair-crm/frontend/FRONTEND_UI_MASTER_STANDARD.md` |
| Fair CRM permission scope | `projects/fair-crm/PERMISSION_SCOPE_GOVERNANCE.md` |
| Fair CRM import architecture | `projects/fair-crm/import/IMPORT_ARCHITECTURE.md` |
| Core current state | `projects/kyrox-core/PROJECT_STATUS.md` |
| Core integration contract | `projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md` |

## Precedence and overlap

1. One topic has one normative source.
2. Shared standards define reusable semantics; project documents add product-specific detail and explicit exceptions.
3. A project exception must be explicit, justified and linked to the shared standard.
4. Archive, chat history and tool-specific local rules never override live canonical documents.
5. Conflicting live documents are a documentation defect and must be resolved before implementation.

## Hard rules

1. Do not repeat the same information as a second authoritative copy; link instead.
2. Status = what is true now. Roadmap = what comes next. Changelog = what changed.
3. Fast-aging facts such as versions, migration heads and transient test counts belong only in status when useful.
4. Reusable technical/process rules live in `standards/`; cross-repo operational rules may live in `ecosystem/WORKFLOW.md`.
5. Product-specific technical/domain rules live under `projects/<name>/` only when genuinely product-specific.
6. Superseded material moves to `archive/` and is non-normative.
7. Application repos must not reintroduce a parallel human-readable rule system.
8. Machine-readable CI/runtime contracts may remain in application repos; their human meaning is documented here.

## Acceptance-flow preservation

Documentation consolidation must never weaken the delivery gates. Applicable work still follows the canonical flow:

**design/ownership → implementation → automated tests/build → permission/security checks → real UI render and responsive/visual QA when UI applies → runtime verification → strict-green acceptance → completion/status update.**

A green build alone is not UI acceptance. Hidden UI is not backend authorization. A legacy baseline may not grow to disguise a new regression. An applicable red gate means the work is not DONE.

## Archive policy

Archive completion reports, one-off audits, superseded drafts and replaced outlines under `archive/`. Archived files are historical and never override a live canonical source.
