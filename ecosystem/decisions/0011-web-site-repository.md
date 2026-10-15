# ADR-0011: kyrox.studio web sitesi reposu (kyrox-web)

- **Durum:** Accepted
- **Tarih:** 2026-10-14 (öneri), 2026-10-15 (kabul; teknik tercih WordPress olarak güncellendi)
- **Karar verenler:** KYROX ekosistem sahipleri

## Bağlam

Kyrox Studio'nun web sitesi (kyrox.studio) hazırlandı. Site bir ana sayfa, bir blog ve arama motorları ile yapay zekâ asistanları için kimlik bilgilerinden (`sitemap.xml`, `robots.txt`, `llms.txt`, schema.org bilgisi) oluşuyor.

Site önce geçici olarak `kyrox-brand` reposunda hazırlandı. Bu yer kalıcı olamaz:

- [ADR-0010](0010-brand-repository.md), `kyrox-brand`'in kapsamını logo dosyaları, renk token'ları ve logoyu üreten betiklerle sınırlar. Web sitesi kodu ve blog içeriği bu kapsamın dışındadır.
- Site kendi yayın döngüsüne sahip; logo dosyalarıyla aynı repoda durursa marka varlıklarının geçmişi site değişiklikleriyle dolar.
- [REPOSITORY_STRATEGY](../REPOSITORY_STRATEGY.md) onaysız yeni repo açılmasını yasaklar; bu yüzden önce bu karar gerekiyor.

İlk taslak bağımlılıksız bir statik derleyiciyle yapıldı: blog yazıları Markdown dosyasıydı ve her metin değişikliği bir PR gerektiriyordu. Site sahibi içeriği (blog, bölüm metinleri, işler, iletişim bilgileri) kod yazmadan bir yönetim panelinden değiştirebilmek istiyor. Bu yüzden teknik tercih kabulden önce WordPress olarak güncellendi.

## Karar

`kyrox-studio/kyrox-web` reposu, kyrox.studio web sitesinin reposudur.

Kapsamı:

- sitenin özel WordPress teması (onaylı tasarımın birebir karşılığı): şablonlar, stiller, betikler, tema ayarları,
- temanın tanımladığı içerik yapıları (ör. "İşler" içerik türü) ve tema etkinleşince oluşan başlangıç içeriği (Ana sayfa, Blog sayfası, örnek yazı, işler kartları),
- sunucu kurulum dosyaları: WordPress ve MariaDB için Docker Compose tanımı, nginx site şablonu, kurulum betiği. **Secret içermez**; şifreler ve WordPress anahtarları yalnızca sunucudaki ayar dosyasında durur,
- sitede kullanılan statik dosyalar: logo ve favicon kopyaları, paylaşım görseli.

Bu repo şunlar **değildir**:

- içerik deposu. Blog yazıları, sayfa metinleri ve yüklenen görseller WordPress veritabanında ve yükleme klasöründe durur; panelden yönetilir,
- ekosistem dokümantasyonu. Ekosistem kuralları `kyrox-platform`'da kalır,
- marka kurallarının yazıldığı yer. Kurallar [standards/brand/BRAND_STANDARD.md](../../standards/brand/BRAND_STANDARD.md) dosyasındadır,
- logo kaynağı. Logo `kyrox-brand`'den kopyalanır ve burada elle düzenlenmez,
- ürün kodu. Fair CRM ve Fair Stand arayüzleri kendi repolarında kalır; site onlara yalnızca link verir (`fuar.kyrox.studio`).

## Teknik tercih

- **WordPress + özel tema.** Onaylı tasarım (koyu ve krem varyant) bir WordPress temasına taşınır. Panelden yönetilenler: blog (WordPress yazıları), hero ve bölüm metinleri, işler kartları (tür, durum, link, çizim seçimi, öne çıkan görsel), iletişim bilgileri, koyu/krem seçimi.
- **SEO ve yapay zekâ.** Tema meta ve Open Graph etiketlerini, JSON-LD bilgisini (`LocalBusiness`, `BlogPosting`), `robots.txt`'yi (yapay zekâ tarayıcılarına açık) ve `/llms.txt`'yi üretir; site haritası WordPress'in kendi site haritasıdır.
- **Barındırma: kendi sunucumuz.** WordPress ve MariaDB, Kyrox sunucusunda Docker ile `/opt/kyrox/kyrox-web` altında çalışır; yalnızca `127.0.0.1`'e bağlanır. nginx'e yalnızca `kyrox.studio` ve `www.kyrox.studio` için bir site bloğu eklenir, mevcut sitelere dokunulmaz. SSL mevcut yöntemle (certbot) alınır.
- **Kaynak sınırı.** Sunucuda kullanılabilir bellek az olduğu için WordPress ve MariaDB küçük bellek ayarlarıyla çalışır.
- **Alan adı.** `kyrox.studio` ve `www` A kayıtları sunucuya yönlendirilir. E-posta (MX) kayıtları değişmez. `fuar.kyrox.studio` ve diğer alt alan adları bu karardan etkilenmez.
- **Mevcut statik derleyici.** Tema tamamlanana kadar tasarım kaynağı olarak repoda kalır; tema yayına girince kaldırılır.

## Teslim profili

Feature profili: `maintenance` / web sitesi.

SaaS etki sınıflandırması:

- organizasyona ait veri / tenant izolasyonu: N/A. Site Kyrox ürünlerinin müşteri verisine erişmez; kendi veritabanı ürün veritabanlarından ayrıdır.
- yetki kapsamı: WordPress yönetici hesapları yalnızca site içeriği içindir; ziyaretçi kaydı kapalıdır. Kyrox Core kimliğiyle bağlantısı yoktur.
- Core ve ürün sahipliği: etkilenmez. Site hiçbir ürün davranışına, kimlik doğrulamaya veya ürün verisine sahip değildir.
- plan / entitlement: N/A.
- kullanım / kota: N/A.
- organizasyon yaşam döngüsü: N/A.
- secret / üretim güvenliği: repoda secret yoktur ve olmamalıdır. Yönetim paneli güçlü şifre ve giriş denemesi sınırıyla korunur; WordPress ve eklenti güvenlik güncellemeleri takip edilir. İletişim bölümü sunucuya veri göndermez; ziyaretçinin kendi e-posta veya WhatsApp uygulamasını açar. Site ziyaretçi kişisel verisi saklamaz.
- arka plan işleri / audit: N/A.
- dışa aktarma / saklama / silme: WordPress veritabanı ve yükleme klasörü sunucunun gecelik yedeğine (`kyrox-backup`) eklenir.
- ölçek / altyapı: tek sunucuda Docker; ek dış hizmet yok.

## Kabul

Bu karar şu koşullar sağlandığında tamamlanmış sayılır:

1. `kyrox-web` `kyrox-studio` organizasyonu altında açılmıştır,
2. site dosyaları `kyrox-brand`'den taşınmış, `kyrox-brand`'den kaldırılmıştır,
3. [REPOSITORY_STRATEGY.md](../REPOSITORY_STRATEGY.md), [DOCUMENT_GOVERNANCE.md](../DOCUMENT_GOVERNANCE.md) ve [STATUS.md](../STATUS.md) repoyu tanır,
4. özel tema `kyrox-web`'dedir ve site Kyrox sunucusunda WordPress ile `kyrox.studio` adresinde SSL ile yayındadır,
5. WordPress veritabanı ve yükleme klasörü gecelik yedeğe dahildir,
6. site haritası Google Search Console ve Bing Webmaster Tools'a gönderilmiştir.

## Değerlendirilen seçenekler

- **Bağımlılıksız statik derleyici + Cloudflare Pages.** İlk taslak buydu. Reddedildi: her içerik değişikliği kod ve PR gerektirir; site sahibi panelden yönetim istiyor.
- **Astro gibi bir statik site çatısı.** Reddedildi: aynı panel eksikliği; ayrı bir headless CMS eklemek gerekirdi.
- **Siteyi `kyrox-brand`'de bırakmak.** Reddedildi: ADR-0010 kapsamını aşar, marka varlıklarının geçmişini site değişiklikleriyle doldurur.
- **Siteyi `kyrox-platform`'a koymak.** Reddedildi: bu repo uygulama kodu barındırmaz ([AGENTS.md](../../AGENTS.md)).
- **Siteyi bir ürün reposuna (ör. `kyrox-fair-crm`) koymak.** Reddedildi: site bir ürüne değil, stüdyonun tamamına aittir.

## Sonuçlar

### Olumlu

- içerik (blog, bölüm metinleri, işler, iletişim) kod yazmadan panelden yönetilir,
- tema kodu ve sunucu kurulumu repoda sürümlenir; içerik veritabanında kalır,
- marka varlıkları reposu sade kalır.

### Olumsuz

- PHP ve MariaDB bakımı ile WordPress güvenlik güncellemeleri gerekir,
- sitenin veritabanı ve yüklemeleri yedeklenmesi gereken yeni veridir,
- sınırlı bellekli sunucuya bir veritabanı daha eklenir,
- logo değişince `kyrox-web`'e de ayrı bir PR gerekir.

## İlgili

- [Repository strategy](../REPOSITORY_STRATEGY.md)
- [ADR-0010: Marka varlıkları reposu](0010-brand-repository.md)
- [Marka standardı](../../standards/brand/BRAND_STANDARD.md)
