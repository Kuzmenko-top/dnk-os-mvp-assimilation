# author: "DNK-e.com Maksym"
# ADR-001: vLLM PagedAttention Integration

## Status
Accepted

## Context
High-throughput LLM inference requires efficient memory management for key-value caches.

## Decision
We adopt vLLM with PagedAttention as our core inference engine.

## Alternatives Considered
1. HuggingFace Transformers native pipeline (high latency, KV cache fragmentation)
2. Ollama REST wrapper (limited concurrency control)

## Consequences
### Positive
- ✅ 3x-5x higher token generation throughput
- ✅ Reduced memory fragmentation

### Negative
- ⚠️ Higher initial GPU memory reservation

## Dependencies
- CUDA 12.1+
- PyTorch 2.3+

## Date
2026-08-15

## Owner
DNK OS Governance Team
