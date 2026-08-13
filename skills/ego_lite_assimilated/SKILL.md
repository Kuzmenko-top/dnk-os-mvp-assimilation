---
name: "ego_lite_assimilated"
description: "Assimilated patterns and components from langchain-ai/ego-lite CDP browser automation"
version: "1.1.0"
category: "research"
author: "DNK-e.com Maksym"
triggers:
  - "ego lite"
  - "cdp browser automation"
  - "browser session reattachment"
  - "ego browser adapter"
inputs_schema:
  type: "object"
  properties:
    command: {type: "string"}
outputs_schema:
  type: "object"
  properties:
    snapshot: {type: "string"}
---

# 🌐 ego-lite Assimilated Skill

## Overview
This skill incorporates SOTA architectural patterns and codebases from LangChain's ego-lite CDP browser-automation architecture.

## Core Specifications
1. **[Research & Evidence Trail](../../docs/reports/rd_assimilation/ego_lite/RN-003_ego-lite-research.md)**
2. **[CDP Browser Architecture](../../docs/tech/specs/DNK-ARCH-003_ego-lite-cdp.md)**
3. **[Component State Contracts](../../docs/tech/specs/DNK-COMP-003_ego-lite-interfaces.md)**
4. **[Sandbox Execution Security](../../docs/tech/standards/DNK-SEC-003_ego-lite-sandbox.md)**

## Intent & Triggers
- Prompt triggers: `"ego lite"`, `"cdp browser automation"`, `"browser session reattachment"`, `"ego browser adapter"`.
- Activates when building Chrome DevTools Protocol (CDP) browser automation helpers or managing task space sessions.

## Quick Recipes & Execution Flow

### Recipe A: Initializing Ego Browser Adapter
```python
from core.adapters.ego_browser_adapter import DNKEgoBrowserAdapter

adapter = DNKEgoBrowserAdapter()
adapter.start()
print(adapter.get_snapshot())
adapter.stop()
```

## Pitfalls & Error Handling
- **CDP Session Loss**: Auto-reattachment requires periodic heartbeat health checks against Chrome CDP endpoint.
- **Host System Pollution**: Always execute browser headless sessions inside isolated Docker containers.
