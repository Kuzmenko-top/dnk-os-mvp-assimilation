# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/HORIZON_CORE_INVENTORY.md"
# purpose: "Baseline Inventory for Target Horizon / Tinker 4.3.1 Theme Blocks 3.0 Core"
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-SHOPIFY-001"]
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# Horizon / Tinker 4.3.1 Core Inventory (Target Baseline)

## 📌 Executive Summary
- **Path**: `/Users/<username>/Kuzmenko/MY_LIFE_WORK/DNK_HUB/services/dnk_shopify/DNK_Ecom_v1_0_0`
- **Extracted Source**: `/Users/<username>/Kuzmenko/MY_LIFE_WORK/DNK_HUB/services/dnk_shopify/purchased_themes/extracted/Tinker 4.3.1`
- **Architecture**: Shopify Blocks 3.0 / Horizon Standard Core Architecture
- **Purpose**: Clean, unpolluted baseline core for theme block expansion.

---

## 📂 Component Counts
| Component Category | File Count | Description |
|---|---|---|
| **Sections** | 41 `.liquid` | Clean container sections with `content_for 'blocks'` support |
| **Theme Blocks** | 95 `.liquid` | Atomic reusable theme blocks in `/blocks` directory |
| **Snippets** | 138 `.liquid` | Core utility scripts, icons, structural helpers |
| **Templates** | 13 `.json` | Standard OS 2.0 JSON templates |
| **Assets** | 124 files | Standard Horizon CSS/JS primitives, standard-actions overrides |
| **Locales** | 51 `.json` | Standard multi-language schema files |
| **Config** | 2 `.json` | Clean `settings_schema.json` and `settings_data.json` |

---

## 🏗️ Blocks 3.0 Architecture Features
1. **Theme Blocks (`/blocks/*.liquid`)**:
   - Reusable theme blocks defined as top-level files in `/blocks`.
   - Reusable across multiple sections via schema `{"type": "@theme"}`.
   - Support for nested children blocks via `{% content_for 'blocks' %}` inside theme blocks.
2. **Section Containers**:
   - Sections render blocks dynamically using `{% content_for 'blocks' %}` instead of rigid `{% for block in section.blocks %}` loops.
   - Schema enables theme block insertion via `{"type": "@theme"}` in section schema `blocks` array.
3. **Core JS/CSS Primitives**:
   - `assets/standard-actions-override.js`: Overrides standard Shopify cart and product actions.
   - `assets/scroll-container.js`: Handles View Transitions and smooth scroll animations.
   - `snippets/scripts.liquid`: Modular JS event listeners and cart-drawer behavior initializer.

---

## 🎯 Sections Supporting Blocks 3.0 Rendering
The following 18 sections natively feature `{% content_for 'blocks' %}`:
- `_blocks.liquid`
- `featured-product-information.liquid`
- `footer-utilities.liquid`
- `footer.liquid`
- `header-announcements.liquid`
- `hero.liquid`
- `layered-slideshow.liquid`
- `main-404.liquid`
- `main-blog-post.liquid`
- `main-blog.liquid`
- `main-page.liquid`
- `marquee.liquid`
- `password.liquid`
- `product-hotspots.liquid`
- `product-information.liquid`
- `product-recommendations.liquid`
- `section.liquid`
- `slideshow.liquid`

The following 17 sections allow `@theme` blocks in their schema:
- `_blocks.liquid`, `collection-list.liquid`, `featured-product-information.liquid`, `header.liquid`, `hero.liquid`, `main-404.liquid`, `main-blog-post.liquid`, `main-blog.liquid`, `main-cart.liquid`, `main-collection-list.liquid`, `main-page.liquid`, `password.liquid`, `predictive-search.liquid`, `product-information.liquid`, `product-list.liquid`, `product-recommendations.liquid`, `section.liquid`.
