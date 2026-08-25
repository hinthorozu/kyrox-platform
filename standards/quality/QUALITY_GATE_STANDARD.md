# KYROX Quality Gate Standard

**Status:** Canonical shared KYROX standard  
**Scope:** KYROX implementation repositories using automated tests, builds, governance checks or machine-readable quality contracts  
**Audience:** Human developers, AI agents, reviewers and CI tooling

The goal is strict and monotonic:

> **New work must never make the verified quality state worse, and known legacy debt must move toward zero.**

## 1. Strict green is the target

The desired repository state is always zero known failures/violations across every applicable quality surface.

A baseline is not permission to keep failures. It is a temporary migration mechanism for debt that demonstrably existed before enforcement was introduced.

The target baseline size is always `0`.

## 2. Distinguish strict PASS from zero-new-regression PASS

### Strict green PASS

All applicable checks pass and no known baseline debt remains.

### Zero-new-regression PASS with known debt

No new regression exists, but an explicitly recorded legacy baseline remains.

Reports must say that debt remains. Never report “all tests passed” when the underlying suite still contains baseline failures.

## 3. Baseline admission

A baseline may be introduced only when all are true:

1. enforcement is being introduced/expanded over an existing non-green area,
2. findings demonstrably predate the current change,
3. exact findings are recorded machine-readably where practical,
4. provenance is recorded when useful,
5. target remains zero,
6. baseline is treated as technical debt, not accepted product behavior.

Never add a newly introduced regression to a baseline merely to make CI green.

## 4. Monotonic baseline

Once a baseline exists:

```text
current_baseline ⊆ previous_baseline
```

It may shrink or become empty. It may not grow, swap old debt for new debt, hide infrastructure/collection failures, or legalize a security/authorization regression.

Any new failure outside the previous baseline is a hard failure.

### SaaS/security findings are not normal baseline debt

A newly introduced finding that weakens a SaaS security boundary is always a hard failure and must not be baseline-admitted merely to restore green CI.

Examples include:

- cross-organization data access or resource-existence leakage,
- missing organization scoping on an organization-owned query/mutation/job,
- SYSTEM permission becoming assignable/effective for an organization role contrary to governance,
- protected backend behavior relying only on hidden UI,
- development bypass/fallback identity becoming production authority,
- secrets/tokens/credentials exposed in committed config, logs or audit payloads,
- product/Core boundary violations that bypass the approved public integration contract,
- client-only entitlement/quota enforcement when the backend must enforce it.

If such a defect demonstrably predates the current enforcement work, it may be tracked as explicit security debt only through an approved remediation decision; the current change must not worsen or reproduce it elsewhere, and the system must not be described as SaaS-safe in that area until remediated.

## 5. Full applicable checks still run

A baseline does not justify skipping the complete applicable suite.

Typical semantics:

```text
0 failures
-> strict PASS

failures are a subset of known baseline
-> zero-new-regression PASS, debt explicitly reported

any failure outside baseline
-> FAIL

non-zero execution without trustworthy parseable findings
-> FAIL as infrastructure/collection error
```

## 6. Resolved debt must be removed

When a baseline finding stops reproducing and stability is confirmed, remove it. Do not retain stale entries “just in case”; oversized baselines weaken regression detection.

## 7. Same principle applies across quality surfaces

The monotonic rule applies to backend tests, frontend tests, static/governance inventories, accessibility/design-system violations and other machine-detectable debt.

A legacy violation in one part of a repository does not authorize a new equivalent violation elsewhere.

## 8. Applicability remains authoritative

Not every feature runs every quality surface. Required checks are determined by the canonical [Feature Applicability Standard](../development/FEATURE_APPLICABILITY_STANDARD.md) and the approved feature contract.

A check may be N/A because the feature does not touch that surface; it may not be N/A because the check is inconvenient or failing.

SaaS-impact classification follows the same rule: affected organization/security/entitlement/usage/lifecycle/runtime dimensions require evidence; unaffected dimensions are N/A with a reason and must not trigger speculative infrastructure work.

## 9. Green CI is not the whole acceptance contract

Automated checks are necessary evidence, but they cannot claim to prove properties they do not exercise.

For security/runtime-sensitive work:

- organization isolation may require cross-organization API/runtime tests,
- authorization-sensitive work may require real login/JWT → Core authorization → product API evidence,
- UI work requires real render/runtime acceptance where defined by the product standard,
- quota/idempotency behavior may require concurrent/retry tests,
- production security configuration may require runtime/environment verification.

Therefore:

```text
CI green
!= automatically DONE
```

when an applicable production-shaped SaaS acceptance path remains unverified or failing.

Canonical completion semantics are defined by the [Feature Delivery Standard](../development/FEATURE_DELIVERY_STANDARD.md) and the [SaaS Readiness Roadmap](../../ecosystem/SAAS_ROADMAP.md).

## 10. Gate changes must test themselves

Changes to CI workflow logic, validators, governance schemas, baseline metadata or quality scripts must trigger the checks necessary to validate those changes. A checker must not have a blind spot where editing the checker avoids running it.

Exact paths are repository implementation details.

## 11. Diagnostic evidence

Failed long-running checks should retain enough short-lived diagnostic evidence to understand the failure without guessing. Artifacts/logs must not contain secrets and do not alter pass/fail semantics.

## 12. Branch protection boundary

CI can detect a failure, but CI alone does not prevent a direct push to an unprotected branch. Hard merge enforcement requires repository rules/branch protection that require the canonical checks.

Do not claim “CI blocks merge/push” unless repository protection actually requires the checks.

A failed protected-branch/main run is a broken-main condition and must be corrected even if the push technically succeeded.

## 13. Completion reporting

Reports must describe the observed state precisely.

Examples:

```text
Strict PASS: all applicable checks green; known baseline = 0; applicable SaaS/runtime acceptance complete.
```

```text
Zero-new-regression PASS: 0 new failures; known legacy baseline remains; target = 0.
```

```text
IMPLEMENTED, NOT ACCEPTED: automated checks green, but an applicable runtime/SaaS acceptance path is still unverified or failing.
```

```text
FAIL: new failure outside accepted legacy baseline.
```

Never collapse these states into the same phrase.

## Golden quality rule

**A baseline can preserve visibility of yesterday’s debt while preventing tomorrow’s regression; it can never legalize new debt, and green CI can never substitute for an applicable SaaS/security/runtime acceptance gate.**

Product/repository extensions may define exact baseline files, workflow names and quality commands; they must not weaken these shared semantics.
