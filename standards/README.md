# KYROX Shared Standards

This directory contains **reusable, product-independent rules** for the KYROX ecosystem.

If a rule should apply to Fair CRM and could also apply unchanged to a future CRM, ERP, inventory, finance or other KYROX product, it belongs here rather than inside a single project's documentation.

## Reading rule

Before reading a product-specific standard, check this index and read every shared standard applicable to the task. Product documents may add domain detail or explicit exceptions; they must not duplicate or silently redefine these rules.

## Index

### Development / feature delivery

- [Feature Delivery Standard](development/FEATURE_DELIVERY_STANDARD.md) — canonical design → ownership/security → backend → UI → test/runtime → deployment/DoD execution order.
- [Feature Applicability Standard](development/FEATURE_APPLICABILITY_STANDARD.md) — canonical feature profiles, REQUIRED/N/A gates, tenant-isolation independence, UI/job/system applicability and review discipline.

### Quality

- [Quality Gate Standard](quality/QUALITY_GATE_STANDARD.md) — strict-green target, zero-new-regression semantics, monotonic legacy baseline, truthful completion reporting and CI/branch-protection boundaries.

### UI / authorization

- [UI Foundation Standard](ui/UI_FOUNDATION_STANDARD.md) — one design system, shared primitives, tokens, responsive/visual QA, accessibility, dirty-form and loading-state foundations.
- [CRUD & UI Authorization Standard](ui/CRUD_UI_AUTHORIZATION_STANDARD.md) — canonical CRUD permission semantics, UI visibility, navigation/route/action gating and backend enforcement.

### Backend

- [Backend Architecture Standards](backend/BACKEND_ARCHITECTURE_STANDARDS.md) — shared layered backend architecture and dependency direction.

### Other shared areas

- `ai/` — shared AI/agent standards.
- `database/` — shared database standards.
- `git/` — shared Git/repository standards.
- `jobs/` — shared background-job standards.

## Ownership rule

A new rule goes here when another current or future product would reasonably reuse the same behavior. If it is genuinely specific to one product, place it under `projects/<product>/` instead.

One rule must have one canonical source. Product/project files are extensions: they may define exact paths, product permission slugs, domain constraints or explicit exceptions, but they must not restate the shared rule as a second authority.
