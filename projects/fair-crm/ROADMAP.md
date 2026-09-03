# FAIR CRM Roadmap

Canonical **future-work / active-work queue** for FAIR CRM. Current delivered truth belongs in [PROJECT_STATUS.md](PROJECT_STATUS.md); completed history belongs in [CHANGELOG.md](CHANGELOG.md). Detailed backlog documents may support this roadmap but must not become competing work queues.

## Cross-cutting SaaS readiness

FAIR CRM participates in the canonical cross-repository [KYROX SaaS Readiness Roadmap](../../ecosystem/SAAS_ROADMAP.md). Every material FAIR CRM change follows the shared SaaS-impact, tenant-isolation, authorization-scope and runtime-acceptance gates even when the concrete SaaS roadmap item is not itself active product work.

The SaaS roadmap is not a second FAIR CRM backlog. When a concrete SaaS item becomes active for FAIR CRM, promote that task into this file with approved scope/ownership before implementation.

### P0.1 Tenant Isolation Certification — DONE

P0.1 is complete. The detailed certification record and final adversarial matrix are preserved in [P0.1 Tenant Isolation Certification](backlog/P0_1_TENANT_ISOLATION_CERTIFICATION.md).

The first hardening wave (TI-01 through TI-06 plus additional derived-reference findings) merged through FAIR CRM PR #82. TI-07 export/download/artifact ownership closed through FAIR CRM #83, TI-08 Platform Super Admin isolation closed through Core #11, and TI-09 final adversarial certification closed through FAIR CRM #84. The final TI-09 head passed Development Standard Gate #268 and Prod-Path E2E #140 before merge.

P0.1 completion is a certification baseline, not an exemption: future organization-owned changes still require the applicable SaaS-impact and cross-organization regression evidence.

### P0.2 Identity / SaaS onboarding bridge + UI — DONE

The identity/onboarding subset of ADR-0006 was approved on 2026-08-27. Core owns the identity runtime; FAIR CRM owns only the product transport bridge and user-facing screens. That approved onboarding/credential workstream is complete as of 2026-08-29.

Canonical implementation tracker: [../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md](../../ecosystem/P0_2_IDENTITY_ONBOARDING_IMPLEMENTATION.md)

Delivered execution order:

- **CRM-BE-01 — Core auth client extensions: DONE** — FAIR CRM PR #86
- **CRM-BE-02 — thin auth bridge routes: DONE** — FAIR CRM PR #87
- **CRM-UI-01 — public signup / activation / recovery screens: DONE** — FAIR CRM PR #88
- **CRM-UI-02 — login account-creation / password-recovery integration: DONE** — FAIR CRM PR #89
- **CRM-UI-03 — authenticated account/security password-change UI: DONE** — FAIR CRM PR #90
- **CRM-UI-04 — Super Admin user-management compatibility certification: DONE** — FAIR CRM PR #91
- **Final cross-repository identity lifecycle certification: DONE** — FAIR CRM PR #92; Development Standard Gate #306 and Prod-Path E2E #151 passed the final head before merge.

The final production-shaped certification runs FAIR CRM against real KYROX Core and Core's SMTP adapter, using a memory-only SMTP sink for action-email capture. It verifies signup → activation → login → forgot/reset → login → password change → login, rejects activation/reset token replay, and proves pre-credential-change access/refresh sessions fail after reset/change. No FAIR CRM/Core application runtime or schema behavior was added by the certification PR.

The existing Super Admin `/admin/system/users` manual user-creation flow and administrator-supplied password mode remain supported. No setup-link mode was added because Core does not yet expose an approved setup-token contract. Password hashing, password policy, activation/reset token authority, identity email and credential mutation remain in Core.

### P0.2 OL-05 destructive organization authority — DONE 2026-09-03

OL-05 is accepted and cross-repository certified. Organization suspend/closure/destructive lifecycle execution remains Platform SuperAdmin / SYSTEM authority only; OrganizationAdmin cannot directly execute it or obtain the required SYSTEM lifecycle permission through an organization role.

Completion evidence:

- KYROX Core PR #21 certified lifecycle endpoint authorization behavior and added audit evidence for successful organization suspend/delete transitions.
- KYROX Core PR #22 certified that SYSTEM-scope lifecycle permissions cannot be assigned to organization-role templates, including by Platform SuperAdmin.
- FAIR CRM current-main verification found no alternate product-owned suspend/delete authority that widens the Core boundary. The organization-management UI consumes Core organization APIs; UI permission gating is UX and Core backend authorization remains authoritative.
- Canonical completion tracker: [../../ecosystem/P0_2_OL_05_IMPLEMENTATION.md](../../ecosystem/P0_2_OL_05_IMPLEMENTATION.md).

**Scope boundary:** OL-05 certifies destructive lifecycle **authority only**. Core delete remains a Core soft-delete/tombstone. OL-06 reactivation, OL-07 suspension job/provider behavior, OL-08 closure/export/retention/delete sequencing, OL-09 retention/grace durations and OL-10 backup restore implications remain separately gated.

### P0.2 OL-06 organization reactivation — DONE 2026-09-04

OL-06 is accepted and cross-repository certified. Organization reactivation remains Platform SuperAdmin / SYSTEM authority only and is valid only as the canonical Core `SUSPENDED -> ACTIVE` transition for a non-deleted organization.

Completion evidence:

- KYROX Core PR #23 added `identity.organizations.reactivate` as a SYSTEM-scoped, non-assignable permission and exposed `POST /organizations/{organization_id}/reactivate`.
- The Core implementation reuses the existing domain transition, emits `identity.organization.reactivated` audit evidence and rejects `ACTIVE`, `PENDING_ACTIVATION`, `ARCHIVED` and soft-deleted/tombstoned source states.
- Core PR #23 final head `655b61155e0ad799d7381d21858c9fd1d5b3a0f7` passed CI #88 and was squash-merged to Core `main` as `f24089cbb29f38b42270d0d9edb2235aa7815719`.
- FAIR CRM current-main verification found no alternate product-owned organization reactivation/suspension authority. No FAIR CRM runtime change was required for OL-06.
- Canonical completion tracker: [../../ecosystem/P0_2_OL_06_IMPLEMENTATION.md](../../ecosystem/P0_2_OL_06_IMPLEMENTATION.md).

**Scope boundary:** OL-06 restores only canonical Core organization lifecycle state. It does not resume queued/running product jobs, re-enable provider credentials, restart outbound mail or define other product side effects. Those semantics are the next decision gate, **OL-07**.

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
- a separate `İptal Et` action moves an operation to `cancelled`,
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
