# author: "DNK-e.com Maksym"
# purpose: "Technical Specification for Wave 3 PDP Conversion Runtime Migration"
# mrh_id: "DNK-SHOPIFY-007-PDP-MIGRATION-SPEC"
# status: "ACTIVE"
# created_at: "2026-08-22"

# DNK-SHOPIFY-007: PDP Migration Technical Specification

## 1. Architectural Architecture & Target Structure

The PDP conversion runtime in `DNK-e.com` utilizes Horizon 2.0 section and block modularity inside `sections/product-information.liquid` and `templates/product.json`.

```text
templates/product.json
  └── sections/product-information.liquid
        ├── snippets/product-media-gallery-content.liquid
        └── snippets/product-information-content.liquid
              ├── blocks/product-title.liquid
              ├── blocks/price.liquid
              ├── blocks/variant-picker.liquid
              ├── blocks/quantity.liquid
              ├── blocks/product-inventory.liquid
              ├── blocks/buy-buttons.liquid
              └── snippets/volume-pricing-info.liquid (Conditional Native)
```

---

## 2. Block Configurations & Settings Blueprint

### 2.1 Variant Picker (`blocks/variant-picker.liquid`)
- **Picker Type**: Button swatches vs dropdown selects (`picker_type`).
- **Swatch Integration**: `snippets/variant-swatches.liquid` for visual color/style swatches.
- **Strikethrough unavailable**: `snippets/strikethrough-variant.liquid` for out-of-stock options.

### 2.2 Quantity Selector (`blocks/quantity.liquid`)
- **Quantity Rules**: Renders `<quantity-selector>` with `data-min="{{ variant.quantity_rule.min }}"` and `data-step="{{ variant.quantity_rule.increment }}"`.

### 2.3 Price Block (`blocks/price.liquid`)
- **Dynamic Re-rendering**: Encapsulated in `<product-price data-block-id="{{ block.id }}">`.
- **Unit Price**: Includes `snippets/unit-price.liquid`.

### 2.4 Buy Buttons (`blocks/buy-buttons.liquid`)
- **Form Component**: `<product-form>` submitting to `/cart/add.js`.
- **Dynamic Checkout Buttons**: Optional Shopify Payment / Apple Pay / Google Pay accelerated checkout buttons.

---

## 3. Data Authority & Metafield Contracts

```yaml
metafield_contracts:
  tier_guidance_display:
    namespace: "dnk_conversion"
    key: "quantity_tiers_json"
    type: "json"
    usage: "DISPLAY_ONLY (for tier guidance when Shopify Function is active)"
    governance_rule: "Must not override variant.price without backend function approval"
```

---

## 4. Quality Gates & Non-Functional Requirements

1. **Performance**: Zero blocking external JS scripts; all PDP JS (`variant-picker.js`, `product-price.js`, `product-form.js`) must be modular and loaded with `defer`.
2. **Accessibility**: ARIA labels on variant swatches, popovers (`volume-pricing-info`), and quantity buttons.
3. **Draft Safety**: No theme Liquid edits applied directly during discovery. Migration code changes must be applied strictly in designated feature branches when authorized.
