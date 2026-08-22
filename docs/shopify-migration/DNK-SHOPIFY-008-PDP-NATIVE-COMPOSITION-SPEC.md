# author: "DNK-e.com Maksym"
# purpose: "Horizon PDP Native Block Composition & Volume Pricing Integration Spec"
# mrh_id: "DNK-SHOPIFY-008-PDP-NATIVE-COMPOSITION-SPEC"
# status: "ACTIVE"
# created_at: "2026-08-22"

# DNK-SHOPIFY-008: Horizon PDP Native Block Composition Specification

## 1. Architectural Blueprint: `sections/product-information.liquid`

The product details layout in Horizon/Tinker relies on modular theme blocks (`@theme`) defined under `blocks/`. The canonical block order for high conversion and compliance is:

```text
Section: product-information
  ├── Block: product-title (Heading & Title)
  ├── Block: price (Dynamic regular & compare-at price)
  ├── Block: dnk-volume-pricing-info (Shopify Native Quantity Price Breaks, conditional)
  ├── Block: variant-picker (Swatches / Pill buttons / Dropdowns)
  ├── Block: quantity (Quantity selector with quantity_rule min/step)
  ├── Block: product-inventory (Stock status badge)
  ├── Block: buy-buttons (Add to cart + Dynamic Checkout Buttons)
  ├── Block: trust-badges (Wave 2A consumer protection & guarantees)
  └── Block: product-description (Accordion / Rich Text description)
```

---

## 2. Block Implementation: `blocks/dnk-volume-pricing-info.liquid`

```liquid
{%- liquid
  assign product_resource = closest.product
  assign selected_variant = product_resource.selected_or_first_available_variant
  assign show_label = block.settings.show_label
-%}

{%- if selected_variant.quantity_price_breaks.size > 0 or selected_variant.quantity_rule.min > 1 or selected_variant.quantity_rule.increment > 1 -%}
  <div class="dnk-volume-pricing-info-block" {{ block.shopify_attributes }}>
    {% render 'volume-pricing-info',
      variant: selected_variant,
      show_label: show_label
    %}
  </div>
{%- endif -%}
```

---

## 3. Governance & Quality Gates

- **Zero JS Price Overrides**: All prices are rendered strictly via `variant.quantity_price_breaks` and Shopify formatted currency.
- **Auto-Hide Condition**: If `selected_variant.quantity_price_breaks` is empty and quantity rules are standard (min=1, increment=1), the block renders 0 DOM elements.
- **Zero Frontend Faking**: No hardcoded tiers, no static countdowns, no unverified discount claims.
