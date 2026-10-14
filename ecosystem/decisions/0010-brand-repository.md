# ADR-0010: Marka varlıkları reposu (kyrox-brand)

- **Durum:** Accepted
- **Tarih:** 2026-10-14
- **Karar verenler:** KYROX ekosistem sahipleri

## Bağlam

KYROX ürünleri Kyrox Studio markası altında yayınlanıyor: Fair CRM, Fair Stand ve kyrox.studio web sitesi. Logo şimdiye kadar her repoya ayrı ayrı PNG olarak kopyalandı. Fair CRM'de hâlâ eski, dokulu logo duruyor (`.STUDİO` yazımı ve eski slogan ile).

2026-10-14'te logo yeniden çizildi. Dokulu versiyonlar kaldırıldı; tek logo artık düz, vektör versiyon. Bu logonun ve renklerinin tek bir yerden dağıtılması gerekiyor. Aksi halde her ürün farklı bir logo ve farklı renk kodu kullanmaya devam eder.

Logo dosyaları (SVG, PNG, favicon) ve renk tanımları uygulamaların doğrudan kullandığı dosyalardır. Bunlar insan için yazılmış doküman değildir. Dolayısıyla `kyrox-platform`'a ait değildirler. Ama hiçbir ürüne de ait değildirler, çünkü hepsi tarafından kullanılırlar.

## Karar

`kyrox-studio/kyrox-brand` reposu marka varlıkları reposu olarak kabul edilir.

Kapsamı:

- logo dosyaları: SVG (kaynak), PNG, favicon, profil görselleri,
- makinenin okuduğu marka tanımları: `tokens/colors.css`, `tokens/tokens.json`,
- logoyu vektör kaynaktan yeniden üreten betikler (`tools/`).

Bu repo şunlar **değildir**:

- marka kurallarının yazıldığı yer. Kurallar [standards/brand/BRAND_STANDARD.md](../../standards/brand/BRAND_STANDARD.md) dosyasındadır,
- bir ürünün arayüz renk sistemi. Ürün arayüz token'ları ürünün kendi reposunda kalır ([UI Foundation Standard](../../standards/ui/UI_FOUNDATION_STANDARD.md)),
- proje fotoğrafı, render veya video arşivi. Büyük medya dosyaları repoya girmez.

## Sahiplik ve sınırlar

- Marka kuralları (logo kullanımı, renkler, yazım) `kyrox-platform/standards/brand/` altındadır. `kyrox-brand` README'si yalnızca dosya listesi verir ve kurallar için buraya link verir.
- Ürünler logoyu `kyrox-brand`'den kopyalar. Ürün reposundaki logo dosyası elle düzenlenmez. Logo değişirse önce `kyrox-brand` güncellenir, sonra ürünler.
- `kyrox-brand` hiçbir ürün davranışına, kimlik doğrulamaya veya veriye sahip değildir.

## Teslim profili

Feature profili: `maintenance` / marka varlıkları.

SaaS etki sınıflandırması:

- organizasyona ait veri / tenant izolasyonu: N/A. Repo sadece statik dosya içerir.
- yetki kapsamı: N/A.
- Core ve ürün sahipliği: etkilenir ve bu ADR ile çözülür. `kyrox-brand` ürün veya platform davranışına sahip değildir.
- plan / entitlement: N/A.
- kullanım / kota: N/A.
- organizasyon yaşam döngüsü: N/A.
- secret / üretim güvenliği: N/A. Repoda secret yoktur ve olmamalıdır.
- arka plan işleri / audit: N/A.
- dışa aktarma / saklama / silme: N/A.
- ölçek / altyapı: N/A.

## Kabul

Bu karar şu koşullar sağlandığında tamamlanmış sayılır:

1. `kyrox-brand` `kyrox-studio` organizasyonu altındadır,
2. [REPOSITORY_STRATEGY.md](../REPOSITORY_STRATEGY.md) ve [DOCUMENT_GOVERNANCE.md](../DOCUMENT_GOVERNANCE.md) repoyu tanır,
3. marka kuralları `standards/brand/BRAND_STANDARD.md` altında tek kaynak olarak durur,
4. `kyrox-brand` README'si kural tekrar etmez,
5. Fair CRM eski dokulu logoyu yeni logo paketiyle değiştirir.

## Sonuçlar

### Olumlu

- tüm ürünler aynı logoyu ve aynı renk kodlarını kullanır,
- logo değişikliği tek bir yerden başlar,
- tasarımcıya veya matbaaya tek bir paket verilir.

### Olumsuz

- ürünler logoyu kopyaladığı için logo değişince her ürüne ayrı PR gerekir,
- logonun `.studio` yazısı Inter fontuyla üretildiği için yeniden üretmek Inter fontunun kurulu olmasını gerektirir.

## İlgili

- [Repository strategy](../REPOSITORY_STRATEGY.md)
- [Marka standardı](../../standards/brand/BRAND_STANDARD.md)
- [ADR-0001](0001-repository-strategy.md)
- [ADR-0009](0009-demo-recorder-repository.md)
