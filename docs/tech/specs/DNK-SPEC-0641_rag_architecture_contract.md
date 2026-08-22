# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-SPEC-0641_rag_architecture_contract.md"
# purpose: "Define Phase 0 RAG Architecture Contract, canonical DTOs, multi-tenant isolation, and EmbeddingProvider SPI."
# canonical_source: true
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-14"
# author: "DNK-e.com Maksym"
# license: "MIT"
# --- END DNK-MRH-HEADER ---

# 🧠 RAG ARCHITECTURE & MULTI-TENANT ISOLATION CONTRACT (DNK-IMPL-006 PHASE 0)

This specification defines the canonical Data Transfer Objects (DTOs), security invariants, provider interfaces, and multi-tenant isolation requirements for the **DNK OS Knowledge Base & RAG Subsystem** under task `DNK-IMPL-006`.

---

## 📐 1. Canonical Data Schemas (DTOs)

All RAG operations, storage interfaces, and retrieval query engines MUST strictly conform to the following dataclass/Pydantic schemas:

```yaml
Document:
  document_id: str         # Deterministic UUID or URI slug
  tenant_id: str           # Trusted tenant UUID
  workspace_id: str        # Trusted workspace UUID
  source_type: str         # e.g., "markdown", "pdf", "code", "notion"
  source_uri: str          # URI or relative path
  checksum: str            # SHA-256 hash of document payload
  version: str             # Document version string
  metadata: dict           # Structural metadata (author, created_at, tags)

Chunk:
  chunk_id: str            # Deterministic hash (e.g. SHA-256 of doc_id + ordinal + content)
  document_id: str         # Parent Document UUID
  tenant_id: str           # Trusted tenant UUID
  workspace_id: str        # Trusted workspace UUID
  ordinal: int             # 0-indexed position within document
  content: str             # Text payload
  content_checksum: str    # SHA-256 hash of chunk content
  metadata: dict           # Chunk-level metadata

Embedding:
  embedding_id: str        # Deterministic UUID
  chunk_id: str            # Associated Chunk UUID
  provider: str            # e.g., "openai", "vertex", "huggingface", "mock"
  model: str               # Model identifier string
  dimensions: int          # Embedding vector length (e.g., 1536)
  vector: list[float]      # Float list vector
  created_at: str          # ISO-8601 timestamp

RetrievalQuery:
  query: str               # User query string
  tenant_id: str           # Trusted tenant UUID (from Request Context)
  workspace_id: str        # Trusted workspace UUID (from Request Context)
  top_k: int               # Max results count (default: 5, max: 100)
  filters: dict            # Optional metadata/category filters
  retrieval_mode: str      # "hybrid", "dense", "sparse"

RetrievalResult:
  chunk_id: str            # Chunk UUID
  document_id: str         # Parent Document UUID
  score: float             # Relevance similarity score [0.0 - 1.0]
  retrieval_method: str    # "dense_pgvector", "sparse_bm25", "hybrid"
  content: str             # Text payload
  provenance: dict         # Provenance info (doc_uri, ordinal, tenant_id, workspace_id)
  metadata: dict           # Chunk & Document metadata
```

---

## 🔒 2. Security & Multi-Tenant Invariants

1. **Trusted Request Context Only**: `tenant_id` and `workspace_id` MUST be sourced exclusively from trusted request context or JWT claims. Prompt contents or user-controlled metadata parameters MUST NEVER override tenant/workspace scope.
2. **Mandatory Vector Partition Filter**: Every pgvector similarity query or similarity calculation MUST explicitly include `WHERE tenant_id = :tenant_id AND workspace_id = :workspace_id`.
3. **Fail-Closed Workspace Enforcement**: Missing `tenant_id` or `workspace_id` in a query context raises `ValueError("Missing workspace scope context")` and terminates execution immediately.
4. **Cross-Tenant Contamination Prevention**: A chunk belonging to Workspace A MUST NEVER be returned to Workspace B under any circumstances, even if both chunks share identical text or embedding vectors.
5. **Idempotent Document Lifecycle**: Re-ingesting a document with matching `document_id` and `version` MUST be idempotent (replacing or skipping duplicate chunk creation without orphaned vectors).
6. **Authorization Isolation**: Embedding provider SPI components have zero authority to alter retrieval authorization or bypass tenant scoping filters.
7. **Secret Scrubbing**: Raw secrets, API keys, and sensitive tokens MUST be scrubbed prior to document chunking and vector indexing.
8. **Provenance Tracking**: Every `RetrievalResult` MUST contain complete provenance metadata detailing document URI, ordinal position, checksum, and tenant/workspace claims.

---

## 🔌 3. Embedding Provider SPI Protocol

All embedding models must implement the provider-neutral `EmbeddingProvider` protocol:

```python
from typing import Protocol, List

class EmbeddingProvider(Protocol):
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding vector for single text payload."""
        ...

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embedding vectors for batch of text payloads."""
        ...

    def model_name(self) -> str:
        """Return provider model identifier."""
        ...

    def dimensions(self) -> int:
        """Return vector dimension size."""
        ...
```

---
**Approved by:** Antigravity AI & DNK_MENTOR_KNOWLEDGE  
**Enforced by:** DNK OS RAG Core Engine  
