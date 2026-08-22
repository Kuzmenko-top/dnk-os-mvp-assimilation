# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-012-NOVA-POSHTA-CONTRACT.md"
# purpose: "Nova Poshta Carrier Integration & Delivery Data Contract Specification"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-012: Nova Poshta Integration Contract Specification

**Task ID**: DNK-SHOPIFY-012  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 5 Nova Poshta Architecture & Contract  

---

## 1. Architectural Mandate & Non-Negotiables

Direct integration with the Nova Poshta API from storefront theme Liquid or frontend JavaScript is **STRICTLY FORBIDDEN** due to:
- Critical security risk of exposing Nova Poshta API keys in client-side bundles.
- Violation of GDPR / privacy standards (sending PII directly from unauthenticated client browser).
- Price authority breach (theme cannot authoritatively calculate shipping rates or create delivery waybills/TTN).

---

## 2. Canonical Integration Architecture

```text
Storefront (PDP / Cart Drawer)
       │
       ▼ (Informational Only)
   Estimated Shipping Snippet / Block
   - Static estimation based on business rules (e.g. "Відправка сьогодні при замовленні до 15:00")
   - Zero live API calls, zero PII transmission
       │
       ▼ (Checkout Stage)
   Shopify Checkout UI Extension / Carrier Service API
       │
       ├── Server-to-Server Nova Poshta Integration App
       ├── Authenticated Backend Proxy with Secured API Key
       └── Generates official Nova Poshta shipping rates and warehouse selection
```

---

## 3. Formal Capability Contract

```yaml
capability_id: "cart.delivery.nova_poshta"
legacy_sources:
  - "snippets/delivery-date.liquid"
  - "snippets/estimated-shipping.liquid"
  - "snippets/shipping-checkpoints.liquid"
customer_outcome: "Accurate shipping estimation and official Nova Poshta warehouse delivery at checkout."
trigger: "Cart checkout handoff / Informational badge on PDP"
data_owner: "Nova_Poshta & Shopify Carrier Service"
data_source: "Shopify Shipping Rates API / Backend App Proxy"
authentication: "server_side"
external_endpoint: "https://api.novaposhta.ua/v2.0/json/ (Server-side ONLY)"
personal_data_processed:
  - "Recipient City / Region"
  - "Warehouse Ref"
  - "Phone Number & Name (at Checkout)"
consent_or_privacy_basis: "Order fulfillment / GDPR compliant checkout contract"
cache_ttl: "3600s (for warehouse directory on backend)"
timeout_ms: 3000
fallback_ui: "Standard flat-rate shipping selection or contact manager note"
failure_mode: "Graceful fallback to standard Shopify checkout delivery options"
cart_or_checkout_authority: "Checkout Shipping Rates Engine"
Horizon_integration_point: "Informational badges in blocks/_product-card.liquid or cart drawer footer"
theme_only_feasible: false
decision: "DEFER"
evidence:
  - "No hardcoded Nova Poshta API keys present in theme code"
  - "Legacy theme only performed client date calculations"
```
