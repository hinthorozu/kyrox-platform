# Fair Stand — Yol Haritası

Item / Category ilişkisel cutover **lokal implementation + lokal acceptance** olarak tamamlandı. Kaynak kontrolü yayını / deployment bu belgenin kapsamında değildir.

Item admin / yazma UI CRM Admin’dedir ve Fair Stand API’ye yazar. Bu yol okuma teslimatıyla sınırlı değildir.

Configurator'ın faz planı (FAZ 4 aktif: modül reçetesi + parametrik / yapısal editör; FAZ 5 Final BOM; FAZ 6 maliyet / Fair CRM):

- Üst seviye plan ve FAZ 4 detayı: `fair-stand` deposundaki `ROADMAP.md` ve `ROADMAP_PHASE_4.md`. `test/roadmapProductionSourceOfTruth.test.js` CI'da onları okuduğu için orada kalır.
- FAZ 5–6 detayı: [ROADMAP_PHASE_5_6.md](ROADMAP_PHASE_5_6.md).
- Faza yerleşmemiş gelecek işler: [PRODUCT_FUTURE.md](PRODUCT_FUTURE.md), [RENDER_FUTURE_BACKLOG.md](RENDER_FUTURE_BACKLOG.md).

Bu belge o planları kopyalamaz; yalnız katalog / platform tarafındaki işleri tutar.

Sonraki işler cutover’ın dışında kalır:

- Tenant-specific kataloglar
- Cost-catalog slug birleşimi (Fair CRM cost-catalog mevcut fazının açıkça dışında)
- Admin Item formu ↔ DB uyumu: serbest metin alanlarının açılır listeye çevrilmesi, ghost alanları ve ölü kolonlar. Ayrıntı ve öneriler: [ADMIN_FORM_DB_AUDIT.md](ADMIN_FORM_DB_AUDIT.md)
