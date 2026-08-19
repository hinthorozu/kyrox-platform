# Platform Ownership Review

Status: Proposed — ownership decisions required before implementation or migration
Date: 2026-07-23

## Purpose

Before adding or moving infrastructure, decide explicitly whether the capability belongs to KYROX Core, a product such as FAIR CRM, or a product-specific handler/adapter. Do not duplicate a shared capability in product repositories simply because the first implementation appeared there.

The key question is:

> Is this generic platform infrastructure reusable by multiple KYROX products, or is it product/domain-specific behavior?

No ownership decision should be inferred silently. If ownership is unclear, stop and document the boundary before implementation.

## General ownership rule

### KYROX Core candidate

A capability is a Core candidate when it is generic and reusable across products without FAIR CRM-specific semantics.

Examples:
- authentication / authorization / organization / membership
- audit
- generic settings
- generic background-job infrastructure
- generic notification infrastructure
- generic Operation Engine lifecycle/capability infrastructure, if it is intended to be reused by multiple KYROX products
- generic email delivery infrastructure, if it is intended to be reused by multiple KYROX products

### Product repository

A capability stays in FAIR CRM when it contains FAIR CRM business meaning or workflow.

Examples:
- fairs, customers, participations
- FAIR CRM automation types and their business rules
- recipient selection based on fairs/customers/segments
- CRM-specific activity/history writes
- Web Scraper, enrichment, bulk-email handlers that orchestrate FAIR CRM domain work

### Handler / adapter

Site/provider-specific execution logic stays behind the relevant handler/adapter boundary.

Examples:
- TUYAP-specific scraping
- provider-specific extraction/parsing behavior
- adapter-specific runtime configuration

## Email ownership — explicit review item

Email must be separated into generic delivery infrastructure and product-specific orchestration.

Potential Core responsibility:
- SMTP/provider account abstraction
- send email
- queue/worker execution
- retry
- delivery status
- rate limiting
- provider abstraction
- generic attachment/delivery mechanics

FAIR CRM responsibility:
- Bulk Email Handler
- deciding which fair/customer/segment receives email
- selecting CRM template/business context
- exclusions and CRM-specific recipient rules
- writing CRM-specific activity/history/results

Example flow:

FAIR CRM BulkEmailHandler
→ prepares recipients/business context
→ KYROX generic email delivery service
→ SMTP/provider

IMPORTANT: This document does NOT yet declare that the generic email service has already been moved to Core. Before implementation/migration, inspect the existing Core and FAIR CRM email code and make an explicit ownership decision: what belongs in Core, what remains in FAIR CRM, and what remains provider-specific. Do not duplicate or move code until that decision is documented.

## Operation Engine ownership — explicit review item

The same review is required for Operation Engine infrastructure.

Potential shared/Core layer:
- operation lifecycle contract
- start/cancel/pause/resume/retry/schedule capability model
- generic run/job state
- generic capability contract

Product layer:
- FAIR CRM automation types
- FAIR CRM handlers
- domain-specific source selection and results

Before moving anything, inspect whether the current FAIR CRM Operation Engine is genuinely generic. Decide explicitly which parts belong in Core and which parts remain product-owned.

## Mandatory rule for future work

For new shared-looking infrastructure:

1. Identify the capability.
2. Decide owner: Core / product / handler-adapter.
3. Document the reason.
4. Only then implement or migrate.

Do not build the same generic infrastructure independently in multiple KYROX products.
