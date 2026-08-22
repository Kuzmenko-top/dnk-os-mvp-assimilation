# author: "DNK-e.com Maksym"
# purpose: "PDP Conversion Runtime Discovery & Parity Audit for Wave 3 Migration"
# mrh_id: "DNK-SHOPIFY-007-PDP-CONVERSION-RUNTIME-AUDIT"
# status: "ACTIVE"
# created_at: "2026-08-22"

# DNK-SHOPIFY-007: PDP Conversion Runtime Audit

## Executive Summary

This audit performs a full discovery and comparative analysis of the **Product Conversion Runtime** between the legacy theme (`DNK_Ecom_v1_0_0`) and the target Horizon-based theme (`DNK-e.com`). The scope covers the entire PDP lifecycle from template resolution down to the Cart Drawer add-to-cart handoff.

---

## 1. Scope & System Entrypoints

The PDP conversion runtime comprises 7 core functional components:

1. **Product Template**: `templates/product.json`
2. **Main Product Section**: `sections/main-product.liquid` (Legacy) vs `sections/product-information.liquid` (Target)
3. **Product Information Blocks**: Title, Price, Variant Picker, Quantity Selector, Inventory, Buy Buttons
4. **Variant Picker Lifecycle**: `variant-picker.js`, `variant-resolution.js`
5. **Quantity Selector Lifecycle**: `component-quantity-selector.js`
6. **Price Renderer**: `product-price.js`, `price-per-item.js`, `snippets/format-price.liquid`
7. **Add-To-Cart & Cart Drawer Handoff**: `product-form.js`, `/cart/add.js` AJAX pipeline

---

## 2. Component Parity & Comparison Matrix

| Component | Legacy (`DNK_Ecom_v1_0_0`) | Target Horizon (`DNK-e.com`) | Parity Status | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Product Template** | Monolithic `templates/product.json` rendering heavy `main-product.liquid` | Modular `templates/product.json` rendering `product-information.liquid` | **Architectural Superiority in Target** | Adopt Horizon native structure |
| **Variant Picker** | `snippets/product-variant-picker.liquid` + `assets/global.js` (DOM swap via Section Rendering API) | `blocks/variant-picker.liquid` + `assets/variant-picker.js` + `assets/variant-resolution.js` | **Fully Supported Native** | Native Horizon implementation |
| **Quantity Selector** | `snippets/quantity-input.liquid` inside forms | `blocks/quantity.liquid` + `assets/component-quantity-selector.js` | **Fully Supported Native** | Native Horizon with `quantity_rule` support |
| **Price Renderer** | Custom `snippets/price.liquid` + `snippets/price-for-above.liquid` | `blocks/price.liquid` + `assets/product-price.js` + `snippets/unit-price.liquid` | **Fully Supported Native** | Native Horizon price renderer |
| **Buy Buttons & Form** | `<product-form>` posting `/cart/add.js` | `<product-form>` in `blocks/buy-buttons.liquid` posting `/cart/add.js` | **Fully Supported Native** | Native Horizon buy buttons |
| **ATC Handoff to Cart Drawer** | Custom JS event opening cart notification / drawer | `assets/product-form.js` dispatching `cart:updated` event to `cart-drawer` | **Fully Supported Native** | Retain Horizon event-driven handoff |
| **Volume Discounts** | Customizer-configured Liquid `snippets/quantity-breaks.liquid` (display-only math) | Native `snippets/volume-pricing-info.liquid` reading `variant.quantity_price_breaks` | **No Checkout Authority in Legacy** | **DISPLAY_ONLY_MANUAL_REVIEW** (Forbidden in theme code) |

---

## 3. Legacy Volume Discount Governance Finding

Legacy `quantity-breaks.liquid` relies on Theme Customizer block settings (`option_1_quantity`, `option_1_percentage_off_text`, etc.) and JavaScript calculations.
- **Price Authority Verification**: `no_verified_authority`.
- **Checkout Enforcement**: The legacy theme calculates prices in frontend Liquid/JS, but **cannot guarantee or enforce discounts at Shopify checkout** without an underlying Shopify Function or Automatic Discount rule.
- **Governance Decision**: Theme Liquid must not promise unverified checkout prices. Implementation of legacy quantity breaks is **FORBIDDEN** until a verified backend price authority contract is established.
