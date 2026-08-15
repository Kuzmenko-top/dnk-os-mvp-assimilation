---
mrh_id: "PATTERN-CATALOG"
title: "DNK OS Pattern Catalog"
author: "DNK-e.com Maksym"
license: "MIT"
status: "Active"
date: "2026-08-15"
---

# DNK OS Pattern Catalog

## DNK-ARCH-014: LangGraph Multi-Agent Orchestration
- **Source:** `langchain-ai/langgraph` / `open-swe`
- **Type:** Multi-agent state machine and execution graph
- **Status:** Active
- **Integration Point:** `core/orchestrator/`
- **Dependencies:** Python 3.10+, `langgraph>=0.2.0`
- **Description:** Stateful multi-agent workflow graph manager that enables dynamic routing, agent state persistence, and human-in-the-loop branching.

## DNK-ARCH-015: open-swe Task Dispatcher
- **Source:** `langchain-ai/open-swe`
- **Type:** Asynchronous worker queue & execution dispatcher
- **Status:** Active
- **Integration Point:** `core/orchestrator/dispatcher.py`
- **Dependencies:** Python 3.11+, asyncio runtime
- **Description:** Non-blocking async dispatcher for spawning, monitoring, and harvesting output from isolated subagents and tool execution tasks.

## DNK-ARCH-016: open-webui RAG Pipeline
- **Source:** `open-webui/open-webui`
- **Type:** Retrieval-Augmented Generation & Human Chat UI
- **Status:** Active
- **Integration Point:** `services/dnk_docs_portal/`
- **Dependencies:** Python 3.10+, FastAPI, Vector Database (Shadow Recall 2.0)
- **Description:** User-facing frontend and documentation RAG interface providing web search, document ingestion, and conversational AI.

## DNK-ARCH-017: vllm PagedAttention Gateway
- **Source:** `vllm-project/vllm`
- **Type:** High-throughput GPU LLM inference engine
- **Status:** Active
- **Integration Point:** `services/llm_gateway/`
- **Dependencies:** CUDA 12.1+, PyTorch 2.1+, `vllm>=0.6.0`
- **Description:** PagedAttention-powered inference server optimizing KV-cache VRAM usage for concurrent multi-agent inference calls.
