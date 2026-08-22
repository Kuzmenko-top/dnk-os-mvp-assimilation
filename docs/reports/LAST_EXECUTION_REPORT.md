# Architecture Note: Hermes Agent Core Orchestration
# author: "DNK-e.com Maksym"
# date: "2026-08-18"
# target: "Antigravity AI Lead Architect"

## 1. Core Architecture Overview
The Hermes Agent core orchestration layer (`core/hermes_agent/agent/`) operates as a modular, stateful cognitive engine designed for autonomous multi-turn problem solving, tool execution, context compression, and subagent swarm coordination.

## 2. Key Subsystems
1. **Conversation Execution Loop (`conversation_loop.py`)**:
   - Manages state machine across turns, model queries, streaming tokens, and prompt construction.
   - Handles mid-turn steering (`[OUT-OF-BAND USER MESSAGE]`) and iteration budgets.
2. **Unified Tool & MCP Dispatcher (`tool_executor.py`, `toolsets.py`)**:
   - Combines Native System Tools, Deferred On-Demand Tools (`tool_search`/`tool_describe`/`tool_call`), and dynamic MCP stdio/HTTP servers.
   - Enforces batch parallelism for independent tool invocations.
3. **Subagent Swarm & Delegation Engine (`delegate_task`)**:
   - Spawns background worker agents in isolated sub-processes.
   - Dynamically binds models via `router_matrix.json`.
   - Supports mid-flight steering and structured output validation (`output_schema`).
4. **Adaptive Context Compressor (`context_compressor.py`)**:
   - Protects initial context (anchor goals) and recent execution history while compressing intermediate tool payloads.
5. **Dual-Tier State & Retrieval (`state.db`, `memory_manager.py`, FTS5)**:
   - Persistent key-value memory (`user` + `memory`), session index search, and cron scheduler.
