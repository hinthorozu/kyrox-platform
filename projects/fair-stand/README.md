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
| [ROADMAP.md](ROADMAP.md) | Ürün iş kuyruğu |

Runtime Item sözleşmesi ve change-gate, CI orada doğruladığı için `fair-stand` deposunda kalır.

## İlgili

- [Document Governance](../../ecosystem/DOCUMENT_GOVERNANCE.md)
- [Repository strategy](../../ecosystem/REPOSITORY_STRATEGY.md)
- [Core integration guide](../kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md)
