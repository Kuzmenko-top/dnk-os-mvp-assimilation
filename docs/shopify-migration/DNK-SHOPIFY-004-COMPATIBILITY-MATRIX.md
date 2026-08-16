# DNK-SHOPIFY-004-COMPATIBILITY-MATRIX
**Task ID**: DNK-SHOPIFY-004
**Author**: DNK-e.com Maksym
**Date**: 2026-08-16

---

## Capabilities Classification Matrix

| Capability ID | Legacy Source | Business Outcome | Decision | Target Path | Rationale |
|---|---|---|---|---|---|
| `cart_drawer_shell` | `sections/cart-drawer.liquid` | Cart Drawer Container | **REPLACE_WITH_HORIZON_NATIVE** | `sections/cart-drawer-section.liquid` | Horizon web component is faster and a11y compliant |
| `free_shipping_progress` | `snippets/cart-progress-bar.liquid` | Increase AOV with threshold bar | **ADAPT** | `blocks/free-shipping-progress.liquid` | Recipe A v2 Theme Block |
| `trust_badges` | `snippets/moneybackcheckcart.liquid` | Social proof & delivery guarantee | **ADAPT** | `blocks/trust-badges.liquid` | Recipe B Static Theme Block |
| `volume_discount` | `snippets/cart-fomo-block.liquid` | Tiered discounts | **ADAPT** | `blocks/volume-discount.liquid` | Theme block presentation (display only) |
