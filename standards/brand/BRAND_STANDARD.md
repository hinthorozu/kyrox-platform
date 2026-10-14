# Kyrox Studio Marka Standardı

Kyrox Studio logosunun, renklerinin ve yazımının tek kural kaynağı. Fair CRM, Fair Stand, kyrox.studio web sitesi, sunumlar, teklifler ve sosyal medya bu kurallara uyar.

Logo dosyaları ve renk tanımları [kyrox-studio/kyrox-brand](https://github.com/kyrox-studio/kyrox-brand) reposundadır ([ADR-0010](../../ecosystem/decisions/0010-brand-repository.md)). Bu doküman kuralları tanımlar; dosyaları kopyalamaz.

## 1. Tek logo

Kyrox Studio'nun tek logosu düz, vektör logodur. Metal, deri ve ahşaptan oluşan K sembolü ile KYROX yazısı ve altındaki `.studio`'dan oluşur.

- Gölgeli, dokulu, parlak veya 3D logo versiyonları **kullanılmaz**. Bunlar 2026-10-14'te kaldırıldı.
- Logoya slogan eklenmez. Slogan ayrı bir metin olarak kullanılır (bölüm 5).

## 2. Versiyonlar

| Versiyon | Dosya (`kyrox-brand/logo/`) | Nerede |
| --- | --- | --- |
| Ana logo, renkli | `svg/kyrox-logo-renkli.svg` | Açık zemin: web, sunum, teklif, e-posta imzası, uygulama |
| Ana logo, koyu zemin | `svg/kyrox-logo-renkli-koyu-zemin.svg` | Siyah veya koyu zemin |
| Ana logo, siyah / beyaz | `svg/kyrox-logo-siyah.svg`, `svg/kyrox-logo-beyaz.svg` | Tek renk baskı, fotoğraf üzeri, lazer kesim, ahşaba yakma, folyo |
| Sembol | `svg/kyrox-ikon-*.svg` | Dar alan: uygulama ikonu, damga, gravür |
| Yazı | `svg/kyrox-yazi-*.svg` | Sembolün sığmadığı dar yatay alan |
| Profil görseli | `png/kyrox-profil-siyah-1080.png` | Instagram, LinkedIn ve diğer tüm hesaplar. Siyah zemin varsayılandır |
| Favicon | `favicon.ico`, `svg/favicon.svg`, `png/apple-touch-icon-180.png` | Web siteleri ve uygulamalar |

Kaynak dosya SVG'dir. PNG yalnızca SVG kullanılamayan yerlerde kullanılır.

## 3. Kullanım kuralları

- **Koruma alanı:** logonun her yanında en az KYROX harf yüksekliğinin yarısı kadar boşluk kalır. Bu alana yazı, çizgi veya başka logo girmez.
- **En küçük boyut:** ana logo ekranda 140 px, baskıda 35 mm genişlik. Sembol ekranda 16 px, baskıda 8 mm. Bundan küçük alanda yalnızca sembol kullanılır.
- **Değiştirilmez:** logo esnetilmez, döndürülmez, eğilmez. Parçaların renkleri ve yerleri değiştirilmez. Düz logoya gölge, parlama veya degrade eklenmez.
- **Zemin:** renkli logo karışık bir fotoğrafın üzerine konmaz; fotoğraf üzerinde beyaz versiyon kullanılır.

## 4. Yazım

- Marka adı metin içinde **Kyrox Studio** olarak yazılır.
- Logodaki `.studio` her zaman **küçük harfle** yazılır. Domaini (`kyrox.studio`) temsil eder; büyük harfe veya `.STUDİO` yazımına çevrilmez.
- Domain ve e-posta adresleri küçük harfle yazılır: `kyrox.studio`, `hello@kyrox.studio`.
- Sosyal medya kullanıcı adı her kanalda aynıdır: `@kyrox.studio`.

## 5. Slogan

- Ana slogan: **Precision meets Craft**.
- Felsefe cümlesi: **Limited projects. Lasting impact.** Web sitesinde ve LinkedIn'de kullanılır. Eski `LAST IMPACT` yazımı kullanılmaz.
- Slogan logonun bir parçası değildir; logonun yanına veya altına ayrı metin olarak konur.

## 6. Renkler

Palet üç ana renge dayanır: **mürekkep, kağıt, bakır**. Değerler `kyrox-brand/tokens/colors.css` ve `tokens.json` dosyalarındadır; projeler değerleri elle yazmak yerine bu dosyaları kullanır.

### 6.1 Ana renkler

| Ad | Token | Değer | Kullanım |
| --- | --- | --- | --- |
| Mürekkep | `--kyrox-ink` | `#0B0B0B` | Başlık, metin, koyu zemin |
| Kağıt | `--kyrox-paper` | `#F5F3EF` | Ana zemin |
| Beyaz | `--kyrox-white` | `#FFFFFF` | Kart, form, tablo |

### 6.2 Bakır, üç ton

Logodaki bakır açık zeminde yazı için fazla açıktır (kağıtta kontrast 3,06; okunabilir metin için en az 4,5 gerekir). Bu yüzden bakır üç tonda kullanılır:

| Ad | Token | Değer | Kullanım | Kontrast |
| --- | --- | --- | --- | --- |
| Bakır | `--kyrox-copper` | `#C47A3A` | Çizgi, ikon, grafik, 24 px ve üstü başlık | Kağıtta 3,06. Gövde metni ve buton zemini olarak **kullanılmaz** |
| Bakır koyu | `--kyrox-copper-text` | `#99602D` | Link, buton zemini, vurgulu metin | Kağıtta 4,66; üstünde beyaz yazı 5,17 |
| Bakır açık | `--kyrox-copper-on-dark` | `#CD8D56` | Koyu zeminde link ve vurgu | Mürekkep üstünde 7,07 |

### 6.3 Sıcak griler

| Ad | Token | Değer | Kullanım | Kağıtta kontrast |
| --- | --- | --- | --- | --- |
| Gri 900 | `--kyrox-gray-900` | `#2A2724` | Gövde metni | 13,4 |
| Gri 600 | `--kyrox-gray-600` | `#6B655D` | İkincil metin, açıklama | 5,2 |
| Gri 400 | `--kyrox-gray-400` | `#A39C93` | Pasif öğe, ikon. **Metin için kullanılmaz** | 2,45 |
| Gri 200 | `--kyrox-gray-200` | `#DEDAD4` | Çizgi, kenarlık | — |
| Gri 100 | `--kyrox-gray-100` | `#EBE8E3` | İkincil yüzey | — |
| Gece | `--kyrox-night` | `#1A1816` | Koyu bölüm zemini | — |

### 6.4 Logo malzeme renkleri

Çelik, ahşap ve deri yalnızca logoda ve malzeme görsellerinde kullanılır; arayüz rengi değildir.

| Ad | Token | Değer |
| --- | --- | --- |
| Çelik | `--kyrox-steel` | `#B4B7BB` |
| Çelik, koyu zemin | `--kyrox-steel-on-dark` | `#C9CCD0` |
| Ahşap | `--kyrox-wood` | `#A2652C` |
| Deri | `--kyrox-leather` | `#7B3B1D` |

### 6.5 Kullanım kuralları

- Oran: kağıt ve beyaz yaklaşık %60, mürekkep %30, bakır %10. Bakır az kullanıldıkça değerli kalır: sayfa başına bir vurgu, bir buton türü.
- Gövde metni en az 4,5, 24 px ve üstü başlık en az 3 kontrast taşır (WCAG AA).
- Koyu zeminde bakır vurgu her zaman `--kyrox-copper-on-dark` ile yapılır.

## 7. Yazı tipleri

| Rol | Font | Ağırlık | Nerede |
| --- | --- | --- | --- |
| Metin ve arayüz | **Inter** | 400, 500, 600, 700 | Her yerde: web, ürünler, sunum, teklif, sosyal medya metni |
| Başlık | **Archivo** | 800, genişlik `font-stretch: 112%`, büyük harf | Web sitesi, sunum ve sosyal medyada büyük başlıklar |

- Logodaki `.studio` Inter Medium'dur. Fair CRM ve Fair Stand arayüzleri Inter kullanır; ürün arayüzlerinde başlık fontu kullanılmaz.
- Her iki font da Google Fonts'tan ücretsizdir ve Türkçe karakterleri tam destekler.
- Archivo yalnızca 22 px ve üstünde kullanılır. Gövde metni, buton, form ve tabloda kullanılmaz.

### 7.1 Boyut ölçeği

| Seviye | Boyut / ağırlık | Not |
| --- | --- | --- |
| Başlık 1 | 48 px / Archivo 800 | Sitede ana başlık; ürünlerde Inter 800 |
| Başlık 2 | 32 px / 700 | |
| Başlık 3 | 22 px / 600 | |
| Gövde | 16 px / 400 | Satır aralığı 1,6; satır uzunluğu en fazla ~70 karakter |
| Açıklama | 13 px / 500 | Gri 600 |
| Üst başlık | 12 px / 600 | Büyük harf, harf aralığı 0,08 em, bakır koyu |

### 7.2 Türkçe büyük harf

CSS `text-transform: uppercase` sayfanın dili Türkçe işaretlenmezse "i" harfini noktasız "I" yapar ("ATÖLYEMİZDEN" yerine "ATÖLYEMIZDEN"). Büyük harfli başlık kullanan her sayfa `lang="tr"` taşır; İngilizce metinler kendi öğesinde `lang="en"` ile işaretlenir.

## 8. Ses tonu

Kyrox bir ustanın konuştuğu gibi konuşur: az, net, ölçüyle. Reklam dili değil, atölye dili.

| İlke | Anlamı |
| --- | --- |
| Net | Bir cümle, bir fikir. Sıfat yerine ölçü, malzeme ve tarih. |
| Ölçülü | Abartı yok. "En iyi", "muhteşem", "eşsiz" kullanılmaz; iş kendini gösterir. |
| Malzemeden konuşur | Meşe, alüminyum profil, deri, dijital baskı. Müşteri neyle çalışıldığını bilir. |
| Az ama derin | "Limited projects. Lasting impact." Az iş alınır, her biri sonuna kadar götürülür. |

Örnekler (sayılar örnektir):

| Yerine | Böyle |
| --- | --- |
| Muhteşem fuar standlarımızla markanızı zirveye taşıyoruz! | 48 m² ada stand. Meşe kaplama, 3 metre ışıklı duvar. Tasarımdan kuruluma 21 gün. |
| Profesyonel ekibimiz her türlü ihtiyacınıza çözüm sunar. | Çizen, kesen ve kuran aynı ekip. Fuar sabahı sürpriz çıkmaz. |
| Hemen arayın, kaçırılmayacak fırsatlar sizi bekliyor! | Bu yıl 12 proje alıyoruz. Fuar tarihinizi ve metrekarenizi yazın, iki gün içinde dönelim. |

- Ana dil Türkçedir. İngilizce yalnızca slogan ve uluslararası fuar işlerinde kullanılır.
- Hitap "siz"dir: samimi, ama resmi olmadan değil.
- Ünlem işareti ve emoji kullanılmaz.

## 9. Ürünlerle ilişki

- Ürünler logoyu `kyrox-brand`'den kopyalar. Ürün reposundaki logo dosyası elle düzenlenmez; logo değişirse önce `kyrox-brand` güncellenir, sonra ürünler.
- Ürün arayüzünün kendi renk sistemi (birincil renk, durum renkleri, yüzeyler) ürüne aittir ve [UI Foundation Standard](../ui/UI_FOUNDATION_STANDARD.md) ile ürünün UI standardına uyar. Bu doküman logo, marka renkleri ve yazı tiplerini tanımlar; ürün arayüz renklerini bağlamaz. Ürünler marka renklerine geçmeye karar verirse bakır tonları 6.2 kurallarıyla kullanılır.

## İlgili

- [ADR-0010: Marka varlıkları reposu](../../ecosystem/decisions/0010-brand-repository.md)
- [Logo ailesi sayfası](https://github.com/kyrox-studio/kyrox-brand/blob/main/kilavuz/logo-ailesi.html) (tüm versiyonların görsel örneği)
- [UI Foundation Standard](../ui/UI_FOUNDATION_STANDARD.md)
