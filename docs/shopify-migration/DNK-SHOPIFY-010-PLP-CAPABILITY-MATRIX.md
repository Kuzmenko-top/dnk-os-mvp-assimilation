# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-010-PLP-CAPABILITY-MATRIX.md"
# purpose: "PLP Feature Disposition and Capability Decision Matrix for Wave 4 Migration"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-010: PLP Capability Decision Matrix

**Task ID**: DNK-SHOPIFY-010
**Author**: DNK-e.com Maksym
**Date**: 2026-08-22
**Phase**: Wave 4 Capability Matrix

---

## 1. Capability Decision Summary

All legacy PLP features have been classified into four canonical governance categories:
- `REPLACE_WITH_HORIZON_NATIVE`: Native Horizon implementation supersedes legacy code.
- `ADAPT`: Preserved feature adapted to fit Horizon Liquid block structure.
- `DEFER`: Non-critical feature deferred to future release waves.
- `EXCLUDE`: Legacy/deprecated custom code removed permanently.

---

## 2. Detailed Capability Disposition Matrix

| Feature ID | Feature Description | Legacy Implementation | Horizon Target Status | Disposition | Rationalization |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PLP-CAP-001** | Collection Banner & Description | `sections/main-collection-banner.liquid` | `templates/collection.json` (`section` + `text`/`image` blocks) | `REPLACE_WITH_HORIZON_NATIVE` | Horizon composable blocks give superior layout control in Theme Editor. |
| **PLP-CAP-002** | Main Product Grid Layout | `sections/main-collection-product-grid.liquid` (15 KB) | `sections/main-collection.liquid` + `snippets/product-grid.liquid` | `REPLACE_WITH_HORIZON_NATIVE` | Horizon CSS Grid layout is lighter, responsive, and maintainable. |
| **PLP-CAP-003** | Product Card Rendering | `snippets/card-product.liquid` (28 KB monolith) | `blocks/_product-card.liquid` / `snippets/product-card.liquid` | `REPLACE_WITH_HORIZON_NATIVE` | Replaces monolithic Liquid file with clean, modular blocks. |
| **PLP-CAP-004** | Faceted Filtering & Sorting | `snippets/facets.liquid` + `assets/facets.js` | `blocks/filters.liquid` + `assets/facets.js` | `REPLACE_WITH_HORIZON_NATIVE` | Horizon natively handles all Search & Discovery filters via Section Rendering API. |
| **PLP-CAP-005** | Grid Density Controls | Non-existent in legacy theme | `snippets/grid-density-controls.liquid` | `REPLACE_WITH_HORIZON_NATIVE` | Adds new Horizon native functionality for desktop/mobile grid switching. |
| **PLP-CAP-006** | Pagination Controls | `snippets/pagination.liquid` | `snippets/pagination-controls.liquid` | `REPLACE_WITH_HORIZON_NATIVE` | Native Horizon pagination preserves URL search params during page turns. |
| **PLP-CAP-007** | Quick Add & Variant Modal | Custom modal in `card-product.liquid` | `snippets/quick-add.liquid` + `quick-add-modal.liquid` | `REPLACE_WITH_HORIZON_NATIVE` | Standardized modal with focus trapping and accessible ARIA markup. |
| **PLP-CAP-008** | Swatches & Color Badges | Custom Liquid logic in `card-product.liquid` | `swatches` block inside `_product-card` | `ADAPT` | Variant swatches rendered natively using Horizon swatch settings. |
| **PLP-CAP-009** | Reviews & Ratings Display | `metafields.reviews.rating` in `card-product` | Standard Liquid metafield binding in `product-card` | `ADAPT` | Uses standard Shopify Product Reviews / Judge.me metafield mapping. |
| **PLP-CAP-010** | Custom Price Color Customizer | `custompricecolors` setting in legacy section | Horizon Color Palette Settings (`settings.color_palette`) | `EXCLUDE` | Custom hardcoded color settings violate Horizon global design system. |
| **PLP-CAP-011** | Promotional Banner In-Grid Cards | Legacy custom inline collection menu | Standard Horizon Collection Blocks | `DEFER` | Merchandising banner cards can be added in Wave 5 if marketing requires. |
