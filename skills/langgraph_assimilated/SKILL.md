---
name: "langgraph_assimilated"
description: "SOTA indices and recipes for LangGraph stateful multi-agent loops and MCP adapters."
---

# 🕸️ LangGraph & MCP Assimilation Index

Meta-index tracking stateful loops, checkpointing, and MCP-routing.

## 📁 Core Specifications

1. **[Research & Evidence Trail](./references/RN-004_langgraph-research.md)**
   - Analysis of `langgraph` and `langchain-mcp-adapters` for DNK OS Core.

2. **[Stateful Graph Architecture](./references/DNK-ARCH-005_langgraph-multi-agent-orchestrator.md)**
   - Loop and cyclic flow orchestration with centralized shared state.

3. **[Component State Contracts](./references/DNK-COMP-005_langgraph-state-contracts.md)**
   - Type-safe Python Pydantic ports, TypedDict schemas, and reducer definitions.

4. **[Sandbox Execution Security](./references/DNK-SEC-005_langgraph-execution-sandbox.md)**
   - Safe isolated container routing, loop caps, and resource limits.

## 📁 Structure

- `scripts/` — скрипти для роботи з графами (створення, запуск, MCP).
- `examples/` — приклади multi-agent флоу (research → plan → execute → review).
- `references/` — приклади артефактів (графи, стейт-моделі, інтеграції).
- `resources/` — додаткові матеріали, посилання, діаграми.

Основна документація:
- [RN-004](../../docs/reports/rd_assimilation/langgraph/RN-004_langgraph-research.md)
- [DNK-ARCH-005](../../docs/tech/specs/DNK-ARCH-005_langgraph-multi-agent-orchestrator.md)
- [DNK-COMP-005](../../docs/tech/specs/DNK-COMP-005_langgraph-state-contracts.md)
- [DNK-SEC-005](../../docs/tech/standards/DNK-SEC-005_langgraph-execution-sandbox.md)

## 🧪 Quick Recipes

### Recipe A: Compiling and Running a Stateful Multi-Agent Loop
- Use the adapter contract inside `core/adapters/dnk_langgraph_adapter.py`.
- Define node handlers, conditional edges, and run state:
  ```python
  from core.adapters.dnk_langgraph_adapter import DNKLangGraphAdapter
  graph = DNKLangGraphAdapter()
  graph.add_node("agent_rick", lambda s: {"messages": ["Rick processed."]})
  graph.add_edge("agent_rick", "agent_yuriy")
  graph.compile_graph()
  final_state = graph.execute({"messages": []}, thread_id="thread_1")
  ```

### Recipe B: Mapping MCP Tool Calls in State Nodes
- Expose registered MCP server tools to active orchestrators.
- Execute tool call with validation and output merge.
