from pathlib import Path
import re

ROOT = Path(r"C:\Users\hinthorozuTUF\Kyrox\kyrox-platform")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Fix doubled path artifact
for fp in ROOT.rglob("*.md"):
    if "_migration" in fp.parts:
        continue
    t = fp.read_text(encoding="utf-8", errors="replace")
    n = t.replace("decisions/decisions/DECISIONS.md", "decisions/DECISIONS.md")
    n = n.replace("../decisions/decisions/DECISIONS.md", "../decisions/DECISIONS.md")
    if n != t:
        fp.write_text(n, encoding="utf-8")

# File-specific relative link maps: path from file -> correct relative
FILE_MAPS = {
    "ecosystem/VISION.md": {
        "../REPOSITORY_STRATEGY.md": "REPOSITORY_STRATEGY.md",
        "docs/ECOSYSTEM.md": "REPOSITORY_STRATEGY.md",
        "REPOSITORY_STRATEGY.md": "REPOSITORY_STRATEGY.md",
    },
    "ecosystem/decisions/0001-repository-strategy.md": {
        "../../WORKFLOW.md": "../WORKFLOW.md",
        "../../REPOSITORY_STRATEGY.md": "../REPOSITORY_STRATEGY.md",
        "../docs/WORKFLOW.md": "../WORKFLOW.md",
        "../docs/REPOSITORY_STRATEGY.md": "../REPOSITORY_STRATEGY.md",
        "../docs/ECOSYSTEM.md": "../REPOSITORY_STRATEGY.md",
    },
    "ecosystem/decisions/0002-core-product-separation.md": {
        "../../REPOSITORY_STRATEGY.md": "../REPOSITORY_STRATEGY.md",
        "../docs/ECOSYSTEM.md": "../REPOSITORY_STRATEGY.md",
        "../docs/REPOSITORY_STRATEGY.md": "../REPOSITORY_STRATEGY.md",
    },
    "projects/fair-crm/VISION.md": {
        "../PROJECT_STATUS.md": "PROJECT_STATUS.md",
        "../CONSTITUTION.md": "CONSTITUTION.md",
        "../PROJECT_CONSTITUTION.md": "CONSTITUTION.md",
        "../docs/DECISIONS.md": "decisions/DECISIONS.md",
        "../CHANGELOG.md": "CHANGELOG.md",
        "DECISIONS.md": "decisions/DECISIONS.md",
        "decisions/DECISIONS.md": "decisions/DECISIONS.md",
    },
    "projects/fair-crm/CONSTITUTION.md": {
        "CONSTITUTION.md": "CONSTITUTION.md",
        "architecture/ARCHITECTURE.md": "architecture/ARCHITECTURE.md",
        "integrations/INTEGRATION_WITH_CORE.md": "integrations/INTEGRATION_WITH_CORE.md",
        "import/MERGE_RULES.md": "import/MERGE_RULES.md",
        "import/IMPORT_MAPPING_STANDARD.md": "import/IMPORT_MAPPING_STANDARD.md",
        "import/IMPORT_ARCHITECTURE.md": "import/IMPORT_ARCHITECTURE.md",
        "decisions/DECISIONS.md": "decisions/DECISIONS.md",
        "docs/ARCHITECTURE.md": "architecture/ARCHITECTURE.md",
        "docs/INTEGRATION_WITH_CORE.md": "integrations/INTEGRATION_WITH_CORE.md",
    },
    "projects/fair-crm/architecture/ARCHITECTURE.md": {
        "PROJECT_STATUS.md": "../PROJECT_STATUS.md",
        "../decisions/DECISIONS.md": "../decisions/DECISIONS.md",
        "INTEGRATION_WITH_CORE.md": "../integrations/INTEGRATION_WITH_CORE.md",
        "DEV_RUNTIME.md": "../ops/DEV_RUNTIME.md",
        "../scripts/server/README.md": "../ops/SERVER_DEPLOY.md",
        "CUSTOMER_DESIGN.md": "../../../archive/fair-crm/domain/CUSTOMER_DESIGN.md",
        "FUAR_CRM_REFERENCE_ANALYSIS.md": "../../../archive/fair-crm/FUAR_CRM_REFERENCE_ANALYSIS.md",
    },
    "projects/fair-crm/decisions/DECISIONS.md": {
        "INTEGRATION_WITH_CORE.md": "../integrations/INTEGRATION_WITH_CORE.md",
        "ARCHITECTURE.md": "../architecture/ARCHITECTURE.md",
        "import/MERGE_RULES.md": "../import/MERGE_RULES.md",
        "import/IMPORT_ARCHITECTURE.md": "../import/IMPORT_ARCHITECTURE.md",
        "import/MATCHING_RULES.md": "../import/MATCHING_RULES.md",
        "import/SOURCE_ADAPTER_FRAMEWORK.md": "../import/SOURCE_ADAPTER_FRAMEWORK.md",
        "import/IMPORT_MAPPING_STANDARD.md": "../import/IMPORT_MAPPING_STANDARD.md",
        "PROJECT_STATUS.md": "../PROJECT_STATUS.md",
        "PRODUCT_VISION.md": "../VISION.md",
        "CONSTITUTION.md": "../CONSTITUTION.md",
        "IMPORT_MAPPING_GRID_COMPLETION.md": "../../../archive/fair-crm/reports/IMPORT_MAPPING_GRID_COMPLETION.md",
        "COMPANY_NAME_MATCHING_COMPLETION.md": "../../../archive/fair-crm/reports/COMPANY_NAME_MATCHING_COMPLETION.md",
        "IMPORT_RESUME_BULK_COMPLETION.md": "../../../archive/fair-crm/reports/IMPORT_RESUME_BULK_COMPLETION.md",
        "CUSTOMER_CLEANUP_ARCHITECTURE.md": "../maintenance/CUSTOMER_CLEANUP_ARCHITECTURE.md",
        "CUSTOMER_COMMUNICATION_PERFORMANCE.md": "../performance/CUSTOMER_COMMUNICATION_PERFORMANCE.md",
        "frontend/RESPONSIVE_UI_STANDARD.md": "../frontend/RESPONSIVE_UI_STANDARD.md",
    },
    "projects/fair-crm/decisions/KNOWN_DECISIONS.md": {
        "decisions/DECISIONS.md": "DECISIONS.md",
        "CONSTITUTION.md": "../CONSTITUTION.md",
        "PROJECT_STATUS.md": "../PROJECT_STATUS.md",
        "AUTH_RBAC_HANDOVER.md": "../integrations/AUTH_RBAC_HANDOVER.md",
        "ARCHITECTURE_STATUS.md": "../../../archive/fair-crm/2026-07-05/ARCHITECTURE_STATUS.md",
        "INTEGRATION_WITH_CORE.md": "../integrations/INTEGRATION_WITH_CORE.md",
        "PROJECT_SNAPSHOT_2026-07-05.md": "../../../archive/fair-crm/2026-07-05/PROJECT_SNAPSHOT.md",
    },
}

for rel, pairs in FILE_MAPS.items():
    fp = ROOT / rel
    if not fp.exists():
        continue
    t = fp.read_text(encoding="utf-8", errors="replace")
    # Replace inside markdown link targets only, longest keys first
    for a in sorted(pairs.keys(), key=len, reverse=True):
        b = pairs[a]
        t = t.replace(f"]({a})", f"]({b})")
        if "#" in a:
            continue
        # also hash anchors kept separately via exact ](path) only
    fp.write_text(t, encoding="utf-8")
    print("fixed", rel)

# Broader pass for common patterns still wrong under projects/fair-crm/**
COMMON = [
    ("](docs/DECISIONS.md)", "](decisions/DECISIONS.md)"),
    ("](../docs/DECISIONS.md)", "](../decisions/DECISIONS.md)"),
    ("](PRODUCT_VISION.md)", "](../VISION.md)"),  # careful - only in decisions
]
# Fix frontend files that still point to ../decisions/decisions
for fp in (ROOT / "projects/fair-crm").rglob("*.md"):
    t = fp.read_text(encoding="utf-8", errors="replace")
    n = t.replace("decisions/decisions/", "decisions/")
    # From frontend/ folder, DECISIONS should be ../decisions/DECISIONS.md
    if fp.parent.name == "frontend":
        n = n.replace("](../DECISIONS.md)", "](../decisions/DECISIONS.md)")
        n = n.replace("](DECISIONS.md)", "](../decisions/DECISIONS.md)")
    if fp.parent.name == "import":
        n = n.replace("](../DECISIONS.md)", "](../decisions/DECISIONS.md)")
    if n != t:
        fp.write_text(n, encoding="utf-8")

# Scan again
broken = []
scan_roots = [ROOT / "ecosystem", ROOT / "projects", ROOT / "standards", ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CONTRIBUTING.md"]
files = []
for r in scan_roots:
    if r.is_file():
        files.append(r)
    else:
        files.extend(r.rglob("*.md"))
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
for b in broken[:80]:
    print(b)
