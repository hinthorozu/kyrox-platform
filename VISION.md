# KYROX Vision

## What KYROX is

KYROX is a **reusable SaaS ecosystem** — a shared foundation and a set of products built on top of it. The goal is to ship multiple SaaS products faster, with consistent architecture, identity, billing, and platform services, without rebuilding the same backend for every product.

## Core-first strategy

We build **KYROX Core first**. Core is the product-independent backend platform: authentication, tenancy, billing hooks, API conventions, and shared services that any KYROX product can adopt.

Products do not define the platform. The platform defines what products can rely on. New capabilities belong in Core when they are reusable; they belong in a product repo when they are product-specific.

## Product-independent backend foundation

KYROX Core must remain **independent of any single product**:

- Core has no dependency on fair-crm or future products.
- Core exposes stable contracts (APIs, events, configuration) that products consume.
- Shared behavior is implemented once in Core and reused across products.

This separation keeps the ecosystem scalable: adding a second or third product should not require rewriting Core.

## FAIR CRM as the first product

**FAIR CRM** is the first product built on KYROX Core. It validates the platform in production: real users, real workflows, real constraints.

FAIR CRM proves that Core is sufficient for a full product while surfacing gaps early. Lessons from FAIR CRM feed back into Core and into platform decisions recorded in this repository.

## Principles

1. **Decide here, implement elsewhere** — Strategy and ADRs live in kyrox-platform; code lives in kyrox-core and product repos.
2. **Core before features** — Platform capabilities precede product-specific shortcuts.
3. **One ecosystem, many products** — Architecture choices favor reuse without coupling products to each other.
4. **Document decisions** — Significant choices become ADRs so future work has context.

## Long-term direction

KYROX aims to support a portfolio of SaaS products on a common backend platform, with clear boundaries between platform and product, and a predictable workflow from vision → milestone → implementation → release.

See [ROADMAP.md](ROADMAP.md) for the current milestone sequence and [docs/ECOSYSTEM.md](docs/ECOSYSTEM.md) for how the pieces fit together.
