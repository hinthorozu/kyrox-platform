# Tenant Isolation System Test Standard

**Status:** Canonical shared KYROX quality standard  
**Scope:** Every product module that owns, reads, mutates, exports, downloads or executes against organization-scoped data  
**Parent rules:** `FEATURE_DELIVERY_STANDARD.md`, `QUALITY_GATE_STANDARD.md`, `ecosystem/SAAS_ROADMAP.md`

## Purpose

P0.1 certification is not a one-time security snapshot. The ABC ↔ XYZ organization boundary is a permanent regression contract for all future organization-scoped work.

`organization` is the canonical account/data boundary. Tenant isolation answers **whose data** an actor may access; RBAC answers **what action** the actor may perform. A permission grant never authorizes a normal organization user to cross the organization boundary.

## Mandatory baseline

For every organization-scoped module, the automated test suite must prove at least the applicable baseline below:

```text
Organization ABC actor -> ABC resource: ALLOW when otherwise authorized
Organization XYZ actor -> ABC resource ID: DENY / not exposed
Organization ABC actor -> XYZ resource ID: DENY / not exposed
```

The rule is symmetric. ABC may not access XYZ and XYZ may not access ABC.

Platform Super Admin is the explicit platform-wide exception and is tested separately according to the canonical Core/Super-Admin contract. A normal user or OrganizationAdmin must never be able to self-assert that exception through headers, query parameters, request bodies or resource identifiers.

## Required adversarial cases

Each module must implement the cases that its API/data/execution model exposes. N/A requires an architectural reason; applicable cases may not be omitted.

- own-organization happy path,
- direct foreign resource UUID/ID,
- foreign parent/child or derived-reference IDs,
- cross-organization source/target mutation,
- mixed-organization bulk IDs,
- organization spoofing through body/query/header input,
- missing trusted organization context,
- background `{organization_id, entity_id/job_id/run_id}` mismatch,
- foreign retry/cancel/status/heartbeat where jobs expose those operations,
- foreign export/download/file/artifact IDs,
- foreign provider/account/configuration IDs,
- corrupt or cross-linked persisted references,
- organization context on audit/job/event side effects.

The lowest reliable layer must enforce tenant scope. Route/UI filtering alone is not sufficient evidence.

## Permanent system-regression gate

Every product with organization-scoped modules must maintain an automated repository-level system guard that:

1. discovers or otherwise inventories organization-scoped production modules,
2. requires each scoped module to register tenant-isolation test evidence,
3. fails CI when a new scoped module has no evidence,
4. permits exclusions only for modules that do not own/access organization-scoped product data and only with a durable architectural reason,
5. verifies that registered evidence resolves to executable automated tests,
6. runs as part of the normal required backend/system test gate.

Adding a new organization-scoped module and merely relying on historic P0.1 tests is forbidden. The new module must add its own applicable ABC/XYZ evidence and register it in the product's system-regression gate.

## FAIR CRM implementation contract

FAIR CRM implements this standard through:

```text
backend/tests/system/tenant_isolation_registry.py
backend/tests/system/test_tenant_isolation_governance.py
```

The system test scans `backend/app/modules/*` for production modules carrying `organization_id`. An unregistered discovered module is a CI failure. Registered evidence must resolve to executable pytest code containing organization context and a foreign/cross-organization negative boundary test.

The existing P0.1 TI-01 through TI-09 suites remain regression evidence; the system registry makes future coverage growth mandatory rather than optional.

## Pull-request / reviewer hard fail

A material change is **NOT DONE** and must not be accepted when any of the following applies:

- a new organization-scoped module is not represented in the system tenant-isolation registry,
- organization-owned access changes without applicable ABC/XYZ negative tests,
- a registry exclusion is used to avoid testing actual organization-owned data,
- a direct ID, relationship, bulk operation, export/download or async execution path can bypass organization scope,
- tests are green only because the new scoped path is not included in the tenant-isolation test contract.

This is a security/quality hard fail, not optional test debt.

## Golden rule

```text
ABC owns ABC data only.
XYZ owns XYZ data only.
ABC <-> XYZ crossing is denied for normal organization actors.
Every new organization-scoped path proves this automatically before DONE.
```
