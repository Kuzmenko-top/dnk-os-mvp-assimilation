# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK_THEME_INVENTORY.md"
# purpose: "Comprehensive Baseline Inventory for Legacy DNK-e.com Sections 2.0 Theme"
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-SHOPIFY-001"]
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-e.com Legacy Theme Inventory (Baseline Audit)

## 📌 Executive Summary
- **Path**: `/Users/<username>/Kuzmenko/MY_LIFE_WORK/DNK_HUB/services/dnk_shopify/DNK-e.com`
- **Git Branch**: `feature/dnk-ecom-v0.0.1-quiz-app` (commit `c6a8051`) / `main` (`ffa0b79`)
- **Connected Repository**: `DNKShopify/DNK-e.com` & `Kuzmenko-top/m-craft.top`
- **Architecture**: Online Store 2.0 / Horizon 0.0.1 hybrid theme

---

## 📂 Component Counts
| Component Category | File Count | Description |
|---|---|---|
| **Sections** | 41 `.liquid` | Core layout sections and container wrappers |
| **Theme Blocks** | 103 `.liquid` | Reusable and section-specific theme blocks (8 custom DNK blocks) |
| **Snippets** | 138 `.liquid` | Micro-components, icons, helpers, and JS loaders |
| **Templates** | 13 `.json` | OS 2.0 page, product, collection, cart, and index templates |
| **Assets** | 126 files | CSS (`.css`), JS (`.js`), fonts, and SVGs |
| **Locales** | 51 `.json` | Internationalization schema files |
| **Config** | 2 `.json` | `settings_schema.json` and `settings_data.json` |

---

## 🧬 Custom DNK E-Commerce Extensions & Blocks (8 Extra Theme Blocks)
The legacy theme contains 8 custom theme blocks developed specifically for DNK CRO, funnels, and logistics:

1. `blocks/free-shipping-progress.liquid` — Dynamic free shipping threshold calculation progress bar.
2. `blocks/nova-poshta-checkout.liquid` — Nova Poshta Ukrainian branch picker and shipping widget.
3. `blocks/quiz-engine.liquid` — Interactive product recommendation quiz container.
4. `blocks/social-proof-urgency.liquid` — Live visitor count, recent purchase notifications, stock urgency timer.
5. `blocks/sticky-add-to-cart.liquid` — Sticky mobile CTA bar with variant selector.
6. `blocks/symptom-quiz.liquid` — Specialized symptom/need diagnostic quiz flow.
7. `blocks/trust-badges.liquid` — Custom security badges, guarantees, payment icons block.
8. `blocks/volume-discount-table.liquid` — Quantity break / tier discount table block.

---

## 🎯 Custom Sections & Enhanced Liquid Components
- `sections/dnk-cro-countdown.liquid` — Custom countdown timer with Wise-Crafter theme styling.
- `sections/header.liquid` — Multi-level navigation, account drawer, predictive search, TMA mobile drawer integration.
- `sections/header-announcements.liquid` — Multi-bar announcement slider with timer.
- `sections/main-collection.liquid` — AJAX filtering, collection grid, and sorting.
- `sections/search-results.liquid` — Predictive search & filter integration.

---

## ⚙️ Config & Metafields Usage
- **Settings Schema**: `config/settings_schema.json` defines brand colors, typography, cart type (drawer vs page), animation settings.
- **Settings Data**: `config/settings_data.json` contains theme presets and active merchant configurations.
- **Metafield Namespaces Used**:
  - `custom.specifications`
  - `custom.badges`
  - `custom.shipping_lead_time`
  - `custom.quiz_mapping`
  - `shop.metafields.dnk`

---

## 🛡️ App Blocks (`@app`) & Theme Block Support
- **Sections supporting `@app` blocks**: `product-information.liquid`, `featured-product-information.liquid`, `main-page.liquid`.
- **Sections supporting `content_for 'blocks'`**: 18 sections (`hero.liquid`, `footer.liquid`, `marquee.liquid`, `slideshow.liquid`, `product-information.liquid`, etc.).
- **Sections supporting `{"type": "@theme"}`**: 17 sections (`header.liquid`, `collection-list.liquid`, `product-list.liquid`, `main-cart.liquid`, etc.).
