# --- DNK-MRH-HEADER ---
# mrh_id: "docs/shopify-migration/DNK_SECTION_BLOCK_MAPPING.md"
# purpose: "Migration Mapping Matrix from Legacy Sections 2.0 to Horizon Blocks 3.0"
# canonical_source: true
# alters_files: []
# triggers_tasks: ["DNK-SHOPIFY-001"]
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# author: "DNK-e.com Maksym"
# --- END DNK-MRH-HEADER ---

# DNK Section & Block Migration Mapping Matrix

## 📌 Migration Strategies Legend
- `preserve`: Keep section/block as-is without structural changes.
- `extract`: Move legacy embedded section block into a standalone reusable theme block in `/blocks`.
- `adapt`: Rewrite Liquid / Schema to conform to Horizon Blocks 3.0 primitives.
- `replace`: Use existing native Horizon block without custom code.
- `manual_review`: Requires architect review before migration due to complex JS/API dependencies.

---

## 📊 Mapping Table

| Legacy Section / Block | Legacy Feature / Purpose | Target Section / Block | Migration Strategy | Risk | Notes / Dependencies |
|---|---|---|---|---|---|
| `blocks/free-shipping-progress.liquid` | Free shipping threshold progress bar | `blocks/free-shipping-progress.liquid` | `extract` | Low | Self-contained Liquid + CSS, needs cart object |
| `blocks/nova-poshta-checkout.liquid` | Nova Poshta UA branch selector | `blocks/nova-poshta-checkout.liquid` | `manual_review` | High | Depends on Nova Poshta API proxy & JS |
| `blocks/quiz-engine.liquid` | Interactive product recommendation quiz | `blocks/quiz-engine.liquid` | `adapt` | Medium | Needs quiz JSON payload & TMA event hooks |
| `blocks/social-proof-urgency.liquid` | Live visitor count & stock urgency | `blocks/social-proof-urgency.liquid` | `extract` | Low | Clean Liquid + CSS animation |
| `blocks/sticky-add-to-cart.liquid` | Sticky mobile CTA bar | `blocks/sticky-add-to-cart.liquid` | `adapt` | Medium | JS event sync with variant selector |
| `blocks/symptom-quiz.liquid` | Symptom diagnostic quiz | `blocks/symptom-quiz.liquid` | `adapt` | Medium | Integrates with `AlleDrops` quiz engine |
| `blocks/trust-badges.liquid` | Security & payment badges | `blocks/trust-badges.liquid` | `extract` | Low | Schema settings for SVG/PNG icons |
| `blocks/volume-discount-table.liquid` | Quantity break pricing table | `blocks/volume-discount-table.liquid` | `extract` | Low | Reads product price breaks / metafields |
| `sections/dnk-cro-countdown.liquid` | Countdown timer with Wise-Crafter style | `sections/dnk-cro-countdown.liquid` | `extract` | Low | Can be ported as section or theme block |
| `sections/header-announcements.liquid` | Announcement bar with multi-slide | `sections/header-announcements.liquid` | `adapt` | Medium | Horizon uses `header-announcements` section |
| `sections/header.liquid` | Main navigation & account drawer | `sections/header.liquid` | `manual_review` | High | Complex JS, sticky behavior, TMA drawer |
| `sections/product-information.liquid` | PDP product form & buy buttons | `sections/product-information.liquid` | `adapt` | Medium | Replaces rigid blocks with `content_for 'blocks'` |
| `sections/hero.liquid` | Hero banner with CTA | `sections/hero.liquid` | `replace` | Low | Native Horizon `hero.liquid` supports `@theme` |
| `sections/marquee.liquid` | Infinite scrolling text/logos | `sections/marquee.liquid` | `replace` | Low | Native Horizon `marquee.liquid` with JS |
| `sections/slideshow.liquid` | Image slideshow | `sections/slideshow.liquid` | `replace` | Low | Native Horizon `slideshow.liquid` |

---

## 🧪 Pilot Section Candidates

### Candidate 1: Simple Pilot (Recommended First Step)
- **Section / Block**: `blocks/free-shipping-progress.liquid` (or `sections/dnk-cro-countdown.liquid`)
- **Reason**: Low complexity, zero external API dependencies, clear schema, isolated CSS/JS, instant editor feedback.
- **Dependencies**: Cart object (`cart.total_price`), settings threshold.
- **Migration Risk**: Low.

### Candidate 2: Complex Pilot (Later Step)
- **Section / Block**: `sections/header.liquid` (or `blocks/nova-poshta-checkout.liquid`)
- **Reason**: Central to site navigation, high traffic impact, sticky JS, multi-level dropdowns, predictive search drawer.
- **Dependencies**: `snippets/scripts.liquid`, predictive search API, cart drawer, Nova Poshta backend proxy.
- **Migration Risk**: High.
