# author: "DNK-e.com Maksym"
# purpose: "Variant, Quantity, Price & Cart Handoff Contracts for Wave 3 PDP Conversion Runtime"
# mrh_id: "DNK-SHOPIFY-007-VARIANT-QUANTITY-PRICE-CONTRACT"
# status: "ACTIVE"
# created_at: "2026-08-22"

# DNK-SHOPIFY-007: Variant, Quantity & Price Contracts

## 1. Variant Change Lifecycle Contract

```yaml
lifecycle_id: pdp.variant.selection_change
trigger_event: "change" on <variant-picker> radio/select inputs
handler: assets/variant-picker.js + assets/variant-resolution.js
dispatched_events:
  - "variant:change"
  - "product:select"
state_updates:
  url: "history.replaceState({}, '', '?variant=' + selectedVariant.id)"
  price_renderer: "<product-price>" listens to "product:select" and replaces DOM element via Section Rendering API or cached payload
  media_gallery: "<product-gallery>" updates active slide to match variant.featured_media
  inventory_status: "<product-inventory>" updates stock status (In stock / Low stock / Sold out)
  buy_buttons: "<buy-buttons>" updates submit button state (Add to Cart vs Sold Out / Disabled)
```

---

## 2. Quantity Lifecycle Contract

```yaml
lifecycle_id: pdp.quantity.change
trigger_event: "input" / "change" on <quantity-selector> input
handler: assets/component-quantity-selector.js
validations:
  min_quantity: "variant.quantity_rule.min" (default: 1)
  max_quantity: "variant.quantity_rule.max" (default: null / unlimited)
  increment_step: "variant.quantity_rule.increment" (default: 1)
state_updates:
  input_value: "Clamped to [min, max] and aligned to increment step"
  subtotal_display: "Recalculated if subtotal block exists"
  volume_pricing_highlight: "Active tier in snippets/volume-pricing-info.liquid updated dynamically"
```

---

## 3. Price Rendering Contract

```yaml
contract_id: pdp.price.render_rules
components:
  - blocks/price.liquid
  - snippets/price.liquid
  - snippets/format-price.liquid
  - snippets/unit-price.liquid
rules:
  regular_price: "Renders variant.price using shop.money_format or shop.money_with_currency_format"
  compare_at_price: "Renders variant.compare_at_price with strikethrough iff variant.compare_at_price > variant.price"
  unit_price: "Renders variant.unit_price and variant.unit_price_measurement if present"
  taxes_and_shipping: "Renders tax and shipping notes based on cart.taxes_included and shop.shipping_policy"
```

---

## 4. Add-To-Cart & Cart Drawer Handoff Contract

```yaml
contract_id: pdp.cart.add_to_cart_handoff
form_element: "<product-form>" in blocks/buy-buttons.liquid
payload:
  id: "selected_variant_id"
  quantity: "quantity_input_value"
  properties: "optional custom line item properties"
ajax_endpoint: "/cart/add.js" (or /cart/add?sections=cart-drawer)
event_flow:
  1. User clicks submit in <product-form>
  2. JS intercepts submit, sets loading state on buy button
  3. POST fetch to /cart/add.js
  4. On HTTP 200 OK:
     a. Dispatches "cart:updated" custom event on document.body
     b. Cart Drawer (<cart-drawer>) catches "cart:updated"
     c. Cart Drawer fetches updated section HTML via Section Rendering API (?sections=cart-drawer)
     d. Cart Drawer updates line items, totals, and Free Shipping Progress Bar
     e. Cart Drawer executes slide-in animation (open)
  5. On HTTP 422 / Error:
     a. Displays error message (e.g. "Quantity exceeds available stock") inside <product-form>
```
