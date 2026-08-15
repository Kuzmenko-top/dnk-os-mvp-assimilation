---
mrh_id: "TECH-DEBT-LEDGER"
title: "DNK OS Tech Debt Ledger"
author: "DNK-e.com Maksym"
license: "MIT"
status: "Active"
date: "2026-08-15"
---

# DNK OS Tech Debt Ledger

## TD-001: vllm CUDA Dependency
- **Date:** 2026-08-15
- **Source:** DNK-ARCH-017
- **Debt:** `vllm` requires CUDA 12.1+ and physical NVIDIA GPUs, but DNK OS targets support for lightweight CPU-only developer environments.
- **Impact:** Cannot execute high-speed local inference gateway on CPU-only edge nodes or macOS local dev without cloud GPU remote forwarding.
- **Payoff Plan:** Create CPU fallback adapter (ONNX Runtime / llama.cpp GGML runner) by Q4 2026.
- **Owner:** Gerych
- **Status:** Open

## TD-002: open-webui Lacks LangGraph State Integration
- **Date:** 2026-08-15
- **Source:** DNK-ARCH-016
- **Debt:** open-webui RAG pipeline executes standalone RAG routines without injecting state back into DNK OS LangGraph (DNK-ARCH-014).
- **Impact:** Inconsistent orchestration patterns between chat UI interactions and autonomous multi-agent swarm state graphs.
- **Payoff Plan:** Implement custom LangGraph execution middleware and state adapter by Q3 2026.
- **Owner:** Gerych
- **Status:** Open

## TD-003: Subagent Isolation Environment Sandboxing
- **Date:** 2026-08-15
- **Source:** DNK-ARCH-015
- **Debt:** open-swe dispatcher executes subagent routines in shared local process contexts when Docker sockets are unavailable.
- **Impact:** Potential filesystem crosstalk between concurrent subagent tasks during high-throughput R&D runs.
- **Payoff Plan:** Enforce strict rootless Podman / Docker zero-host process isolation wrapper across all dispatcher workers by Q4 2026.
- **Owner:** Gerych
- **Status:** Open
