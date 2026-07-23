# FAIR CRM — Adapter Workflow Step Architecture

## Karar

Scraper otomasyonlarında **workflow tanımı adapter bazlı**, **workflow yürütme motoru Operation Engine bazlı** olacaktır.

Bu ayrımın amacı, her adapter'ın kaynak/site yapısına göre farklı adımlar tanımlayabilmesini; buna karşılık step lifecycle, progress, log, checkpoint, hata, retry ve ileride resume gibi ortak davranışların tek bir Operation Engine altyapısından yönetilmesini sağlamaktır.

## Sorumluluk ayrımı

### Adapter sorumluluğu

Adapter şunları tanımlar:

- Kaç step olduğu
- Step sırası
- Her step'in gerçek işi
- Site/kaynak özel navigation ve extraction davranışı
- Step'in ürettiği ara sonuçlar

Adapter kendi workflow motorunu yazmaz.

### Operation Engine sorumluluğu

Operation Engine şunları yönetir:

- Hangi step'te olunduğu
- Step başlangıç / bitiş durumu
- Step progress
- Log ve history
- Checkpoint
- Hata durumu
- Retry
- İleride desteklenirse pause / resume
- Bir step tamamlanınca sıradaki step'e geçiş

Operation Engine adapter'ın kaç step içerdiğini veya step'in site içinde ne yaptığını bilmek zorunda değildir.

## Örnek — Tüyap NEW

Tüyap NEW adapter'ı örneğin şu workflow'u tanımlayabilir:

1. Liste sayfalarını dolaş
2. Firma / katılımcı linklerini topla
3. Toplanan detay linklerini tek tek işle
4. İstenen alanları çıkar ve sonucu üret

Örnek çalışma:

- 120 liste sayfası dolaşılır
- yaklaşık 1500 firma linki çıkarılır
- 1500 detay linki tek tek ziyaret edilir
- seçilen alanlar detaylardan çıkarılır

Bu adımlar **Tüyap NEW adapter'ına özgüdür**.

## Örnek — PDF Adapter / XYZ Fuarı

PDF tabanlı bir adapter çok daha kısa bir workflow tanımlayabilir:

1. PDF'i aç / oku
2. Veriyi çıkar

Bu adapter'ın Tüyap NEW ile aynı step sayısına veya aynı workflow yapısına sahip olması gerekmez.

## Temel ilke

> **Workflow definition = Adapter**  
> **Workflow execution/state machine = Operation Engine**

Her adapter kendi kaynak yapısına uygun step'leri tanımlar; ortak motor bu step'leri aynı lifecycle ve gözlemlenebilirlik altyapısıyla yürütür.

## Uygulama notu

Bu belge mimari kararı kaydeder. Mevcut scraper davranışına otomatik olarak yeni step/checkpoint/resume özelliği eklenmiş sayılmaz. Gerçek implementasyon ayrıca planlanacak ve mevcut çalışma davranışı önce doğrulanacaktır.
