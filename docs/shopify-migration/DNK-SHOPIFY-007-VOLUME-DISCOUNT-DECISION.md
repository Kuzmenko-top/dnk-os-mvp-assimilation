# author: "DNK-e.com Maksym"
# purpose: "Governance Decision and Price Authority Audit for PDP Volume Discounts"
# mrh_id: "DNK-SHOPIFY-007-VOLUME-DISCOUNT-DECISION"
# status: "ACTIVE"
# created_at: "2026-08-22"

# DNK-SHOPIFY-007: Volume Discount Governance Decision

## 1. Context & Governance Imperative

In Wave 2A (Cart Drawer), Volume Discount was deferred to Wave 3 (Product Conversion Runtime) so that price authority, variant selection, quantity rules, and currency settings could be verified on the PDP before any discounted pricing claim appears in the cart.

The fundamental governance principle enforced across DNK OS E-commerce is:
> **The theme Liquid/JS layer may render tier guidance, but MAY NOT independently promise or fake checkout prices that the Shopify checkout engine is incapable of confirming.**

---

## 2. Price Authority Audit

We evaluated all 6 potential Price Authorities for the legacy Volume Discount (`snippets/quantity-breaks.liquid`):

| Possible Price Authority | Evaluation for Legacy `quantity-breaks.liquid` | Verified Status |
| :--- | :--- | :--- |
| **Shopify Automatic Discount** | Not configured or bound to theme customizer block settings | ❌ Unverified |
| **Shopify Functions** | No active Shopify Function detected for customizer tier settings | ❌ Unverified |
| **Shopify App** | No backend app contract mapping `option_1_quantity` to checkout lines | ❌ Unverified |
| **Shopify B2B / Catalog Pricing** | Supported natively in Horizon (`variant.quantity_price_breaks`), but not used by legacy customizer block | ❌ Unverified for legacy |
| **Metafield Display-Only** | Legacy uses block settings, not structured metafields | ❌ Unverified |
| **No Verified Authority** | **Legacy calculates tier prices purely via frontend Liquid math and JS DOM tricks without checkout enforcement** | **CONFIRMED** |

---

## 3. Official Governance Decision

```yaml
volume_discount_status: DISPLAY_ONLY_MANUAL_REVIEW
implementation: FORBIDDEN_IN_THEME_LIQUID
action_taken:
  - Legacy snippets/quantity-breaks.liquid IS EXCLUDED from migration.
  - No custom frontend price-faking scripts will be ported to Horizon.
  - Native Shopify Volume Pricing (snippets/volume-pricing-info.liquid) is adopted as the sole approved extension point when B2B / Quantity Price Breaks are enabled.
```

---

## 4. Migration & Integration Strategy

1. **Horizon Native Standard**:
   - Use Horizon's native `snippets/volume-pricing-info.liquid` and `assets/price-per-item.js`.
   - Native volume pricing relies directly on Shopify's official `variant.quantity_price_breaks` and `variant.quantity_rule`, which are **100% verified server-side at Shopify checkout**.

2. **Future Wave 3.2 / Wave 5 Upgrade Path**:
   - If marketing requires tiered quantity discounts for standard D2C products without B2B, the merchant must deploy a **Shopify Function (Discounts API)** or a verified Shopify App.
   - Once a server-side discount contract is verified, tier badges may be rendered via standard theme blocks.
