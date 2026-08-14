# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/tech/specs/DNK-ARCH-017_vllm-patterns.md"
# purpose: "Architectural Patterns Extraction for vllm High-Throughput Inference in DNK OS"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

# 🏗️ DNK Architecture Spec: vllm High-Throughput Patterns (DNK-ARCH-017)

Architectural patterns extracted from `vllm-project/vllm` for implementation in `DNKOS_MVP` model proxy and inference orchestration layer.

---

## 1. System Topology

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DNK OS Application Layer                         │
│                    (Swarm Engine / Workflow Orchestrator)              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │    DNKOmniRouter Gateway    │  (Model Abstraction & Load Balancer)
                     └──────────────┬──────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           ▼                        ▼                        ▼
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│ Paged KV Cache Engine│ │ Continuous Scheduler │ │ Prefix Cache Hash    │
│ (Block Memory Pool)  │ │ (Iteration-Level Queue)│ │ (RAG System Prompts) │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

---

## 2. Key Extracted Architectural Patterns

### 2.1 Paged Memory Allocation Pattern
- **Logical-to-Physical Block Table:** Decouples prompt context length from physical GPU allocation.
- **Shared Memory Pages:** Multiple agent sessions sharing the same system prompt share physical KV blocks via reference counting.

### 2.2 Continuous Iteration-Level Request Scheduling
- Eliminates static batching constraints.
- Schedules prompts dynamically per decoding step (`prefill` vs `decode` phase priority).

### 2.3 Prefix Cache KV Reuse Pattern
- Automatic SHA-256 block hashing of system instructions and RAG grounding documents.
- Fast-path cache hit bypasses prefill compute overhead.

---

## 3. Implementation Target in `DNKOS_MVP`
- `core/model_proxy/omni_router.py` -> Integrate ModelConfig abstraction and continuous batching adapters.
- `core/memory/scones_memory.py` -> Prefix-cache hashing for recurring system prompts.
