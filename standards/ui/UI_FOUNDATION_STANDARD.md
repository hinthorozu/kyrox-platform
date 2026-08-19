# KYROX UI Foundation Standard

**Status:** Canonical shared KYROX standard  
**Scope:** User-facing KYROX product interfaces  
**Audience:** Human developers, AI agents, reviewers and UI quality tooling

This document defines product-independent UI engineering principles. Product UI standards define exact component names, tokens, visual language and supported breakpoints; they must not weaken these foundations.

## 1. One design system per product

A product has one canonical UI/design system. Do not create page-local parallel button, input, modal, table, navigation, feedback or layout families when an existing shared primitive can solve the problem.

When the shared system is insufficient:

1. explain why,
2. extend the shared primitive when appropriate,
3. add a new shared primitive only when the need is genuinely distinct,
4. document any specialty exception.

## 2. Shared primitives over copied styling

Copying CSS/classes into a raw element is not equivalent to using the shared component API. Consumers use the product's canonical primitives so behavior, accessibility and future changes remain centralized.

## 3. Design tokens over magic values

Typography, spacing, colors, surfaces, borders, radius, shadow, focus, control sizes and layout dimensions come from the product's token system. Page-specific magic values or one-off breakpoints require explicit justification.

## 4. Responsive by default

Interfaces are designed as fluid systems, not screenshots for one desktop width.

Use appropriate combinations of flexible layout, grid/flex, `minmax`, `clamp`, controlled containers and responsive wrapping. Critical actions must remain usable at supported narrow widths.

Product standards define supported viewport targets and specialized responsive engines such as data-table behavior.

## 5. Real visual QA is required

Build/type/static-governance success does not prove UI quality. Applicable UI work is evaluated on a real render for:

- alignment,
- spacing/density,
- hierarchy,
- typography/readability,
- field/control sizing,
- action placement,
- overflow/clipping/overlap,
- responsive balance,
- loading/empty/error behavior.

A technically passing but visibly broken interface is not accepted.

## 6. Accessibility is part of the component contract

Applicable UI must preserve semantic controls, label/control relationships, keyboard navigation, visible focus, disabled semantics, appropriate ARIA and modal/dialog focus behavior.

Icon-only actions require an accessible name.

## 7. Forms protect unsaved work

Create/edit/update flows must not silently discard meaningful unsaved user changes. Products use one shared dirty-form mechanism across applicable page, modal, drawer and wizard surfaces.

Expected semantics:

- clean exit does not ask unnecessarily,
- dirty exit requires explicit discard confirmation,
- choosing to stay preserves entered data,
- successful save resets the dirty baseline,
- failed save does not clear dirty state,
- do not create page-local `window.confirm` or a second dirty-state framework when a shared mechanism exists.

Exact copy and implementation API are product-specific.

## 8. Loading, empty, error and refresh are distinct states

- Initial request with no successful data yet shows an explicit loading state.
- Empty state is shown only after a successful empty result.
- Failed request with no data shows an error/retry state rather than infinite loading.
- Background refresh of already-successful data should preserve visible data and user context rather than flashing a full initial loader, unless the product explicitly requires otherwise.

## 9. Scalable lists use shared table/list infrastructure

For server-backed scalable datasets, products use their canonical server-side list/table infrastructure rather than page-local client-side pagination/filter/sort engines.

Responsive list behavior is centralized in shared product infrastructure; each page does not invent its own mobile table strategy.

## 10. Permission-aware UI

Protected navigation/routes/actions follow the canonical [CRUD & UI Authorization Standard](CRUD_UI_AUTHORIZATION_STANDARD.md). UI visibility uses effective capabilities and does not substitute for backend authorization.

## 11. Specialty UI is explicit

A specialty surface is allowed only when the normal shared system cannot represent the requirement without distortion. It still follows tokens, accessibility, responsive behavior and overall product visual language.

“Specialty” is not a blanket exemption from design-system governance.

## 12. Acceptance rule

A UI change is complete only when all applicable evidence agrees:

```text
shared component/design-system conformance
+ effective-permission behavior
+ responsive behavior
+ accessibility behavior
+ real visual QA
+ real API/runtime behavior where applicable
```

Product-specific UI documents are implementation profiles of this standard, not competing foundations.
