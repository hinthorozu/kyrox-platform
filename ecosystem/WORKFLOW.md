# KYROX Workflow

How humans and AI agents decide, document, and implement work across the three repositories.

## Principles

1. **Decide in platform, implement in code repos.** Cross-repo strategy and ADRs land in `kyrox-platform` first.
2. **Core stays product-agnostic.** Product domain behavior belongs in `fair-crm` (or future products).
3. **Documentation lives only here.** Application repos must not grow Markdown doc trees. See [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md).
4. **Status and roadmap stay separated.** Update the correct status/roadmap files; do not paste live status into standards.
5. **SaaS safety is part of delivery.** Every material change classifies its SaaS impact and proves every affected organization/security/runtime boundary before it can be DONE.

## Decision → classify SaaS impact → implement → verify

```text
1. Classify work
   - Ecosystem / cross-repo → ecosystem/ + ADR if needed
   - Reusable platform capability → kyrox-core (respect freeze)
   - Product feature → fair-crm

2. Classify SaaS impact
   - organization-owned data / tenant isolation
   - organization vs system permission scope
   - Core vs product vs provider ownership
   - plan / entitlement behavior
   - usage / quota behavior
   - organization/account lifecycle
   - secrets / production security
   - background jobs / audit / async execution
   - export / retention / deletion lifecycle
   - scale / infrastructure dependency
   Affected = REQUIRED evidence; unaffected = N/A with reason.

3. Document intent
   - New rule / architecture → ADR or project decision doc
   - New cross-repo SaaS strategy → ecosystem/SAAS_ROADMAP.md
   - New concrete product/Core plan → owning project roadmap
   - Status change after delivery → status file + changelog

4. Implement in the owning code repo
   - Follow standards/backend, project constitution, integration guide
   - Reuse Core platform contracts; do not duplicate Core-owned capabilities

5. Verify
   - Backend: targeted/full pytest as appropriate
   - Frontend (fair-crm): npm run build
   - Tenant/security: cross-organization / permission-scope / async-scope tests when applicable
   - Runtime: documented reset/start scripts and production-shaped auth/workflow checks when behavior is runtime-sensitive

6. Sync documentation
   - Update projects/*/PROJECT_STATUS.md and ecosystem/STATUS.md summary when truth changes
   - Update CHANGELOG entries in the owning project tree
   - Archive superseded design docs instead of leaving conflicting “live” copies
```

Canonical SaaS sequencing: [SAAS_ROADMAP.md](SAAS_ROADMAP.md).  
Binding feature gates: [../standards/development/FEATURE_DELIVERY_STANDARD.md](../standards/development/FEATURE_DELIVERY_STANDARD.md).

### Authorization and real-runtime acceptance gate

When a feature introduces or depends on a new permission code, authorization is part of the same delivery path as the feature. The permission catalog, product role matrix/mapping, seed or synchronization path, and real runtime authorization check must all be aligned before the feature can be accepted.

- Mock authorization, `AllowAllAuthorization`, dev bypass, or unit/API tests with authorization overridden are useful implementation tests, but they are **not acceptance evidence**.
- A feature that requires authorization is **not complete** while a real user/JWT receives `401`/`403` on the intended flow.
- For UI work, build success alone is insufficient. The affected UI flow must open with real authorization and display the real API data required by that workflow.
- End-to-end acceptance must follow the production-shaped path: real login/JWT → Core authorization check → product API → affected UI/workflow → real result/data.
- If any link in that chain fails, report the feature as implemented but **not accepted / not complete**; do not mark it DONE because mocks, bypasses, unit tests, or frontend build pass.

### SaaS safety acceptance gate

For every material change, green CI is necessary but does not replace evidence for the affected SaaS boundary.

When applicable, acceptance must prove:

- normal organization users and OrganizationAdmin cannot cross organization boundaries,
- Platform Super Admin follows the documented bypass model rather than being misclassified as a tenant leak,
- organization/system permission scope matches governance and assignability,
- background/internal work preserves validated organization context or has deliberate system scope,
- product/Core ownership remains correct and public integration contracts are used,
- permission and entitlement/plan decisions are not conflated,
- backend quota/usage enforcement is concurrency/retry safe when hard limits apply,
- organization lifecycle behavior follows explicit approved policy rather than invented Owner/self-service destructive semantics,
- development bypass/fallback identities and unsafe secret handling cannot become production authority,
- export/retention/delete behavior is verified when data lifecycle changes.

If an affected SaaS property is unresolved, untested where testing is required, or fails the real runtime path, report **implemented but not accepted / not complete** even if ordinary tests/build are green.

## Active milestone

Only **M4 — FAIR CRM v1** is active. M1–M3 are completed and archived. See [ROADMAP.md](ROADMAP.md) and [STATUS.md](STATUS.md).

The cross-cutting SaaS readiness sequence is maintained in [SAAS_ROADMAP.md](SAAS_ROADMAP.md). It does not activate speculative Core work by itself.

## kyrox-core freeze (during M4)

Allowed without lifting freeze:

- Bug fixes, security fixes, performance fixes
- Reusable platform needs driven by FAIR CRM (documented)

Not allowed without an ecosystem decision:

- Product domain logic in Core
- Speculative platform features not required by a product

Billing/subscription, generic metering, observability or other platform candidates become active only after a real product requirement and the applicable ownership/planning decision.

## AI agent operating rules

### Before starting architecture-sensitive or material feature work

Read:

1. [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md)
2. [STATUS.md](STATUS.md), [ROADMAP.md](ROADMAP.md), and [SAAS_ROADMAP.md](SAAS_ROADMAP.md)
3. Owning project README + PROJECT_STATUS
4. Relevant standards and ADRs

### Requirements / ambiguity gate

- AI agents and automation must **not invent, infer, reinterpret, or silently complete** product requirements when the user request or canonical documentation is incomplete, ambiguous, or conflicting.
- Before implementation, compare the request against the canonical roadmap, SaaS roadmap, status, constitution, standards, ADRs, and existing behavior relevant to the task.
- If a material requirement is missing, unclear, contradictory, or would require choosing between multiple valid product behaviors, **stop before changing code and ask the user for a decision**.
- Do not choose a default behavior merely because it is common practice, technically convenient, or appears reasonable.
- Do not silently invent permission scope, Core/product ownership, Owner roles, organization lifecycle behavior, entitlement semantics, quota semantics or billing behavior.
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
- SaaS readiness does not override simple-first: classify future impacts now, but implement only the capability required by the approved current slice.
- Example: if Step 1 is only “select a Fair”, Step 1 loads the Fair options, stores the selected Fair, and enables Next. Adapter capabilities, scraper config, output fields, and other Step 2 data must not block or delay Step 1; they load when Step 2 is entered.

### Boundaries

- Work only in the repository that owns the change.
- Never import Core Python modules into fair-crm, share DB sessions, or create cross-repo foreign keys.
- Prefer updating the canonical document over creating a parallel “source of truth.”
- Do not embed fast-aging facts (test counts, SHAs, “current sprint”) into permanent standards.
- Do not introduce a parallel Tenant account model, duplicate Core authorization/organization/audit/jobs infrastructure, or speculative Core SaaS capabilities without an accepted ownership decision.

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

- [SAAS_ROADMAP.md](SAAS_ROADMAP.md)
- [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md)
- [PHILOSOPHY.md](PHILOSOPHY.md)
- [VISION.md](VISION.md)
- [standards/ai/](../standards/ai/)
- [standards/git/](../standards/git/)
