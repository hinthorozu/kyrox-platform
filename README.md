# kyrox-platform

**Management and decision center for the KYROX ecosystem.**

This repository holds roadmap, vision, architecture decisions, product plans, and milestone tracking. It is the single source of truth for *what* we build, *why* we build it, and *when* — not *how* the code is written.

## What this repository is

- The strategic hub for the KYROX SaaS ecosystem
- Home for vision, roadmap, and milestone definitions
- Record of architecture decisions (ADRs)
- Product planning and ecosystem documentation
- The place where decisions are made before implementation begins

## What this repository is not

- **Not an application.** There is no backend, frontend, or deployable service here.
- **Not a monorepo.** Application code lives in dedicated repositories.
- **Not a catch-all.** We do not add extra repos (UI library, SDK, docs site, etc.) until explicitly decided.

## Fixed repository strategy

KYROX uses three repositories. This structure is final for now.

| Repository        | Role                                              |
|-------------------|---------------------------------------------------|
| **kyrox-platform** | Ecosystem strategy, roadmap, ADRs, product planning |
| **kyrox-core**     | Reusable SaaS backend platform                    |
| **fair-crm**       | First product built on KYROX Core                 |

See [docs/REPOSITORY_STRATEGY.md](docs/REPOSITORY_STRATEGY.md) and [decisions/0001-repository-strategy.md](decisions/0001-repository-strategy.md) for details.

## Current state

| Area                    | Status                          |
|-------------------------|---------------------------------|
| Active implementation   | [kyrox-core](https://github.com/kyrox/kyrox-core) |
| Active product          | [fair-crm](https://github.com/kyrox/fair-crm)     |
| Current milestone       | **M2 Identity** (active)        |

## Repository layout

```
kyrox-platform/
├── README.md
├── VISION.md
├── ROADMAP.md
├── CHANGELOG.md
├── docs/
│   ├── ECOSYSTEM.md
│   ├── REPOSITORY_STRATEGY.md
│   └── WORKFLOW.md
├── decisions/
│   ├── ADR_INDEX.md
│   ├── 0001-repository-strategy.md
│   └── 0002-core-product-separation.md
├── products/
│   └── FAIR_CRM.md
└── milestones/
    ├── M1_FOUNDATION.md
    ├── M2_IDENTITY.md
    ├── M3_PLATFORM_SERVICES.md
    └── M4_FAIR_CRM_V1.md
```

## Getting started

1. Read [VISION.md](VISION.md) for the long-term direction.
2. Check [ROADMAP.md](ROADMAP.md) and the active milestone in `milestones/`.
3. Follow [docs/WORKFLOW.md](docs/WORKFLOW.md) when making or implementing decisions.
4. Record significant choices as ADRs in `decisions/`.

## Related documents

- [Vision](VISION.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)
- [Ecosystem overview](docs/ECOSYSTEM.md)
- [ADR index](decisions/ADR_INDEX.md)
