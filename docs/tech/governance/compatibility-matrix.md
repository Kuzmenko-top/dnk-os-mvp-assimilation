---
mrh_id: "COMPATIBILITY-MATRIX"
title: "DNK OS Technology Stack Compatibility Matrix"
author: "DNK-e.com Maksym"
license: "MIT"
status: "Active"
date: "2026-08-15"
---

# DNK OS Compatibility Matrix

## Technology Stack Compatibility

| Component | Python | CUDA | Ray | LangGraph | FastAPI | Notes |
|-----------|--------|------|-----|-----------|---------|-------|
| **DNK OS Core Baseline** | 3.12 | Optional | No | Yes | Yes | Baseline system requirement |
| **DNK-ARCH-014 (langchain/langgraph)** | 3.10+ | N/A | No | Yes | Yes | ✅ Fully Compatible |
| **DNK-ARCH-015 (open-swe dispatcher)** | 3.11+ | N/A | Optional | Yes | Yes | ✅ Fully Compatible |
| **DNK-ARCH-016 (open-webui rag)** | 3.10+ | Optional | No | No | Yes | ⚠️ Lacks native LangGraph graph adapter |
| **DNK-ARCH-017 (vllm paged-attention)** | 3.9+ | 12.1+ | Required | No | Yes | ❌ Requires CUDA 12.1+ / GPU node |

## Action Items & Tech Debt Roadmap
- [ ] **TD-001 (DNK-ARCH-017):** Implement CPU fallback adapter (ONNX Runtime / Llama.cpp) for non-GPU nodes (Target: Q4 2026)
- [ ] **TD-002 (DNK-ARCH-016):** Build custom LangGraph execution hook for open-webui RAG agent pipeline (Target: Q3 2026)
