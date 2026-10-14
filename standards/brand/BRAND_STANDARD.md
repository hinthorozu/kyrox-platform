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

Logo renkleri sabittir. Değerler `kyrox-brand/tokens/colors.css` ve `tokens.json` dosyalarındadır; projeler değerleri elle yazmak yerine bu dosyaları kullanır.

| Ad | Token | Değer | Kullanım |
| --- | --- | --- | --- |
| Çelik | `--kyrox-steel` | `#B4B7BB` | Logo, açık zemin |
| Çelik, koyu zemin | `--kyrox-steel-on-dark` | `#C9CCD0` | Logo, koyu zemin |
| Ahşap | `--kyrox-wood` | `#A2652C` | Logo |
| Deri | `--kyrox-leather` | `#7B3B1D` | Logo |
| Mürekkep | `--kyrox-ink` | `#0B0B0B` | Yazı, koyu zemin |
| Kağıt | `--kyrox-paper` | `#F5F3EF` | Açık zemin |
| Bakır | `--kyrox-copper` | `#C47A3A` | Marka vurgu rengi |

Tam marka paleti, fontlar ve ses tonu henüz tanımlanmadı. Tanımlandığında bu dokümana eklenir.

## 7. Ürünlerle ilişki

- Ürünler logoyu `kyrox-brand`'den kopyalar. Ürün reposundaki logo dosyası elle düzenlenmez; logo değişirse önce `kyrox-brand` güncellenir, sonra ürünler.
- Ürün arayüzünün kendi renk sistemi (birincil renk, durum renkleri, yüzeyler) ürüne aittir ve [UI Foundation Standard](../ui/UI_FOUNDATION_STANDARD.md) ile ürünün UI standardına uyar. Bu doküman yalnızca logo ve marka renklerini tanımlar; ürün arayüz renklerini bağlamaz.

## İlgili

- [ADR-0010: Marka varlıkları reposu](../../ecosystem/decisions/0010-brand-repository.md)
- [Logo ailesi sayfası](https://github.com/kyrox-studio/kyrox-brand/blob/main/kilavuz/logo-ailesi.html) (tüm versiyonların görsel örneği)
- [UI Foundation Standard](../ui/UI_FOUNDATION_STANDARD.md)
