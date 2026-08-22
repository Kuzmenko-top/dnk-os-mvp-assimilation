# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-013-ROLLOUT-AND-ROLLBACK-PLAN.md"
# purpose: "Step-by-Step Staging Rollout and Instant Rollback Playbook"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-013: Rollout and Rollback Plan

**Task ID**: DNK-SHOPIFY-013  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 6 Release Preparation  

---

## 1. Staging & Release Rollout Sequence

1. **Step 1: Staging Preview Validation (Draft Mode)**
   - Maintain theme in unpublished draft state on `dnk-ecom.myshopify.com`.
   - Run end-to-end user journeys (Cart, PDP, PLP, Search, Checkout handoff).
2. **Step 2: Backup Current Live Theme**
   - Download/duplicate existing live theme as `LIVE_BACKUP_YYYY-MM-DD` prior to publish.
3. **Step 3: Staging to Production Promotion**
   - Merge `feature/01-tinker-analysis` to release branch upon final human authorization.
   - Publish draft theme in Shopify Admin.
4. **Step 4: Post-Publish Smoke Tests**
   - Verify live Cart Drawer open/add/checkout.
   - Verify analytics events (page_view, add_to_cart, begin_checkout).

---

## 2. Instant Rollback Playbook

In the event of an unexpected live checkout failure or critical bug:

1. **Trigger Condition**: Any checkout interruption or critical storefront rendering error.
2. **Immediate Action**:
   - In Shopify Admin -> Online Store -> Themes: Click **Publish** on `LIVE_BACKUP_YYYY-MM-DD`.
   - Reversion to previous stable theme occurs in < 5 seconds.
3. **Post-Mortem**:
   - Isolate defect in draft theme copy.
   - Log incident in governance repository under `docs/reports/incidents/`.
