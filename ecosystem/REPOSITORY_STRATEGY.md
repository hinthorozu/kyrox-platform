# Repository Strategy

Fixed KYROX repository model. Changes require a new ADR. Decision records: [ADR-0001](decisions/0001-repository-strategy.md), [ADR-0007](decisions/0007-fair-stand-product-ownership.md) and [ADR-0010](decisions/0010-brand-repository.md).

## The repositories

| Repository | Purpose | Contains application code? | Contains Markdown docs? |
|------------|---------|----------------------------|-------------------------|
| **kyrox-platform** | Management and documentation hub | No | **Yes — only docs hub** |
| **kyrox-core** | Reusable SaaS backend platform | Yes | **No** |
| **kyrox-fair-crm** | First CRM product on KYROX Core; hosts Fair Stand configurator shell and Admin catalog UI with same-origin proxy | Yes | **No** |
| **kyrox-fair-stand** | Fair Stand configurator runtime plus independent catalog API (`:8002`) and `fair_stand` database | Yes | Machine-readable contracts plus Fair Stand runtime docs required by that repo's change-gate |
| **kyrox-brand** | Marka varlıkları: logo dosyaları (SVG/PNG/favicon), renk token'ları ve logoyu yeniden üreten betikler | Hayır — yalnızca statik dosyalar ve betikler | Hayır — kısa bir dosya listesi README'si dışında yok; marka kuralları `standards/brand/` altında |
| **kyrox-web** | kyrox.studio web sitesi: özel WordPress teması ve sunucu kurulum dosyaları | Evet — tema ve kurulum; içerik WordPress veritabanında | Hayır — kurulum README'si dışında yok |

All **ecosystem** and **cross-product** human documentation is maintained under this repository. See [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md). Fair Stand keeps its own runtime contracts in `fair-stand` because that repository's change-gate is machine-verified there; product ownership and ecosystem rules remain here.

## Responsibilities

### kyrox-platform

- Ecosystem vision, roadmap, status, workflow
- Cross-repo ADRs and repository strategy
- Project documentation trees under `projects/`
- Shared standards under `standards/`
- Historical archive under `archive/`

Nothing in this repo is deployed. It does not contain application `backend/` or `frontend/` packages.

### kyrox-core

- Authentication and identity
- Organization / membership multi-tenancy primitives
- Shared platform services (audit, settings, jobs, notifications)
- Public HTTP APIs and contracts consumed by products

Core is the shared backend foundation for all KYROX products. Documentation: [projects/kyrox-core/](../projects/kyrox-core/). Core must not contain Fair Stand Item/Category domain logic.

### kyrox-fair-crm

- CRM domain features
- Product UI and CRM product database (`crm_` tables)
- Data integration / import / scraper product workflows
- Product deployment and configuration
- Fair Stand configurator mount, Admin catalog screens, and same-origin `/api/v1/fair-stand/` proxy — not the catalog process or `fair_stand` database

fair-crm is the reference CRM product that validates Core in real use. Documentation: [projects/fair-crm/](../projects/fair-crm/).

### kyrox-brand

- Kyrox Studio logo dosyaları ve makinenin okuduğu marka tanımları (`tokens/`)
- Ürünler logoyu buradan kopyalar; marka kuralları [standards/brand/BRAND_STANDARD.md](../standards/brand/BRAND_STANDARD.md) dosyasındadır
- Ürün davranışına, kimlik doğrulamaya veya veriye sahip değildir ([ADR-0010](decisions/0010-brand-repository.md))

### kyrox-web

- kyrox.studio için özel WordPress teması (onaylı tasarım, koyu ve krem varyant), içerik yapıları ve başlangıç içeriği
- WordPress ve MariaDB için Docker Compose tanımı, nginx site şablonu ve kurulum betiği; secret içermez
- İçerik (yazılar, sayfa metinleri, görseller) WordPress veritabanında ve yükleme klasöründe durur, panelden yönetilir
- Ürün davranışına, Core kimliğine veya ürün verisine sahip değildir ([ADR-0011](decisions/0011-web-site-repository.md))

### kyrox-fair-stand

- Configurator runtime, catalog UI, scene/renderer, module behavior, client project persistence
- Item/Category catalog API and PostgreSQL `fair_stand` database
- Does not own Core auth and does not own CRM customer/fair/todo data

Documentation: [projects/fair-stand/](../projects/fair-stand/).

## Boundaries

1. **Platform vs implementation** — Decide and document in kyrox-platform; implement in kyrox-core, kyrox-fair-crm, or kyrox-fair-stand according to ownership.
2. **Core vs product** — Core never depends on products; products depend on Core via HTTP only ([ADR-0002](decisions/0002-core-product-separation.md)).
3. **Fair Stand vs Fair CRM** — CRM hosts Fair Stand UI and Admin catalog screens. Catalog API/DB run as the Fair Stand process (`:8002`, database `fair_stand`). Hosting the UI is not Item domain ownership ([ADR-0007](decisions/0007-fair-stand-product-ownership.md), [ADR-0008](decisions/0008-fair-stand-independent-service.md)).
4. **No unapproved optional repos** — Do not create kyrox-ui, kyrox-sdk, kyrox-docs, or similar without an ADR. Fair Stand is recognized by ADR-0007/0008. `kyrox-brand` ADR-0010 ile onaylanmış marka varlıkları reposudur ve ürün/runtime davranışına sahip değildir. `kyrox-web` ADR-0011 ile onaylanmış web sitesi reposudur; ürün davranışına sahip değildir.
5. **No Markdown ecosystem-rule trees in Core/CRM** — Keep ecosystem/shared docs here. Fair Stand may keep runtime change-gate contracts in-repo.

## Naming and ownership

- Repositories use the `kyrox-` prefix and match their GitHub names (`kyrox-core`, `kyrox-fair-crm`, `kyrox-fair-stand`). Product names in code stay `fair-crm` / `fair-stand` (service names, prefixes below).
- Fair Stand tables/APIs use the `fair_stand` / `/fair-stand` prefix. CRM tables use `crm_`.
- Cross-repo references use repository names and milestone IDs (for example M4, ADR-0001).
- `kyrox-brand` ve `kyrox-web` stüdyonun tamamına ait oldukları için `kyrox-` önekini kullanır.
- Tüm repolar `kyrox-studio` GitHub organizasyonu altındadır.

## When to add a repository

Adding another repository (beyond those recorded here) requires:

1. An ADR in `ecosystem/decisions/`
2. Updates to [ROADMAP.md](ROADMAP.md) and this file
3. Explicit approval before creating the remote repository

## Related

- [ADR-0001: Repository strategy](decisions/0001-repository-strategy.md)
- [ADR-0002: Core and product separation](decisions/0002-core-product-separation.md)
- [ADR-0007: Fair Stand product ownership](decisions/0007-fair-stand-product-ownership.md)
- [ADR-0009: Demo recorder repository](decisions/0009-demo-recorder-repository.md) (Deprecated; repo silindi)
- [ADR-0010: Marka varlıkları reposu](decisions/0010-brand-repository.md)
- [ADR-0011: kyrox.studio web sitesi reposu](decisions/0011-web-site-repository.md)
- [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md)
- [STATUS.md](STATUS.md)
