# Changelog

All notable Fair CRM releases are documented in this file.

Format: one version section per completed sprint milestone. Update this file after every completed sprint.

---

## Unreleased

### P0.2 Identity / SaaS onboarding final lifecycle certification — 2026-08-29

- Completed the approved P0.2 identity/onboarding workstream through FAIR CRM PR #92 after CRM-UI-03 and CRM-UI-04 were merged and certified.
- CRM-UI-03 shipped authenticated `/settings/security` through FAIR CRM PR #90. Current/new password and confirmation UX use the existing thin FAIR CRM/Core bridge; Core remains authoritative for current-password verification, PasswordPolicy, hashing and credential mutation. Successful change revokes Core sessions, clears the FAIR CRM refresh cookie and local frontend session, and returns to `/login`.
- PR #90 final head `d99dcec064a9fecb9452729aca490a1f9f76a849` passed Development Standard Gate #300 / run `33234676182` and merged as `c40bd8518eca2561640c00de0537d8e0e0e85fbb`.
- CRM-UI-04 certified the existing `/admin/system/users` manual user-create path through FAIR CRM PR #91: administrator-supplied passwords remain supported, FAIR CRM forwards them unchanged to Core, protected role/Super Admin controls remain backend-authoritative, and no unsupported setup-link or new Super Admin assignment path was added.
- PR #91 final head `a5730c767ff1274484bfe9ddaa55c948cf4d73f9` passed Development Standard Gate #303 / run `33235256876` and merged as `b6cd8b8c9baebee54d83334f4c5669ea1564106e`. The phase was test-only and changed no production runtime, backend, schema or permission catalog.
- Final FAIR CRM PR #92 added CI-only cross-repository lifecycle certification. Real FAIR CRM runs against real KYROX Core and Core's real SMTP adapter, with activation/reset mail captured only by an in-process memory-only SMTP sink. The certified lifecycle is signup → activation → login → forgot/reset → login → password change → login; activation/reset replay is rejected and pre-credential-change access/refresh sessions are rejected after reset/change.
- PR #92 final head `d498245c4c60bd36b9b3a8aeffed4912e198123b` passed Development Standard Gate #306 / run `33246959509` and Prod-Path E2E #151 / run `33246959442`. The existing production-shaped validation passed `35` tests with `0` failures before the P0.2 lifecycle certification also passed. PR #92 merged as `2f9f159a303ffd055121547de51dcaefc15fc6a9`.
- The lifecycle script keeps raw action tokens, generated passwords and access/refresh material process-local and does not persist or upload them. PR #92 changes CI/test/governance only; no FAIR CRM/Core application runtime or schema behavior changed.
- This completion is intentionally limited to the approved identity/onboarding subset. ADR-0006 suspension, closure/delete/export/retention, billing/entitlement and other still-gated lifecycle decisions remain open.

### P0.2 Identity / SaaS onboarding login integration — 2026-08-29

- Completed CRM-UI-02 through FAIR CRM PR #89: the existing login screen now exposes `Şifremi unuttum` → `/forgot-password` and `Hesap oluştur` → `/signup` entry points to the public identity flows delivered by CRM-UI-01.
- Existing login submit/authentication/session behavior is unchanged. Activation success continues to return the user to login and does not silently issue an implicit product session.
- Added focused frontend coverage for the login link labels/targets and extended the existing P0.2 public-auth feature contract; no backend or credential-authority logic was added.
- PR #89 final head `298dcadbd88df5580db97d7c5f0305570e2c3e26` passed Development Standard Gate #293 / run `33233998091`: `57` frontend test files / `308` tests passed, production build passed and the zero-new UI-governance regression gate passed. The frontend-only change did not produce a separate Prod-Path E2E run. It merged to FAIR CRM `main` as `874c24b1c4c56ea7087e3acd6ea0708117e3a1a3`.
- No FAIR CRM schema migration was required. The next P0.2 implementation phase is CRM-UI-03 authenticated security/password-change settings.

### P0.2 Identity / SaaS onboarding public auth UI — 2026-08-29

- Completed CRM-UI-01 through FAIR CRM PR #88: public `/signup`, `/activate`, `/forgot-password` and `/reset-password` screens now consume the delivered thin FAIR CRM/Core identity bridge without requiring an authenticated product session.
- Signup collects organization name + email only; activation/reset collect the new credential and pass the one-time action token through the bridge. FAIR CRM does not validate/persist identity action tokens or mutate credentials locally.
- Activation/reset tokens are captured from the link into memory and removed from the browser address bar after initial render; missing-token states fail safely without echoing token material.
- Public auth pages use shared FAIR CRM form/card/banner primitives, accessible loading/error/success states and the standard `PageShell`; Core remains authoritative for password policy, token validity and credential changes.
- Frontend bridge coverage proves exact public paths/payloads, safe Core 4xx feedback, sanitized upstream 5xx handling and malformed-success fail-closed behavior. Public-route/missing-token rendering coverage is included in the normal Vitest suite.
- PR #88 final head `3111660795f001d37e899e40abda9d880a3aa1d5` passed Development Standard Gate #291 / run `33233202519`: `56` frontend test files / `307` tests passed, production build passed and the zero-new UI-governance regression gate passed. The frontend-only change did not produce a separate Prod-Path E2E run. It merged to FAIR CRM `main` as `9265dbb24b13e404c8a18cdd21918948a3997b06`.
- No FAIR CRM schema migration was required. The next P0.2 implementation phase is CRM-UI-02 login integration.

### P0.2 Identity / SaaS onboarding backend bridge — 2026-08-29

- Completed CRM-BE-01 through FAIR CRM PR #86: the existing thin `CoreAuthClient` now proxies Core signup, activation completion, forgot/reset password and authenticated password-change APIs without reproducing Core identity business logic.
- Completed CRM-BE-02 through FAIR CRM PR #87: FAIR CRM now exposes matching `/api/v1/auth/*` bridge routes over the Core client while preserving the existing login/refresh/logout transport pattern.
- Public signup/activation/forgot/reset calls remain unauthenticated product transport; authenticated password change forwards the Bearer access token to Core rather than validating credentials locally.
- Successful reset/password-change responses clear the FAIR CRM refresh cookie because Core invalidates prior sessions/credentials; failed validation does not incorrectly clear still-valid product cookie state.
- Credential authority remains in Core: no FAIR CRM password hashing, password policy, raw activation/reset-token persistence or credential mutation was introduced.
- CRM-BE-01 final head passed Development Standard Gate #278 and Prod-Path E2E #148 before merge. CRM-BE-02 final head `1068a5a94d26799e6b63565e18cf6a61e5699a72` passed Development Standard Gate #280 with `1781 passed` and Prod-Path E2E #149 before merge to FAIR CRM `main` as `0c8a0004f5067dbd8041898a1fe590026c22d736`.
- No FAIR CRM schema migration was required. The next P0.2 implementation phase is CRM-UI-01 public signup/activation/password-recovery UI.

### SaaS P0.1 Tenant Isolation Certification — 2026-08-26

- Completed TI-01 through TI-09 against the canonical `organization` tenant/account boundary; no parallel Tenant entity introduced.
- Hardened scraper/background jobs, import/data-operation workers, mail/SMTP ownership, customer communication children, quote/template/participation/activity/todo derived references, export/download artifacts and managed quote logos.
- Certified Platform Super Admin global scope through the Core DB-backed identity model; request body/query/header data cannot self-assert the bypass.
- Final adversarial matrix adds mixed-organization bulk IDs, cross-organization source/target mutation, request-scope spoofing, missing organization context, direct contact/activity/cost-catalog foreign IDs and audit organization context.
- Final FAIR CRM closure: PR #84; Development Standard Gate #268 and Prod-Path E2E #140 passed. Core Super Admin certification: Core PR #11 / Core CI #54.
- Canonical evidence: [backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md](backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md)

### Bulk Email Wizard — Gönder + Operation Detail (step 4) — 2026-07-24

- Wizard 4. adım gerçek gönderim: `POST /api/v1/operations/bulk-email/send` → Operation + BulkEmailHandler → mevcut batch/outbox/worker
- Migration `0058` (nullable fair_id/customer_id/participation_id + attempt-based activity unique) + `0059` (`outbox.fair_name`)
- Manuel/Excel: aynı motor; CRM’siz recipient’te activity yok; CRM bağlıysa attempt bazlı activity audit
- Retry tamamen manuel (`Gönderilmeyenleri Tekrar Gönder`); `sent` yeniden gönderilmez; `sending_timeout` failed grubunda, otomatik retry yok
- Ortak `OperationDetailPage`: canlı log, alıcı sonuç tablosu, JSON/Excel export (gerçek outbox)
- Multi-fair: tek Operation, global dedupe; frontend `npm run build` PASS; targeted backend tests PASS

### Bulk Email Wizard — Özet / Önizleme (step 3) — 2026-07-23

- Özet adımında gerçek alıcı + mail template preview (`POST /api/v1/operations/bulk-email/preview`)
- Manuel/Excel: birleştirme, tekilleştirme, geçersiz eleme; Fuar Listesi: mevcut `fair_emails` recipient resolution + filtreler (çoklu fuar)
- Gönderim / batch / outbox / worker yok; 0 alıcıda Gönder adımına geçiş engelli
- Frontend `npm run build` PASS; Manuel + Fuar UI doğrulandı; batch sayısı değişmedi

### Bulk Email Wizard — Alıcı Kaynağı (step 1) — 2026-07-23

- Tip-özel wizard route: `/operations/new/bulk-email`
- Otomasyonlar → Yeni Otomasyon → Toplu E-posta → Devam Et → Alıcı Kaynağı
- Kaynak A/B: Manuel / Excel veya Fuar Listesi (birlikte değil); gönderim/sorgulama yok
- Frontend `npm run build` PASS; UI flow verified

### Bulk Email Wizard — Mail Ayarları (step 2) — 2026-07-23

- Stepper: Alıcı Kaynağı → Mail Ayarları → Özet → Gönder (Özet/Gönder henüz yok)
- Mail Şablonu / SMTP Hesabı / Konu; `listMailTemplates` + `listSmtpAccounts`
- Geri/ileri form state korunur; gönderim yok
- Frontend `npm run build` PASS; real API + UI verified

### Scraper Automation e2e (ADR-036) — 2026-07-22

- First executable Operation type: `scraper` via `ScraperHandler`
- Otomasyonlar → tip seçici → `/operations/new/scraper` (Scraper Wizard)
- Adapter → fair (adapter-filtered) → `requested_fields` → settings → summary/start
- Reuses `FairScraperJobRunner` + import handoff; Operation ↔ `scraper_run_id` link; cancel/progress mapping
- Fair Detail “Scraper Çalıştır…” UI action removed; scraper start is Otomasyonlar → Web Scraper only
- Backend operations/scraper targeted tests PASS; frontend `npm run build` PASS
- Canon: [decisions/DECISIONS.md](decisions/DECISIONS.md) ADR-036

### Todo / Participation / Automation UI finalize (acceptance 2026-07-22)

**Todo (insan işi)**

- Optional `customer_id` + `source_fair_id` — valid combos: bare / +customer / +fair / +both; detail+edit always available
- Activity **only** on explicit complete (`POST /todos/{id}/complete`): atomic, idempotent, exactly 1 `task_completed`
- create/update (including customer/fair attach/detach) never creates Activity
- UI: “Tamamla ve sonucu kaydet”; `task_completed` displays as **Diğer** on list/detail/edit (backend type preserved)
- Creatable categories exclude system-operation slugs (`toplu_mail`, `whatsapp`, `veri_temizleme`, `sms`); legacy rows readable
- Acceptance: independent/customer/fair/customer+fair detail/edit UI PASS; complete/update Activity rules PASS; responsive + browser/network/console PASS

**Participation (Customer ↔ Fair)**

- Active model fields: Fair, Salon (hall), Stand, Not — Customer + Fair required keys
- Create/update API and UI no longer use `participation_status`, `visited_at`, `primary_contact_id` (legacy DB columns may remain)
- Customer table + fair-side UI PASS; Visual QA 390/768/1024/1440 PASS; FINAL UI gate PASS

**Operations Engine + Automation UI rename**

- Backend: Operation / OperationRun / `/api/v1/operations` / `crm_operations*` (technical names unchanged)
- User-facing Turkish: **İşlemler → Otomasyonlar**, **İşlem → Otomasyon**
- Examples: scraper, enrichment, bulk email, duplicate check, data cleanup
- Frontend tests / UI gates / build PASS

Canon: [CONSTITUTION.md](CONSTITUTION.md) Activity Timeline; [todo/TODO_MODULE_DECISIONS.md](todo/TODO_MODULE_DECISIONS.md) §8–§8c; [decisions/DECISIONS.md](decisions/DECISIONS.md) ADR-034 / ADR-035

### Central Activities screen + hard delete (ADR-033)

- Org-wide `GET /api/v1/activities` with server-side search, customer, type, status, date-range filters
- Single hard delete `DELETE /api/v1/activities/{id}` → `204` (physical row removal)
- Bulk hard delete `POST /api/v1/activities/bulk-delete` with partial-result reporting
- Frontend `/activities` central list: UniversalDataTable, dual pagination, row selection, detail modal, confirm dialogs
- Worklist `last_activity_id` remains `ON DELETE SET NULL` (no silent cascade of unrelated rows)
- Decision: [decisions/DECISIONS.md](decisions/DECISIONS.md) ADR-033

### Width-responsive table standard (ADR-032 update)

- Default list engine: `UniversalDataTable` → `WidthResponsiveDataTable` (container width, column order = priority, child rows)
- Dual top+bottom pagination default via `ServerDataTableFrame` / `ServerDataTablePagination`
- Column squeezing / letter-break wrapping forbidden; `priority: "technical"` stays detail-only
- `ResponsiveDataTable` deprecated as thin adapter; all UniversalDataTable screens inherit the standard
- Docs: [frontend/RESPONSIVE_UI_STANDARD.md](frontend/RESPONSIVE_UI_STANDARD.md)

### Global Responsive UI Design System (ADR-032)

- Shared responsive standard for all Fair CRM screens (390 / 768 / 1024 / 1440)
- Form/filter 3/2/1, `FilterPanel`, `TruncatedText`, `TechnicalDetails`, modal bottom-sheet
- List tables: width-responsive engine (see above)
- [frontend/RESPONSIVE_UI_STANDARD.md](frontend/RESPONSIVE_UI_STANDARD.md)

### Import Job Permanent Delete

- `DELETE /api/v1/data-integration/imports/{batch_id}` — hard delete batch, rows, jobs, stored Excel bytes
- Active analyze/apply job or `analyzing`/`applying` status blocks delete (409)
- Import list **Sil** button with confirmation dialog + success toast

### Import Job Resume Flow + Decision Bulk Actions

- Upload sonrası Import İşleri listesine yönlendirme
- **Devam Et** — status-aware setup/decision resume (`/imports/continue/:id`)
- Bulk preview: `POST .../bulk-actions/preview` (veri değiştirmez)
- Bulk apply job: `POST .../bulk-actions/apply` (202, background)
- Batch apply/bulk lock (409); idempotent bulk (skip rows with decision)
- [../../archive/fair-crm/reports/IMPORT_RESUME_BULK_COMPLETION.md](../../archive/fair-crm/reports/IMPORT_RESUME_BULK_COMPLETION.md)

### Company Name Matching Stabilization

- Turkish-aware normalization + legal suffix / abbreviation handling
- Token-based scoring with confidence bands (70 / 85 / 95)
- Match explanations stored on import rows (`_match_explanation`)
- [../../archive/fair-crm/reports/COMPANY_NAME_MATCHING_COMPLETION.md](../../archive/fair-crm/reports/COMPANY_NAME_MATCHING_COMPLETION.md)

### Universal Excel Import — Column Mapping Grid + Analysis Queue

- Excel preview + per-column mapping grid (dropdown per column)
- Wizard setup: upload → sheet → header → mapping grid → Import Jobs list
- Batch lifecycle statuses (`mapping_completed`, `analysis_queued`, `analyzing`, `decision_required`, …)
- Background analyze via `POST .../analyze-job` (FastAPI BackgroundTasks)
- Organization-level analyze concurrency lock (409 on conflict)
- Migration `0015_import_batch_lifecycle`
- [../../archive/fair-crm/reports/IMPORT_MAPPING_GRID_COMPLETION.md](../../archive/fair-crm/reports/IMPORT_MAPPING_GRID_COMPLETION.md)

### Development runtime (Sprint — Dev Auto Start Standard v1) — MERGE APPROVED

- `docker-compose.yml` — `restart: unless-stopped` on PostgreSQL
- `scripts/dev/dev-lib.ps1` — shared Docker/runtime helpers
- `scripts/dev/dev-start.ps1` — idempotent auto-start (Docker + backend + frontend)
- `scripts/dev/dev-stop.ps1` — stop runtime processes; optional `-StopInfra`
- `scripts/dev/reset-dev.ps1` — refactored to use `dev-lib.ps1` (force reset unchanged)
- `scripts/dev/verify-dev-auto-start.ps1` — automated validation suite
- Windows reboot manual verification: **PASS** (2026-07-02)
- [ops/DEV_RUNTIME.md](ops/DEV_RUNTIME.md) — auto-start workflow documented
- [../../archive/fair-crm/reports/DEV_AUTO_START_COMPLETION.md](../../archive/fair-crm/reports/DEV_AUTO_START_COMPLETION.md) — validation results + sign-off

### Shipped (implementation)

- Customer hard-delete cascade safety (ADR-020) — migrations `0012` / `0013`; archive preserved, DR hard delete cascades
- **Backup format options (Sprint 09.2.4 / ADR-021)** — Admin create modal: `.dump` (DR), `.sql` (plain export), Universal Data Package `.zip` (MVP)
- Migration `0014_backup_format_options` — `backup_format`, `manifest_json` on `system_backups`
- `UniversalDataPackageService` — vendor-independent JSON + manifest ZIP export (not restore)
- Restore remains `.dump`-only; SQL and data package are export/migration formats
- **Universal Server-Side DataTable Sorting Rule (ADR-019)** — mandatory sortable data columns except Actions
- `UniversalDataTable` component — column `{ key, title, sortable: true }` auto-manages sort headers
- Canonical API sort params: `sort_by` + `sort_order` (legacy `sort`/`direction`/`sort_dir` aliases retained)
- All list screens migrated: Fairs, Customers, Participations, Contacts, Activities, Imports, Admin Backups
- Backend whitelist tests extended; invalid sort fields fall back safely (no 400)
- URL sort state on Fairs, Customers, Imports, Backups list pages

### Architecture (documentation only — Sprint 09.2.5)

- **ADR-022** — System Administration & Business Continuity Roadmap (1–2 years)
- Official Admin → System navigation target; Business Continuity conceptual model
- Backup Policy Engine design (Daily / Weekly / Monthly, change detection, retention)
- Backup History, trigger types (Backup vs Policy vs History vs DR vs Restore vs UDP)
- Future: cloud/remote backup (S3, Azure Blob, GCS, NAS), DR workspace, platform admin modules
- Updated: `PROJECT_STATUS.md`, `CONSTITUTION.md`, `VISION.md`

### Product management (documentation only — Sprint 09.2.6)

- **ADR-023** — Tier-Based Product Delivery Strategy (Tier 1–4)
- Planning rule: Tier assignment before roadmap; default priority Tier 1 → 2 → 3 → 4
- Tier 1 gate: UX (Tier 3) does not outrank open foundation without documented override
- Updated: `PROJECT_STATUS.md`, `CONSTITUTION.md`, `VISION.md`

## v0.9.3 — Admin Database Backup Workspace

- **System Administration** module foundation (`system_admin`) — first production-grade admin capability
- Shared backup engine (`app/shared/database_backup`) — used by dev PowerShell scripts and Admin API (no duplicated dump logic)
- Migration `0011_system_backups` — backup metadata (`system_backups` table)
- Admin API `/api/v1/admin/backups` — create (202 + background job), list, get, download
- Restore foundation — `RestoreService`, disabled endpoint (`501`), UI Restore button disabled
- Frontend **Admin → System → Database Backups** at `/admin/system/backups` with live progress polling
- Permissions: `fair_crm.admin.backups.create`, `.read`, `.download`
- Path traversal protection on download; files served from gitignored `backups/` only
- ADR-018 + runtime DoD: migration, reset-dev, Swagger verification, live API, live UI
- Backend tests (185) PASS; frontend build PASS

## v0.9.2 — Database Backup / Restore Standard (dev utility)

- `scripts/dev/backup-db.ps1` — PostgreSQL custom-format backup (`.dump`) with post-backup `pg_restore -l` verification
- `scripts/dev/restore-db.ps1` — safe restore with `-WhatIf` / `-DryRun` and database-name confirmation
- `scripts/dev/list-backups.ps1` — list local backups with timestamp and size
- Reads `DATABASE_URL` from `backend/.env`; stores dumps under gitignored `backups/`
- CONSTITUTION.md — Development Utilities / Database Safety section

## v0.9.1 — Universal Source Adapter Framework

- **SourceAdapter** protocol and **SourceAdapterRegistry** — pluggable data sources without Import Engine changes
- **ExcelSourceAdapter** migrated to formal adapter lifecycle (Connect → Read → Normalize → Preview)
- Upload and sheet selection resolve adapters via registry
- Background apply job fix — runs after DB commit via FastAPI `BackgroundTasks`
- ADR-017 + [import/SOURCE_ADAPTER_FRAMEWORK.md](import/SOURCE_ADAPTER_FRAMEWORK.md)
- Backend tests (180) PASS

## v0.9.0 — Data Integration Workspace & Universal Import Engine

- **Data Integration module** (`data_integration`) — Universal Import Engine with Excel adapter
- API `/api/v1/data-integration/imports/*` (legacy `/imports/*` retained)
- Excel header modes: İlk satır başlık / Başlık yok / Başlık satırını ben seçeceğim
- Sheet selection, import batch list, background apply jobs with progress polling
- Migration `0010_data_integration` — jobs, templates, batch header fields
- Frontend **Veri Entegrasyonu** at `/data-integration` (Import İşleri, Yeni Import, Jobs, Reports)
- Merge decisions extended: `participation_only`, `manual_review`
- Runtime DoD: migration `0010`, dev reset, Swagger verification, live API script (4 scenarios)
- Backend tests (176) and frontend build PASS

---

## v0.8.3 — Universal Server-Side DataTable Standard

- Shared list query contract: `page`, `pageSize`, `search`, `sort`, `direction`, entity filters (legacy aliases retained)
- Shared list response: nested `pagination`, `sorting`, `filters` on all list endpoints
- Server-side search/sort/filter extended to Contacts, Activities, Participations, Import rows
- Fair Participants list optimized for 29k+ participation records (server-side only)
- Migration `0009_list_indexes` for customer, fair, activity, participation list fields
- Frontend `useServerDataTable` hook with URL state sync (refresh, back, forward, shareable links)
- Enhanced `DataTable` with sortable column headers (ASC → DESC → NONE cycle)
- Migrated: Customers, Fairs, Customer Detail tabs, Fair Participants, Import Wizard preview rows
- ADR-015 documented; List Screen Definition of Done added to CONSTITUTION.md
- Backend tests (173) and frontend build PASS

---

## v0.8.2 — Detail Page Action Standard

- `PageHeader` extended with typed `actions` array API (`primary` | `secondary` | `danger`) and breadcrumb back links
- Customer Detail action bar: Düzenle, İletişim Kişisi Ekle, Fuara Ekle, Yeni Aktivite, Arşivle — available from any tab without returning to list
- Fair Detail action bar: Düzenle, Katılımcı Firma Ekle, Katılımcıları İçe Aktar, Yeni Aktivite (disabled pending fair-scoped activity API), Arşivle
- Edit/archive modals and forms wired directly on Detail pages; Import Wizard opens from Fair Detail with fair preselected
- ADR-014 — Detail Page Action Standard documented in [decisions/DECISIONS.md](decisions/DECISIONS.md)
- Frontend build and browser verification PASS

---

## v0.8.1 — Smart Merge Viewer & Cleanup

- Merge diff viewer: field-level CRM vs Import preview with entity grouping (Customer, Participation, Contact)
- Backend `merge_preview` on import row list/decision responses with Turkish summary lines
- Preview UX: filters, company search, sort by confidence/company/status
- Contact import apply verified end-to-end (API + live script)
- Legacy `POST /api/v1/imports/customers/upload` deprecated for removal in v0.9.0
- Removed unused frontend `ImportsPage.tsx`
- `scripts/verify_wizard_imports_live.py` extended with merge preview + contact scenarios
- Dev runtime reset script: `scripts/dev/reset-dev.ps1` + [ops/DEV_RUNTIME.md](ops/DEV_RUNTIME.md)

---

## v0.8.0 — Smart Import Wizard Phase 1

- Smart Import Wizard: 9-step UI at `/imports` with fair context (ADR-012)
- `POST /api/v1/imports/upload` — raw Excel preview without CRM writes
- `PATCH /api/v1/imports/{batch_id}/column-mapping` — manual mapping (headerless Excel supported)
- `POST /api/v1/imports/{batch_id}/analyze` — separate analyze step
- `PATCH /api/v1/imports/{batch_id}/rows/bulk-decision` — bulk merge decisions
- Import batch `fair_id` required for wizard flow; migration `0008_import_wizard`
- Two-level duplicate detection: Customer + Participation in selected Fair
- Apply creates/updates `CustomerFairParticipation` with hall/stand/notes on participation
- Fair Detail → Katılımcıları İçe Aktar entry route `/imports/fair/{id}`
- `fair_name` removed from supported mapping fields
- Backend tests (18 wizard scenarios) + legacy import tests retained
- Frontend build verified

---

## v0.7.0 — Customer Fair Participation

- `CustomerFairParticipation` join entity (`crm_customer_fair_participations`) linking customers and fairs
- Hall, stand, participation status, notes, primary contact, visited_at on participation (import-ready)
- Participation statuses: planned, exhibitor, visited, contacted, follow_up_required, not_interested, customer, other
- Unique active customer + fair; soft delete; recreate allowed after delete
- Primary contact must belong to the same customer
- Create blocked for archived customer or fair
- API: `GET /customers/{id}/fair-participations`, `GET /fairs/{id}/participants`, CRUD `/fair-participations/{id}`
- Customer detail **Katıldığı Fuarlar** tab (add, edit, delete)
- Fair detail page with **Katılımcı Firmalar** tab; company name links to customer detail
- Turkish UI labels and status translations
- Backend tests and `scripts/verify_participations_live.py`

---

## v0.6.0 — Import Engine v1

- Import batch and import row persistence with preview/apply workflow
- Excel (.xlsx) upload with Turkish column alias mapping (Firma Adı, E-posta, …)
- Company name normalization for duplicate detection (Turkish chars, legal suffix removal)
- Row validation (required company_name, multi-email, website URL)
- Duplicate detection within batch and against existing customers (exact + fuzzy via SequenceMatcher)
- Per-row merge decisions: create_new, update_existing, skip (no blind auto-merge)
- Apply import: create/update customers, merge empty fields, merge multi-email, contact create/update
- Import activities (type note, source import) on create/update
- API: `POST /imports/customers/upload`, batch/rows GET, decision PATCH, apply POST
- Frontend **İçe Aktarma** page at `/imports` with upload panel, preview summary, rows table, apply confirm
- Backend tests and live verification script (`scripts/verify_imports_live.py`)

---

## v0.5.1 — UX & Navigation Foundation

- Sidebar + top bar application layout with breadcrumb navigation
- Reusable UI component library under `frontend/src/components/ui/`
- Customer detail page unified tab experience
- Activity timeline with badges, date emphasis, and hover cards
- Standardized empty states, loading skeletons, and confirm dialogs (replacing `window.confirm`)
- Consistent table, form, badge, and color styling across customers, contacts, activities, and fairs
- Responsive sidebar toggle for tablet/narrow screens
- Search placeholder standardization

---

## v0.5.0 — Customer Activities

- Activity CRUD (create, read, update, soft delete)
- List activities by customer with pagination and sorting
- Activity types: call, meeting, email, whatsapp, note, fair_visit, follow_up, other
- Activity status: open, completed, cancelled
- Activity source enum with default `manual` (system/automation values ready for future integrations)
- Optional contact linkage with same-customer validation
- Follow-up date support
- Customer detail page **Aktiviteler** tab with timeline list and add/edit dialog
- Turkish frontend labels for types, status, and source
- Backend tests and live API verification script

---

## v0.4.1 — Multi-Email Support (Customer & Contact)

- Semicolon-separated multi-email in existing `email` string field
- Comma and whitespace normalization on create/update
- Duplicate email deduplication
- Per-address validation with invalid address in error detail
- Turkish frontend placeholder and validation messages

---

## v0.4.0 — Customer Contacts

- Contact CRUD (create, read, update, soft delete)
- List contacts by customer
- Primary contact rule (one `is_primary` per customer)
- Full name computed in API response (not stored in database)
- Customer detail page with İletişim Kişileri tab
- Turkish frontend labels and validation messages
- Backend tests

---

## v0.1.0 — Customer Management Foundation

Initial customer module foundation: domain model, backend structure, Core integration, and Phase 1 design.

---

## v0.2.0 — Customer Management Production Ready

- CRUD
- Archive
- Restore
- Pagination
- Sorting

---

## v0.3.0 — Fair Management

- CRUD
- Archive
- Restore
- Pagination
- Search
- Sorting

---

## Update Protocol

When a sprint completes:

1. Add a new version section below the header (above older entries).
2. List delivered features as bullet points.
3. Bump version according to sprint scope (minor version per major module sprint unless otherwise decided).
4. Update [PROJECT_STATUS.md](PROJECT_STATUS.md) to match the new current version.
