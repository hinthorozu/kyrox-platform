# FAIR CRM / KYROX — Quality Gate Standard

**Status:** Canonical / binding quality-gate standard  
**Scope:** Fair CRM CI, test debt, regression prevention, acceptance reporting  
**Audience:** Human developers, AI coding agents, reviewers and CI tooling

This document defines how automated quality evidence is interpreted and enforced for Fair CRM.

The goal is strict and monotonic:

> **New work must never make the verified quality state worse, and every known legacy defect must move toward zero.**

This standard complements:

- `DEVELOPMENT_STANDARD.md` — delivery order and Definition of Done,
- `FEATURE_APPLICABILITY_STANDARD.md` — which gates are REQUIRED or N/A,
- `frontend/FRONTEND_UI_MASTER_STANDARD.md` — frontend/UI governance.

---

## 1. Strict green is the target state

The desired repository state is always:

```text
backend tests: 0 failures
frontend tests: 0 failures
build: success
feature contracts: valid
UI governance: 0 violations
new regressions: 0
```

A baseline is not a substitute for fixing failures. It is a temporary migration mechanism for **pre-existing debt discovered when enforcement is introduced to a repository that was already non-green**.

The target baseline size is always:

```text
0
```

---

## 2. Two different meanings of PASS

CI and completion reports must distinguish these states explicitly.

### Strict green PASS

```text
All applicable checks pass.
No known baseline test failures remain.
No baseline governance debt remains.
```

This is the final desired state.

### Zero-new-regression PASS with known debt

```text
No new regression was introduced by the current repository state/change.
Only explicitly recorded pre-existing baseline failures remain.
```

This is **not** equivalent to “all tests pass”.

When known debt remains, reports must say so explicitly, including the current count when available.

Example:

```text
QUALITY GATE: PASS — 0 new regressions; 19 known backend test failures remain; target=0.
```

Forbidden wording:

```text
All backend tests passed.
```

when pytest still reports known failures.

---

## 3. Legacy baseline admission rule

A new baseline may be seeded only when all of the following are true:

1. Enforcement is being introduced or expanded over an existing repository area.
2. The failures/violations demonstrably existed before the enforcement rollout or current feature change.
3. The exact failing test node IDs or governance findings are recorded machine-readably.
4. The source commit/run used to establish the baseline is recorded where practical.
5. The baseline target remains zero.
6. The baseline is reviewed as technical debt, not accepted product behavior.

A baseline must never be used as a routine response to a newly introduced failure.

---

## 4. Monotonic baseline rule

Once a baseline exists:

```text
current_baseline ⊆ previous_baseline
```

The baseline may:

- shrink,
- become empty.

The baseline may **not**:

- grow,
- replace one known failure with a new failure,
- add a new failing test simply to make CI green,
- hide collection/infrastructure errors,
- convert a security/authorization regression into accepted debt.

Any newly failing test outside the previous baseline is a hard CI failure.

---

## 5. Backend test debt contract

Fair CRM stores the current backend known-failure baseline as machine-readable governance metadata:

```text
.kyrox/backend-test-baseline.json
```

The baseline contains exact pytest node IDs.

The CI validator must verify at minimum:

- valid JSON/structure,
- unique node IDs,
- target failure count remains zero,
- policy remains `zero_new_failures`,
- current baseline does not contain entries absent from the comparison-base baseline after initial seeding.

The full backend pytest suite still runs. The gate evaluates the actual failing node IDs against the baseline.

### Result rules

```text
pytest = 0 failures
-> strict PASS

pytest failures ⊆ known baseline
-> zero-new-regression PASS with explicit known debt

pytest contains any failure outside baseline
-> FAIL

pytest exits non-zero without parseable test failures
-> FAIL as collection/infrastructure error
```

The CI must not skip the full suite merely because a baseline exists.

---

## 6. Baseline reduction rule

If a known baseline failure stops reproducing, CI should surface it as a removal candidate.

After stability is confirmed, remove the entry from the baseline.

Do not retain resolved entries “just in case”. An oversized baseline weakens regression detection.

The expected progression is:

```text
19 -> 18 -> 17 -> ... -> 1 -> 0
```

Never:

```text
19 -> 20
```

---

## 7. Frontend/UI legacy debt

The same monotonic principle applies to pre-existing UI governance debt.

Where a full repository UI inventory already contains legacy violations, CI may compare the current inventory with the comparison-base inventory and require:

```text
new violations = 0
```

Existing violations remain visible debt and should be reduced independently.

A feature may not introduce a new design-system violation because an older page already contains similar debt.

When no legacy UI debt remains, the repository should move to strict full-governance enforcement.

---

## 8. Feature applicability remains authoritative

Not every feature runs every quality surface.

Applicability is determined by `FEATURE_APPLICABILITY_STANDARD.md` and the machine-readable Feature Contract.

Examples:

```text
backend-only scheduled job
-> backend tests REQUIRED
-> frontend tests N/A with reason

UI-only maintenance
-> frontend tests/UI governance REQUIRED
-> backend tests N/A when no backend executable behavior changes
```

A quality gate may be N/A only because the feature contract proves the surface does not apply. It may not be marked N/A because the check is inconvenient or failing.

---

## 9. Gate changes test themselves

Changes to quality-gate scripts, workflow files, schemas or baseline validators must trigger the relevant quality gates themselves.

The gate must not contain a blind spot where modifying the checker avoids running the checker.

At minimum, changes to these classes of files must trigger their own validation:

```text
.github/workflows/*quality/development-standard*
.kyrox/*schema/baseline/feature metadata*
scripts/*quality/validation/governance*
```

Exact repository paths are implementation details owned by the code repository.

---

## 10. Diagnostic evidence

When a long-running CI job fails, enough evidence must be retained to diagnose it without guessing.

Where supported, CI should retain a short-lived artifact/log containing the quality command output.

Diagnostic artifacts do not change pass/fail semantics and must not contain secrets.

---

## 11. Branch protection boundary

GitHub Actions alone detects failure; it does not prevent a direct push to an unprotected branch.

For hard merge enforcement, the repository must configure GitHub branch protection/rulesets requiring the canonical development-standard checks before merge.

Until that repository setting is enabled:

- CI remains binding evidence,
- a failed `main` run is a broken-main condition,
- direct pushes can technically bypass pre-merge enforcement and therefore must not be treated as equivalent to protected merges.

Do not claim “CI blocks merge/push” unless repository protection actually requires the checks.

---

## 12. Completion reporting

A delivery report must state the real observed state.

Examples:

### Strict green

```text
Feature Contract: PASS
Frontend tests/build/UI gate: PASS
Backend full suite: PASS (0 failures)
```

### Known backend debt remains

```text
Feature Contract: PASS
Frontend tests/build/UI gate: PASS
Backend regression gate: PASS (0 new failures)
Backend full pytest: 19 known failures remain; target=0
```

### Failure

```text
Backend regression gate: FAIL
New failing test: tests/...::test_x
```

Never collapse these three states into the same phrase.

---

# Golden quality rule

**A baseline can preserve visibility of yesterday’s debt while preventing tomorrow’s regression; it can never legalize new debt.**

```text
Known state
  -> explicit machine-readable baseline when strictly necessary
  -> full applicable checks still execute
  -> new regression = FAIL
  -> resolved debt = baseline shrinks
  -> target = strict green / zero baseline
```
