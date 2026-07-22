# FAIR CRM — Otomasyon Mimarisi ve Wizard Kapsamları

## 1. Temel ürün ayrımı

- **Todo / Görevler = insan işi.**
- **Operation Engine / Otomasyonlar = sistem işi veya sistem tarafından orkestre edilen iş.**
- Backend teknik isimleri `Operation*` olarak kalır.
- Kullanıcı tarafındaki UI adı **Otomasyonlar**dır.

## 2. Ortak motor, tipe özel wizard ve handler

Tüm otomasyonlar aynı **Operation Engine** lifecycle altyapısını kullanır.

### Operation Engine ortak sorumlulukları

- lifecycle ve status yönetimi
- queue / çalışma durumu
- progress
- loglama
- history
- error / retry kayıtları
- başlangıç / bitiş zamanları
- cancel / durdurma davranışı
- çalışma sonucu / result takibi

### Tipe özel sorumluluklar

Her otomasyon tipi kendi:

- wizard akışına,
- input ve ayarlarına,
- validation kurallarına,
- handler implementasyonuna,
- gerçek işi yapan servislerine

sahiptir.

Tek bir ortak Operation Wizard kullanılmaz.

```text
Tipe Özel Wizard
       ↓
Operation
       ↓
Tipe Özel Handler
       ↓
Gerçek İş
       ↓
Ortak Operation Engine lifecycle / log / history / progress
```

Örnek:

```text
Scraper Wizard
→ Operation(type=scraper)
→ ScraperHandler

Bulk Email Wizard
→ Operation(type=bulk_email)
→ BulkEmailHandler

Enrichment Wizard
→ Operation(type=enrichment)
→ EnrichmentHandler
```

Scraper ile email aynı wizard adımlarını paylaşmaz. Ortak olan kısım çalışma, status, progress, log, history, hata ve retry altyapısıdır.

---

# 3. Wizard kapsamları

## 3.1 Scraper Wizard

### Amaç

İnternet veya fuar sitelerindeki katılımcı verilerini otomatik toplamak.

### Kullanıcı akışı

- Scraper kaynağını / site adapterını seçer.
- Fuarı veya hedef kaynağı seçer.
- Gerekli URL / liste / sayfa bilgilerini girer.
- Scraper'a özel çalışma ayarlarını belirler.
- Otomasyonu başlatır.

### Sistem davranışı

- İlgili `ScraperHandler` çalışır.
- Sayfalar taranır.
- Firma / katılımcı verileri toplanır.
- Ham sonuç saklanır.
- Bulunan kayıt sayısı ve progress takip edilir.
- Hatalı / başarısız sayfalar loglanır.
- Çalışma Operation history altında tutulur.

### CRM yazma kuralı

Scraper doğrudan CRM müşteri verisini değiştirmez. Toplanan veri mevcut **Veri Entegrasyonu / Import** akışına teslim edilir.

---

## 3.2 Zenginleştirme Wizard

### Amaç

CRM'de bulunan müşterilerin eksik veya yetersiz bilgilerini dış kaynaklardan araştırıp zenginleştirmek.

### Hedef bilgi örnekleri

- website bulma
- email bulma
- telefon bulma
- şehir / ülke bulma
- firma hakkında ek bilgi bulma
- iletişim bilgilerinin doğrulanması

### Kullanıcı akışı

- İşlenecek müşterileri / fuarları seçer.
- Araştırılacak alanları seçer.
- Kullanılacak zenginleştirme yöntemini / kaynağını seçer.
- Otomasyonu başlatır.

### Sistem davranışı

- `EnrichmentHandler` çalışır.
- Müşteriler sırayla işlenir.
- Bulunan bilgiler mevcut CRM verileriyle karşılaştırılır.
- `bulundu / bulunamadı / hata` gibi sonuçlar tutulur.
- Progress, log ve history oluşturulur.

### Açık ürün kararı

Bulunan bilginin CRM'e **otomatik yazılması** veya **kullanıcı onayından sonra yazılması** henüz belirlenmemiştir. Uygulama öncesi ürün sahibi kararı gerekir.

---

## 3.3 Toplu Email Wizard

### Amaç

Belirlenen müşteri grubuna aynı kampanya / şablon kapsamında toplu email göndermek.

### Kullanıcı akışı

- Hedef müşteri grubunu seçer.
- Bir veya birden fazla fuar seçebilir.
- Gerekirse segment seçer.
- Email şablonunu seçer.
- SMTP hesabını seçer.
- Gönderim ayarlarını belirler.
- Gönderimi başlatır.

### Sistem davranışı

- `BulkEmailHandler` çalışır.
- Alıcı listesi oluşturulur.
- Her müşteri için email adresi kontrol edilir.
- Mail kuyruğu oluşturulur.
- Gönderimler gerçekleştirilir.
- Her alıcı için ayrı sonuç tutulur.

Örnek sonuçlar:

- gönderildi
- başarısız
- timeout
- email yok
- geçersiz email
- bounce

Toplam progress gösterilir, log/history tutulur ve gönderilen mailler müşteri aktivitesine bağlanabilir.

Bu otomasyon **kampanya / batch odaklıdır**.

---

## 3.4 Email Wizard

### Amaç

Tekil veya sınırlı sayıdaki müşteriye belirli bir amaçla otomatik email göndermek.

Toplu Email'den farkı: kampanya / batch odaklı değil, **belirli müşteri veya olay odaklıdır**.

### Kullanım örnekleri

- Bir müşteriye otomatik bilgi maili gönderme
- Belirli bir olaydan sonra mail gönderme
- Bir işlem sonucunda müşteriye mail gönderme

### Kullanıcı akışı

- Müşteri / alıcı seçer.
- Şablon veya içerik seçer.
- SMTP hesabını seçer.
- Gönderimi başlatır.

### Sistem davranışı

- `EmailHandler` çalışır.
- Mail oluşturulur ve gönderilir.
- Sonuç loglanır.
- Activity / history kaydı oluşturulabilir.
- Başarısızlık ve timeout durumları Operation Engine'e bildirilir.

---

## 3.5 Veri Temizleme Wizard

### Amaç

Mevcut CRM verilerindeki bozuk, eksik, hatalı veya tutarsız kayıtları bulmak ve temizlemek.

### Kontrol / işlem örnekleri

- duplicate müşteri tespiti
- eksik email
- eksik telefon
- geçersiz email
- geçersiz telefon formatı
- hatalı ülke
- hatalı şehir
- firma adı normalize etme
- gereksiz boşluk / karakter temizliği
- büyük / küçük harf standardizasyonu
- aynı verinin farklı formatlarda tutulmasının tespiti
- `data_problem` işaretli kayıtların kontrolü

### Kullanıcı akışı

- Hedef müşteri grubunu seçer.
- Çalışacak temizlik kontrollerini seçer.
- Otomasyonu başlatır.

### Sistem davranışı

- `DataCleanupHandler` çalışır.
- Kayıtlar taranır.
- Problemler sınıflandırılır.
- Temiz / problemli kayıt sayıları gösterilir.
- Problem detayları saklanır.
- Progress, log ve history tutulur.

### Duplicate kontrolü

Duplicate müşteri kontrolü Veri Temizleme kapsamındaki işlem türlerinden biri olabilir. Mevcut wizard setinde ayrı bir **Duplicate Kontrol Wizard** tanımlanmamıştır.

### Açık ürün kararı

Tespit edilen hataların sistem tarafından **otomatik düzeltilmesi** veya **kullanıcı onayından sonra uygulanması** henüz belirlenmemiştir. Uygulama öncesi ürün sahibi kararı gerekir.

---

## 3.6 WhatsApp Wizard

### Amaç

Müşterilere sistem üzerinden WhatsApp mesajı göndermek veya WhatsApp tabanlı otomasyon çalıştırmak.

### Kullanıcı akışı

- Hedef müşteri / müşterileri seçer.
- Mesaj / şablon seçer.
- Kullanılacak WhatsApp hesabı / entegrasyonunu seçer.
- Otomasyonu başlatır.

### Sistem davranışı

- `WhatsAppHandler` çalışır.
- Telefon numarası doğrulanır.
- Mesajlar gönderilir.
- Her müşteri için gönderim sonucu tutulur.
- Başarılı / başarısız sonuçlar loglanır.
- Progress ve history oluşturulur.
- Gerektiğinde müşteri Activity kaydı oluşturulabilir.

### Açık ürün kararı

WhatsApp sağlayıcısı ve API entegrasyonu henüz belirlenmemiştir.

---

## 3.7 Hatırlatma Wizard

### Amaç

Belirlenen koşul veya tarihe göre sistemin otomatik aksiyon üretmesi.

### Kullanım örnekleri

- Mail gönderildikten 5 gün sonra cevap yoksa hatırlatma
- Takip tarihi bugün olan müşterileri işleme
- Geciken takipleri bulma
- Belirli tarihte işlem başlatma
- Belirli koşul oluşunca Todo oluşturma

### Kullanıcı akışı

- Hatırlatmanın amacını belirler.
- Hedef kayıtları / kaynağı seçer.
- Tarih veya koşulu belirler.
- Hatırlatma sonucunda yapılacak aksiyonu belirler.

### Sistem davranışı

- `ReminderHandler` çalışır.
- Zaman / koşul kontrol edilir.
- Şart gerçekleştiğinde tanımlanan aksiyon çalıştırılır.
- Gerektiğinde **Todo oluşturulur**.
- Sonuç Operation history / log altında tutulur.

---

# 4. Mevcut wizard sırası

1. Scraper Wizard
2. Zenginleştirme Wizard
3. Toplu Email Wizard
4. Email Wizard
5. Veri Temizleme Wizard
6. WhatsApp Wizard
7. Hatırlatma Wizard

Bu sıra uygulama önceliği anlamına gelmez; yalnızca mevcut tanımlı wizard setini gösterir. Uygulama sırası ürün sahibi tarafından ayrıca belirlenir.
