# Fair Stand — Çöp Kutusu / Legacy Documentation

> Bu dosya **silme alanı değildir**. Güncel sistemle çelişen, artık geçerli olmayan veya doğrulanmadan uygulanmaması gereken eski dokümantasyon burada **kayıpsız** tutulur.
>
> Buraya taşınan bir fikir Git geçmişine terk edilmiş sayılmaz. Yeniden doğrulanırsa uygun canonical dokümana geri alınabilir.

## Kaynak: PR #6 öncesi eski `README.md`

Kaynak snapshot: `03a7bade2ed8542d8c2d45766e5ecaffa5b196ea`

### Eski / artık canonical olmayan ürün ve mimari varsayımları

- İlk sürümde yalnız mevcut Maxima stand modüllerinin esas alınacağı ve özel ahşap panel sistemi geliştirilmeyeceği varsayımı.
- 300 cm duvarın `150 + 150`, `200 + 100`, `100 + 100 + 100` gibi kombinasyonlarla çözülmesi ve kullanıcının alternatif kombinasyon seçmesi yaklaşımı. Bu fikir tarihsel ürün tasarımı olarak korunur; güncel placement/behavior contract'ının yerine geçmez.
- Her modül için `ağırlık`, `bağlantı noktaları`, `uyumlu/yasak kombinasyonlar`, `maksimum raf`, `maliyet`, `satış fiyatı`, `stok` alanlarının tek katalog modelinde tutulması yönündeki eski taslak. Güncel sistemde sorumluluklar catalog / behavior / recipe / ileride CRM katmanlarına ayrılmıştır.
- Kullanıcının teknik panel yerleşimi çizmek yerine yalnız ölçü, stand tipi ve ihtiyacını seçmesi; sistemin tüm standı otomatik kurması şeklindeki ilk ürün akışı. Otomatik üretim fikri değerlidir ancak güncel editörün manuel placement yeteneklerini geçersiz kılan zorunlu bir kural değildir.
- Three.js için eski genel yetenek/açıklama metni ve `Three.js kullanılabilir` ifadesi. Three.js artık olasılık değil mevcut renderer altyapısıdır.
- `Her bölüm ayrı 3D parça veya ayrı malzeme yüzeyi olarak tanımlanır` şeklindeki eski implementation varsayımı. Güncel renderer/state contract'ına source-of-truth değildir.

### Doğrulanmamış saha kuralları — KODLANMAMALI

Eski README bu maddeleri zaten taslak/doğrulanması gereken olarak işaretliyordu. Kayıp olmaması için burada korunuyor:

- Bir panelde en fazla 3 sıra raf olabilir.
- Belirli bir uzunluktan sonra düz duvara izin verilmemelidir.
- Yaklaşık 4 metreden sonra destek, dönüş veya ilave dikme gerekebilir.
- 5–6 metrelik kesintisiz duvarlarda baza, destek veya kırılım zorunlu olabilir.
- Raflar yalnızca belirli sabit yükseklik noktalarına takılabilir.
- Bazı panel kombinasyonları statik veya estetik nedenlerle yasaklanabilir.

Bu değerler üretim/montaj verisiyle doğrulanmadan runtime kuralı haline getirilmez.

### Eski MVP kapsamı / tarihsel plan

- Stand tipleri: düz sırt duvar, L stand, U stand.
- İlk modüller: 50/100/150/200 panel, tek standart yükseklik, boş panel, raflı panel, kasalı panel.
- İlk fonksiyonlar: alan ölçüsü, stand tipi, otomatik panel dizilimi, alternatif kombinasyonlar, panel seçme, raf sayısı, basit renk, gerçek zamanlı 3D, otomatik modül/aksesuar listesi, tasarım kaydetme.
- `İlk sürüm çalışmadan depo, lightbox, gelişmiş baskı, CNC veya kapsamlı fiyatlandırmaya geçilmemelidir` şeklindeki eski sıra kuralı. Repo bu aşamayı geçtiği için artık aktif plan değildir.

### Eski önerilen klasör mimarisi

```text
fair-stand/
├── app/
├── components/
├── configurator/
├── rules/
├── catalog/
├── models/
├── materials/
├── pricing/
├── projects/
└── docs/
```

Bu yapı uygulanmış repository yapısı değildir; tarihsel mimari öneri olarak korunur.

### Eski uygulama sırası

1. Maxima modül envanterini çıkar.
2. Modüllerin gerçek ölçülerini ve kodlarını kaydet.
3. Bağlantı, raf ve duvar kurallarını yazılı hale getir.
4. Modüllerin basit GLB/GLTF modellerini hazırla.
5. Tek bir düz duvar oluşturma prototipi geliştir.
6. 50–200 cm modüllerle otomatik uzunluk çözümünü geliştir.
7. Alternatif panel kombinasyonlarını göster.
8. Panel ve panel bölümü renk değiştirmeyi çalıştır.
9. Raf ekleme ve raf sayısı kurallarını uygula.
10. L stand oluşturmayı ekle.
11. U stand oluşturmayı ekle.
12. Geçersiz yapı kontrollerini ekle.
13. Otomatik parça listesini oluştur.
14. Fiyat ve teklif altyapısını ekle.
15. Proje kaydetme ve paylaşma akışını ekle.
16. Son aşamada arayüzü ve görsel kaliteyi geliştir.

Bu liste tarihsel sıradır; güncel aktif plan `fair-stand` deposundaki `ROADMAP.md` / `ROADMAP_PHASE_4.md` ve `projects/fair-stand/ROADMAP_PHASE_5_6.md`'dir.

### Eski ilk somut görev

> 50, 100, 150 ve 200 cm Maxima modüllerinin listesini, gerçek ölçülerini, bağlantı noktalarını ve hangi aksesuarlarla kullanılabildiğini çıkarmak.

Bu görev tarihsel başlangıç checkpoint'i olarak korunur; güncel sprint değildir.

---

## Dokümantasyon kuralı

Bundan sonra bir doküman sadeleştirilirken:

1. Güncel ve doğru bilgi canonical dokümanda tutulur.
2. Gelecek planı ilgili roadmap'e taşınır.
3. Tarihsel fakat değerli bilgi history/legacy alanında korunur.
4. Güncel sistemle çelişen veya doğrulanmamış bilgi bu dosyaya taşınır.
5. İçerik, yalnız 'eski' olduğu gerekçesiyle sessizce silinmez.
