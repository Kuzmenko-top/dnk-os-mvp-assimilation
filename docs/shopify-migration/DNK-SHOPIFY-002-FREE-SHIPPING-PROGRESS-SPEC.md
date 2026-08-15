# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-002-FREE-SHIPPING-PROGRESS-SPEC.md"
# purpose: "Technical Compatibility & Migration Specification for Free Shipping Progress Block"
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-SHOPIFY-002"]
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-002 — Free Shipping Progress Compatibility Specification

## 1. Legacy Behavior
- **Source File**: `services/dnk_shopify/DNK-e.com/blocks/free-shipping-progress.liquid`
- **Features**: Displayed static threshold message ("Додайте ще 450 ₴") and static progress width ("70%").
- **Limitations**:
  - Hardcoded UAH currency symbol and fixed remaining amount.
  - Lacked dynamic Liquid calculation using `cart.total_price`.
  - Lacked accessibility attributes (`role="progressbar"`, `aria-valuenow`, `aria-live="polite"`).
  - Lacked event listener for AJAX cart updates (`cart:updated`, `cart:refresh`).

---

## 2. Target Horizon Conventions
- **Target File**: `services/dnk_shopify/DNK_Ecom_v1_0_0/blocks/free-shipping-progress.liquid`
- **Architecture**: Shopify Blocks 3.0 Web Component (`<free-shipping-progress>`).
- **Data Model**:
  - Uses `cart.total_price` (in cents / currency subunits).
  - Converts threshold setting (`free_shipping_threshold`) to subunits: `threshold * 100`.
  - Formats remaining amount using Liquid filter `| money`.
  - Calculates percentage dynamically: `current_total * 100 / threshold_subunits`.
- **Accessibility**:
  - Container wraps status text with `aria-live="polite"`.
  - Progress bar container includes `role="progressbar"`, `aria-valuenow`, `aria-valuemin="0"`, `aria-valuemax="100"`.
- **Event Lifecycle**:
  - Encapsulated custom element listens for `cart:updated`, `cart:refresh`, and `cart-drawer:updated` events.
  - Dynamically updates width percentage and status text without full page reload.

---

## 3. Schema & Settings Mapping
| Legacy Setting ID | Target Setting ID | Type | Label / Purpose | Default |
|---|---|---|---|---|
| N/A | `icon_emoji` | `text` | Emoji icon prefix | `"🚚"` |
| N/A | `title` | `text` | Title / Service description | `"Безкоштовна доставка Новою Поштою"` |
| `free_shipping_threshold` | `free_shipping_threshold` | `number` | Threshold in store currency units | `3000` |
| N/A | `remaining_message` | `text` | Status text when below threshold | `"Додайте ще [amount]"` |
| `achieved_message` | `achieved_message` | `text` | Status text when threshold reached | `"🎉 Вітаємо! Ви отримали безкоштовну доставку!"` |

---

## 4. Acceptance Tests & Edge Cases
- **Cart Empty (`cart.item_count == 0`)**: Progress bar displays 0%, displays remaining amount equal to total threshold.
- **Below Threshold (`cart.total_price < threshold_subunits`)**: Progress bar displays proportional width; remaining message correctly formats `[amount]`.
- **Threshold Reached (`cart.total_price >= threshold_subunits`)**: Progress bar displays 100%, text switches to `achieved_message` in emerald color.
- **Threshold Disabled (`threshold == 0`)**: Automatically evaluates as achieved (100%).
- **AJAX Cart Update**: Web component updates width smoothly without DOM re-render errors.
