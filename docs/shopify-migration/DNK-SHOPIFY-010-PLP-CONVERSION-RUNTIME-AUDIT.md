# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-010-PLP-CONVERSION-RUNTIME-AUDIT.md"
# purpose: "Comprehensive Runtime Audit of Legacy vs Horizon Collection PLP Conversion Architecture"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-010: Collection PLP Conversion Runtime Audit

**Task ID**: DNK-SHOPIFY-010
**Author**: DNK-e.com Maksym
**Date**: 2026-08-22
**Phase**: Wave 4 PLP Discovery and Audit

---

## 1. Executive Summary & Audit Mandate

This audit compares the legacy Shopify theme (`DNK_Ecom_v1_0_0`) collection implementation against the target Horizon architecture (`DNK-e.com`). The goal is to evaluate collection layout, filtering/sorting mechanics, product card composition, pagination, quick add, and cart drawer handoff to confirm zero-gap native Horizon adoption.

Key finding: **Horizon Native 100% Coverage**. No custom AJAX filtering engine or monolithic product card migration is required.

---

## 2. Legacy vs Target Entrypoint Mapping

### Legacy Theme (`DNK_Ecom_v1_0_0`)
- **Template JSON**: `templates/collection.json`
- **Main Section**: `sections/main-collection-product-grid.liquid` (15 KB monolithic section)
- **Banner Section**: `sections/main-collection-banner.liquid` (3.7 KB)
- **Product Card Snippet**: `snippets/card-product.liquid` (28 KB monolith)
- **Filtering Snippet**: `snippets/facets.liquid` (56.5 KB)
- **Filtering Script**: `assets/facets.js` (10 KB)
- **Quick Add Script**: `assets/quick-add.js` (6.7 KB)
- **Pagination Snippet**: `snippets/pagination.liquid` (2.5 KB)

### Target Horizon Theme (`DNK-e.com`)
- **Template JSON**: `templates/collection.json` (modular JSON template)
- **Main Section**: `sections/main-collection.liquid`
- **Filters Block**: `blocks/filters.liquid`
- **Product Card Block**: `blocks/_product-card.liquid` / `blocks/product-card.liquid`
- **Product Card Snippets**: `snippets/product-card.liquid`, `snippets/product-grid.liquid`
- **Filtering Snippets**: `snippets/list-filter.liquid`, `snippets/price-filter.liquid`, `snippets/sorting.liquid`, `snippets/filter-remove-buttons.liquid`, `snippets/grid-density-controls.liquid`
- **Filtering Script**: `assets/facets.js`
- **Quick Add Snippets**: `snippets/quick-add.liquid`, `snippets/quick-add-modal.liquid`
- **Quick Add Script**: `assets/quick-add.js`
- **Pagination Snippet**: `snippets/pagination-controls.liquid`

---

## 3. Section Rendering API & State Management Boundaries

Horizon's filtering and sorting mechanism operates via Shopify's Section Rendering API:

```text
User Interaction (Filter / Sort / Paginate)
       │
       ▼
   facets.js (FacetFiltersForm)
       │
       ├── Build SearchParams URL (e.g. ?filter.v.price.gte=10&sort_by=price-ascending)
       ├── Fetch Section HTML via ?section_id=main-collection
       │
       ▼
   DOM Replacement Boundaries
       ├── #product-grid (Product Cards Container)
       ├── #FacetFiltersForm (Active Filter State & Counts)
       ├── #FilterRemoveButtons (Active Filter Pills)
       └── #pagination-controls (Updated Pagination Links)
       │
       ▼
   History State Sync
       └── history.pushState({}, '', newUrl) + popstate event listener for back/forward
```

### Browser History & Accessibility (a11y)
- `history.pushState` updates the URL state seamlessly without full page reloads.
- `popstate` event listeners intercept browser Back/Forward navigation to re-fetch the exact section state.
- **Focus Management**: Upon DOM replacement, focus is programmatically restored to the active filter trigger or grid boundary (`#product-grid`), preventing focus loss for screen readers.

---

## 4. Performance & Resource Audit

- **AJAX Overhead**: Strictly 1 Section Rendering API fetch per filter/sort/paginate user action (`?section_id=main-collection`).
- **Image Optimization**: Images inside `_product-card-gallery` use native `loading="lazy"` and `srcset` scaling to prevent excessive bandwidth usage.
- **Listener Leak Prevention**: Event listeners are registered via event delegation on stationary containers (`FacetFiltersForm`) or properly cleaned up prior to replacing inner DOM HTML.

---

## 5. Security & Price Authority Compliance

- **Zero Client-Side Discount Math**: Prices rendered on PLP cards strictly derive from Shopify Liquid `product.price`, `product.compare_at_price`, and `product.price_varies`.
- **Zero Cart Mutation on Filter**: Filtering actions perform read-only GET requests for section HTML; no `/cart/add.js` or write operations occur during collection navigation.
