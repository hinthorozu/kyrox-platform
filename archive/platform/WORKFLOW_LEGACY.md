# KYROX Workflow

Standard workflow for ecosystem decisions and implementation across kyrox-platform, kyrox-core, and fair-crm.

## Overview

```
Decide → Implement → Review → Quality check → Commit → Push → Tag (if milestone-worthy)
```

Work starts with clarity in **kyrox-platform** and finishes with verified, tagged releases in **kyrox-core** or **fair-crm**.

## Steps

### 1. Decide in kyrox-platform

- Capture significant architectural or strategic choices as **ADRs** in `decisions/`.
- Update **roadmap** or **milestone** docs when scope or priority changes.
- Ensure the target repository (kyrox-core vs fair-crm) is explicit before implementation starts.

**Output:** Updated docs, approved scope, linked ADR or milestone ID.

### 2. Implement in kyrox-core or product repo

- **Platform capabilities** (identity, tenancy, shared services) → **kyrox-core**
- **Product-specific features** (CRM domain, product UI) → **fair-crm**
- Do not add application code to kyrox-platform.
- Reference milestone IDs (e.g. `M2`) in branch names or PR descriptions where helpful.

**Output:** Code changes in the correct repository only.

### 3. Review

- Peer review via pull request in kyrox-core or fair-crm.
- Confirm alignment with relevant ADRs and active milestone scope.
- For cross-cutting changes, note links to kyrox-platform docs in the PR description.

**Output:** Approved PR ready to merge.

### 4. Quality check

- Run tests, lint, and type checks defined in the implementation repository.
- Verify no forbidden dependencies (e.g. Core must not depend on fair-crm).
- Smoke-test critical paths for the change.

**Output:** Green CI and manual verification as required by the repo.

### 5. Commit

- Use clear commit messages describing **why**, not only what changed.
- Prefer conventional commits where the repo already uses them.
- Squash or merge per repository convention after review.

**Output:** Changes committed on the target branch (typically `main` or integration branch).

### 6. Push

- Push to the remote repository after merge or direct commit per team policy.
- Ensure kyrox-platform docs stay in sync if the decision or milestone status changed.

**Output:** Remote branch updated; CI runs on push if configured.

### 7. Tag when milestone-worthy

- Tag releases in **kyrox-core** or **fair-crm** when a milestone slice or version boundary is reached.
- Use semver or milestone tags as defined by each repo (e.g. `v0.2.0-m2`, `m2-identity-complete`).
- Update **ROADMAP.md**, milestone files, and **CHANGELOG.md** in kyrox-platform when a milestone completes.

**Output:** Git tag on the implementation repo; platform docs reflect new status.

## Repository cheat sheet

| Activity              | Repository      |
|-----------------------|-----------------|
| ADRs, roadmap, vision | kyrox-platform  |
| Identity, platform API| kyrox-core      |
| CRM product features  | fair-crm        |

## Current milestone

**M2 Identity** is active. Implementation work belongs in **kyrox-core** unless explicitly product-only scope in fair-crm.

See [ROADMAP.md](../ROADMAP.md) and [M2_IDENTITY.md](../milestones/M2_IDENTITY.md).
