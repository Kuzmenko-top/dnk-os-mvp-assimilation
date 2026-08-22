# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-012-INTEGRATION-RISK-MATRIX.md"
# purpose: "Security, Privacy, Price Authority, and Performance Risk Matrix for External Integrations"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-012: External Integration Risk Matrix

**Task ID**: DNK-SHOPIFY-012  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 5 Integration Risk Assessment  

---

## 1. Risk Evaluation Matrix

| Risk ID | Integration / Feature | Failure Mode | Impact Severity | Probability | Mitigation Strategy | Governance Mandate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RISK-012-01** | Nova Poshta API Key Exposure | API Key embedded in Liquid/JS bundle | **CRITICAL** | Low | Server-side App Proxy or Checkout UI Extension only. Zero keys in theme. | **ENFORCED** |
| **RISK-012-02** | Client-Side Cart Gift Desync | JS auto-adds gift item but backend removes it at checkout due to discount mismatch | **HIGH** | High | Migrate gift logic to Shopify Functions Cart Transform API. Disallow theme `/cart/add.js` loops. | **ENFORCED** |
| **RISK-012-03** | Third-party API Latency & Blocking | External shipping API hangs, blocking PDP or Cart Drawer rendering | **HIGH** | Medium | Theme only renders static fallback / Shopify CDN data. External calls asynchronous with strict 2000ms timeout. | **ENFORCED** |
| **RISK-012-04** | PII Leak via Unauthenticated Requests | Customer phone/address sent to unvetted frontend webhook | **CRITICAL** | Low | All checkout PII strictly confined to Shopify Checkout sandbox. | **ENFORCED** |
| **RISK-012-05** | Broken Recommendations Empty State | Recommendation endpoint returns 0 items, leaving broken empty card container | **MEDIUM** | Medium | Enforce **0 DOM output** rule via JavaScript/Liquid check (`if (recommendations.length === 0) container.remove()`). | **ENFORCED** |

---

## 2. Summary Governance Decision

All complex external integrations (Live Nova Poshta rate calculation & TTN generation, Tiered Gift auto-injection) are formally classified as **Backend / App / Checkout UI Extension responsibilities** and are strictly excluded from theme-level Liquid hacks.
