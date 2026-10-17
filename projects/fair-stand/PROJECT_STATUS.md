# Fair Stand — Proje Durumu

| Alan | Değer |
|------|--------|
| Son doğrulama | **2026-10-18** |
| Implementation deposu | `kyrox-studio/kyrox-fair-stand` |
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

## Otomatik kayıt süresi — 2026-10-18

`kyrox-fair-stand` PR #282.

**Kullanıcı tarafı**
- Proje kartında Kaydet düğmelerinin altında **Otomatik kayıt** listesi var: Kapalı (Otomatik Kayıt Kapalı), 3, 5, 7 ve 10 dk. Varsayılan 3 dk.
- Önceki sabit 30 sn bekleme ve 60 sn üst sınır kalktı. Seçilen süre hem bekleme hem üst sınırdır.
- Kapalı seçilince süreli kayıt yapılmaz. Durum satırı kaydedilmemiş değişikliği gösterir; kayıt **Kaydet** ile elle yapılır.
- Kaydedilmemiş değişiklik iki durumda hemen kaydedilir: sekme gizlenince ve editörden çıkılınca. Bu, Kapalı seçiliyken de geçerlidir.
- Sayfa kapatılırken veya yenilenirken tarayıcı uyarı verir.

**Veri.**
- Süre seçimi yalnız tarayıcıda tutulur (`localStorage`, `fairStand.autosaveMinutes`).
- Proje kaydı, şema, migration ve API değişmez.

**SaaS etkisi.** Organization izolasyonu, yetki, entitlement ve kullanım ölçümü değişmez. Item master, katalog ve BOM etkilenmez.

## Sahne editörü: geri al / ileri al — 2026-10-18

[GROUP_LOCK_ROADMAP.md](GROUP_LOCK_ROADMAP.md) Faz 2. `kyrox-fair-stand` PR #281 merge edildi; CI (contract gate, test, pytest, build, Chromium E2E) yeşil.

**Kullanıcı tarafı**
- **Ctrl/Cmd+Z** geri al; **Ctrl/Cmd+Y** ve **Ctrl/Cmd+Shift+Z** ileri al. Üst bantta Geri al / İleri al düğmeleri.
- Kapsam: taşıma, döndürme, ekleme, silme, çoğaltma, renk, görsel, cam, separatör, kumaş, kilit ve zemin.
- Son 50 adım tutulur.
- Geçmiş kaydedilmez. Proje açılınca, yeni projede ve görsel silinince sıfırlanır; geçmiş revizyon görünümünde kapalıdır.

**Veri.** Proje kaydı, şema, migration ve proje sürümü değişmez; geçmiş yalnız tarayıcı belleğindedir.

**SaaS etkisi.** Organization izolasyonu, yetki, entitlement ve kullanım ölçümü değişmez. Item master, katalog ve BOM etkilenmez.

## Sahne editörü: öğe kilidi — 2026-10-17

[GROUP_LOCK_ROADMAP.md](GROUP_LOCK_ROADMAP.md) Faz 1. `kyrox-fair-stand` PR #278 merge edildi; CI (contract gate, test, pytest, build, Chromium E2E) yeşil. Sunucuya yayın bu kayıtta yoktur.

**Kullanıcı tarafı**
- Sağ tık menüsünde **Kilitle / Kilidi aç**.
- **Shift+tık** ile toplu seçim ve sağ tıkla toplu kilitleme.
- Kilitli öğe sürüklenmez, ok tuşları ve Shift+R ile oynamaz, boyutlandırılamaz, silinemez.
- Zincir kaydırması (taşıma, katalogdan bırakma, Ekle/Çoğalt, toplu ekleme) kilitli öğeyi oynatacaksa işlem reddedilir.
- Görünüm işlemleri kilitliyken de çalışır.
- Kopya kilitsiz doğar; "Tüm özellikleri kaldır" kilidi korur.

**Veri.** Kilit proje örneğinin `locked: true` alanıdır. Proje `payload` (`{stand, modules}`) içinde taşınır; şema, migration ve proje sürümü değişmez. İçe aktarmada alan boolean olarak doğrulanır.

**SaaS etkisi.**
- Kilit organization'a ait proje kaydının içindedir; organization izolasyonu, yetki, entitlement ve kullanım ölçümü değişmez.
- Item master, katalog ve BOM etkilenmez; kilit Item/BOM özelliği değildir.

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
