---
mrh_id: "ADR-003"
title: "open-webui RAG Pipeline & Knowledge Interface"
author: "DNK-e.com Maksym"
license: "MIT"
status: "Accepted"
date: "2026-08-15"
---

# ADR-003: open-webui RAG Pipeline & Knowledge Interface

## Status
Accepted

## Context
DNK OS users and developers require a unified visual interface and RAG (Retrieval-Augmented Generation) pipeline for interacting with the assimilated knowledge graph, documentation, and live system state.

## Decision
We integrate the **open-webui RAG pipeline (DNK-ARCH-016)** as the standard human-agent chat interface and knowledge query gateway. It connects directly to the vector store / hybrid retrieval engine (Shadow Recall 2.0).

## Alternatives Considered
1. **Custom Streamlit / Gradio UI** — Rejected due to lack of production-grade authentication, role-based access control, and rich document chat features.
2. **AnythingLLM** — Rejected due to rigid internal RAG pipeline structure that prevented custom LangGraph graph hooks.

## Consequences
### Positive
- Production-ready user interface out of the box with multi-modal chat support.
- Flexible web search and RAG collection management.

### Negative
- Currently lacks native LangGraph graph state integration (recorded in Tech Debt TD-002).

## Dependencies
- Related Pattern: **DNK-ARCH-016 (open-webui RAG)**
- Upstream Gateway: **DNK-ARCH-017 (vLLM PagedAttention)**
- Vector Backend: **Hybrid Recall Engine (BM25 + Dense Vector)**

## Date
2026-08-15

## Owner
DNK_MENTOR / Gerych
