# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-015-IMPLEMENTATION-ROADMAP.md"
# purpose: "Implementation Roadmap for Wave 8 Deferred Capabilities"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-015: Wave 8 Implementation Roadmap

**Task ID**: DNK-SHOPIFY-015  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  

---

## 1. Wave 8 Execution Sequence

### Wave 8.1: Product Recommendations (Low Risk, Quick Win)
- **Action**: Enable and configure Shopify Search & Discovery App.
- **Theme Impact**: Minimal. Ensure `product-recommendations.liquid` is placed correctly on PDP and Cart Drawer footer.
- **Gate**: UAT verification of relevant products appearing dynamically.

### Wave 8.2: Nova Poshta Integration (High Risk, App Dev)
- **Action**: Evaluate existing Nova Poshta Shopify Apps (e.g., Nova Poshta Global, custom apps).
- **Theme Impact**: Zero Liquid changes. Ensure standard shipping fallback is configured.
- **Gate**: App installed in Staging environment; Checkout UI extension tested.

### Wave 8.3: Gift Rewards via Functions (High Risk, Custom Logic)
- **Action**: Develop or install a Shopify Functions app utilizing the Cart Transform API.
- **Theme Impact**: Update Cart Drawer UI to visually highlight line items where `price == 0` and `is_gift == true`. Remove any legacy gift JS loops.
- **Gate**: Cart threshold tests (add, remove, inventory depletion).

## 2. Dependency Management
- Wave 8.2 and 8.3 require backend access and potentially custom App development (Node.js/Remix + Rust/WASM for Functions). They are decoupled from the core Theme Migration lifecycle and should be treated as independent feature epics.
