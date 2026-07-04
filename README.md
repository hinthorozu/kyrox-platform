# kyrox-platform

**Management repository and single source of truth for the KYROX ecosystem.**

This repository holds roadmap, vision, architecture decisions, product plans, milestone tracking, live status, and intentionally deferred work. It is the authoritative place for *what* we build, *why* we build it, and *when* - not *how* the code is written. Application code remains in [kyrox-core](https://github.com/kyrox/kyrox-core) and [fair-crm](https://github.com/kyrox/fair-crm).

## What This Repository Contains

- **Vision** - long-term direction ([VISION.md](VISION.md))
- **ADRs** - architecture and ecosystem decisions ([decisions/](decisions/))
- **Status** - current implementation snapshot ([STATUS.md](STATUS.md))
- **Roadmap** - milestone sequence and progress ([ROADMAP.md](ROADMAP.md))
- **Milestones** - detailed scope per phase ([milestones/](milestones/))
- **Deferred backlog** - intentionally postponed work ([KNOWN_DEFERRED.md](KNOWN_DEFERRED.md))
- **Agent workflow** - AI/Cursor/Codex operating guidance ([AI_WORKFLOW.md](AI_WORKFLOW.md), [AGENTS.md](AGENTS.md))

## What This Repository Is

- The strategic hub and management center for the KYROX SaaS ecosystem
- Home for vision, roadmap, status, and milestone definitions
- Record of architecture decisions (ADRs)
- Product planning and ecosystem documentation
- The place where decisions are made before implementation begins

## What This Repository Is Not

- **Not an application.** There is no backend, frontend, or deployable service here.
- **Not a monorepo.** Application code lives in dedicated repositories.
- **Not a catch-all.** We do not add extra repos (UI library, SDK, docs site, etc.) until explicitly decided.

## Fixed Repository Strategy

KYROX uses three repositories. This structure is final for now.

| Repository | Role |
|------------|------|
| **kyrox-platform** | Ecosystem strategy, roadmap, ADRs, status, product planning |
| **kyrox-core** | Reusable SaaS backend platform |
| **fair-crm** | First product built on KYROX Core |

See [docs/REPOSITORY_STRATEGY.md](docs/REPOSITORY_STRATEGY.md) and [decisions/0001-repository-strategy.md](decisions/0001-repository-strategy.md) for details.

## Current State

| Area | Status |
|------|--------|
| Platform baseline | **Completed** - kyrox-core **v0.4.0** (307 passed, 1 skipped; Alembic head `20260701_0025`) |
| kyrox-core | **Frozen** - bug, security, performance, and CRM-driven reusable platform fixes only |
| Active product | [fair-crm](https://github.com/kyrox/fair-crm) - active development |
| Current milestone | **M4 FAIR CRM v1** (active) |
| Current phase | FAIR CRM product delivery and data-integration pipeline hardening |

FAIR CRM is no longer in a "not started" state. Customer/Fair/Participation foundations exist, Adapter Management is completed, Linked Fairs are completed, Fair -> Adapter relationship is completed, Adapter CRUD is completed, and Run v2 + JSON Handoff is completed.

Current technical target: **Canonical Import Schema**. Next target: **Import Batch / Preview / Duplicate / Merge** pipeline.

See [STATUS.md](STATUS.md) for the full capability matrix.

## Repository Layout

```text
kyrox-platform/
├── README.md
├── VISION.md
├── STATUS.md
├── ROADMAP.md
├── CHANGELOG.md
├── KNOWN_DEFERRED.md
├── AI_WORKFLOW.md
├── AGENTS.md
├── docs/
│   ├── ECOSYSTEM.md
│   ├── REPOSITORY_STRATEGY.md
│   └── WORKFLOW.md
├── decisions/
│   ├── ADR_INDEX.md
│   └── ...
├── products/
│   └── FAIR_CRM.md
└── milestones/
    ├── M1_FOUNDATION.md
    ├── M2_IDENTITY.md
    ├── M3_PLATFORM_SERVICES.md
    └── M4_FAIR_CRM_V1.md
```

## Getting Started

1. Read [STATUS.md](STATUS.md) for what is done and in progress today.
2. Read [VISION.md](VISION.md) for the long-term direction.
3. Check [ROADMAP.md](ROADMAP.md) and the active milestone in `milestones/`.
4. Review [KNOWN_DEFERRED.md](KNOWN_DEFERRED.md) before assuming missing features are oversights.
5. Follow [docs/WORKFLOW.md](docs/WORKFLOW.md), [AI_WORKFLOW.md](AI_WORKFLOW.md), and [AGENTS.md](AGENTS.md) when making or implementing decisions.
6. Record significant choices as ADRs in `decisions/`.

## Related Documents

- [Status](STATUS.md)
- [Vision](VISION.md)
- [Roadmap](ROADMAP.md)
- [Deferred backlog](KNOWN_DEFERRED.md)
- [Changelog](CHANGELOG.md)
- [Ecosystem overview](docs/ECOSYSTEM.md)
- [ADR index](decisions/ADR_INDEX.md)
