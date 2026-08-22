# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-011-PLP-VALIDATION.md"
# purpose: "PLP Merchandising Adaptation Acceptance Test & Validation Matrix"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-011: PLP Validation & Acceptance Matrix

**Task ID**: DNK-SHOPIFY-011  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 4A Acceptance Testing  

---

## 1. Acceptance Test Matrix

| Test ID | Scenario | Execution Procedure | Expected Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-011-01** | Product without rating / badge metadata | Inspect DOM of product card with 0 reviews & equal price/compare_at. | **0 DOM output** for `.rating-wrapper` and `.product-badges`. No empty wrapper `<div>` nodes. | **PASS** |
| **TC-011-02** | Product with valid review rating | Inspect product card with `metafields.reviews.rating` populated. | Renders star icons, rating value, and review count cleanly with full ARIA accessibility. | **PASS** |
| **TC-011-03** | Product with color swatch options | Inspect product card with color swatches defined in variant options. | Interactive `<product-swatches>` element rendered with proper image/color swatches. | **PASS** |
| **TC-011-04** | Sold Out product state | Inspect product card with `product.available == false`. | Sold Out badge renders; native availability state remains unchanged. | **PASS** |
| **TC-011-05** | Sale product state | Inspect product card with `product.compare_at_price > product.price`. | Sale badge renders; `product.price` and `product.compare_at_price` render natively without frontend math. | **PASS** |
| **TC-011-06** | Facet Filter / Sort / Paginate | Interact with URL filters (`?filter.v.price...`), sorting, and page controls. | Native URL state updates, Section Rendering API updates grid seamlessly without full page reload. | **PASS** |
| **TC-011-07** | Quick Add & Cart Drawer Handoff | Click Quick Add button on product card, select variant, submit form. | Quick Add modal traps focus; form submission dispatches `cart:update` event to `dnk-cart-drawer-adapter`. | **PASS** |
| **TC-011-08** | Responsive Card Layout | Test card grid on 320px mobile viewport up to 1920px desktop screen. | Grid layout is stable; 0 horizontal overflow; touch targets meet 44px min size. | **PASS** |
| **TC-011-09** | Console & Network Cleanliness | Open browser DevTools console & network tab during navigation. | 0 JavaScript console errors; 0 unexpected external HTTP requests. | **PASS** |

---

## 2. Security & Compliance Checklist

- [x] Zero client-side discount math in JS/Liquid.
- [x] Zero promotional claim fabrication.
- [x] Zero modifications to forbidden files (`sections/main-collection.liquid`, `blocks/filters.liquid`, `assets/facets.js`).
- [x] Zero direct Cart API calls during filter/sort operations.
- [x] Zero external HTTP/3rd-party requests added.
