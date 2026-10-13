# Fair Stand — Gelecek Ürün Gereksinimleri

> Bu belge, mevcut README'nin görevi olmayan fakat **kaybolmaması gereken gelecek ürün fikirlerini ve veri ihtiyaçlarını** toplar.
>
> Bu maddelerin burada bulunması tamamlandıkları anlamına gelmez. Aktif geliştirme sırası `fair-stand` deposundaki `ROADMAP.md` ve `ROADMAP_PHASE_4.md` ile bu ağaçtaki [ROADMAP_PHASE_5_6.md](ROADMAP_PHASE_5_6.md) tarafından belirlenir.

## Kaynak

`fair-stand` deposunda PR #6 öncesi eski `README.md` snapshot'ı: `03a7bade2ed8542d8c2d45766e5ecaffa5b196ea`.

## Gelecek çıktılar

Eski README'de tanımlanmış ve korunması gereken ürün çıktıları:

- Yaklaşık fiyat hesabı.
- Detaylı satış teklifi.
- PDF teklif çıktısı.
- Montaj sırası.
- Bağlantı elemanı listesi.
- Depodan ürün toplama listesi.
- Paketleme listesi.
- Stok kontrolü.
- Müşteri logosu ve baskı dosyaları.
- Numaralandırılmış montaj şeması.
- Kullanıcı ve proje yönetimi.
- Proje paylaşma/onaylama akışı.

### Mevcut roadmap ile ilişkisi

- Fiyat/maliyet ve ticari katalog eşlemesi: FAZ 6 ile ilişkili.
- Bağlantı elemanı ve gerçek malzeme listesi: FAZ 4–5 recipe / connection graph / Final BOM ile ilişkili.
- Kullanıcı/proje ownership ve revision/audit: FAZ 6 entegrasyon planıyla kısmen ilişkili.
- PDF teklif, montaj sırası, depo toplama, paketleme, stok kontrolü, baskı dosyaları, numaralandırılmış montaj şeması ve proje paylaşma/onaylama: mevcut phase roadmap'lerde açık ve eksiksiz birer teslimat olarak tanımlı değildir; bu nedenle burada korunur ve ileride fazlandırılmalıdır.

## Toplanması gereken teknik / ticari veriler

Her gerçek modül/parça için ihtiyaç duyulabilecek veri seti:

- Ad ve ürün kodu.
- Gerçek ölçüler.
- Ağırlık.
- Fotoğraf.
- 3D model.
- Bağlantı noktaları / anchor bilgisi.
- Uyumlu aksesuarlar.
- Gerekli montaj parçaları / recipe.
- Maksimum taşıma kapasitesi.
- Maliyet ve satış fiyatı.
- Stok bilgisi.

Bu alanların tamamının tek dosya/modelde tutulması zorunlu değildir. Güncel mimaride catalog, behavior, recipe, renderer ve ileride Fair CRM sorumlulukları ayrıdır.

## Saha tarafından kesinleştirilmesi gereken bilgiler

Aşağıdaki konular ürün/üretim/montaj verisiyle doğrulanmalıdır:

- Maksimum düz duvar uzunluğu.
- Destek gereken aralık.
- Maksimum raf sayısı.
- Rafların izin verilen yükseklikleri.
- Raf taşıma kapasitesi.
- Kasa eklenebilen panel/modül tipleri.
- Köşe birleşim kuralları.
- Kapı ve depo ölçüleri.
- Stand yüksekliği seçenekleri.
- Baza ve zemin seçenekleri.

Doğrulanmamış sayısal tahminler [LEGACY_TRASH.md](../../archive/fair-stand/LEGACY_TRASH.md) içinde korunur; doğrulandıktan sonra canonical rule/recipe/roadmap dokümanına alınır.

## Ürün vizyonundan korunacak esas fikir

Fair Stand'ın uzun vadeli değeri yalnız 3D görselleştirme değildir. Hedef zincir:

`tasarım -> üretilebilir yapı -> fiziksel parça/BOM -> montaj/operasyon çıktıları -> maliyet/teklif -> proje/revision izlenebilirliği`

Bu vizyon güncel mimarinin `catalog + behavior + recipe + connection graph + Final BOM + CRM/costing` ayrımıyla geliştirilmelidir.
