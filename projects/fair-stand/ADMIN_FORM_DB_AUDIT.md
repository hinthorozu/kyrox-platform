# Fair Stand — Admin formu ↔ kod ↔ DB denetimi

| Alan | Değer |
|------|--------|
| Denetim tarihi | 2026-10-18 |
| Kapsam | CRM Admin **Item Tipleri** ve **Item** düzenleme formları |
| Karşılaştırılan | CRM formu (`kyrox-fair-crm` `FairStandSnapCatalogAdminPage.tsx`, `FairStandItemsAdminPage.tsx`) · Fair Stand backend (`models.py`, `admin_snap_catalog.py`, `admin_items.py`, `item_type_behavior_seed.py`) · sahne motoru (`src/moduleBehavior.js` vb.) · canlı `fair_stand` DB (Alembic head `0066_metal_separator_area`) |
| Durum | Yalnız tespit. Kod değişikliği yapılmadı. |

Alanların anlamı için: `kyrox-fair-stand` deposunda `docs/refactor/FAIR_STAND_DB_KULLANIM_KILAVUZU.md` ve `docs/refactor/DATABASE.md`.

## 1. Item tipi (`fair_stand_item_type` + `fair_stand_item_type_scene_behavior`)

**Sonuç: form, backend ve DB birebir uyumlu.**

| Alan | Formdaki seçenekler = backend = DB CHECK |
|------|------|
| `placement` | `wall`, `free`, `wall-overlay`, `top`. Formdaki boş seçenek, sahne davranışı satırı olmayan tip anlamına gelir. |
| `collision` | `segment`, `footprint`, `none` |
| `move_snap_cm` | > 0 |
| `magnetic_snap` | `standard`, `none`, `short-up-joint` |
| `wall_capacity` | `include`, `exclude` |
| `connection_endpoint` | `segment`, `logical-fixture` |
| `collision_depth` | `physical`, `wall-backbone` |
| `endpoint_contact` | `standard`, `thin-wall-endpoint` |
| `boundary_snap` | `stand-edge`, `wall-inner-face` |
| `collision_height` | `full` |
| `ghost_opacity` | 0–1 |

Canlı veri:
- 45 tip var, hepsi aktif.
- 44 tipin sahne davranışı var. Davranışı olmayan tek tip `production` (Üretim); beklenen durum budur.
- Kural dışı değer yok.

**Not (açık):** `ghost_kind` ve `ghost_renderer` formda zorunlu serbest metin. Ancak sahne motoru yalnız `ghost.opacity` değerini kullanıyor; tür ve renderer değerleri yalnız dolu olup olmadıkları için kontrol ediliyor. 44 tipin hepsi aynı değeri taşıyor: `silhouette` / `module-silhouette` / 0.38. Bu iki alan fiilen işlevsiz.

## 2. Item (`fair_stand_items`)

**Sonuç: 4 alan formda serbest metin veya serbest sayı, DB ise sabit liste kabul ediyor.**

Formdaki öneri listesi, DB'de daha önce kullanılmış değerlerden (`distinct`) üretiliyor. Bu alanlar için backend'de ayrıca kontrol yok. Yanlış değeri DB CHECK reddediyor ve kullanıcı yalnız genel bir hata görüyor: "Girilen değerlerden biri geçersiz." Hangi alanın hatalı olduğu söylenmiyor.

| Alan | Form | DB kabul eder | Canlı dağılım (127 item) |
|------|------|------|------|
| `composition_mode` | serbest metin | `NULL`, `recipe` | recipe 31 · NULL 96 |
| `side_insert_rotation` | serbest metin | `NULL`, `inherit`, `default` | inherit 76 · default 1 · NULL 50 |
| `eye_count` | serbest sayı | `NULL`, 2, 3 | 2 → 1 · 3 → 1 · NULL 125 |
| Dönüş üçlüsü: `rotation_step_deg`, `default_rotation_deg`, `side_insert_rotation` | 3 bağımsız alan | Üçü birlikte dolu ya da üçü birlikte boş (`ck_fair_stand_items_rotation_trio`) | Kayıtlar tutarlı (dolu 77, boş 50) |

**DB kısıtı olmayan ama sahne motorunun tam metin beklediği alanlar.** Bu alanlarda yazım hatası hata vermez; ürün sessizce yanlış davranır.

| Alan | Motor beklentisi | Canlı değerler |
|------|------|------|
| `shape` | `L` (`designState.js`) | L 3 · NULL 124 |
| `material` | Raf gövde uyumu için `sunta` (`items.js`) | sunta 26, alüminyum 17, cam 9, mdf 2, ahşap 1, metal 1, NULL 71 |
| `variant` | `wall-short-1`, `wall-short-2` | 4 + 4 · NULL 119 |

**Ölü kolonlar.** `snap_anchor` ve `snap_target_item_type`:
- 127 item'ın hepsinde boş.
- Formda yoklar.
- Bootstrap yükünde yoklar.
- Sahne motoru bunları okumuyor.

**Uyumlu bulunanlar:**
- `unit`: aktif birimlerden seçiliyor; DB FK var.
- `item_type`, kategori ve önizleme listeleri.
- `snap_requires_rule_id` / `snap_provides_rule_id`: form ikisinin birlikte seçilmesini engelliyor; DB'de XOR kısıtı var.
- `default_opacity`: 0–1.
- `catalog_visible` → kategori, sıra ve önizleme zorunlu.
- `is_render` → yüzey bayrakları.
- Pasif tipte aktif item yok.

## 3. Önerilen düzeltmeler (onay bekliyor)

`AGENTS.md` kuralı gereği her madde önce envanterle sunulur; kullanıcı onay vermeden kod yazılmaz.

1. **Açılır listeye çevir:** `composition_mode` (Yok / recipe), `side_insert_rotation` (Yok / inherit / default), `eye_count` (Yok / 2 / 3), `shape` (Yok / L).
2. **Dönüş üçlüsü:** formda üç alanı birlikte doğrula ve tek bir açıklayıcı hata göster.
3. **Backend:** bu alanlar için açık kontrol ve alan adını söyleyen hata mesajı ekle; genel CHECK hatasına düşmesin.
4. **`material` / `variant`:** sabit liste mi (DB CHECK veya ayrı tablo) yoksa öneri listesi mi kalacağı ürün kararıdır.
5. **Ghost alanları:** kaldır, formda gizle ya da motorda gerçekten kullan. Ürün kararıdır.
6. **Ölü kolonlar** (`snap_anchor`, `snap_target_item_type`): migration ile kaldırılması değerlendirilsin. Ürün kararıdır.
