# author: "DNK-e.com Maksym"
# ADR-003: Open WebUI RAG Pipeline

## Status
Accepted

## Context
Local-first knowledge retrieval requires hybrid dense/sparse search over pgvector.

## Decision
Adopt Open WebUI RAG pipeline integrated with pgvector shadow recall.

## Alternatives Considered
1. External SaaS vector store (violates sovereignty)
2. Qdrant standalone container (deprecated, replaced by pgvector)

## Consequences
### Positive
- ✅ Zero external data leaks
- ✅ Single source of truth in PostgreSQL

### Negative
- ⚠️ Vector index compilation load during initial ingest

## Dependencies
- PostgreSQL 16 + pgvector
- Google GenAI Embeddings API

## Date
2026-08-15

## Owner
DNK OS Governance Team
