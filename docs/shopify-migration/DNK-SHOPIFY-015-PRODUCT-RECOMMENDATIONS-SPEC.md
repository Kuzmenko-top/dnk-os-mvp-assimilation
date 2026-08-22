# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-015-PRODUCT-RECOMMENDATIONS-SPEC.md"
# purpose: "Technical Specification for Native Shopify Product Recommendations"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-015: Product Recommendations Specification

**Task ID**: DNK-SHOPIFY-015  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  

---

## 1. Capability Profile
```yaml
capability:
  business_value: "Increased AOV and item discovery on PDP and Cart Drawer."
  customer_outcome: "Relevant products shown based on current item or cart contents."
  implementation_options:
    - "Legacy custom Liquid loops (Forbidden)"
    - "Third-party recommendations App (High Overhead)"
    - "Native Horizon block + Shopify Search & Discovery API (Recommended)"
  recommended_option: "Native Horizon block + Shopify Search & Discovery API"
  data_owner: "Shopify (Search & Discovery App)"
  checkout_authority: "Shopify Catalog Engine"
  storefront_responsibilities: 
    - "Render `product-recommendations` web component"
    - "Handle empty states (0 DOM output)"
  backend_responsibilities: 
    - "Algorithm routing (Related vs. Complementary)"
  required_shopify_plan_features: ["Shopify Search & Discovery App (Free)"]
  authentication_and_secrets: "None (Public Storefront API)"
  personal_data_and_privacy: "None (Session contextual only)"
  performance_budget: "< 500ms API response; lazy-loaded block"
  failure_and_fallback: "Component self-destructs (display: none) if fetch fails or returns 0 items."
  observability: "Shopify Analytics (recommendation click-through rate)"
  estimated_delivery_risk: "low"
```

## 2. Intent Distinction
- **Related Products (`intent=related`)**: Substitutes or visually similar items (e.g., other t-shirts).
- **Complementary Products (`intent=complementary`)**: Add-ons (e.g., batteries for a flashlight), managed explicitly via Shopify Search & Discovery app.

## 3. Inventory & Market Rules
- Out-of-stock products are automatically omitted by the API by default.
- Currency and pricing are automatically localized to the active Shopify Market.

## 4. Acceptance Criteria
- `product-recommendations` component fetches data asynchronously.
- 0 DOM layout shift on load.
- If response is empty, block is fully hidden.
