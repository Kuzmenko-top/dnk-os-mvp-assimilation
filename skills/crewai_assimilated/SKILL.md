---
name: "crewai_assimilated"
description: "SOTA indices and recipes for crewAI role-playing agents, task pipelines, and hierarchical crews"
version: "2.1.0"
category: "orchestration"
author: "DNK-e.com Maksym"
triggers:
  - "crewai"
  - "role playing crew"
  - "task pipeline crew"
  - "agent backstory persona"
inputs_schema:
  type: "object"
  properties:
    tasks: {type: "array"}
    agents: {type: "array"}
outputs_schema:
  type: "object"
  properties:
    result: {type: "string"}
---

# 👥 crewAI Orchestration Assimilation Skill

## Overview
Meta-index and operational guide for configuring role-based subagent personas (Role, Goal, Backstory), task pipelines, and hierarchical crews.

## Core Specifications
1. **[Research & Evidence Trail](../../docs/reports/rd_assimilation/crewai/RN-006_crewai-research.md)**
2. **[Multi-Agent Patterns](../../docs/tech/specs/DNK-ARCH-006_crewai-multi-agent-patterns.md)**
3. **[Component State Contracts](../../docs/tech/specs/DNK-COMP-006_crewai-interfaces.md)**
4. **[Sandbox Execution Security](../../docs/tech/standards/DNK-SEC-006_crewai-execution-sandbox.md)**

## Intent & Triggers
- Prompt triggers: `"crewai"`, `"role playing crew"`, `"task pipeline crew"`, `"agent backstory persona"`.
- Activates when creating persona-driven agent teams with sequential or hierarchical delegation.

## Quick Recipes & Execution Flow

### Recipe A: Bootstrapping a Role-Playing Sequential Crew
- Use adapter contract inside `core/adapters/dnk_crewai_adapter.py`:
  ```python
  from core.adapters.dnk_crewai_adapter import DNKCrewAgent, DNKCrewTask, DNKCrewOrchestrator
  scout = DNKCrewAgent(role="Scout", goal="Find files", backstory="Expert R&D specialist")
  task = DNKCrewTask(description="Scan /docs", expected_output="Files list", agent=scout)
  crew = DNKCrewOrchestrator()
  crew.add_agent(scout)
  crew.add_task(task)
  result = crew.kickoff()
  ```

## Pitfalls & Error Handling
- **Persona Context Pollution**: Keep backstory prompts clean and structured to avoid token window over-saturation.
- **Unbounded Delegation Loops**: Limit task retry attempts and max iteration counts on subagents.
