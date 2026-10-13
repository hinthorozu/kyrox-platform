# Fair Stand — BASE ailesi Item migration (handoff)

> **TARİHÎ HANDOFF.** Oturum notudur; güncel sistem açıklaması değildir. Runtime kimliği `itemKey`; `catalogKey` hydrate cutover cümleleri bayat. Güncel: `fair-stand` deposundaki `docs/items/definitions/BASE_*.md` ve `audit/SISTEM_MUTABAKAT_RAPORU.md`. 2026-10-13'te `fair-stand/fair-stand-base-family-migration-handoff.md` adından buraya taşındı.

Durum: **implementasyon tamam; commit/push yok.** (tarihî not)
Local: `contract:verify` ✓ · `npm test` 624 ✓ · `build` ✓ · full E2E `28/28` (`--workers=1`; default parallel lokalında timeout flake).

Repo: `fair-stand` · `Version2` (TV/çöp/overlay flush PR #131 merge edildi).

## Sıra

1. Sweep + change-contract taslağı (tests affected; browser domain varsa targeted E2E)
2. **10 satır plan** (dosyalar, COMPOSITE_ITEMS vs recipe, wall_base sınırı, test listesi) → **onay bekle**
3. Onay sonrası implement + docs (definitions canonical; bugünkü MD’ler → current-system)
4. Targeted: `test/baseModule.test.js`, `test/baseRecipes.test.js`, `test/baseTopsItemContract.test.js` + yeni parent contract testi (3× getItem, recipe parity, wall_base izolasyonu)
5. E2E: üç baza drag + save itemKey/catalogKey + faces persist
6. Gate → targeted → npm test → build → E2E → tarayıcıda üçünü sürükle

## Önce oku (kod yazma)

SYSTEM_CHANGE_GATE.md, SYSTEM_IMPACT_SWEEP.md, SYSTEM_DEVELOPMENT_CONTRACT.md, PROJECT_RULES.md, ARCHITECTURE_RULES.md, ITEM_CONTRACT.md, ITEM_CONTRACT_CHECKLIST.md, ITEM_MIGRATION_RULES.md, MODULE_BEHAVIOR_STANDARD.md.

## Referans kalıp

- Parent: `door_100` / `wall_showcase_*` → **COMPOSITE_ITEMS** + recipe BOM
- **Kullanma:** COMMERCIAL_ITEMS / fridge kalıbı / `getCommercialItemForType('base')`

## Kapsam

- Parents: `BASE_100`, `BASE_150`, `BASE_200`
- Tek type: `base` · width 100/150/200 · depth/height 50
- `itemKey = catalogKey`
- Catalog / factory default ölçü → `getItem`
- Recipe sahibi: `moduleRecipes.js` · miktar/unit uydurma yok
- Behavior: `moduleBehavior.js` → base (free, 50 cm snap, footprint, logical-fixture)

## Alt Item’lar (yeniden migrate etme)

`base_top_107_50` / `157_50` / `206_50`, `profile_91` / `140_5` / `190` / `41_5`, `upright_49_5`, `panel_98` / `147_5` / `197` / `48_5`, `connector_start`, `connector_single` — zaten `productionParts.js` + tanımlar.

## Ürün kararları

- Bileşik Item (reçete var); parametrik genişlik varyantı; ayrı type yok
- BOM: mevcut recipe parity; yeni part yok
- `wall_base_100/150/200` **bu iş değil** (type: base-wall); aynı `base_top_*` satırını paylaşır — reçete/quantity bozma
- Eski save: alias yok; `itemKey` yoksa load’da `catalogKey → hydrate`
- Placement / editable faces / procedural renderer / context-menu parity
- Renderer kalınlık/overhang business SoT değil

## Yapma

TV / tvConfig / COMMERCIAL_ITEMS / LED · wall_base_* parent migration · `if (itemKey === 'BASE_150')` behavior · recipe miktarını “düzeltme” · commit/push

## Tuzak

`createBaseModuleState(widthCm)` type+width ile gidiyor; catalogKey factory’den sonra yazılıyor. Cutover: factory `getItem(catalogKey)` (veya eşdeğer). Üç key, bir type.

## Envanter MD

`docs/items/definitions/BASE_100.md` | `BASE_150.md` | `BASE_200.md` (composition: standalone satırı yanlış; kod recipe)

## Bitti sayılır

Üç `BASE_*` `getItem` ile çözülür; factory Item’dan default; type `base` tek davranış; recipe/alt Item miktarı aynı; wall_base kırılmaz; runtime parity; regression yeşil.
