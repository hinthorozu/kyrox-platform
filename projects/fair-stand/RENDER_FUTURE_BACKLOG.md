# Fair Stand — Render / Görsel Kalite Gelecek Backlog'u

> Bu belge geçmişte **FAZ 4** adı altında yazılmış render geliştirme fikirlerini kayıpsız korur.
>
> **Önemli:** Güncel canonical FAZ 4, `fair-stand` deposundaki `ROADMAP_PHASE_4.md` içinde tanımlanan **Module Recipe / Raw BOM / Parametric / Connection Graph** çalışmasıdır. Bu belgedeki render işleri artık FAZ 4 olarak kabul edilmez; henüz yeni faz/sprint numarası verilmemiş gelecek backlog'udur.

## Korunan render hedefleri

- Sahne gerçekçiliğinin artırılması.
- Fuar salonu / environment yaklaşımı.
- Environment / HDRI tabanlı aydınlatma.
- Daha fiziksel ve gerçekçi ışık düzeni.
- Ambient Occlusion / temas gölgeleri.
- PBR materyal kalitesinin yükseltilmesi: roughness, metalness, normal/bump vb.
- Daha gerçekçi zemin, profil, panel, mobilya ve kumaş materyalleri.
- Gelişmiş shadow / contact shadow kalitesi.
- Post-processing ve renk düzenleme seçenekleri.
- Ekran renderer'ından ayrılmış yüksek kaliteli render pipeline'ı.
- Daha kaliteli nihai render çıktısı.

## Tarihsel bağlam

FAZ 3 kapanışında mevcut kamera açısından PNG render, 3× supersampling, sRGB output, ACES Filmic tone mapping ve yükseltilmiş shadow-map kalitesi tamamlanmış olarak kaydedilmişti. O tarihte bir sonraki render geliştirmeleri `FAZ 4` etiketiyle not edilmişti.

Daha sonra proje roadmap'i yeniden tanımlandı ve güncel FAZ 4 üretim reçetesi / parametrik yapı / connection graph kapsamına ayrıldı. Bu nedenle eski render planı silinmek yerine bu backlog'a ayrılmıştır.

## Aktivasyon kuralı

Bu işler tekrar aktif geliştirmeye alınırken:

1. Güncel renderer mimarisi ve performans bütçesi incelenir.
2. İşler yeni bir faz/sprint altında yeniden önceliklendirilir.
3. `fair-stand` deposundaki `ROADMAP.md` içine açıkça eklenir.
4. Eski `FAZ 4` etiketi tekrar kullanılmaz.
