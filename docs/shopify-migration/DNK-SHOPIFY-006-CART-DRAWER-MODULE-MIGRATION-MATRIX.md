# DNK-SHOPIFY-006-CART-DRAWER-MODULE-MIGRATION-MATRIX
**Task ID**: DNK-SHOPIFY-006
**Author**: DNK-e.com Maksym
**Date**: 2026-08-16

---

## Migration Decision Matrix

| Capability ID | Decision | Wave | Rationale / Required Evidence |
|---|---|---|---|
| `cart.shipping.free_shipping_progress` | **ADAPT** | Wave 1B | Verified threshold calculation in subunits; zero cart mutation |
| `cart.trust.badges_and_guarantee` | **ADAPT** | Wave 1B | Verified return policy law evidence; clean SSL copy |
| `cart.trust.payment_icons` | **REPLACE_WITH_HORIZON_NATIVE** | Wave 1B | Native dynamic SVG payment icons |
| `cart.pricing.volume_discount` | **DEFER** | Wave 3 | Requires checkout pricing authority via Shopify Functions |
| `cart.delivery.nova_poshta` | **DEFER** | Wave 5 | Requires verified API proxy & app configuration |
| `cart.upsell.product_recommendations` | **DEFER** | Wave 5 | Requires recommendations API & inventory rules |
| `cart.urgency.countdown_fomo` | **EXCLUDE** | N/A | Artificial urgency prohibited without real inventory/event proof |
