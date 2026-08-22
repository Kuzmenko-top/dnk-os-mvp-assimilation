# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK-SHOPIFY-011-PLP-METADATA-CONTRACT.md"
# purpose: "Approved Metadata Contract for PLP Product Card Merchandising Elements"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-22"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK-SHOPIFY-011: PLP Metadata Contract Specification

**Task ID**: DNK-SHOPIFY-011  
**Author**: DNK-e.com Maksym  
**Date**: 2026-08-22  
**Phase**: Wave 4A Metadata Contract Definition  

---

## 1. Approved Product Card Metadata Contracts

All PLP visual enhancements must derive strictly from approved Shopify standard objects and metafield definitions.

### A. Review Ratings Metafields
```yaml
review_rating_contract:
  rating_value:
    liquid_path: "product.metafields.reviews.rating.value.rating"
    data_type: "number / float"
    description: "Average star rating value (e.g., 4.8)"
  scale_max:
    liquid_path: "product.metafields.reviews.rating.value.scale_max"
    data_type: "number / integer"
    description: "Maximum scale value (default: 5)"
  rating_count:
    liquid_path: "product.metafields.reviews.rating_count"
    data_type: "number / integer"
    description: "Total number of verified product reviews"
  fallback_behavior: "0 DOM output if rating_value is blank"
```

### B. Swatches & Option Metadata
```yaml
swatch_metadata_contract:
  option_values:
    liquid_path: "product.options_with_values"
    swatch_map: "product_option.values | map: 'swatch'"
    data_type: "Shopify Swatch Object (color / image)"
  fallback_behavior: "0 DOM output if swatch_count == 0"
```

### C. Badge Metadata Contracts
```yaml
badge_metadata_contract:
  sold_out_badge:
    condition: "product.available == false"
    label_translation_key: "content.product_badge_sold_out"
    style_class: "color-custom-badge-sold-out"
  sale_badge:
    condition: "product.compare_at_price > product.price"
    label_translation_key: "content.product_badge_sale"
    style_class: "color-custom-badge-sale"
  forbidden_badges:
    - "Hardcoded 'Sale' / 'Bestseller' strings without Liquid condition"
    - "Frontend calculated discount percentage claims"
  fallback_behavior: "0 DOM output if neither sold_out nor sale condition is met"
```

---

## 2. Invalidation & Data Integrity Rules

1. **No Data Fabrication**: If a product has no reviews, swatches, or discount status, no fake rating or placeholder badge shall be injected.
2. **No Unapproved Metafield Namespace**: Metafields outside `product.metafields.reviews.*` or official Shopify standard namespaces are forbidden unless explicitly governance-approved.
