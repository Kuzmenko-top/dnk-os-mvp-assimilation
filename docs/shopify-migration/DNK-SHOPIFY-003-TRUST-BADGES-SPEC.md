# DNK-SHOPIFY-003-TRUST-BADGES-SPEC: Trust Badges Theme Block Specification
**Task ID**: DNK-SHOPIFY-003
**Task Slug**: trust-badges-cart-drawer-horizon-compatibility
**Author**: DNK-e.com Maksym
**Date**: 2026-08-16
**Pattern**: Recipe B (Static / Repeater Content Block)

---

## 1. Audit & Claim Evidence Matrix

| Badge / Claim | Legacy source | Real Evidence / Proof | Resolution |
|---|---|---|---|
| **Payment Method Icons** | `blocks/payment-icons.liquid` | Native `shop.enabled_payment_types` in Shopify Admin | **Preserve** / Render dynamic SVGs or custom icons |
| **Nova Poshta Delivery** | Legacy snippet `cart-checkpoints-bar.liquid` | Active store shipping provider (Nova Poshta) | **Preserve** / Configurable badge with icon + text |
| **14 Days Money Back / Return** | Legacy snippet `moneybackcheckcart.liquid` | Consumer Rights Policy (14 days return law / store policy) | **Preserve** / Configurable badge |
| **SSL Secure Payment** | Legacy copy ("100% Guarantee") | Shopify SSL & PCI-DSS 256-bit Checkout Encryption | **Rewrite** to clean text ("Безпечна оплата SSL") |
| **Unverified Certificates** | Legacy copy ("Official Certification") | No verifiable legal certificate attached | **Exclude** (per governance rule) |

---

## 2. Block Architecture Specification (`blocks/trust-badges.liquid`)

- **Block Type**: `@theme` Theme Block (`blocks/trust-badges.liquid`)
- **Integration Target**: `Cart drawer` (`sections/cart-drawer-section.liquid`) via `{% content_for 'blocks' %}`
- **Dependencies**: Native Liquid, CSS Grid/Flexbox primitives, zero external JavaScript or third-party tracking scripts.
- **Accessibility**:
  - `{{ block.shopify_attributes }}` attached to custom element or container.
  - Decorative icons `aria-hidden="true"`.
  - Alt text for badge images.

---

## 3. Schema Structure & Customizer Options
- **Optional Heading**: E.g., "Чому обирають нас"
- **Layout**: Columns range (1 to 4) / responsive grid.
- **Badge 1..4 Settings**:
  - `icon_1_emoji` / `icon_1_image`
  - `title_1`
  - `text_1`
  - `url_1`
