# author: "DNK-e.com Maksym"
# ADR-004: LangGraph State Contract Orchestrator

## Status
Accepted

## Context
Complex multi-agent workflows require checkpointing and stateful DAG branching.

## Decision
Use LangGraph as stateful orchestrator core.

## Alternatives Considered
1. Custom async task queue (high maintenance)
2. Celery / RabbitMQ (overkill for agentic DAGs)

## Consequences
### Positive
- ✅ Built-in state persistence and time-travel debugging
- ✅ Native async state transitions

### Negative
- ⚠️ State schema migration overhead

## Dependencies
- LangGraph 0.1+
- FastAPI 0.110+

## Date
2026-08-15

## Owner
DNK OS Governance Team
