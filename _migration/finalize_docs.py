from pathlib import Path

EXCLUDE_PARTS = {".git", "node_modules", "dist", "build", "venv", ".venv", "__pycache__"}


def list_md(root: Path):
    out = []
    for p in root.rglob("*.md"):
        if any(part in EXCLUDE_PARTS for part in p.parts):
            continue
        out.append(p)
    return out


def delete_all_md(root: Path):
    deleted = []
    for p in list_md(root):
        p.unlink()
        deleted.append(str(p.relative_to(root)).replace("\\", "/"))
    return deleted


P = Path(r"C:\Users\hinthorozuTUF\Kyrox\kyrox-platform")
F = Path(r"C:\Users\hinthorozuTUF\Kyrox\fair-crm")
C = Path(r"C:\Users\hinthorozuTUF\Kyrox\kyrox-core")

# Remove superseded platform root/legacy doc locations (content already under ecosystem/projects/archive)
legacy_platform_paths = [
    P / "STATUS.md",
    P / "ROADMAP.md",
    P / "VISION.md",
    P / "PROJECT_PHILOSOPHY.md",
    P / "KNOWN_DEFERRED.md",
    P / "CHANGELOG.md",
    P / "AI_WORKFLOW.md",
    P / "CONTRIBUTING.md",
    P / "docs/ECOSYSTEM.md",
    P / "docs/REPOSITORY_STRATEGY.md",
    P / "docs/WORKFLOW.md",
    P / "decisions/ADR_INDEX.md",
    P / "decisions/0001-repository-strategy.md",
    P / "decisions/0002-core-product-separation.md",
    P / "decisions/0003-identity-security-strategy.md",
    P / "decisions/0004-audit-service-strategy.md",
    P / "milestones/M1_FOUNDATION.md",
    P / "milestones/M2_IDENTITY.md",
    P / "milestones/M3_PLATFORM_SERVICES.md",
    P / "milestones/M4_FAIR_CRM_V1.md",
    P / "products/FAIR_CRM.md",
]
removed_platform = []
for p in legacy_platform_paths:
    if p.exists():
        p.unlink()
        removed_platform.append(str(p.relative_to(P)).replace("\\", "/"))
print("removed_platform_legacy", len(removed_platform))

# Thin CONTRIBUTING pointer
(P / "CONTRIBUTING.md").write_text(
    "# Contributing\n\n"
    "Process and contribution rules live in "
    "[ecosystem/WORKFLOW.md](ecosystem/WORKFLOW.md).\n\n"
    "Documentation ownership: "
    "[ecosystem/DOCUMENT_GOVERNANCE.md](ecosystem/DOCUMENT_GOVERNANCE.md).\n",
    encoding="utf-8",
)

fair_deleted = delete_all_md(F)
core_deleted = delete_all_md(C)

print("fair_deleted", len(fair_deleted))
print("core_deleted", len(core_deleted))

# Verify
fair_left = list_md(F)
core_left = list_md(C)
print("fair_left", len(fair_left))
print("core_left", len(core_left))
for p in fair_left + core_left:
    print("REMAINING", p)

# Required files check
required = [
    "ecosystem/ROADMAP.md",
    "ecosystem/STATUS.md",
    "ecosystem/WORKFLOW.md",
    "ecosystem/REPOSITORY_STRATEGY.md",
    "ecosystem/DOCUMENT_GOVERNANCE.md",
    "projects/fair-crm/README.md",
    "projects/fair-crm/PROJECT_STATUS.md",
    "projects/kyrox-core/README.md",
    "projects/kyrox-core/PROJECT_STATUS.md",
]
for rel in required:
    ok = (P / rel).exists()
    print("REQUIRED", rel, "OK" if ok else "MISSING")

# Write deletion manifest
manifest = P / "_migration/deletion_manifest.txt"
manifest.write_text(
    "PLATFORM_LEGACY\n"
    + "\n".join(removed_platform)
    + "\n\nFAIR_CRM\n"
    + "\n".join(fair_deleted)
    + "\n\nKYROX_CORE\n"
    + "\n".join(core_deleted)
    + "\n",
    encoding="utf-8",
)
print("manifest_written")
