---
name: "langgraph_assimilated"
description: "SOTA indices and recipes for LangGraph stateful multi-agent loops and MCP adapters"
version: "2.1.0"
category: "orchestration"
author: "DNK-e.com Maksym"
triggers:
  - "langgraph"
  - "stateful graph loop"
  - "mcp adapter graph"
  - "cyclic agent orchestrator"
inputs_schema:
  type: "object"
  properties:
    messages: {type: "array"}
    thread_id: {type: "string"}
outputs_schema:
  type: "object"
  properties:
    final_state: {type: "object"}
---

# 🕸️ LangGraph & MCP Assimilation Skill

## Overview
Meta-index and operational guide for configuring stateful graph execution loops, thread-based checkpointing, and dynamic Model Context Protocol (MCP) tool adapters.

## Core Specifications
1. **[Research & Evidence Trail](../../docs/reports/rd_assimilation/langgraph/RN-004_langgraph-research.md)**
2. **[Stateful Graph Architecture](../../docs/tech/specs/DNK-ARCH-005_langgraph-multi-agent-orchestrator.md)**
3. **[Component State Contracts](../../docs/tech/specs/DNK-COMP-005_langgraph-state-contracts.md)**
4. **[Sandbox Execution Security](../../docs/tech/standards/DNK-SEC-005_langgraph-execution-sandbox.md)**

## Intent & Triggers
- Prompt triggers: `"langgraph"`, `"stateful graph loop"`, `"mcp adapter graph"`, `"cyclic agent orchestrator"`.
- Activates when building cyclic agent loops or routing complex multi-step workflows.

## Quick Recipes & Execution Flow

### Recipe A: Compiling and Running a Stateful Multi-Agent Loop
- Use adapter contract inside `core/adapters/dnk_langgraph_adapter.py`:
  ```python
  from core.adapters.dnk_langgraph_adapter import DNKLangGraphAdapter
  graph = DNKLangGraphAdapter()
  graph.add_node("agent_rick", lambda s: {"messages": ["Rick processed."]})
  graph.add_edge("agent_rick", "agent_yuriy")
  graph.compile_graph()
  final_state = graph.execute({"messages": []}, thread_id="thread_1")
  ```

### Recipe B: Mapping MCP Tool Calls in State Nodes
- Route tools registered in MCP servers dynamically through state nodes.

## Pitfalls & Error Handling
- **Infinite Cyclic Recursion**: Always enforce max recursion depth limits on graph execution instances.
- **State Reducer Mutation**: Use immutable state updates or explicit dictionary reducers to avoid concurrency race conditions.
