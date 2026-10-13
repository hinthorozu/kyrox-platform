# Fair Stand

KYROX ekosistemindeki fuar standı configurator ürünü.

**Kod deposu:** `https://github.com/hinthorozu/fair-stand`  
**İnsan / AI ekosistem dokümantasyonu:** `kyrox-platform` altındaki bu ağaç  
**Runtime sözleşmeleri:** `fair-stand` deposu (`ITEM_CONTRACT.md`, change-gate)  
**Ekosistem durumu:** [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md)  
**Sahiplik ADR:** [../../ecosystem/decisions/0007-fair-stand-product-ownership.md](../../ecosystem/decisions/0007-fair-stand-product-ownership.md)  
**Item / Category as-built mimari:** [ITEM_CATALOG_ARCHITECTURE.md](ITEM_CATALOG_ARCHITECTURE.md)

## Sahiplik

| Konu | Sahip |
|------|--------|
| Item kimliği (`itemKey`), Category kimliği (DB `id`) ve Preview kimliği (DB `id`) | Fair Stand ürünü |
| Item / Category ilişkisel veri (`fair_stand_*`) | Fair Stand domain |
| Configurator, catalog projeksiyonu, sahne, BOM | Fair Stand deposu |
| Fiziksel PostgreSQL `fair_stand` + FastAPI `:8002` | Fair Stand deposu |
| Auth / org UUID / session | KYROX Core; CRM login köprüsü + same-origin JWT |

| CRM müşteri, fuar, görev, `crm_*` tabloları | Fair CRM |

Fair Stand’ın CRM `/fair-stand` rotasına gömülmesi Item verisini CRM domaini yapmaz.

Catalog, Item’ların projeksiyonudur. Category `id` asla Item kimliği değildir.

Kanonik Item ürün verisi DB/API’den gelir; static JS Item/Category master yoktur. Ayrıntı: [ITEM_CATALOG_ARCHITECTURE.md](ITEM_CATALOG_ARCHITECTURE.md).

## Bu ağaçtaki Fair Stand-only kanonik belgeler

| Belge | Rol |
|-------|-----|
| [ITEM_CATALOG_ARCHITECTURE.md](ITEM_CATALOG_ARCHITECTURE.md) | Item / Category as-built mimari (tek kaynak) |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Canlı ürün durumu |
| [ROADMAP.md](ROADMAP.md) | Katalog / platform iş kuyruğu; configurator üst seviye planı ve FAZ 4 detayı `fair-stand` deposundadır |
| [ROADMAP_PHASE_5_6.md](ROADMAP_PHASE_5_6.md) | FAZ 5 (Final BOM) ve FAZ 6 (maliyet / Fair CRM) detaylı planı |
| [PRODUCT_FUTURE.md](PRODUCT_FUTURE.md) | Henüz faza yerleşmemiş gelecek ürün gereksinimleri |
| [RENDER_FUTURE_BACKLOG.md](RENDER_FUTURE_BACKLOG.md) | Render / HDRI / PBR gelecek backlog'u |

Tarihsel Fair Stand kayıtları (normatif değil): [../../archive/fair-stand/](../../archive/fair-stand/) — `MILESTONES.md`, `CHANGELOG_2026-08.md`, `LEGACY_TRASH.md`, `BASE_FAMILY_MIGRATION_HANDOFF.md`.

Runtime Item sözleşmesi, change-gate belgeleri ve CI'ın okuduğu `ROADMAP.md` / `ROADMAP_PHASE_4.md`, CI orada doğruladığı için `fair-stand` deposunda kalır.

## İlgili

- [Document Governance](../../ecosystem/DOCUMENT_GOVERNANCE.md)
- [Repository strategy](../../ecosystem/REPOSITORY_STRATEGY.md)
- [Core integration guide](../kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)
