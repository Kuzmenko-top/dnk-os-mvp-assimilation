# --- DNK-MRH-HEADER ---
# mrh_id: "RN-013_google-skills-research"
# purpose: "Research report on google/skills standard assimilation for DNK OS Skill Architecture"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---

# RN-013: Google Skills Specification Research Report

## 1. Overview & Context
This report analyzes the `google/skills` open standard for agent procedural knowledge representation. The purpose of assimilating `google/skills` into DNK OS is to establish a deterministic, machine-parsable, and type-safe skill standard across all agent domain masters and subagent swarms.

## 2. Key Findings & Standard Requirements
1. **Extended YAML Frontmatter Schema**:
   - Required keys: `name`, `description`, `version`, `category`, `tags`, `author`, `triggers` (intent patterns), `inputs_schema`, `outputs_schema`.
2. **Structural Markdown Sectioning**:
   - Every `SKILL.md` must present standardized headings:
     - `# <Title>`
     - `## Overview`
     - `## Core Specifications`
     - `## Intent & Triggers`
     - `## Input / Output Contracts`
     - `## Quick Recipes & Execution Flow`
     - `## Pitfalls & Error Handling`
3. **Trigger & Intent Matching Engine**:
   - Skills are selected via semantic trigger matching against user prompts or orchestrator task descriptions.
4. **Directory Layout Hygiene**:
   - Mandatory subdirectories for complex skills: `scripts/`, `examples/`, `references/`, `resources/`.

## 3. Integration Plan for DNKOS_MVP
- **`DNK-SKILL-STD-001`**: Draft canonical skill assimilation standard document.
- **Skill Upgrades**: Update `open_canvas_assimilated`, `langgraph_assimilated`, and `crewai_assimilated` to comply 100% with `DNK-SKILL-STD-001`.
- **Validation Engine**: Implement automated test suite in `tests/verification/test_google_skills_standard.py` to enforce compliance across all skills in the repository.

## 4. Impact & Benefit Analysis
- **Zero Ambiguity**: Declarative schemas for skill inputs and outputs prevent hallucinated argument passing.
- **Automated Routing**: Intent triggers allow `OmniRouter` and `SkillManager` to dynamically load the exact skill needed for a subtask.
