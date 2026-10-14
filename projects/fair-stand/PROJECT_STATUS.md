# Fair Stand — Proje Durumu

| Alan | Değer |
|------|--------|
| Son doğrulama | **2026-10-13** |
| Implementation deposu | `kyrox-studio/fair-stand` |
| Hosted backend | Fair Stand FastAPI (`:8002`) / PostgreSQL `fair_stand` |
| Item master | İlişkisel PostgreSQL; catalog bootstrap API |
| Category master | `fair_stand_categories` |
| Catalog | Yalnız Item projeksiyonu |

## Uygulama durumu

**IMPLEMENTATION STATUS:** LOCAL READY

**REMOTE / GITHUB STATUS:** bu görevde değerlendirilmedi / değiştirilmedi.

Lokal runtime acceptance PASS. `deployed` / `merged` / `production` iddiası yoktur.

## Mevcut yetenek durumu

| Alan | Durum |
|------|--------|
| Ürün sahipliği | ADR-0007 ile kanonik |
| Item / Category DB | PostgreSQL `fair_stand`; Fair Stand API |
| Configurator | Fair Stand runtime; Item registry API bootstrap |
| Proje kaydet / yükle | Sunucu PostgreSQL `fair_stand_projects` (payload `{stand, modules}`). IndexedDB yalnız önbellek. Item master değil |
| Tenant-scoped Item katalog | Kapsam dışı; katalog global |
| Static JS Item master | Kaldırıldı |
| Fallback / dual SoT | Yok |
| Migration | Fair Stand Alembic head `0066_metal_separator_area`. `0065_metal_separator` katalogda görünmeyen `metal_separator` Item'ını ekler; `0066` bu Item'ı `metre_kare` birimiyle maliyetlendirilebilir yapar (dönüştürülmüş panel bloğu adet değil en × boy olarak faturalanır). `fair_stand_cost_items` organization Item fiyatını ve manuel kalemi aynı tabloda tutar. ITEM satırında `item_key` zorunlu, `name` ve `unit` boştur. MANUAL satırında `item_key` boştur, `name` ve `unit` zorunludur. `unit` → `fair_stand_units.unit_key`, ON UPDATE CASCADE, ON DELETE CASCADE. Aynı organization aynı Item’ı iki kez yazamaz. Manuel ad ve birim için ek unique yoktur. `fair_stand_items` fiyat kolonu taşımaz. `fair_stand_items.is_cost_enabled` NOT NULL, default false; mevcut satırlar false kalır. Bu bayrak fiyat, birim ve reçete miktarı değildir. `fair_stand_item_type` sınıflandırmadır. Sahne davranışı isteğe bağlı `fair_stand_item_type_scene_behavior` satırıdır; satır yoksa tip non-scene’dir. `production` behavior satırı taşımaz. `digital_print`, `mesh_fabric`, `lightbox_fabric` bu tipe bağlı gizli Item’lardır. `foam_logo` kaldırıldı. Strafor metrekare `illuminated-foam` sahne kaydına yazılır. `tulle_fabric` (görünen ad Tül, tip `tulle-fabric`) tek Item’dır: katalogda görünür, sahneye sürüklenir, BOM miktarı en × boy / 10000 m² olarak aynı `itemKey` ile yazılır ve maliyet kalemi bu `itemKey` ile eşleşir. Kalınlık item master `depth_cm` 0.4 değeridir. İlk yerleşim `default_z_cm` 350 değerini kullanır. `fair_stand_items.unit` → `fair_stand_units.unit_key` FK’sidir: ON UPDATE CASCADE, ON DELETE RESTRICT. Proje BOM’u katalogdaki `elektrik_panosu` satırını her listeye 1 adet yazar; bu satır modül reçetesi değildir. Aynı liste Dijital Baskı, Mesh ve Lightbox alanlarını kendi production kalemlerine, strafor alanını `illuminated-foam` kaydına bağlar. |

Mimari ayrıntı: [ITEM_CATALOG_ARCHITECTURE.md](ITEM_CATALOG_ARCHITECTURE.md).

## Kamera etkileşimi düzeltmesi — 2026-10-13

OrbitControls için kaçırılan fare bırakma, pointer capture kaybı, iptal ve pencere odağı kaybı ele alındı. Normal bırakmada damping korunur; hesap gerçek geçen zamana bağlıdır ve 4/10 FPS koşullarında kare hızına bağlı uzama yapmaz. Blur veya görünürlük kaybı birikmiş kamera hareketini mevcut görünümü değiştirmeden temizler. Nesne yerleşimi, snap, Ctrl/Cmd seçimi, Shift+R ve zemin çizimi kendi akışlarını korur.

Lokal kanıt: 1.124 JavaScript testi; 10 Chromium kamera/etkileşim senaryosu; taşıma/snap, yerleşim ghost'u, zemin alanı ve ViewCube regresyonları. Syntax, build, dependency audit ve change-contract kapıları geçti. Düşük FPS ve blur regresyonları düzeltme öncesinde başarısız, düzeltme sonrasında başarılı olarak ölçüldü. Bu doğrulama fiziksel sorunlu bilgisayarın testinin yerine geçtiği veya canlı deployment yapıldığı anlamına gelmez.

Kapsam yalnız Fair Stand kamera UI/runtime davranışıdır. API, veritabanı, migration, Core sözleşmesi, organization izolasyonu, yetki, kayıt/BOM ve Item master değişikliği yoktur. GitHub teslimat kanıtının sahibi ilgili uygulama PR/CI kayıtlarıdır.

## Son doğrulanan lokal sayılar (fast-aging)

Invariant değildir. 2026-09-18 lokal implementation:

| Ölçüm | Değer |
|-------|--------|
| Categories | 6 |
| Items | 96 |
| Visible Items | 58 |
| Components | 186 |
| Assets | 19 |
| JSON / JSONB / EAV | Katalog ilişkisel. Proje `payload` JSONB `{stand, modules}`. EAV yok |
