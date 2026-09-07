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

**Scope boundary:** OL-05 certifies destructive lifecycle **authority only**. Core delete remains a Core soft-delete/tombstone. OL-06 reactivation and OL-07 suspension job/provider behavior are separately certified; later closure/export/retention/delete semantics remain OL-08 through OL-10 scope.

### P0.2 OL-06 organization reactivation — DONE 2026-09-04

OL-06 is accepted and cross-repository certified. Organization reactivation remains Platform SuperAdmin / SYSTEM authority only and is valid only as the canonical Core `SUSPENDED -> ACTIVE` transition for a non-deleted organization.

Completion evidence:

- KYROX Core PR #23 added `identity.organizations.reactivate` as a SYSTEM-scoped, non-assignable permission and exposed `POST /organizations/{organization_id}/reactivate`.
- The Core implementation reuses the existing domain transition, emits `identity.organization.reactivated` audit evidence and rejects `ACTIVE`, `PENDING_ACTIVATION`, `ARCHIVED` and soft-deleted/tombstoned source states.
- Core PR #23 final head `655b61155e0ad799d7381d21858c9fd1d5b3a0f7` passed CI #88 and was squash-merged to Core `main` as `f24089cbb29f38b42270d0d9edb2235aa7815719`.
- FAIR CRM current-main verification found no alternate product-owned organization reactivation/suspension authority. No FAIR CRM runtime change was required for OL-06.
- Canonical completion tracker: [../../ecosystem/P0_2_OL_06_IMPLEMENTATION.md](../../ecosystem/P0_2_OL_06_IMPLEMENTATION.md).

**Scope boundary:** OL-06 restores only canonical Core organization lifecycle state. Product-side suspension/reactivation job/provider semantics are defined and certified by OL-07; closure/offboarding behavior remains OL-08 through OL-10 scope.

### P0.2 OL-07 suspension job/provider behavior — DONE 2026-09-07

OL-07 is accepted and cross-repository certified. FAIR CRM consumes the Core-owned product lifecycle snapshot and deterministically handles queued work, running work, outbound provider handoff, ambiguous in-flight mail outcomes and later organization reactivation.

Completion evidence:

- **OL07-03:** Core PR #25 + FAIR CRM PR #249 established the public lifecycle snapshot contract and fail-closed FAIR CRM lifecycle guard.
- **OL07-04:** FAIR CRM PR #250 terminalizes suspension-blocked queued/pending organization-owned work before start.
- **OL07-05:** FAIR CRM PR #251 cooperatively stops already-running covered work at safe checkpoints and terminalizes it as cancelled.
- **OL07-06:** FAIR CRM PR #252 re-checks lifecycle immediately before real SMTP/provider handoff, preventing new external side effects after suspension is observed while preserving encrypted provider configuration.
- **OL07-07:** FAIR CRM PR #253 durably persists `SENDING` before provider handoff, safely recovers the SQLAlchemy session on checkpoint-commit failure before any provider call, and makes ambiguous provider/SMTP handoff outcomes terminal non-auto-retry.
- **Final reactivation/resumption certification:** FAIR CRM PR #254 proves Core `SUSPENDED -> ACTIVE` does not resurrect suspension-cancelled jobs/runs/mail, permits fresh/new work, permits non-terminal work deferred only by lifecycle-authority outage once authority returns `ACTIVE`, preserves provider credentials without lifecycle re-enable, and keeps ambiguous provider handoff non-auto-retry. Development Standard Gate #700 and Prod-Path E2E #264 passed the final head before merge.
- Canonical completion tracker: [../../ecosystem/P0_2_OL_07_IMPLEMENTATION.md](../../ecosystem/P0_2_OL_07_IMPLEMENTATION.md).

**Scope boundary:** OL-07 does not authorize closure/export/retention/anonymization/delete sequencing, provider credential revocation for closure, retention/grace periods or backup restore policy. Those remain OL-08 through OL-10 decision scope.

### P0.2 OL08-01 non-destructive closure orchestration — IMPLEMENTED / CERTIFICATION PENDING 2026-09-07

OL08-A is accepted narrowly and authorizes only the non-destructive closure execution/state-machine slice. FAIR CRM PR #255 implements that runtime and has merged; Platform cross-repository certification/docs sync remains the final OL08-01 step.

Delivered runtime:

- FAIR CRM-owned durable organization closure execution and append-only event evidence,
- migration `0077_organization_closure_executions`,
- SYSTEM-authorized start/status/retry using the existing Core destructive organization authority boundary,
- live Core `SUSPENDED` precondition for start/retry,
- same-key idempotency plus DB-enforced one-open-execution race protection,
- explicit blocked/retry evidence on the same execution,
- cross-organization denial registered in the canonical tenant-isolation registry,
- no closure-complete/tombstone-ready state and no Core delete call.

Verification evidence:

- FAIR CRM PR #255 final head `aa34cd3e5d00ec6f7d6b7adaad4afa950319830e`,
- Development Standard Gate #707 / run `34155567277`: success,
- Prod-Path E2E #270 / run `34155567315`: success,
- merged to FAIR CRM `main` as `e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`.

Canonical tracker: [../../ecosystem/P0_2_OL_08_IMPLEMENTATION.md](../../ecosystem/P0_2_OL_08_IMPLEMENTATION.md).

**Next gate after OL08-01 certification:** **OL08-B — closure export obligation/contract.** OL08-B remains OPEN and must be explicitly accepted before export work begins. OL08-C through OL08-G, OL-09 retention/grace and OL-10 backup/restore also remain gated. No provider secret destruction, product-data/artifact deletion/anonymization or Core tombstone is authorized by OL08-01.

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
