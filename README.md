# KYROX Platform

**KYROX Platform is the single documentation and knowledge hub for the entire KYROX ecosystem.**

Human-readable rules, standards, architecture decisions, project documentation, status, roadmap and AI operating instructions live here. Application repositories (`kyrox-core`, `fair-crm`, and future products) are implementation and verification repositories: code, tests, migrations, CI and machine-readable runtime/quality contracts may live there, but human/AI documentation must not be duplicated there.

## First read — humans and AI agents

When you are given the KYROX ecosystem, **start with this repository**. Do not begin by inferring rules from application code or from tool-specific local rule files.

Read in this order:

1. [AGENTS.md](AGENTS.md) — universal human/AI entry and routing rules.
2. [ecosystem/DOCUMENT_GOVERNANCE.md](ecosystem/DOCUMENT_GOVERNANCE.md) — where every kind of knowledge belongs and precedence rules.
3. [standards/README.md](standards/README.md) — reusable standards shared by current and future products.
4. Open the owning project tree only after the shared rules are known:
   - Fair CRM → [projects/fair-crm/README.md](projects/fair-crm/README.md)
   - KYROX Core → [projects/kyrox-core/README.md](projects/kyrox-core/README.md)
5. For current state / planned work, read [ecosystem/STATUS.md](ecosystem/STATUS.md) and [ecosystem/ROADMAP.md](ecosystem/ROADMAP.md).

## Core doctrine

> **Humans and AI agents learn the system from `kyrox-platform`. Code repositories are implementation and verification layers.**

A reusable rule belongs under `standards/`. A rule or fact that applies only to one product belongs under `projects/<product>/`. Cross-repository strategy and governance belongs under `ecosystem/`.

If the same rule appears in more than one place, that is a documentation defect: keep one canonical source and replace the others with links or remove them.

## Repositories

| Repository | Role |
|------------|------|
| [kyrox-platform](.) | **All human/AI documentation**, shared standards, project docs, ADRs, roadmap, status |
| [kyrox-core](https://github.com/hinthorozu/kyrox-core) | Shared SaaS backend implementation, tests, migrations and CI |
| [fair-crm](https://github.com/hinthorozu/fair-crm) | Fair CRM implementation, tests, migrations, CI and machine-readable feature contracts |

## Knowledge layout

| Path | Purpose |
|------|---------|
| [standards/](standards/) | Reusable rules that should apply to more than one current/future product |
| [projects/fair-crm/](projects/fair-crm/) | Fair CRM-only product/domain/UI/ops knowledge |
| [projects/kyrox-core/](projects/kyrox-core/) | Core-only architecture/API/implementation knowledge |
| [ecosystem/](ecosystem/) | Cross-repo governance, workflow, strategy, status and roadmap |
| [archive/](archive/) | Historical/superseded material; never normative |

## Important shared standards

- [CRUD & UI Authorization Standard](standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md) — reusable CRUD permission semantics and UI visibility/action rules.
- [Backend Architecture Standards](standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md)

For the complete index, use [standards/README.md](standards/README.md).
