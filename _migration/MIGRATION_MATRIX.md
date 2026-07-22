# Documentation Migration Matrix (2026-07-22)

Columns: Kaynak repo | Kaynak dosya | Durum | Sorun | Hedef dosya | İşlem | Birleşeceği belgeler | Not

## Ecosystem / Platform

| Kaynak repo | Kaynak dosya | Durum | Sorun | Hedef dosya | İşlem | Birleşeceği belgeler | Not |
|-------------|--------------|-------|-------|-------------|-------|----------------------|-----|
| kyrox-platform | ROADMAP.md | STALE | FAIR CRM snapshot eski | ecosystem/ROADMAP.md | REWRITE | STATUS, M4 | Canonical Import dili temizlendi |
| kyrox-platform | STATUS.md | STALE | Import next hedefi yanlış | ecosystem/STATUS.md | REWRITE | fair-crm PROJECT_STATUS | Özet + pointer |
| kyrox-platform | docs/WORKFLOW.md | STALE | M2 active iddiası | ecosystem/WORKFLOW.md | MERGE | AI_WORKFLOW, CONTRIBUTING, AGENTS | Tek süreç belgesi |
| kyrox-platform | docs/REPOSITORY_STRATEGY.md | CURRENT | — | ecosystem/REPOSITORY_STRATEGY.md | REWRITE | ADR-0001 | Docs-only hub kuralı eklendi |
| kyrox-platform | — | — | — | ecosystem/DOCUMENT_GOVERNANCE.md | REWRITE | — | Yeni zorunlu SSoT haritası |
| kyrox-platform | VISION.md | CURRENT | — | ecosystem/VISION.md | MOVE | — | |
| kyrox-platform | PROJECT_PHILOSOPHY.md | CURRENT | — | ecosystem/PHILOSOPHY.md | MOVE | — | |
| kyrox-platform | KNOWN_DEFERRED.md | STALE | CRM deferred yanlış | ecosystem/KNOWN_DEFERRED.md | REWRITE | STATUS | |
| kyrox-platform | CHANGELOG.md | STALE | Integration Preparation | ecosystem/CHANGELOG.md | MOVE+fix | — | |
| kyrox-platform | decisions/* | MIXED | ADR-0003 JWT org_id | ecosystem/decisions/* | KEEP AS CANONICAL / REWRITE | Core ADR-0001 | 0003 as-built |
| kyrox-platform | milestones/M1–M3 | HISTORICAL | — | archive/milestones/* | ARCHIVE | — | Banner eklendi |
| kyrox-platform | milestones/M4 | STALE | Import next | projects/fair-crm/MILESTONE_M4.md | REWRITE | PROJECT_STATUS | |
| kyrox-platform | products/FAIR_CRM.md | STALE | Duplicate status | archive/platform/... | ARCHIVE | README | |

## Fair CRM

| Kaynak repo | Kaynak dosya | Durum | Sorun | Hedef dosya | İşlem | Birleşeceği belgeler | Not |
|-------------|--------------|-------|-------|-------------|-------|----------------------|-----|
| fair-crm | README.md / AGENTS.md | STALE | Import next | archive + projects/fair-crm/README | REWRITE | STATUS | |
| fair-crm | PROJECT_STATUS.md | CURRENT | — | projects/fair-crm/PROJECT_STATUS.md | MOVE | — | Ürün SSoT |
| fair-crm | PROJECT_CONSTITUTION.md | CURRENT | — | projects/fair-crm/CONSTITUTION.md | MOVE | — | |
| fair-crm | ROADMAP.md / CHANGELOG.md / VISION / DECISIONS | MIXED | Sprint numarası çakışması | projects/fair-crm/* | MOVE | STATUS | ROADMAP ops backlog |
| fair-crm | docs/ARCHITECTURE.md | STALE | Import next | projects/fair-crm/architecture/ | REWRITE | INTEGRATION | Header düzeltildi |
| fair-crm | docs/import/* | CURRENT | — | projects/fair-crm/import/ | MOVE | wizard specs | |
| fair-crm | IMPORT_WIZARD_* / IMPORT_ENGINE | HISTORICAL | Implementation forbidden | archive/fair-crm/import/ | ARCHIVE | MERGE_RULES | |
| fair-crm | completion reports | REPORT | — | archive/fair-crm/reports/ | ARCHIVE | — | |
| fair-crm | frontend UI standards | CURRENT | Çoklu canonical | projects/fair-crm/frontend/ | MOVE | master > responsive | |
| fair-crm | background-job-standard | CURRENT | Paylaşımlı | standards/jobs/ | MOVE | — | |
| fair-crm | UI audit / legacy reports | REPORT | — | archive/fair-crm/ui-audits|legacy | ARCHIVE | — | |
| fair-crm | (tüm .md proje dosyaları) | — | Yanlış repo | — | DELETE AFTER MERGE | platform | 77 silindi |

## KYROX Core

| Kaynak repo | Kaynak dosya | Durum | Sorun | Hedef dosya | İşlem | Birleşeceği belgeler | Not |
|-------------|--------------|-------|-------|-------------|-------|----------------------|-----|
| kyrox-core | PRODUCT_INTEGRATION_GUIDE.md | CURRENT | — | projects/kyrox-core/integrations/ | MOVE | ADR-0003 | As-built sözleşme |
| kyrox-core | BACKEND_ARCHITECTURE_STANDARDS.md | CURRENT | — | standards/backend/ | MOVE | ADR-0002 | |
| kyrox-core | docs/ROADMAP.md | MIXED | Integration prep dili | projects/kyrox-core/ROADMAP.md | MOVE+FIX | ecosystem ROADMAP | |
| kyrox-core | CHANGELOG.md | CURRENT | — | projects/kyrox-core/CHANGELOG.md | MOVE | — | |
| kyrox-core | README/AGENTS | MIXED | — | archive + projects README/STATUS | REWRITE | platform STATUS | |
| kyrox-core | DECISIONS/0001 | DUPLICATE | Platform ADR-0002 | archive/kyrox-core/decisions/ | DELETE AFTER MERGE | ecosystem ADR-0002 | |
| kyrox-core | DECISIONS/0002–0003 | CURRENT | — | projects/kyrox-core/decisions/ | MOVE | — | |
| kyrox-core | *_PLATFORM_DESIGN.md | HISTORICAL | Stale permissions/JWT | archive/kyrox-core/designs/ | ARCHIVE | Integration guide | |
| kyrox-core | .cursor/.kyrox/.github md | CURRENT | Agent/git | standards/ai|git | MOVE | WORKFLOW | |
| kyrox-core | (tüm .md) | — | Yanlış repo | — | DELETE AFTER MERGE | platform | 21 silindi |

## Doğrulama özeti

- fair-crm / kyrox-core proje `.md` = 0 (vendor `node_modules` / `.venv` hariç)
- Zorunlu ecosystem + project giriş dosyaları mevcut
- JWT `org_id` çelişkisi: kod + Integration Guide esas alındı; ADR-0003 as-built olarak düzeltildi
