# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-015-NOVA-POSHTA-ARCHITECTURE-SPEC.md"
# purpose: "Technical Architecture for Secure Nova Poshta Integration"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-015: Nova Poshta Architecture Specification

**Task ID**: DNK-SHOPIFY-015  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  

---

## 1. Capability Profile
```yaml
capability:
  business_value: "Accurate shipping costs and warehouse selection for Ukrainian market."
  customer_outcome: "Select exact Nova Poshta branch/postomat at checkout."
  implementation_options:
    - "Theme JavaScript direct API calls (Forbidden - Security Risk)"
    - "Custom App Proxy + Checkout UI Extension (Recommended)"
  recommended_option: "Custom App Proxy + Checkout UI Extension"
  data_owner: "Nova Poshta & Shopify Carrier Service API"
  checkout_authority: "Shopify Checkout Shipping Engine"
  storefront_responsibilities: 
    - "Render static informational delivery estimates (e.g., 'Delivery in 1-2 days')"
  backend_responsibilities: 
    - "Securely store Nova Poshta API Token"
    - "Query cities and warehouses via App Proxy"
    - "Generate Carrier Service shipping rates"
    - "Automate TTN (Waybill) generation on order paid"
  required_shopify_plan_features: ["Carrier Calculated Shipping (CCS) / Advanced Plan"]
  authentication_and_secrets: "Backend isolated DB/Vault (Never exposed to Storefront)"
  personal_data_and_privacy: "GDPR minimal; only name/phone sent to NP upon order creation."
  performance_budget: "App Proxy response < 1000ms"
  failure_and_fallback: "Standard flat-rate shipping option if API is down."
  observability: "App-level logging (Datadog/Sentry) for NP API timeouts."
  estimated_delivery_risk: "high"
```

## 2. Storefront (Theme) vs Checkout Boundary
- **Storefront (Theme)**: Strictly informational. No API calls to NP.
- **Checkout (UI Extension)**: Renders the custom warehouse picker dropdown securely within the Shopify Checkout sandbox.

## 3. Acceptance Criteria
- Zero NP API keys found in theme code (`.liquid`, `.js`).
- Warehouse selection occurs inside Checkout, not Cart Drawer.
- Fallback shipping rate exists if Nova Poshta API fails.
