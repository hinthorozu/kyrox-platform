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