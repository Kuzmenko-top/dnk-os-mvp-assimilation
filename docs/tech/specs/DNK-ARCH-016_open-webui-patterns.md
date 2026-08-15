# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/tech/specs/DNK-ARCH-016_open-webui-patterns.md"
# purpose: "Architectural Patterns Extraction for open-webui Integration into DNK OS Visual Shell & RAG Core"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

# 🏗️ DNK Architecture Spec: open-webui Patterns (DNK-ARCH-016)

Architectural patterns extracted from `open-webui/open-webui` for implementation in `DNKOS_MVP` Visual Shell, OmniRouter, and Deep RAG subsystems.

---

## 1. System Topology

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DNK OS Visual Shell Frontend                    │
│                     (Chat-Driven UI / Generative UI)                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼  (SSE / WebSocket Stream)
                     ┌─────────────────────────────┐
                     │    DNKOmniRouter Gateway    │  (Multi-Model Proxy & Valves)
                     └──────────────┬──────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           ▼                        ▼                        ▼
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│  DNK Deep RAG 2.0    │ │  DNK Tool Pipeline   │ │ DNK Auth & Sessions  │
│ (Hybrid Search Engine│ │(Valves/Filters/Tools)│ │ (JWT / RBAC Control) │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

---

## 2. Key Extracted Architectural Patterns

### 2.1 Filter & Valve Pipeline Pattern
- Middleware chain wrapping LLM invocations:
  - `Pre-Filter`: Sanitize prompt, insert user memory/context, attach RAG grounding chunks.
  - `Model Invocation`: Dispatch to target model via OmniRouter.
  - `Post-Filter`: Format markdown, validate JSON schemas, log telemetry metrics.

### 2.2 Dynamic Multi-Model Gateway
- Abstract endpoint handling request transformations:
  - Standardizes payload schemas across Vertex AI, OpenAI, Anthropic, and local Ollama nodes.
  - Provides automatic retry and fallback model routing upon API errors.

### 2.3 Hybrid Dense/Sparse RAG Pipeline
- Two-stage retrieval:
  1. Semantic dense search using embedding distance.
  2. Lexical keyword filtering using BM25.
  3. Reciprocal Rank Fusion (RRF) combining top results before prompt injection.

---

## 3. Implementation Target in `DNKOS_MVP`
- `core/model_proxy/omni_router.py` -> Add Filter/Valve pipeline support.
- `services/dnk_canvas_api/` -> Adopt SSE/WebSocket token streaming.
- `core/memory/` -> Integrate Hybrid RAG retrieval patterns.
