# ADR-0008: Fair Stand catalog API as independent service

- **Status:** Accepted
- **Date:** 2026-09-20
- **Deciders:** KYROX ecosystem maintainers

## Context

ADR-0007 hosted the Fair Stand Item catalog physically inside Fair CRM. Configurator UI already mounts into the CRM `/fair-stand` page. Management screens already live in CRM Admin. The remaining coupling is the catalog API and `fair_stand_*` tables living in the CRM process and `fair_crm` database.

## Decision

1. **Fair Stand API** is a separate FastAPI process (`:8002`) with its own PostgreSQL database `fair_stand` on the same server.
2. **Configurator UI** remains the existing Fair Stand visual UI, mounted into a CRM `div` via `mountFairStand`. There is no second Stand admin product and no CRM `/stand/admin.html` embed. `mountFairStand` may use an internal CSS-isolation iframe; that is not a second application.
3. **Category / preview / item catalog management** remains the existing CRM Admin React pages. Those pages call `/api/v1/fair-stand/...`.
4. **Same-origin Nginx** routes `/api/v1/fair-stand/` to the Stand process. Core JWT + `X-Organization-Id` are reused; no second login.
5. **CRM frontend** still compiles the configurator (`@fair-stand` alias). Catalog/API/schema changes deploy with Stand only. Configurator visual changes still ship with the CRM frontend build.
6. **Leftover `fair_crm.fair_stand_*` tables are dropped** by CRM Alembic `0089_drop_fair_stand_tables` after the Stand DB holds the catalog. Downgrade is not supported; restore from backup if needed.

This amends physical hosting in ADR-0007; product ownership in ADR-0007 is unchanged.

## Related

- [ADR-0007](0007-fair-stand-product-ownership.md)
