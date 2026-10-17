# Kilit, Geri Alma, Gruplama ve Şablonlar — Yol Haritası

> **Durum:**
>
> | Faz | Durum |
> |---|---|
> | Faz 1 — Kilit | Uygulandı: `kyrox-fair-stand` PR #278, CI yeşil, `main`'de |
> | Faz 2–6 | Plan, kod yok |
>
> Her faz ayrı PR'dır ve kodlamadan önce kullanıcı onayı alınır (`kyrox-fair-stand/AGENTS.md` kod öncesi checkpoint).
>
> Belgenin yeri: Fair Stand plan belgeleri `kyrox-platform/projects/fair-stand/` altında tutulur (`AGENTS.md` sert kural). Aşağıdaki dosya yolları `kyrox-fair-stand` deposuna göredir.
>
> Her faz `SYSTEM_CHANGE_GATE.md` + `SYSTEM_IMPACT_SWEEP.md` zincirinden geçer: `.github/change-contract.json` beyanı → `npm run contract:verify` → targeted regression → `npm test` → `python -m pytest` → `npm run build` → `npm run e2e`.
>
> Kilit, grup ve şablon **fiziksel ürün değildir**: BOM'a, üretime ve maliyete kendileri girmez, `itemKey` taşımaz (`ITEM_CONTRACT.md` kapsamı dışı; açık ürün kararı). Şablondan sahneye konan parçalar normal Item'dır ve BOM'a bugünkü gibi girer.

## 1. Neden

| # | Durum | Örnek | Çözüm | Faz |
|---|---|---|---|---|
| A | Yanlışlıkla kaydırıp yapıyı bozmak | Depo (kapı dahil 5 duvar parçası), duvara konan TV, yere konan box | **Kilit** | 1 |
| B | Yapılan bir hatayı düzeltmek | Yanlış taşıma, yanlış silme, yanlış renk | **Geri al / İleri al** | 2 |
| C | Bağlı parçaların ayrı ayrı oynaması | `wall_200_350` + 3 raf + baza; duvar + lambalar; masa + 3 sandalye | **Grup** (çapalı) | 3 |
| D | Grubun da yanlışlıkla oynamaması | Kurulmuş depo grubu | **Grup kilidi** | 3 |
| E | Grubun içinde ne olduğunu görmek | "Duvar raflı grup" → hangi parçalar? | **Grup listesi paneli** | 3 |
| F | Kurulu grubu bir daha kullanmak | Masa + 3 sandalyeyi çoğaltmak | **Grup çoğaltma** | 3 |
| G | Bir yapıyı bütün olarak taşımak | Depoyu standın başka yerine almak | **Çok duvarlı grup** | 4 |
| H | Sık kullanılan seti her projede hazır bulmak | Organizasyonun "raflı TV'li duvar" seti | **Kurumsal şablon** | 5 |

## 2. Bugünkü durum (koda göre)

- **Seçim tek öğelik.** `selectedModuleId` tek değer (`src/scene3d.js`). Ctrl/Cmd+tık öğe değil **panel yüzeyi** seçer (görsel/renk için; `selectRectangleTo`). Öğeler için çoklu seçim yok.
- **Taşıma tek öğelik.** `dragSession` tek `moduleState` taşır. Bırakınca yalnız plan içindeki yerleşimler yazılır (`finishPlacementDrag`). Duvar zincirinde `planContinuousModuleMove` komşuları kaydırabilir (`src/moduleMove.js`, `wallReflow.js`). Serbest öğe `validatePlacementAgainstModules` ile doğrulanır (`src/modulePlacement.js`). Ok tuşları seçili tek öğeyi taşır.
- **Raf duvara bağlı değil.** Raf bırakılırken duvar bulunup panel birleşimine oturtulur (`snapPanelSeamOverlayPlacement`). Ama yalnız raf kendi mutlak `placement`'ını saklar; "hangi duvara ait" alanı yoktur. Duvar taşınınca raf yerinde kalır.
- **Yerleşim türleri** (canlı `fair_stand_item_type_scene_behavior`):
  - `flat-panel`, `door`, `panel`, `profile`, `connector` → `wall`
  - `shelf`, `tv`, `illuminated-foam` → `wall-overlay`
  - `led-floodlight` → `top`
  - `base`, `box-block`, `counter`, `chair`, `table-*`, `sofa-*`, bitkiler → `free`
- **Duvar yerleşimi iki türlü.** Kenar zinciri (`wallId`: `back` / `left` / `right`; taşıma komşuları kaydırır) ve serbest sıra (`wallId: 'free'`; standın içindeki duvarlar, zincir hesabına girmez).
- **Admin önizlemedeki kilit grubu.** Ürün 3D önizlemesinde (Admin) parçalar `lock_group_id` ile katı grup olarak kilitlenir; "Kilitle", "Gruba ekle", "Gruptan çıkar / Kilidi aç" komutları vardır (`src/itemAdminAssemblyLock.js`, `docs/refactor/ITEM_3D_PREVIEW.md`). Bu **Item montajı** içindir, sahne/proje kilidi değildir; ikisi karıştırılmaz. Katı grup hareket mantığı Faz 3'te yeniden kullanılmak üzere incelenir. Kullanıcıya görünen adlar tutarlı seçilir.
- **Benzer mevcut kavram.** Lightbox/Mesh kumaşı (`fabricGroupId`) birden fazla modülü bağlar ve onları **taşımayı engeller** (`getFabricMoveLock`). Bu kuralı bozmayız.
- **Proje state'i.**
  - Sahne `main.js` içindeki `currentModules` dizisinden kurulur (`rebuildWall` → `scene3d.buildWall`). Stand kurulumu `rebuildSceneFromSetup` ile, proje yükleme `restoreProject` ile yapılır.
  - Anlık görüntü `buildProjectSnapshot()` ile alınır. Otomatik kayıt bu görüntünün imzasını izler (`getProjectStateSignature`, `src/autosaveController.js`).
  - Proje biçimi `{ id, version: 1, modules, stand }` (`src/projectImportValidation.js`). `normalizeModuleItemState` modülü yerinde düzeltir, bilinmeyen alanı silmez.
- **Çoğaltma.** `duplicateModuleState` modülü JSON olarak **bütünüyle kopyalar**, yeni kimlik verir (`src/designState.js`). Duvar zincirinde `duplicateContextModule` yanına ekleme planı kullanır (`src/main.js`).
- **Görseller proje başınadır.** `fair_stand_project_assets` (`organization_id` + `project_id`).
- **Organizasyon.** Projeler, proje görselleri ve maliyet kalemleri organizasyona bağlı (`organization_id`). Item kataloğu (`fair_stand_items`) **ortak**, organizasyona ait değil.
- **Geri alma (Ctrl+Z) yok.**

## 3. Kavramlar

- **Toplu seçim** — Shift+tık ile birden fazla öğe seçmek. Kalıcı değildir; toplu kilitleme ve grup kurmanın ön adımıdır. Ctrl, panel yüzey seçimi olarak kalır.
- **Kilit** — öğenin bulunduğu yere sabitlenmesi. Kilitli öğe taşınmaz, döndürülmez, silinmez. Görünüm (renk, görsel, TV içeriği) değiştirilebilir.
- **Geri al / İleri al** — proje tasarımındaki her değişikliğin adım adım geri alınması ve yinelenmesi.
- **Grup** — isimli, kalıcı öğe kümesi. Bir üyeye tıklamak bütün grubu seçer; grup birlikte taşınır.
- **Çapa** — grubun taşıma referansı. Grupta duvar parçası varsa çapa odur, yoksa ilk üyedir. Taşıma başlarken her üyenin çapaya göre göreli konumu (boyunca / önünde / yükseklik / dönüş) hesaplanır. Çapa kendi kurallarıyla taşınır, üyeler aynı göreli konumla yeniden yerleştirilir.
- **Grup kilidi** — grubun bütün olarak kilitlenmesi.
- **Kurumsal şablon** — bir grubun organizasyon kataloğuna kaydedilmiş hali. Sahneye konunca **normal parçalara ve yeni bir gruba açılır**; şablon bir Item değildir.

## 4. Fazlar

### Faz 1 — Kilit (A)

> **Durum: uygulandı** (`kyrox-fair-stand` PR #278).
> - Kaynak `src/moduleLock.js`.
> - Testler `test/moduleLock.test.js` ve `e2e/module-lock.spec.mjs`.
> - Uygulamada verilen kararlar:
>   - Kilit Sil ve Boyutlandır'ı pasifleştirir.
>   - "Tüm özellikleri kaldır" kilidi korur ve kilitli Işıklı Straforu silmez.
>   - Sahnede kilit simgesi yok; kilit menü başlığında ve seçim bilgisinde "Kilitli" olarak görünür.
>   - Stand kurulumu "Yeni proje oluşturulacak" akışı olduğu ve eski kayıtlı projeyi koruduğu için ek kilit uyarısı eklenmedi.

**Amaç.** Depo, TV, box gibi yerleşmiş parçaların yanlışlıkla bozulmasını bitirmek.

**Davranış**
- Sağ tık → **Kilitle** / **Kilidi aç**.
- Shift+tık ile toplu seçim → **Seçilenleri kilitle / kilidini aç**.
- Kilitli öğe:
  - Sürüklenmez. Sürüklenmeye çalışılırsa "Kilitli — taşımak için önce kilidi açın" uyarısı çıkar; kamera dönüşü normal çalışır.
  - Ok tuşları ve döndürme kısayolu çalışmaz.
  - Silinemez: Sil tuşu ve menü uyarı verir.
  - Seçilebilir; renk, görsel ve TV içeriği değiştirilebilir.
- **Dolaylı hareketi de engeller.** Duvar zincirinde ekleme, çoğaltma ya da başka öğenin taşınması kilitli bir öğeyi kaydıracaksa işlem reddedilir ve hangi kilitli öğenin engellediği yazılır. Kontrol, plan (`placements`) uygulanmadan önceki ortak noktada yapılır.
- Seçiliyken menüde ve durum çubuğunda "Kilitli" görünür. Sahnede kilit simgesi gösterilip gösterilmeyeceği uygulama sırasında karar verilir.

**Veri.** Modül state'ine `locked: true` (yoksa kilitsiz). Proje kaydı, yeniden yükleme, ZIP dışa/içe aktarma ve revizyonlarda korunur. Eski projeler değişmeden açılır. `duplicateModuleState` her şeyi kopyaladığı için çoğaltmada `locked` açıkça temizlenir; kopya kilitsiz doğar.

**Açık kontroller.** Otomatik duvar / otomatik depo / "sahneyi sıfırla" kilitli öğeyle karşılaşınca ne yapar? Sunucu payload'ı alanı aynen saklıyor mu?

**Dokunulacak yüzeyler.**
- `src/scene3d.js`: sürükleme, ok ve döndürme girişleri; toplu seçim.
- `src/moduleContextMenu.js`.
- `src/main.js`: silme, çoğaltma, ekleme yolları.
- Plan uygulayan yerleşim yolları.
- `src/designState.js`: çoğaltmada kilidin temizlenmesi.
- `src/helpGuide.js`.
- Yeni `src/moduleLock.js` ve onun `systemChangeContract.js` path eşlemesi.

Kesin liste `contract:verify` discovery'si ile çıkarılır.

**Testler.**
- Unit: taşıma, döndürme ve silme reddi; reflow planı kilitli öğeyi kaydırıyorsa ret; çoğaltma kilitsiz; kayıt round-trip.
- E2E (`e2e/module-lock.spec.mjs`): kilitle → sürükle → yerinde → yenile → hâlâ kilitli → kilidi aç → taşınabilir.

**Kabul.** Kilitli öğe hiçbir yolla (sürükleme, ok, döndürme, sil, zincir kaydırması) yer değiştirmez; kilit kayıttan sonra korunur; CI zinciri yeşil.

### Faz 2 — Geri al / İleri al (B)

**Amaç.** Tasarımda yapılan her değişikliği geri alabilmek. Gruplamadan önce gelir; grup işlerinde yapılan hata da geri alınabilsin.

**Davranış**
- **Ctrl+Z** geri al; **Ctrl+Y** ve **Ctrl+Shift+Z** ileri al. Araç çubuğunda iki düğme bulunur, geri alınacak adım yoksa pasiftir.
- Geri alınabilen işler: taşıma, döndürme, ekleme, silme, çoğaltma, renk, görsel yerleşimi, Lightbox kumaşı, kilit, grup işlemleri, zemin alanı, stand değişiklikleri.
- Her bırakma ya da menü komutu **tek adımdır**. Sürükleme sırasındaki ara konumlar adım sayılmaz.
- Metin kutusunda yazarken Ctrl+Z tarayıcının kendi metin geri almasıdır; tasarımı etkilemez.

**Teknik yaklaşım: anlık görüntü yığını**
- Değişiklikten önceki tasarım (`stand`, `modules`, ileride `groups`) `buildProjectSnapshot` temelinde kopyalanıp yığına eklenir.
- Geri almada o görüntü `currentModules` ve stand'e yazılır, sahne mevcut yollarla (`rebuildWall`, gerekirse `rebuildSceneFromSetup`) yeniden kurulur.
- Değişiklik tespiti, otomatik kaydın kullandığı imza mantığıyla yapılır: kullanıcı eylemi bittiğinde imza değiştiyse önceki görüntü yığına girer.
- Sınır: son 50 adım (uygulamada ölçülüp kesinleşir).
- Geçmiş **kaydedilmez**. Proje değişince, revizyon açılınca ve sayfa yenilenince sıfırlanır.

**Riskler / kararlar**
- **Görsel silme.** Görsel yöneticisinden bir görselin silinmesi proje varlığını siler (`deleteProjectAsset`). Eski bir adımda o görsel kullanılıyorsa geri alındığında görsel boş görünür. Öneri: görsel silme geri alma kapsamı dışında, ayrı ve onaylı bir işlem olarak kalır.
- **Otomatik kayıt.** Geri alma da bir değişikliktir; otomatik kayıt onu normal şekilde kaydeder.
- **Bellek.** Her adım tasarımın JSON kopyasıdır. Proje boyutuna göre ölçülür; gerekirse sınır düşürülür.

**Dokunulacak yüzeyler.** Yeni `src/designHistory.js` (saf yığın: ekle / geri / ileri / sınır / sıfırla; testli), `src/main.js` (yakalama noktaları, geri yükleme, araç çubuğu), `src/viewKeyboardShortcuts.js` (kısayollar), `index.html` (düğmeler), `src/helpGuide.js`.

**Testler.**
- Unit: yığın davranışı; sınır; yeni değişiklikte ileri dalın silinmesi.
- E2E (`e2e/design-undo.spec.mjs`): taşı → Ctrl+Z → eski yerinde → Ctrl+Y → yeni yerinde; sil → Ctrl+Z → geri geldi.

**Kabul.** Listelenen bütün işler tek tek geri alınır ve yinelenir; proje değişince geçmiş sıfırlanır; CI zinciri yeşil.

### Faz 3 — Grup: tek çapa, liste paneli, çoğaltma (C, D, E, F)

**Amaç.** Duvar + raflar + baza, duvar + lambalar, masa + sandalyeler birlikte hareket etsin. Grup kilitlenebilsin, içeriği görülebilsin, çoğaltılabilsin.

**Davranış: oluşturma ve düzenleme**
- Shift+tık ile 2+ öğe seç → sağ tık → **Grup oluştur** → isim (varsayılan "Grup 1").
- Üyeye tıklamak bütün grubu seçer: tüm üyelerde çerçeve ve grup adı.
- **Gruba ekle (attach):** grup seçiliyken Shift ile yeni öğe ekle → "Gruba ekle".
- **Gruptan çıkar (detach):** Alt+tık ile gruptaki tek öğeyi seç → "Gruptan çıkar".
- **Yeniden adlandır**, **Grubu çöz**, **Grubu kilitle / kilidini aç** (Faz 1 kuralları bütün gruba uygulanır).
- **Sil** (grup seçiliyken): bütün grup, onay sorularak silinir. Kilitliyse silinmez.
- Öğe silinince gruptan düşer. Grupta 1 öğe kalırsa grup çözülür.

**Davranış: birlikte taşıma**
- Sürükleme ve ok tuşlarıyla, §3'teki çapa mantığıyla.
- Çapa bugünkü kurallarla taşınır (zincir, mıknatıs, snap aynen).
- Raf, TV, ışıklı köpük, lamba ve baza duvarın yeni yerine aynı göreli konumla oturtulur. Duvar başka kenara geçerse üyeler de döner.
- Bir üye bile sığmıyor ya da çakışıyorsa bütün taşıma reddedilir ve bütün üyelerde kırmızı gölge çıkar. Grup üyeleri birbirine çakışma sayılmaz.

**Davranış: grup listesi paneli (E)**
- Kenar çubuğunda **Gruplar** bölümü: her grup adıyla, üye sayısıyla ve kilit durumuyla listelenir.
- Grup açılınca üyeleri listelenir. Her satırda katalogdaki ad ve ölçü (ör. "Raf 100", "Baza 200") bulunur.
- Satıra tıklayınca o parça sahnede seçilir ve kamera ona odaklanır.
- Satırdan **gruptan çıkar**; grup başlığından **yeniden adlandır / kilitle / çöz**.

**Davranış: grup çoğaltma (F)**
- Sağ tık → **Grubu çoğalt**. Bütün üyeler yeni kimliklerle kopyalanır (`duplicateModuleState`), kopyalar yeni bir gruba alınır: "Grup adı (kopya)". Renk, görsel ve göreli konumlar aynı kalır; kopyalar kilitsiz doğar. `duplicateModuleState` metal separatör grup kimliklerini zaten yeniliyor; kopya grubun metal levhaları orijinalden ayrı sayılır.
- **Yerleşim:**
  - Serbest gruplarda (masa + sandalyeler) kopya grubun yanına konur. Yer yoksa uyarı verilir ve hiçbir şey eklenmez.
  - Duvar çapalı gruplarda çapa bugünkü duvar çoğaltma kuralıyla yanına eklenir (zincir planı), üyeler yeni duvara göre yerleştirilir.
- Kopya her zaman geçerli bir konuma konur; konamıyorsa işlem tümden reddedilir.

**Kısıtlar**
- Grupta en fazla **1 duvar parçası** (`wall`) bulunur; çapa odur. Yanına sınırsız `wall-overlay`, `top`, `free` üye eklenebilir.
- Lightbox kumaşına bağlı modül bugünkü gibi taşınamaz.
- Bir öğe aynı anda tek grupta olur.

**Veri.** Proje düzeyinde `groups: [{ id, name, moduleIds, locked }]`. Göreli konumlar kaydedilmez, taşıma başında hesaplanır. İçe aktarma doğrulaması: üyeler var mı, öğe tek grupta mı, duvar sayısı ≤ 1 mi. Geri al / ileri al grupları da kapsar.

**Dokunulacak yüzeyler.**
- Yeni `src/moduleGroups.js`: oluştur, ekle, çıkar, çöz, adlandır, doğrula, çoğalt; çapa ve göreli konum hesabı. Saf ve testli.
- `src/scene3d.js`: grup seçimi, çoklu gölge, toplu taşıma.
- `src/moduleContextMenu.js`.
- Kenar çubuğu (`src/sidebarController.js` ve ilgili HTML).
- `src/main.js` ve proje kayıt yolu.
- `src/projectImportValidation.js`.
- `src/featureContracts.js`: `module-group` feature contract'ı, çünkü birden fazla modülü koordine eder.
- `src/helpGuide.js`.

**Testler.**
- Unit: grup işlemleri; çapa taşınınca raf ve baza göreli konumu; kenar değişince dönüş; çakışmada tümden ret; çoğaltmada yeni kimlik ve kopya grubu; içe aktarma doğrulaması.
- E2E (`e2e/module-group.spec.mjs`): duvar + raf + baza → grupla → isim → listede üç parça görünüyor → sürükle → üçü aynı göreli konumda → çoğalt → yenile → iki grup duruyor → detach → çöz.

**Kabul.**
- Gruplu duvar taşınınca raf ve baza "ayrı oynamaz".
- Liste paneli üyeleri doğru gösterir.
- Çoğaltma eksiksiz bir kopya grup üretir.
- Kayıttan sonra her şey korunur; CI zinciri yeşil.

### Faz 4 — Çok duvarlı gruplar: serbest sıra (G)

**Amaç.** Depo gibi standın içinde duran, birden fazla duvar parçasından (kapı dahil) kurulu yapıyı bütün olarak taşımak ve çoğaltmak.

**Kapsam.** Gruptaki bütün duvar parçaları serbest sırada (`wallId: 'free'`) ise birden fazla duvar parçasına izin verilir. Grup katı cisim gibi taşınır: aynı öteleme, üyeler arası bağlantı korunur. Doğrulama her üye için grup dışı öğelere karşı yapılır.

**Ön koşul.** Kullanıcının gerçek depo kaydında duvar parçalarının `wallId` değerleri incelenir. Kenar zincirine dokunan parça varsa o grup Faz 6'ya kalır.

**Testler.** Unit (çok duvarlı katı taşıma, dış çakışmada ret) ve E2E (5 parçalı depo grubunu taşı; parçalar arası mesafe değişmez).

### Faz 5 — Kurumsal şablonlar (H)

**Amaç.** Bir grubu organizasyonun kendi kataloğuna kaydedip başka projelerde tek hamlede kullanmak.

**Neden Item değil, şablon**
- Item kataloğu (`fair_stand_items`) ortaktır, organizasyona ait değildir.
- Bir Item'ın BOM reçetesi, birimi ve davranış ailesi olmalıdır (`ITEM_CONTRACT.md`). Grubu Item yapmak BOM'u ikiye katlama ve sözleşme dışı paralel model riski taşır.
- **Şablon** ise yalnız "hangi parçalar, nasıl dizilmiş" bilgisini saklar. Sahneye konunca normal parçalara açılır. Her parça zaten bir Item olduğu için BOM ve maliyet bugünkü gibi doğru çıkar.

**Davranış**
- Grup seçiliyken sağ tık → **Şablon olarak kaydet** → isim (ör. "Raflı TV'li duvar"), isteğe bağlı açıklama.
- Kenar çubuğunda **Şablonlarım** bölümü: organizasyonun şablonları ve küçük önizlemeleri.
- Sürükle-bırak ya da tıklayıp yerleştirme: şablon tek gölge olarak taşınır. Bırakılınca parçalar normal modüller olarak eklenir ve şablon adıyla **yeni bir grup** kurulur.
- Sahnede her şey normal gruptur: istenmeyen parça **gruptan çıkarılıp silinebilir** ya da grup çözülebilir. Bu sahneyi etkiler, şablonu değiştirmez.
- Şablon yönetimi: yeniden adlandır, güncelle (seçili grupla üzerine yaz), sil. Yetki kuralı uygulamada karara bağlanır.

**Veri (sunucu)**
- Yeni tablo `fair_stand_group_templates`: `id`, `organization_id`, `name`, `description`, `payload` (JSON: parçalar, göreli konumlar, renkler, görsel yerleşimleri), `created_by`, tarihler. `organization_id` ile izole edilir.
- Görseller bugün **proje başına** tutulduğu için şablondaki görseller ayrı ele alınır.
  - **Öneri, 5a:** şablon renkleri ve yapıyı taşır, görseller boş gelir.
  - **5b:** şablon görselleri ayrı depolanır ve şablon sahneye konunca projeye kopyalanır.
- Parçalar `itemKey` ile saklanır. Şablon açılırken katalogda artık olmayan bir `itemKey` varsa o parça atlanır ve kullanıcıya yazılır.

**Dokunulacak yüzeyler.**
- Backend: model, alembic migration, uygulama servisi, API rotaları, organizasyon yetki kontrolü, pytest.
- Frontend: şablon istemcisi, kenar çubuğu bölümü, yerleştirme akışı (Faz 3 çoğaltma mantığını yeniden kullanır), `src/featureContracts.js`.

**Testler.**
- pytest: organizasyon izolasyonu, yetki, payload doğrulaması.
- Unit: şablon ↔ grup dönüşümü, eksik `itemKey`.
- E2E: grup → şablon kaydet → yeni proje → şablonu yerleştir → parçalar ve grup oluştu → bir parçayı çıkar/sil.

### Faz 6 — Gelişmiş

- Kenar duvar zincirine (`back` / `left` / `right`) bağlı birden fazla duvar parçasının grup olarak taşınması (zincir/reflow ile birlikte).
- Grubu döndürme (çapa merkezli, Item rotation adımlarına uygun; `docs/refactor/ROTATION.md`).
- (Opsiyonel, ayrı karar) Rafların gruplamadan bağımsız olarak bağlı oldukları duvarı her zaman takip etmesi: raf state'ine kalıcı "ev sahibi duvar" bağı.
- (Opsiyonel) Şablon görsellerinin şablonla birlikte taşınması (5b).

## 5. Kararlar

| Konu | Karar | Durum |
|---|---|---|
| Faz sırası | Kilit → Geri al → Grup → Çok duvarlı grup → Şablon → Gelişmiş | Öneri |
| Toplu seçim tuşu | Shift+tık (Ctrl panel seçiminde kalır) | Karar (Faz 1) |
| Gruptan tek öğe seçmek | Alt+tık | Öneri |
| Kilitli öğe silinebilir mi | Hayır, önce kilit açılır | Karar (Faz 1) |
| Grup seçiliyken Sil | Bütün grup, onaylı | Öneri |
| Çoğaltılan öğe / grup | Kilitsiz doğar (Faz 1 karar); grup kopyası yeni gruptur (öneri) | Kısmen karar |
| Grupta duvar sayısı (Faz 3) | En fazla 1 | Öneri |
| Geri alma geçmişi | Kaydedilmez, son 50 adım | Öneri |
| Görsel silme geri alınır mı | Hayır, ayrı onaylı işlem | Öneri |
| Şablon Item mı | Hayır, sahnede normal parçalara açılan şablon | Öneri |
| Şablonda görseller | 5a'da yok, 5b'de ayrı depolama | Öneri |
| Kilit / grup / şablon BOM'a girer mi | Hayır (parçalar girer) | Ürün kararı |

## 6. Riskler

- `src/scene3d.js` çok büyük (~350 KB). Seçim ve sürükleme değişiklikleri mevcut kaynak-şekli testlerine dokunabilir (`test/moduleSelectionState.test.js`, `test/moduleSelectionVisual.test.js`, `test/ctrlMultiSelect.test.js`, `test/scene3dPublicContract.test.js`). Discovery çıktısına göre gözden geçirilir.
- Kilit kontrolü yalnız sürüklemeye konursa zincir kaydırması, ekleme, çoğaltma ya da otomatik planlayıcılar kilidi delebilir. Kontrol, plan uygulanmadan önceki ortak noktaya konmalıdır.
- **Shift tuşu çakışması.** Kamerayı yöneten hazır Three.js kontrolünde Shift + sol tıkla boş alanı sürüklemek kamerayı döndürmek yerine kaydırır (pan). Bu varsayılan davranıştır ve uygulamadan önce bu projede doğrulanacaktır. Çoklu seçim de Shift+tık kullanacağı için kural şudur:
  - **Shift+tık bir parçanın üstündeyse:** Parça seçime eklenir ya da çıkarılır; kamera kımıldamaz. Tıklama kamera kontrolünden önce yakalanır; bugün Ctrl+tık için yapılanın aynısıdır (`test/ctrlMultiSelect.test.js`).
  - **Shift+tık / sürükleme boş alandaysa:** Bugünkü kamera davranışı aynen korunur.
- Geri alma yakalama noktası kaçırılırsa bir işlem geri alınamaz; değişiklik tespiti tek noktadan (imza) yapılmalıdır.
- Şablonlar organizasyonlar arası veri sızıntısına açık bir yüzeydir; `organization_id` izolasyonu backend testleriyle korunur.
