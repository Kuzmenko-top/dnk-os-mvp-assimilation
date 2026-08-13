# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-ARCH-013_google-skills-integration"
# purpose: "Architecture specification for google/skills standard integration in DNK OS"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-MRH-HEADER ---

# DNK-ARCH-013: Google Skills Architecture Specification

## 1. System Topology & Skill Lifecycle

```
+-------------------------------------------------------------------+
|                        Skill Registry / Manager                   |
|  - Parse Frontmatter YAML (name, version, triggers, schema)       |
|  - Validate Markdown Section Integrity                            |
|  - Intent Matching & Dynamic Skill Selection                      |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                         Skill Directory                           |
|  /skills/<skill_name>/                                            |
|    ├── SKILL.md  (YAML Frontmatter + Structural Sections)         |
|    ├── scripts/  (Executable helpers)                            |
|    ├── examples/ (Usage recipes)                                  |
|    ├── references/ (Architectural links)                          |
|    └── resources/ (Assets and schemas)                            |
+-------------------------------------------------------------------+
```

## 2. Structural Governance Rules
1. **Frontmatter Validation**:
   - `name`: Match folder name (`^[a-z0-9_]+$`).
   - `version`: Semantic version string (`X.Y.Z`).
   - `triggers`: Non-empty list of string keywords/regexes.
   - `category`: Skill taxonomy classification.

2. **Required Markdown Headings**:
   - `# <Skill Name>`
   - `## Overview`
   - `## Core Specifications`
   - `## Intent & Triggers`
   - `## Input / Output Contracts`
   - `## Quick Recipes & Execution Flow`
   - `## Pitfalls & Error Handling`

## 3. Integration with SkillManager
- `SkillManager` dynamically inspects `DNKOS_MVP/skills/*/SKILL.md`.
- Evaluates triggers against incoming agent context before loading skill content.
