# --- DNK-MRH-HEADER ---
# mrh_id: "DNKOS_MVP/docs/tech/specs/DNK-COMP-017_vllm-contracts.md"
# purpose: "Component Contracts for vllm Scheduler, Block Manager, and Engine Primitives"
# author: "DNK-e.com Maksym"
# license: "MIT"
# canonical_source: true
# alters_files: []
# triggers_tasks: []
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# --- END DNK-MRH-HEADER ---

# 📄 DNK Component Contracts: vllm Interfaces (DNK-COMP-017)

Data contracts and interface definitions for vllm extracted inference primitives in `DNKOS_MVP`.

---

## 1. Data Contracts & Schemas

### 1.1 `InferenceRequestPayload`
```python
class InferenceRequestPayload(BaseModel):
    request_id: str
    prompt: str
    model_name: str
    sampling_params: Dict[str, Any]  # temperature, top_p, max_tokens
    block_size: int = 16
    enable_prefix_caching: bool = True
```

### 1.2 `KVCacheBlockMeta`
```python
class KVCacheBlockMeta(BaseModel):
    block_id: int
    ref_count: int
    hash_key: str
    is_gpu: bool = True
```

---

## 2. Interface Contracts

### 2.1 `IterationSchedulerPort`
```python
class IterationSchedulerPort(ABC):
    @abstractmethod
    def schedule_next_step(self) -> Dict[str, Any]:
        """Selects active prefill and decode sequences for the next GPU iteration."""
        pass

    @abstractmethod
    def add_request(self, request: InferenceRequestPayload) -> None:
        pass
```

### 2.2 `BlockManagerPort`
```python
class BlockManagerPort(ABC):
    @abstractmethod
    def allocate_blocks(self, num_blocks: int) -> List[KVCacheBlockMeta]:
        pass

    @abstractmethod
    def free_blocks(self, block_ids: List[int]) -> None:
        pass
```
