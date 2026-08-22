# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-013-DRAFT-RUNTIME-REGRESSION.md"
# purpose: "Draft Runtime Regression Matrix Covering Cart, PDP, PLP, Pricing, and Accessibility"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-013: Draft Theme Runtime Regression Matrix

**Task ID**: DNK-SHOPIFY-013  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 6 Regression Testing  

---

## 1. Test Matrix & Execution Verification

| Test Scenario ID | Target Domain | Action / State Change | Expected Behavior | Actual Behavior | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REG-01** | Cart Drawer | Open empty cart | Display native empty cart state with CTA. Zero JS errors. | Empty state rendered, focus trapped. | **PASS** |
| **REG-02** | Cart Drawer | Add item from PDP | Cart Drawer slides open via Section Rendering API; line item added. | Section re-rendered; price total exact. | **PASS** |
| **REG-03** | Cart Drawer | Update qty / remove item | Dynamic live update; subtotal updates without full page reload. | Updated cleanly via Shopify Cart API. | **PASS** |
| **REG-04** | PDP Runtime | Switch variant swatch / dropdown | URL param `variant=` updates, price & gallery update via custom element. | Smooth variant switch; 0 layout shift. | **PASS** |
| **REG-05** | PDP Pricing | Volume pricing view | If `quantity_price_breaks` present, render native table. If empty, 0 DOM. | Table renders conditionally; 0 empty nodes. | **PASS** |
| **REG-06** | PLP Facets | Select filter checkbox | URL search params updated; product grid reloaded via Section Rendering API. | Facets synced; pagination reset. | **PASS** |
| **REG-07** | PLP Quick Add | Click Quick Add on product card | Product added to Cart Drawer; Cart Drawer opens seamlessly. | Quick add triggers Cart Drawer event. | **PASS** |
| **REG-08** | Accessibility | Keyboard navigation in Cart & Modals | Tab focus trapped in dialog; Escape key closes drawer and returns focus to trigger. | A11y dialog standards met. | **PASS** |
| **REG-09** | Performance | Network payload & listeners | Zero duplicate event listeners, native lazy loading on images (`loading="lazy"`). | No memory leaks; clean event cleanup. | **PASS** |

---

## 2. Regression Verdict

All 9 runtime test scenarios passed with **ZERO REGRESSIONS** against the native Horizon baseline.
