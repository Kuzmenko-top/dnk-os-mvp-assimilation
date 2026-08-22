# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-014-UAT-EVALUATION-MATRIX.md"
# purpose: "UAT Evaluation Matrix Across Catalog Archetypes, Devices, and Customer States"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-014: UAT Evaluation Matrix

**Task ID**: DNK-SHOPIFY-014  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 7 UAT Matrix  

---

## 1. Catalog Archetype Evaluation

| Product Archetype | Expected Storefront Display | Pricing / Badge Rule | UAT Status |
| :--- | :--- | :--- | :--- |
| **Standard D2C Product** | Native `<product-form>`, single price, Add to Cart enabled | Regular price, no badges | **VERIFIED** |
| **Multi-Variant Swatches** | Swatch selection, dynamic image switch, URL variant sync | Active variant price displayed | **VERIFIED** |
| **Sold Out Item** | Disabled CTA, "Sold Out" badge rendered | `available == false`, 0 add-to-cart | **VERIFIED** |
| **Compare-At Sale Item** | "Sale" badge rendered, original price struck through | `compare_at_price > price` | **VERIFIED** |
| **Reviews Metafield Item** | Star rating stars & count displayed | `metafields.reviews.rating` rendered; 0 DOM if empty | **VERIFIED** |
| **B2B Volume Pricing Item** | Native volume break table rendered conditionally | Rendered only if `quantity_price_breaks` populated | **VERIFIED** |

---

## 2. Device & Viewport Matrix

| Viewport / Environment | Key Interaction Target | Acceptance Standard | UAT Status |
| :--- | :--- | :--- | :--- |
| **Mobile (iOS Safari / Chrome)** | Touch scroll, swipe gallery, Cart Drawer bottom-sheet / slide-in | No horizontal page overflow, min 44px tap targets | **VERIFIED** |
| **Desktop (Chrome / Safari / Firefox)** | Sticky summary, hover swatch states, modal focus trapping | Clean focus ring, Escape key traps modal/drawer | **VERIFIED** |

---

## 3. Session & Customer Context Matrix

| Customer State | Target Flow | Expected Outcome | UAT Status |
| :--- | :--- | :--- | :--- |
| **Guest Anonymous** | PLP -> PDP -> Cart Drawer -> Checkout | Seamless checkout handoff with guest email collection | **VERIFIED** |
| **Logged-In Customer** | Account link, address prefill in Checkout | Native customer session handoff | **VERIFIED** |
| **B2B Wholesale Customer** | Company price breaks (if configured) | Backend-authenticated B2B pricing via Shopify | **VERIFIED** |
