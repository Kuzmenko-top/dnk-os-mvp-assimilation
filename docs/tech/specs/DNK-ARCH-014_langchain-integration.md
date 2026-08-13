# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/tech/specs/DNK-ARCH-014_langchain-integration.md"
# purpose: "Architecture Specification for LangChain LCEL Integration into DNK OS Hexagonal Core"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

# 🏗️ DNK Architecture Spec: LangChain Integration (DNK-ARCH-014)

Architecture specification for embedding LangChain Expression Language (LCEL) chains, runnable components, and tool bindings into DNK OS MVP.

---

## 1. System Context & Hexagonal Topology

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DNK OS Application Layer                         │
│   (Swarm Engine / Workflow Orchestrator / Canvas API / Agent Factory)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │     DNKLangChainPort        │  (Hexagonal Port Interface)
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │    DNKLangChainAdapter      │  (Concrete LCEL Adapter)
                     └──────────────┬──────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           ▼                        ▼                        ▼
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│  LCEL Chain Engine   │ │  DNKLangGraphAdapter │ │ OmniRouter & SCONES  │
│ (Runnables/Parsers)  │ │   (Graph Node Integration) │ (Telemetry/Memory)  │
└──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

---

## 2. Core Architectural Components

### 2.1 `DNKLangChainPort` (Interface)
Defines the contract for creating and executing LCEL chains:
- `create_chain(prompt_template, model_name, output_parser)` -> `DNKLCELChain`
- `invoke_chain(chain_id, input_data, config)` -> `Dict[str, Any]`
- `register_tool(tool_fn, name, description)` -> `Dict[str, Any]`
- `bind_tools_to_chain(chain_id, tools)` -> `DNKLCELChain`

### 2.2 `DNKLangChainAdapter` (Adapter Implementation)
Implements `DNKLangChainPort`:
- Wraps native or mocked LCEL runnables (`RunnableSequence`, `RunnableParallel`, `RunnablePassthrough`).
- Manages execution metrics, error distillation via `ErrorDistiller`, and fallback retries.
- Translates input payloads and formats output objects into structured domain DTOs.

### 2.3 Integration with `DNKLangGraphAdapter`
- Provides `as_graph_node(chain_id)` method to wrap an LCEL chain as a standard LangGraph state graph node callable `(state: DNKGraphState) -> Dict[str, Any]`.
- Ensures seamless state progression, checkpointing, and error distillation during graph node execution.

---

## 3. Non-Functional Requirements & Security
- **Path Hygiene:** Uses relative paths (`DNKOS_MVP/core/adapters/...`).
- **Telemetry:** Fires `RuntimeEvent` for chain start, step execution, and completion.
- **Fail-Safety:** Catches exceptions and converts them to distilled error memories without crashing parent processes.
