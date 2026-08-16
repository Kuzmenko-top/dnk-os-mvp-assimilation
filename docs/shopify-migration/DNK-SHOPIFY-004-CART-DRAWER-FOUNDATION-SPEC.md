# DNK-SHOPIFY-004-CART-DRAWER-FOUNDATION-SPEC
**Task ID**: DNK-SHOPIFY-004
**Author**: DNK-e.com Maksym
**Date**: 2026-08-16

---

## 1. Recommended Cart Drawer Strategy
**Strategy**: `DNK_COMPATIBILITY_ADAPTER` (Extend Native Horizon).

- **Horizon Platform Runtime Owns**:
  - `<theme-drawer>` and `<cart-drawer-component>` DOM shell.
  - Cart mutation events (`cart:updated`, `cart:refresh`).
  - Section Rendering API updates.
- **DNK Compatibility Layer Owns**:
  - Theme block extension point (`"blocks": [{"type": "@theme"}, {"type": "@app"}]` in `cart-drawer-section.liquid`).
  - Custom interactive and content blocks (`free-shipping-progress`, `trust-badges`, `volume-discount`).
