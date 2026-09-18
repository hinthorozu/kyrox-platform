# Fair Stand — Project Status

| Field | Value |
|-------|-------|
| Last verified | **2026-09-18** |
| Implementation repository | `hinthorozu/fair-stand` |
| Hosted backend | Fair CRM bounded context `app.modules.fair_stand` / tables `fair_stand_*` |
| Item master | Relational PostgreSQL via catalog bootstrap API |
| Category master | `fair_stand_categories` |
| Catalog | Item projection only |

## Current capability state

| Area | Status |
|------|--------|
| Product ownership | Canonical in ADR-0007 |
| Item/Category DB | Hosted in Fair CRM PostgreSQL, Fair Stand domain |
| Configurator | Fair Stand runtime; bootstraps Item registry from API |
| Project save/load | Client IndexedDB (not Item master) |
| Tenant-scoped Item catalogs | Not in scope; catalog is global |
