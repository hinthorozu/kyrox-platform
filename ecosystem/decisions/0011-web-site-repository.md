# ADR-0011: kyrox.studio web sitesi reposu (kyrox-web)

- **Durum:** Proposed
- **Tarih:** 2026-10-14
- **Karar verenler:** KYROX ekosistem sahipleri

## Bağlam

Kyrox Studio'nun web sitesi (kyrox.studio) hazırlandı. Site bir ana sayfa, bir blog ve arama motorları ile yapay zekâ asistanları için kimlik dosyalarından (`sitemap.xml`, `robots.txt`, `llms.txt`, schema.org bilgisi) oluşuyor. Blog yazıları Markdown dosyası olarak tutuluyor ve küçük bir derleme betiği siteyi statik HTML'e çeviriyor.

Site şu an geçici olarak `kyrox-brand` reposunda, `claude/web-site-blog` dalında, `web-site/` klasöründe duruyor. Bu yer kalıcı olamaz:

- [ADR-0010](0010-brand-repository.md), `kyrox-brand`'in kapsamını logo dosyaları, renk token'ları ve logoyu üreten betiklerle sınırlar. Web sitesi kodu ve blog içeriği bu kapsamın dışındadır.
- Site kendi yayın döngüsüne sahip: her blog yazısı veya metin değişikliği bir yayın tetikler. Logo dosyalarıyla aynı repoda durursa marka varlıklarının geçmişi site değişiklikleriyle dolar.
- [REPOSITORY_STRATEGY](../REPOSITORY_STRATEGY.md) onaysız yeni repo açılmasını yasaklar; bu yüzden önce bu karar gerekiyor.

## Karar

`kyrox-studio/kyrox-web` reposu, kyrox.studio web sitesinin reposu olarak açılır.

Kapsamı:

- sitenin kaynak dosyaları: sayfalar, şablonlar, stiller, betikler,
- blog yazıları (`src/blog/*.md`),
- kurum bilgisinin tek kaynağı `site.json` (adres, telefon, hizmetler); site, `llms.txt`, `robots.txt` ve schema.org bilgisi bundan üretilir,
- derleme ve önizleme betikleri,
- sitede kullanılan statik dosyalar: logo ve favicon kopyaları, paylaşım görseli, site görselleri.

Bu repo şunlar **değildir**:

- ekosistem dokümantasyonu. Blog yazıları kamuya açık site içeriğidir, ekosistemin nasıl çalıştığını anlatan kural veya plan değildir. Ekosistem kuralları `kyrox-platform`'da kalır,
- marka kurallarının yazıldığı yer. Kurallar [standards/brand/BRAND_STANDARD.md](../../standards/brand/BRAND_STANDARD.md) dosyasındadır,
- logo kaynağı. Logo `kyrox-brand`'den kopyalanır ve burada elle düzenlenmez,
- ürün kodu. Fair CRM ve Fair Stand arayüzleri kendi repolarında kalır; site onlara yalnızca link verir (`fuar.kyrox.studio`).

## Teknik tercih

- **Bağımlılıksız derleyici.** Site, paket kurmadan `node build.mjs` ile derlenir. Astro gibi bir çatı değerlendirildi; mevcut ihtiyaç (ana sayfa, Markdown blog, sitemap, RSS) için ek bağımlılık gerekmediği ve derleme her ortamda kurulumsuz doğrulanabildiği için şimdilik tercih edilmedi. İhtiyaç büyürse ayrı bir kararla geçilebilir.
- **Yayın: Cloudflare Pages.** Kök klasör, `node build.mjs` derleme komutu, `dist` çıktı klasörü. `main` güncellenince site kendiliğinden yayınlanır.
- **Alan adı:** `kyrox.studio` kök alan adı siteye bağlanır. `fuar.kyrox.studio` ve diğer alt alan adları bu karardan etkilenmez.

## Teslim profili

Feature profili: `maintenance` / web sitesi.

SaaS etki sınıflandırması:

- organizasyona ait veri / tenant izolasyonu: N/A. Site statiktir, kullanıcı hesabı yoktur.
- yetki kapsamı: N/A.
- Core ve ürün sahipliği: etkilenmez. Site hiçbir ürün davranışına, kimlik doğrulamaya veya veriye sahip değildir.
- plan / entitlement: N/A.
- kullanım / kota: N/A.
- organizasyon yaşam döngüsü: N/A.
- secret / üretim güvenliği: repoda secret yoktur ve olmamalıdır. İletişim formu sunucuya veri göndermez; ziyaretçinin kendi e-posta veya WhatsApp uygulamasını açar. Site kişisel veri saklamaz.
- arka plan işleri / audit: N/A.
- dışa aktarma / saklama / silme: N/A.
- ölçek / altyapı: statik barındırma; ek altyapı yok.

## Kabul

Bu karar şu koşullar sağlandığında tamamlanmış sayılır:

1. `kyrox-web` `kyrox-studio` organizasyonu altında açılmıştır,
2. `kyrox-brand` içindeki `web-site/` klasörü geçmişiyle birlikte `kyrox-web`'e taşınmış, `kyrox-brand`'den kaldırılmıştır,
3. [REPOSITORY_STRATEGY.md](../REPOSITORY_STRATEGY.md), [DOCUMENT_GOVERNANCE.md](../DOCUMENT_GOVERNANCE.md) ve [STATUS.md](../STATUS.md) repoyu tanır,
4. site Cloudflare Pages üzerinden `kyrox.studio` adresinde yayındadır,
5. `sitemap.xml` Google Search Console ve Bing Webmaster Tools'a gönderilmiştir.

## Değerlendirilen seçenekler

- **Siteyi `kyrox-brand`'de bırakmak.** Reddedildi: ADR-0010 kapsamını aşar, marka varlıklarının geçmişini site değişiklikleriyle doldurur.
- **Siteyi `kyrox-platform`'a koymak.** Reddedildi: bu repo uygulama kodu barındırmaz ([AGENTS.md](../../AGENTS.md)).
- **Siteyi bir ürün reposuna (ör. `fair-crm`) koymak.** Reddedildi: site bir ürüne değil, stüdyonun tamamına aittir.

## Sonuçlar

### Olumlu

- site ve blog kendi yayın döngüsüne sahip olur; bir yazı eklemek tek dosyalık bir PR'dır,
- kurum bilgisi tek yerden (`site.json`) yönetilir; site, `llms.txt` ve schema.org bilgisi birbiriyle çelişmez,
- marka varlıkları reposu sade kalır.

### Olumsuz

- logo değişince `kyrox-web`'e de ayrı bir PR gerekir,
- bir repo daha bakım ister.

## İlgili

- [Repository strategy](../REPOSITORY_STRATEGY.md)
- [ADR-0010: Marka varlıkları reposu](0010-brand-repository.md)
- [Marka standardı](../../standards/brand/BRAND_STANDARD.md)
