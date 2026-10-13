# Fair Stand — FAZ 5–6 Roadmap

> **Tek kaynak:** Bu belge FAZ 5 ve FAZ 6'nın detaylı planıdır. FAZ 4 detayları ve üst seviye plan `fair-stand` deposundaki `ROADMAP_PHASE_4.md` ve `ROADMAP.md` içindedir (CI onları orada okur).

## Mimari sıra

1. **FAZ 4 — Modül reçetesi + parametrik/yapısal editör:** Her modül kendi fiziksel parçalarını ve Raw BOM'unu bilir; connection graph sahnedeki ilişkileri bilir.
2. **FAZ 5 — Final BOM / Assembly Normalization:** Modül Raw BOM'larını sahne bağlantılarına göre birleştirir, ortak parçaları düşer ve gerçek final malzeme listesini çıkarır.
3. **FAZ 6 — Maliyet / Fair CRM:** FAZ 5 Final BOM'unu katalog ve fiyat verisiyle maliyete dönüştürür.

---

# FAZ 5 — FINAL BOM / GERÇEK SAHNE MALZEME LİSTESİ

## Amaç

FAZ 4'te zaten kendi reçetesini bilen modülleri sahne seviyesinde birleştirip gerçek montaj sonucunu hesaplamak.

FAZ 5'in ana sorusu:

**"Bu sahnenin tamamını gerçekten kurmak için hangi fiziksel parçadan kaç tane gerekiyor?"**

FAZ 5'te fiyat hesabı yapılmaz.

## 5.1 — Raw BOM toplama

- [ ] Tüm aktif scene instance'larının FAZ 4 Raw BOM çıktıları toplanır.
- [ ] Her satır kaynak instance/recipe ile izlenebilir kalır.
- [ ] Gizli/silinmiş/aktif olmayan instance'ların dahil edilme kuralları açık tanımlanır.
- [ ] Aynı part ID farklı ölçülerdeyse ayrı tutulur.

## 5.2 — Connection Graph analizi

- [ ] FAZ 4'ün `INNER_CORNER`, `INLINE_JOIN`, anchor ilişkileri Final BOM girdisidir.
- [ ] Yalnız koordinat yakınlığı ortak parça düşmek için yeterli değildir.
- [ ] Gerçek üretim semantiğine göre shared upright/profile/connector kuralları tanımlanır.
- [ ] Köşe, inline, T-junction ve bağımsız uç gibi durumlar gerçek üretim verisiyle doğrulanır.

## 5.3 — Panel ve aparat seçiminin sahne bağlamında tamamlanması

- [ ] Modül Raw BOM'u bağlantıya göre varyant seçebiliyorsa connection graph doğru varyantı tetikler.
- [ ] Normal / iç-köşe panel ailesi seçimi gerçek bağlantı durumuna göre doğrulanır.
- [ ] Köşe, çiftli ve standart bağlantı aparatlarının sahne seviyesindeki nihai kullanımı hesaplanır.
- [ ] Başlangıç aparatı yalnız gerçek panel run başlangıcında sayılır.
- [ ] Nihai adet kuralları gerçek üretim Excel/verisiyle doğrulanmadan tahmin edilmez.

## 5.4 — Shared-Part / Assembly Normalization

Pipeline:

`Scene Instances -> Raw BOM -> Connection Analysis -> Shared-Part Deduction/Merge -> Dimension Normalization -> Final BOM`

- [ ] Ortak kullanılan dikme/profil/aparat yalnız bir kez sayılır.
- [ ] Paylaşım kuralı doğrulanmamış parçalar güvenli varsayımla ayrı sayılır.
- [ ] Aynı `partId + aynı ölçü` uygun olduğunda aggregate edilir.
- [ ] Farklı ölçüdeki aynı part ID yanlışlıkla merge edilmez.
- [ ] Final miktar negatif olamaz.
- [ ] Raw → Final farkı açıklanabilir olur; örn. `8 raw dikme - 3 shared = 5 final dikme`.

## 5.5 — Yüzey / m² miktarları

- [ ] Fiziksel panel/yüzey gerçek ölçüsünden `areaM2` üretilebilir.
- [ ] Baskı/görsel uygulanan yüz `printAreaM2` üretir.
- [ ] Boya/kaplama için ayrı miktar kategorileri desteklenebilir.
- [ ] Tek yüz / çift yüz ayrımı korunur.
- [ ] Cam, standart panel, özel kaplama gibi yüzey tipleri ayrıştırılır.
- [ ] Hesap bounding box yerine gerçek yüz kimliği kullanır.

## 5.6 — Gerçek Excel doğrulaması

- [ ] Elle çıkarılmış gerçek malzeme Excel'i üretim source-of-truth olarak kullanılır.
- [ ] Seçili gerçek proje otomatik Final BOM ile hesaplanır.
- [ ] Excel ile satır satır karşılaştırılır.
- [ ] Fark varsa Excel'i sisteme uydurmak yerine recipe/connection/normalization algoritması incelenir.
- [ ] Havrano gibi gerçek projelerde manuel köşe işaretlemesi olmadan sonuç üretilebilmelidir.

## 5.7 — Referans kabul senaryoları

- [ ] Tek 50/100/150/200 modül.
- [ ] Aynı doğrultuda iki modül birleşimi.
- [ ] İç köşe birleşimi.
- [ ] Birden fazla köşe içeren gerçek stand.
- [ ] `4 × 200 cm = 800 cm` zinciri.
- [ ] Bir bağlantı kaldırıldığında Final BOM'un deterministik değişmesi.

## FAZ 5 kapanış kriteri

- [ ] Sahne → Raw BOM → connection analysis → Final BOM zinciri deterministik.
- [ ] Gerçek Excel ile seçilmiş referans projeler doğrulanmış.
- [ ] Raw/Final traceability mevcut.
- [ ] Panel, dikme, profil, aparat ve yüzey miktarları güvenilir.
- [ ] `npm test` ve `npm run build` temiz.
- [ ] Fiyat hesabı henüz yapılmıyor.

---

# FAZ 6 — MALİYET / FAIR CRM ENTEGRASYONU

## Amaç

FAZ 5'in doğrulanmış Final BOM ve miktarlarını Fair CRM katalog/fiyat altyapısıyla eşleştirip proje maliyetini güvenilir şekilde hesaplamak.

## 6.1 — Fair CRM / Kyrox Core platform entegrasyonu

- [ ] Fair Stand içinde ikinci login/kullanıcı sistemi yapılmaz.
- [ ] Authentication/session kaynağı Kyrox Core / mevcut platform olur.
- [ ] `CustomModuleRepository` backend adapter'ı local adapter contract'ıyla uyumlu çalışır.
- [ ] Custom modül ownership backend tarafında doğrulanır.
- [ ] Project/revision kimliği entegrasyon boyunca korunur.

## 6.2 — Catalog / fiyat eşlemesi

- [ ] Her maliyetlenebilir `partId` Fair CRM catalog/external ID'ye eşlenir.
- [ ] `adet`, `m`, `m²`, `kg`, `set` gibi birimler ortak contract ile eşleşir.
- [ ] Fair CRM alış/maliyet fiyatı, satış/markup gerekirse, para birimi ve geçerlilik tarihinin sahibidir.
- [ ] Eksik catalog eşleşmesi `unmapped` olarak raporlanır.
- [ ] Eksik fiyat `0` kabul edilmez; `unpriced` olarak raporlanır.
- [ ] Hesap hangi catalog/version/fiyat snapshot'ıyla yapıldığını saklar.

## 6.3 — Hazır sahne objeleri

- [ ] Masa, sandalye, takım, bar taburesi, TV, depo içeriği, aydınlatma vb. hazır objeler catalog ID'ye bağlanır.
- [ ] Scene instance sayıları aggregate edilir.
- [ ] Aynı catalog ID tek ticari satırda toplanabilir.
- [ ] Custom varyasyon base catalog kimliğini miras alabilir veya override edebilir.

## 6.4 — Fire, işçilik ve ek maliyet

- [ ] Malzeme bazlı fire oranı.
- [ ] Minimum sipariş / yukarı yuvarlama kuralları.
- [ ] İşçilik `adet`, `m`, `m²`, saat veya recipe bazlı hesaplanabilir.
- [ ] Nakliye, kurulum, elektrik vb. proje seviyesinde ayrı tutulur.
- [ ] Otomatik ve manuel maliyet satırlarının kaynağı açık olur.

## 6.5 — Costing output

- [ ] Final BOM + hazır objeler + yüzey miktarları costing girdisidir.
- [ ] Her satırda kaynak, miktar, birim, catalog ID ve fiyat bilgisi gösterilir.
- [ ] Toplam proje maliyeti hesaplanır.
- [ ] Eksik fiyat ve validation sorunları ayrıca listelenir.
- [ ] Aynı proje state + aynı fiyat snapshot aynı maliyet sonucunu üretir.

## 6.6 — Revision / Audit

- [ ] Tasarım revizyonu ile BOM ve maliyet revizyonu ilişkilendirilir.
- [ ] Eski maliyet sonucu sessizce overwrite edilmez.
- [ ] Hangi tasarımın hangi fiyat tarihiyle hesaplandığı izlenebilir.
- [ ] Fair CRM aktarımı project/revision kimliği taşır.

## FAZ 6 kapanış kriteri

- [ ] Final BOM Fair CRM kataloglarına güvenilir eşleniyor.
- [ ] Eksik fiyat/catalog durumları açık raporlanıyor.
- [ ] Fire/işçilik/ek maliyet kuralları test edilmiş.
- [ ] Aynı snapshot deterministik costing sonucu üretiyor.
- [ ] Revision/audit izi korunuyor.
- [ ] Production ownership/auth entegrasyonu server-side doğrulanıyor.

---

# Faz sınırı özeti

- **FAZ 4:** Modül kendi fiziksel reçetesini ve Raw BOM'unu bilir; parametrik/custom yapı ve connection graph kurulur.
- **FAZ 5:** Tüm modüllerin Raw BOM'u sahne bağlantılarına göre normalize edilerek Final BOM çıkarılır.
- **FAZ 6:** Final BOM ve diğer ticari miktarlar Fair CRM fiyatlarıyla maliyete dönüşür.
