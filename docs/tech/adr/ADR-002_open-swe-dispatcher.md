---
mrh_id: "ADR-002"
title: "open-swe Asynchronous Task Dispatcher"
author: "DNK-e.com Maksym"
license: "MIT"
status: "Accepted"
date: "2026-08-15"
---

# ADR-002: open-swe Asynchronous Task Dispatcher

## Status
Accepted

## Context
Executing complex multi-step software engineering tasks and subagent code refactoring in DNK OS requires an isolated, non-blocking task queue capable of scheduling background agents, managing timeouts, and handling concurrent code generation routines.

## Decision
We adopt the **open-swe Dispatcher architecture (DNK-ARCH-015)** as the core asynchronous task execution layer. The dispatcher handles task distribution, execution sandboxing, and state persistence across worker threads.

## Alternatives Considered
1. **Celery + Redis Worker Queue** — Kept for simple background microservice tasks, but rejected as main agent dispatcher due to lack of native agent graph state tracking.
2. **Temporal.io** — Rejected due to high external infrastructure complexity for the baseline MVP footprint.

## Consequences
### Positive
- Seamless non-blocking agent delegation and task dispatch.
- Integrated retry logic and step-level state inspection.
- Native alignment with LangGraph multi-agent execution graphs.

### Negative
- Requires robust event loop monitoring to prevent task starvations during heavy concurrent runs.

## Dependencies
- Related Pattern: **DNK-ARCH-015 (open-swe Dispatcher)**
- Upstream Integration: **DNK-ARCH-014 (LangGraph Orchestration)**
- Downstream Resource: **DNK-ARCH-017 (vLLM Gateway)**

## Date
2026-08-15

## Owner
DNK_MENTOR / Gerych
