# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-010-PLP-NATIVE-COMPOSITION-SPEC.md"
# purpose: "Horizon Native PLP Composition Specification and Data Contract Reference"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-010: PLP Native Composition Specification

**Task ID**: DNK-SHOPIFY-010
**Author**: DNK-e.com Maksym
**Date**: 2026-08-22
**Phase**: Wave 4 Native Composition Specification

---

## 1. Product Card Data Contract

The Horizon product card architecture (`blocks/_product-card.liquid`, `snippets/product-card.liquid`) binds strictly to native Shopify objects:

```yaml
product_card_data_contract:
  title: "product.title"
  url: "product.url"
  featured_image: "product.featured_media"
  secondary_image: "product.media[1]"
  price: "product.price"
  compare_at_price: "product.compare_at_price"
  price_varies: "product.price_varies"
  available: "product.available"
  swatches: "product.options_with_values (Color / Material)"
  badges:
    sale: "product.compare_at_price > product.price"
    sold_out: "product.available == false"
    custom_tags: "product.tags (e.g. 'New', 'Bestseller')"
  ratings_metafield:
    rating_value: "product.metafields.reviews.rating.value.rating"
    rating_scale_max: "product.metafields.reviews.rating.value.scale_max"
    rating_count: "product.metafields.reviews.rating_count"
```

---

## 2. Filter URL Contracts & Examples

Horizon filters format query parameters compliant with Shopify's Search & Discovery standard:

| Filter Type | URL Query Parameter Pattern | Example URL |
| :--- | :--- | :--- |
| **Price Range** | `filter.v.price.gte` / `filter.v.price.lte` | `?filter.v.price.gte=10.00&filter.v.price.lte=100.00` |
| **Availability** | `filter.v.availability` | `?filter.v.availability=1` |
| **Vendor** | `filter.p.vendor` | `?filter.p.vendor=DNK` |
| **Product Type** | `filter.p.m.custom.type` | `?filter.p.m.custom.type=Shirt` |
| **Variant Option** | `filter.v.option.<name>` | `?filter.v.option.color=Black&filter.v.option.size=M` |
| **Sort Order** | `sort_by` | `?sort_by=price-ascending` |

---

## 3. Grid Density Contract

Grid density control (`snippets/grid-density-controls.liquid`) operates as an interactive UI toggle on the PLP header:
- **Values**: `small` (high density, 5 columns), `medium` (standard, 4 columns), `large` (large cards, 3 columns).
- **CSS Custom Property State**: Sets `data-grid-density="small|medium|large"` on `#product-grid`.
- **URL / Cookie Sync**: Preserves user preference in local browser session without triggering full page re-fetches.

---

## 4. Quick Add & Cart Drawer Handoff Contract

```text
Product Card "Quick Add" Click
       │
       ▼
   snippets/quick-add.liquid / quick-add-modal.liquid
       │
       ├── Displays variant picker / options
       ├── User submits form POST /cart/add.js
       │
       ▼
   Cart State Change Event (`cart:update` / `cart:refresh`)
       │
       ▼
   dnk-cart-drawer-adapter / Horizon Cart Drawer
       ├── Re-fetches drawer section HTML
       └── Opens Drawer with new line item
```

---

## 5. Accessibility (a11y) Invariants

- **Filter Accordions / Drawers**: Controlled via `<button aria-expanded="true|false" aria-controls="FilterDrawer">`.
- **Quick Add Modal**: Traps keyboard focus (`Tab` / `Shift+Tab`) inside modal bounds; restores focus to trigger button upon close (`Escape` or backdrop click).
- **Section Rerender Announcement**: Uses an `aria-live="polite"` region to announce updated product count (e.g. "Showing 12 of 48 products").
