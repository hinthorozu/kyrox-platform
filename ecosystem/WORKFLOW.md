# KYROX Workflow

How humans and AI agents decide, document, and implement work across the three repositories.

## Principles

1. **Decide in platform, implement in code repos.** Cross-repo strategy and ADRs land in `kyrox-platform` first.
2. **Core stays product-agnostic.** Product domain behavior belongs in `fair-crm` (or future products).
3. **Documentation lives only here.** Application repos must not grow Markdown doc trees. See [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md).
4. **Status and roadmap stay separated.** Update the correct status/roadmap files; do not paste live status into standards.

## Decision → implement → verify

```text
1. Classify work
   - Ecosystem / cross-repo → ecosystem/ + ADR if needed
   - Reusable platform capability → kyrox-core (respect freeze)
   - Product feature → fair-crm

2. Document intent
   - New rule / architecture → ADR or project decision doc
   - New plan → roadmap file
   - Status change after delivery → status file + changelog

3. Implement in the owning code repo
   - Follow standards/backend, project constitution, integration guide

4. Verify
   - Backend: targeted/full pytest as appropriate
   - Frontend (fair-crm): npm run build
   - Runtime: documented reset/start scripts when behavior is runtime-sensitive

5. Sync documentation
   - Update projects/*/PROJECT_STATUS.md and ecosystem/STATUS.md summary
   - Update CHANGELOG entries in the owning project tree
   - Archive superseded design docs instead of leaving conflicting “live” copies
```

### Authorization and real-runtime acceptance gate

When a feature introduces or depends on a new permission code, authorization is part of the same delivery path as the feature. The permission catalog, product role matrix/mapping, seed or synchronization path, and real runtime authorization check must all be aligned before the feature can be accepted.

- Mock authorization, `AllowAllAuthorization`, dev bypass, or unit/API tests with authorization overridden are useful implementation tests, but they are **not acceptance evidence**.
- A feature that requires authorization is **not complete** while a real user/JWT receives `401`/`403` on the intended flow.
- For UI work, build success alone is insufficient. The affected UI flow must open with real authorization and display the real API data required by that workflow.
- End-to-end acceptance must follow the production-shaped path: real login/JWT → Core authorization check → product API → affected UI/workflow → real result/data.
- If any link in that chain fails, report the feature as implemented but **not accepted / not complete**; do not mark it DONE because mocks, bypasses, unit tests, or frontend build pass.

## Active milestone

Only **M4 — FAIR CRM v1** is active. M1–M3 are completed and archived. See [ROADMAP.md](ROADMAP.md) and [STATUS.md](STATUS.md).

## kyrox-core freeze (during M4)

Allowed without lifting freeze:

- Bug fixes, security fixes, performance fixes
- Reusable platform needs driven by FAIR CRM (documented)

Not allowed without an ecosystem decision:

- Product domain logic in Core
- Speculative platform features not required by a product

## AI agent operating rules

### Before starting architecture-sensitive work

Read:

1. [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md)
2. [STATUS.md](STATUS.md) and [ROADMAP.md](ROADMAP.md)
3. Owning project README + PROJECT_STATUS
4. Relevant standards and ADRs

### Requirements / ambiguity gate

- AI agents and automation must **not invent, infer, reinterpret, or silently complete** product requirements when the user request or canonical documentation is incomplete, ambiguous, or conflicting.
- Before implementation, compare the request against the canonical roadmap, status, constitution, standards, ADRs, and existing behavior relevant to the task.
- If a material requirement is missing, unclear, contradictory, or would require choosing between multiple valid product behaviors, **stop before changing code and ask the user for a decision**.
- Do not choose a default behavior merely because it is common practice, technically convenient, or appears reasonable.
- Do not broaden task scope beyond what the user approved and what canonical documentation requires.
- Existing canonical rules remain binding unless the user explicitly changes them. When the user changes a rule, update the owning canonical document as part of the work.
- Minor implementation details that do not change product behavior may follow existing project patterns without an extra question.
- When uncertainty is discovered after implementation has started, pause further changes, preserve completed safe work, and surface the exact ambiguity before continuing.

### Simple-first / need-now execution rule

- Implement and validate the **smallest working vertical slice first**. Prove the real path with the minimum fields, minimum UI, minimum API behavior, and minimum data needed for that step before enriching it.
- A screen, wizard step, modal, or workflow stage must do **only the work required for that current stage**.
- Do **not** preload, prefetch, validate, transform, prepare, or execute work for a later stage merely because it will be needed eventually.
- Fetch or compute later-stage data **when the user enters or explicitly advances to the stage that needs it**, unless there is a measured, documented performance reason to preload it.
- Do not add helper copy, summary rows, secondary metadata, extra controls, background preparation, or speculative UX before the basic working flow is accepted.
- Enrichment happens **after** the simple real flow works end-to-end. “Future usefulness”, “common UX”, or “it may save a click later” is not sufficient justification to complicate the current step.
- Example: if Step 1 is only “select a Fair”, Step 1 loads the Fair options, stores the selected Fair, and enables Next. Adapter capabilities, scraper config, output fields, and other Step 2 data must not block or delay Step 1; they load when Step 2 is entered.

### Boundaries

- Work only in the repository that owns the change.
- Never import Core Python modules into fair-crm, share DB sessions, or create cross-repo foreign keys.
- Prefer updating the canonical document over creating a parallel “source of truth.”
- Do not embed fast-aging facts (test counts, SHAs, “current sprint”) into permanent standards.

### Fair CRM UI work

Before changing UI code, read [FRONTEND_UI_MASTER_STANDARD.md](../projects/fair-crm/frontend/FRONTEND_UI_MASTER_STANDARD.md).

### Core integration work

Use [PRODUCT_INTEGRATION_GUIDE.md](../projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md) as the contract.

### Git

- Commit only when the user requests it.
- Do not force-push protected branches.
- Keep generated artifacts and secrets out of commits.

## Contribution shape

1. Prefer small, reviewable changes.
2. Match existing code style in the target repo.
3. For process or standard changes, update this file or `standards/` rather than scattering rules into READMEs.

## Related

- [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md)
- [PHILOSOPHY.md](PHILOSOPHY.md)
- [VISION.md](VISION.md)
- [standards/ai/](../standards/ai/)
- [standards/git/](../standards/git/)
