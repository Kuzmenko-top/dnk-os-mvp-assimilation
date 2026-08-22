# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-011-PLP-MERCHANDISING-SPEC.md"
# purpose: "Wave 4A PLP Merchandising Native Block Adaptation Specification"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-011: PLP Merchandising Native Block Adaptation Specification

**Task ID**: DNK-SHOPIFY-011  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 4A Merchandising Adaptation  

---

## 1. Architectural Scope & Invariants

This specification defines the adaptation of native merchandising elements on product listing cards within the Horizon theme (`DNK-e.com`).

### Core Rules
1. **0 DOM Output Rule**: If metadata for review ratings, swatches, or badges does not exist or is empty for a product, no empty wrapper containers, placeholders, or broken DOM nodes shall be rendered.
2. **Price Authority Invariant**: No frontend JavaScript or Liquid math may calculate discounts, tier pricing, or promotional claims. All pricing displays strictly render native Liquid attributes (`product.price`, `product.compare_at_price`, `product.price_varies`).
3. **Native Runtime Boundary**: No changes to `sections/main-collection.liquid`, `blocks/filters.liquid`, `assets/facets.js`, or native quick-add / pagination / cart drawer components.

---

## 2. Merchandising Module Specifications

### A. Review Ratings & Count (`blocks/review.liquid`)
- **Condition**: Renders ONLY when `product.metafields.reviews.rating.value.rating != blank`.
- **Display**: Accessible SVG stars with rating count and numerical score.
- **Null State**: Entire block is skipped (`{%- if rating != blank -%}`), resulting in 0 DOM output.

### B. Variant Swatches (`blocks/swatches.liquid` & `snippets/variant-swatches.liquid`)
- **Condition**: Renders ONLY when `swatch_count > 0` across product option values.
- **Display**: Interactive swatch pills mapped directly from variant image/color metadata.
- **Null State**: Entire `<product-swatches>` element is omitted, resulting in 0 DOM output.

### C. Product Badges (`blocks/_product-card-gallery.liquid`)
- **Condition**: Renders ONLY when `product.available == false` (Sold Out) OR `product.compare_at_price > product.price` (Sale).
- **Display**: Rectangular badge styled via `snippets/product-badges-styles.liquid`.
- **Null State**: Entire `.product-badges` wrapper is skipped, resulting in 0 DOM output.

---

## 3. Scope Controls

### Allowed File Paths
- `blocks/_product-card.liquid`
- `snippets/product-card.liquid`
- `snippets/product-card-*.liquid`
- `assets/dnk-product-card.css`
- `docs/migration/DNK-SHOPIFY-011-*.md`

### Forbidden File Paths
- `sections/main-collection.liquid`
- `blocks/filters.liquid`
- `assets/facets.js`
- `snippets/list-filter.liquid`
- `snippets/price-filter.liquid`
- `snippets/sorting.liquid`
- `snippets/product-grid.liquid`
- `snippets/quick-add.liquid`
- `snippets/quick-add-modal.liquid`
- `assets/quick-add.js`
- `assets/variant-picker.js`
- `assets/product-form.js`
- `snippets/cart-drawer.liquid`
- `assets/dnk-cart-drawer-adapter.js`
- `config/settings_schema.json`
- `config/settings_data.json`
