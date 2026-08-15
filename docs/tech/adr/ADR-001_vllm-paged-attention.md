---
mrh_id: "ADR-001"
title: "vllm PagedAttention Integration for LLM Gateway"
author: "DNK-e.com Maksym"
license: "MIT"
status: "Accepted"
date: "2026-08-15"
---

# ADR-001: vllm PagedAttention Integration for LLM Gateway

## Status
Accepted

## Context
DNK OS requires high-throughput, low-latency local LLM inference across multi-agent swarms. Standard HuggingFace Transformers inference leads to high GPU memory fragmentation, non-optimal KV-cache management, and low batch utilization during concurrent agent runs.

## Decision
We adopt **vLLM with PagedAttention (DNK-ARCH-017)** as the primary high-performance LLM inference engine in `services/llm_gateway/`. PagedAttention allows virtual memory allocation for KV-cache, enabling up to 4x throughput improvements and near-zero memory waste.

## Alternatives Considered
1. **HuggingFace TGI (Text Generation Inference)** — Rejected due to higher memory fragmentation and license constraints for custom quantization extensions.
2. **Ollama / Llama.cpp** — Kept as secondary CPU fallback adapter, but rejected for primary production GPU gateway due to performance bottlenecks under heavy concurrent batch loads.

## Consequences
### Positive
- 3x-4x increase in concurrent request capacity.
- Zero memory waste from dynamic KV-cache page allocation.
- OpenAI-compatible API endpoint out of the box.

### Negative
- Hard dependency on CUDA 12.1+ and NVIDIA GPU architecture (recorded in Tech Debt TD-001 for CPU fallback requirement).
- Increased initial VRAM overhead for memory pool reservation.

## Dependencies
- Related Pattern: **DNK-ARCH-017 (vllm PagedAttention)**
- Downstream Integration: **DNK-ARCH-014 (LangGraph Orchestration)**
- Downstream Integration: **DNK-ARCH-016 (open-webui RAG)**

## Date
2026-08-15

## Owner
DNK_MENTOR / Gerych
