---
name: "crewai_assimilated"
description: "SOTA indices and recipes for crewAI role-playing agents, task pipelines, and hierarchical crews."
---

# 👥 crewAI Orchestration Assimilation Index

Meta-index tracking role-based agents, task sequences, and hybrid crews.

## 📁 Core Specifications

1. **[Research & Evidence Trail](./references/RN-006_crewai-research.md)**
   - Analysis of `crewAIInc/crewAI` for persona-driven loops.

2. **[Multi-Agent Patterns](./references/DNK-ARCH-006_crewai-multi-agent-patterns.md)**
   - Hybrid graph/linear pipeline topologies and Role/Goal/Backstory models.

3. **[Component State Contracts](./references/DNK-COMP-006_crewai-interfaces.md)**
   - Python interfaces (`DNKCrewAgentPort`, `DNKCrewOrchestratorPort`).

4. **[Sandbox Execution Security](./references/DNK-SEC-006_crewai-execution-sandbox.md)**
   - Agent limits, memory caps, and task depth boundaries.

## 📁 Structure

- `scripts/` — запуск Crews та ініціалізація процесів.
- `examples/` — приклади Role-Playing сесій (scout → slice → synthesize).
- `references/` — конфігурації ролей та цілей для субагентів.
- `resources/` — діаграми взаємодії та супровідні лінки.

Основна документація:
- [RN-006](../../docs/reports/rd_assimilation/crewai/RN-006_crewai-research.md)
- [DNK-ARCH-006](../../docs/tech/specs/DNK-ARCH-006_crewai-multi-agent-patterns.md)
- [DNK-COMP-006](../../docs/tech/specs/DNK-COMP-006_crewai-interfaces.md)
- [DNK-SEC-006](../../docs/tech/standards/DNK-SEC-006_crewai-execution-sandbox.md)

## 🧪 Quick Recipes

### Recipe A: Bootstrapping a Role-Playing Sequential Crew
- Use the adapter contract inside `core/adapters/dnk_crewai_adapter.py`.
- Define rich personas (role, goal, backstory) and sequential steps:
  ```python
  from core.adapters.dnk_crewai_adapter import DNKCrewAgent, DNKCrewTask, DNKCrewOrchestrator
  scout = DNKCrewAgent(role="Scout", goal="Find files", backstory="Expert R&D specialist")
  task = DNKCrewTask(description="Scan /docs", expected_output="Files list", agent=scout)
  crew = DNKCrewOrchestrator()
  crew.add_agent(scout)
  crew.add_task(task)
  result = crew.kickoff()
  ```
