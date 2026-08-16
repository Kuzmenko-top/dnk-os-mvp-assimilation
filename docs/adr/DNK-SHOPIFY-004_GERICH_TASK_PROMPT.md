# DNK-SHOPIFY-004 — Full Theme Molecular Graph & Horizon/Tinker Migration Blueprint

## Mission

You are **GERYCH Shopify Theme Migration Squad**. Execute a discovery-first, evidence-driven architectural analysis that establishes the correct foundation for migrating the legacy **DNK eCom** Shopify theme into the new **DNK eCom Horizon 3.0 / Tinker** architecture.

Your goal is **not** to generate another isolated Liquid block. Your goal is to reconstruct the functional model of both themes, build a machine-readable molecular code graph, identify native Horizon extension points, and produce a controlled migration blueprint that preserves verified DNK business capabilities while adopting Horizon as the runtime owner.

The output must become a reusable knowledge base for the DNK Theme Migration Service being developed in DNK OS.

---

## Architectural Context

### Source system

- Legacy DNK eCom theme: established production-grade functionality.
- It contains valuable sections, snippets, assets, Cart Drawer modules, business rules, and UX behavior that must be discovered before migration.
- The legacy Cart Drawer is a pinned global section located between header and template content. It composes multiple snippets/modules and is opened/updated by cart-related interactions.

### Target system

- Target: DNK eCom built on Shopify **Horizon / Tinker**, using modern Theme Blocks architecture.
- Canonical theme delivery repository: `DNKShopify/DNK-e.com`.
- Canonical remote: `shopify_github`.
- Active delivery branch: `feature/01-tinker-analysis`.
- Current canonical HEAD: `b1067eac176e0150e5869f5f4ee3cb96635dfce9`.
- Store: `dnk-ecom.myshopify.com`.
- Theme mode: draft only.

### Non-negotiable principle

```text
Legacy DNK theme = functional specification and source of capability evidence.
Horizon/Tinker = platform runtime, lifecycle owner, and architectural baseline.
DNK compatibility layer = controlled migration boundary.
```

Do **not** clone the legacy Cart Drawer shell blindly into Horizon.
Do **not** migrate isolated snippets before proving their host/runtime contract.
Do **not** replace native Horizon behavior unless evidence proves that a safe extension path does not exist.

---

## Primary Objective

Create a complete architecture package that answers, with evidence:

1. What capabilities exist in the legacy DNK eCom theme?
2. How are they connected at Liquid, JavaScript, DOM, Cart API, CSS, configuration, and data-source levels?
3. What are the equivalent or extensible components in Horizon/Tinker?
4. Which legacy capabilities should be preserved, adapted, rewritten, replaced with native Horizon, deferred, or excluded?
5. What is the correct implementation strategy for the DNK Cart Drawer in Horizon?
6. What migration waves minimize runtime and commercial risk?

---

## Scope: Discovery and Architecture Only

### Allowed

- Read and analyze all accessible documentation.
- Read legacy and target theme source trees in full.
- Use the dedicated Shopify Theme Migration Squad.
- Use Gemini Flash for repository inventory, dependency extraction, graph construction, candidate mapping, and document drafting.
- Use Shopify documentation and Horizon/Tinker source/documentation as primary target references.
- Run read-only Git commands and static validation commands.
- Inspect the draft theme in Shopify Admin for architecture and validation evidence, without publishing.
- Create local analysis artifacts and governance documentation only after repository/branch rules are verified.

### Forbidden in this phase

```yaml
theme_code_changes: forbidden
new_theme_commits: forbidden
theme_push: forbidden
force_push: forbidden
theme_publish: forbidden
production_touched: false
production_published: false
```

Do not create new feature blocks, modify Cart Drawer Liquid, change JavaScript, or alter the theme schema during this task.

---

## Preflight: Resolve Sources Before Analysis

Before analyzing, provide a source-resolution table:

| Role | Required evidence |
|---|---|
| Legacy theme root | Exact absolute local path and Git identity, if any |
| Target theme root | Exact absolute local path and Git identity |
| Shopify delivery repository | `DNKShopify/DNK-e.com` |
| Delivery remote | `shopify_github` |
| Delivery branch | `feature/01-tinker-analysis` |
| Draft theme | Exact Shopify Admin theme name and connected repository/branch |
| Working fork | Identify `Kuzmenko-top/m-craft.top` only as non-canonical unless proven otherwise |

Run and report read-only Git evidence for the target:

```bash
git remote -v
git branch --show-current
git status --short
git rev-parse HEAD
git log --oneline --decorate -10
git ls-remote shopify_github refs/heads/feature/01-tinker-analysis
```

If roots, remotes, or branch identities are ambiguous, stop and report `BLOCKED_SOURCE_IDENTITY`. Do not make assumptions.

---

## Workstream A — Complete Theme Census

Analyze both theme trees, including:

```text
layout/
templates/
templates/customers/
sections/
blocks/
snippets/
assets/
config/
locales/
```

Produce an inventory for each theme with counts and paths for:

- Liquid layouts, templates, sections, blocks, snippets.
- JavaScript assets, modules, custom elements, and entry points.
- CSS assets, component styles, tokens, and selector coupling.
- Schema settings, presets, block declarations, app blocks, dynamic sources.
- Liquid objects, metafields, metaobjects, and settings references.
- External URLs, apps, CDNs, analytics integrations, and APIs.
- Claims relating to payment, delivery, returns, certificates, discounts, security, urgency, or social proof.

Static extraction must identify at minimum:

```text
{% render %}
{% include %}
{% section %}
{% sections %}
{% content_for %}
{% form %}
{% paginate %}
{% liquid %}
asset_url
section.settings
block.settings
settings.*
metafields
metaobjects
/cart.js
/cart/add.js
/cart/change.js
/cart/update.js
section rendering requests
addEventListener
dispatchEvent
CustomEvent
querySelector/querySelectorAll
customElements.define
```

---

## Workstream B — Molecular Code Graph

Build two full graphs and one migration graph:

```text
1. Legacy DNK eCom molecular graph
2. Horizon/Tinker molecular graph
3. Legacy → Horizon migration map
```

### Required node types

```yaml
node_types:
  - layout
  - template
  - section
  - theme_block
  - section_block
  - snippet
  - asset_js
  - asset_css
  - custom_element
  - liquid_object
  - schema_setting
  - metafield
  - metaobject
  - endpoint
  - dom_selector
  - browser_event
  - cart_mutation
  - external_service
  - app_dependency
  - claim
  - capability
```

### Required edge types

```yaml
edge_types:
  - renders
  - includes
  - imports
  - styles
  - reads
  - writes
  - listens_to
  - emits
  - mutates
  - replaces
  - requires
  - exposes
  - calls
  - depends_on
  - conflicts_with
  - maps_to
```

### Required node fields

```yaml
id: "stable logical id"
type: "node type"
path: "repository-relative path when applicable"
name: "human-readable name"
role: "runtime or business role"
source_theme: "legacy | horizon"
runtime_criticality: "low | medium | high | critical"
evidence:
  - "line references, command output references, or documentation source"
```

### Required edge fields

```yaml
source: "node id"
target: "node id"
type: "edge type"
evidence: "static or runtime evidence"
confidence: "high | medium | low"
```

For every runtime-critical capability, prove a traceable flow:

```text
User trigger
  → browser event or form submit
  → JavaScript/custom element
  → Shopify/Liquid/API data source
  → cart mutation or render request
  → section/DOM replacement mechanism
  → resulting UX state
```

Do not infer runtime behavior only from filenames. Mark unproven edges as `confidence: low` and list the validation required.

---

## Workstream C — Cart Drawer Foundation

Cart Drawer is the priority subgraph and the first migration vertical slice.

### Legacy discovery requirements

Identify and map:

- Exact layout insertion point: prove how the drawer is pinned between header and template/main content.
- Drawer host section/snippet, DOM root, overlay, dialog, close control, accessibility behavior.
- Every entry point: header cart icon, add-to-cart, quick-add, product form, upsell, quantity controls, other triggers.
- Every Liquid render relation and all dependent snippets.
- Every JS module/custom element/event/selector tied to the drawer.
- Every Cart API endpoint and section-rendering update path.
- Full lifecycle: initial load → open → add → cart refresh → quantity update → remove → empty cart → close → reopen.
- CSS dependencies and hard-coded selectors.
- Cart-specific capabilities: shipping progress, payment methods, delivery UI, trust badges, discount display, upsells, legal copy.

### Horizon/Tinker discovery requirements

Identify and map:

- Actual native Cart Drawer files and their location in the installed target version.
- Native drawer host/custom elements, event contracts, re-render contract, AJAX lifecycle, selectors, and accessibility handling.
- What Horizon owns and what is supported for extension.
- Whether a stable merchant-configurable extension zone already exists.
- Whether a `@theme` block acceptance plus `{% content_for 'blocks' %}` pattern is safe and compatible at the identified host.
- Version-specific constraints and anything that must not be overridden.

### Cart Drawer decision framework

Recommend exactly one default strategy, with evidence:

```yaml
cart_drawer_strategy:
  - EXTEND_NATIVE_HORIZON
  - DNK_COMPATIBILITY_ADAPTER
  - FULL_DNK_REPLACEMENT
```

`FULL_DNK_REPLACEMENT` is allowed only if the report demonstrates that native Horizon cannot safely support the required functional contract. It requires a separate mentor decision and must not be implemented in this task.

The expected default is `DNK_COMPATIBILITY_ADAPTER`:

```text
Native Horizon Cart Drawer owns:
- drawer shell
- lifecycle
- cart mutation flow
- DOM replacement/re-render logic
- focus and accessibility primitives

DNK adapter owns:
- compatibility mapping
- approved extension zones
- initialization of DNK enhancements after native rendering
- feature-specific presentation modules
- migration telemetry/evidence hooks
```

---

## Workstream D — Compatibility Matrix

Create a row for every legacy capability, not merely every file.

### Required decisions

```yaml
allowed_decisions:
  - PRESERVE
  - ADAPT
  - REWRITE
  - REPLACE_WITH_HORIZON_NATIVE
  - DEFER
  - EXCLUDE
```

### Required schema per capability

```yaml
capability_id: "stable id"
legacy_sources: []
business_outcome: "customer/store outcome"
entrypoints: []
data_authority: "Shopify cart | Shopify checkout | Shopify Functions | app | metafield | theme display | unknown"
data_sources: []
runtime_dependencies: []
cart_mutation_behavior: "none | add_to_cart | quantity_update | remove | update | unknown"
dom_contract: []
legacy_risk: "low | medium | high | critical"
horizon_native_equivalent: "path/component or none"
horizon_extension_point: "path/contract or none"
recommended_target_type: "native | adapter | theme_block | section | snippet | app | excluded"
recommended_target_path: "proposed path or N/A"
decision: "PRESERVE | ADAPT | REWRITE | REPLACE_WITH_HORIZON_NATIVE | DEFER | EXCLUDE"
rationale: "evidence-based reason"
validation_scenarios: []
blockers: []
```

### Price, discount, and claim governance

- Theme code may present data but must not become the source of truth for checkout price or discounts.
- Any discount/volume price promise without checkout authority must be `DISPLAY_ONLY / MANUAL_REVIEW`, `DEFER`, or `EXCLUDE`.
- Any certificate, delivery, payment, return, security, urgency, or social-proof claim must include its evidence source.
- Claims without factual/legal/configuration evidence must be rewritten, removed, or excluded.

---

## Workstream E — Migration Blueprint

Create a dependency-aware migration plan. The plan must prioritize runtime foundations before presentation details.

### Mandatory migration waves

| Wave | Scope | Exit criteria |
|---|---|---|
| 0 | Theme census, molecular graphs, contracts | Complete evidence package; no untracked critical entrypoints |
| 1 | Cart Drawer foundation | Approved native/adapter strategy and complete drawer subgraph |
| 2 | Cart Drawer modules | Verified progress, trust, payment/delivery presentation modules |
| 3 | Product conversion runtime | Product form, variants, quantity/price contracts, volume logic |
| 4 | Content and merchandising | Reusable sections, cards, editorial components, collections |
| 5 | Integrations | Nova Poshta, apps, external data, recommendations/upsells |
| 6 | Regression and cutover | Draft parity evidence, rollback plan, production go/no-go |

For every wave provide:

```yaml
wave_id: "0..6"
objective: "..."
prerequisites: []
components: []
implementation_pattern: "native | adapter | theme block | section | app"
risks: []
validation: []
rollback_boundary: "..."
definition_of_done: []
```

---

## Required Deliverables

Create the following artifacts in the governance workspace according to its branch rules. Do not write to the theme delivery branch in this phase.

```text
docs/shopify-migration/DNK-SHOPIFY-004-THEME-INVENTORY.md
docs/shopify-migration/DNK-SHOPIFY-004-LEGACY-MOLECULAR-GRAPH.md
docs/shopify-migration/DNK-SHOPIFY-004-HORIZON-MOLECULAR-GRAPH.md
docs/shopify-migration/DNK-SHOPIFY-004-CART-DRAWER-FOUNDATION-SPEC.md
docs/shopify-migration/DNK-SHOPIFY-004-COMPATIBILITY-MATRIX.md
docs/shopify-migration/DNK-SHOPIFY-004-MIGRATION-BLUEPRINT.md
docs/shopify-migration/graphs/legacy-theme.graph.json
docs/shopify-migration/graphs/horizon-theme.graph.json
docs/shopify-migration/graphs/cart-drawer.graph.json
docs/shopify-migration/graphs/migration-map.graph.json
docs/handoffs/HANDOFF_DNK-SHOPIFY-004_<YYYY-MM-DD>.md
```

Use a dedicated governance branch:

```text
mentor/shopify/DNK-SHOPIFY-004-theme-molecular-graph
```

Before creating the branch, confirm the governance repository identity, default base branch, working-tree cleanliness, and remote reconciliation. Push governance documentation only after an explicit branch/push authorization if the operating procedure requires it.

---

## Final Report Format

Return a concise structured report first, followed by links/paths to evidence:

```yaml
task_id: DNK-SHOPIFY-004
status: COMPLETED | PARTIALLY_COMPLETED | BLOCKED
phase: discovery_and_architecture

source_identity:
  legacy_theme_root: "..."
  target_theme_root: "..."
  target_repository: DNKShopify/DNK-e.com
  target_remote: shopify_github
  target_branch: feature/01-tinker-analysis
  target_head: "..."

inventory:
  legacy:
    layouts: 0
    templates: 0
    sections: 0
    blocks: 0
    snippets: 0
    js_assets: 0
    css_assets: 0
  horizon:
    layouts: 0
    templates: 0
    sections: 0
    blocks: 0
    snippets: 0
    js_assets: 0
    css_assets: 0

graphs:
  legacy_nodes: 0
  legacy_edges: 0
  horizon_nodes: 0
  horizon_edges: 0
  migration_mappings: 0
  unproven_critical_edges: []

cart_drawer:
  legacy_entrypoint: "..."
  legacy_pinned_placement_proven: true | false
  horizon_entrypoint: "..."
  native_extension_points: []
  recommended_strategy: EXTEND_NATIVE_HORIZON | DNK_COMPATIBILITY_ADAPTER | FULL_DNK_REPLACEMENT
  rationale: "..."
  blockers: []

migration_summary:
  preserve: 0
  adapt: 0
  rewrite: 0
  replace_with_horizon_native: 0
  defer: 0
  exclude: 0
  recommended_next_wave: "..."

safety:
  theme_code_changed: false
  theme_commits_created: false
  theme_push_performed: false
  production_touched: false
  production_published: false

evidence_paths: []
mentor_decisions_required: []
```

---

## Definition of Done

This task is complete only when all conditions below are met:

- Both theme roots and delivery/governance repository identities are proven.
- Full theme census exists for legacy and Horizon/Tinker.
- Graph JSON is valid and includes all runtime-critical Cart Drawer nodes and edges.
- Cart Drawer pinned placement in legacy is proven with path/line evidence.
- Native Horizon Cart Drawer contract is mapped from the actual target version, not assumed.
- Every legacy Cart Drawer module has a compatibility decision and target recommendation.
- All price/discount/legal-claim risks are explicitly classified.
- Migration waves contain prerequisites, validation, rollback boundary, and DoD.
- No theme code has changed; no theme commit or push has occurred; production remains untouched.

---

## Operating Principle

```text
Do not migrate files.
Migrate verified capabilities.

Do not replace Horizon runtime by default.
Extend it through controlled, documented boundaries.

Do not trust an AI-generated mapping without static and runtime evidence.
Every critical claim must be traceable to code, configuration, documentation, or draft-theme validation.
```
