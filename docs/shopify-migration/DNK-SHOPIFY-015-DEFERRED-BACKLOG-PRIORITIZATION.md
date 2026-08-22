# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-015-DEFERRED-BACKLOG-PRIORITIZATION.md"
# purpose: "Wave 8 Prioritization Matrix for Deferred Commerce Capabilities"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-015: Deferred Backlog Prioritization

**Task ID**: DNK-SHOPIFY-015  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 8 Deferred Backlog  

---

## 1. Executive Summary

During Waves 1-7, complex external integrations and legacy JavaScript hacks were safely deferred to ensure the stability of the core commerce runtime (Cart, PDP, PLP). This document establishes the prioritization and delivery strategy for these deferred capabilities.

---

## 2. Prioritization Matrix

| Rank | Capability | Business Value | Tech Risk | Delivery Strategy | Target Architecture |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | **Product Recommendations** | High (AOV uplift) | Low | Immediate / Wave 8.1 | Native Horizon Block + Shopify Search & Discovery API |
| **2** | **Nova Poshta Integration** | Critical (Fulfillment) | High | Mid-term / App Dev | Custom App Proxy + Checkout UI Extension |
| **3** | **Gift Rewards / Tiers** | High (Conversion) | High | Mid-term / App Dev | Shopify Functions (Cart Transform) + Admin Discounts |

---

## 3. Guiding Principles for Implementation

1. **Zero Client-Side Math**: Storefront code (Liquid/JS) must NEVER calculate prices, discounts, or shipping rates.
2. **Zero API Keys in Theme**: No secret tokens (e.g., Nova Poshta API key) shall exist in the theme bundle.
3. **Graceful Degradation**: If an app proxy or API fails, the storefront must fail gracefully with zero layout shift or blocking errors.
4. **Backend Authority**: Checkout and cart mutations are authoritative only when validated by Shopify backend systems.
