# FAIR CRM — Quality Gate Extension

**Status:** Binding Fair CRM repository extension  
**Canonical shared rule:** [../../standards/quality/QUALITY_GATE_STANDARD.md](../../standards/quality/QUALITY_GATE_STANDARD.md)

Fair CRM inherits the shared KYROX Quality Gate Standard unchanged. This file defines only Fair CRM-specific quality metadata and enforcement surfaces. It must not weaken strict-green, zero-new-regression, monotonic-baseline or truthful-reporting semantics.

## 1. Backend legacy-baseline metadata

Fair CRM stores backend known-failure governance metadata at:

```text
.kyrox/backend-test-baseline.json
```

The baseline records exact pytest node IDs and exists only to represent demonstrably pre-existing debt when needed by the repository gate. Its target is always zero.

The validator must reject baseline growth/new failures and must not use the baseline to hide collection/infrastructure errors or newly introduced authorization/security regressions.

## 2. Feature-contract metadata

Fair CRM machine-readable feature contracts live under:

```text
.kyrox/features/*.json
.kyrox/feature-contract.schema.json
```

These are CI/governance inputs, not human documentation. Applicability semantics come from [FEATURE_APPLICABILITY_STANDARD.md](FEATURE_APPLICABILITY_STANDARD.md) and the shared KYROX applicability standard.

## 3. Fair CRM quality surfaces

Depending on feature applicability, evidence may include:

- full/targeted backend pytest,
- frontend tests,
- frontend production build,
- feature-contract validation,
- UI/design-system governance,
- permission/route/action guard checks,
- production-shaped runtime authorization verification.

A material delivery reports every applicable surface accurately. A green build does not prove runtime authorization; mocked authorization does not prove the production-shaped path.

## 4. UI governance

Legacy UI debt, if any, follows the shared monotonic rule: no new violations and existing debt moves toward zero. New work may not copy an old violation as precedent.

Canonical frontend implementation rules: [frontend/FRONTEND_UI_MASTER_STANDARD.md](frontend/FRONTEND_UI_MASTER_STANDARD.md).

## 5. Self-testing gates

Changes to Fair CRM workflow/quality scripts, `.kyrox` schemas/baselines/contracts or governance validators must trigger the checks needed to validate those changes. Exact paths and workflow names are implementation details of the Fair CRM code repository.

## 6. Branch protection and reporting

Do not claim GitHub CI prevents a merge/push unless required checks are actually enforced by repository rulesets/branch protection.

Completion reports distinguish:

- strict green,
- zero-new-regression with explicitly remaining legacy debt,
- failure/new regression.

Never call all three states “PASS” without qualification.

## Related

- [Shared Quality Gate Standard](../../standards/quality/QUALITY_GATE_STANDARD.md)
- [Fair CRM Feature Applicability Extension](FEATURE_APPLICABILITY_STANDARD.md)
- [Fair CRM Development Standard](DEVELOPMENT_STANDARD.md)
- [Fair CRM Frontend UI Master Standard](frontend/FRONTEND_UI_MASTER_STANDARD.md)
