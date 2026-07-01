# Architecture Decision Records (ADR) Index

Index of architecture and ecosystem decisions for KYROX. ADRs live in this directory and are referenced from roadmap, workflow, and implementation repos.

## Format

- Filename: `NNNN-short-title.md` (zero-padded number, kebab-case title)
- Status: Proposed | Accepted | Deprecated | Superseded
- New decisions increment the number; do not renumber existing ADRs

## Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| [0001](0001-repository-strategy.md) | Repository strategy | Accepted | 2026-07-01 |
| [0002](0002-core-product-separation.md) | Core and product separation | Accepted | 2026-07-01 |
| [0003](0003-identity-security-strategy.md) | Identity security strategy | Accepted | 2026-07-01 |
| [0004](0004-audit-service-strategy.md) | Audit service strategy | Accepted | 2026-07-01 |

## Creating a new ADR

1. Copy the structure from an existing ADR in this folder.
2. Assign the next sequential number.
3. Add an entry to this index.
4. Link from relevant docs in `docs/` or `milestones/` if applicable.
5. Implement only after status is **Accepted**.
