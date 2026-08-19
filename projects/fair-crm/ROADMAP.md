# FAIR CRM Roadmap

Canonical **future-work / active-work queue** for FAIR CRM. Current delivered truth belongs in [PROJECT_STATUS.md](PROJECT_STATUS.md); completed history belongs in [CHANGELOG.md](CHANGELOG.md). Detailed backlog documents may support this roadmap but must not become competing work queues.

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

- [Email Communication Preferences](backlog/EMAIL_COMMUNICATION_PREFERENCES.md)
- [Mail Send Operations Backlog](backlog/MAIL_SEND_OPERATIONS_BACKLOG.md)
- [MailerSend Provider Remaining Work](backlog/PROVIDER_MAILERSEND_REMAINING.md)

When one of these becomes active work, promote the item into this roadmap and keep the detailed document only as supporting specification. When completed or superseded, update status/changelog and archive the obsolete backlog document.

## Planning rule

Do not infer a new “next sprint” from old sprint numbers or stale status text. New ordering is recorded here only after an explicit product decision. Reusable rules belong under `../../standards/`; Fair CRM-specific behavior belongs in this project tree.
