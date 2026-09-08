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

The final production-shaped certification runs FAIR CRM against real KYROX Core and Core's SMTP adapter, using a memory-only SMTP sink for action-email capture. It verifies signup → activation → login → forgot/reset → login → password change → login, rejects activation/reset token replay, and proves pre-credential-change access/refresh sessions fail after reset/change.

The existing Super Admin `/admin/system/users` manual user-creation flow and administrator-supplied password mode remain supported. No setup-link mode was added because Core does not yet expose an approved setup-token contract. Password hashing, password policy, activation/reset token authority, identity email and credential mutation remain in Core.

### P0.2 OL-05 destructive organization authority — DONE 2026-09-03

OL-05 is accepted and cross-repository certified. Organization suspend/closure/destructive lifecycle execution remains Platform SuperAdmin / SYSTEM authority only; OrganizationAdmin cannot directly execute it or obtain the required SYSTEM lifecycle permission through an organization role.

Completion evidence:

- KYROX Core PR #21 certified lifecycle endpoint authorization behavior and added audit evidence for successful organization suspend/delete transitions.
- KYROX Core PR #22 certified that SYSTEM-scope lifecycle permissions cannot be assigned to organization-role templates, including by Platform SuperAdmin.
- FAIR CRM current-main verification found no alternate product-owned suspend/delete authority that widens the Core boundary.
- Canonical completion tracker: [../../ecosystem/P0_2_OL_05_IMPLEMENTATION.md](../../ecosystem/P0_2_OL_05_IMPLEMENTATION.md).

**Scope boundary:** OL-05 certifies destructive lifecycle authority only. Core delete remains a Core soft-delete/tombstone; product-data offboarding semantics remain later OL-08 scope.

### P0.2 OL-06 organization reactivation — DONE 2026-09-04

OL-06 is accepted and cross-repository certified. Organization reactivation remains Platform SuperAdmin / SYSTEM authority only and is valid only as canonical Core `SUSPENDED -> ACTIVE` for a non-deleted organization.

Completion evidence:

- Core PR #23 added `identity.organizations.reactivate`, `POST /organizations/{organization_id}/reactivate` and audit evidence,
- only a non-deleted `SUSPENDED` organization may transition to `ACTIVE`,
- Core PR #23 final head `655b61155e0ad799d7381d21858c9fd1d5b3a0f7` passed CI #88 and merged as `f24089cbb29f38b42270d0d9edb2235aa7815719`,
- FAIR CRM required no alternate OL-06 runtime.

Canonical completion tracker: [../../ecosystem/P0_2_OL_06_IMPLEMENTATION.md](../../ecosystem/P0_2_OL_06_IMPLEMENTATION.md).

### P0.2 OL-07 suspension job/provider behavior — DONE 2026-09-07

OL-07 is accepted and cross-repository certified. FAIR CRM consumes the Core-owned product lifecycle snapshot and deterministically handles queued work, running work, outbound provider handoff, ambiguous in-flight mail outcomes and later organization reactivation.

Completion evidence:

- **OL07-03:** Core PR #25 + FAIR CRM PR #249 established lifecycle snapshot + fail-closed guard.
- **OL07-04:** FAIR CRM PR #250 terminalizes suspension-blocked queued/pending work before start.
- **OL07-05:** FAIR CRM PR #251 cooperatively stops covered running work at safe checkpoints.
- **OL07-06:** FAIR CRM PR #252 blocks new SMTP/provider handoff after suspension is observed.
- **OL07-07:** FAIR CRM PR #253 durably persists `SENDING`, recovers checkpoint-commit failure safely and makes ambiguous provider/SMTP outcomes terminal non-auto-retry.
- **Final reactivation/resumption:** FAIR CRM PR #254 proves reactivation does not resurrect terminalized work and permits only fresh/safely deferred work. Development Standard Gate #700 and Prod-Path E2E #264 passed the final head before merge.

Canonical completion tracker: [../../ecosystem/P0_2_OL_07_IMPLEMENTATION.md](../../ecosystem/P0_2_OL_07_IMPLEMENTATION.md).

### P0.2 OL08-01 non-destructive closure orchestration — DONE 2026-09-07

OL08-A is accepted and OL08-01 is implementation/certification complete.

Delivered runtime:

- FAIR CRM-owned durable organization closure execution + append-only event evidence,
- migration `0077_organization_closure_executions`,
- SYSTEM-authorized start/status/retry,
- live Core `SUSPENDED` precondition,
- same-key idempotency + DB-enforced one-open-execution race protection,
- explicit blocked/retry evidence on the same execution,
- cross-organization denial in the canonical tenant-isolation registry,
- no closure-complete/tombstone-ready state and no Core delete call.

Evidence:

- FAIR CRM PR #255 final head `aa34cd3e5d00ec6f7d6b7adaad4afa950319830e`,
- Development Standard Gate #707 / run `34155567277`: success,
- Prod-Path E2E #270 / run `34155567315`: success,
- FAIR CRM merge `e47d4ffced9f963fd06bc263996d2d5d95e7c5f2`,
- Platform PR #36 / Platform Standards CI #104 completed cross-repository certification and merged as `f08f3a334c56c3c1be31694af56bf65330e44fe9`.

Canonical tracker: [../../ecosystem/P0_2_OL_08_IMPLEMENTATION.md](../../ecosystem/P0_2_OL_08_IMPLEMENTATION.md).

### P0.2 OL08-B closure-export technical contract — PARTIALLY ACCEPTED 2026-09-07

The accepted architecture is a policy-conditioned, organization/execution-scoped export contract with a versioned completeness manifest.

Accepted:

- `required` / `not_required` disposition model; missing/unknown fails closed,
- no runtime `not_required` success until a separately accepted policy source exists,
- explicit v1 structured-data completeness registry,
- hard exclusion of reusable provider/security credentials,
- Core identity kept outside FAIR CRM export ownership,
- generated/binary artifacts deferred to OL08-E,
- initial control remains Platform SuperAdmin / SYSTEM/operator-only,
- no export-planning state opens an irreversible cleanup/tombstone gate.

Detailed decision: [../../ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md](../../ecosystem/P0_2_OL_08_B_EXPORT_DECISION.md).

#### OL08-02 closure quiescence certification — DONE 2026-09-08

FAIR CRM PR #256 certified that an open closure execution remains governed by the existing OL-07 queued/running/provider/lifecycle guards. The certification also fixed the closure start parent/event FK flush ordering without adding an intermediate commit or new cancellation framework.

#### OL08-03A export manifest/completeness planner — DONE 2026-09-08

FAIR CRM PR #257 implemented the bounded non-destructive planner authorized by OL08-B after OL08-02:

- durable export-plan identity tied to organization + closure execution + schema version,
- versioned manifest metadata,
- explicit structured-data class registry,
- organization-scoped record planning/counting,
- deterministic record-ID-only fingerprints,
- included/excluded/deferred reason evidence,
- hard secret-source exclusion,
- SYSTEM-only planning/status metadata API,
- idempotency, tenant-isolation and audit evidence.

No persistent/downloadable package, customer-facing handover, `not_required` success, `integrity_verified` irreversible gate, provider revoke/secret purge, organization-wide data/artifact deletion/anonymization, cleanup-complete/tombstone-ready state or Core tombstone was added.

### P0.2 OL08-C provider credential disposition — ACCEPTED 2026-09-08

Platform PR #41 accepted the bounded credential-only contract. The accepted architecture separates outbound disablement, provider-side invalidation, local reusable send-secret zeroization and webhook signing-secret drain/final purge.

#### OL08-04A credential disposition state/evidence foundation — DONE / CERTIFIED 2026-09-08

FAIR CRM PR #258 implements the first bounded runtime slice:

- migration `0079_closure_credential_dispositions`,
- durable organization + closure-execution + email-account credential disposition rows,
- append-only non-secret credential evidence,
- SYSTEM-only start/list/get/retry/reconcile,
- live Core `SUSPENDED` fail-closed mutation precondition,
- outbound account eligibility disabled before credential destruction,
- generic SMTP reusable password classified `operator_required`,
- local SMTP password zeroization only after explicit external invalidation evidence,
- current-model MailerSend API tokens classified `supported_unidentifiable` and kept blocked,
- operator evidence cannot override supported-but-unidentifiable MailerSend credentials,
- unverified MailerSend target metadata cannot authorize provider deletion/local token purge,
- webhook signing secret may remain explicitly `receive_only_pending`.

Evidence:

- FAIR CRM PR #258 final head `ea12e43f0ba0066842630208217d27962fdde53c`,
- Development Standard Gate #719 / run `34194802163`: success,
- Prod-Path E2E #279 / run `34194802141`, final attempt 2: success,
- FAIR CRM merge `f5fb4ad18165848ae632b71496a5e5d1cb7a403b`,
- Platform PR #42 final head `7d3de63c8072b908d8d3c2c38a3a386af22e3921`,
- Platform Standards CI #116 / run `34196046348`: success,
- Platform merge `144ee611c1f061d10ec36c4713b08262a1465bf1`.

This is **not full OL08-C completion**. Current-model MailerSend credentials must remain fail-closed until deterministic exact-token targeting exists, and final webhook signing-secret zeroization remains dependent on an accepted drain criterion. Any time-based drain duration remains OL-09.

#### Active lifecycle decision-readiness — OL-09 retention / grace

The next safe lifecycle work is policy/readiness, not destructive runtime.

Canonical readiness: [../../ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md](../../ecosystem/P0_2_OL_09_RETENTION_GRACE_DECISION_READINESS.md).

Recommended first decisions:

- **OL09-A:** closure grace/reversibility and authoritative clock origin,
- **OL09-B:** webhook receive-only drain criterion.

Readiness alone does not select a duration and authorizes no runtime. No purge/delete worker or timer should be implemented until the applicable subsection is explicitly accepted.

Still blocked:

- persistent/downloadable closure package and its retention/expiry lifecycle,
- `not_required` success without accepted policy,
- deterministic completion of current-model MailerSend credentials without exact targeting,
- final webhook signing-secret purge before its accepted drain criterion,
- organization-wide data/artifact deletion/anonymization,
- retention/grace duration execution,
- backup ageing/restore reconciliation,
- `cleanup_complete` / `ready_for_tombstone`,
- Core tombstone.

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

In particular, the current implementation includes quotation-related capabilities and a cost catalog track that was missing from the old roadmap documentation. Its existing code, migrations, permissions, tests and UI/API state must be reflected accurately; do not redesign or duplicate it from stale planning notes.

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
