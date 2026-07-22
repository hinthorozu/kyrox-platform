from pathlib import Path

P = Path(r"C:\Users\hinthorozuTUF\Kyrox\kyrox-platform")

# --- Fix PROJECT_STATUS links ---
ps = P / "projects/fair-crm/PROJECT_STATUS.md"
text = ps.read_text(encoding="utf-8")
replacements = [
    ("PROJECT_CONSTITUTION.md", "CONSTITUTION.md"),
    ("docs/PRODUCT_VISION.md", "VISION.md"),
    ("docs/DEV_RUNTIME.md", "ops/DEV_RUNTIME.md"),
    ("docs/DEV_AUTO_START_COMPLETION.md", "../../archive/fair-crm/reports/DEV_AUTO_START_COMPLETION.md"),
    ("docs/frontend/RESPONSIVE_UI_STANDARD.md", "frontend/RESPONSIVE_UI_STANDARD.md"),
    ("docs/DECISIONS.md", "decisions/DECISIONS.md"),
    ("docs/import/SOURCE_ADAPTER_FRAMEWORK.md", "import/SOURCE_ADAPTER_FRAMEWORK.md"),
    ("docs/import/IMPORT_ARCHITECTURE.md", "import/IMPORT_ARCHITECTURE.md"),
]
for a, b in replacements:
    text = text.replace(a, b)
text = text.replace(
    "[PROJECT_STATUS.md](PROJECT_STATUS.md), [CHANGELOG.md](CHANGELOG.md), and [CONSTITUTION.md](CONSTITUTION.md) together form the single source of truth for project state and standards.",
    "[PROJECT_STATUS.md](PROJECT_STATUS.md), [CHANGELOG.md](CHANGELOG.md), and [CONSTITUTION.md](CONSTITUTION.md) form the product status/standards SSoT. Ecosystem status: [../../ecosystem/STATUS.md](../../ecosystem/STATUS.md). See [../../ecosystem/DOCUMENT_GOVERNANCE.md](../../ecosystem/DOCUMENT_GOVERNANCE.md).",
)
text = text.replace("[PROJECT_CONSTITUTION.md](CONSTITUTION.md)", "[CONSTITUTION.md](CONSTITUTION.md)")
ps.write_text(text, encoding="utf-8")
print("fixed PROJECT_STATUS links")

const = P / "projects/fair-crm/CONSTITUTION.md"
if const.exists():
    t = const.read_text(encoding="utf-8")
    for a, b in [
        ("docs/PRODUCT_VISION.md", "VISION.md"),
        ("docs/DECISIONS.md", "decisions/DECISIONS.md"),
        ("docs/frontend/FRONTEND_UI_MASTER_STANDARD.md", "frontend/FRONTEND_UI_MASTER_STANDARD.md"),
        ("docs/frontend/RESPONSIVE_UI_STANDARD.md", "frontend/RESPONSIVE_UI_STANDARD.md"),
        ("docs/DEV_RUNTIME.md", "ops/DEV_RUNTIME.md"),
        ("AGENTS.md", "../../AGENTS.md"),
    ]:
        t = t.replace(f"]({a})", f"]({b})")
    const.write_text(t, encoding="utf-8")
    print("fixed CONSTITUTION links")

for name in ["FRONTEND_UI_MASTER_STANDARD.md", "RESPONSIVE_UI_STANDARD.md", "UI_DESIGN_SYSTEM.md"]:
    fp = P / "projects/fair-crm/frontend" / name
    if not fp.exists():
        continue
    t = fp.read_text(encoding="utf-8")
    t = t.replace("../DECISIONS.md", "../decisions/DECISIONS.md")
    t = t.replace("../../PROJECT_CONSTITUTION.md", "../CONSTITUTION.md")
    t = t.replace("../PROJECT_CONSTITUTION.md", "../CONSTITUTION.md")
    fp.write_text(t, encoding="utf-8")
print("fixed frontend standards links")

for name in [
    "IMPORT_ARCHITECTURE.md",
    "SOURCE_ADAPTER_FRAMEWORK.md",
    "MERGE_RULES.md",
    "MATCHING_RULES.md",
    "IMPORT_MAPPING_STANDARD.md",
]:
    fp = P / "projects/fair-crm/import" / name
    if not fp.exists():
        continue
    t = fp.read_text(encoding="utf-8")
    t = t.replace("../DECISIONS.md", "../decisions/DECISIONS.md")
    t = t.replace(
        "../architecture/scraper-akisi-v2-adapter-builder.md",
        "../scraper/ADAPTER_BUILDER_V2.md",
    )
    fp.write_text(t, encoding="utf-8")
print("fixed import links")

for rel, pairs in {
    "projects/fair-crm/integrations/INTEGRATION_WITH_CORE.md": [
        ("../ARCHITECTURE.md", "../architecture/ARCHITECTURE.md"),
        ("../DECISIONS.md", "../decisions/DECISIONS.md"),
        ("../AUTH_RBAC_HANDOVER.md", "AUTH_RBAC_HANDOVER.md"),
    ],
    "projects/fair-crm/integrations/AUTH_RBAC_HANDOVER.md": [
        ("../KNOWN_DECISIONS.md", "../decisions/KNOWN_DECISIONS.md"),
        ("../CI_PROD_PATH_E2E.md", "../testing/CI_PROD_PATH_E2E.md"),
    ],
    "projects/fair-crm/ops/DEV_RUNTIME.md": [
        (
            "DEV_AUTO_START_COMPLETION.md",
            "../../../archive/fair-crm/reports/DEV_AUTO_START_COMPLETION.md",
        ),
    ],
    "projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md": [
        (
            "BACKEND_ARCHITECTURE_STANDARDS.md",
            "../../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md",
        ),
        ("KYROX_CORE_ARCHITECTURE.md", "../README.md"),
        ("ROADMAP.md", "../ROADMAP.md"),
    ],
    "standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md": [
        ("KYROX_CORE_ARCHITECTURE.md", "../../projects/kyrox-core/README.md"),
        (
            "DECISIONS/0002-backend-layered-architecture.md",
            "../../projects/kyrox-core/decisions/0002-backend-layered-architecture.md",
        ),
    ],
}.items():
    fp = P / rel
    if not fp.exists():
        continue
    t = fp.read_text(encoding="utf-8")
    for a, b in pairs:
        t = t.replace(a, b)
    fp.write_text(t, encoding="utf-8")
print("fixed integration/ops/core links")

idx = P / "ecosystem/decisions/ADR_INDEX.md"
if idx.exists():
    t = idx.read_text(encoding="utf-8")
    if "Documentation hub path" not in t:
        t = (
            "# ADR Index\n\n> Location: `ecosystem/decisions/` under kyrox-platform.\n\n"
            + t.lstrip("# ADR Index\n").lstrip()
        )
    idx.write_text(t, encoding="utf-8")
print("fixed ADR_INDEX")

banner = (
    "> **Historical milestone document.** Not an active plan. "
    "Live roadmap: [ecosystem/ROADMAP.md](../../ecosystem/ROADMAP.md). "
    "Live status: [ecosystem/STATUS.md](../../ecosystem/STATUS.md).\n\n"
)
for name in ["M1_FOUNDATION.md", "M2_IDENTITY.md", "M3_PLATFORM_SERVICES.md"]:
    fp = P / "archive/milestones" / name
    t = fp.read_text(encoding="utf-8")
    if "Historical milestone document" not in t:
        fp.write_text(banner + t, encoding="utf-8")
print("added milestone archive banners")

dbanner = (
    "> **Historical design draft.** Not normative. "
    "As-built contract: [PRODUCT_INTEGRATION_GUIDE.md](../../../projects/kyrox-core/integrations/PRODUCT_INTEGRATION_GUIDE.md). "
    "Core status: [PROJECT_STATUS.md](../../../projects/kyrox-core/PROJECT_STATUS.md).\n\n"
)
for fp in (P / "archive/kyrox-core/designs").glob("*.md"):
    t = fp.read_text(encoding="utf-8")
    if "Historical design draft" not in t:
        fp.write_text(dbanner + t, encoding="utf-8")
print("added core design archive banners")
print("LINK_FIX_DONE")
