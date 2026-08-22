# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-012-UPSELL-GIFT-CONTRACT.md"
# purpose: "Upsells, Cross-sells, and Gift Rewards Commerce Data Contract Specification"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-012: Upsell & Gift Rewards Commerce Data Contract

**Task ID**: DNK-SHOPIFY-012  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 5 Upsell and Gift Commerce Contract  

---

## 1. Product Upsell & Recommendations Contract

```yaml
capability_id: "cart.recommendations.upsell"
legacy_sources:
  - "snippets/upsell-block.liquid"
customer_outcome: "Relevant cross-sell and complementary product suggestions on PDP and in Cart Drawer."
trigger: "Product view or Cart Drawer open"
data_owner: "Shopify (Search & Discovery / Catalog Engine)"
data_source: "/recommendations/products.json?product_id={id}&intent=related"
authentication: "none (Storefront Public API)"
external_endpoint: "none (Shopify Native Storefront Route)"
personal_data_processed: []
consent_or_privacy_basis: "Legitimate interest / Anonymous browsing session"
cache_ttl: "Browser session / CDN cached"
timeout_ms: 2000
fallback_ui: "0 DOM output if no recommendations returned"
failure_mode: "Container auto-hides silently"
cart_or_checkout_authority: "Shopify Catalog"
Horizon_integration_point: "blocks/product-recommendations.liquid / dnk-cart-drawer-adapter upsell container"
theme_only_feasible: true
decision: "REPLACE"
evidence:
  - "Horizon has native product-recommendations block supporting Shopify Recommendations API"
```

---

## 2. Gift Rewards & Tiered Promotion Contract

```yaml
capability_id: "cart.rewards.gifts"
legacy_sources:
  - "snippets/cart-gift.liquid"
  - "snippets/auto-add-gifts.liquid"
  - "snippets/quantity-gifts.liquid"
customer_outcome: "Free gift or bonus item awarded when order value or quantity exceeds specified threshold."
trigger: "Cart subtotal threshold reached"
data_owner: "Shopify Functions / Shopify Discounts Engine"
data_source: "Shopify Admin Automatic Discounts API"
authentication: "none (Server-evaluated via Shopify Checkout Function)"
external_endpoint: "none"
personal_data_processed: []
consent_or_privacy_basis: "E-commerce promotion"
cache_ttl: "Dynamic per cart session"
timeout_ms: 0
fallback_ui: "Standard cart line items without gift badge"
failure_mode: "Gift not applied if inventory depleted or threshold unmet"
cart_or_checkout_authority: "Shopify Backend (Order Routing & Functions)"
Horizon_integration_point: "Cart Drawer informational milestone banner"
theme_only_feasible: false
decision: "DEFER"
evidence:
  - "Legacy theme manipulated cart via client-side /cart/add.js, causing sync race conditions and inventory leaks"
  - "Must be implemented via Shopify Functions (Discount / Cart Transform API)"
```
