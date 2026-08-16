# RECIPE B: Static / Repeater Content Theme Block Pattern
**Category**: Shopify Horizon Blocks 3.0 Standard Pattern
**Author**: DNK-e.com Maksym
**Date**: 2026-08-16

---

## 1. Overview & Use Case
Recipe B governs the creation of static or repeater theme blocks (such as Trust Badges, Value Propositions, Feature Cards, Policy Highlights) designed to be embedded directly into container sections (`Cart Drawer`, `PDP Information`, `Footer Utilities`, etc.).

---

## 2. Key Architecture Standards
1. **Schema Target Rules**: Do NOT use `"target": "section"` in `blocks/*.liquid`. This property is reserved for App Blocks and causes Shopify Theme Editor to hide `@theme` blocks in container section menus.
2. **Zero External Dependency**: Pure Liquid + CSS styling matching Horizon container CSS variables (`--color-background`, `--color-foreground`, `--border-radius`).
3. **Claim Evidence & Compliance Guard**:
   - Only include verified merchant guarantees (supported shipping methods, 14-day legal return policy, SSL checkout).
   - Exclude fake badges or unverified certificates.
4. **Accessibility First**:
   - Attach `{{ block.shopify_attributes }}` on the outer container element for live Theme Editor highlight.
   - Mark decorative icon/emoji spans with `aria-hidden="true"`.
