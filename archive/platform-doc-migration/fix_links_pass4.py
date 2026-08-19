from pathlib import Path
import re

ROOT = Path(r"C:\Users\hinthorozuTUF\Kyrox\kyrox-platform")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

FILE_MAPS = {
    "projects/fair-crm/VISION.md": {
        "../decisions/DECISIONS.md": "decisions/DECISIONS.md",
    },
    "projects/fair-crm/architecture/ARCHITECTURE.md": {
        "DEV_RUNTIME.md": "../ops/DEV_RUNTIME.md",
    },
    "projects/fair-crm/import/IMPORT_ARCHITECTURE.md": {
        "../IMPORT_ENGINE.md": "../../../archive/fair-crm/import/IMPORT_ENGINE.md",
    },
    "projects/fair-crm/import/IMPORT_MAPPING_STANDARD.md": {
        "../IMPORT_WIZARD_UX_FLOW.md": "../../../archive/fair-crm/import/IMPORT_WIZARD_UX_FLOW.md",
    },
    "projects/fair-crm/import/MERGE_RULES.md": {
        "../IMPORT_WIZARD_MERGE_RULES.md": "../../../archive/fair-crm/import/IMPORT_WIZARD_MERGE_RULES.md",
    },
    "projects/fair-crm/integrations/AUTH_RBAC_HANDOVER.md": {
        "CI_PROD_PATH_E2E.md": "../testing/CI_PROD_PATH_E2E.md",
        "KNOWN_decisions/DECISIONS.md": "../decisions/DECISIONS.md",
        "DEV_RESTART_GUIDE.md": "../ops/DEV_RESTART_GUIDE.md",
        "PROJECT_SNAPSHOT_2026-07-05.md": "../../../archive/fair-crm/2026-07-05/PROJECT_SNAPSHOT.md",
    },
    "projects/fair-crm/integrations/INTEGRATION_WITH_CORE.md": {
        "ARCHITECTURE.md": "../architecture/ARCHITECTURE.md",
        "decisions/DECISIONS.md": "../decisions/DECISIONS.md",
        "DEV_RUNTIME.md": "../ops/DEV_RUNTIME.md",
        "../../kyrox-platform/decisions/0004-audit-service-strategy.md": "../../../ecosystem/decisions/0004-audit-service-strategy.md",
    },
    "projects/fair-crm/legacy/UMCRM_MIGRATION.md": {
        "IMPORT_ENGINE.md": "../../../archive/fair-crm/import/IMPORT_ENGINE.md",
    },
    "projects/fair-crm/ops/DEV_RESTART_GUIDE.md": {
        "../scripts/server/README.md": "SERVER_DEPLOY.md",
        "AUTH_RBAC_HANDOVER.md": "../integrations/AUTH_RBAC_HANDOVER.md",
        "CI_PROD_PATH_E2E.md": "../testing/CI_PROD_PATH_E2E.md",
        "PROJECT_SNAPSHOT_2026-07-05.md": "../../../archive/fair-crm/2026-07-05/PROJECT_SNAPSHOT.md",
    },
    "projects/fair-crm/ops/DEV_RUNTIME.md": {
        "CI_PROD_PATH_E2E.md": "../testing/CI_PROD_PATH_E2E.md",
        "PROJECT_SNAPSHOT_2026-07-05.md": "../../../archive/fair-crm/2026-07-05/PROJECT_SNAPSHOT.md",
        "AUTH_RBAC_HANDOVER.md": "../integrations/AUTH_RBAC_HANDOVER.md",
        "ARCHITECTURE_STATUS.md": "../../../archive/fair-crm/2026-07-05/ARCHITECTURE_STATUS.md",
        "KNOWN_decisions/DECISIONS.md": "../decisions/DECISIONS.md",
    },
    "projects/fair-crm/performance/CUSTOMER_COMMUNICATION_PERFORMANCE.md": {
        "decisions/DECISIONS.md": "../decisions/DECISIONS.md",
    },
    "projects/fair-crm/performance/INFRASTRUCTURE_PERFORMANCE_ROADMAP.md": {
        "CUSTOMER_CLEANUP_ARCHITECTURE.md": "../maintenance/CUSTOMER_CLEANUP_ARCHITECTURE.md",
        "import/MATCHING_RULES.md": "../import/MATCHING_RULES.md",
    },
    "projects/fair-crm/scraper/ADAPTER_BUILDER_V2.md": {
        "../PRODUCT_VISION.md": "../VISION.md",
    },
    "projects/fair-crm/testing/GITHUB_WORKFLOWS.md": {
        "../docs/CI_PROD_PATH_E2E.md": "CI_PROD_PATH_E2E.md",
    },
    "projects/kyrox-core/decisions/0002-backend-layered-architecture.md": {
        "0001-core-product-separation.md": "../../../ecosystem/decisions/0002-core-product-separation.md",
    },
    "projects/kyrox-core/decisions/0003-organization-as-tenant-concept.md": {
        "../IDENTITY_PLATFORM_DESIGN.md": "../../../archive/kyrox-core/designs/IDENTITY_PLATFORM_DESIGN.md",
        "0001-core-product-separation.md": "../../../ecosystem/decisions/0002-core-product-separation.md",
    },
    "projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md": {
        "PLATFORM_SERVICES_DESIGN.md": "../../../archive/kyrox-core/designs/PLATFORM_SERVICES_DESIGN.md",
        "IDENTITY_PLATFORM_DESIGN.md": "../../../archive/kyrox-core/designs/IDENTITY_PLATFORM_DESIGN.md",
        "../../kyrox-platform/decisions/0004-audit-service-strategy.md": "../../../ecosystem/decisions/0004-audit-service-strategy.md",
    },
    "standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md": {
        "DECISIONS/0001-core-product-separation.md": "../../ecosystem/decisions/0002-core-product-separation.md",
        "ROADMAP.md": "../../projects/kyrox-core/ROADMAP.md",
    },
    "projects/fair-crm/frontend/UI_DESIGN_SYSTEM.md": {
        # referenced allowlist doc never existed as standalone; point to specialty evidence archive
        "UI_INVENTORY_ALLOWLIST.md": "../../../archive/fair-crm/ui-audits/2026-07-22/SPECIALTY_COMPONENTS.md",
    },
}

for rel, pairs in FILE_MAPS.items():
    fp = ROOT / rel
    if not fp.exists():
        print("missing", rel)
        continue
    t = fp.read_text(encoding="utf-8", errors="replace")
    for a in sorted(pairs.keys(), key=len, reverse=True):
        t = t.replace(f"]({a})", f"]({pairs[a]})")
    fp.write_text(t, encoding="utf-8")
    print("fixed", rel)

broken = []
files = list((ROOT / "ecosystem").rglob("*.md")) + list((ROOT / "projects").rglob("*.md")) + list(
    (ROOT / "standards").rglob("*.md")
) + [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CONTRIBUTING.md"]
for fp in files:
    text = fp.read_text(encoding="utf-8", errors="replace")
    for m in LINK_RE.finditer(text):
        url = m.group(2).strip()
        if url.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path_part = url.split("#", 1)[0]
        if not path_part:
            continue
        if not (fp.parent / path_part).resolve().exists():
            broken.append(f"{fp.relative_to(ROOT).as_posix()} -> {path_part}")
print("broken_after", len(broken))
for b in broken:
    print(b)
