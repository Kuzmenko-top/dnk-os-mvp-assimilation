# DNK-SHOPIFY-006-CART-DRAWER-CAPABILITY-REGISTER
**Task ID**: DNK-SHOPIFY-006
**Author**: DNK-e.com Maksym
**Date**: 2026-08-16

---

## Capabilities Register

### 1. `cart.shipping.free_shipping_progress`
- **Legacy sources**: `snippets/cart-progress-bar.liquid`, `snippets/cart-checkpoints-bar.liquid`
- **Customer outcome**: Motivates cart size increase to reach free delivery threshold.
- **Data authority**: `cart.total_price` (Subunits calculation).
- **Horizon placement**: DNK extension zone inside Cart Drawer.
- **Decision**: **ADAPT** (`blocks/free-shipping-progress.liquid`).

### 2. `cart.trust.badges_and_guarantee`
- **Legacy sources**: `snippets/moneybackcheckcart.liquid`
- **Customer outcome**: Reassures customer regarding return policy and SSL security.
- **Data authority**: Consumer Protection Law / Store Policy.
- **Horizon placement**: DNK extension zone inside Cart Drawer.
- **Decision**: **ADAPT** (`blocks/trust-badges.liquid`).

### 3. `cart.trust.payment_icons`
- **Legacy sources**: `blocks/payment-icons.liquid`
- **Customer outcome**: Displays accepted payment methods.
- **Data authority**: `shop.enabled_payment_types`.
- **Decision**: **REPLACE_WITH_HORIZON_NATIVE** (Horizon payment_icons block).

### 4. `cart.pricing.volume_discount`
- **Legacy sources**: `snippets/cart-fomo-block.liquid`
- **Customer outcome**: Displays volume discount tiers.
- **Data authority**: Shopify Functions / Checkout authority.
- **Decision**: **DEFER** (Must establish checkout pricing contract in Wave 3).

### 5. `cart.delivery.nova_poshta`
- **Legacy sources**: `snippets/cart-checkpoints-bar.liquid`
- **Customer outcome**: Informs customer about Nova Poshta delivery options.
- **Data authority**: Nova Poshta API / Carrier Service.
- **Decision**: **DEFER** (Wave 5 Integrations).

### 6. `cart.upsell.product_recommendations`
- **Legacy sources**: `snippets/cart-gift.liquid`
- **Customer outcome**: Recommends complementary products.
- **Data authority**: Shopify Recommendations API.
- **Decision**: **DEFER** (Wave 5 Integrations).

### 7. `cart.urgency.countdown_fomo`
- **Legacy sources**: `snippets/cart-fomo-block.liquid`
- **Customer outcome**: Artificial urgency countdown timer.
- **Data authority**: Theme display only.
- **Decision**: **EXCLUDE** (Violates truthfulness & privacy rules).
