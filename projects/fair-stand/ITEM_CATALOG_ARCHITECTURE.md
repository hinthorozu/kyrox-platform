# Fair Stand Item / Category katalog mimarisi (as-built)

Bu belge Fair Stand Item ve Category sisteminin **yerelde doğrulanmış as-built mimarisidir**. Ürün sahipliği [ADR-0007](../../ecosystem/decisions/0007-fair-stand-product-ownership.md) ile tanımlıdır. Runtime Item semantiği `fair-stand` deposundaki `docs/items/contract/ITEM_CONTRACT.md` dosyasındadır; bu dosya o sözleşmeyi kopyalamaz, fiziksel soT ve hosting sınırını belgeler.

## Sahiplik

Fair Stand ürünü şunların sahibidir:

- Item semantiği ve kanonik kimlik `itemKey`
- Category semantiği ve kanonik kimlik: veritabanının ürettiği integer `id`
- Preview semantiği ve kanonik kimlik: veritabanının ürettiği integer `id`
- Item / Category ürün verisi (`fair_stand_*`)
- Catalog projeksiyonu
- Configurator, sahne, renderer tüketimi
- BOM / composition ilişkileri
- Fair Stand FastAPI (`:8002`) ve PostgreSQL `fair_stand`

Fair CRM:

- `/fair-stand` konfigüratör kabuğu (`mountFairStand`)
- Admin katalog / preview React sayfaları
- same-origin `/api/v1/fair-stand/` proxy (Vite / Nginx → `:8002`)
- Fair Stand Item domain owner **değildir**

KYROX Core:

- auth
- organization context
- RBAC / paylaşılan platform
- Fair Stand Item domain **içermez**

CRM kabuğunda `/fair-stand` gömülü olması CRM’e Item sahipliği vermez. `crm_*` tabloları ile `fair_stand_*` arasında iş FK’si yoktur.

## Tek kaynak

Kanonik Item ürün verisi şu zincirden gelir:

```text
PostgreSQL fair_stand (ayrı DB)
→ Fair Stand API (:8002)
→ same-origin `/api/v1/fair-stand/...` (CRM Vite/Nginx proxy)
→ Fair Stand catalog bootstrap
→ bellek içi Item registry
→ catalog / designState / scene / renderer / BOM
```

Kurallar:

- Static `ITEMS` master yoktur.
- Static `CATALOG_CATEGORIES` master yoktur.
- DB/API otoritedir.
- Bootstrap başarısız olursa `items.js` veya başka bir JS master’a fallback **yoktur**.
- Dual source of truth yoktur.
- Bootstrap başarısızsa configurator fail-closed durur; yarım registry ile sahne açılmaz.

`items.js` bellek içi registry / facade’dır; 96 Item’lık dondurulmuş master taşımaz. `catalog.js` Category listesini bootstrap’ten alır; ikinci Category master değildir.

Catalog, Item master’ın **projeksiyonudur**. İkinci Item master değildir.

## Kimlikler

| Kimlik | Anlam |
|--------|--------|
| `itemKey` | Kanonik Item kimliği |
| `id` | Kanonik Category kimliği (DB-generated INTEGER) |
| `id` | Kanonik Preview kimliği (DB-generated INTEGER) |

Category string `catalog_key` / `catalogKey` yoktur. Runtime ürün kimliği olarak Category `id` okunmaz / yazılmaz; Item kimliği yalnız `itemKey`dır.

## Veritabanı

Tablolar ayrı PostgreSQL veritabanı `fair_stand` içindedir (`fair_stand_*` ad alanı). Katalog tabloları ilişkiseldir (JSON / EAV yok) ve `organization_id` taşımaz. Proje kaydı `fair_stand_projects` satırıdır: `payload` JSONB `{stand, modules}`, zorunlu `customer_id` UUID (`crm_customers` FK’si yok). Katalog FK’lerinin varsayılanı `ON DELETE CASCADE` + `ON UPDATE CASCADE`dır. İki açık istisna `ON DELETE RESTRICT` kullanır: `fair_stand_items.item_type` ve `fair_stand_items.unit`. Ürün silme stratejisi fiziksel DELETE değil `is_active` ile deaktive etmektir.

Migration head (Stand): `0058_item_cost_enabled`. `0058` `fair_stand_items.is_cost_enabled` kolonunu ekler: BOOLEAN NOT NULL, default false. Mevcut satırlar false kalır. Kolon fiyat, birim ve reçete miktarı değildir. `0053_item_type_scene_behavior` item type sınıflandırmasını sahne davranışından ayırır. `0043` / `0044` cam panel SKU satırıdır, kolon eklemez. İlk şema `0001_fair_stand_schema`. CRM leftover drop: `0089_drop_fair_stand_tables`. Historical CRM revisions `0084`–`0088` yalnızca eski `fair_crm` kopyasını anlatır.

### 1. `fair_stand_categories`

Category satırı. `id` INTEGER PK AUTO INCREMENT birincil anahtardır; ad, sıra (`catalog_index`) ve aktiflik burada durur. `catalog_key` yoktur.

### 2. `fair_stand_catalog_preview_kinds`

Yönetilebilir Catalog Preview entity’si. `id` INTEGER PK AUTO INCREMENT birincil anahtardır ve `fair_stand_items.preview_id` FK hedefidir. İkinci preview FK yoktur. `preview_key` yoktur.

Satır alanları: `display_name`, `markup`, `css_code`, `sort_index`, `is_active`, `created_at`, `updated_at`.

Runtime source of truth bu tablodur. Fair Stand generic renderer (`catalogPreviewRenderer.js`) bootstrap `previewKinds` kaydını Item context’i ile DOM/CSS silüetine çevirir. Key-specific JS renderer map yoktur. Fiziksel DELETE yok; kullanımdayken archive reddedilir, aksi halde `is_active=false`.

Super Admin Fair CRM Admin ekranlarından SYSTEM izinleriyle CRUD yapar. OrganizationAdmin ve özel org rolleri bu izinleri alamaz.

### `fair_stand_units`

Global ölçü birimi kataloğu. `id` INTEGER PK AUTO INCREMENT. Kolonlar: `unit_key` (addan üretilen unique teknik kimlik; JSON `unitKey`; ad değişince yeniden üretilir), `name`, `symbol`, `is_active` (default true), `created_at`, `updated_at`. `organization_id` yoktur. Migration unit satırı eklemez. `fair_stand_items.unit` nullable `VARCHAR(64)` kolonudur ve `fair_stand_units.unit_key` hedefine gider: `fk_fair_stand_items_unit_key`, ON UPDATE CASCADE, ON DELETE RESTRICT. Unit key değişince bağlı Item değerlerini veritabanı aynı transaction içinde günceller. Uygulama bu kopyayı yapmaz. Archive yalnız `is_active=false` yazar; key ve Item unit değerleri durur. Inactive bir unit key’i Item’a yazmak reddedilmez; FK yalnız varlığı garanti eder. Yönetim Fair Stand admin API `/admin/units` üzerindedir. Yetki mevcut SYSTEM `fair_crm.admin.fair_stand.catalog.read|create|update|archive` izinleridir. CRM yalnız Super Admin `Ölçü Birimleri` ekranını sunar. Alembic head `0058_item_cost_enabled`.

### `fair_stand_item_type` ve `fair_stand_item_type_scene_behavior`

`fair_stand_item_type` yalnız sınıflandırmadır: `id`, `key`, `display_name`, `is_active`, `created_at`, `updated_at`. Item `item_type` bu tablonun `key` kolonuna gider (ON UPDATE CASCADE, ON DELETE RESTRICT). Bu FK değiştirilmedi.

Sahne davranışı isteğe bağlı 1:1 child tablodadır: `fair_stand_item_type_scene_behavior`. PK ve FK `item_type_id` → `fair_stand_item_type.id`, ON UPDATE CASCADE ve ON DELETE CASCADE. Ayrı `scene_enabled` kolonu yoktur. Behavior satırı varsa tip scene-capable’dır ve bootstrap bugünkü düz `placement`, `collision`, `moveSnapCm`, `ghost` alanlarını verir. Behavior satırı yoksa tip non-scene’dir ve bu alanlar payload’da yoktur.

`production` non-scene sınıflandırmadır. `digital_print`, `mesh_fabric`, `lightbox_fabric` ve `foam_logo` bu tipe bağlı gizli Item’lardır. `catalog_visible` drag/drop katalog görünürlüğüdür. `is_render` çizim bayrağıdır. Scene capability bu iki bayrak değildir.

Proje BOM’u bu Item’lara formül gömmez. `collectPrintAreas` mevcut baskı alanı toplamını üretir; `resolveProjectBom` o toplamı `resolveItemBom` ile leaf satıra çevirir. Dijital Baskı bölümü `digital_print`, Mesh - Delikli Branda bölümü `mesh_fabric`, Lightbox Bezi bölümü `lightbox_fabric`, Strafor Logo bölümü `foam_logo` olur. Birim Item kataloğundaki `unit` değeridir. Detay satırları (`printAreas`) durur. Bu key’ler bileşen reçetesinde yoktur; leaf, reçete miktarına eklenerek ikinci kez sayılmaz.

Kayıtlı bir tipin behavior’ı yokken sahne API’si duvar paketine düşmez; `moduleBehavior.js` hata verir. Registry’de hiç olmayan eski string için mevcut duvar fallback’i durur.

### 3. `fair_stand_items`

Ana Item satırı. `item_key`, ad, `item_type`, catalog görünürlüğü, `category_id`, `catalog_item_index` ve **`preview_id`** burada durur. `category_id` `fair_stand_categories.id` FK’sıdır (CASCADE/CASCADE). `is_cost_enabled` BOOLEAN NOT NULL, default false; JSON `isCostEnabled`. Item'ın ilerideki maliyet hesabına dahil olup olmadığını söyler. Fiyat tutmaz ve reçete miktarını değiştirmez.

Preview’in Item üzerindeki gerçek alanı `fair_stand_items.preview_id`dır. `fair_stand_catalog_preview_kinds` hem FK bütünlüğünü hem de markup/CSS tanımının tek kaynağını taşır.

### 4. `fair_stand_item_dimensions`

Kanonik fiziksel ürün ölçüleri (`width_cm`, `depth_cm`, `height_cm`, `length_cm`, `thickness_cm`, `mount_height_cm`, `wall_gap_cm`).

### 5. `fair_stand_item_scene_dimensions`

Sahneye özgü ölçü ezme katmanı. Runtime kuralı: `sceneDimensions[field] ?? dimensions[field]`. Yeni length→width remap uydurulmaz.

### 6. `fair_stand_item_strip_occupancy`

Strip occupancy üstverisi (`align`, `strip_count`).

### 7. `fair_stand_item_assets`

Item → kanonik asset referansı (`asset_role`, `relative_path`). Binary blob tutulmaz.

### 8. `fair_stand_item_components`

Ebeveyn–çocuk composition / BOM satırları (`quantity`, `sort_order`). Özyinelemeli A→B→C desteklenir; A→B→A yazımda reddedilir.

### 9. `fair_stand_item_video_walls`

Video wall yapısı (`rows`, `cols`, `panel_item_key`).

### 10. `fair_stand_item_body_parts`

Showcase / gövde çocuk Item rolleri (`side`, `horizontal`, `glass_shelf`).

Stand zarfı Item/Category katalog tablosu değildir. Canonical: Fair Stand `docs/refactor/STAND_DIMENSIONS.md`.

## Asset / GLB model

GLB/JPG binary DB’de saklanmaz.

Fiziksel dosyalar Fair Stand static storage altındadır:

`fair-stand/public/models/`

DB `fair_stand_item_assets` “bu Item hangi kanonik dosyayı kullanır?” sorusunu cevaplar.

Örnek:

```text
item_key = chair_eames
asset_role = model
relative_path = eames_chair.glb
```

Backend aggregate `modelFile = eames_chair.glb` üretir. Fair Stand renderer bellek içi registry’den `item.modelFile` okur, `/models/<modelFile>` yolunu Three.js `GLTFLoader` ile yükler.

Item-specific model dosya adı renderer kodunda ikinci master olarak hardcode edilmez.

`default_screen` rolü aynı mantıktadır. Örnek: `tv-screen.jpg`. Aggregate alanı `defaultScreenFile`dır.

Kullanıcı proje görseli (`imageAssetId`) kanonik Item asset değildir; `fair_stand_item_assets` tablosuna taşınmaz. Binary `fair_stand_project_assets` ve disk yolundadır; IndexedDB önbellektir.

## Ürün verisi vs kod

DB’de duranlar (ürün verisi):

- Item / Category kimliği
- catalog metadata
- dimensions / scene dimensions
- material, `default_color` (integer RGB)
- nominal genişlik, connector, panel rolü
- rotasyon / scale bayrakları
- composition, body parts, video wall
- asset referansları
- Item’a özgü diğer kanonik ürün üstverisi

Kodda kalanlar (algoritma / type-family):

- generic renderer
- placement, collision ve snapping algoritması; değerler scene behavior satırından okunur
- `moduleBehavior.js` type-family contract
- catalog preview **renderer implementasyonu**

Örnek: DB `preview_id = 20`; generic renderer bootstrap tanımının markup/CSS’ini çizer. Bilinmeyen preview id fail-closed kalır.

## Proje örneği state

Item master DB’dedir. Kayıtlı proje örneği `fair_stand_projects.payload` (`{stand, modules}`) içindedir. Çizim kaydı `customer_id` değiştirmez. IndexedDB (`projectStore`) aynı kaydın önbelleğidir ve Item master’a gömülmez.

Proje örneğine ait olanlar (örnek):

- instance `id`
- x / y / z, rotation, wall
- yüzey rengi ezmesi
- `imageAssetId`, `imageTransform`
- `shelfLightingOn` ve diğer runtime override’lar

Bunlar kanonik Item master değildir.

## API / bootstrap

Okuma uçları (Fair CRM session auth, mevcut `X-Organization-Id` entegrasyonu; yeni permission kodu yok):

- `GET /api/v1/fair-stand/catalog/bootstrap`
- `GET /api/v1/fair-stand/items/{item_key}`

Bootstrap tek snapshot’ta `revision`, `categories`, `items` ve `previewKinds` döner. `standDimensions` aynı HTTP cevabında taşınır ama Item/Category katalog modeli değildir; `docs/refactor/STAND_DIMENSIONS.md`.

Akış:

```text
CRM authenticated shell
→ Fair Stand mount (catalogHeaders host window’a yazılır)
→ catalog bootstrap await
→ categories + Items + previewKinds
→ initializeStandDimensions(standDimensions)
→ initialize in-memory registry
→ configurator start
```

Registry initialize edilmeden `getItem()` fail-fast / fail-closed’dır.

Bilinmeyen `item_key` API’de 404 / fail-closed.

## Son doğrulanan lokal sayılar

Bu sayılar mimari invariant değildir; **son doğrulanan lokal implementation** özetidir. Fast-aging’dir. Güncel canlı durum [PROJECT_STATUS.md](PROJECT_STATUS.md) içindedir.

| Ölçüm | Değer |
|-------|--------|
| Migration | Fair Stand head `0058_item_cost_enabled` |
| Categories | 6 |
| Items | 121 |
| Visible Items | 58 |
| Components | 186 |
| Assets | 19 |
| JSON / JSONB / EAV | Katalog ilişkisel. Proje `payload` JSONB `{stand, modules}`. EAV yok |

## İlgili belgeler

- [ADR-0007](../../ecosystem/decisions/0007-fair-stand-product-ownership.md)
- [README.md](README.md)
- [PROJECT_STATUS.md](PROJECT_STATUS.md)
- Fair Stand runtime: `docs/items/contract/ITEM_CONTRACT.md`
