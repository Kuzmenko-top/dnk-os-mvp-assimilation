# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-014-STAGING-UAT-PLAN.md"
# purpose: "Staging and User Acceptance Testing (UAT) Execution Plan for Horizon Release Candidate"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-014: Staging / UAT Plan

**Task ID**: DNK-SHOPIFY-014  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 7 Staging & UAT RC  

---

## 1. Staging Verification Objectives

The purpose of this UAT plan is to execute a rigorous, non-destructive validation of the Horizon draft theme (`feature/01-tinker-analysis` @ `99d43eeaae315832033feffd2d850021f1624b6c`) across core customer journeys prior to any production publication decision.

---

## 2. Testing Roles and Governance Protocol

- **Session Owner / Lead Mentor**: `DNK_MENTOR_SHOPIFY`
- **Builder / Swarm Manager**: `Gerych`
- **Merchant Evaluator / QA**: `DNK-e.com Maksym`
- **Publish Authorization Policy**: `STRICT_MANUAL_GATE` — Production publish is forbidden without an explicit, standalone `PUBLISH: YES` confirmation.

---

## 3. Core Customer Journey Test Protocols

```text
Journey 1: Discovery & Browse (PLP)
  ├── Filter by availability, price range, variant options
  ├── Sort by Featured, Price Low-High, Price High-Low, Best Selling
  ├── Quick Add interaction from grid card
  └── Pagination / infinite scroll validation

Journey 2: Evaluation & Configuration (PDP)
  ├── Variant swatch switching & URL parameter sync (?variant=...)
  ├── Dynamic price & compare-at-price updates
  ├── Volume pricing table rendering (only when quantity_price_breaks present)
  ├── Add-to-cart form submission
  └── Zero layout shift & responsive gallery inspection

Journey 3: Conversion & Checkout (Cart Drawer)
  ├── Slide-in drawer on cart mutation
  ├── Free shipping threshold milestone bar
  ├── Line item quantity adjustment and removal
  └── Checkout button handoff ensuring all attributes and line items persist intact
```
