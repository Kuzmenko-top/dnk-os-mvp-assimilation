# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/tech/specs/DNK-COMP-016_open-webui-contracts.md"
# purpose: "Component Contracts for open-webui Router, Filter, and RAG Pipeline Interfaces"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

# 📄 DNK Component Contracts: open-webui Interfaces (DNK-COMP-016)

Data contracts and interface definitions for open-webui extracted components in `DNKOS_MVP`.

---

## 1. Data Contracts & Schemas

### 1.1 `ModelRequestPayload`
```python
class ModelRequestPayload(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    stream: bool = True
    valves: Dict[str, Any] = Field(default_factory=dict)
```

### 1.2 `RAGSearchQueryResult`
```python
class RAGSearchQueryResult(BaseModel):
    query: str
    dense_matches: List[Dict[str, Any]]
    sparse_matches: List[Dict[str, Any]]
    fused_results: List[Dict[str, Any]]
    latency_ms: float
```

---

## 2. Interface Contracts

### 2.1 `PipelineFilterPort`
```python
class PipelineFilterPort(ABC):
    @abstractmethod
    def inlet(self, body: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Pre-processing pipeline step before LLM invocation."""
        pass

    @abstractmethod
    def outlet(self, body: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Post-processing pipeline step after LLM response completion."""
        pass
```

### 2.2 `MultiModelRouterPort`
```python
class MultiModelRouterPort(ABC):
    @abstractmethod
    def route_request(self, payload: ModelRequestPayload) -> Any:
        pass

    @abstractmethod
    def stream_response(self, payload: ModelRequestPayload) -> Generator[str, None, None]:
        pass
```
