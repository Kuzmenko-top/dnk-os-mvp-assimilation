# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-012-INTEGRATION-INVENTORY.md"
# purpose: "Comprehensive Inventory of Legacy Theme Integrations, Snippets, and Data Contracts"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-012: External Integrations & Commerce Data Contracts Inventory

**Task ID**: DNK-SHOPIFY-012  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 5 Discovery  

---

## 1. Inventory Summary

This document catalogues all legacy snippets, external couplings, recommendation blocks, shipping calculators, and gift incentives identified in `DNK_Ecom_v1_0_0` alongside their architectural disposition for Horizon.

---

## 2. Integration & Capability Inventory

| Capability ID | Module / Feature | Legacy Source Snippet(s) | Data Owner | Authority Level | Recommended Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `cart.delivery.estimate` | Delivery Date & Timer Estimation | `snippets/delivery-date.liquid`<br>`snippets/estimated-shipping.liquid`<br>`snippets/estimated-shipping-cart-block.liquid` | Theme Static Settings | Informational UI Only (Non-Authoritative) | `REPLACE` with clean informational Liquid block (no client-side hardcoded carrier keys). |
| `cart.delivery.checkpoints` | Shipping Checkpoints / Progress | `snippets/shipping-checkpoints.liquid`<br>`snippets/blinking-shipping-and-text.liquid` | Theme Static Settings | Informational UI Only | `REPLACE` with Horizon announcement / informational blocks. |
| `cart.delivery.nova_poshta` | Nova Poshta Carrier Integration | Not present in legacy liquid (UI date mock only) | Nova Poshta / Carrier Service | Checkout Authoritative (Shopify Shipping / Carrier API) | `DEFER` to Shopify App / Checkout UI Extension. Forbidden in theme Liquid. |
| `cart.recommendations.upsell` | Product Upsell / Cross-sell | `snippets/upsell-block.liquid` (21.9 KB) | Shopify Search & Discovery API | Shopify Catalog / Recommendations Engine | `REPLACE` with Horizon native `blocks/product-recommendations.liquid`. |
| `cart.rewards.gifts` | Auto-Add & Tiered Cart Gifts | `snippets/cart-gift.liquid`<br>`snippets/auto-add-gifts.liquid`<br>`snippets/quantity-gifts.liquid` | Shopify Functions / Discount API | Backend Cart Authority | `DEFER` to Shopify Functions / App. Forbidden client-side `/cart/add.js` tier manipulation. |
| `cart.rewards.free_shipping_bar` | Free Shipping Progress Bar | `snippets/cart-drawer.liquid` (legacy bar) | Shopify Market / Shipping Settings | Cart Subtotal vs Threshold | `ADAPT` via `dnk-cart-drawer-adapter` using store threshold settings. |

---

## 3. Data Governance & Security Invariants

1. **Zero Secret Storage in Theme**: No API keys (Nova Poshta API token, 3rd party logistics tokens) shall ever be committed or exposed in theme Liquid or assets.
2. **Zero Client Cart Mutation for Discounts**: No client-side JavaScript math or automated `/cart/add.js` calls for tiered free gifts without backend Shopify Functions authorization.
3. **Privacy First**: No customer PII (names, phone numbers, delivery addresses) shall be routed through unauthenticated frontend endpoints.
