# --- DNK-MRH-HEADER ---
# mrh_id: "DNK-SKILL-STD-001_skills-assimilation"
# purpose: "Canonical governance standard for skill creation, assimilation, and verification across DNK OS"
# author: "DNK-e.com Maksym"
# license: "MIT"
# status: "Active"
# version: "1.0.0"
# updated_at: "2026-08-13"
# --- END DNK-SKILL-STD-001 ---

# DNK-SKILL-STD-001: Skills Assimilation & Governance Standard

## 1. Scope & Objective
This standard defines the mandatory structure, metadata format, sectioning, and verification rules for all procedural skills integrated into `DNKOS_MVP/skills/`.

## 2. Mandatory Rules for SKILL.md Files

### Rule 2.1: YAML Frontmatter Requirements
Every `SKILL.md` must start with a valid YAML frontmatter block containing:
- `name`: String matching folder name (`skills/<name>/SKILL.md`).
- `description`: String summarizing purpose.
- `version`: Semver string (e.g. `1.0.0`, `2.0.0`).
- `category`: Category string (e.g. `research`, `orchestration`, `ui`, `devops`).
- `author`: String attribution (default: `DNK-e.com Maksym`).
- `triggers`: Non-empty list of trigger keyphrases for intent matching.

### Rule 2.2: Structural Markdown Sections
Every `SKILL.md` MUST contain the following 6 section headings:
1. `# <Skill Name>`
2. `## Overview`
3. `## Core Specifications`
4. `## Intent & Triggers`
5. `## Quick Recipes` (or `## Quick Recipes & Execution Flow`)
6. `## Pitfalls & Error Handling`

### Rule 2.3: Relative Path Hygiene
- Links to internal specifications must use relative markdown links (`../../docs/tech/specs/...`).
- No absolute host file paths (`/Users/<username>/...`) allowed.

### Rule 2.4: Verification Compliance
All skills in `DNKOS_MVP/skills/` are validated automatically by `tests/verification/test_google_skills_standard.py`.
