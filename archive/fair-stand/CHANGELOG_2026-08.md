# Changelog

> **TARİHÎ GÜNLÜK.** Ağustos 2026 civarında durur; `itemKey` / self BOM / Playwright E2E bu dosyada yoktur. Güncel durum: `fair-stand` deposundaki `audit/SISTEM_MUTABAKAT_RAPORU.md` ve `projects/fair-stand/PROJECT_STATUS.md`. 2026-10-13'te `fair-stand/Changelog.md` adından buraya taşındı.

Bu dosya, Fair Stand / Maxima Stand Konfigüratörü projesinde başlangıçtan o tarihe yapılan geliştirmeleri kronolojik olarak kaydeder.

## Başlangıç ve proje iskeleti

1. Proje, bağımsız çalışan bir 3D fuar standı konfigüratörü olarak başlatıldı.
2. GitHub deposu olarak `hinthorozu/fair-stand` kullanıldı.
3. İlk proje notları ve hedefleri `README.md` dosyasına yazıldı.
4. Uygulama için Vite tabanlı bir frontend yapısı oluşturuldu.
5. 3D sahne motoru olarak Three.js eklendi.
6. Three.js OrbitControls entegrasyonu yapıldı.
7. `package.json` oluşturuldu.
8. `npm run dev`, `npm run test`, `npm run build` ve `npm run preview` scriptleri tanımlandı.
9. GitHub Actions üzerinden otomatik test ve build kontrolü kuruldu.

## Maxima sistem ölçüleri ve katalog

10. Stand yüksekliği 350 cm olarak tanımlandı.
11. Stand derinliği 10 cm olarak tanımlandı.
12. Düz panel yapısı 7 adet yatay bölüme ayrıldı.
13. Her yatay bölüm 50 cm yükseklik olacak şekilde modellendi.
14. Standart düz panel genişlikleri 50 / 100 / 150 / 200 cm olarak tanımlandı.
15. `Düz Panel 50` katalog öğesi eklendi.
16. `Düz Panel 100` katalog öğesi eklendi.
17. `Düz Panel 150` katalog öğesi eklendi.
18. `Düz Panel 200` katalog öğesi eklendi.
19. `3 Raflı Vitrin 100` katalog öğesi tanımlandı.
20. `2 Raflı Vitrin 100` katalog öğesi tanımlandı.
21. `Depo Kapısı 100` katalog öğesi tanımlandı.
22. `Separatör 100` katalog öğesi tanımlandı.
23. `Separatör 50` katalog öğesi tanımlandı.

## İlk 3D duvar prototipi

24. Three.js sahnesi oluşturuldu.
25. Perspektif kamera eklendi.
26. OrbitControls ile sahne döndürme ve zoom desteği eklendi.
27. Hemisphere light eklendi.
28. Directional light eklendi.
29. Gölge desteği açıldı.
30. Zemin plane'i eklendi.
31. Grid zemini eklendi.
32. Maxima benzeri dikey profil geometrileri oluşturuldu.
33. Maxima benzeri yatay ray geometrileri oluşturuldu.
34. Her düz modül için 7 ayrı seçilebilir panel yüzeyi üretildi.
35. Panel arka gövdesi ayrı mesh olarak oluşturuldu.
36. Panel ön yüzeyi ayrı mesh olarak oluşturuldu.
37. Modüllerin yan yana hizalı şekilde yerleştirilmesi sağlandı.
38. İlk demo olarak 350 cm duvarın otomatik şekilde `200 + 150` modüllerine bölünmesi sağlandı.

## Düz duvar oluşturma motoru

39. Duvar genişliği doğrulama fonksiyonu yazıldı.
40. Minimum duvar genişliği 50 cm olarak belirlendi.
41. Şimdilik duvar ölçülerinin 50 cm katları olması şartı eklendi.
42. 50 / 100 / 150 / 200 cm modülleri kullanarak otomatik düz duvar oluşturma algoritması yazıldı.
43. Algoritmada büyük modülden küçüğe seçim yapılarak modül sayısının azaltılması hedeflendi.
44. 350 cm için `200 + 150` sonucu test edildi.
45. 600 cm için `200 + 200 + 200` mantığı desteklendi.
46. Otomatik duvar çözüm motoru için testler yazıldı.

## Kullanıcı arayüzü

47. Sol tarafta kontrol paneli oluşturuldu.
48. Toplam duvar genişliği girişi eklendi.
49. `Oluştur` butonu eklendi.
50. Oluşturulan duvarın toplam ölçüsünü ve modül dağılımını gösteren bilgi alanı eklendi.
51. Elle 50 cm modül ekleme butonu eklendi.
52. Elle 100 cm modül ekleme butonu eklendi.
53. Elle 150 cm modül ekleme butonu eklendi.
54. Elle 200 cm modül ekleme butonu eklendi.
55. `Duvarı temizle` butonu eklendi.
56. Seçili yüzey bilgisi alanı eklendi.
57. Renk seçici eklendi.
58. `Rengi uygula` butonu eklendi.
59. Görsel / logo dosya seçme alanı eklendi.
60. `Görseli kaldır` butonu eklendi.
61. Sağ üstte sahne kullanım ipuçları eklendi.
62. Arayüz mobil ekranlar için responsive hale getirildi.

## 11 Ağustos 2026 — FAZ 3 / Zemin sistemi tamamlandı

- Aktif stand alanı sabit **5 cm yüksekliğinde platform** haline getirildi; modüller ve duvarlar platform üst kotuna taşındı.
- Platform yüksekliği zemin tipi ve renk değişikliklerinden bağımsız, değişmez 5 cm olarak sabitlendi.
- **Karolaj** zemini gerçek ölçekte **100 × 100 cm** olarak eklendi; stand ölçüsü tam metre değilse son karo otomatik kalan ölçüde kırpılır (ör. 450 cm = 100 + 100 + 100 + 100 + 50).
- Karolaj, mevcut **Aktif renk → Rengi uygula** aracıyla boyanabilir hale getirildi; grid/derz çizgileri renk değişiminde korunur.
- **Halı / Halıfleks** zemini eklendi; yüzey mevcut aktif renk aracıyla boyanabilir hale getirildi.
- Parke zemini üç sabit seçenek olarak ayrıldı: **Parke Açık**, **Parke Sarı**, **Parke Beton**.
- Parke deseni tuğla görünümünden çıkarılıp uzun, ince ve şaşırtmalı parke/laminat lamel düzenine dönüştürüldü.
- Parke seçenekleri serbest renk boyamasının dışında bırakıldı; kendi sabit yüzey tonlarını kullanır.
- Zemin seçimi ve boyama davranışları mevcut panel/modül renk sistemini bozmadan entegre edildi.
- **FAZ 3 / 1. Zemin ayarlanması tamamlandı.**

## 11 Ağustos 2026 — LED projektör ve hareket davranışları

- LED Projektör katalog modülü eklendi; siyah ince floodlight gövde, braket ve emissive lens geometrisi oluşturuldu.
- Projektör ilk sürümde 350 cm duvar üst kotuna bağlanan üst aksesuar olarak tanımlandı; duvar kapasitesini ve normal modül collision hesabını tüketmez.
- Projektör/lamba hareketi 50 cm yerine **20 cm adım/snap** hassasiyetine çekildi.
- Sağ/sol ekleme sırasında yeni lambanın zemine düşmesi problemi düzeltildi.
- Lamba/projektör seçim ve hareket yüzeyi genişletildi; yalnız ön yüzünden değil gövdenin kullanılabilir yüzeylerinden seçilebilir hale getirildi.
- Hareketli modüllerde seçim davranışı ortaklaştırıldı; modülün uygun mesh yüzeylerinden seçim, taşıma ve `R` rotasyonu çalışır.
- `R` rotasyonu modül merkezinden yapılacak şekilde düzeltildi; dönüş sırasında modülün gereksiz yürümesi azaltıldı.
- Lambalar yalnız duvar dibine bağlı kalmadan stand alanında **serbest yerleşebilir** hale getirildi.
- Serbest lambaların köşelerden dönebilmesi ve bırakıldığında kaybolmaması için placement/drop akışı düzeltildi.

## 11 Ağustos 2026 — Mobilya / banko düzenlemeleri

- Raflı modüllerin derinliği **38 cm** olarak güncellendi.
- 100 / 150 / 200 cm bankolar ortak panel mantığına geçirildi.
- Bankolarda yalnız **4 köşe dikmesi** kullanılır.
- Ön, sağ ve sol yüzlerde duvar panel sistemine benzer biçimde **üst üste 2 panel** bulunur.
- Banko panel yüzeyleri renk/görsel uygulaması için ayrı seçilebilir kalırken modül taşıma ve rotasyon davranışına da katılır.
- Banko panelleri ve yatay ayrım çizgileri köşe profillerinden dışarı taşmayacak şekilde flush hale getirildi.
- Banko üst tablası baza mantığıyla **her kenarda 2 cm taşma** yapacak şekilde korundu.

## 11 Ağustos 2026 — Seçim, rotasyon ve silme ergonomisi

- Hareketli modüllerde tıklanabilir/selectable mesh kapsamı genişletildi; üst/yan/ön gibi uygun gövde yüzeylerinden modül seçimi mümkün hale getirildi.
- Panel yüzeylerinin renk/görsel seçilebilirliği korunurken aynı yüzey üzerinden modül hareket/rotasyon davranışı da desteklendi.
- `R` ile rotasyon modülün bulunduğu yerde, kendi merkezi etrafında yapılacak şekilde iyileştirildi.
- Klavyedeki **Delete** tuşu mevcut sağ tık → Sil akışıyla aynı silme fonksiyonuna bağlandı.
- Input/textarea gibi metin giriş alanlarında Delete kısayolunun modül silmesini tetiklemesi engellendi.

## 11 Ağustos 2026 — Proje kaydetme, açma ve proje izolasyonu

- Proje state'i kalıcı saklanabilir hale getirildi.
- **Yeni / Kaydet / Aç / Sil** proje akışı eklendi.
- Projede stand tipi ve ölçüleri, zemin ayarları, tüm modüller, placement/rotasyon state'i, panel renkleri ve panel görsel referansları saklanır.
- Three.js mesh'leri doğrudan saklanmaz; proje açıldığında kayıtlı state üzerinden sahne yeniden üretilir.
- Proje kayıtlarına ileride migration yapılabilmesi için versiyonlama altyapısı eklendi.
- Kullanılan görseller global arşiv yerine **projeye özel asset** mantığına geçirildi.
- Her görsel `projectId` ile ilişkilendirilir; bir projeye yüklenen görsel başka projede görünmez.
- Proje silindiğinde o projeye bağlı asset'lerin de temizlenebilmesi için proje-asset ilişkisi kuruldu.

## 11 Ağustos 2026 — Otomatik kaydetme

- Manuel **Kaydet** butonu korunarak otomatik kaydetme eklendi.
- Proje en az bir kez manuel kaydedildikten sonra autosave aktif olur.
- Modül ekleme/silme/taşıma/döndürme, renk, görsel, zemin ve proje adı dahil proje state değişiklikleri takip edilir.
- Son değişiklikten sonra **5 saniye** yeni işlem yapılmazsa tek autosave gerçekleştirilir.
- Arka arkaya yapılan işlemler debounce edilerek gereksiz IndexedDB yazımı önlenir.
- Kullanıcıya `Değişiklik var`, `Kaydediliyor…`, `Kaydedildi · Otomatik` durumları gösterilir.
- Görsel blob'ları her autosave'de yeniden yazılmaz; proje state'i güncellenir.

## 11 Ağustos 2026 — FAZ 3 / Mevcut kamera açısından PNG render

- Sahnedeki **Render Al** özelliği eklendi.
- Render, preset kamera kullanmaz; kullanıcının o anda baktığı **kamera açısı, zoom ve pan** değerlerini birebir korur.
- Render sırasında seçim çerçeveleri ve editör yardımcıları geçici olarak gizlenir; işlem sonrası sahne normal haline döner.
- PNG çıktı kalitesi **3× supersampling** seviyesine yükseltildi.
- Three.js renderer için **sRGB output color space** ve **ACES Filmic tone mapping** etkinleştirildi.
- Tone mapping exposure değeri mevcut sahne için ayarlandı.
- Ana directional light shadow map çözünürlüğü **2048 × 2048 → 4096 × 4096** yükseltildi.
- Toolbar `pointer-events` davranışı düzeltilerek Render Al butonunun tıklanabilir olması sağlandı.
- FAZ 3 render hedefi: mevcut gerçek zamanlı Three.js sahnesinden mümkün olan temiz ve yüksek çözünürlüklü çıktıyı almak.

## FAZ 4 NOTU — İleri / fotogerçekçi render

FAZ 3'te render, mevcut gerçek zamanlı Three.js sahnesinin kalite sınırları içinde tutulacaktır. **Fotogerçekçi ve ileri seviye render geliştirmeleri FAZ 4 kapsamına alınmıştır.**

FAZ 4 render araştırma/geliştirme başlıkları:

- Daha fiziksel ve gerçekçi ışık düzeni.
- Ambient Occlusion / temas gölgeleri.
- PBR materyal kalitesinin yükseltilmesi (roughness, metalness, normal/bump vb.).
- Daha gerçekçi zemin, profil, panel, mobilya ve kumaş materyalleri.
- Gelişmiş shadow/contact shadow kalitesi.
- Environment / HDRI tabanlı aydınlatma değerlendirmesi.
- Post-processing ve renk düzenleme seçenekleri.
- Render için ekran renderer'ından ayrılmış yüksek kaliteli ayrı pipeline ihtiyacının değerlendirilmesi.
- Gerekirse Three.js dışı veya sunucu/harici render motoru entegrasyonunun teknik ve maliyet açısından değerlendirilmesi.
- Kullanıcının mevcut kamera açısını koruyarak daha yüksek kaliteli nihai müşteri sunum çıktısı üretmek ana hedef olacaktır.
