# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-015-GIFT-REWARDS-FUNCTIONS-SPEC.md"
# purpose: "Technical Specification for Shopify Functions Gift Rewards"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-015: Gift Rewards & Tiered Promotions Specification

**Task ID**: DNK-SHOPIFY-015  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  

---

## 1. Capability Profile
```yaml
capability:
  business_value: "Increased AOV via spend-threshold free gifts."
  customer_outcome: "Free item automatically awarded in cart at checkout when rules are met."
  implementation_options:
    - "Client-side /cart/add.js loops (Forbidden - Race conditions/Inventory leaks)"
    - "Shopify Functions: Cart Transform API / Discount API (Recommended)"
  recommended_option: "Shopify Functions (Cart Transform API)"
  data_owner: "Shopify Backend (Order Routing & Functions)"
  checkout_authority: "Shopify Functions Engine"
  storefront_responsibilities: 
    - "Display informational progress bar ('Spend $X more for a free gift')"
    - "Render the gift line-item normally once returned by the Cart API"
  backend_responsibilities: 
    - "Evaluate cart total against configured thresholds"
    - "Inject gift line-item at $0.00 via Cart Transform"
    - "Validate inventory levels before injection"
  required_shopify_plan_features: ["Shopify Plus or Functions-enabled store"]
  authentication_and_secrets: "None (Internal Shopify execution)"
  personal_data_and_privacy: "None"
  performance_budget: "< 5ms execution time for WASM Function"
  failure_and_fallback: "Gift is not applied. Order proceeds normally."
  observability: "Shopify Functions run logs in Partner Dashboard."
  estimated_delivery_risk: "high"
```

## 2. Core Mechanics & Guardrails
- **No JS Manipulation**: The theme must not attempt to add or remove the gift item via JavaScript. The Shopify backend handles injection and removal (if cart drops below threshold).
- **Inventory Protection**: The function must not inject a gift if the variant inventory is `0`.
- **Stacking Rules**: Defined strictly within the Shopify Admin discount configuration.

## 3. Acceptance Criteria
- Gift item appears in cart payload automatically upon threshold met.
- Gift item disappears automatically if cart value drops below threshold.
- Zero client-side `/cart/update.js` calls made by the theme to manage the gift.
