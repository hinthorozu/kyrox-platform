# KYROX Shared Standards

This directory contains **reusable, product-independent rules** for the KYROX ecosystem.

If a rule should apply to Fair CRM and could also apply unchanged to a future CRM, ERP, inventory, finance or other KYROX product, it belongs here rather than inside a single project's documentation.

## Reading rule

Before reading a product-specific standard, check this index and read every shared standard applicable to the task. Product documents may add domain detail or explicit exceptions; they must not duplicate or silently redefine these rules.

## Index

### UI / authorization

- [CRUD & UI Authorization Standard](ui/CRUD_UI_AUTHORIZATION_STANDARD.md) — canonical CRUD permission semantics, UI visibility, navigation/route/action gating and backend enforcement.

### Backend

- [Backend Architecture Standards](backend/BACKEND_ARCHITECTURE_STANDARDS.md)

### Other shared areas

- `ai/` — shared AI/agent standards.
- `database/` — shared database standards.
- `git/` — shared Git/repository standards.
- `jobs/` — shared background-job standards.

## Ownership rule

A new rule goes here when another current or future product would reasonably reuse the same behavior. If it is genuinely specific to one product, place it under `projects/<product>/` instead.

One rule must have one canonical source. Do not create a second normative copy inside project docs or code repositories.
