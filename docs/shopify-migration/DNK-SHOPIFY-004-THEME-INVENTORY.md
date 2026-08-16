# DNK-SHOPIFY-004-THEME-INVENTORY: Complete Theme Census
**Task ID**: DNK-SHOPIFY-004
**Author**: DNK-e.com Maksym
**Date**: 2026-08-16

---

## 1. Census Summary

| Category | Legacy DNK Ecom (v1.0.0) | Target Horizon / Tinker (v4.3.1) |
|---|---|---|
| **Layouts** | 2 (`theme.liquid`, `password.liquid`) | 2 (`theme.liquid`, `password.liquid`) |
| **Templates** | 24 | 13 |
| **Sections** | 103 | 44 |
| **Blocks** | 1 (legacy custom block) | 97 |
| **Snippets** | 164 | 138 |
| **JS Assets** | 50 | 162 |
| **CSS Assets** | 12 | 6 |
| **Total Artifacts** | 356 | 462 |

---

## 2. Key Observations
- Legacy theme heavily relied on custom snippets included statically inside sections.
- Target Horizon theme utilizes modular Blocks 3.0 (`blocks/`) with native `<custom-element>` JS web components.
