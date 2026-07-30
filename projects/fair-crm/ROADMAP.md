# FAIR CRM Roadmap

Bu doküman FAIR CRM için yapılan işleri ve bundan sonra yapılacak işleri iki ana başlık altında toplar.

---

## NOT

### Operation Engine Duraklatma Standardı

- Mevcut "Durdur" davranışı operasyonu iptal (cancelled) etmektedir.
- Operation Engine için beklenen davranış değiştirilecektir.
- "Durdur" butonu bundan sonra operasyonu iptal etmeyecek, duraklatacaktır.
- Durum akışı: running → paused → running.
- Ayrı bir "İptal Et" aksiyonu bulunacak ve yalnızca bu aksiyon cancelled durumuna geçirecektir.
- Duraklatılan operasyon mevcut ilerleme, loglar ve ara durumunu koruyacaktır.
- Devam Ettir ile aynı noktadan kaldığı yerden devam edecektir.


(Bu not mevcut roadmap içeriğine ek gereksinim olarak eklenmiştir.)