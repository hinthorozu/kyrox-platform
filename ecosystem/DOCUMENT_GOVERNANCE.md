# Document Governance

Single source of truth rules for all KYROX documentation. Documentation lives **only** in this repository (`kyrox-platform`). Application repositories (`kyrox-core`, `fair-crm`) contain **no** Markdown documentation files.

## Where information lives

| Information type | Location | Notes |
|------------------|----------|-------|
| Ecosystem strategy, cross-repo decisions | `ecosystem/` | Vision, philosophy, ADRs, deferred work |
| Live cross-repo status | `ecosystem/STATUS.md` | Summaries only; links to project status for detail |
| Ecosystem roadmap / milestones | `ecosystem/ROADMAP.md` | M1–Mn sequence; product sprint detail stays in project roadmaps |
| Human + AI process | `ecosystem/WORKFLOW.md` | How work is decided and executed |
| Three-repo model | `ecosystem/REPOSITORY_STRATEGY.md` | Fixed structure; changes need ADR |
| This governance policy | `ecosystem/DOCUMENT_GOVERNANCE.md` | Ownership and anti-duplication rules |
| Fair CRM product docs | `projects/fair-crm/` | Architecture, UI, import, ops, product ADRs |
| KYROX Core product docs | `projects/kyrox-core/` | Services, integration contract, Core ADRs |
| Shared technical standards | `standards/` | Rules that apply to more than one project |
| Historical / superseded docs | `archive/` | Keep for history; never treat as live rules |

## Single source of truth (SSoT)

| Topic | Canonical file |
|-------|----------------|
| Document ownership & anti-duplication | `ecosystem/DOCUMENT_GOVERNANCE.md` |
| Ecosystem live status | `ecosystem/STATUS.md` |
| Ecosystem roadmap / milestones | `ecosystem/ROADMAP.md` |
| Repository strategy | `ecosystem/REPOSITORY_STRATEGY.md` + [ADR-0001](decisions/0001-repository-strategy.md) |
| Core vs product separation | [ADR-0002](decisions/0002-core-product-separation.md) |
| Identity security (as-built) | [ADR-0003](decisions/0003-identity-security-strategy.md) |
| Audit strategy | [ADR-0004](decisions/0004-audit-service-strategy.md) |
| Process / workflow | `ecosystem/WORKFLOW.md` |
| Fair CRM live product status | `projects/fair-crm/PROJECT_STATUS.md` |
| Fair CRM product constitution / DoD | `projects/fair-crm/CONSTITUTION.md` |
| Fair CRM product ADRs | `projects/fair-crm/decisions/DECISIONS.md` |
| Fair CRM UI standard | `projects/fair-crm/frontend/FRONTEND_UI_MASTER_STANDARD.md` |
| Fair CRM import architecture | `projects/fair-crm/import/IMPORT_ARCHITECTURE.md` |
| Core live status | `projects/kyrox-core/PROJECT_STATUS.md` |
| Core product integration contract | `projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md` |
| Backend layered architecture standard | [standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md](../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md) |

## Hard rules

1. **Same information must not be repeated** as a second authoritative copy. Other files may link or summarize in one short paragraph and must point to the canonical file.
2. **Status information** (versions, current sprint, capability matrices, quality gates) lives **only** in status files (`ecosystem/STATUS.md`, `projects/*/PROJECT_STATUS.md`). Do not embed live status into architecture standards, ADRs, or workflow docs.
3. **Future plans** live in roadmap files (`ecosystem/ROADMAP.md`, `projects/*/ROADMAP.md`). Do not bury active plans only inside status completion logs.
4. **Permanent process rules** live in `ecosystem/WORKFLOW.md` or `standards/`.
5. **Repo-specific technical rules** live under `projects/<name>/`.
6. **Fast-aging facts** (exact test counts, commit SHAs, “current sprint” labels) belong in status files only — never in permanent standards.
7. **Old documents** are moved to `archive/` with a historical banner when superseded. Prefer archive over silent deletion when the content has historical value.
8. **Application repos** (`fair-crm`, `kyrox-core`) must not reintroduce Markdown documentation. Code comments and non-Markdown config (for example `.cursor/rules/*.mdc`) may remain in those repos when required by tooling.

## Writing status vs roadmap

- Status = what is true **now** (completed capabilities, current version, active milestone).
- Roadmap = what comes **next** and the ordered sequence of milestones/sprints.
- Changelog = what **changed** in a release or planning revision.

## Archive policy

Place under `archive/` when a document is:

- A completion report or one-off audit evidence pack
- A design draft replaced by an as-built guide
- A completed milestone (M1–M3) kept for history
- A superseded product outline that duplicated status

Archived files must start with a short note: historical, not normative, and a link to the live replacement when one exists.
