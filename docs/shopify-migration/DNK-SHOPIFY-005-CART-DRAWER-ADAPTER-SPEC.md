# DNK-SHOPIFY-005-CART-DRAWER-ADAPTER-SPEC: Wave 1B Compatibility Adapter Foundation
**Task ID**: DNK-SHOPIFY-005
**Author**: DNK-e.com Maksym
**Date**: 2026-08-16
**Phase**: Wave 1B Runtime Foundation

---

## 1. Runtime Ownership Boundary
```text
Horizon Platform Runtime:
  Owns: Cart mutation AJAX requests (/cart/add.js, /cart/change.js),
        Drawer shell (<theme-drawer> & <cart-drawer-component>),
        Focus & Accessibility primitives, Native events.

DNK Compatibility Adapter (assets/dnk-cart-drawer-adapter.js):
  Owns: Feature-zone discovery, post-render initialization,
        Module lifecycle hooks, Idempotent telemetry.
```

## 2. Invariants & Constraints
- **Zero Cart Mutation**: Adapter NEVER makes native `/cart/*.js` calls.
- **Idempotent Design**: Single window instance `window.DNKCartDrawerAdapterInstance`.
- **Zero External HTTP Requests**: All logic executes locally in browser.
