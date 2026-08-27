# FAIR CRM Roadmap

Canonical **future-work / active-work queue** for FAIR CRM. Current delivered truth belongs in [PROJECT_STATUS.md](PROJECT_STATUS.md); completed history belongs in [CHANGELOG.md](CHANGELOG.md). Detailed backlog documents may support this roadmap but must not become competing work queues.

## Cross-cutting SaaS readiness

FAIR CRM participates in the canonical cross-repository [KYROX SaaS Readiness Roadmap](../../ecosystem/SAAS_ROADMAP.md). Every material FAIR CRM change follows the shared SaaS-impact, tenant-isolation, authorization-scope and runtime-acceptance gates even when the concrete SaaS roadmap item is not itself active product work.

The SaaS roadmap is not a second FAIR CRM backlog. When a concrete SaaS item becomes active for FAIR CRM, promote that task into this file with approved scope/ownership before implementation.

### P0.1 Tenant Isolation Certification — DONE

P0.1 is complete. The detailed certification record and final adversarial matrix are preserved in [P0.1 Tenant Isolation Certification](backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md).

The first hardening wave (TI-01 through TI-06 plus additional derived-reference findings) merged through FAIR CRM PR #82. TI-07 export/download/artifact ownership closed through FAIR CRM #83, TI-08 Platform Super Admin isolation closed through Core #11, and TI-09 final adversarial certification closed through FAIR CRM #84. The final TI-09 head passed Development Standard Gate #268 and Prod-Path E2E #140 before merge.

P0.1 completion is a certification baseline, not an exemption: future organization-owned changes still require the applicable SaaS-impact and cross-organization regression evidence.

### P0.2 Identity / SaaS onboarding bridge + UI — ACTIVE, CORE-DEPENDENT

The identity/onboarding subset of ADR-0006 was approved on 2026-08-27. Core owns the identity runtime; FAIR CRM owns only the product transport bridge and user-facing screens.

Canonical implementation tracker: [../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md](../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md)

FAIR CRM scope, after the dependent Core APIs are implemented/certified:

- extend the existing Core auth client with signup, activation, forgot/reset and authenticated change-password calls,
- expose thin `/api/v1/auth/*` bridge routes using the existing login/refresh/logout transport pattern,
- add `/signup`, `/activate`, `/forgot-password`, `/reset-password` public screens,
- add authenticated account/security password-change UI,
- add login links for account creation and password recovery,
- preserve the existing Super Admin `/admin/system/users` manual user-creation flow,
- preserve admin-supplied manual passwords,
- optionally add a second "send setup link" user-creation mode only after the Core setup-token contract exists,
- keep password hashing, activation/reset tokens, identity email and credential authority out of FAIR CRM,
- verify the real flow with the permanent ABC ↔ XYZ tenant-isolation system gate plus applicable Development Standard and Prod-Path E2E gates.

The FAIR CRM portion must not start by inventing temporary product-local signup/password infrastructure while Core dependencies are unfinished.

The remaining P0.2 suspension/closure/retention decisions are still gated and are not activated by this onboarding workstream.

## Active product-quality track

### Permission-controlled UI consistency

Audit and correct FAIR CRM frontend surfaces so effective permissions consistently control what the authenticated user can see and execute.

Canonical shared rule: [../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md](../../standards/ui/CRUD_UI_AUTHORIZATION_STANDARD.md).

Scope includes, where applicable:

- navigation and module entry points,
- direct routes,
- list toolbar actions,
- row/detail actions,
- create/edit/delete controls,
- non-CRUD actions such as send/execute/restore when they have explicit permissions.

UI hiding is not security; backend authorization remains authoritative. The work is complete only when UI gating and backend denial behavior agree with effective permissions.

## Documentation/status reconciliation

The codebase has advanced beyond the previous July roadmap/status snapshot. Before declaring new product sequencing, reconcile existing implemented capabilities with current project status and changelog.

In particular, the current implementation includes quotation-related capabilities and a **cost catalog** track that was missing from the old roadmap documentation. Its existing code, migrations, permissions, tests and UI/API state must be reflected accurately in `PROJECT_STATUS.md` / `CHANGELOG.md`; do not redesign or duplicate it from stale planning notes.

## Planned product behavior

### Operation Engine — pause vs cancel

Current `Durdur` behavior cancels an operation. Planned behavior:

- `Durdur` pauses instead of cancelling,
- lifecycle supports `running → paused → running`,
- a separate `İptal Et` action moves the operation to `cancelled`,
- paused operations preserve progress, logs and intermediate state,
- `Devam Ettir` resumes from the preserved point.

This is a product behavior change and requires backend lifecycle, handler capability, UI, permission and real-runtime acceptance alignment before completion.

## Deferred / detailed backlog

The following detailed documents are supporting backlog specifications. They are not separate sources of roadmap priority:

- [P0.1 Tenant Isolation Certification](backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md) — completed certification record for the P0.1 SaaS gate.
- [Email Communication Preferences](backlog/EMAIL_COMMUNICATION_PREFERENCES.md)
- [Mail Send Operations Backlog](backlog/MAIL_SEND_OPERATIONS_BACKLOG.md)
- [MailerSend Provider Remaining Work](backlog/PROVIDER_MAILERSEND_REMAINING.md)

When one of these becomes active work, promote the item into this roadmap and keep the detailed document only as supporting specification. When completed or superseded, update status/changelog and archive the obsolete backlog document.

## Planning rule

Do not infer a new “next sprint” from old sprint numbers or stale status text. New ordering is recorded here only after an explicit product decision. Reusable rules belong under `../../standards/`; Fair CRM-specific behavior belongs in this project tree.
