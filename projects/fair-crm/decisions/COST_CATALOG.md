# Maliyet Kataloğu — Ürün Kararı

**Durum:** Tasarım kararı / henüz implement edilmedi  
**Tarih:** 2026-08-17

## Amaç

Teklif hazırlanmadan önce kullanılacak ürün ve hizmetlerin standart maliyet bilgilerini organizasyon bazında tanımlamak.

Örnek:

- Ürün: `Minyon Sandalye Takımı`
- Birim: `Adet`
- Birim fiyat: `1.500 TL`
- Maliyet hesabında miktar `4` girildiğinde sonuç otomatik olarak `4 × 1.500 = 6.000 TL` olur.

Bu doküman yalnızca şu an üzerinde anlaşılmış **Maliyet Kataloğu** kapsamını kaydeder. Teklif maliyet hesabı ve çizim sistemi entegrasyonu sonraki fazlardır.

## Menü ve UI

- Kullanıcıya görünen menü adı: **Maliyet Kataloğu**
- Yerleşim: **Yönetim / Admin** alanı altında.
- Ana sol menüde bağımsız günlük operasyon modülü olarak konumlandırılmayacak.
- Sayfa tek ekran olacaktır.
- Üst bölüm: **Kategoriler Tablosu**
- Alt bölüm: **Ürünler Tablosu**
- Her iki tablo, form ve CRUD akışı mevcut Fair CRM **UI standartlarına** uygun yapılacaktır; yeni ve bağımsız bir UI paterni üretilmeyecektir.

## Yetkilendirme

Permission scope: **ORGANIZATION**.

- Organizasyon kullanıcıları rol/permission kurallarına göre erişir.
- Super Admin mevcut merkezi Super Admin bypass davranışıyla tam erişebilir.
- Kategori ve ürünler için CRUD izinleri ayrı tutulacaktır.

Planlanan permission kodları:

```text
fair_crm.cost_catalog.categories.read
fair_crm.cost_catalog.categories.create
fair_crm.cost_catalog.categories.update
fair_crm.cost_catalog.categories.delete

fair_crm.cost_catalog.products.read
fair_crm.cost_catalog.products.create
fair_crm.cost_catalog.products.update
fair_crm.cost_catalog.products.delete
```

Bu permission'ların tamamı `permission_scope = organization` olacaktır.

## Kategoriler

Kategoriler organizasyon tarafından CRUD olarak yönetilir.

Örnekler:

- Mobilya
- Elektrik
- Baskı
- Nakliye
- İşçilik

Kategori listesi sistem tarafından sabitlenmeyecek; organizasyon kendi kategorilerini ekleyip yönetecektir.

## Ürün / Hizmet Kaydı

Her katalog kaleminde en az şu bilgiler bulunacaktır:

```text
Kategori
Ürün / Hizmet Adı
Slug
Birim
Birim Fiyat
Para Birimi
```

### Slug

Her ürün/hizmet kaydının bir `slug` alanı olacaktır.

Slug yalnızca URL amacıyla düşünülmemektedir. Gelecekte Fair Stand çizim/konfigüratör sistemi ile Maliyet Kataloğu arasında ortak eşleştirme anahtarı olarak kullanılacaktır.

Örnek:

```text
Kategori: Mobilya
Ürün: Minyon Sandalye Takımı
Slug: minyon-sandalye-takimi
Birim: Adet
Birim Fiyat: 1500
Para Birimi: TL
```

Gelecekte çizim sistemindeki bir modülün slug değeri ile katalog ürününün slug değeri eşleştiğinde, çizimde kullanılan adet/metraj üzerinden maliyet otomatik üretilebilecektir.

**Not:** Fair Stand entegrasyonu bu fazın kapsamında değildir.

## Birimler

Ürün/hizmet oluşturulurken birim dropdown üzerinden seçilecektir.

İlk konuşulan birim örnekleri:

- Adet
- Kg
- m²
- Metre
- Gün
- Saat

Gerekirse liste daha sonra genişletilebilir.

## Para Birimi ve Kur

İlk kapsamda en az:

- TL
- USD

para birimleri desteklenecektir.

TL fiyat doğrudan kullanılacaktır.

USD fiyat girildiğinde sistem **güncel kuru çekip TL karşılığını kullanıcıya gösterecektir**.

Örnek:

```text
Birim fiyat: 250 USD
Güncel kur: <çekilen kur>
TL karşılığı: 250 × kur
```

Maliyet hesabı aşamasında kullanılan kurun değeri ve tarihi saklanmalıdır; böylece eski bir maliyet hesabının hangi kurla üretildiği sonradan izlenebilir.

Kur sağlayıcısı / teknik entegrasyon yöntemi henüz kararlaştırılmamıştır.

## Sonraki Fazlar — Şimdilik Yapılmayacak

### 1. Maliyet Hesabı

Teklif öncesinde katalogdan ürün/hizmet seçilip miktar girilecek ve toplam maliyet otomatik hesaplanacaktır.

Örnek:

```text
Minyon Sandalye Takımı
4 Adet × 1.500 TL = 6.000 TL
```

### 2. Teklif Entegrasyonu

Maliyet hesabı daha sonra mevcut teklif akışına bağlanacaktır. Bu karar dokümanı teklif modülünde yapılacak değişikliği henüz tanımlamaz.

### 3. Fair Stand Entegrasyonu

`fairstand.umaay.com` çizim/konfigüratör sistemindeki modüller daha sonra slug üzerinden Maliyet Kataloğu ürünleriyle eşleştirilecektir.

Hedef gelecek akış:

```text
Fair Stand modül slug
        ↕
Maliyet Kataloğu ürün slug
        ↓
Çizimdeki adet / metraj
        ↓
Otomatik maliyet
```

Bu entegrasyon **şimdi yapılmayacaktır**.

## Şu Anki Karar Özeti

1. Özelliğin adı **Maliyet Kataloğu**.
2. Yönetim/Admin altında yer alacak.
3. Sayfada üstte Kategoriler, altında Ürünler tablosu olacak.
4. Kategori ve ürünler tam CRUD olacak.
5. Permission scope `ORGANIZATION`; Super Admin tam erişebilecek.
6. Ürünlerde kategori, ad, slug, birim, birim fiyat ve para birimi tutulacak.
7. Birim dropdown olacak.
8. TL ve USD desteklenecek; USD için güncel kur ve TL karşılığı gösterilecek.
9. Slug gelecekte Fair Stand çizim sistemi entegrasyonunda ortak eşleştirme anahtarı olacak.
10. Maliyet Hesabı, Teklif entegrasyonu ve Fair Stand otomatik maliyet entegrasyonu sonraki fazlarda yapılacak.
