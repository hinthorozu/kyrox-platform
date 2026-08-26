# P0.2 Organization Lifecycle Runtime Audit

- **Status:** Evidence audit — no lifecycle policy accepted by this document
- **Date:** 2026-08-26
- **Decision authority:** [ADR-0006](decisions/0006-organization-lifecycle-and-onboarding.md) remains **Proposed**
- **Roadmap gate:** P0.2 — Organization lifecycle contract and SaaS onboarding decisions

## Purpose

Record the verified current runtime behavior that the P0.2 lifecycle decision must account for. This is an evidence document, not an implementation authorization. It does not change ADR-0006 from Proposed and does not authorize Core or FAIR CRM runtime changes.

The audit deliberately separates two concerns:

1. **tenant isolation** — whether work stays inside the authoritative `organization_id`; P0.1 certification covers this,
2. **organization lifecycle** — whether work is still allowed to execute after the organization is suspended or soft-deleted.

A worker can be tenant-safe and still be lifecycle-unsafe if it continues external or mutating side effects after suspension.

## Verified behavior matrix

| Capability | Current behavior after Core organization suspension | Evidence / callsite | P0.2 implication |
| --- | --- | --- | --- |
| Core organization suspend | `SuspendOrganizationUseCase` loads the organization, applies the domain `suspend` transition and updates the Core repository. No product callback/orchestration is invoked. | `kyrox-core/backend/app/modules/identity/application/organization/suspend_organization.py` | Core status change alone cannot stop product-owned work. |
| Normal permission-protected requests | Core authorization requires an active organization, so normal organization-scoped RBAC calls are denied once the organization is suspended. | Core authorization contract already certified during P0.1/TI-08; organization routes remain scope-enforced. | New protected product requests are blocked when they reach Core authorization. |
| Existing login/session/refresh | Login/refresh currently validate identity/session state without making organization-active status the lifecycle authority. A suspended organization's tokens/session can therefore remain present even though later protected permission checks fail. | `kyrox-core` authentication flow audit performed during P0.2. | Decide whether suspend must revoke sessions/refresh tokens or whether RBAC denial alone is sufficient. |
| Adapter test scraper background run | The request is permission-checked before queueing. `AdapterTestRunJobRunner` later executes from local FAIR CRM state using `{organization_id, run_id}` and cancellation state; it does not re-check Core organization status. | `fair-crm/backend/app/modules/scraper/api/routes.py`; `.../scraper/application/adapter_test_run_job_runner.py` | A scraper already queued/running can continue after suspension unless product orchestration cancels/drains it. |
| Customer-contact enrichment | The request is permission-checked before queueing. `EnrichmentRunJobRunner` continues scanning, writing progress/artifacts and may create/analyze an import batch using local organization scope; no execution-time Core organization-active guard is present. | `fair-crm/backend/app/modules/scraper/application/enrichment_run_job_runner.py` | Suspension semantics must explicitly cancel, pause or drain enrichment and define whether partial import handoff is retained. |
| Import analyze/apply/bulk jobs | Background runner intentionally uses local organization-scoped repositories. Apply code states that permission was verified when the job was queued and uses `AllowAllAuthorizationAdapter()` during execution. Analyze/bulk execution follows the same background-job trust model. | `fair-crm/backend/app/modules/data_integration/application/import_job_runner.py` | A queued import can continue CRM mutations after suspension. P0.2 needs an execution-time lifecycle guard or deterministic suspension orchestration. |
| Operation start | `StartOperationUseCase` checks Core permission before starting/scheduling a run. | `fair-crm/backend/app/modules/operations/application/start_operation.py` | Suspension prevents a new start when Core authorization is reached. |
| Bulk-email operation after scheduling | `BulkEmailHandler` creates/schedules a product batch/job with `organization_id`. After scheduling, delivery is handled by the mail worker pipeline. The handler's cancel hook documents in-flight SMTP as not safely interruptible and is a best-effort no-op. | `fair-crm/backend/app/modules/operations/infrastructure/handlers/bulk_email_handler.py` | Policy must distinguish queued-not-sent mail from an SMTP send already in flight. |
| Mail worker / dispatcher | Worker and dispatcher use organization-scoped local records and dispatch through `EmailDeliveryService`; no execution-time Core organization-active check is present. | `fair-crm/backend/app/modules/mail_send_operations/application/process_mail_send_operations_worker.py`; `.../mail_send_operation_dispatcher.py` | A queued eligible message can still reach the provider after suspension. |
| Email account/provider credentials | Credentials/config are FAIR CRM-owned. `EmailDeliveryService` rejects deleted/inactive email accounts but does not check Core organization lifecycle status. Core suspension does not flip product `email_accounts.is_active`. | `fair-crm/backend/app/modules/email_accounts/infrastructure/persistence/models.py`; `.../email_delivery/application/email_delivery_service.py` | Secrets may remain encrypted for reactivation, but they must become unusable for outbound side effects while suspended if ADR-0006 proposal is accepted. |
| Core organization delete | Current Core delete is a Core soft-delete/tombstone operation and does not orchestrate FAIR CRM data/jobs/provider state. | ADR-0006 verified architecture and Core organization application layer. | Product retention/purge/export/provider cleanup must precede or accompany the Core tombstone according to an accepted closure policy. |
| Reactivation | The Core domain transition exists but no public organization reactivation API is currently exposed. | ADR-0006 verified architecture. | Operational suspension cannot be treated as a complete reversible lifecycle until a supported reactivation path is accepted and implemented. |

## OL-07 finding

The current system has a consistent split:

```text
request/start time
  -> Core authorization sees organization status
  -> suspended organization is denied

already queued/running FAIR CRM work
  -> product worker trusts previously established organization_id/job context
  -> tenant isolation remains intact
  -> Core organization active/suspended state is generally not re-checked
  -> work may continue until its own completion/cancel/error rules stop it
```

This means **P0.1 remains valid**: the observed workers stay organization-scoped. The issue is instead the open **P0.2 OL-07 lifecycle contract**.

## Required policy decisions exposed by the audit

ADR-0006 cannot move from Proposed to Accepted until the lifecycle owner explicitly decides at least the following:

1. **Session behavior:** revoke active sessions/refresh tokens on suspend, or allow token material to remain while every protected call is denied by organization status.
2. **Queued jobs:** whether not-yet-started jobs are cancelled, paused or retained for reactivation.
3. **Running scraper/enrichment jobs:** immediate cooperative cancellation versus bounded drain to a safe checkpoint.
4. **Import mutations:** whether an already-running import may finish a transaction/batch, must stop at the next row/checkpoint, or must roll back where possible.
5. **Queued outbound mail:** prevent provider dispatch after suspension; define terminal status for unsent items.
6. **In-flight provider calls:** define best-effort behavior because SMTP/provider sends cannot always be recalled once handed off.
7. **Provider credentials:** keep encrypted but lifecycle-disabled during suspension versus explicit account deactivation; define reactivation behavior without losing configured secrets.
8. **Audit evidence:** record the suspension transition and the deterministic disposition of affected jobs/side effects.

## Architecture constraint for implementation after acceptance

If ADR-0006 is accepted, the implementation must not make FAIR CRM query Core tables directly. The lifecycle authority remains Core and product behavior remains FAIR CRM-owned.

A production implementation should therefore use an explicit public contract, for example a product-safe organization lifecycle check/snapshot and/or auditable lifecycle orchestration/event contract. The exact mechanism remains a decision/implementation detail after acceptance.

Any execution-time guard must remain **fail-closed** for destructive or external side effects when authoritative lifecycle state cannot be established, while avoiding a design that silently turns every local row operation into an unbounded synchronous Core dependency.

## Current conclusion

- P0.1 tenant isolation: **DONE; unaffected by this audit**.
- P0.2 lifecycle: **IN DECISION / ARCHITECTURE GATE**.
- ADR-0006: **Proposed**.
- OL-07: **verified runtime gap; policy details still open**.
- Runtime lifecycle fixes: **not authorized yet**.

## Related

- [ADR-0006: Organization lifecycle and SaaS onboarding contract](decisions/0006-organization-lifecycle-and-onboarding.md)
- [KYROX SaaS Readiness Roadmap](SAAS_ROADMAP.md)
- [KYROX Ecosystem Status](STATUS.md)
