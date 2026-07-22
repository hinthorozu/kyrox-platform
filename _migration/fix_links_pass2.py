from pathlib import Path
import re

ROOT = Path(r"C:\Users\hinthorozuTUF\Kyrox\kyrox-platform")

# Absolute-ish replacements applied to file text (order matters: longer first)
GLOBAL_REPLACEMENTS = [
    # Fair CRM old docs paths → new
    ("docs/frontend/FRONTEND_UI_MASTER_STANDARD.md", "frontend/FRONTEND_UI_MASTER_STANDARD.md"),
    ("docs/frontend/RESPONSIVE_UI_STANDARD.md", "frontend/RESPONSIVE_UI_STANDARD.md"),
    ("docs/frontend/UI_DESIGN_SYSTEM.md", "frontend/UI_DESIGN_SYSTEM.md"),
    ("docs/import/SOURCE_ADAPTER_FRAMEWORK.md", "import/SOURCE_ADAPTER_FRAMEWORK.md"),
    ("docs/import/IMPORT_ARCHITECTURE.md", "import/IMPORT_ARCHITECTURE.md"),
    ("docs/import/IMPORT_MAPPING_STANDARD.md", "import/IMPORT_MAPPING_STANDARD.md"),
    ("docs/import/MERGE_RULES.md", "import/MERGE_RULES.md"),
    ("docs/import/MATCHING_RULES.md", "import/MATCHING_RULES.md"),
    ("docs/IMPORT_RESUME_BULK_COMPLETION.md", "../../archive/fair-crm/reports/IMPORT_RESUME_BULK_COMPLETION.md"),
    ("docs/COMPANY_NAME_MATCHING_COMPLETION.md", "../../archive/fair-crm/reports/COMPANY_NAME_MATCHING_COMPLETION.md"),
    ("docs/IMPORT_MAPPING_GRID_COMPLETION.md", "../../archive/fair-crm/reports/IMPORT_MAPPING_GRID_COMPLETION.md"),
    ("docs/DEV_AUTO_START_COMPLETION.md", "../../archive/fair-crm/reports/DEV_AUTO_START_COMPLETION.md"),
    ("docs/DEV_RUNTIME.md", "ops/DEV_RUNTIME.md"),
    ("docs/DEV_RESTART_GUIDE.md", "ops/DEV_RESTART_GUIDE.md"),
    ("docs/ARCHITECTURE.md", "architecture/ARCHITECTURE.md"),
    ("docs/INTEGRATION_WITH_CORE.md", "integrations/INTEGRATION_WITH_CORE.md"),
    ("docs/LEGACY_UMCRM_MIGRATION.md", "legacy/UMCRM_MIGRATION.md"),
    ("docs/DECISIONS.md", "decisions/DECISIONS.md"),
    ("docs/KNOWN_DECISIONS.md", "decisions/KNOWN_DECISIONS.md"),
    ("docs/PRODUCT_VISION.md", "VISION.md"),
    ("PROJECT_CONSTITUTION.md", "CONSTITUTION.md"),
    ("docs/BACKEND_ARCHITECTURE_STANDARDS.md", "../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md"),
    ("BACKEND_ARCHITECTURE_STANDARDS.md", "../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md"),
    # Ecosystem old paths from ADRs / vision
    ("docs/ECOSYSTEM.md", "../REPOSITORY_STRATEGY.md"),
    ("docs/WORKFLOW.md", "../WORKFLOW.md"),
    ("docs/REPOSITORY_STRATEGY.md", "../REPOSITORY_STRATEGY.md"),
    ("../docs/ECOSYSTEM.md", "../REPOSITORY_STRATEGY.md"),
    ("../docs/WORKFLOW.md", "../WORKFLOW.md"),
    ("../docs/REPOSITORY_STRATEGY.md", "../REPOSITORY_STRATEGY.md"),
    ("../milestones/M3_PLATFORM_SERVICES.md", "../../archive/milestones/M3_PLATFORM_SERVICES.md"),
    ("milestones/M3_PLATFORM_SERVICES.md", "../archive/milestones/M3_PLATFORM_SERVICES.md"),
    ("../milestones/M4_FAIR_CRM_V1.md", "../../projects/fair-crm/MILESTONE_M4.md"),
    ("../STATUS.md", "../STATUS.md"),
    ("../ROADMAP.md", "../ROADMAP.md"),
]

# Per-directory extra replacements (relative to file parent)
PER_DIR = {
    "projects/fair-crm": [
        ("../PROJECT_STATUS.md", "PROJECT_STATUS.md"),
        ("../PROJECT_CONSTITUTION.md", "CONSTITUTION.md"),
        ("../CONSTITUTION.md", "CONSTITUTION.md"),
        ("../docs/DECISIONS.md", "decisions/DECISIONS.md"),
        ("../CHANGELOG.md", "CHANGELOG.md"),
        ("DECISIONS.md", "decisions/DECISIONS.md"),
    ],
    "projects/fair-crm/decisions": [
        ("../ARCHITECTURE.md", "../architecture/ARCHITECTURE.md"),
        ("../PRODUCT_VISION.md", "../VISION.md"),
        ("../PROJECT_STATUS.md", "../PROJECT_STATUS.md"),
        ("../frontend/", "../frontend/"),
    ],
    "projects/kyrox-core": [
        ("docs/BACKEND_ARCHITECTURE_STANDARDS.md", "../../standards/backend/BACKEND_ARCHITECTURE_STANDARDS.md"),
        ("docs/PRODUCT_INTEGRATION_GUIDE.md", "integrations/PRODUCT_INTEGRATION_GUIDE.md"),
        ("docs/ROADMAP.md", "ROADMAP.md"),
        ("KYROX_CORE_ARCHITECTURE.md", "../../archive/kyrox-core/KYROX_CORE_ARCHITECTURE.md"),
    ],
    "ecosystem": [
        ("docs/ECOSYSTEM.md", "REPOSITORY_STRATEGY.md"),
    ],
}

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def apply_repls(text: str, pairs):
    for a, b in pairs:
        text = text.replace(a, b)
    return text


def fix_file(fp: Path):
    rel = fp.relative_to(ROOT).as_posix()
    text = fp.read_text(encoding="utf-8", errors="replace")
    orig = text
    text = apply_repls(text, GLOBAL_REPLACEMENTS)
    for prefix, pairs in PER_DIR.items():
        if rel.startswith(prefix + "/") or rel == prefix or rel.startswith(prefix):
            # only apply when file under that tree
            if rel == prefix or rel.startswith(prefix + "/"):
                text = apply_repls(text, pairs)
    if text != orig:
        fp.write_text(text, encoding="utf-8")
        return True
    return False


changed = 0
for fp in ROOT.rglob("*.md"):
    if "_migration" in fp.parts:
        continue
    if fix_file(fp):
        changed += 1
print("files_changed", changed)

# Second pass: resolve remaining broken relative links with heuristics
broken = []
for fp in list((ROOT / "ecosystem").rglob("*.md")) + list((ROOT / "projects").rglob("*.md")) + list(
    (ROOT / "standards").rglob("*.md")
) + [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CONTRIBUTING.md"]:
    text = fp.read_text(encoding="utf-8", errors="replace")
    for m in LINK_RE.finditer(text):
        url = m.group(2).strip()
        if url.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path_part = url.split("#", 1)[0]
        if not path_part:
            continue
        target = (fp.parent / path_part).resolve()
        if not target.exists():
            broken.append((fp.relative_to(ROOT).as_posix(), path_part))

print("broken_after", len(broken))
for b in broken[:60]:
    print(f"{b[0]} -> {b[1]}")
