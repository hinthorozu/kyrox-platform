# KYROX System Behavior Map Standard

**Status:** Canonical shared KYROX standard  
**Scope:** User-facing actions, API-triggered behavior, scheduled/background behavior, permission-controlled operations and tenant-scoped data access  
**Audience:** Human developers, AI agents, reviewers and repository enforcement tooling

The System Behavior Map makes executable product behavior traceable from trigger to outcome without creating a second source of business truth.

Its purpose is to answer, for every material behavior:

```text
Trigger / UI surface
  -> frontend action/handler when applicable
  -> frontend API/client call when applicable
  -> HTTP route or job entry point
  -> authorization requirement
  -> organization/system scope
  -> application/use-case orchestration
  -> repository/external service/worker side effect
  -> response/result
  -> user-visible outcome when applicable
```

The map is evidence and navigation. The implementation remains runtime truth; the canonical KYROX standards remain policy truth.

## 1. Ownership and source-of-truth boundary

Human-readable reusable rules belong in `kyrox-platform`.

Application repositories own:

- machine-readable behavior inventory/configuration needed by CI,
- static extraction tooling,
- runtime/system tests,
- product-specific mappings and exceptions,
- generated reports/artifacts.

Do not copy this standard into an application repository. Cursor rules, AGENTS files and product documentation may point to it but must not redefine it.

## 2. Behavior identity

Every material behavior needs a stable identity or a deterministic machine-derived signature.

A behavior signature should be based on stable implementation semantics such as:

```text
<HTTP method> <normalized path>
<job/schedule key>
<UI route + semantic action>
```

Generated identifiers must not depend on line numbers or ephemeral build output.

## 3. Required evidence dimensions

The map separates dimensions that are often incorrectly collapsed.

### Trigger / surface

Identify where execution begins:

- navigation or page load,
- button/menu/row/detail action,
- form submit,
- direct API consumer,
- webhook,
- scheduled job,
- queue/worker/background operation,
- system/maintenance trigger.

### Frontend chain

When frontend is applicable, trace as far as tooling can prove:

```text
route/component
-> control or handler
-> API/client function
-> HTTP method/path
```

A reference to an API function is evidence of usage, but is not automatically proof of the exact visible control that invokes it.

### Backend chain

Trace:

```text
HTTP/job entry
-> guard/dependency
-> use case/service
-> repository/adapter
-> side effect/result
```

Static tooling may report unresolved links instead of guessing.

### Authorization

Record the effective backend permission/capability enforcing the action when applicable.

Frontend visibility and backend authorization are separate evidence. A matching frontend permission does not substitute for backend enforcement.

### Organization scope

Tenant isolation is separate from authorization.

For organization-owned data, evidence must show how validated organization context reaches the scoped query/mutation/job. Valid evidence can include:

- explicit `organization_id` propagation,
- an approved organization-scoped repository/session abstraction,
- another canonical enforcement mechanism whose behavior is proven by tests.

The absence of an explicit repository predicate is not, by itself, proof that isolation is missing if a canonical central scope mechanism exists. Conversely, the presence of a permission check is not proof of organization isolation.

### Result

Record what execution returns or causes:

- response/status/schema,
- persisted mutation,
- external-service call,
- emitted job/event,
- download/export,
- UI refresh/navigation/toast or other visible result when applicable.

## 4. Evidence levels

Every mapped dimension uses truthful evidence levels.

```text
DISCOVERED   machine found the implementation element
LINKED       two adjacent elements are statically connected
STATIC_VERIFIED  the required static contract is proven
RUNTIME_VERIFIED real execution proves the accepted path
UNKNOWN      tooling cannot prove the relationship yet
N/A          dimension does not apply, with architectural reason
```

`UNKNOWN` is preferable to an inferred or invented relationship.

## 5. Generated inventory vs reviewed evidence

Prefer generated inventory for facts that can be recovered deterministically from code:

- frontend API calls,
- backend routes,
- HTTP method/path matching,
- dependency/guard names,
- direct permission literals/constants,
- direct organization-context propagation,
- code references to frontend API functions,
- feature-contract linkage.

Reviewed/manual evidence is allowed only where static extraction cannot reliably recover semantics, such as dynamic dispatch, runtime adapter selection or a user-visible result whose meaning depends on domain context.

Manual evidence must identify its source and must not override contradictory executable evidence.

## 6. Monotonic coverage rule

System-map enforcement follows the canonical Quality Gate Standard.

When enforcement is introduced over an existing system, historical unresolved findings may be treated as visible migration debt. The accepted set must be monotonic:

```text
current_unresolved ⊆ previous_unresolved
```

Therefore:

- existing unresolved behavior may remain temporarily,
- existing unresolved behavior should be reduced,
- a new unmapped frontend call is a regression,
- a new route/permission mismatch is a regression,
- a new organization-scope regression is a hard failure,
- new code must not be hidden by expanding a baseline.

The target unresolved count is always `0`.

## 7. Comparison semantics

A repository may generate inventories for the PR base and current commit and compare stable finding signatures.

Typical result:

```text
base finding still exists
-> known debt, reported

base finding disappears
-> improvement

new finding appears
-> FAIL
```

Counts alone are insufficient when one defect disappears and another unrelated defect appears. Comparators should use stable finding signatures where practical.

## 8. Tenant-isolation acceptance

Static scope evidence is useful but does not replace cross-organization acceptance where the risk is material.

For organization-owned direct-resource access, mutations, exports/downloads, bulk operations and background execution, the applicable Feature Delivery/Test standards still require runtime or API evidence that another organization cannot access the resource.

A behavior map may therefore report separately:

```text
tenant_scope_static: VERIFIED
cross_org_runtime: UNKNOWN
```

This is not contradictory; it identifies exactly what remains unproven.

## 9. UI/action acceptance

For user-facing actions the desired end state is traceability such as:

```text
Customers / Archive
-> CustomersPage action
-> archiveCustomer()
-> DELETE /api/v1/customers/{customer_id}
-> fair_crm.customers.delete
-> organization scope
-> ArchiveCustomerUseCase
-> CustomerRepository
-> CustomerResponse
-> row/state refresh
```

Static tooling is not required to invent a button label or handler when JSX/dynamic composition prevents deterministic extraction. It must expose the unresolved segment so coverage work can close it deliberately.

## 10. Background and system behavior

The map is not UI-only.

Scheduled jobs, webhooks, workers, maintenance loops, lifecycle operations and platform/system-admin behavior must be represented when material. User permission may be N/A for a system trigger, while organization/system scope remains mandatory to classify.

## 11. CI integration

Application repositories should integrate behavior-map checks into their canonical development/quality gate rather than create an unrelated acceptance model.

At minimum CI should:

1. generate current inventory,
2. generate or load comparison-base inventory,
3. compare stable findings,
4. fail on new regressions,
5. retain diagnostic inventory/report artifacts when useful,
6. keep runtime/security acceptance separate where static analysis cannot prove it.

A checker change must trigger the checker itself.

## 12. AI and Cursor behavior

AI agents are developers, not authorities over acceptance.

Repository agent/Cursor rules should tell an agent to:

- read this canonical standard for material behavior changes,
- inspect the existing implementation before editing,
- update implementation/tests/contracts as applicable,
- run the repository behavior-map and quality gates,
- report unresolved evidence truthfully,
- never mark work DONE merely because generated documentation was updated.

The CI/runtime evidence decides acceptance, not the agent's claim.

## 13. Hard-fail conditions

Reject new work when applicable evidence shows:

- a frontend HTTP call has no matching backend contract without an explicit external/API reason,
- method/path drift exists between consumer and route,
- protected behavior loses backend authorization,
- frontend and backend authorization semantics diverge,
- organization-owned access loses organization scoping,
- dynamic/unresolved behavior is silently presented as verified,
- generated findings are suppressed only to restore green CI,
- the system map becomes a second normative documentation source.

## 14. Definition of Done

For a material behavior change, System Behavior Map acceptance is complete only when:

- applicable trigger/route/API links are represented,
- authorization evidence is represented,
- organization/system scope is classified,
- new static-map regressions are zero,
- applicable cross-organization/runtime evidence is complete under the Feature Delivery Standard,
- generated reports describe unresolved legacy debt honestly.

The map supplements, and never weakens, the Feature Delivery, Feature Applicability, Quality Gate, UI Authorization and tenant-isolation standards.

## Golden rule

**Generate what code can prove, test what static analysis cannot prove, mark the rest UNKNOWN, and never let new behavior make traceability or isolation coverage worse.**
