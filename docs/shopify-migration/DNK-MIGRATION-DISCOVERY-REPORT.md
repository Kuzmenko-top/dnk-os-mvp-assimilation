# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-MIGRATION-DISCOVERY-REPORT.md"
# purpose: "Canonical Discovery & Baseline Audit Report for DNK Theme Migration"
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-SHOPIFY-001"]
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK Theme Migration Discovery Report

## 📌 Repository
- **Repository**: `Kuzmenko-top/dnk-os-mvp-assimilation`
- **Branch**: `mentor/shopify/DNK-SHOPIFY-001-dnk-theme-migration-discovery`
- **Commit SHA**: `ac03847212af7e9c8cac021e89b8af8563a2682f` (Base `main`)

## 🏗️ Source Theme (Legacy)
- **Path**: `/Users/<username>/Kuzmenko/MY_LIFE_WORK/DNK_HUB/services/dnk_shopify/DNK-e.com`
- **Connected Remote**: `https://github.com/DNKShopify/DNK-e.com.git`
- **Branch**: `feature/dnk-ecom-v0.0.1-quiz-app` / `main`
- **Commit**: `c6a8051` ("feat(horizon): integrate quiz app assets into DNK Ecom v0.0.1")
- **Theme Version**: Sections 2.0 / DNK Ecom v0.0.1

## 🎯 Target Core (Horizon Blocks 3.0)
- **Path**: `/Users/<username>/Kuzmenko/MY_LIFE_WORK/DNK_HUB/services/dnk_shopify/DNK_Ecom_v1_0_0`
- **Reference Clean Extracted**: `/Users/<username>/Kuzmenko/MY_LIFE_WORK/DNK_HUB/services/dnk_shopify/purchased_themes/extracted/Tinker 4.3.1`
- **Branch**: `dnk-ecom-v0.0.1` / `main`
- **Horizon Version**: Blocks 3.0 / Tinker 4.3.1 Baseline Core

## 🔌 Shopify Connection
- **Store**: `dnk-ecom` (`dnk-ecom.myshopify.com`)
- **Connected Repository**: `DNKShopify/DNK-e.com`
- **Connected Branch**: `main` (Live Production), `staging` (Staging preview), `feature/dnk-ecom-v0.0.1-quiz-app` (Unpublished development validation theme)
- **Validation Theme**: Unpublished Theme (Development Preview)
- **Production Touched**: `NO`

## 📊 Inventory Summary
- **Legacy Sections**: 41
- **Legacy Theme Blocks**: 103 (includes 8 custom DNK blocks)
- **Legacy Snippets**: 138
- **Legacy Templates**: 13
- **Legacy Assets**: 126
- **Target Sections**: 41
- **Target Theme Blocks**: 95 (clean core baseline)
- **Target Private Blocks**: 0
- **Target Snippets**: 138

## ⚠️ Migration Risks
- **Schema Risks**: Transitioning from nested section blocks to top-level theme blocks requires updating `{% schema %}` to include `{"type": "@theme"}` and creating individual `/blocks/*.liquid` files.
- **Liquid Risks**: Replacing `{% for block in section.blocks %}` with `{% content_for 'blocks' %}` requires ensuring proper Liquid context variables are passed to child blocks.
- **JavaScript Risks**: Section-specific event listeners (e.g. in `header.liquid` or `sticky-add-to-cart.liquid`) must be decoupled from section IDs and attached via standard event delegation.
- **App Block Risks**: Apps like `@app` blocks must be preserved in section schemas to prevent breaking installed Shopify apps.
- **Metafield Risks**: Custom metafield references (`custom.specifications`, `custom.shipping_lead_time`) must be mapped to schema settings.
- **Settings Migration Risks**: `settings_data.json` preset values must be aligned between legacy and target schemas.

## 🧪 Pilot Recommendation
- **Simple Candidate**: `blocks/free-shipping-progress.liquid` (or `sections/dnk-cro-countdown.liquid`)
  - *Why*: Isolated Liquid component, clear cart price threshold dependencies, low risk, high CRO value.
  - *Expected Manual Work*: Port Liquid markup, verify cart JS update hooks, register schema.
- **Complex Candidate**: `sections/header.liquid`
  - *Why*: Essential site navigation, multi-level dropdowns, TMA drawer, sticky scroll JS.
  - *Expected Manual Work*: Decouple menu rendering, test predictive search drawer, verify responsive breakpoints.

## ⛔ Not Implemented
- No production deployment performed.
- No live theme files modified or published.
- No mass conversion or bulk renaming executed.
- No merge to `main` branch.
