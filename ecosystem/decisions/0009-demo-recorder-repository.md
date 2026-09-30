# ADR-0009: Demo recorder repository

- **Status:** Accepted
- **Date:** 2026-09-30
- **Deciders:** KYROX ecosystem maintainers

## Context

KYROX needs repeatable product-usage videos that exercise the real deployed user interface rather than simulated screens.

The first approved workflow is FAIR CRM login -> customer creation -> customer detail -> Standlar -> Yeni Proje -> Fair Stand scene.

This work is operational/demo automation. It must not become FAIR CRM or Fair Stand runtime behavior, must not own product data, and must not introduce a second authentication or authorization model.

## Decision

Create `hinthorozu/kyrox-demo-recorder` as a dedicated automation repository.

Its scope is limited to:

- Playwright-driven browser automation against deployed KYROX product UIs,
- video/screenshot capture for demos and usage documentation,
- GitHub Actions workflows that run explicitly requested recordings and upload generated media as workflow artifacts,
- secret-free source code; credentials are supplied only through runtime environment variables or GitHub Actions secrets.

The repository is **not**:

- a production KYROX service,
- a source of product/domain truth,
- an authentication, authorization, organization, or data store,
- a replacement for product E2E acceptance gates,
- a home for ecosystem standards or product documentation.

Human-readable ecosystem rules remain in `kyrox-platform`. Product behavior remains owned by the product repositories.

## Ownership and boundaries

- FAIR CRM routes, labels, permissions and customer behavior remain owned by `fair-crm`.
- Fair Stand scene/configurator behavior remains owned by `fair-stand`.
- Core identity and organization behavior remain owned by `kyrox-core`.
- `kyrox-demo-recorder` is only an external browser consumer of the deployed UI.
- Recorder failures do not redefine product acceptance; product CI/runtime gates remain authoritative.

## Security

- No passwords, tokens, session state or other secrets are committed.
- Production/demo credentials are injected at runtime.
- GitHub Actions credentials use repository/environment secrets, never workflow inputs or committed files.
- Recorder artifacts must not intentionally capture credentials; recording starts only after sensitive form filling when practical, or the login portion is edited/cropped if the password field could reveal sensitive input.
- Demo accounts must use the minimum permissions required by the recorded flow.

## Delivery profile

Feature profile: `maintenance` / developer tooling.

SaaS-impact classification:

- organization-owned data / tenant isolation: N/A to recorder ownership; the recorder only exercises the product's existing organization-scoped UI.
- permission scope: N/A to recorder ownership; existing product permissions remain authoritative.
- Core vs product ownership: affected and resolved by this ADR; recorder owns no product/platform behavior.
- plan / entitlement: N/A.
- usage / quota: N/A.
- organization lifecycle: N/A.
- secrets / production security: REQUIRED; credentials are runtime-only and must never be committed.
- background jobs / audit: N/A.
- export / retention / deletion: N/A.
- scale / infrastructure: N/A.

## Acceptance

The initial recorder slice is accepted only when:

1. source contains no credentials,
2. Playwright can launch the browser and record video,
3. the real FAIR CRM path can be exercised with runtime-provided demo credentials,
4. the generated video is uploaded as a GitHub Actions artifact,
5. failure is explicit when required environment variables or expected UI controls are missing.

## Consequences

### Positive

- usage videos become repeatable,
- no manual screen recording is required,
- recorder logic stays out of product runtime repositories,
- future demo flows can reuse one small automation harness.

### Negative

- UI text/structure changes may require recorder locator maintenance,
- GitHub Actions needs separately configured demo credentials,
- recorder output is auxiliary evidence, not product acceptance evidence.

## Related

- [Repository strategy](../REPOSITORY_STRATEGY.md)
- [Workflow](../WORKFLOW.md)
- [ADR-0001](0001-repository-strategy.md)
- [ADR-0007](0007-fair-stand-product-ownership.md)
- [ADR-0008](0008-fair-stand-independent-service.md)
