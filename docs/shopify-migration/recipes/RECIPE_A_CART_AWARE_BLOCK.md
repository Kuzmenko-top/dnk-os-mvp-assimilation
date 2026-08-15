# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/recipes/RECIPE_A_CART_AWARE_BLOCK.md"
# purpose: "Canonical Migration Recipe A for Cart-Aware Interactive Theme Blocks"
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-SHOPIFY-003"]
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# Canonical Recipe A: Cart-Aware Interactive Theme Block Migration

## 📌 Overview
This recipe defines the standardized procedure for migrating legacy Shopify interactive blocks that depend on cart state (`cart.total_price`, `cart.item_count`) into Horizon Blocks 3.0 compatible theme blocks.

---

## 🏗️ Step-by-step Transformation Pipeline

### Step 1: Encapsulated Web Component Wrapper
Wrap the Liquid markup in a custom HTML element (e.g. `<free-shipping-progress>`) to prevent global scope leaks and enable lifecycle management.

### Step 2: Guarded Custom Element Registration
Always check if the custom element is already registered before calling `customElements.define()`:
```javascript
if (!customElements.get('block-element-name')) {
  customElements.define('block-element-name', class extends HTMLElement { ... });
}
```

### Step 3: Event-Driven Cart Listener
Attach listeners to standard Shopify and Horizon cart events:
- `cart:updated`
- `cart:refresh`
- `cart-drawer:updated`

### Step 4: Subunit Price Calculations
All money calculations in Liquid and JavaScript MUST use currency subunits (cents):
- Liquid: `assign threshold_subunits = threshold_value | times: 100`
- JavaScript: `const percent = Math.min(100, Math.round((totalPriceSubunits / thresholdSubunits) * 100));`

### Step 5: Accessibility Standard (ARIA)
- Container wrapping updated status text MUST feature `aria-live="polite"`.
- Progress bar container MUST feature `role="progressbar"`, `aria-valuenow`, `aria-valuemin="0"`, `aria-valuemax="100"`.

### Step 6: Theme Editor Attributes
Attach `{{ block.shopify_attributes }}` to the root custom element for native Shopify Theme Editor interaction.
