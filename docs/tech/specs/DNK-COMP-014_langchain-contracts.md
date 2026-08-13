# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/tech/specs/DNK-COMP-014_langchain-contracts.md"
# purpose: "Component & Data Contracts for LangChain Adapter Primitive Interfaces in DNK OS"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

# 📄 DNK Contracts Spec: LangChain Components & Interfaces (DNK-COMP-014)

Formal interfaces and state schemas for `DNKLangChainAdapter` and cross-adapter compatibility.

---

## 1. Data Contracts (Schemas & DTOs)

### 1.1 `ChainExecutionRequest`
```python
class ChainExecutionRequest(BaseModel):
    chain_id: str
    tenant_id: str = "default"
    workspace_id: str = "default"
    inputs: Dict[str, Any]
    config: Optional[Dict[str, Any]] = None
```

### 1.2 `ChainExecutionResult`
```python
class ChainExecutionResult(BaseModel):
    chain_id: str
    status: str  # "success", "failed", "fallback"
    output: Dict[str, Any]
    duration_ms: float
    error: Optional[str] = None
```

### 1.3 `ToolDefinitionSpec`
```python
class ToolDefinitionSpec(BaseModel):
    name: str
    description: str
    parameters_schema: Dict[str, Any]
```

---

## 2. Interface Contracts

### 2.1 `LangChainPort` (Abstract Port)
```python
class LangChainPort(ABC):
    @abstractmethod
    def create_chain(
        self, chain_id: str, prompt_template: str, model_name: str = "default"
    ) -> Any:
        pass

    @abstractmethod
    def invoke_chain(
        self, request: ChainExecutionRequest
    ) -> ChainExecutionResult:
        pass

    @abstractmethod
    def register_tool(
        self, name: str, description: str, func: Callable
    ) -> ToolDefinitionSpec:
        pass

    @abstractmethod
    def wrap_as_graph_node(
        self, chain_id: str
    ) -> Callable[[Any], Dict[str, Any]]:
        pass
```

---

## 3. LangGraph Cross-Adapter State Contract

When an LCEL chain is wrapped as a node for `DNKLangGraphAdapter`, it consumes and returns updates on `DNKGraphState`:
- **Input mapping:** Reads `state.messages` or `state.initial_data`.
- **Output mutation:** Returns a dictionary update to be merged into `DNKGraphState` state dictionary (e.g., `{"messages": [output_msg], "status": "running"}`).
