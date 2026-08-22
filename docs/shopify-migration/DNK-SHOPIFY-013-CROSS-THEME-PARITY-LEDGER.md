# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-013-CROSS-THEME-PARITY-LEDGER.md"
# purpose: "Comprehensive Cross-Theme Parity Ledger Synthesizing Waves 1 through 5"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-013: Cross-Theme Parity Ledger

**Task ID**: DNK-SHOPIFY-013  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 6 Regression & Migration Readiness  

---

## 1. Master Capability Parity Register

| Capability Domain | Legacy Capability (`DNK_Ecom_v1_0_0`) | Target Implementation (Horizon Draft) | Parity Status | Evidence & Validation | Owner | Risk | Rollout Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cart Drawer** | Monolithic `snippets/cart-drawer.liquid` (73KB) | Horizon `cart-drawer.liquid` + `dnk-cart-drawer-adapter` | **PARITY_ACHIEVED** | Wave 1B/2A verified. Zero legacy CSS/JS injection. | Theme / Storefront | Low | **READY** |
| **Cart Free Shipping** | Hardcoded client math bar | Horizon adapter reading store market thresholds | **PARITY_ACHIEVED** | Verified against shop currency settings. | Theme / Storefront | Low | **READY** |
| **Cart Claims** | Unverified urgency & fake delivery badges | Verified store policy contract (0 DOM if empty) | **PARITY_ACHIEVED** | Strict policy checks; 0 unverified claims. | Merchandising | Low | **READY** |
| **PDP Form / Variants** | Legacy jQuery & `product.liquid` scripts | Native Custom Element `<product-form>`, `<variant-picker>` | **PARITY_ACHIEVED** | Wave 3 audit passed. Native Section Rendering API. | Theme / Horizon | Low | **READY** |
| **Volume Pricing** | Client-side JS discount calculation math | Native `quantity_price_breaks` display gate | **PARITY_ACHIEVED** | Wave 3.2 verified. 0 DOM output when breaks empty. | Backend / B2B | Low | **READY** |
| **PLP Facets & Filters** | Custom legacy filter wrappers | Native `<facets-form>` and Search & Discovery filters | **PARITY_ACHIEVED** | Wave 4 audit passed. Native URL params sync. | Theme / Horizon | Low | **READY** |
| **PLP Merchandising** | Hardcoded rating/swatch wrappers | Native review metafields, system badges, native swatches | **PARITY_ACHIEVED** | Wave 4A audit passed. Zero DOM output if empty. | Merchandising | Low | **READY** |
| **Logistics / Carrier** | Hardcoded UI date estimates | Shopify Shipping & Checkout UI Extension / App Proxy | **DEFERRED (SAFE)** | Wave 5 audit passed. Zero carrier API keys in theme. | Logistics / Backend | Low | **DEFERRED** |
| **Upsells & Gifts** | Client `/cart/add.js` loops & custom snippets | Horizon `product-recommendations` + Shopify Functions | **READY / DEFERRED** | Wave 5 audit passed. Backend checkout price authority. | Backend / Marketing | Low | **READY** |

---

## 2. Integrity Verification Summary

- **Total Assessed Capabilities**: 9 Core Domains
- **Parity Achieved / Ready**: 7 Domains
- **Safely Deferred to Backend / Apps**: 2 Domains (Nova Poshta Checkout Extension, Shopify Functions Gifts)
- **Unresolved / Broken Capabilities**: 0
