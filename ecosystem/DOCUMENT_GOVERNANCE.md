# Document Governance

Single source of truth rules for all KYROX human- and AI-readable knowledge.

## Platform doctrine

> **Humans and AI agents learn the KYROX system from `kyrox-platform`. Application repositories are implementation and verification layers.**

All human-readable standards, architecture, decisions, product rules, status, roadmap and operating instructions live in this repository. Application repositories (`kyrox-core`, `fair-crm`, future products) contain code, tests, migrations, CI and machine-readable contracts required by implementation or verification; they must not become parallel documentation systems.

## Classification rule — where information belongs

Use the narrowest correct canonical owner:

| Information type | Location | Rule |
|------------------|----------|------|
| Reusable rule/behavior for more than one current or future product | `standards/` | Write once; products consume it |
| Cross-repo strategy, workflow, ownership, ecosystem decisions | `ecosystem/` | Applies to the ecosystem as a whole |
| Fair CRM-only product/domain/UI/ops behavior | `projects/fair-crm/` | May extend shared standards, not copy them |
| KYROX Core-only architecture/API/implementation behavior | `projects/kyrox-core/` | May extend shared standards, not copy them |
| Live cross-repo status | `ecosystem/STATUS.md` | Summary only |
| Project live status | `projects/<name>/PROJECT_STATUS.md` | Exact project state |
| Ecosystem roadmap | `ecosystem/ROADMAP.md` | Cross-project sequencing |
| Product roadmap | `projects/<name>/ROADMAP.md` | Product-specific future work |
| Historical/superseded material | `archive/` | Never normative |
| CI/runtime machine-readable contracts | Application repo when technically required | Not human documentation; no prose-rule duplication |

### Decision test

Ask one question first:

**“Would another KYROX product reasonably use this same rule?”**

- **Yes** → `standards/`.
- **No, only this product** → `projects/<product>/`.
- **It coordinates repositories/products** → `ecosystem/`.

Example: CRUD permission semantics and permission-driven UI visibility are reusable, therefore canonical under `standards/ui/`. A Fair CRM-specific `customer.merge` business rule belongs under `projects/fair-crm/`.

## Single source of truth (SSoT)

| Topic | Canonical file |
|-------|----------------|
| Platform knowledge entry | `README.md` + `AGENTS.md` |
| Document ownership & anti-duplication | `ecosystem/DOCUMENT_GOVERNANCE.md` |
| Shared standards index | `standards/README.md` |
| Shared CRUD / permission-driven UI behavior | `standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md` |
| Ecosystem live status | `ecosystem/STATUS.md` |
| Ecosystem roadmap / milestones | `ecosystem/ROADMAP.md` |
| Repository strategy | `ecosystem/REPOSITORY_STRATEGY.md` + [ADR-0001](decisions/0001-repository-strategy.md) |
| Core vs product separation | [ADR-0002](decisions/0002-core-product-separation.md) |
| Identity security (as-built) | [ADR-0003](decisions/0003-identity-security-strategy.md) |
| Audit strategy | [ADR-0004](decisions/0004-audit-service-strategy.md) |
| Role templates and permission governance | [ADR-0005](decisions/0005-role-template-and-permission-governance.md) |
| Process / workflow | `ecosystem/WORKFLOW.md` |
| Fair CRM live product status | `projects/fair-crm/PROJECT_STATUS.md` |
| Fair CRM product constitution / DoD | `projects/fair-crm/CONSTITUTION.md` |
| Fair CRM feature delivery execution order / acceptance gates | `projects/fair-crm/DEVELOPMENT_STANDARD.md` |
| Fair CRM feature applicability / REQUIRED-N/A rules | `projects/fair-crm/FEATURE_APPLICABILITY_STANDARD.md` |
| Fair CRM CI / zero-new-regression / legacy quality-debt rules | `projects/fair-crm/QUALITY_GATE_STANDARD.md` |
| Fair CRM product ADRs | `projects/fair-crm/decisions/DECISIONS.md` |
| Fair CRM UI implementation/design standard | `projects/fair-crm/frontend/FRONTEND_UI_MASTER_STANDARD.md` |
| Fair CRM-specific permission scope governance | `projects/fair-crm/PERMISSION_SCOPE_GOVERNANCE.md` |
| Fair CRM import architecture | `projects/fair-crm/import/IMPORT_ARCHITECTURE.md` |
| Core live status | `projects/kyrox-core/PROJECT_STATUS.md` |
| Core product integration contract | `projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md` |
| Backend layered architecture standard | [standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md](../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md) |

## Precedence and overlap

1. **One topic has one normative source.** If two files define the same reusable rule, merge the rule into the shared standard and remove/reduce the duplicates to links and product-specific additions.
2. Shared standards define reusable semantics. Project documents define product-specific implementation, domain detail and explicit exceptions.
3. A project document must not silently redefine a shared rule. Any exception must be explicit, justified and link to the shared standard it overrides.
4. Archive, chat history, generated notes and tool-specific local rules never override live canonical documents.
5. If two live documents conflict and neither is an explicit exception, treat it as a documentation defect and resolve it before implementation.

## Hard rules

1. **Same information must not be repeated** as a second authoritative copy. Use links instead of copied normative paragraphs.
2. **Status information** (versions, current sprint, capability matrices, quality gates) lives only in status files.
3. **Future plans** live in roadmap files.
4. **Permanent reusable process/technical rules** live in `standards/` or, when cross-repo operational, `ecosystem/WORKFLOW.md`.
5. **Repo/product-specific technical rules** live under `projects/<name>/` only when they are genuinely product-specific.
6. **Fast-aging facts** belong in status files only.
7. **Old documents** move to `archive/` with a historical banner when superseded.
8. **Application repos must not reintroduce a parallel human-readable rule system.** Tool-specific files may exist only when technically unavoidable; they must contain no independent normative rules and should point to this platform entry point if a tool requires a local hook.
9. Machine-readable CI/runtime contracts may remain in application repos, but their human meaning and governance must be documented canonically here.

## Writing status vs roadmap

- Status = what is true **now**.
- Roadmap = what comes **next**.
- Changelog = what **changed**.
- Standard = reusable binding behavior.
- Project rule = binding behavior unique to one product.

## Archive policy

Place under `archive/` when a document is a completion report, one-off audit pack, superseded draft, completed milestone, or replaced product outline. Archived files must clearly state that they are historical and point to the live replacement when one exists.
