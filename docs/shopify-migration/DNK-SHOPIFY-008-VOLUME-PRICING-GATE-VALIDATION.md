# author: "DNK-e.com Maksym"
# purpose: "Validation of Volume Pricing Governance Gate for Wave 3.2"
# mrh_id: "DNK-SHOPIFY-008-VOLUME-PRICING-GATE-VALIDATION"
# status: "ACTIVE"
# created_at: "2026-08-22"

# DNK-SHOPIFY-008: Volume Pricing Gate Validation

## 1. Governance Gate Principles

1. **Checkout Price Authority**: Theme Liquid must NEVER calculate or promise discounts that checkout cannot verify.
2. **Shopify Native Volume Pricing**: Uses official `variant.quantity_price_breaks` (B2B/Catalogs/Functions).
3. **Display-Only Boundary**: If `quantity_price_breaks` is empty, block remains completely hidden.

---

## 2. Validation Matrix

| Test Scenario | Input Data | Expected UI Behavior | Verified Status |
| :--- | :--- | :--- | :--- |
| **Standard Product (D2C)** | `variant.quantity_price_breaks = []`, `quantity_rule.min = 1` | Block is hidden; 0 DOM output; standard PDP conversion | **PASSED** |
| **Product with Minimum Quantity Rule** | `quantity_rule.min = 3`, `quantity_rule.increment = 3` | Block renders quantity rule hint popover ("Minimum: 3, Increments: 3") | **PASSED** |
| **Product with B2B/Catalog Quantity Price Breaks** | `quantity_price_breaks = [{min: 5, price: 8000}, {min: 10, price: 7000}]` | Popover table renders tiers; active tier highlights when quantity matches | **PASSED** |
| **Variant Switching** | Switch between Variant A (no breaks) and Variant B (has breaks) | Block dynamically shows/hides via `assets/variant-picker.js` DOM replacement | **PASSED** |
| **Cart Drawer Sync** | Add quantity to cart | `cart-drawer` renders items with verified line prices | **PASSED** |

---

## 3. Legacy Exclusions Confirmed

- Legacy `snippets/quantity-breaks.liquid`: **EXCLUDED**
- Legacy `snippets/buy-more-discounts.liquid`: **EXCLUDED**
- Artificial Timer (`timer.js`): **EXCLUDED**
