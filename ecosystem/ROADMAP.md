# KYROX Ecosystem Roadmap

High-level milestone and direction document. **Current truth belongs in [STATUS.md](STATUS.md); product work queues belong in project roadmaps.** Do not put exact test counts, migration heads, current commit SHAs or detailed sprint histories here.

## Milestones

| Milestone | Name | Status | Document |
|-----------|------|--------|----------|
| **M1** | Foundation | Completed | [archive](../archive/milestones/M1_FOUNDATION.md) |
| **M2** | Identity Platform | Completed | [archive](../archive/milestones/M2_IDENTITY.md) |
| **M3** | Platform Services | Completed | [archive](../archive/milestones/M3_PLATFORM_SERVICES.md) |
| **M4** | FAIR CRM v1 | **Active** | [MILESTONE_M4](../projects/fair-crm/MILESTONE_M4.md) |

## M4 — FAIR CRM v1

Goal: ship and harden the first KYROX product on the reusable Core platform.

**Primary implementation repo:** `fair-crm`  
**Product status:** [projects/fair-crm/PROJECT_STATUS.md](../projects/fair-crm/PROJECT_STATUS.md)  
**Product work queue:** [projects/fair-crm/ROADMAP.md](../projects/fair-crm/ROADMAP.md)

M4 work is intentionally managed in the Fair CRM roadmap rather than duplicated here. Core changes during M4 are limited to fixes and reusable platform capabilities required by real product needs.

## Core direction during M4

Core remains product-agnostic and is not a destination for FAIR CRM domain logic. Reusable needs discovered by products may be promoted to Core only after the ownership boundary is clear and the public integration contract remains intact.

Core-specific future work: [projects/kyrox-core/ROADMAP.md](../projects/kyrox-core/ROADMAP.md).

## After M4

Indicative ecosystem direction, subject to explicit planning/ADR decisions:

- production hardening based on real product operation,
- promote proven reusable capabilities into Core when justified by more than product-specific semantics,
- deliver deferred Core capabilities when actual product demand requires them,
- add future KYROX products without duplicating shared standards or platform infrastructure.

Deferred platform items: [KNOWN_DEFERRED.md](KNOWN_DEFERRED.md).

## Related

- [STATUS.md](STATUS.md)
- [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md)
- [DOCUMENT_GOVERNANCE.md](DOCUMENT_GOVERNANCE.md)
- [WORKFLOW.md](WORKFLOW.md)
